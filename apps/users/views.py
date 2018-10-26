from django.shortcuts import render
from django.views import View
from apps.products.models import RequestProduct, Product

# Create your views here.
class ProfileView(View):

    @property
    def user_id(self):
        if "user_id" in self.kwargs:
            return self.kwargs["user_id"]
        return None

    def get(self, request, *args, **kwargs):
        products_published = Product.objects.filter(author__id=self.user_id).all()
        products_requested = RequestProduct.objects.filter(user__id=self.user_id).all()
        return render(request, "users/profile.html", locals())
