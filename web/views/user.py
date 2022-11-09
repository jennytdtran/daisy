from itertools import groupby

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)

from core.constants import Permissions
from core.forms.user import UserForm, UserEditFormActiveDirectory, UserEditFormManual
from core.models import User
from core.models.project import ProjectUserObjectPermission
from core.models.dataset import DatasetUserObjectPermission
from core.models.user import UserSource
from core.permissions.checker import CheckerMixin
from web.views.utils import AjaxViewMixin


def superuser_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass

    return wrapper


@superuser_required()
class UsersListView(ListView):
    model = User
    template_name = "users/user_list.html"


@superuser_required()
class UserCreateView(CreateView, AjaxViewMixin):
    model = User
    template_name = "users/user_form.html"
    form_class = UserForm
    success_message = "New  user profile has been created"

    def form_valid(self, form):
        user = form.save(commit=False)
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        groups = form.cleaned_data["groups"]
        user.set_password(password)
        user.username = email
        user.source = UserSource.MANUAL
        user.save()
        user.groups.set(groups)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("users")


@superuser_required()
class UserEditView(UpdateView):
    model = User
    template_name = "users/user_form_edit.html"
    success_message = "User profile has been updated"

    def get_form_class(self):
        user = self.get_object()
        if user.source == UserSource.ACTIVE_DIRECTORY:
            return UserEditFormActiveDirectory
        else:
            return UserEditFormManual

    def get_success_url(self):
        return reverse_lazy("user", kwargs={"pk": self.object.id})


@superuser_required()
class UserDetailView(DetailView):
    model = User
    template_name = "users/user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        can_edit = True
        context["can_edit"] = can_edit
        context["manual_source"] = UserSource.MANUAL
        project_set = ProjectUserObjectPermission.objects.filter(user=context["user"])
        dataset_set = DatasetUserObjectPermission.objects.filter(user=context["user"])
        key_func = lambda x: x.content_object
        project_perms = {
            k: [p.permission.codename for p in list(l)]
            for k, l in groupby(project_set, key_func)
        }
        dataset_perms = {
            k: [p.permission.codename for p in list(l)]
            for k, l in groupby(dataset_set, key_func)
        }
        context["project_perms"] = project_perms
        context["dataset_perms"] = dataset_perms
        context["ds_perms_const"] = list(map(lambda x: f"{x}_dataset", [p.value for p in Permissions]))
        context["pj_perms_const"] = list(map(lambda x: f"{x}_project", [p.value for p in Permissions]))
        context["perms_const"] = list(Permissions)
        return context


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST or None)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Important!
            messages.success(
                request, "Your password was successfully updated! Please login again"
            )
            return redirect("logout")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(
        request,
        "users/user_change_password.html",
        {
            "form": form,
        },
    )


class UserPasswordChange(PasswordChangeView):
    template_name = "users/user_change_password.html"
    success_url = "/"

    def get_success_url(self):
        return reverse_lazy("login")


class UserDelete(CheckerMixin, DeleteView):
    model = User
    template_name = "../templates/generic_confirm_delete.html"
    success_url = reverse_lazy("users")
    success_message = "User was deleted successfully."

    def get_context_data(self, **kwargs):
        context = super(UserDelete, self).get_context_data(**kwargs)
        context["action_url"] = "user_delete"
        context["id"] = self.object.id
        return context
