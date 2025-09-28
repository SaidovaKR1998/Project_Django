#from django.urls import path
#from catalog.apps import CatalogConfig
#from catalog.views import home, contacts, product_detail

#app_name = CatalogConfig.name

#urlpatterns = [
#    path('', home, name='home'),
#    path('contacts/', contacts, name='contacts'),
#    path('product/<int:product_id>/', product_detail, name='product_detail'),
#]

from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import HomeView, ProductDetailView, ContactsView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
