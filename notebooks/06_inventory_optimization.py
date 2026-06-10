#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


forecast_df = pd.read_csv(
    "../data/forecast_predictions.csv"
)

forecast_df["Date"] = pd.to_datetime(
    forecast_df["Date"]
)

forecast_df.head()


# In[3]:


forecast_df["Demand_STD"] = (
    forecast_df
    .groupby(
        ["Store","Dept"]
    )["Weekly_Sales"]
    .transform("std")
)


# In[4]:


forecast_df[
[
"Store",
"Dept",
"Weekly_Sales",
"Demand_STD"
]
].head()


# In[5]:


z_score = 1.65
lead_time = 2

forecast_df["Safety_Stock"] = (

    z_score

    *

    forecast_df["Demand_STD"]

    *

    np.sqrt(lead_time)

)


# In[6]:


forecast_df["Average_Demand"] = (

    forecast_df

    .groupby(
        ["Store","Dept"]
    )["Predicted_Sales"]

    .transform("mean")

)


# In[7]:


forecast_df["Reorder_Point"] = (

    forecast_df["Average_Demand"]

    *

    lead_time

    +

    forecast_df["Safety_Stock"]

)


# In[8]:


ordering_cost = 100
holding_cost = 5

forecast_df["Annual_Demand"] = (

    forecast_df["Average_Demand"]

    *

    52

)


# In[9]:


forecast_df["EOQ"] = np.sqrt(

    (

        2

        *

        forecast_df["Annual_Demand"]

        *

        ordering_cost

    )

    /

    holding_cost

)


# In[10]:


forecast_df["Recommended_Order_Qty"] = (

    forecast_df["Predicted_Sales"]

    +

    forecast_df["Safety_Stock"]

)


# In[11]:


inventory_results = forecast_df[
[
"Store",
"Dept",
"Date",

"Predicted_Sales",

"Safety_Stock",

"Reorder_Point",

"EOQ",

"Recommended_Order_Qty"
]
]

inventory_results.head(20)


# In[12]:


inventory_results.to_csv(

    "../data/inventory_optimization_results.csv",

    index=False

)


# In[13]:


plt.figure(
    figsize=(10,6)
)

sns.histplot(

    inventory_results["Safety_Stock"],

    bins=50

)

plt.title(
    "Safety Stock Distribution"
)

plt.show()


# In[14]:


plt.figure(
    figsize=(10,6)
)

sns.histplot(

    inventory_results["EOQ"],

    bins=50

)

plt.title(
    "EOQ Distribution"
)

plt.show()


# In[15]:


inventory_results.sort_values(

    by="Safety_Stock",

    ascending=False

).head(10)


# In[16]:


inventory_results.sort_values(

    by="Recommended_Order_Qty",

    ascending=False

).head(10)

