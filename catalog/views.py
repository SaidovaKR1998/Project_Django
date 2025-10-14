from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from .models import Product
from .forms import ProductForm

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import DetailView

from .models import Category
from .services import get_products_by_category, get_categories_with_products
from .services import get_all_published_products, get_featured_products

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
    paginate_by = 12

    def get_queryset(self):
        return get_all_published_products()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = get_featured_products()
        return context


# Кешируем главную страницу на 5 минут
@cache_page(60 * 5)
def home(request):
    featured_products = get_featured_products()
    context = {
        'featured_products': featured_products,
    }
    return render(request, 'catalog/home.html', context)

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

# Кешируем страницу продукта на 15 минут
@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Дополнительные данные, если нужны
        return context


def category_products(request, category_slug):
    """
    Представление для отображения продуктов по категории
    """
    products = get_products_by_category(category_slug)
    categories = get_categories_with_products()

    # Получаем текущую категорию для отображения названия
    current_category = None
    if products.exists():
        current_category = products.first().category
    else:
        # Если продуктов нет, все равно пытаемся получить категорию
        try:
            current_category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            current_category = None

    context = {
        'products': products,
        'categories': categories,
        'current_category': current_category,
        'current_category_slug': category_slug,
    }

    return render(request, 'catalog/category_products.html', context)
