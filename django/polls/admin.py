from django.contrib import admin
from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    fields = ['choice_text', 'votes', 'image']  # Include the image field
    readonly_fields = []


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    list_filter = ["pub_date"]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)

# admin heslo12345