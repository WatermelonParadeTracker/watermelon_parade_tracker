from utils.scraping import get_samidoun_data, split_sam_event_info
from utils.scraping import split_event_info, get_uscpr_web_data
import streamlit as st
import pandas as pd
from streamlit_folium import folium_static


def get_sam_df():
    from utils.sam_mapping import get_state_abbreviation, create_map, add_loc 

    event = ("ALBUQUERQUE, NM (US) – Fr Oct 20, 5 pm, UNM Hospital, 2211 Lomas Blvd NE. Info: https://www.instagram.com/p/CyjwpR0LUyr/",
            "https://www.instagram.com/p/CyjwpR0LUyr/")
    result = split_sam_event_info(event)
    # print(result)

    split_str = 'send us updates!'
    end_str = 'Join the'
    url = 'https://samidoun.net/2023/10/calendar-of-resistance-for-palestine-events-and-actions-around-the-world/'

    event_info = get_samidoun_data(url, split_str, end_str)
    # st.write(event_info)

    split_info = [split_sam_event_info(event) for event in event_info]

    # Create a DataFrame from the split info
    columns = ['City', 'State', 'Country', 'Date', 'Time', 'Venue', 'Link', 'Link Info']


    # st.write(split_info)
    df = pd.DataFrame(split_info, columns=columns)
    df = df.dropna(subset=['City'])
    # df['City'] = df['City'].apply(lambda x: x.split(' ')[0] if x else x)
    df['City'] = df['City'].apply(lambda x: x.split(',')[0] if x else x)
    df['City'] = df['City'].apply(lambda x: x.split('/')[0] if x else x)
    df['City'] = df['City'].apply(lambda x: x.split('(')[0] if x else x)

    df['State']=df['State'].apply(lambda x: get_state_abbreviation(x) if x else x)
    df['State'] = df['State'].apply(lambda x: x.split('(')[0] if x else x)

    # st.write(df)
    df = add_loc(df)
    df = df.dropna(subset=['Longitude', 'Latitude'])
    return df



def get_uscpr_df():
    from utils.mapping import add_loc, create_map

    url_default = "https://uscpr.org/oct-2023-protests"
    split_str_default = 'Join a protest'
    end_str_default = 'Know a protest'

    event_info = get_uscpr_web_data(url_default, split_str_default, end_str_default)
    # Apply the function to each event in event_info
    split_info = [split_event_info(event) for event in event_info]

    # Create a DataFrame from the split info
    columns = ['City', 'State', 'Date', 'Time', 'Location', 'Link']
    df = pd.DataFrame(split_info, columns=columns)
    df = add_loc(df)
    return df