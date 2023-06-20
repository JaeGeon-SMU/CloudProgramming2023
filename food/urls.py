from django.urls import path

from food import views

urlpatterns = [
    path('info/',views.FoodRender ),
    path('search/', views.FoodSearch.as_view()),
    path('search/<int:pk>',views.food_result_view),
]