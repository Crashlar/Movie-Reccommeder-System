import streamlit as st

# Initialize session state
if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None

# Define pages
home_page = st.Page("pages/Home.py", title="Home", icon="🏠", default=True)
details_page = st.Page("pages/Movie_Details.py", title="Movie Details", icon="📽️")

# Initialize navigation
# Adding 'position' can sometimes help stability in multipage apps
pg = st.navigation({"Menu": [home_page, details_page]}, position="sidebar")
pg.run()