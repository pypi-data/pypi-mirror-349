import os
import requests
import httpx
import asyncio
import time
import nest_asyncio
import jwt
import json
from json import JSONDecodeError
from typing import Optional, Dict
from datetime import date, datetime
from ipylab import JupyterFrontEnd, Panel, SplitPanel
from ipywidgets import widgets, Layout, HBox
from IPython import display 

from kudaf_extension.auth import feide_oauth2
from kudaf_extension.utils import (
    get_internal_jupyter_process_details,
    safe_file_open_wb, 
    safe_file_open_w,
    parse_content_disposition_header,
)
       

class KudafNotebook:
    """
    This class handles the Jupyter Notebook UI and Events for the Kudaf project
    """   
    def __init__(self):
        # App settings
        self.ksettings = {}
        self.jupyter_process = get_internal_jupyter_process_details()
        auth_header = self.jupyter_process.get('auth_header_str')
        self.request_header = {"Authorization": auth_header} if auth_header else {}

        # Grab also an instance of the Auth module
        self.auth = feide_oauth2

        # Global variables
        self.granted_variables = {}
        self.fetch_variables = []
        self.download_query_params = {}

        # Set up a nested Event Loop, needed to be able to nest async 
        # calls within Jupyter's runnig Tornado loop
        # (Thus we avoid having to set up a separate web server on a different port)
        nest_asyncio.apply()
        loop = asyncio.get_event_loop()

        self.loop = loop 

        # JupyterFrontend app
        self.frontend_app = JupyterFrontEnd()

        ### Kudaf Top Menu Bar UI components ###
        self.kudaf_login_button = widgets.Button(
            description='Enable Kudaf', 
            button_style='warning',
            icon="toggle-off", 
            tooltip='Click me to log into Feide'
        )
        self.kudaf_login_status_checkbox = widgets.Checkbox(
            value=False,
            description='Logged Out',
            disabled=True,
            indent=False
        )
        self.kudaf_display_button = widgets.Button(
            description='Granted Variables', 
            button_style='warning',
            icon="cart-arrow-down", 
            tooltip='Click me to display and download your granted Kudaf variables',
            disabled=False,
        )
        self.logged_out_toppanel_box_children = [
            self.kudaf_login_button, 
            self.kudaf_login_status_checkbox,
        ]
        self.logged_in_toppanel_box_children = [
            self.kudaf_login_button, 
            self.kudaf_login_status_checkbox,
            self.kudaf_display_button,
        ]
        self.top_buttons_box = HBox(self.logged_out_toppanel_box_children)

        top_inline_panel = Panel()
        top_inline_panel.children = [self.top_buttons_box]
        top_inline_panel.layout = Layout(overflow='hidden')
        self.top_inline_panel = top_inline_panel

        # Toggle flag to detect the presence of the top inline panel
        self.top_inline_panel_present = False

        ## Split-panel components ##
        split_panel = SplitPanel()
        split_panel.title.label = 'Kudaf Panel'
        split_panel.title.closable = True
        self.split_panel = split_panel

        # Add button on-click behavior
        self.kudaf_login_button.on_click(self.on_login_button_clicked)
        self.kudaf_display_button.on_click(self.on_display_button_clicked)

    def run(self, base_browser_url: Optional[str] = None):
        # Establish basic Notebook settings
        base_url = self.jupyter_process.get('base_url')


        # Establish Notebook settings dict from App config
        self.ksettings = self.get_kudaf_settings(base_url=base_url)

        # Update some settings if not same as given
        new_settings = {}

        if self.ksettings.get('base_url') != base_url:
            self.ksettings['base_url'] = base_url
            new_settings.update({"base_url": base_url,})
            
        if base_browser_url is not None and self.ksettings.get('base_browser_url') != base_browser_url:
            self.ksettings['base_browser_url'] = base_browser_url
            new_settings.update({"base_browser_url": base_browser_url,})

        if self.ksettings.get('jupyter_process') != self.jupyter_process:
            self.ksettings['jupyter_process'] = self.jupyter_process
            new_settings.update({"jupyter_process": self.jupyter_process,})

        if new_settings:
            self.update_kudaf_settings(
                new_settings=new_settings,
                base_url=base_url,
            )

        # Show Top Inline Panel with Kudaf Button
        if not self.top_inline_panel_present:
            self.frontend_app.shell.add(self.top_inline_panel, 'top')
            self.top_inline_panel_present = True
      
    def on_login_button_clicked(self, result):
        ksettings = self.ksettings
        if ksettings.get('access_token') and \
            not self.auth.is_expired(datetime.fromisoformat(ksettings.get('access_token_expires'))):
            print("Already logged in, until {}".format(ksettings.get('access_token_expires')))
            return
        
        # Start log-in process
        status_code = self.loop.run_until_complete(self.feide_login())
        still_busy = True
        while still_busy:
            # Refresh settings dict
            ksettings = self.get_kudaf_settings(base_url=ksettings.get('base_url'))
            # if ksettings.get('jwt_token') is not None:
            if ksettings.get('jupyter_token') is not None:
                still_busy = False
                # if isinstance(ksettings.get('jwt_token'), dict):
                if isinstance(ksettings.get('jupyter_token'), dict):
                    print('LOGIN ERROR: {} - Details: {}'.format(
                        # ksettings.get('jwt_token').get('error'), ksettings.get('jwt_token').get('error_description')
                        ksettings.get('jupyter_token').get('error'), ksettings.get('jupyter_token').get('error_description')
                    ))
                    # Abort here, don't try to retrieve variables
                    return None
            else:
                time.sleep(1)
                print("Still waiting for the login process...\n")

        # Successful log-in -> Keep Tokens safe in this running Notebook instance only
        self.ksettings = ksettings  
        print("SUCCESSFUL LOGIN - NOTEBOOK KSETTINGS: {}".format(self.ksettings))
        # Delete access tokens from served settings
        self.update_kudaf_settings(
            new_settings={
                'access_token': "",
                'jupyter_token': "",
            },
            base_url=ksettings.get('base_url'),
        )
        # self.delete_kudaf_settings_tokens()

        # Change login button
        self.kudaf_login_button.description = "Kudaf enabled"
        self.kudaf_login_button.button_style = "success"
        self.kudaf_login_button.icon = "toggle-on"

        # Change Feide login checkbox
        self.kudaf_login_status_checkbox.description = "Logged In"
        self.kudaf_login_status_checkbox.value = True

        # Modify top panel box to add display button
        self.top_buttons_box.children = self.logged_in_toppanel_box_children

        # Print Granted Applications
        self.granted_applications = self.loop.run_until_complete(self.get_granted_applications())
        print("============================================================")
        print('KUDAF APPLICATIONS GRANTED: \n{}'.format(self.granted_applications))
        print("============================================================")


    def on_display_button_clicked(self, result):
        if not self.granted_applications:
            print("No granted applications in Kudaf")
            return None
        
        # Grab split panel
        split_panel = self.split_panel
        
        # Build split-panel UI
        application_titles = []
        applications_children = []
        
        for title, application_grant in self.granted_applications.items():
            application_accordion_titles = []
            application_accordion_titles.append(f"Application title: {title}")

            vbox_display_fields = widgets.VBox()

            application_titles.append(title)

            application_vbox_list = []

            display_fields = ["application_id", "dataset", "approval_message_user"]

            for display_field in display_fields:
                # Add field name to row
                text_widget = widgets.Textarea(
                    layout=widgets.Layout(
                        display='flex',
                        flex_flow='row', 
                        flex_basis='content',
                        align_items='stretch', 
                        border='solid',
                        width='auto',
                        height='auto',
                    ),
                )
                text_widget.description = display_field
                if isinstance(application_grant.get(display_field), dict):
                    # Convert to pretty printable json dump with 4 spaces indentation
                    value = json.dumps(application_grant.get(display_field), indent=4)
                else:
                    value = str(application_grant.get(display_field))
                text_widget.value = value

                application_vbox_list.append(text_widget)

            vbox_display_fields.children = application_vbox_list

            applications_children.append(vbox_display_fields)

        # Populate Applications accordion nest
        accordion_nest = widgets.Accordion(
            titles=application_titles,
            children=applications_children,
        )
        # Add to split panel
        split_panel.children = [accordion_nest]

        # Display Kudaf split panel
        self.frontend_app.shell.add(split_panel, 'main', { 'mode': 'split-bottom' })
    
    def parse_retrieval_url(self, data_url: str, variable: str) -> list:
        """
        - Extracts the query parameters from the data retrieval URL
        - Builds UI input components for each one, either one of: Datetime picker or Text
        . Returns an HBox widget with the built UI input components 
        """
        # Check if there are any query params in the URL
        parsed = requests.utils.urlparse(data_url)
        query = parsed.query

        if not query:
            return []
        
        try:
            orig_params = dict(x.split('=') for x in query.split('&'))   
        except ValueError:
            # Probably bad URL (ends in & or something like that)
            print("ERROR for Variable: {} - Most likely malformed received URL: {}".format(variable, data_url))
            return  []

        params_ui_items = []

        for p, q in orig_params.items():
            input_element = []

            _param_button = widgets.Button(
                layout=widgets.Layout(
                    display='flex',
                    flex_flow='row', 
                    align_items='stretch', 
                    border='none',
                    width='auto'
                ),
                disabled=True,
                button_style='',
            )
            _param_button.description = p.capitalize() + ": "
            _param_button.tooltip = p.capitalize()
                
            input_element.append(_param_button)

            if "start" in p or "stop" in p or "timestamp" in p:
                input_tooltip = "Please enter Date in ISO-8601 format: YYYY-MM-DD (e.g 2023-09-01)"
                input_placeholder = "Date (e.g 2023-09-01)"
                # date_picker = widgets.DatePicker(
                #     description='',
                #     disabled=False,
                #     max=date.today(),
                #     layout=widgets.Layout(
                #         width='auto',
                #         background_color='#FFFACD'
                #     ),             
                # )
                # date_picker.parameter = p
                # date_picker.variable = variable

                # if q:
                #     if type(q) == date:
                #         date_picker.value = q
                #     elif type(q) == str:
                #         try:
                #             q = date.fromisoformat(q)
                #         except ValueError:
                #             q = None
                #         else:
                #             date_picker.value = q

                # date_picker.observe(self.on_query_param_value_change, names='value')
        
                # input_element.append(date_picker)
            else:
                input_tooltip = "Please fill out desired choice or press Enter to accept the given default"
                input_placeholder = ""

            text_input = widgets.Text(
                disabled=False,
                continuous_update=False,
            )
            if q:
                text_input.value = q

            text_input.parameter = p
            text_input.variable = variable
            text_input.placeholder = input_placeholder
            text_input.description_tooltip = input_tooltip

            text_input.observe(self.on_query_param_value_change, names='value')

            input_element.append(text_input)

            params_ui_items += input_element

        return params_ui_items

    def on_query_param_value_change(self, change: Dict):
        owner_widget = change.get('owner')
        new_value = change.get('new')
        if type(new_value) == date:
            query = new_value.isoformat()
        else:
            if not new_value or new_value == 'null':
                # Don't add this parameter
                return
            else:
                query = str(new_value)

        self.download_query_params[owner_widget.variable][owner_widget.parameter] = query

        return
    
    def on_download_button_clicked(self, button_widget): 
        if not self.download_query_params:
            print("NO QUERY PARAMETERS")

        query_string = "&".join(p + "=" + q \
            for p, q in self.download_query_params[button_widget.variable].items() \
            if q not in ["", 'null', 'None', None]
        )
        print("QUERY STRING: {}".format(query_string))

        download_url = button_widget.url
        if query_string:
            download_url += "?" + query_string

        var_params = {
            'variable': button_widget.variable,
            'datasource_id': button_widget.datasource_id,
            "url": download_url,
        }
        print("DOWNLOAD VAR PARAMS: {}".format(var_params))

        # Change button's icon and color while it downloads
        button_widget.icon = 'hourglass-half'
        button_widget.button_style = 'danger'
        button_widget.tooltip = 'Busy downloading data...'

        # Async call to download
        result = self.loop.run_until_complete(self.fetch_granted_data(var_params=var_params))

        # Clear param choices just downloaded
        self.download_query_params[button_widget.variable] = {}

        # Reset button back to normal
        button_widget.icon = 'download'
        button_widget.button_style = 'warning'
        button_widget.tooltip = 'Click to download data'

        print("DOWNLOAD RESULT: {}".format(result))
        return result

    async def fetch_granted_data(self, var_params: Dict):
        print("RETRIEVING DATA FOR VARIABLE: {}".format(var_params))
        jwt_token = self.ksettings.get('jwt_token')
        desired_datasource = var_params.get('datasource_id')
        token_datasource = None
        is_token_expired = True

        if jwt_token:
            # Decode current JWT to check if still valid
            try:
                decoded_jwt = jwt.decode(jwt_token, options={"verify_signature": False})
            except Exception as e:
                print("Error decoding JWT: {}".format(e.args))
            else:
                # Check JWT has right Audience and has not yet expired
                token_datasource = decoded_jwt.get('aud').split('/')[-1]
                is_token_expired = self.auth.is_expired(self.ksettings.get('jwt_token_expires'))

        if token_datasource != desired_datasource or is_token_expired:
            # Fresh Token Exchange for the Variable's Datasource ID
            jwt_token, jwt_token_expires = await self.auth.token_exchange(
                access_token=self.ksettings.get('access_token'),
                datasource_id=desired_datasource,
            )
            if not isinstance(jwt_token, str):
                return {"Data Retrieval ERROR on Token Exchange": jwt_token}
            
            # Save JWT to Notebook settings
            self.ksettings['jwt_token'] = jwt_token
            self.ksettings['jwt_token_expires'] = jwt_token_expires


        headers={
            "Authorization": "Bearer " + jwt_token,
        }
        print("READY TO DOWNLOAD REQUEST - HEADERS: {}".format(headers))

        client = httpx.AsyncClient(
            verify=False,
            limits=httpx.Limits(keepalive_expiry=0),
            timeout=httpx.Timeout(None, connect=5.0),
        )

        try:
            async with client.stream("GET", var_params.get('url'), headers=headers) as response:
                # Check whether response contains a file attachment
                cd_header = response.headers.get('Content-Disposition')
                print("DOWNLOAD RESPONSE HEADERS: {}".format(response.headers))
                if cd_header:
                    filename = parse_content_disposition_header(cd_header=cd_header)
                    filepath = os.path.join(os.getcwd(), 'downloads', filename)
                    with safe_file_open_wb(filepath) as file:
                        async for chunk in response.aiter_bytes():
                            file.write(chunk)
                else:
                    if response.headers.get('Content-Type') == "application/json":
                        # Save as JSON file
                        filename = var_params.get('variable') + ".json"
                    else:
                        # Save as TXT file
                        filename = var_params.get('variable') + ".txt"

                    filepath = os.path.join(os.getcwd(), 'downloads', filename)

                    with safe_file_open_w(filepath) as file:
                        async for chunk in response.aiter_text():
                            file.write(chunk)

                return {"result": "Downloaded File: {} Bytes: str({})".format(
                    filepath, response.headers.get('Content-Length', "")),
                }
        except Exception as e:
            print("NOTEBOOK DOWNLOAD ERROR: {}".format(str(e)))
            return {"result": str(e)}

    async def feide_login(self):
        async with httpx.AsyncClient(headers=self.request_header) as client:
            base_url = self.ksettings.get('base_url')
            response = await client.get(
                url=base_url + '/kudaf/login',
                follow_redirects=True
            )

            return response.status_code

    def get_kudaf_settings(self, base_url: Optional[str] = None):
        if base_url is None:
            base_url = self.ksettings.get('base_url')
        response = httpx.get(
            url=base_url + '/kudaf/settings',
            headers=self.request_header,
            follow_redirects=True
        )

        try:
            jresp = response.json()
        except JSONDecodeError:
            jresp = {
                "error_code": response.status_code,
                "error_msg": response.text,
            }

        return jresp

    def update_kudaf_settings(self, new_settings: Dict, base_url: Optional[str] = None):
        if base_url is None:
            # Take it from Notebook's settings
            base_url = self.ksettings.get('base_url')

        try:
            response = httpx.patch(
                url=base_url + '/kudaf/settings',
                headers=self.request_header,
                json=new_settings,
            )
        except Exception as e:
            print("NOTEBOOK FAILED TO UPDATE KUDAF SETTINGS with new values: {}".format(new_settings))
            return {}
        
        try:
            jresp = response.json()
        except JSONDecodeError:
            jresp = {
                "error_code": response.status_code,
                "error_msg": response.text,
            }

        return jresp

    async def get_granted_applications(self):
        async with httpx.AsyncClient(headers=self.request_header) as client:
            base_url = self.ksettings.get('base_url')
            response = await client.get(
                url=base_url + '/kudaf/granted-applications',
                params={
                'jupyter_token': self.ksettings.get('jupyter_token'),
                },
                follow_redirects=True,
            )
            
        try:
            jresp = response.json()
        except JSONDecodeError:
            jresp = {
                "error_code": response.status_code,
                "error_msg": response.text,
            }

        return jresp

    @staticmethod
    def set_base_url_from_browser():
        """
        Javascript functions to find out the Notebook's Base URL (origin) and save that to the Kudaf Settings via PATCH call to app's KudafSettingsHandler
        Returns HTML, so need to copy/paste from cell output to do anything with it
        """
        burl_js = display.Javascript(
        """
        function patch_settings(base_url, new_settings) {
            const xhr = new XMLHttpRequest();
            xhr.open("PATCH", base_url + "/kudaf/settings");
            xhr.setRequestHeader("Content-type", "application/json; charset=utf-8");
            xhr.onload = () => {
                var data = JSON.parse(xhr.responseText);
                if (xhr.readyState == 4 && xhr.status == "200") {
                console.log(data);
                } else {
                console.log(`Error: ${xhr.status}`);
                }
            };
            xhr.send(new_settings);
        }

        var nurl = window.location.href;
        var burl = window.location.origin;
        const new_settings = JSON.stringify({
            notebook_url: nurl,
            base_url: burl + "/studiolab/default/jupyter",
        });

        patch_settings(burl, new_settings);
        """
        )
        display.display(burl_js)

    @staticmethod
    def get_base_url_from_browser():
        """
        Javascript to find out the Notebook's Base URL
        Returns HTML, so need to copy/paste from cell output to do anything with it
        """
        return display.HTML("""
            <div id="javascriptId"></div>
            <script type="text/javascript">
            var nurl = window.location.href;
            var burl = window.location.origin;
            if (burl.includes('sagemaker.aws')) {
                var base = burl + "/studiolab/default/jupyter";
            } else {
                var base = burl;
            };
            var selected = document.getElementById("javascriptId");
            selected.innerHTML = JSON.stringify({
                notebook_url: nurl,
                origin: burl,
                base_url: base,
            });
            </script>
            """)


kudaf_notebook = KudafNotebook()