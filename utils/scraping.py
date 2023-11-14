# Define a function to split event info
import requests
from bs4 import BeautifulSoup
import csv
import streamlit as st
import re
import folium
import pandas as pd
import datetime


@st.cache_data
def split_event_info(event):
    text, link = event
    # st.write(event)
    try:
        location, event = (text.split(':')[0], text.split(':')[1])
    except:
        try:
            location, event = (text.split('|')[0], text.split('|')[1])
        except:
            location, event = None, None

    try:
        city, state = location.split(',')
    except:
        city, state = (location, location)
    try:
        date = event.split(',')[0]
    except:
        date = None
    try: 
        rest = event.split(',')[1]
        try:

            time = rest.split('.')[0]
        except:
            time = rest.split(',')[0]
    except:
        time = 'Check link'
    return city, state, date, time, location, link

@st.cache_data
def get_uscpr_web_data(url, split_str, end_str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
    }
    # Make a request to the website
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parse the content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html')
    # soup.text
    # st.write(response.content)
    # st.write(soup.contents)

    html_str = str(soup)
    # st.write(html_str)

    # Find the indices of your markers
    start_idx = html_str.find(split_str)
    end_idx = html_str.find(end_str)

    # If both markers are found
    if start_idx != -1 and end_idx != -1:
        # Extract the substring between these markers
        events_html_str = html_str[start_idx:end_idx]
        
        # Parse this substring with BeautifulSoup
        events_soup = BeautifulSoup(events_html_str, 'html.parser')
        
        # Now extract the events and links from events_soup
        event_lines = events_soup.find_all(['p', 'li'])
        event_info = []
        for line in event_lines:
            text = line.text
            link_tag = line.find('a', href=True)
            link = link_tag['href'] if link_tag else None
            if link:  # assuming every event has a link
                event_info.append((text, link))
        event_info = event_info[2:]
        
        # Save to CSV
        today = datetime.datetime.now().strftime('%Y_%m_%d')

        with open(f'data/uspcr_events_{today}.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Event Info', 'Link'])  # write header
            writer.writerows(event_info)  # write data rows
        
        # Display in Streamlit
        # st.write(event_info)
    else:
        st.write("Markers not found in the HTML")
    return event_info


def get_samidoun_data(url, split_str, end_str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
    }
    # Make a request to the website
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parse the content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html')

    html_str = str(soup)

    # Find the indices of your markers
    start_idx = html_str.find(split_str)
    end_idx = html_str.find(end_str)

    # If both markers are found
    if start_idx != -1 and end_idx != -1:
        # Extract the substring between these markers
        events_html_str = html_str[start_idx:end_idx]
        
        # Parse this substring with BeautifulSoup
        events_soup = BeautifulSoup(events_html_str, 'html.parser')
        
        # Now extract the events and links from events_soup
        event_lines = events_soup.find_all(['p', 'li'])
        event_info = []
        for line in event_lines:
            text = line.text
            link_tag = line.find('a', href=True)
            link = link_tag['href'] if link_tag else None
            if link:  # assuming every event has a link
                event_info.append((text, link))
                today = datetime.datetime.now().strftime('%Y_%m_%d')

        with open(f'data/samidoun_events_{today}.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Event Info', 'Link'])  # write header
            writer.writerows(event_info)  # write data rows
        
            # Display in Streamlit
            # st.write(event_info)
    else:
        st.write("Markers not found in the HTML")

    return event_info


# @st.cache_data
# def split_sam_event_info(event):
#     text, link = event

#     # Split location and event details using " – " as the delimiter
#     try:
#         location, event_details = text.split('-')
#     except:
#         st.write(text)

#     # Split city and country/state, checking for "(US)" in the text
#     if "(US)" in location:
#         city, state_country = location.split(", ")
#         state_country = state_country.replace(" (US)", "").strip()
#         country = "US"
#     else:
#         city = location
#         state_country = None
#         country = location.split(", ")[-1].strip()  # Assume the last word is the country

#     # Split date, time, and venue using regex
#     match = re.match(r'^(.+?), (\d+:\d+ [apmAPM]+), (.+?)\. Info: (.+)$', event_details)
#     if match:
#         date, time, venue, info_link = match.groups()
#     else:
#         # Handle the case where the regex doesn't match
#         date, time, venue, info_link = (None, None, None, None)

#     return city, state_country, country, date, time, venue, link, info_link




@st.cache_data
def split_sam_event_info(event):
    text, link = event

    # Use regex to split location and event details
    location_event_split = re.match(r'^(.+?) ?– (.+)$', text)
    if location_event_split:
        location, event_details = location_event_split.groups()
    else:
        # Handle case where regex doesn't match
        return (None,) * 8  # Return tuple of eight None values

    # Split city and country/state, checking for "(US)" in the text
    if "(US)" in location:
        try:
            city, state_country = location.split(", ")
            state_country = state_country.replace(" (US)", "").strip()
            country = "US"
        except:
            city, state_country = location, location
            country = "US"
        
    else:
        city = location
        state_country = None
        country = location.split(", ")[-1].strip()  # Assume the last word is the country

    # Use regex to split date, time, and venue
    details_split = re.match(r'^(.+?), (\d+:\d+ [apmAPM]+), (.+?)\. Info: (.+)$', event_details)
    if details_split:
        date, time, venue, info_link = details_split.groups()
    else:
        # Handle case where regex doesn't match
        date, time, venue, info_link = (None, None, None, None)

    return city, state_country, country, date, time, venue, link, info_link

