# %%
import pandas as pd
import numpy as np
from ggly import ggplot, aes, load_data

diamonds = load_data("diamonds.csv")
diamonds = diamonds.sample(500)

(
    ggplot(diamonds, aes(x='carat', y='price', color='cut'))
    .geom_point(alpha=0.7)
    .geom_smooth(method='lm', se=False, color='black')
)


# %%
# Example 1: Basic Scatter Plot with Color
print("Creating scatter plot...")
(
    ggplot(diamonds, aes(x='carat', y='price', color='cut'))
    .geom_point(alpha=0.7)
    .labs(
        title="Diamond Prices",
        subtitle="Price vs. Carat by Cut Quality",
        x="Carat",
        y="Price (USD)",
        color="Cut Quality"
    )
    .theme_ggplot2()
    .show()
)



# %%

# Example 2: Line Chart
print("Creating line chart...")
economics = pd.read_csv('../data/economics.csv')
economics['date'] = pd.to_datetime(economics['date'])

(
    ggplot(economics, aes(x='date', y='unemploy'))
    .geom_line(color='red')
    .geom_point(color='green')
    .show()
)

# %%

# Example 3: Bar Chart
print("Creating bar chart...")
mpg = pd.read_csv('../data/mpg.csv')

(
    ggplot(mpg, aes(x='class'))
    .geom_bar(mapping=aes(fill='drv'), position='stack')
    .labs(
        title="Car Types",
        subtitle="Count by Class",
        x="Class",
        y="Count"
    )
    .theme_minimal()
    .show()
)

# %%

# Example 4: Boxplot
print("Creating boxplot...")
(
    ggplot(mpg, aes(x='class', y='hwy'))
    .geom_boxplot()
    .labs(
        title="Highway MPG by Car Class",
        x="Class",
        y="Highway MPG"
    )
    .coord_flip()  # Flip coordinates for horizontal boxplot
    .theme_minimal()
    .show()
)

# %%

# Example 5: Histogram
print("Creating histogram...")
(
    ggplot(diamonds, aes(x='price'))
    .geom_histogram(bins=30, fill='steelblue', alpha=0.7)
    .labs(
        title="Diamond Price Distribution",
        x="Price (USD)",
        y="Count"
    )
    .theme_minimal()
    .show()
)

# %%

# Example 6: Facet Wrap
print("Creating facet wrap plot...")
(
    ggplot(mpg, aes(x='displ', y='hwy', color='drv'))
    .geom_point()
    .facet_wrap('class', nrow=2)
    .labs(
        title="Highway MPG vs. Displacement",
        subtitle="By Car Class and Drive Type",
        x="Displacement (L)",
        y="Highway MPG",
        color="Drive Type"
    )
    .theme_minimal()
    .show()
)

# %%
print("Creating facet grid plot...")
(
    ggplot(diamonds, aes(x='carat', y='price', color='cut'))
    .geom_point(alpha=0.7)
    .geom_line()
    #geom_smooth(method='lm', se=False, color='black')
    .facet_grid(rows='cut', cols='clarity')
    .theme_ggplot2()
    .show()
)
# %%
