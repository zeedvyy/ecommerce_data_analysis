import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu
import os
from babel.numbers import format_currency

st.set_page_config(
    page_title="E-Commerce Dashboard | Azegdita Vanaya Lerrick",
    layout="wide",
)

# Load data
all_df = pd.read_csv("dashboard/main_data.csv", low_memory=False)
all_df.reset_index(inplace=True)

# Parse date columns
datetime_columns = ["order_purchase_timestamp", "order_approved_at", 
                    "order_delivered_carrier_date", "order_delivered_customer_date", 
                    "order_estimated_delivery_date"]
for column in datetime_columns:
    if column in all_df.columns:
        all_df[column] = pd.to_datetime(all_df[column])

# Sidebar Menu for Year Selection
with st.sidebar:
    selected = option_menu(
        menu_title="Olist Dashboard Analysis",
        options=["Monthly Orders Trend", "Total Sales by Product Category", "Average Rating by Product Category", "Customer Distribution", "Time Analysis", "Sales and Product by City"],
        default_index=0,
    )

# Filter Data for Selected Year
if selected == "Monthly Orders Trend":
    st.title("Monthly Orders Trend")
    # Sidebar for Year Selection
    year_selected = st.sidebar.selectbox("Select Year", ["2016", "2017", "2018"], index=0)
    if year_selected == "2016":
        year_df = all_df[all_df['order_purchase_timestamp'].dt.year == 2016]
    elif year_selected == "2017":
        year_df = all_df[all_df['order_purchase_timestamp'].dt.year == 2017]
    else:
        year_df = all_df[all_df['order_purchase_timestamp'].dt.year == 2018]

    # Monthly Orders Trend Visualization
    def monthly_orders_trend(df):
        monthly_orders_df = df.resample('M', on='order_purchase_timestamp').size()

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=monthly_orders_df.index,
            y=monthly_orders_df.values,
            mode='lines+markers',
            marker=dict(color='blue', size=8),
            line=dict(width=3),
        ))

        fig.update_layout(
            title="Monthly Orders Trend",
            xaxis=dict(
                title="Month",
                titlefont=dict(size=14),
                tickfont=dict(size=12),
            ),
            yaxis=dict(
                title="Number of Orders",
                titlefont=dict(size=14),
                tickfont=dict(size=12),
            ),
            width=650,
            height=400,
        )
        st.plotly_chart(fig)

    # Show Monthly Orders Trend
    monthly_orders_trend(year_df)

elif selected == "Total Sales by Product Category":
    st.title("Total Sales by Product Category")

    # Nested option menu for "Top-selling" and "Worst-selling" categories
    sales_category = option_menu(
        menu_title="Sales Category",
        options=["Top-selling Category", "Worst-selling Category"],
        default_index=0,
        orientation="horizontal"
    )

    # Function to calculate total sales by product category
    def df_product_sales_by_category(df):
        # Group data by product category and sum the sales
        df_category_sales = df.groupby(by="product_category_name").agg({
            "payment_value": "sum",
        }).reset_index().sort_values(by="payment_value", ascending=False)
        return df_category_sales

    # Function to calculate top-selling categories
    def df_top_selling_category(df):
        df_category_sales = df_product_sales_by_category(df)
        return df_category_sales.head(10)

    # Function to calculate worst-selling categories
    def df_worst_selling_category(df):
        df_category_sales = df_product_sales_by_category(df)
        return df_category_sales.tail(10)

    if sales_category == "Top-selling Category":
        st.subheader("Top-selling Categories Over 2016 - 2018")

        # Get the sales data by product category for top-selling
        df_category_sales = df_top_selling_category(all_df)

        with st.container():
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=df_category_sales['product_category_name'],
                y=df_category_sales['payment_value'],
                marker=dict(
                    color='rgb(173, 216, 230)',  # Set color here
                ),
            ))

            # Use zip to iterate over the data correctly
            for category, value in zip(df_category_sales['product_category_name'], df_category_sales['payment_value']):
                fig.add_annotation(
                    x=category,
                    y=value,
                    text=str(value),
                    font=dict(
                        size=10,
                        color='white',  # Set text color here
                    ),
                    showarrow=False,
                    textangle=0,
                    align='center',
                    yshift=10
                )

            fig.update_layout(
                title='Top-selling Product Categories',
                xaxis=dict(
                    title='Product Category',
                    tickangle=45,
                    tickfont=dict(
                        size=12,
                    ),
                    automargin=True,
                ),
                yaxis=dict(
                    title='Total Sales',
                    tickformat='plain',
                    tickfont=dict(
                        size=12,
                    ),
                ),
                width=800,
                height=500,
                showlegend=False,
            )

            st.plotly_chart(fig)

    elif sales_category == "Worst-selling Category":
        st.subheader("Worst-selling Categories Over 2016 - 2018")

        # Get the sales data by product category for worst-selling
        df_category_sales = df_worst_selling_category(all_df)

        with st.container():
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=df_category_sales['product_category_name'],
                y=df_category_sales['payment_value'],
                marker=dict(
                    color='rgb(173, 216, 230)',  # Set color here
                ),
            ))

            # Use zip to iterate over the data correctly
            for category, value in zip(df_category_sales['product_category_name'], df_category_sales['payment_value']):
                fig.add_annotation(
                    x=category,
                    y=value,
                    text=str(value),
                    font=dict(
                        size=10,
                        color='white',  # Set text color here
                    ),
                    showarrow=False,
                    textangle=0,
                    align='center',
                    yshift=10
                )

            fig.update_layout(
                title='Worst-selling Product Categories',
                xaxis=dict(
                    title='Product Category',
                    tickangle=45,
                    tickfont=dict(
                        size=12,
                    ),
                    automargin=True,
                ),
                yaxis=dict(
                    title='Total Sales',
                    tickformat='plain',
                    tickfont=dict(
                        size=12,
                    ),
                ),
                width=800,
                height=500,
                showlegend=False,
            )

            st.plotly_chart(fig)

