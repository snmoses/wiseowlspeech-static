from django.apps import AppConfig


class DjangoStaticProjectConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cms"

    def ready(self):
        import cms.signals