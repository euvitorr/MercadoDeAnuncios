import logging
from datetime import datetime
from random import shuffle

from django.contrib import messages
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import (
    get_list_or_404,
    get_object_or_404,
    redirect,
    render,
    resolve_url,
)
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

# from .forms import EntityForm,AvatarForm
from .forms import AddressForm, ContactFormSet, UploadForm
from .models import (
    Address,
    Question,
    QuestionCategory,
)

# Create your views here.
logger = logging.getLogger(__name__)


class HomeTemplateView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, *args, **kwargs):
        contex = super().get_context_data(**kwargs)
        questions = list(Question.objects.filter(active=True))
        shuffle(questions)
        contex["questions"] = questions[:5]
        contex["background"] = [
            "background-1",
            "background-2",
            "background-3",
            "background-4",
        ]
        return contex


class QuestionListView(ListView):
    model = Question
    paginate_by = 5

    def get_queryset(self):
        question = self.request.GET.get("search", "")
        category_pk = self.request.GET.get("category", "0")
        category = QuestionCategory.objects.filter(pk=category_pk).first()

        if category_pk == "0":
            return self.model.objects.filter(question__icontains=question)

        return self.model.objects.filter(
            category=category, question__icontains=question
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = QuestionCategory.objects.all()
        return context


def termo_privacidade(request):
    return render(request, "termo.html", {})


def list_entity_and_project(request):
    term = request.GET.get("term")
    result = list(
        Entity.objects.filter(razao_social__icontains=term).values("razao_social", "id")
    )
    return JsonResponse(result, safe=False)

