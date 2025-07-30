import sys 
from jupyter_server.extension.application import ExtensionApp
from jupyter_server.serverapp import ServerApp
from kudaf_extension.handler import (
    FeideLoginHandler,
    FeideOAuthRedirectHandler,
    KudafSettingsHandler,
    KudafPermissionsHandler,
)
from kudaf_extension.utils import get_internal_jupyter_process_details

class KudafExtensionApp(ExtensionApp):

    # -------------- Required traits --------------
    name = "kudaf"
    default_url = "/kudaf"
    load_other_extensions = True
    file_url_prefix = "/render"

    # --- ExtensionApp traits you can configure ---
    static_paths = ['/static']
    template_paths = ['/templates']
    # settings = {
    #     "disable_check_xsrf": True,
    #     "xsrf_cookies": False,
    # }
    handlers = [
        ('/kudaf/login', FeideLoginHandler),
        ('/kudaf/oauth2-redirect', FeideOAuthRedirectHandler),
        ('/kudaf/settings', KudafSettingsHandler),
        ('/kudaf/granted-applications', KudafPermissionsHandler),
    ]

    # ----------- add custom traits below ---------
    allow_origin = "*"
    ...

    def initialize_settings(self):
        ...
        # Update the self.settings trait to pass extra
        # settings to the underlying Tornado Web Application.
        # base_url = ServerApp.base_url.default_value_repr()
        self.settings.update({
            "disable_check_xsrf": True,
            "xsrf_cookies": False,
            "kudaf": {
                "server_process": sys.executable,
                "access_token": None,
                "access_token_expires": None,
                "jwt_token": None,
                "jwt_token_expires": None,
                "jupyter_token": None,
                "jupyter_token_expires": None,
                "user": {},
                "base_url": "http://localhost:8888", 
                "base_browser_url": "http://localhost:8888",
                "permissions_endpoint": "https://kudaf-soknad-staging.sokrates.edupaas.no/api/v1/grants/approved/",
                "granted_applications": {},
        },
    })

    def initialize_handlers(self):
        ...
        # Extend the self.handlers trait
        self.handlers.extend(self.__class__.handlers)

    def initialize_templates(self):
        ...
        # Change the jinja templating environment

    async def stop_extension(self):
        ...
        # Perform any required shut down steps