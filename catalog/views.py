#from django.shortcuts import render, get_object_or_404
#from .models import Product

#def home(request):
#    products = Product.objects.all()
#    return render(request, 'home.html', {'products': products})

#def contacts(request):
#    return render(request, 'contacts.html')

#def product_detail(request, product_id):
#    product = get_object_or_404(Product, id=product_id)
#    return render(request, 'product_detail.html', {'product': product})

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, Category


class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


class ContactsView(TemplateView):
    template_name = 'contacts.html'
