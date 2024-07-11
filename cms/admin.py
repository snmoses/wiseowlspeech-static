from .models import Article, Settings, Testimonials, TeamMember
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.core.management import call_command
from .models import Settings
from django.utils.html import format_html
from django import forms
from django.core.exceptions import ValidationError


# Register your models here.
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'created_at', 'published', 'display_order')
    ordering = ('display_order', 'name')
    


class TestimonialAdminForm(forms.ModelForm):
    class Meta:
        model = Testimonials
        fields = '__all__'

    def clean(self):
        if self.instance.pk is None and Testimonials.objects.exists():
            raise ValidationError('There can only be one instance of Testimonials.')
        return super().clean()


@admin.register(Testimonials)
class TestimonialsAdmin(admin.ModelAdmin):
    TestimonialAdminForm
    list_display = ('created_at',)
    search_fields = ('content',)

    def changelist_view(self, request, extra_context=None):
        # Redirect to the change view if an instance already exists
        obj = Testimonials.objects.first()
        if obj:
            return HttpResponseRedirect(f'/admin/cms/testimonials/{obj.pk}/change/')
        return super(Testimonials, self).changelist_view(request, extra_context)

    def has_add_permission(self, request):
        # Allow adding only if no instances exist
        return not Testimonials.objects.exists()



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'published')
    search_fields = ('title', 'content')
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    change_list_template = "admin/settings_changelist.html"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('distill/', self.admin_site.admin_view(self.distill_site), name='distill_site'),
        ]
        return custom_urls + urls
    
    def distill_site(self, request):
        settings = Settings.objects.first()
        if settings:
            call_command('distill-local', settings.dest_dir, force=True)
        self.message_user(request, "Site distilled successfully!")
        return HttpResponseRedirect("../")

    def render_distill_button(self, request):
        distill_url = reverse('admin:distill_site')
        return format_html(
            '''
            <div style="margin-bottom: 10px;">
            <a class="button" style="background-color: red; color: white; padding: 10px 20px; font-size: 16px;" href="{}">PUBLISH SITE</a></div>''',
            distill_url
        )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['distill_button'] = self.render_distill_button(request)
        return super().changelist_view(request, extra_context=extra_context)
