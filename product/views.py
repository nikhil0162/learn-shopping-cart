from django.shortcuts import render
from .models import Product, Cart
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .serializers import ProductSerializer, CartSerializer
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django.http import JsonResponse

@csrf_exempt
@api_view(['GET'])
def product_list(request):
    product_qs = Product.objects.all()
    serializer = ProductSerializer(product_qs, many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(['GET', 'POST'])
def cart_list(request):
    if not request.session.session_key:
        request.session.create()
    guest_user_key = request.session.session_key
    # print(request.GET.get('guest_user_key'))
    # guest_user_key = request.session.session_key
    print(request.session.session_key)
    if request.method == "GET":
        cart_qs = Cart.objects.filter(guest_user=guest_user_key)
        serializer = CartSerializer(cart_qs, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        request.data['guest_user'] = request.session.session_key
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"details": "Created"})
    return Response({'errors': serializer.errors})

@csrf_exempt
@api_view(['DELETE'])
def deleteAllCart(request, guest_user):
    if guest_user:
        cart_qs = Cart.objects.filter(guest_user=guest_user).delete()
        return Response({'details': 'all carts has been delete successfully'})
    return Response({'details': 'guest user id is wrong'})


class CartRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


def product_page(request):
    product_qs = Product.objects.all()
    return render(request, 'products/products.html', {"product_qs": product_qs})

def cart_page(request):
    product_qs = Product.objects.all()
    cart_qs = Cart.objects.all()
    print(request.session.session_key)
    guest_user_key = request.session.session_key
    return render(request, 'products/cart.html', {"product_qs": product_qs, 'cart_qs': cart_qs, 'guest_user_key':guest_user_key})