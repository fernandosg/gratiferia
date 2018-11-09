from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.http import HttpResponseForbidden
from apps.products.models import RequestProduct, Product, Category
from apps.users.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import UserProfileForm

# Create your views here.
class ProfileView(View):

    @property
    def user_id(self):
        if "user_id" in self.kwargs:
            return self.kwargs["user_id"]
        return None

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if self.user_id is None:
            if request.user is not None:
                user = request.user
            else:
                return HttpResponseForbidden()
        else:
            user = User.objects.filter(id=self.user_id).first()
        title = "Perfil del usuario {}".format(user.name)
        result = Product.objects.filter(author__id=user.id)
        products_published = result.all()[:4]
        total_products_published = result.count()
        return render(request, "users/profile.html", locals())


class ProfileEditView(View):

    @property
    def user_id(self):
        if "user_id" in self.kwargs:
            return self.kwargs["user_id"]
        return None

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        title = "Editando perfil"
        user = request.user
        return render(request, "users/profile_form.html", locals())


    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        title = "Editando perfil"
        post = request.POST.copy()
        user = User.objects.filter(id=request.user.id).first()
        form = UserProfileForm(post, instance=user)
        if form.is_valid():
            obj = form.save(commit=False)
            if post["password"] is not None and post["password"] != "":
                obj.set_password(post["password"])
            obj.save()
            messages.success(request, "Contraseña cambiada con éxito")
            return redirect(reverse("my_profile"))
        else:
            for e in form.errors:
                print(e)
                messages.error(request, e)
        return render(request, "users/profile_form.html", locals())


class UserProductsView(View):

    @property
    def user_id(self):
        if "user_id" in self.kwargs:
            return self.kwargs["user_id"]
        return None

    def get(self, request, *args, **kwargs):
        if self.user_id is None:
            return HttpResponseForbidden()
        user = User.objects.filter(id=self.user_id).first()
        categories = Category.objects.order_by("name").all()
        products = Product.objects.filter(author=user).all()
        title = "Productos del usuario {}".format(user.name)
        return render(request, "products/products_list.html", locals())
