from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.safestring import mark_safe

from .models import (
    Address,
    Question,
    QuestionCategory,
)
from .utils import format_cnpj


@admin.register(QuestionCategory)
class QuestionsAQuestionCategorydmin(admin.ModelAdmin):
    model = QuestionCategory
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Question)
class QuestionsAdmin(admin.ModelAdmin):
    model = Question
    list_display = (
        "question",
        "active",
        "category",
    )
    list_filter = (
        "category__name",
        "active",
    )
    search_fields = (
        "question",
        "answer",
    )


class AddressInline(admin.StackedInline):
    model = Address
    fields = (
        "street",
        "street_number",
        "complement",
        "zipcode",
        "city",
        "state",
        "country",
    )
