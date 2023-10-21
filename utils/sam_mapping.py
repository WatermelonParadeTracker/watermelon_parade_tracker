from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

import requests
from bs4 import BeautifulSoup
import csv
import streamlit as st
import re
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
import pandas as pd
from geopy.geocoders import Nominatim
import datetime
import us 

import us

def get_state_abbreviation(state_name_or_abbreviation):
    state = us.states.lookup(state_name_or_abbreviation)
    if state:
        return state.abbr
    else:
        return None
    

@st.cache_data
def add_loc(df):
    df['Latitude'], df['Longitude'] = zip(*df.apply(lambda row: get_lat_lon(row['City'], row['State'], row['Country']), axis=1))
    return df

def create_map(df): 
    # Create a base map
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=2)
    # Create a marker cluster
    marker_cluster = MarkerCluster().add_to(m)
    for idx, event in df.iterrows():
        folium.Marker(
            location=[event['Latitude'], event['Longitude']],
            popup=f"{event['City']}, {event['State'] if event['State'] else event['Country']}: {event['Date']} at {event['Time']}<br><a href='{event['Link']}' target='_blank'>Link</a>",
            icon=folium.Icon(color='blue', icon='info-sign'),
        ).add_to(marker_cluster)
    return m

# # Function to get latitude and longitude
# def get_lat_lon(city, state, country):
#     geolocator = Nominatim(user_agent="event_locator")
#     query = f'{city}, {state if state else country}'

#     try:
#         location = geolocator.geocode(query)
#         if location:
#             return location.latitude, location.longitude
#     except GeocoderTimedOut:
#         return get_lat_lon(city, state, country)  # Retry on timeout

#     return None, None  # Return None if location is not found
def get_lat_lon(city, state, country):
    geolocator = Nominatim(user_agent="event_locator", timeout=10)  # Increased timeout to 10 seconds
    query = f'{city}, {state if state else country}'

    try:
        location = geolocator.geocode(query)
        if location:
            return location.latitude, location.longitude
        else:
            # st.warning(f'Geocode failed for query: {query}')  # Log warning for failed geocode
            pass
            return None, None
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        st.warning(f'Geocode timed out or unavailable for query: {query}')  # Log warning for timeout or unavailability
        return None, None