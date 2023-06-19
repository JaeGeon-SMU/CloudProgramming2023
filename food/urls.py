from django.urls import path

from food import views

urlpatterns = [
    path('info/',views.FoodRender ),

]