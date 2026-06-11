import streamlit as st

st.set_page_config(
    page_title="DemandForecast AI",
    page_icon="📈",
    layout="wide"
)

# Load CSS
with open("dashboard/assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# Sidebar
st.sidebar.title("DemandForecast AI")

st.sidebar.caption(
    "Retail Demand Forecasting Engine"
)

st.sidebar.divider()



# Main page
st.title("DemandForecast AI")

st.subheader(
    "Predict future demand and optimize inventory."
)

st.info(
    """
    Navigate using the pages menu on the left.
    """
)