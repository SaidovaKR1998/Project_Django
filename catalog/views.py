from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from .models import Product
from .forms import ProductForm

class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()

class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

# ЗАЩИЩЕННЫЕ ПРЕДСТАВЛЕНИЯ - только для авторизованных пользователей
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Автоматически назначаем владельца
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner  # Только владелец может редактировать

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'

    def test_func(self):
        product = self.get_object()
        # Владелец ИЛИ модератор может удалять
        return (self.request.user == product.owner or
                self.request.user.has_perm('catalog.delete_product'))

# ФУНКЦИИ ДЛЯ ПУБЛИКАЦИИ И СНЯТИЯ С ПУБЛИКАЦИИ
@login_required
def publish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # Только владелец может публиковать
    if request.user == product.owner and request.method == 'POST':
        product.publication_status = 'published'
        product.save()
        return redirect('catalog:product_list')
    return render(request, 'catalog/publish_confirm.html', {'product': product})

@login_required
@permission_required('catalog.can_unpublish_product', raise_exception=True)
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.publication_status = 'draft'
        product.save()
        return redirect('catalog:product_list')
    return render(request, 'catalog/unpublish_confirm.html', {'product': product})