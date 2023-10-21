import streamlit as st 
from utils.makers import get_sam_df, get_uscpr_df
import pandas as pd
import datetime
from streamlit_folium import folium_static
from utils.sam_mapping import create_map 

st.set_page_config(layout='wide')

st.title('Watermelon Parade Tracker')



col1, col2 = st.columns([1, 7])


with col1:
    update_latest = st.button('Update')
if update_latest:
    sam_df = get_sam_df()
    uscpr_df = get_uscpr_df()
    sam_df.to_csv('data/sam_df.csv')
    uscpr_df.to_csv('data/uscpr_df')
else: 
    try:
        sam_df = pd.read_csv('data/sam_df.csv')
        uscpr_df = pd.read_csv('data/uscpr_df.csv')
    except:
        sam_df = get_sam_df()
        uscpr_df = get_uscpr_df()
        sam_df.to_csv('data/sam_df.csv')
        uscpr_df.to_csv('data/uscpr_df')


# uscpr_df['Country'] = 'US/CA'

# st.write('Sam Df')
# st.write(sam_df)
# st.write('USCPR')
# st.write(uscpr_df)

df = pd.concat([uscpr_df, sam_df], axis =0).drop_duplicates(subset=['Link'], keep='first')
df['Date'] = df['Date'].apply(lambda x: x.split('.')[0] if x else x)
# st.write(df)


with col1:
    st.subheader('Filters')
    select_date = st.checkbox('Date', False)
    if select_date:
        # Get the current year
        current_year = datetime.datetime.now().year
        # Add the current year to the 'Date' column values
        df['Date'] = df['Date'] + f' {current_year}'
        # Convert the 'Date' column to pandas datetime format if it's not already

        df['Date'] = df['Date'].apply(lambda x: pd.to_datetime(x, format ='mixed'))
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
    default_countries = list(set(df['Country']))
    if select_state:
        selected_state = st.selectbox('', default_states+default_countries)
        # Convert selected_date to pandas datetime format to match the 'Date' column format

        # Filter your DataFrame based on the selected date
        if selected_state in default_states:
            df = df[df['State'] == selected_state]
        if selected_state in default_countries:
            df = df[df['Country'] == selected_state]

with col2:
    m = create_map(df)
    folium_static(m)