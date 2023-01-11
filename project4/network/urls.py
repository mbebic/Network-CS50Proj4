
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("updatelikecount/<int:post_id>", views.updatelikecount, name = "updatelike"),
    path("profile/<int:user_id>", views.userprofile, name="profile"),
    path("followunfollow/<int:user_id>", views.followunfollow, name="followunfollow"),
    path("editpost/<int:post_id>", views.editpost, name="editpost"),
    path("following/<int:user_id>", views.following, name="following"),
]
