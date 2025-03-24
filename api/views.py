from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny

from drf_yasg.utils import swagger_auto_schema
from knox.views import LoginView as KnoxLoginView, LogoutView as KnoxLogoutView
from knox.auth import TokenAuthentication

from .models import Product
from .serializers import ProductSerializer


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=AuthTokenSerializer)
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        request.session['selected_products'] = []

        return super().post(request, format=None)


class LogoutView(KnoxLogoutView):
    def post(self, request, *args, **kwargs):
        request.session.flush()  # clear selected_products
        return super().post(request, *args, **kwargs)


class CurrentUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            'username': request.user.username,
            'email': request.user.email,
        })


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get("search")
        ordering = self.request.query_params.get("ordering")
        if query:
            queryset = queryset.filter(name__icontains=query)
        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset


class ProductSelectionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        selected = request.session.get('selected_products', [])
        if pk not in selected:
            selected.append(pk)
        request.session['selected_products'] = selected
        return Response({"status": "selected", "selected": selected})

    def get(self, request):
        selected = request.session.get('selected_products', [])
        products = Product.objects.filter(pk__in=selected)
        return Response(ProductSerializer(products, many=True).data)
