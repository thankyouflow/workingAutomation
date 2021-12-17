import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rc("font", family="Malgun Gothic") # Windows
plt.rc("axes", unicode_minus=False)

# test
pd.Series([1,3,5,-7,9]).plot.bar(title="한글 제목")

file_name = '/Users/tyflow/Downloads/coronic.csv'

df = pd.read_csv(file_name, encoding='cp949')

df = df.sort_values(by="연번", ascending=False)
df.head()

print(df.head())