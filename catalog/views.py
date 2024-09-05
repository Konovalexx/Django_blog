from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseForbidden
from catalog.models import Product, ProductVersion
from catalog.forms import ProductForm, ProductVersionForm, ProductModeratorForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context['products']:
            product.current_version = product.versions.filter(is_current=True).first()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_version'] = self.object.versions.filter(is_current=True).first()
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        product = self.get_object()
        product.views_count += 1
        product.save()
        return response

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def get_form_class(self):
        product = self.get_object()
        if product.created_by != self.request.user and self.request.user.groups.filter(name='Moderators').exists():
            self.template_name = 'catalog/product_form_moder.html'
            return ProductModeratorForm
        return ProductForm

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if product.created_by != request.user and not request.user.groups.filter(name='Moderators').exists():
            return HttpResponseForbidden("Вы не можете редактировать этот товар.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        version_number = self.request.POST.get('version_number')
        version_name = self.request.POST.get('version_name')
        is_current = 'is_current' in self.request.POST

        if version_number and version_name:
            if is_current:
                ProductVersion.objects.filter(product=self.object).update(is_current=False)
            ProductVersion.objects.update_or_create(
                product=self.object,
                version_number=version_number,
                defaults={
                    'version_name': version_name,
                    'is_current': is_current,
                }
            )
        return response

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if product.created_by != request.user and not request.user.groups.filter(name='Moderators').exists():
            return HttpResponseForbidden("Вы не можете удалить этот товар.")
        return super().dispatch(request, *args, **kwargs)

class ProductVersionCreateView(LoginRequiredMixin, CreateView):
    model = ProductVersion
    form_class = ProductVersionForm
    template_name = 'catalog/productversion_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs.get('slug'))
        if product.created_by != request.user and not request.user.groups.filter(name='Moderators').exists():
            return HttpResponseForbidden("Вы не можете добавлять версии для этого товара.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        product = form.cleaned_data['product']
        if form.cleaned_data['is_current']:
            ProductVersion.objects.filter(product=product).update(is_current=False)
        return super().form_valid(form)

class ProductVersionUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductVersion
    form_class = ProductVersionForm
    template_name = 'catalog/productversion_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        product_version = self.get_object()
        if product_version.product.created_by != request.user and not request.user.groups.filter(name='Moderators').exists():
            return HttpResponseForbidden("Вы не можете обновлять эту версию товара.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        product = form.cleaned_data['product']
        if form.cleaned_data['is_current']:
            ProductVersion.objects.filter(product=product).update(is_current=False)
        return super().form_valid(form)