elif selected == "Average Rating by Product Category":
    st.title("Average Rating by Product Category")

    # Nested option menu for "Top-rated" and "Worst-rated" categories
    rating_category = option_menu(
        menu_title="Rating Category",
        options=["Top-rated Category", "Worst-rated Category"],
        default_index=0,
        orientation="horizontal"
    )

    # Function to calculate average rating by product category
    def df_average_rating_by_category(df):
        df_avg_rating = df.groupby('product_category_name')['review_score'].mean().reset_index()
        df_avg_rating = df_avg_rating.sort_values(by='review_score', ascending=False)
        return df_avg_rating

    # Get the average rating by category
    df_avg_rating = df_average_rating_by_category(all_df)

    if rating_category == "Top-rated Category":
        st.subheader("Top-rated Product Categories")

        # Get the top-rated categories
        top_rated_category = df_avg_rating.head(10)

        with st.container():
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=top_rated_category['product_category_name'],
                y=top_rated_category['review_score'],
                marker=dict(color='rgb(0, 128, 0)'),  # Green for top-rated categories
            ))

            # Annotate each bar with the average rating value
            for category, value in zip(top_rated_category['product_category_name'], top_rated_category['review_score']):
                fig.add_annotation(
                    x=category,
                    y=value,
                    text=f"{value:.2f}",
                    font=dict(size=10, color='white'),
                    showarrow=False,
                    textangle=0,
                    align='center',
                    yshift=10
                )

            fig.update_layout(
                title='Top-rated Product Categories',
                xaxis=dict(
                    title='Product Category',
                    tickangle=45,
                    tickfont=dict(size=12),
                    automargin=True,
                ),
                yaxis=dict(
                    title='Average Rating',
                    tickfont=dict(size=12),
                ),
                width=800,
                height=500,
                showlegend=False,
            )

            st.plotly_chart(fig)

    elif rating_category == "Worst-rated Category":
        st.subheader("Worst-rated Product Categories")

        # Get the worst-rated categories
        worst_rated_category = df_avg_rating.tail(10)

        with st.container():
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=worst_rated_category['product_category_name'],
                y=worst_rated_category['review_score'],
                marker=dict(color='rgb(255, 0, 0)'),  # Red for worst-rated categories
            ))

            # Annotate each bar with the average rating value
            for category, value in zip(worst_rated_category['product_category_name'], worst_rated_category['review_score']):
                fig.add_annotation(
                    x=category,
                    y=value,
                    text=f"{value:.2f}",
                    font=dict(size=10, color='white'),
                    showarrow=False,
                    textangle=0,
                    align='center',
                    yshift=10
                )

            fig.update_layout(
                title='Worst-rated Product Categories',
                xaxis=dict(
                    title='Product Category',
                    tickangle=45,
                    tickfont=dict(size=12),
                    automargin=True,
                ),
                yaxis=dict(
                    title='Average Rating',
                    tickfont=dict(size=12),
                ),
                width=800,
                height=500,
                showlegend=False,
            )

            st.plotly_chart(fig)
    
    # Add Rating and Review Analysis
    st.subheader("Rating and Review Analysis")

    # Top 5 Products with the Highest Rating
    avg_rating_df = all_df.groupby(['product_id', 'product_category_name']).agg({'review_score': 'mean'}).reset_index()
    top_rated_products = avg_rating_df.sort_values(by='review_score', ascending=False).head(5)
    st.write("Top 5 Products with the Highest Ratings:")
    st.table(top_rated_products[['product_id', 'product_category_name', 'review_score']])

    # Rating Distribution
    rating_dist_df = all_df.groupby('review_score').agg({'order_id': 'nunique'}).reset_index()
    rating_dist_df.columns = ['Review Score', 'Order Count']

    rating_fig = go.Figure()

    rating_fig.add_trace(go.Bar(
        x=rating_dist_df['Review Score'],
        y=rating_dist_df['Order Count'],
        name='Order Count',
        marker=dict(color='rgb(102, 205, 170)'),
    ))

    rating_fig.update_layout(
        title="Rating Distribution",
        xaxis=dict(title='Review Score'),
        yaxis=dict(title='Order Count'),
        width=800,
        height=500,
    )

    st.plotly_chart(rating_fig)


