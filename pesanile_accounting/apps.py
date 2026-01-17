from django.apps import AppConfig


class PesanileAccountingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pesanile_accounting'

    def ready(self):
        import pesanile_accounting.signals
