from .models import Settings, Testimonials, Article

def global_variables(request):
    settings = Settings.objects.first()
    try:
        return {
            'site_name': settings.site_name,
            'site_headline': settings.site_headline,
            'site_teaser': settings.site_teaser,
            'about': settings.about,
        }
    except:
        return {
            'site_name': 'set up site name in site settings',
            'site_headline': 'set up site headline in site settings',
            'site_teaser': 'set up site teaser in site settings',
            'about': 'put "about" description in site settings',
        }