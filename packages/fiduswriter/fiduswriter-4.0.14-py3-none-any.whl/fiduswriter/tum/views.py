import requests

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)


class TUMOAuth2Adapter(OAuth2Adapter):
    provider_id = "tum"
    access_token_url = "https://campus.tum.de/tumonline/wbOAuth2.token"
    authorize_url = "https://campus.tum.de/tumonline/wbOAuth2.authorize"
    profile_url = "https://campus.tum.de/tumonline/!co_loc_wsoa2user.userinfo"

    def complete_login(self, request, app, token, **kwargs):
        extra_data = self.get_user_info(token)
        login = self.get_provider().sociallogin_from_response(
            request, extra_data
        )
        return login

    def get_user_info(self, token):
        auth_header = f"Bearer {token.token}"
        headers = {
            "Accept": "application/json",
            "Authorization": auth_header,
            "accept": "application/json",
        }
        resp = requests.get(self.profile_url, headers=headers)
        resp.raise_for_status()
        return resp.json()


oauth2_login = OAuth2LoginView.adapter_view(TUMOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(TUMOAuth2Adapter)
