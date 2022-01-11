from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from cart.models import Cart, DeliveryCost
from accounts.models import CustomUser,Customers
from .serializers import CartSerializer, DeliveryCostSerializer
from cart.helpers import CartHelper
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = Customers.objects.all().order_by('id')
#     serializer_class = UserSerializer



class CartViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all().order_by('id')
    serializer_class = CartSerializer

    @action(methods=['get'], detail=False, url_path='checkout/(?P<userId>[^/.]+)', url_name='checkout')
    def checkout(self, request, *args, **kwargs):
        print("hello migth some pother issues")
        try:
            user = Customers.objects.get(admin=request.user)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'Error': str(e)})

        cart_helper = CartHelper(user)
        checkout_details = cart_helper.prepare_cart_for_checkout()

        if not checkout_details:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'error': 'Cart of user is empty.'})

        return Response(status=status.HTTP_200_OK, data={'checkout_details': checkout_details})


class DeliveryCostViewSet(viewsets.ModelViewSet):
    queryset = DeliveryCost.objects.all().order_by('id')
    serializer_class = DeliveryCostSerializer
