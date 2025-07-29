from datachampsai import DCAI

doc = '''
Q: List the customers which are degrowing in Quantity but growing in rate in 2024?
Hint: See the growth percentage from 2023 to 2024 for each customer for 
1) Quantity growth = Q
2) Total Sales Amount growth = A
Then isolate companies where Q<0 and A>0 

###
List the customers which are growing in Quantity but degrowing in rate in 2024?

###
Which are the new launches (product description) with value in 2024?
Hint: products with sales in 2024 but NO SALES before 2024.

###
Which are the discontinued portfolios (product description) with value in 2024?
Hint: Products with no sales in 2024 but sales in 2023.

###
What is the sales value of customers lost in 2024 for Domestic category?
Hint: Isolate customers with sales in 2023 But NO SALES in 2024 in domestic category,
Then calculate the total sales amount for them.

###
What is the sales value of new customers gained in 2024 for Export category?
Hint: Isolate the customers who had sales in 2024 but no sales before 2024
Filter that for the export category, and get their total sales.

###
What Sales Value of customers for the month of May 23 have sales rate less than the average rate charged to that customer during the year ?
Hint: Use quantity weighted average to calculate the sales rate for 2023 and May 2023. 
Finally, get the total sales value of the customers with year_price > may_price

###
What Sales Value of customers for the month of May 23 have sales quantity less than 50% of the average monthly quantity sold to that customer during the year?
Hint: Isolate customers where (total_quantity_in_2023 / 12 ) * 0.5 is greater than total_quantity_in_May23.
Then give the sum of their total sales so far.

###
What is the Quantity CAGR of Sprocket in Domestic sales category from 2021 to 2024?
Hint: find the total quantity of the Sprocket domestic sale in 2021 AND 2024. Then calculate the CAGR (years = 2024-2021 = 3)

###
What is the Value CAGR of Cylinder in Domestic sales category from 2021 to 2024?
Hint: find the total sales amount of Cylinder domestic sale in 2021 AND 2024. Then calculate the CAGR (years = 2024-2021 = 3)

###
Which product shows the highest standard deviation in the number of repeat customers purchasing it?
Hint: For each product, calculate the total number of customers purchasing it in each year available. Then find the standard deviation across it.
What are the variances in billed quantity for the top 5 products with highest revenue contribution?'''

dc = DCAI('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', doc)

response = dc.rephrase_query(
    "what were the new launches in 2022?",
    chat_history=["Hello", "Hi there"]
)

print(response)
