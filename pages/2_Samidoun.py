from utils.scraping import get_samidoun_data, split_sam_event_info
from utils.sam_mapping import get_state_abbreviation, create_map, add_loc 
import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
from utils.makers import get_sam_df

st.set_page_config(layout='wide')
st.title('Watermelon Parade Tracker')

df = get_sam_df()
m=create_map(df)
folium_static(m)

st.write('Email samidoun@samidoun.net or tag them on social media to add more')