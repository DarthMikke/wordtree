from django.contrib import admin
from .models import Language, Word


class LanguageAdmin(admin.ModelAdmin):
	list_display = ("name", "short_name")


@admin.action(description='Mark as approved')
def mark_approved(modeladmin, request, queryset):
    queryset.update(approved=True)


class WordAdmin(admin.ModelAdmin):
	list_display = ("romanize", "language", "approved")
	actions = [mark_approved]


# Register your models here.
admin.site.register(Language, LanguageAdmin)
admin.site.register(Word, WordAdmin)
