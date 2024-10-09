E-Commerce Data Analysis
---
This project aims to analyze e-commerce data from the Brazilian E-Commerce dataset, focusing on answering key business questions that can help improve business strategies and operations. The dataset contains detailed information about orders made at Olist, a Brazilian marketplace. It includes customer behavior, order details, payments, and reviews. 
---

### Business Questions Addressed:
1. What product categories have the highest and lowest total sales?
2. What is the average product rating by category?
3. What is the most commonly used payment method by customers?
4. Which city has the highest number of orders?
5. Are there any seasonal trends in the number of orders per month?
6. What is the average delivery time for products?
7. What is the average customer expenditure per order?
8. Is there a relationship between product category and review rating?
9. What is the best-selling product category?
10. Are there differences in delivery time based on payment methods?

Dataset
The dataset used for this analysis was sourced from Kaggle and can be accessed by clicking [here](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). It contains multiple CSV files that cover various aspects of the e-commerce process, such as orders, products, customers, payments, and reviews.

## How to Run the AppFollow these steps to set up the environment and run the Streamlit application:

### Setup Environment (Shell/Terminal):
git clone https://github.com/zeedvyy/ecommerce_data_analysis.git
cd ecommerce_data_analysis
pipenv install
pipenv shell

### Run Streamlit App
python -m streamlit run dashboard/dashboard.py