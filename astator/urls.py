from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from . import forms

urlpatterns = [
    # Default - index
    path("", views.index, name="index"),

    # User authentication and user profiles
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("change_password", views.change_password, name="change_password"),
    # Reseting password
    path("reset_password", auth_views.PasswordResetView.as_view(template_name="astator/password_reset.html", form_class=forms.ResetPasswordForm), name="password_reset"),
    path("reset_password_sent", auth_views.PasswordResetDoneView.as_view(template_name="astator/password_reset_sent.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name="astator/password_reset_confirm.html", form_class=forms.SetNewPassword), name="password_reset_confirm"),
    path("reset_password_complete", auth_views.PasswordResetCompleteView.as_view(template_name="astator/password_reset_complete.html"), name="password_reset_complete"),
    
    # Rest of app
    path("myprofile", views.myprofile, name="myprofile"),
    path("create", views.create, name="create"),
    path("script/<int:script_id>", views.script, name="script"),
    path("users/<str:username>", views.users, name="users"),
    path("terms", views.terms, name="terms"),
    path("writerhub/", views.writerhub, name="writerhub"),
    path("explore", views.explore, name="explore"),
    path("explore/<str:query>", views.browse, name="browse"),
    path("read/<int:script_id>", views.read, name="read"),
    path("delete/<int:script_id>", views.delete, name="delete"),

    # API
    path("add_note/<int:script_id>", views.add_note, name="add_note"),
    path("delete_note/<int:note_id>", views.delete_note, name="delete_note"),
    path("read_later/<int:script_id>", views.read_later, name="read_later"),
    path("finish_reading/<int:script_id>", views.finish_reading, name="finish_reading"),

    # Blog
    path("blog", views.blog, name="blog"),
    path("blog/<int:post_id>", views.blog_posts, name="blog_posts"),
]