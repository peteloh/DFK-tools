import streamlit as st

# Custom imports 
from streamlit_multipage import MultiPage
from streamlit_pages import tool1_heroes, tool2_summons # import your pages here

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.sidebar.title("Defi Kingdoms Tools")

# Add all your applications (pages) here
app.add_page("Heros Tracker", tool1_heroes.app)
app.add_page("Summoning Guru", tool2_summons.app)

# The main app
app.run()

    
    

    