from django.urls import path
from .import views

urlpatterns =[
    path("", views.home, name="home"), 
    path("starter-graph", views.starter, name="starter"), 
    path("combo", views.combo, name="combo"), 
    path("programming", views.programming, name="programming"), 
    path("products/", views.products, name="products"), 
]