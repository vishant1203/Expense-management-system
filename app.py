import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import json
from add_update_UI import add_update_UI
from analytics_UI import analytics_UI
from analytics_by_months_UI import analytics_by_months_UI

from streamlit import header

API_URL="http://127.0.0.1:8000" #localhost: 127.0.0.1

st.title("Expense Management System")
tab1,tab2, tab3=st.tabs(["Add/Update","Analytics by Category", "Analytics by Months"]) #creation of tabs

with tab1:
    add_update_UI()
with tab2:
    analytics_UI()
with tab3:
    analytics_by_months_UI()