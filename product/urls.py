from django.urls import path
from .views import product_list, cart_list,CartRUDView,product_page,cart_page, deleteAllCart
from django.views.generic import TemplateView

urlpatterns = [
    # path('products/', TemplateView.as_view(template_name='products/products.html')),
    path('products/', product_page),
    
    path('carts/', cart_page),
    path('api/products/', product_list),
    path('api/carts/', cart_list),
    path('api/carts/<int:pk>/', CartRUDView.as_view()),
    path('api/carts/delete_all/<guest_user>/', deleteAllCart),
]