elif selected == "Customer Distribution":
    st.title("Customer Distribution")
    
    # Dropdown for year selection
    year_selected = st.sidebar.selectbox("Select Year", ["2016", "2017", "2018"], index=0)

    # Filter Data for Selected Year
    if year_selected == "2016":
        year_df = all_df[all_df['order_purchase_timestamp'].dt.year == 2016]
    elif year_selected == "2017":
        year_df = all_df[all_df['order_purchase_timestamp'].dt.year == 2017]
    else:
        year_df = all_df[all_df['order_purchase_timestamp'].dt.year == 2018]
    
    # Customer Distribution by City
    city_df = year_df.groupby('customer_city').agg({'customer_id': 'nunique'}).reset_index()
    city_df.columns = ['City', 'Customer Count']

    # Sort the cities by customer count
    sorted_city_df = city_df.sort_values(by='Customer Count', ascending=False)
    
    # Top Customers and Worst Customers
    top_customers = sorted_city_df.head(5)  # Top 5 cities
    worst_customers = sorted_city_df.tail(5)  # Worst 5 cities

    # Create visualization for customer distribution
    fig = go.Figure()

    # Add trace for top customers
    fig.add_trace(go.Bar(
        x=top_customers['City'],
        y=top_customers['Customer Count'],
        name="Top Customers",
        marker=dict(color='rgb(102, 205, 170)'),
    ))

    # Add trace for worst customers
    fig.add_trace(go.Bar(
        x=worst_customers['City'],
        y=worst_customers['Customer Count'],
        name="Worst Customers",
        marker=dict(color='rgb(255, 99, 71)'),
    ))

    # Annotate bars
    for city, count in zip(top_customers['City'], top_customers['Customer Count']):
        fig.add_annotation(
            x=city,
            y=count,
            text=str(count),
            font=dict(size=12, color='white'),
            showarrow=False,
            textangle=0,
            align='center',
            yshift=10
        )

    for city, count in zip(worst_customers['City'], worst_customers['Customer Count']):
        fig.add_annotation(
            x=city,
            y=count,
            text=str(count),
            font=dict(size=12, color='white'),
            showarrow=False,
            textangle=0,
            align='center',
            yshift=10
        )

    # Update layout for the plot
    fig.update_layout(
        title=f"Customer Distribution for {year_selected}",
        xaxis=dict(title='City', tickangle=45),
        yaxis=dict(title='Customer Count'),
        barmode='group',  # Display bars side by side
        width=800,
        height=500,
    )
    
    st.plotly_chart(fig)

    # Segmentasi Pembelian Berdasarkan Metode Pembayaran
    payment_method_df = year_df.groupby('payment_type').agg({'order_id': 'nunique'}).reset_index()
    payment_method_df.columns = ['Payment Type', 'Purchase Count']

    st.subheader(f"Purchase Segmentation Based on Payment Method ({year_selected})")
    payment_fig = go.Figure()

    payment_fig.add_trace(go.Pie(
        labels=payment_method_df['Payment Type'],
        values=payment_method_df['Purchase Count'],
        hole=0.3,
        marker=dict(colors=['rgb(102, 205, 170)', 'rgb(255, 99, 71)', 'rgb(255, 215, 0)', 'rgb(70, 130, 180)']),
    ))

    st.plotly_chart(payment_fig)

    # Rata-rata Pengeluaran per Pelanggan
    avg_spending_df = year_df.groupby('customer_id').agg({'payment_value': 'sum'}).reset_index()
    avg_spending_per_customer = avg_spending_df['payment_value'].mean()

    st.subheader(f"Average Spend per Customer ({year_selected})")
    st.write(f"Average Spend per Customer is: {avg_spending_per_customer:.2f}")


    # # Analisis Rating dan Review
    # avg_rating_df = year_df.groupby('product_id').agg({'review_score': 'mean'}).reset_index()
    # top_rated_products = avg_rating_df.sort_values(by='review_score', ascending=False).head(5)

    # st.subheader(f"Rating and Review Analysis ({year_selected})")
    # st.write("Top 5 Products with the Highest Rating::")

    # # Create a table or visualization for top-rated products
    # st.write(top_rated_products[['product_id', 'review_score']])

    # # Visualize the rating distribution
    # rating_dist_df = year_df.groupby('review_score').agg({'order_id': 'nunique'}).reset_index()
    # rating_dist_df.columns = ['Review Score', 'Order Count']

    # rating_fig = go.Figure()

    # rating_fig.add_trace(go.Bar(
    #     x=rating_dist_df['Review Score'],
    #     y=rating_dist_df['Order Count'],
    #     marker=dict(color='rgb(102, 205, 170)'),
    # ))

    # st.plotly_chart(rating_fig)

