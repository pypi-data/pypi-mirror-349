import tornado
import httpx
import jwt
from datetime import datetime
from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.extension.handler import ExtensionHandlerMixin
from kudaf_extension.auth import feide_oauth2


class FeideLoginHandler(ExtensionHandlerMixin, JupyterHandler):
    @tornado.web.authenticated
    async def get(self):
        """
        Feide OAuth2 Login handler
        """
        ksettings = self.settings['kudaf'].copy()
        refreshed = await feide_oauth2.login(ksettings)
        if refreshed:
            self.settings['kudaf'].update(refreshed)

        self.write(self.settings['kudaf'])


class FeideOAuthRedirectHandler(ExtensionHandlerMixin, JupyterHandler):
    @tornado.web.authenticated
    async def get(self):
        """
        Feide OAuth2 Redirect URL handler
        """
        jupyter_token = self.settings.get('kudaf', {}).get('jupyter_token', None)
        # jwt_token = self.settings.get('kudaf', {}).get('jwt_token', None)
        jupyter_token_expires = self.settings.get('kudaf', {}).get('jwt_token_expires', None)
        # jwt_token_expires = self.settings.get('kudaf', {}).get('jwt_token_expires', None)
        if jupyter_token is None:
            # Set Authorization Code received from 1st OAuth2 step (Authorization request)
            code = self.get_argument('code')
            state = self.get_argument('state')
            access_token, jupyter_token, access_token_expires = await feide_oauth2.get_access_token(code, state)
            
            if access_token is not None:
                self.settings['kudaf']['access_token'] = access_token
                self.settings['kudaf']['jupyter_token'] = jupyter_token
                self.settings['kudaf']['access_token_expires'] = access_token_expires.isoformat()
 
                # Get User details  #TODO: Do we need this? Extract from JWT instead?
                user = await feide_oauth2.get_user_info(access_token, access_token_expires)
                self.settings['kudaf']['user'] =  user

                #TODO: Try to close the (now blank) auth window
                # raise web.HTTPFound(location='http://localhost:8888/lab/tree/feidestats.ipynb')
                #web.Response(text="YOU CAN NOW CLOSE THIS WINDOW - Authorization Code: {}, State: {}".format(code, state))
                #pyautogui.hotkey('ctrl', 'w')
                #IPython.display.Javascript('window.close();')
                #await asyncio.sleep(1)
                self.write('<div>Authentication complete, YOU CAN NOW CLOSE THIS WINDOW</div>')
            else:
                print("Missing access token")
                #await asyncio.sleep(1) 
        elif jupyter_token_expires and feide_oauth2.is_expired(datetime.fromisoformat(jupyter_token_expires)):
            # Refresh JWT
            jupyter_token, jupyter_token = await feide_oauth2.token_refresh(access_token)
            # Refresh Extension settings
            self.settings['kudaf']['jupyter_token'] = jupyter_token
            self.settings['kudaf']['jupyter_token_expires'] = jupyter_token_expires.isoformat()


class KudafSettingsHandler(ExtensionHandlerMixin, JupyterHandler):
    @tornado.web.authenticated
    async def get(self):
        self.write(self.settings.get('kudaf', {}))

    @tornado.web.authenticated
    async def patch(self):
        if not self.get_json_body():
            # Delete tokens
            updates = {
                'access_token': "",
                'jupyter_token': "",
            }
        else:
            updates = self.get_json_body()
        self.settings['kudaf'].update(updates)
        print("UPDATED Kudaf settings: {}".format(self.settings['kudaf']))
        self.write(self.settings['kudaf'])


class KudafPermissionsHandler(ExtensionHandlerMixin, JupyterHandler):
    @tornado.web.authenticated
    async def get(self):
        jwt_token = self.get_argument('jupyter_token')
        if not jwt_token:
            print("PERMISSIONS HANDLER: NO JWT TOKEN RECEIVED -> SKIPPING PERMISSIONS REQUEST")
            self.write({})

        response = httpx.get(
                url="https://kudaf-soknad-staging.sokrates.edupaas.no/api/v1/grants/approved/",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json",
                    "Authorization": "Bearer " + jwt_token,
                })

        if response.status_code != 200:
            self.write({})
            return
        else:
            permissions_token = response.json()
            if not permissions_token:
                self.write({})
                return

            # Decode the JWT token
            granted_applications = {}
            payload = jwt.decode(permissions_token, options={"verify_signature": False})

            for granted_appl in payload.get('granted_applications', {}):
                title = granted_appl.get('title', str(granted_appl.get('application_id')))

                granted_applications[title] = granted_appl

            self.settings['kudaf']['granted_applications'] = granted_applications

            self.write(granted_applications)
            return
