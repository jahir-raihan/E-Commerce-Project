from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import redirect


class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        return '/user/redirect-user/base-location/'
