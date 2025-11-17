from django.apps import AppConfig

class AuditoriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aplications.auditoria'
    verbose_name = 'Registro de cambios'


    def ready(self):
        import aplications.auditoria.signals
