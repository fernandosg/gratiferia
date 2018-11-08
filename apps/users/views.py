from django.shortcuts import render
from django.views import View
from django.http import HttpResponseForbidden
from apps.products.models import RequestProduct, Product, Category
from apps.users.models import User

# Create your views here.
class ProfileView(View):

    @property
    def user_id(self):
        if "user_id" in self.kwargs:
            return self.kwargs["user_id"]
        return None

    def get(self, request, *args, **kwargs):
        if self.user_id is None:
            if request.user is not None:
                user = request.user
            else:
                return HttpResponseForbidden()
        else:
            user = User.objects.filter(id=self.user_id).first()
        result = Product.objects.filter(author__id=user.id)
        products_published = result.all()[:4]
        total_products_published = result.count()
        return render(request, "users/profile.html", locals())


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
