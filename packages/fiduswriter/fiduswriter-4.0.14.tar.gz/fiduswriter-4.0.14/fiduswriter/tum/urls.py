from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import TUMProvider


urlpatterns = default_urlpatterns(TUMProvider)
