from django.contrib import admin
from .models import Profile, Post, Entry, Tag, Comment

class EntryStackedInline(admin.StackedInline):
    model = Entry
    extra = 4

@admin.register(Post)
class Post(admin.ModelAdmin):
    inlines = [EntryStackedInline]

admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Profile)
