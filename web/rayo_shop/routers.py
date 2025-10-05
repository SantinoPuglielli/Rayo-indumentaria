class DatabaseRouter:
    django_apps = ['admin', 'auth', 'contenttypes', 'sessions']
    
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'core' and model._meta.model_name == 'carouselslide':
            return 'django_system'
        if model._meta.app_label in self.django_apps:
            return 'django_system'
        return 'default'
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'core' and model._meta.model_name == 'carouselslide':
            return 'django_system'
        if model._meta.app_label in self.django_apps:
            return 'django_system'
        return 'default'
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'core' and model_name == 'carouselslide':
            return db == 'django_system'
        if app_label in self.django_apps:
            return db == 'django_system'
        if app_label == 'catalog':
            return False  # NO migrar, tablas ya existen
        return None