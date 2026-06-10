CREATE TABLE sales (

    Store INT,

    Dept INT,

    Date DATE,

    Weekly_Sales FLOAT,

    IsHoliday BOOLEAN

);



CREATE TABLE features (

    Store INT,

    Date DATE,

    Temperature FLOAT,

    Fuel_Price FLOAT,

    MarkDown1 FLOAT,

    MarkDown2 FLOAT,

    MarkDown3 FLOAT,

    MarkDown4 FLOAT,

    MarkDown5 FLOAT,

    CPI FLOAT,

    Unemployment FLOAT,

    IsHoliday BOOLEAN

);



CREATE TABLE stores (

    Store INT PRIMARY KEY,

    Type VARCHAR(5),

    Size INT

);



CREATE TABLE forecast_results (

    Store INT,

    Dept INT,

    Forecast_Date DATE,

    Forecasted_Demand FLOAT,

    Lower_CI FLOAT,

    Upper_CI FLOAT

);



CREATE TABLE inventory_recommendations (

    Store INT,

    Dept INT,

    Forecasted_Demand FLOAT,

    Safety_Stock FLOAT,

    Reorder_Point FLOAT,

    EOQ FLOAT,

    Inventory_Gap FLOAT,

    Recommended_Order FLOAT

);