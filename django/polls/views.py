from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from .models import Choice, Question

# Index view - výpis otázok
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


# Detail view - detail otázky
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


# Výsledky ankety
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


# Funkcia pre hlasovanie, prihlásený používateľ
@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


# Funkcia pre registráciu používateľa
def register(request):
    if request.user.is_authenticated:
        # Ak je používateľ už prihlásený, presmerujeme na hlavnú stránku
        return redirect('polls:index')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automaticky sa prihlási nového používateľa
            messages.success(request, f'Account created for {user.username}!')
            return redirect('polls:index')  # Po registrácii presmerujeme na hlavnú stránku
    else:
        form = UserCreationForm()
    return render(request, 'polls/register.html', {'form': form})


# Login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect('polls:index')  # Ak je používateľ už prihlásený, presmerujeme na hlavnú stránku
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('polls:index')
    else:
        form = AuthenticationForm()
    
    return render(request, 'polls/login.html', {'form': form})


# Logout view - používateľ sa odhlási
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('polls:index')


def detail(request, question_id):
    messages.error(request, "Musíte byť prihlásený, aby ste mohli pokračovať.")