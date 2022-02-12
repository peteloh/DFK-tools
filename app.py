import streamlit as st

# Custom imports 
from streamlit_multipage import MultiPage
from sub_applications import tool1_heroes, tool2_summons # import your pages here

# Create an instance of the app 

app = MultiPage()

st.set_page_config(
    page_title="dfk tools",
    layout='wide'
    )

# Title of the main page

col1, col2 = st.sidebar.columns((4,9))

col2.image("./images/jewel_icon.png")

st.sidebar.title("DFK Tools")

# Add all your applications (pages) here
app.add_page("Summoning Guru", tool2_summons.app)
app.add_page("Heros Tracker", tool1_heroes.app)

# The main app
app.run()

st.sidebar.text("")

st.sidebar.markdown("Made by Pete Loh")

    
    

    