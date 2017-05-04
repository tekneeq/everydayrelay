from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Wine, Review, News

class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('wine', 'rating', 'user_name', 'comment', 'pub_date')
    list_filter = ['pub_date', 'user_name']
    search_fields = ['comment']

admin.site.register(Wine)
admin.site.register(Review, ReviewAdmin)
admin.site.register(News)
