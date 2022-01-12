from django.contrib import admin
from django.utils.html import format_html  # Thank you https://stackoverflow.com/questions/1949248/how-to-add-clickable-links-to-a-field-in-django-admin
from .models import Language, Word


class LanguageAdmin(admin.ModelAdmin):
	list_display = ("name", "short_name")


@admin.action(description='Mark as approved')
def mark_approved(modeladmin, request, queryset):
    queryset.update(approved=True)


class WordAdmin(admin.ModelAdmin):
	list_display = ("romanize", "language", "approved")
	actions = [mark_approved]
	readonly_fields = ['source_link']
	fieldsets = (
		(None, {'fields': ('text', 'romanized', 'language', 'parent', 'reconstructed', )}),
		(None, {'fields': ('approved', ('source', 'source_link'))})
	)

	def source_link(self, obj):
		return format_html('<a href="{url}">Link</a>', url=obj.source)


# Register your models here.
admin.site.register(Language, LanguageAdmin)
admin.site.register(Word, WordAdmin)
