from .models import Settings

def get_dest_base_dir():
    # Get the existing Settings instance or return a default value
    try:
        return Settings.objects.get().dest_dir
    except Settings.DoesNotExist:
        return "/var/www/html/nginx"  # Or another sensible default
