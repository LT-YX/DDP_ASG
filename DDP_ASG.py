import streamlit as st
import pandas as pd
import numpy as np
import regex as re

# Read the Excel file
data = pd.read_excel('DDP_ASG.xlsx') # Requires pip install openpyxl
data.fillna("-", inplace=True) 

# ----------------------------------------------------------------------

# Initialize variables
previous_stop = None
rowData = []
headers = ['Service No', 'Next Bus', 'Next Bus 2', 'Next Bus 3']

badge_keywords = {
    'Transport': ['stn', 'int'],
    'Accommodation': ['hotel', 'hostel', 'inn', 'resort', 'lodge', 'motel','ritz-carlton'],
    'Attraction': ['sentosa', 'gallery', 'museum', 'zoo', 'park', 'gardens', 'esplanade', 'theatre','float'],
    'Shopping': ['orchard', 'bugis','ion','mall','vivocity'],
    'Cultural': ['chinatown', 'little india'],
    'Food': ['hawker', 'food court', 'restaurant', 'food centre', 'boat quay', 'clarke quay','lau pa sat'],
    'Airport':['airport']
    
}
badge_colors = {
    'Transport': "#a2c4ff",  # Light Blue
    'Attraction': "#b59dff",     # Purple
    'Shopping': "#ffa9b6",       # Light Red
    'Cultural': '#fcd374' ,       # Light Yellow
    'Food': "#ffa87a",            # Light orange
    'Accommodation': "#ffabed",  # Light pink,
    'Airport': "#76D5C7"
}
category_icons = {
    'Transport': "🚌",
    'Attraction': "🎡",
    'Shopping': "🛍️",
    'Cultural': "🏮",
    'Food': "🍜",
    'Accommodation': "🛏️",
    'Airport': "✈️"
}
#-------------------------------------------------------------------------
# -- Function to display headers
def headers():
    st.markdown(f""" <table style="width: 100%; margin-bottom:0rem">
    <tr>
        <td style ="width: 25%">🚍 Bus Number</td>
        <td style = "width: 75%">Bus arrival times</td>
    </tr> </table>
    """, unsafe_allow_html=True)
# ----------------------------------------------------------------------

# -- Function to Get Badges
def get_badge(location):
    for category, keywords in badge_keywords.items():
        for keyword in keywords:
            if keyword.lower() in location.lower():
                color = badge_colors[category]
                emoji = category_icons[category]
                return f"""<span style="background-color:{color}; 
                padding:2px 8px; border-radius:12px; 
                font-size:12px; margin-right:6px;">
                {emoji} {category}
                </span>"""
    return ""
# -- Display title
# Display the Streamlit app title and description
st.title("Tourist Bus Stop Information in Singapore")
st.write("This is a simple app to display bus stop data that might be relevant for tourists visiting Singapore." \
"\nContains bus stop information of various touristy locations, notable locations, and next bus arrival times.")

# -- Side bar
st.sidebar.subheader("🔎 Jump to Bus Stop")
unique_stops = data[['BusStopCode', 'Description']].drop_duplicates()

for _, row in unique_stops.iterrows():
    code = row['BusStopCode']
    desc = row['Description']
    st.sidebar.markdown(f"[🚌 {code:05d} - {desc}](#{code})", unsafe_allow_html=True)
# ----------------------------------------------------------------------

for i, row in data.iterrows():
    current_stop = row['BusStopCode']
    current_service = row['ServiceNo']
    current_description = row['Description']
    destination_code = row['DestinationCode']
    destination_desc = row['DestinationDescription']

    if current_stop != previous_stop:
        # link for table of contents and displays bus stop code and description
        st.markdown(
            f'''
            <div id="{current_stop}" style="margin-top: -70px; padding-top: 70px;"> 
                <h2>🚌 Bus Stop {current_stop:05d} - {current_description}</h2>
            </div>
            ''',
            unsafe_allow_html=True
        )
        previous_stop = current_stop

    with st.container(border=True):
        cols = st.columns([2, 2, 2, 2])
        cols[0].markdown(f"<b>🚌 Bus Number {row['ServiceNo']}</b>", unsafe_allow_html=True)
        cols[1].markdown(f"<span style='font-size:16px'>| ⏱ {row['NextBus']}</span>", unsafe_allow_html=True)
        cols[2].markdown(f"<span style='font-size:16px'>| ⏱ {row['NextBus2']}</span>", unsafe_allow_html=True)
        cols[3].markdown(f"<span style='font-size:16px'>| ⏱ {row['NextBus3']}</span>", unsafe_allow_html=True)
        
    
        with st.expander(f"📍 Additional Information", expanded=False):

            notable_locations = row['NotableLocations'].split(',') if pd.notna(row['NotableLocations']) else [] # Prevents error if no notable locations
            stops_until = row['StopsUntil'].split(',') if pd.notna(row['StopsUntil']) else []

            # Create card-style layout

            st.markdown(f"**🗺️ Notable Destinations (within 20 stops):**", unsafe_allow_html=True)

            # Show each destination with badge
            for j in range(len(notable_locations)):
                if j < len(stops_until):
                    location = notable_locations[j].strip()
                    stops = stops_until[j].strip()

                    badge = get_badge(location)

                    st.markdown(
                        f"""<div style="margin-bottom:8px;">{badge}<span style="font-size:15px;">{location} in {stops} stops</span></div>""",
                        unsafe_allow_html=True
                    )

            # Final stop info
            st.markdown(f"<br>🛑 **Last Destination:** {row['DestinationDescription']}", unsafe_allow_html=True)

            # End card
            st.markdown("</div>", unsafe_allow_html=True)