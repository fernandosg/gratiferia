from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from .forms import ProductForm, ImageForm
from .models import Product, ImageProduct, RequestProduct
from apps.users.models import User
from apps.inbox.models import Message
from apps.products.models import Category
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Create your views here.
class ProductIndexView(View):

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()[:10]
        categories = Category.objects.order_by("name").all()
        return render(request, "products/products_list.html", locals())


class ProductsByCategoryView(View):

    @property
    def slug(self):
        if "slug" in self.kwargs:
            return self.kwargs["slug"]
        return None

    def get(self, request, *args, **kwargs):
        category = self.slug
        if category is None:
            return HttpResponseForbidden()
        category = Category.objects.filter(slug=self.slug).first()
        categories = Category.objects.order_by("name").all()
        products = Product.objects.filter(category=category).all()[:10]
        title = "Productos de la categoría {}".format(category.name)
        return render(request, "products/products_list.html", locals())


class ProductDetailView(View):

    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(slug=kwargs["slug"]).first()
        title = "Producto {}".format(product.name)
        return render(request, "products/detail.html", locals())


class ProductRequestView(View):

    @property
    def slug(self):
        if "slug" in self.kwargs:
            return self.kwargs["slug"]
        return None

    def send_message_to_author_for_request_product(self, author_product, title_product):
        content = "Hola me interesa el producto {}, estoy solicitando el producto. Puedes revisar en tu panel en la sección de Solicitudes mi solicitud.".format(title_product)
        Message.objects.create(from_user=self.request.user, to_user=author_product, content=content)

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if self.slug is None:
            return HttpResponseForbidden()
        product = Product.objects.filter(slug=self.slug).first()
        if RequestProduct.objects.filter(product=product, user=request.user).exists():
            messages.error(request, "Ya has solicitado este producto")
        if product.is_not_available():
            messages.error(request, "Este producto no esta disponible para solicitar")
        else:
            request_product = RequestProduct.objects.create(product=product, user=request.user)
            request_product.product.request_product()
            self.send_message_to_author_for_request_product(product.author, product.name)
            messages.success(request, "Producto solicitado con éxito")
        title = "Producto {}".format(product.name)
        return render(request, "products/detail.html", locals())

class ProductCreateView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = ProductForm()
        return render(request, "products/create.html", locals())

    @method_decorator(login_required)
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

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(slug=self.slug).first()
        return render(request, "products/images/create.html", locals())

    @method_decorator(login_required)
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
