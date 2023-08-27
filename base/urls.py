from django.contrib import admin
from django.urls import path,include
from . import views
from chatbot.views import home as chatHome
app_name = 'base'

urlpatterns = [
    path('',views.home,name="home"),
    path('product/<str:pk>/',views.ProductView,name='product'),
    path('Update-Product/<str:pk>/',views.updateProduct,name="update-product"),
    path('delete-Product/<str:pk>/',views.deleteProduct,name="delete-product"),
    path('Add-Product/',views.addProduct,name="add-product"),
    path('search-product/',views.SearchedProduct.as_view(),name="search-product"),
    path('navbar/', views.navbar, name='navbar'),
    path('login-page/',views.LoginPage.as_view(),name="login"),
    path('logout-page/',views.logoutUser.as_view(),name="logout"),
    path('register/',views.registerPage.as_view(),name="register"),
    path('cart/',views.CartView.as_view(),name="cart-product"),
    path('AddtoCart/<str:pk>/',views.AddtoCart.as_view(),name='add-cart'),
    path('contact/',chatHome,name="contact-user"),
]
