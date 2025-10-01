import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# --- SIDINSTÄLLNINGAR ---
st.set_page_config(
    page_title="Brottsanalys",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ta bort Streamlit-menyer
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Brottsanalys 1950–2010")

# --- API URL och endpoints ---
API_URL = "http://127.0.0.1:8000"
ENDPOINT_ALL = "/all_data"
ENDPOINT_CATEGORIZED = "/categorized_crimes"
ENDPOINT_KPIS = "/kpis"

# --- Hämta data för kategoriserade brott ---
response = requests.get(f"{API_URL}{ENDPOINT_CATEGORIZED}")
df_categories = pd.DataFrame(response.json())

# --- Slider för år ---
year = st.slider(
    "Välj år",
    min_value=int(df_categories['Year'].min()),
    max_value=int(df_categories['Year'].max()),
    value=2008
)
row = df_categories[df_categories['Year'] == year]

# --- Visa KPI:er för det valda året ---
kpi_response = requests.get(f"{API_URL}{ENDPOINT_KPIS}?year={year}")
kpis = kpi_response.json()

st.subheader(f"KPI:er för år {year}")
col1, col2, col3 = st.columns(3)
col1.metric("Totalt antal brott", kpis["total_crimes"])
col2.metric("Population", kpis["population"])
col3.metric("Brott per capita", f"{kpis['avg_crimes_per_capita']:.6f}")

# --- Pie chart för brottskategorier ---
categories = ['Våldsbrott', 'Stöldbrott', 'Ekonomiska brott', 'Vandalisering', 'Under influenser']
values = [
    row['Violent'].values[0],
    row['Theft'].values[0],
    row['Economic'].values[0],
    row['Vandal'].values[0],
    row['Alc/Drug'].values[0]
]

fig = px.pie(
    names=categories,
    values=values,
    title=f'Brottsandelar år {year}'
)
fig.update_traces(textinfo='percent+label')
st.plotly_chart(fig, use_container_width=True)
