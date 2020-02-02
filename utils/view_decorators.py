from django.conf import settings


class cache_control:
    """Add a Cache-Control header. This will be respected by CloudFlare as well for distributed caching kappa"""

    def __init__(self, seconds):
        self.seconds = seconds

    def __call__(self, func):
        def view(*args, **kwargs):
            response = func(*args, **kwargs)

            # pass through if DEBUG
            if settings.DEBUG:
                return response

            # set http response header and value.
            response['Cache-Control'] = f'max-age={self.seconds}, public'
            response['Vary'] = 'Accept-Encoding'

            # return the HttpResponse object.
            return response

        return view
