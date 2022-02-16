import streamlit as st

# Custom imports 
from streamlit_multipage import MultiPage
from applications import tool1_heroes, tool2_summons, tool3_check_sales, tool4_database # import your pages here

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
app.add_page("Heroes Tracker", tool1_heroes.app)
app.add_page("Recent Hero Sales", tool3_check_sales.app)
app.add_page("Analytics", tool4_database.app)

# The main app
app.run()
st.sidebar.markdown("#")
st.sidebar.markdown("This tool is not desinged for mobile use")
st.sidebar.markdown("#")
st.sidebar.markdown("This tool is made to assist in interactions with Defi Kingdoms Application")
st.sidebar.markdown("https://game.defikingdoms.com/")
st.sidebar.markdown("#")
st.sidebar.markdown("Made by Pete Loh")

    
    

    