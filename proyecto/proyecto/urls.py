from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login, name='login'),
    path('inicio/',views.inicio, name='inicio'),
]