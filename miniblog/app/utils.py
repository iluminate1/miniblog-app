from django.db.models import Count
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *

menu = [
    {"title": "About", "url_name": "about", "class": "fa fa-fw fa-info"},
    {"title": "Add post", "url_name": "add_page", "class": "fa fa-fw fa-plus"},
    {"title": "FeedBack", "url_name": "contact", "class": "fa fa-fw fa-comment"},
    {"title": "ADMIN PANEL", "url_name": "admin_panel", "class": "fa fa-fw fa-lock"},
]


class DataMixin:
    paginate_by = 5

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count("item"))
        user_menu = menu.copy()

        # if not self.request.user.is_authenticated:
        #     user_menu.pop(1)

        if not self.request.user.is_staff:
            user_menu.pop()

        context["menu"] = user_menu

        context["cats"] = cats

        context["item_amount"] = Item.objects.filter(is_published=True).select_related(
            "cat"
        )

        if "cat_selected" not in context:
            context["cat_selected"] = 0
        return context


class RedirectPermissionRequiredMixin(
    LoginRequiredMixin,
):
    login_url = reverse_lazy("login")
    redirect_field_name = "home"

    def handle_no_permission(self):
        return redirect(self.get_login_url())


# class AuthenticatedMixin(object):
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()
#         return super(AuthenticatedMixin, self).dispatch(request, *args, **kwargs)
