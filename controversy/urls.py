from django.urls import path
from . import views

app_name = "controversy"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<slug:slug>/', views.ControversyView.as_view(), name='detail'),
]