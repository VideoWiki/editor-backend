from django.apps import AppConfig


class UserauthenticationConfig(AppConfig):
    name = 'user'

class UserMailConfig(AppConfig):
    name = 'user'

    def ready(self):
        import user.signals


