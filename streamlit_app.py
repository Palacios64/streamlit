import streamlit_option_menu
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('https://raw.githubusercontent.com/Palacios64/Excel_Clase/refs/heads/main/Coffee%20Shop%20Sales%20(1).csv')

with open('waves.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# App title and subtitle
st.markdown('<p class="dashboard_title">App for Coffee Sales</p>', unsafe_allow_html=True)
st.markdown('<p class="dashboard_subtitle">Look at the information of coffee sales</p>', unsafe_allow_html=True)

# Horizontal menu
menu_selected = option_menu(
    None,
    ["Top 3 Stores", "KPI's markdowns", "Relationship quantity and unit price", "Sales by product", "Interactive Map"],
    icons=['house', 'cloud-upload', "list-task", 'gear', 'map'],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"background-color": "#B7A6F6"},
        "icon": {"color": "#802EF2", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#88A3E2"},
        "nav-link-selected": {"background-color": "#7A577A"},
    }
)

# Menu options
if menu_selected == "Top 3 Stores":
    st.subheader("Top 3 Stores by Total Sales Quantity")
    top_3_stores = df.groupby('store_location')['transaction_qty'].sum().nlargest(3)
    fig3 = px.bar(top_3_stores, x=top_3_stores.index, y=top_3_stores.values,
                  title="Top Stores by Total Sales Quantity")
    st.plotly_chart(fig3)

elif menu_selected == "KPI's markdowns":
    st.markdown("Key Performance Indicators")
    st.markdown("- **Total Products Sold:** %d" % df['transaction_qty'].sum())
    most_visited_store = df['store_location'].mode()[0]
    st.markdown("- **Most Visited Store:** %s" % most_visited_store)

elif menu_selected == "Relationship quantity and unit price":
    st.subheader("Relationship between Transaction Quantity and Unit Price")
    sns.scatterplot(data=df, x='transaction_qty', y='unit_price', color='purple', edgecolor='w')
    plt.title('Quantity vs Unit Price')
    st.pyplot(plt)

elif menu_selected == "Sales by product":
    st.subheader("Total Sales by Product Category")
    sales_by_category = df.groupby('product_category')['transaction_qty'].sum().sort_values()
    sales_by_category.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Total Sales by Product Category')
    plt.xlabel('Product Category')
    plt.ylabel('Total Transaction Quantity')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)

elif menu_selected == "Interactive Map":
    st.subheader("Interactive Map of Sales by Store Location")
    
    # Group data by store_location
    sales_map_data = df.groupby('store_location', as_index=False).agg({
        'transaction_qty': 'sum',
        'unit_price': 'mean'
    })
    
  
    location_coords = {
        'Lower Manhattan': [40.722, -74.0059],
        'Upper Manhattan': [40.826, -73.944],
    }
    sales_map_data[['latitude', 'longitude']] = sales_map_data['store_location'].apply(
        lambda loc: location_coords.get(loc, [None, None])
    ).tolist()
    
    # Create map
    fig_map = px.scatter_mapbox(
        sales_map_data,
        lat='latitude',
        lon='longitude',
        size='transaction_qty',
        hover_name='store_location',
        color='unit_price',
        size_max=15,
        zoom=10,
        title="Store Sales Locations"
    )
    fig_map.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig_map)
