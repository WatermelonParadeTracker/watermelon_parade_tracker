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
        city, state = (location, location)
    date = event.split(',')[0]
    rest = event.split(',')[1]
    try:
        time = rest.split('.')[0]
    except:
        time = rest.split(',')[0]
    return city, state, date, time, location, link

@st.cache_data
def get_web_data(url, split_str, end_str):
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
        with open('events.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Event Info', 'Link'])  # write header
            writer.writerows(event_info)  # write data rows
        
        # Display in Streamlit
        # st.write(event_info)
    else:
        st.write("Markers not found in the HTML")
    return event_info

# URL to scrape

# url = st.text_input('Enter URL:', url_default)
# split_str = st.text_input('Split on:', split_str_default)
# end_str = st.text_input('End on:', end_str_default)

st.title('Watermelon Parade Tracker')
col1, col2 = st.columns([1, 7])

url_default = "https://uscpr.org/oct-2023-protests"
split_str_default = 'Join a protest'
end_str_default = 'Know a protest'

event_info = get_web_data(url_default, split_str_default, end_str_default)
# Apply the function to each event in event_info
split_info = [split_event_info(event) for event in event_info]

# Create a DataFrame from the split info
columns = ['City', 'State', 'Date', 'Time', 'Location', 'Link']
df = pd.DataFrame(split_info, columns=columns)
df = add_loc(df)

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