

import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import datetime
from utils.mapping import create_map
from utils.makers import get_uscpr_df

st.set_page_config(layout='wide')
st.title('Watermelon Parade Tracker')
col1, col2 = st.columns([1, 7])

df = get_uscpr_df()
# Use st.date_input to allow the user to select a date
with col1:
    st.subheader('Filters')
    select_date = st.checkbox('Date', False)
    if select_date:
        # Get the current year
        current_year = datetime.datetime.now().year
        # Add the current year to the 'Date' column values
        df['Date'] = df['Date'] + f' {current_year}'
        # Convert the 'Date' column to pandas datetime format if it's not already
        df['Date'] = pd.to_datetime(df['Date'])
        # Get the minimum and maximum dates from your DataFrame to set the bounds of the date_input widget
        min_date = df['Date'].min().date()
        max_date = df['Date'].max().date()
        
        selected_date = st.date_input('', min_value=min_date, max_value=max_date)
        # Convert selected_date to pandas datetime format to match the 'Date' column format
        selected_date = pd.to_datetime(selected_date)
        # Filter your DataFrame based on the selected date
        df = df[df['Date'] == selected_date]

    # Use st.date_input to allow the user to select a date
    select_state= st.checkbox('State', False)
    default_states = list(set(df['State']))
    if select_state:
        selected_state = st.selectbox('', default_states)
        # Convert selected_date to pandas datetime format to match the 'Date' column format

        # Filter your DataFrame based on the selected date
        df = df[df['State'] == selected_state]

m = create_map(df)
# Display the map in Streamlit
with col2:
    st.subheader('Events')
    folium_static(m)
    st.markdown(
    "Add event [here](https://forms.gle/aDR6GdSEWc6FCZt66)."
)


