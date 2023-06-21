import pandas as pd
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView

from blog.models import Post
from food.models import SearchFood, SearchTime


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


def food_result_view(request,pk):
    self = SearchFood.objects.get(pk=pk)
    df = pd.read_excel('food/foo.xlsx')
    if self.kcal > self.zero:
        if self.protein > self.zero:
            if self.fat > self.zero:
                if self.carbohydrate > self.zero:
                    sub_df = df[(df['에너지(㎉)'] >= self.kcal) & (df['단백질(g)'] >= self.protein) &
                                (df['지방(g)'] >= self.fat) & (df['탄수화물(g)'] >= self.carbohydrate)]
                else :
                    sub_df = df[(df['에너지(㎉)'] >= self.kcal) & (df['단백질(g)'] >= self.protein) &
                                (df['지방(g)'] >= self.fat) & (df['탄수화물(g)'] <= abs(self.carbohydrate))]
            else:
                if self.carbohydrate > self.zero:
                    sub_df = df[(df['에너지(㎉)'] >= self.kcal) & (df['단백질(g)'] >= self.protein) &
                                (df['지방(g)'] <= abs(self.fat)) & (df['탄수화물(g)'] >= self.carbohydrate)]
                else :
                    sub_df = df[(df['에너지(㎉)'] >= self.kcal) & (df['단백질(g)'] >= self.protein) &
                                (df['지방(g)'] <= abs(self.fat)) & (df['탄수화물(g)'] <= abs(self.carbohydrate))]
        else:
            if self.fat > self.zero:
                if self.carbohydrate > self.zero:
                    sub_df = df[(df['에너지(㎉)'] >= self.kcal) & (df['단백질(g)'] <= abs(self.protein)) &
                                (df['지방(g)'] >= self.fat) & (df['탄수화물(g)'] >= self.carbohydrate)]
                else:
                    sub_df = df[(df['에너지(㎉)'] >= self.kcal) & (df['단백질(g)'] <= abs(self.protein)) &
                                (df['지방(g)'] >= self.fat) & (df['탄수화물(g)'] <= abs(self.carbohydrate))]
            else:
                if self.carbohydrate > self.zero:
                    sub_df = df[(df['에너지(㎉)'] >= self.kcal) & (df['단백질(g)'] <= abs(self.protein)) &
                                (df['지방(g)'] <= abs(self.fat)) & (df['탄수화물(g)'] >= self.carbohydrate)]
                else:
                    sub_df = df[(df['에너지(㎉)'] >= self.kcal) & (df['단백질(g)'] <= abs(self.protein)) &
                                (df['지방(g)'] <= abs(self.fat)) & (df['탄수화물(g)'] <= abs(self.carbohydrate))]
    else:
        if self.protein > self.zero:
            if self.fat > self.zero:
                if self.carbohydrate > self.zero:
                    sub_df = df[(df['에너지(㎉)'] <= abs(self.kcal)) & (df['단백질(g)'] >= self.protein) &
                                (df['지방(g)'] >= self.fat) & (df['탄수화물(g)'] >= self.carbohydrate)]
                else:
                    sub_df = df[(df['에너지(㎉)'] <= abs(self.kcal)) & (df['단백질(g)'] >= self.protein) &
                                (df['지방(g)'] >= self.fat) & (df['탄수화물(g)'] <= abs(self.carbohydrate))]
            else:
                if self.carbohydrate > self.zero:
                    sub_df = df[(df['에너지(㎉)'] <= abs(self.kcal)) & (df['단백질(g)'] >= self.protein) &
                                (df['지방(g)'] <= abs(self.fat)) & (df['탄수화물(g)'] >= self.carbohydrate)]
                else:
                    sub_df = df[(df['에너지(㎉)'] <= abs(self.kcal)) & (df['단백질(g)'] >= self.protein) &
                                (df['지방(g)'] <= abs(self.fat)) & (df['탄수화물(g)'] <= abs(self.carbohydrate))]
        else:
            if self.fat > self.zero:
                if self.carbohydrate > self.zero:
                    sub_df = df[(df['에너지(㎉)'] <= abs(self.kcal)) & (df['단백질(g)'] <= abs(self.protein)) &
                                (df['지방(g)'] >= self.fat) & (df['탄수화물(g)'] >= self.carbohydrate)]
                else:
                    sub_df = df[(df['에너지(㎉)'] <= abs(self.kcal)) & (df['단백질(g)'] <= abs(self.protein)) &
                                (df['지방(g)'] >= self.fat) & (df['탄수화물(g)'] <= abs(self.carbohydrate))]
            else:
                if self.carbohydrate > self.zero:
                    sub_df = df[(df['에너지(㎉)'] <= abs(self.kcal)) & (df['단백질(g)'] <= abs(self.protein)) &
                                (df['지방(g)'] <= abs(self.fat)) & (df['탄수화물(g)'] >= self.carbohydrate)]
                else:
                    sub_df = df[(df['에너지(㎉)'] <= abs(self.kcal)) & (df['단백질(g)'] <= abs(self.protein)) &
                                (df['지방(g)'] <= abs(self.fat)) & (df['탄수화물(g)'] <= abs(self.carbohydrate))]



    context={'sub_df':sub_df.to_html(justify='center')}
    return render(request,'food/food_search_result.html',context)

def FoodMore(request):
    return render(request,'food/food_more.html')

class FoodTimeSearch(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = SearchTime
    fields = ['time']

    template_name = 'food/food_time_search.html'
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    #등록되고 staff 나 superuser여야함
    def form_valid(self, form):
        if self.request.user.is_authenticated and (self.request.user.is_superuser or self.request.user.is_staff):
            form.instance.author = self.request.user
            return super(FoodTimeSearch,self).form_valid(form)
        else:
            return redirect('/blog/')

def food_time_search_result(request,pk):
    md=Post
    total_kcal=0
    time=SearchTime.objects.get(pk=pk)
    model = Post.objects.filter(created_at__day=time.time)
    for i in model:
        total_kcal+=i.get_kcal_over_check_num()
    fatter=round(total_kcal/7200,5)
    model_dict={
        'model':model,
        'total':total_kcal,
        'fatter':fatter
    }

    return render(request,'food/food_time_search_result.html',model_dict)

