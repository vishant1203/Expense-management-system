import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import json

from streamlit import header

API_URL="http://127.0.0.1:8000" #localhost: 127.0.0.1

st.title("Expense Management System")
tab1,tab2, tab3=st.tabs(["Add/Update","Analytics by Category", "Analytics by Months"]) #creation of tabs


with tab3:
    def analytics_by_months_UI():
        response=requests.get(f"{API_URL}/month_wise_expense")
        if response.status_code==200:
            expenses=response.json()
            #st.write(expenses)
        else:
            st.error("failed to retrieve any data")

        df=pd.DataFrame({
            'Month number': [expense['month_number'] for expense in expenses],
            'Month': [expense['month_name'] for expense in expenses],
            'Amount':[expense['total'] for expense in expenses]
        })
        st.subheader("Expense breakdown by months")
        st.bar_chart(data=df.set_index("Month")['Amount'], width=0, height=0, use_container_width=True)

        df=df.set_index("Month number")
        df['Amount']=df['Amount'].map("{:.2f}".format)
        df=st.table(df)