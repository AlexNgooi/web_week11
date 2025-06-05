from django.apps import AppConfig


class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'
    
    def ready(self):
        """Initialize Firebase when Django app is ready"""
        # Import here to avoid circular imports
        from . import firebase_config
        # Firebase will initialize itself on import