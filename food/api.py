import pandas as pd

df = pd.read_excel('foo.xlsx')
kcal=300
protein=33.4
fat=8.49
tansu=39
print(df)


sub_df = df[(df['에너지(㎉)'] >= kcal) & (df['단백질(g)'] >= protein)&
                                    (df['지방(g)'] >= fat)& (df['탄수화물(g)'] >= tansu)]
html=sub_df.to_html()
print(html)