elif selected == "Time Analysis":
    st.title("Time Based Sales Analysis")
    
    # Rata-rata Waktu Pengiriman (Tepat Waktu vs Terlambat)
    st.subheader("Average Delivery Time (On Time vs Late)")
    
    # Menghitung selisih waktu antara pengiriman yang diestimasi dan yang sebenarnya
    all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])
    all_df['order_delivered_customer_date'] = pd.to_datetime(all_df['order_delivered_customer_date'])
    all_df['order_estimated_delivery_date'] = pd.to_datetime(all_df['order_estimated_delivery_date'])
    
    # Menghitung selisih waktu pengiriman
    all_df['delivery_time_diff'] = (all_df['order_delivered_customer_date'] - all_df['order_estimated_delivery_date']).dt.days
    
    # Label pengiriman tepat waktu atau terlambat
    all_df['delivery_status'] = all_df['delivery_time_diff'].apply(lambda x: 'On time' if x <= 0 else 'Late')
    
    # Visualisasi pengiriman tepat waktu dan terlambat
    delivery_status_count = all_df['delivery_status'].value_counts()
    fig = go.Figure(data=[go.Bar(
        x=delivery_status_count.index,
        y=delivery_status_count.values,
        marker=dict(color=['rgb(102, 205, 170)', 'rgb(255, 99, 71)'])
    )])

    fig.update_layout(
        title="On Time vs Late Delivery",
        xaxis=dict(title="Delivery Status"),
        yaxis=dict(title="Order Quantity"),
        width=800,
        height=500
    )
    st.plotly_chart(fig)

    # Waktu Pembelian dan Rating Produk
    st.subheader("Purchase Time and Product Ratings")
    
    # Menghitung rata-rata rating berdasarkan jam pembelian
    all_df['hour_of_purchase'] = all_df['order_purchase_timestamp'].dt.hour
    purchase_rating = all_df.groupby('hour_of_purchase')['review_score'].mean().reset_index()
    
    # Visualisasi rating berdasarkan jam pembelian
    fig = go.Figure(data=[go.Scatter(
        x=purchase_rating['hour_of_purchase'],
        y=purchase_rating['review_score'],
        mode='lines+markers',
        marker=dict(color='rgb(255, 99, 71)')
    )])

    fig.update_layout(
        title="Average Product Rating Based on Time of Purchase",
        xaxis=dict(title="Purchase Time"),
        yaxis=dict(title="Average Rating"),
        width=800,
        height=500
    )
    st.plotly_chart(fig)

    # Customer Purchase Time (Pagi, Siang, Malam)
    st.subheader("Customer Purchase Time (Morning, Afternoon, Evening)")
    
    # Membuat kategori waktu pembelian
    def categorize_purchase_time(hour):
        if 0 <= hour < 6:
            return 'Malam'
        elif 6 <= hour < 12:
            return 'Pagi'
        elif 12 <= hour < 18:
            return 'Siang'
        else:
            return 'Sore'
    
    all_df['purchase_time_of_day'] = all_df['hour_of_purchase'].apply(categorize_purchase_time)
    
    # Visualisasi distribusi waktu pembelian
    purchase_time_distribution = all_df['purchase_time_of_day'].value_counts()
    fig = go.Figure(data=[go.Bar(
        x=purchase_time_distribution.index,
        y=purchase_time_distribution.values,
        marker=dict(color='rgb(102, 205, 170)')
    )])

    fig.update_layout(
        title="Purchase Time Distribution",
        xaxis=dict(title="Purchase Time"),
        yaxis=dict(title="Order Quantity"),
        width=800,
        height=500
    )
    st.plotly_chart(fig)

    # Pengaruh Hari dalam Minggu Terhadap Penjualan
    st.subheader("The Effect of the Day of the Week on Sales")
    
    # Mengambil hari dalam minggu
    all_df['day_of_week'] = all_df['order_purchase_timestamp'].dt.day_name()
    day_of_week_sales = all_df.groupby('day_of_week')['order_id'].count().reset_index()
    
    # Urutkan berdasarkan hari dalam minggu
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_of_week_sales['day_of_week'] = pd.Categorical(day_of_week_sales['day_of_week'], categories=day_order, ordered=True)
    day_of_week_sales = day_of_week_sales.sort_values('day_of_week')
    
    # Visualisasi pengaruh hari dalam minggu
    fig = go.Figure(data=[go.Bar(
        x=day_of_week_sales['day_of_week'],
        y=day_of_week_sales['order_id'],
        marker=dict(color='rgb(255, 99, 71)')
    )])

    fig.update_layout(
        title="The Effect of the Day of the Week on Sales",
        xaxis=dict(title="Day of Week"),
        yaxis=dict(title="Order Quantity"),
        width=800,
        height=500
    )
    st.plotly_chart(fig)

