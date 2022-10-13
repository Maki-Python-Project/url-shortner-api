from django.contrib import admin

from .models import UrlShortener


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'longurl', 'shorturl'
    )
    save_on_top = True


admin.site.register(UrlShortener, ArticleAdmin)
