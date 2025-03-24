from django.urls import path
from knox import views as knox_views
from .views import (
    LoginView, LogoutView, CurrentUserView,
    ProductListView, ProductSelectionView
)


urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='knox_login'),
    path('auth/logout/', LogoutView.as_view(), name='knox_logout'),
    path('auth/logout-all/', knox_views.LogoutAllView.as_view(), name='knox_logout_all'),
    path('user/', CurrentUserView.as_view(), name='current-user'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/select/', ProductSelectionView.as_view(), name='select-product'),
    path('products/selected/', ProductSelectionView.as_view(), name='selected-products'),
]
