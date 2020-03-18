import pandas as pd
import seaborn as sns
from matplotlib.pyplot import plot

obj1 = []
df = pd.Dataframe(obj1)

# Scatter plot ========================

scatter_plot = sns.scatterplot(data=df, x="nameofcolx", y="nameofcoly", style="summer", hue="summer")
plot.title("")
plot.xtitle("")
plot.ytitle("")

# Bar plot ========================

bar_plot = sns.barplot(data=df, x="nameofcolx", y="nameofcoly", style="summer", hue="summer")

# Line plot ========================

line_plot = sns.lineplot(data=df, x="nameofcolx", y=["nameofcoly1", "nameofcoly2"], style="summer", hue="summer")

# Count plot ========================

count_plot = sns.countplot(data=df, x="nameofcolx", style="summer", hue="summer")

# Heat Map ========================

heat_map = sns.heatmap("some_list", cmap=["blue", "red"])