from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from catalog.models import Product, ProductVersion
from catalog.forms import ProductForm, ProductVersionForm

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
        # Получаем текущую версию продукта
        current_version = self.object.versions.filter(is_current=True).first()
        context['current_version'] = current_version
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Обновление счетчика просмотров
        product = self.get_object()
        product.views_count += 1
        product.save()
        return response

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Обработка версии продукта при обновлении
        version_number = self.request.POST.get('version_number')
        version_name = self.request.POST.get('version_name')
        is_current = 'is_current' in self.request.POST

        if version_number and version_name:
            # Обновляем текущую версию, если новая версия указана как активная
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

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

class ProductVersionCreateView(CreateView):
    model = ProductVersion
    form_class = ProductVersionForm
    template_name = 'catalog/productversion_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        product = form.cleaned_data['product']
        if form.cleaned_data['is_current']:
            ProductVersion.objects.filter(product=product).update(is_current=False)
        return super().form_valid(form)

class ProductVersionUpdateView(UpdateView):
    model = ProductVersion
    form_class = ProductVersionForm
    template_name = 'catalog/productversion_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        product = form.cleaned_data['product']
        if form.cleaned_data['is_current']:
            ProductVersion.objects.filter(product=product).update(is_current=False)
        return super().form_valid(form)