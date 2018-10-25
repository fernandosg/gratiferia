from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from .forms import ProductForm, ImageForm
from .models import Product, ImageProduct
from apps.users.models import User

# Create your views here.
class ProductDetailView(View):

    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(slug=kwargs["slug"]).first()
        return render(request, "products/detail.html", locals())

class ProductCreateView(View):

    def get(self, request, *args, **kwargs):
        form = ProductForm()
        return render(request, "products/create.html", locals())

    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        form = ProductForm(post)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = User.objects.first() # only for checking
            product.save()
            return redirect(reverse("product_detail", kwargs={"slug":product.slug}))
        else:
            for e in form.errors:
                messages.error(request, e)
        return render(request, "products/create.html", locals())


class ProductEditView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "", locals())


class ProductImageCreateView(View):

    @property
    def slug(self):
        if "slug" in self.kwargs:
            return self.kwargs["slug"]
        return None

    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(slug=self.slug).first()
        return render(request, "products/images/create.html", locals())

    def post(self, request, *args, **kwargs):
        product = Product.objects.filter(slug=self.slug).first()
        post = request.POST.copy()
        form = ImageForm(post, request.FILES)
        if form.is_valid():
            image = form.save()
            ImageProduct.objects.create(image=image, product=product)
            return redirect(reverse("product_detail", kwargs={"slug": product.slug}))
        else:
            for e in form.errors:
                print(e)
                messages.error(request, e)
        return render(request, "products/images/create.html", locals())