# Example Usage:

# def split_event_info(event):
#     text, link = event

#     # Use regex to split location and event details
#     location_event_split = re.match(r'^(.+?) ?– (.+)$', text)
#     if location_event_split:
#         location, event_details = location_event_split.groups()
#     else:
#         # Handle case where regex doesn't match
#         return (None,) * 8  # Return tuple of eight None values

#     # Split location into city, state, and country
#     location_parts = location.split(", ")
#     city = location_parts[0]
#     state = None
#     country = None
#     if len(location_parts) > 1:
#         # If there's a "(US)" in the text, assume it's a US state
#         if "(US)" in location_parts[1]:
#             state = location_parts[1].replace(" (US)", "")
#             country = "US"
#         else:
#             country = location_parts[1]
    
#     # Use regex to split date, time, and venue
#     details_split = re.match(r'^(.+?), (\d+:\d+ [apmAPM]+), (.+?)\. Info: (.+)$', event_details)
#     if details_split:
#         date, time, venue, info_link = details_split.groups()
#     else:
#         # Handle case where regex doesn't match
#         date, time, venue, info_link = (None, None, None, None)

#     return city, state, country, date, time, venue, link, info_link


# def split_sam_event_info(event):
#     text, link = event

#     # Use regex to split location and event details
#     location_event_split = re.match(r'^(.+?) ?– (.+)$', text)
#     if location_event_split:
#         location, event_details = location_event_split.groups()
#     else:
#         # Handle case where regex doesn't match
#         return (None,) * 8  # Return tuple of eight None values

#     # Split location into city, state, and country
#     location_parts = location.split(", ")
#     city = location_parts[0]
#     state = None
#     country = None
#     if len(location_parts) > 1:
#         # If there's a "(US)" in the text, assume it's a US state
#         if "(US)" in location_parts[1]:
#             state = location_parts[1].replace(" (US)", "")
#             country = "US"
#         else:
#             country = location_parts[1]

#     # Use regex to split date, time, and venue
#     details_split = re.match(r'^(.+?) (\d+:\d+ [apmAPM]+), (.+?)\.? Info: (.+)$', event_details)
#     if details_split:
#         day, time, venue, info_link = details_split.groups()
#     else:
#         # Handle case where regex doesn't match
#         day, time, venue, info_link = (None, None, None, None)

#     return city, state, country, day, time, venue, link, info_link



# def split_sam_event_info(event):
#     text, link = event

#     # Use regex to split location and event details
#     location_event_split = re.match(r'^(.+?) ?– (.+)$', text)
#     if location_event_split:
#         location, event_details = location_event_split.groups()
#     else:
#         # Handle case where regex doesn't match
#         return (None,) * 8  # Return tuple of eight None values

#     # Split location into city, state, and country
#     location_parts = location.split(", ")
#     city = location_parts[0]
#     state = None
#     country = None
#     if len(location_parts) > 1:
#         # If there's a "(US)" in the text, assume it's a US state
#         if "(US)" in location_parts[1]:
#             state = location_parts[1].replace(" (US)", "")
#             country = "US"
#         else:
#             country = location_parts[1]

#     # Use regex to split date, time, and venue
#     details_split = re.match(r'^([A-Za-z]+ [A-Za-z]+ \d+), (\d+:\d+ [apmAPM]+), (.+?)\.? Info:? (.+)$', event_details)
#     if details_split:
#         day, time, venue, info_link = details_split.groups()
#     else:
#         # Handle case where regex doesn't match
#         day, time, venue, info_link = (None, None, None, None)

#     return city, state, country, day, time, venue, link, info_link


def split_sam_event_info(event):
    text, link = event
    
    # Use regex to split location and event details
    location_event_split = re.match(r'^(.+?) ?– (.+)$', text)
    if location_event_split:
        location, event_details = location_event_split.groups()
    else:
        # Handle case where regex doesn't match
        return (None,) * 8  # Return tuple of eight None values
    
    # Split location into city, state, and country
    location_parts = location.split(", ")
    city = location_parts[0]
    state = None
    country = None
    if len(location_parts) > 1:
        # If there's a "(US)" in the text, assume it's a US state
        if "(US)" in location_parts[1]:
            state = location_parts[1].replace(" (US)", "")
            country = "US"
        else:
            country = location_parts[1]
    
    # Extract date using regex
    date_match = re.search(r'([A-Za-z]+ \d+)', event_details)
    if date_match:
        date = date_match.group(1)
    else:
        date = None
    
    # Extract time using regex
    time_match = re.search(r'(\d+:\d+ [apmAPM]+)', event_details)
    if time_match:
        time = time_match.group(1)
    else:
        time = None
    
    # Extract venue using regex
    venue_match = re.search(r'(\d+ [apmAPM]+), (.+?)\.? Info', event_details)
    if venue_match:
        venue = venue_match.group(2)
    else:
        venue = None
    
    return city, state, country, date, time, venue, link, None  # No separate info link in this version
