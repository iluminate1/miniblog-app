from django.urls import path

from django.views.generic.base import RedirectView

from .views import *

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("addpage/", AddPost.as_view(), name="add_page"),
    path("contact/", ContactFormView.as_view(), name="contact"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
    path("about/", about, name="about"),
    path("profile/", Profile.as_view(), name="profile"),
    path("profile/category/<slug:cat_slug>/", ItemCategoryProfile.as_view(), name="profile_category"),
    path("post/<slug:post_slug>/", ShowPost.as_view(), name="post"),
    path("category/<slug:cat_slug>/", ItemCategory.as_view(), name="category"),
    path('admin', RedirectView.as_view(url=reverse_lazy('admin:index')), name='admin_panel'),
    
]
