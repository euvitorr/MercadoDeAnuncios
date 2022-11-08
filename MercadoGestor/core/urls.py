from django.urls import path

from core.views import (
    QuestionListView,
)

app_name = "core"
urlpatterns = [
    path("list/question", QuestionListView.as_view(), name="question_list"),

]
