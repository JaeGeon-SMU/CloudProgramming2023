import pandas as pd
from django.db import models

# Create your models here.
class SearchTime(models.Model):
    time=models.IntegerField()

    def __str__(self):
        return self.time

    def get_absolute_url(self):
        return f'/food/more/{self.pk}'
class SearchFood(models.Model):
    kcal=models.FloatField(default=0,null=True)
    protein=models.FloatField(default=0,null=True)
    fat=models.FloatField(default=0,null=True)
    carbohydrate=models.FloatField(default=0,null=True)
    zero=models.FloatField(default=0,null=True)



    def get_absolute_url(self):
        return f'/food/search/{self.pk}'

    def get_fit_food(pk):
        self=SearchFood.objects.get(pk=pk)
        df = pd.read_excel('food/foo.xlsx')
        if self.kcal>self.zero:
            if self.protein>self.zero:
                if self.fat>self.zero:
                    if self.carbohydrate>0:
                        sub_df = df[(df['에너지(㎉)'] >= self.kcal) & (df['단백질(g)'] >= self.protein)&
                                (df['지방(g)'] >= self.fat)& (df['탄수화물(g)'] >= self.carbohydrate)]

        return sub_df

    def get_kcal(self):
        return float(self.kcal)

    def get_protein(self):
        return float(self.kcal)

    def get_fat(self):
        return float(self.fat)

    def get_carbohydrate(self):
        return float(self.carbohydrate)