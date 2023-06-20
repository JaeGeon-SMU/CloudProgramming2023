import pandas as pd
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView

from food.models import SearchFood


def FoodRender(request):
    return render(request, 'food/food_info.html')

class FoodSearch(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = SearchFood
    fields = ['kcal','protein','fat','carbohydrate']

    template_name = 'food/food_search.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
    def form_valid(self, form):
        if self.request.user.is_authenticated and (self.request.user.is_superuser or self.request.user.is_staff):
            form.instance.author = self.request.user
            return super(FoodSearch, self).form_valid(form)
        else:
            return redirect('/food/info')
class FoodSearchResult(DetailView):
    model = SearchFood
    template_name = 'food/food_search_result.html'

def food_result_view(request,pk):
    self=SearchFood.objects.get(pk=pk)
    self = SearchFood.objects.get(pk=pk)
    df = pd.read_excel('food/foo.xlsx')
    if self.kcal > self.zero:
        if self.protein > self.zero:
            if self.fat > self.zero:
                if self.carbohydrate > 0:
                    sub_df = df[(df['에너지(㎉)'] >= self.kcal) & (df['단백질(g)'] >= self.protein) &
                                (df['지방(g)'] >= self.fat) & (df['탄수화물(g)'] >= self.carbohydrate)]
    context={'sub_df':sub_df.to_html(justify='center')}
    return render(request,'food/food_search_result.html',context)