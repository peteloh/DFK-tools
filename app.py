import streamlit as st

# Custom imports 
from streamlit_multipage import MultiPage
from streamlit_pages import tool1_heroes, tool2_summons # import your pages here

# Create an instance of the app 

app = MultiPage()

st.set_page_config(
    page_title="dfk tools",
    layout='wide'
    )

# Title of the main page
st.sidebar.header("Defi Kingdoms Tools")

# Add all your applications (pages) here
app.add_page("Summoning Guru", tool2_summons.app)
app.add_page("Heros Tracker", tool1_heroes.app)

# The main app
app.run()

    
    

    