elif selected == "Sales and Product by City":
    st.title("Total Sales and Product Sold by City")
    
    # Group by customer_city to calculate total sales and units sold for all years
    city_sales_df = all_df.groupby('customer_city').agg({
        'payment_value': 'sum',  # Total sales
        'order_item_id': 'sum'   # Total units sold
    }).reset_index()
    
    city_sales_df.columns = ['City', 'Total Sales', 'Product Sold']

    # Sort the data by total sales
    sorted_city_sales_df = city_sales_df.sort_values(by='Total Sales', ascending=False)

    # Create a dual-axis chart with a bar chart for Total Sales and a line chart for Units Sold
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add trace for total sales (Primary y-axis) - Bar chart
    fig.add_trace(go.Bar(
        x=sorted_city_sales_df['City'],
        y=sorted_city_sales_df['Total Sales'],
        name="Total Sales",
        marker=dict(color='rgb(102, 205, 170)'),
    ), secondary_y=False)

    # Add trace for units sold (Secondary y-axis) - Line chart
    fig.add_trace(go.Scatter(
        x=sorted_city_sales_df['City'],
        y=sorted_city_sales_df['Product Sold'],
        name="Product Sold",
        mode='lines+markers',
        marker=dict(color='rgb(255, 99, 71)'),
    ), secondary_y=True)

    # Update layout for the plot
    fig.update_layout(
        title="Total Sales and Product Sold by City",
        xaxis=dict(title='City', tickangle=45),
        barmode='group',  # Display bars side by side
        width=800,
        height=500,
    )

    # Update y-axes titles
    fig.update_yaxes(title_text="Total Sales", secondary_y=False)
    fig.update_yaxes(title_text="Product Sold", secondary_y=True)
    
    st.plotly_chart(fig)
