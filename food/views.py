from django.shortcuts import render


def FoodRender(request):
    return render(request, 'food/food_info.html')