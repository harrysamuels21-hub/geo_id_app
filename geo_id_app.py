import pandas as pd
import streamlit as st

def load_data():
    return pd.read_csv(r'C:\Users\harry.samuels\Documents\Geo_ID\data\county_merg.csv',
  	   dtype={
            "STATEFP_x": str,
            "COUNTYGEOID": str,
            "COUNTYNAME": str,
            "STATE_NAME": str
        }
)

county_merg = load_data()

# Your function
def geoid_lookup(geoid):
    geoid = str(geoid)
    #State Query
    geoid_state = geoid[:2]
    state_query = county_merg.query("STATEFP_x == @geoid_state")
    state_name = state_query['STATE_NAME'].iloc[0]
    
    #County Query
    geoid_county = geoid[:5]
    county_query = county_merg.query("COUNTYGEOID == @geoid_county")
    county_name = county_query['COUNTYNAME'].iloc[0]
    
    #Census Tract Query
    geoid_tract = geoid[5:9]
    
    #Census Block Query
    geoid_block = geoid[11:]
    
    return {
    "State/Territory": state_name,
    "County": county_name,
    "Census Tract": geoid_tract if geoid_tract else None,
    "Census Block": geoid_block if geoid_block else None
}

# Streamlit app
st.title("GeoID Look-Up App")

# Input box
user_input = st.text_input("Enter your GEOID here: ")

# Button to run function
if st.button("Run Lookup"):
    if user_input:  # only run if something was entered
        result = geoid_lookup(user_input)
        st.success(result)
    else:
        st.warning("Please enter a GEOID first.")
