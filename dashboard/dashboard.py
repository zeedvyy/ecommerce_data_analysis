import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="E-Commerce Dashboard | Azegdita Vanaya Lerrick",
    layout="wide",
)

all_df = pd.read_csv("dashboard/main_data.csv", low_memory=False)
all_df.reset_index(inplace=True)

datetime_columns = ["order_purchase_timestamp", "order_approved_at", 
                    "order_delivered_carrier_date", "order_delivered_customer_date", 
                    "order_estimated_delivery_date"]
for column in datetime_columns:
    if column in all_df.columns:
        all_df[column] = pd.to_datetime(all_df[column])

st.title('E-Commerce Dashboard')

def total_revenue(df):
    return df['payment_value'].sum()

def monthly_orders_trend(df):
    monthly_orders_df = df.resample('ME', on='order_purchase_timestamp').size()

    plt.figure(figsize=(10, 6))
    sns.lineplot(x=monthly_orders_df.index, y=monthly_orders_df.values, marker='o')
    plt.title('Monthly Orders Trend')
    plt.xlabel('Month')
    plt.ylabel('Number of Orders')
    plt.grid(True)
    st.pyplot(plt)

def total_sales_by_category(df):
    sales_by_category = df.groupby('product_category_name')['payment_value'].sum().reset_index()
    sales_by_category = sales_by_category.sort_values(by='payment_value', ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=sales_by_category, x='payment_value', y='product_category_name', 
                hue='product_category_name', palette='viridis', legend=False)
    plt.title('Total Sales by Product Category')
    plt.xlabel('Total Sales')
    plt.ylabel('Product Category')
    st.pyplot(plt)

def average_rating_by_category(df):
    average_rating = df.groupby('product_category_name')['review_score'].mean().reset_index()
    average_rating = average_rating.sort_values(by='review_score', ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=average_rating, x='review_score', y='product_category_name', 
                hue='product_category_name', palette='magma', legend=False)
    plt.title('Average Rating by Product Category')
    plt.xlabel('Average Rating')
    plt.ylabel('Product Category')
    st.pyplot(plt)

def total_payments_by_type(df):
    payments_by_type = df['payment_type'].value_counts().reset_index()
    payments_by_type.columns = ['payment_type', 'count']

    plt.figure(figsize=(10, 6))
    sns.barplot(data=payments_by_type, x='payment_type', y='count', 
                hue='payment_type', palette='coolwarm', legend=False)
    plt.title('Total Payments by Payment Type')
    plt.xlabel('Payment Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    st.pyplot(plt)

def top_cities_by_orders(df):
    top_cities = df['customer_city'].value_counts().head(10)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_cities.values, y=top_cities.index, 
                hue=top_cities.index, palette='magma', legend=False)
    plt.title('Top 10 Cities by Number of Orders')
    plt.xlabel('Number of Orders')
    plt.ylabel('City')
    st.pyplot(plt)

def distribution_of_average_payment(df):
    average_payment = df['payment_value'].mean()
    
    plt.figure(figsize=(10, 6))
    sns.histplot(df['payment_value'], bins=50, kde=True, color='purple')
    plt.axvline(average_payment, color='red', linestyle='dashed', linewidth=1)
    plt.title('Distribution of Average Payment per Order')
    plt.xlabel('Payment Value (BRL)')
    plt.ylabel('Frequency')
    st.pyplot(plt)

def favorite_category(df):
    favorite = df.groupby('product_category_name')['review_score'].mean().reset_index()
    favorite = favorite.sort_values(by='review_score', ascending=False).head(1)

    st.subheader('Favorite Product Category')
    st.write(f'🏅 **Category:** {favorite["product_category_name"].values[0]}')
    st.write(f'⭐ **Average Rating:** {favorite["review_score"].values[0]:.2f}')

total_rev = total_revenue(all_df)
st.header(f'Total Revenue: {total_rev:.2f} BRL')

favorite_category(all_df)

with st.container():
    st.subheader('Monthly Orders Trend')
    monthly_orders_trend(all_df)

    st.subheader('Total Sales by Product Category')
    total_sales_by_category(all_df)

    st.subheader('Average Rating by Product Category')
    average_rating_by_category(all_df)

    st.subheader('Total Payments by Payment Type')
    total_payments_by_type(all_df)

    st.subheader('Top 10 Cities by Number of Orders')
    top_cities_by_orders(all_df)

    st.subheader('Distribution of Average Payment per Order')
    distribution_of_average_payment(all_df)