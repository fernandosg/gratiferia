from django.shortcuts import render
from django.views import View
from django.contrib import messages
from apps.products.models import ReportProduct, Product
from django.http import HttpResponseForbidden

# Create your views here.
class RevitionIndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "", locals())


class RevitionProductIndexView(View):

    @property
    def product_id(self):
        if "product_id" in self.kwargs:
            return self.kwargs["product_id"]
        return None

    def get(self, request, *args, **kwargs):
        reports_product = ReportProduct.objects.filter(product__visible=False).all()
        return render(request, "dashboard/revition/products/index.html", locals())

    def post(self, request, *args, **kwargs):
        reports_product = ReportProduct.objects.filter(product__visible=False).all()
        product_id = self.product_id
        if product_id is None:
            return HttpResponseForbidden()
        product = Product.objects.filter(id=product_id).first()
        product.visible = False
        product.save()
        messages.success(request, "El producto ha sido deshabilitado con éxito")
        return render(request, "dashboard/revition/products/index.html", locals())

class RevitionImageIndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "", locals())
