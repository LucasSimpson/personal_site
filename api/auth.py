from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions


# custom auth. reasons are as follows:
# 1) There will only ever be 1 user (me). Hence, I don't need a database of all users, I just need
#       to check against 1 password
# 2) I can't use most of the built-in auth, as they all rely on django user/session/stuff, which
#       all use and expect an SQL database, which I have disabled. This leaves only token based auth
# 3) I don't use token based auth because I wan't to be able to auth directly from browsable API.
# Thus, I set this custom auth. All POST requests are authenticated against this singular password :)
# TODO: auth against rotating key
class IsLucasAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):

        # we only care about POST requests
        if request.method == 'POST':
            token = request.POST.get('auth_token', None)

            if not token or token != settings.AUTH_TOKEN:
                raise exceptions.AuthenticationFailed('Invalid auth token')

            return 'Lucas', None

        return 'Anon', None
