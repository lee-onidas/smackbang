from numpy import NaN, empty
import streamlit as st
import datetime
import base64
import pandas as pd
from streamlit_folium import folium_static
import folium
import requests
import os
from dotenv import load_dotenv, find_dotenv
import time
from smackbang.matches import get_matches
from smackbang.midpoint import midpoint


env_path = find_dotenv()
load_dotenv(env_path)
RAPID_API_TOKEN = os.getenv('API_TOKEN')
RAPID_API_KEY = os.getenv('API_KEY')
airports = pd.read_csv('data/airport_codes.csv')
back_front_df = pd.DataFrame()

# ---------------------------
#        Page Configuration
# ---------------------------

st.set_page_config(
    page_title= 'SmackBang: Find the middle ground',
    page_icon= 'images/smackbang_favicon_32x32.png',
    layout= 'wide')

# Remove the menu button from Streamlit
st.markdown(""" <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style> """, unsafe_allow_html=True)


# ---------------------------
#        Header
# ---------------------------

row1_1, row1_2 = st.columns((0.2, 2))

row1_1.image('images/smackbang_favicon_32x32.png', width = 120)
row1_2.title('SmackBang:  Find the middle ground')
row1_2.markdown('Connect with friends, family and colleagues')


# ---------------------------
#        User Input
# ---------------------------

row2_1, row2_2 = st.columns((1,1))

with row2_1:

    # User One input, search and convert to string
    origin_one_input = st.selectbox('Origin 1', airports)
    origin_one = airports.loc[airports['city_airport'] == origin_one_input, 'iata_code' ].to_string(index=False)

    # User Two input, search and convert to string
    origin_two_input = st.selectbox('Origin 2', airports)
    origin_two = airports.loc[airports['city_airport'] == origin_two_input, 'iata_code' ].to_string(index=False)


with row2_2:
    # Departure and return placeholder dates
    default_departure_date = datetime.date.today() + datetime.timedelta(days=28)
    future_date = default_departure_date + datetime.timedelta(days=50)

    # Departure and return date input fields
    departure_date = (st.date_input('Meeting Date', default_departure_date, min_value=datetime.date.today())).strftime("%d/%m/%Y")
    return_date_check = st.checkbox("Do you want to add a return date?")

    if return_date_check:
        return_date = (st.date_input('Return Date', future_date)).strftime("%d/%m/%Y")

    # Continent
    continent_input = st.selectbox('Continents', ('Asia', 'Africa', 'Europe', 'North America', 'South America', 'Oceania'))

    def continent_name(continent_input):
        result = {
                'Asia' : 'AS',
                'Africa' : 'AF',
                'Europe' : 'EU',
                'North America' : 'NA',
                'South America' : 'SA',
                'Oceania' : 'OC',
                }

        return result.get(continent_input)

    continent = continent_name(continent_input)

# ---------------------------
#        API Magic Area
# ---------------------------

    if st.button('SmackBang my Destinations'):
        # Spinner
        with st.spinner('Hold on while we search 1,000\'s of flights ...'):
            time.sleep(10)


        # Matches.py API query and output
        matches_df = get_matches(origin_one, origin_two, departure_date, continent, return_date='', currency='USD')
        back_front_df = matches_df.copy()

        # format price
        back_front_df['combined_price'] = back_front_df['combined_price'].apply(lambda x: f"${x:,.0f}")


        # Playing with price format
        #back_front_df['price'][:,:] = back_front_df['price'][:,:].apply(lambda x: f"${x:,.0f}")
        #back_front_df.iloc[1, 'Sydney'] =  back_front_df.iloc[1, 'Sydney'].apply(lambda x: f"${x:,.0f}")


# ---------------------------
#        User Output
# ---------------------------

st.write(''' ''')

st.header('Destinations')

if origin_one_input == 'Origin' or origin_two_input == 'Origin':
    st.markdown(f'Enter your destinations, dates and your continent above.')
else:
    city_one = airports.loc[airports['city_airport'] == origin_one_input, 'city' ].to_string(index=False)
    city_two = airports.loc[airports['city_airport'] == origin_two_input, 'city' ].to_string(index=False)
    st.markdown(f'Destinations between {city_one} and {city_two} are displayed below')

row3_1, row3_2 = st.columns(2)

# Formatting Output dataframe

back_front_df.rename(columns = {'price':'Price from',
                                'duration' : 'Duration from',
                                'combined_price' : 'Combined Price',
                                 }, inplace = True)

with row3_1:
    if not back_front_df.empty:
        st.dataframe(back_front_df[['Price from','Duration from','Combined Price' ]], 800, 600)
    else:
        st.write('')

row3_1 = st.columns(1)

with row3_2:

    df_map = back_front_df

    if origin_one_input == 'Origin' or origin_two_input == 'Origin' :
        m = folium.Map(location=[0, 100], zoom_start=2, width='100%')
    else:
        origin_one_lat = airports.loc[airports['city_airport'] == origin_one_input, 'lat' ].to_string(index=False)
        origin_one_lon = airports.loc[airports['city_airport'] == origin_one_input, 'lon' ].to_string(index=False)
        origin_two_lat = airports.loc[airports['city_airport'] == origin_two_input, 'lat' ].to_string(index=False)
        origin_two_lon = airports.loc[airports['city_airport'] == origin_two_input, 'lon' ].to_string(index=False)

        starting_location = midpoint(origin_one_lat, origin_one_lon, origin_two_lat, origin_one_lat)

        m = folium.Map(location=starting_location, zoom_start=2, width='100%')

        # City markers
        for _, dest in df_map.iterrows():

            folium.Marker(
                location=[dest.lat, dest.lon],
                popup= [dest.index],
                icon=folium.Icon(color="blue", icon="info-sign"),
            ).add_to(m)

        # Origin One marker
        folium.Marker(
            location=[origin_one_lat, origin_one_lon],
            popup= [origin_one_input],
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(m)

        # Origin Two marker
        folium.Marker(
            location=[origin_two_lat, origin_two_lon],
            popup= [origin_two_input],
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(m)


        folium_static(m)


#st.write(back_front_df.head())
