from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import redirect


# Overriding Account Adapter to redirect user -> from where he came from ( Only for social auth )
class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        return '/account/redirect-user/base-location/'

    def get_logout_redirect_url(self, request):
        return '/account/login/'

    def get_signup_redirect_url(self, request):
        return '/account/redirect-user/base-location/'
