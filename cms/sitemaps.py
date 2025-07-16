from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import TeamMember, Article, Testimonials


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return [
            "cms:about-us.html",
            "cms:faq.html",
            "cms:testimonials.html",
            "cms:services.html",
            "cms:expertise.html",
            "cms:contact.html",
        ]

    def location(self, item):
        return reverse(item)


# class TeamMemberSitemap(Sitemap):
#    changefreq = "weekly"
#    priority = 0.8
#
#    def items(self):
#        return TeamMember.objects.filter(published=True)
#
#    def lastmod(self, obj):
#        return obj.created_at
#
#
class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Article.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.created_at


# class TestimonialSitemap(Sitemap):
#    changefreq = "weekly"
#    priority = 0.8
#
#    def items(self):
#        return Testimonials.objects.filter(published=True)
#
#    def lastmod(self, obj):
#        return obj.created_at
