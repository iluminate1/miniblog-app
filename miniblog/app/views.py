from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    FormView,
)

from unidecode import unidecode
from django.utils.text import slugify

from .forms import *
from .models import *
from .utils import *

# Create your views here.


class HomePage(DataMixin, ListView):
    model = Item
    template_name = "index.html"
    context_object_name = "posts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title="Home page", item_amount=self.get_queryset()
        )
        return context | c_def

    def get_queryset(self):
        return Item.objects.filter(is_published=True).select_related("cat")


class AddPost(RedirectPermissionRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "addpage.html"
    success_url = reverse_lazy("home")
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add post")
        return context | c_def

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.slug = slugify(unidecode(self.object.title))
        self.object.save()
        return super(AddPost, self).form_valid(form)


class ContactFormView(RedirectPermissionRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = "contact.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Feedback")
        return context | c_def

    def form_valid(self, form):
        print(self.request.POST)
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(ContactFormView, self).form_valid(form)
        # return redirect("home")


class ShowPost(DataMixin, DetailView):
    model = Item
    template_name = "post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context["post"])
        return context | c_def


class ItemCategory(DataMixin, ListView):
    model = Item
    template_name = "index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Item.objects.filter(
            cat__slug=self.kwargs["cat_slug"], is_published=True
        ).select_related("cat")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs["cat_slug"])
        c_def = self.get_user_context(
            title="Category - " + str(c.name),
            cat_selected=c.pk,
        )
        return context | c_def


class RegisterUser(DataMixin, FormView):
    form_class = RegisterUserForm
    template_name = "register.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Sing up")
        return context | c_def

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = "login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Sing in")
        return context | c_def

    def get_success_url(self):
        return reverse_lazy("home")


class Profile(RedirectPermissionRequiredMixin, DataMixin, ListView):
    model = Item
    template_name = "profile.html"
    context_object_name = "posts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title="Profile",
            is_profile=True,
            item_amount=self.get_queryset(),
        )
        return context | c_def

    def get_queryset(self):
        return Item.objects.filter(
            is_published=True, user=self.request.user
        ).select_related("cat")


class ItemCategoryProfile(RedirectPermissionRequiredMixin, DataMixin, ListView):
    model = Item
    template_name = "profile.html"
    context_object_name = "posts"
    allow_empty = True

    def get_queryset(self):
        return Item.objects.filter(
            cat__slug=self.kwargs["cat_slug"], is_published=True, user=self.request.user
        ).select_related("cat")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs["cat_slug"])
        c_def = self.get_user_context(
            title="Category - " + str(c.name),
            cat_selected=c.pk,
            is_profile=True,
        )
        return context | c_def


def about(request):
    user_menu = menu.copy()
    if not request.user.is_staff:
        user_menu.pop()

    return render(
        request,
        "about.html",
        {
            "item_amount": Item.objects.filter(is_published=True).select_related("cat"),
            "cats": Category.objects.annotate(Count("item")),
            "menu": user_menu,
            "title": "About",
            "is_profile": False,
        },
    )


def logout_user(request):
    logout(request)
    return redirect("login")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")
