from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django_distill import distill_path
from cms.models import Article
from . import views


def get_article_slugs_for_django_distill():
    for article in Article.objects.all():
        yield {'slug': article.slug}


def get_none_for_django_distill():
    return None

        
app_name='cms'
urlpatterns = [
    path('', views.index, name='index'),
    distill_path('', views.index, name='index', distill_func=get_none_for_django_distill, distill_file='index.html'),

    path("articles/<slug:slug>.html/", views.article_detail, name="article_detail"),
    distill_path('articles/<slug:slug>.html', views.article_detail, name='article_detail', distill_func=get_article_slugs_for_django_distill, distill_file='articles/{slug}.html'),

    path('about-us.html/', views.about, name='about-us.html'),
    distill_path('about-us.html', views.about, name='about-us.html', distill_func=get_none_for_django_distill, distill_file='about-us.html'),

    path('services.html/', views.services, name='services.html'),
    distill_path('services.html', views.services, name='services.html', distill_func=get_none_for_django_distill, distill_file='services.html'),

    path('faq.html/', views.faq, name='faq.html'),
    distill_path('faq.html', views.faq, name='faq.html', distill_func=get_none_for_django_distill, distill_file='faq.html'),

    path('testimonials.html/', views.testimonials, name='testimonials.html'),
    distill_path('testimonials.html', views.testimonials, name='testimonials.html', distill_func=get_none_for_django_distill, distill_file='testimonials.html'),

    path('expertise.html/', views.expertise, name='expertise.html'),
    distill_path('expertise.html', views.expertise, name='expertise.html', distill_func=get_none_for_django_distill, distill_file='expertise.html'),

    path('blog.html/', views.blog, name='blog.html'),
    distill_path('blog.html', views.blog, name='blog.html', distill_func=get_none_for_django_distill, distill_file='blog.html'),

    path('contact.html/', views.contact, name='contact.html'),
    distill_path('contact.html', views.contact, name='contact.html', distill_func=get_none_for_django_distill, distill_file='contact.html'),

]

urlpatterns += staticfiles_urlpatterns()
print(f'urlpatterns {urlpatterns}')
