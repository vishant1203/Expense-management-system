import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import json

from streamlit import header

API_URL="http://127.0.0.1:8000" #localhost: 127.0.0.1

st.title("Expense Management System")
tab1,tab2=st.tabs(["Add/Update","Analytics"]) #creation of tabs


with tab2:
    def analytics_UI():
        col1, col2=st.columns(2)
        with col1:
            start_date=st.date_input("Start_date",datetime(2024,8,2))
        with col2:
            end_date=st.date_input("End_date",datetime(2024,8,2))
        payload={
                "start_date": f"{start_date}",
                "end_date": f"{end_date}"
            }

        response=requests.post(f"{API_URL}/analytics/", json=payload)
        #st.write(response.json())
        response=response.json()
        df = pd.DataFrame({
            'Category':[key for key,value in response.items()],
            'Total':[round(value['Total'],2) for key, value in response.items()],
            'Percentage':[round(value['percentage'],1) for key, value in response.items()]
        })

        df_sorted=df.sort_values(by='Percentage', ascending=False)
        st.subheader("Expense breakdown by category in bar chart form")
        st.bar_chart(data=df_sorted.set_index("Category")['Percentage'],width=0, height=0, use_container_width=True)
        #st.bar_chart(data=df_sorted.set_index("Category")['Percentage'], width=0, height=0, use_container_width=True)
        #use_container_width= This tells Streamlit to make the chart stretch to fill the width of its container (like a column or page).


        st.subheader("Expense breakdown by category")
        df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format) # This converts the numbers in the "Total" and "Percentage" columns into strings formatted with exactly 2 decimal places.
        df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)
        df = st.table(df_sorted)