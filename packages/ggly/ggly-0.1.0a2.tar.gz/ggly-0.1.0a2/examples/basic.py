# %%

import pandas as pd
from ggly import ggplot, aes, load_data

# Sample data
mpg = load_data("mpg.csv")

# Create a scatter plot with color grouped by class
(
    ggplot(mpg, aes(x='cty', y='hwy', color='class'))
    .geom_point(size=10)
    .labs(
        title="Fuel consumption",
        subtitle="Highway Mileage vs City Mileage",
        x="City Mileage",
        y="Highway Mileage",
        color="Class of vehicles"
    )
    #.theme_minimal()
    .show()
)

# %%
# Create a bar chart
(
    ggplot(mpg, aes(x='class'))
    .geom_bar()
    .labs(
        title="Vehicle Classes",
        subtitle="Count by class",
        x="Class",
        y="Count"
    )
    .facet_wrap('~class')
    .theme_minimal()
    .show()
)

# %%
