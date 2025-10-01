import streamlit as st
import pandas as pd
import plotly.express as px
from utils.constants import CSV_PATH
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent 
sys.path.insert(0, str(PROJECT_ROOT))  


# --- SIDINSTÄLLNINGAR ---
st.set_page_config(
    page_title="Brottsanalys",
    page_icon="📊",
    layout="wide",           # Gör sidan "wide"
    initial_sidebar_state="collapsed"  # Dölj sidopanelen
)

# Ta bort hamburger-menyn och Streamlit footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- SIDANS INNEHÅLL ---
st.title("Brottsanalys 1950–2010")

# Ladda data
df = pd.read_csv(CSV_PATH) 

# Definiera brottskategorier
violent_crimes = ['murder', 'assault', 'rape', 'sexual.offenses']
theft_crimes = ['burglary', 'vehicle.theft', 'shop.theft', 'stealing.general', 'out.of.vehicle.theft', 'robbery']
vandal_crimes = ['criminal.damage']
alc_and_drug_crimes = ['narcotics', 'drunk.driving']
economic_crimes = ['fraud']

# Skapa nya kolumner med summor per kategori
df['Violent'] = df[violent_crimes].sum(axis=1)
df['Theft'] = df[theft_crimes].sum(axis=1)
df['Vandal'] = df[vandal_crimes].sum(axis=1)
df['Alc/Drug'] = df[alc_and_drug_crimes].sum(axis=1)
df['Economic'] = df[economic_crimes].sum(axis=1)


# Om du vill visa andel istället för absolut antal
# df['Total_categorized'] = df['Violent'] + df['Theft'] + df['Economic'] + df['Vandal'] + df['Alc/Drug']
# df['Violent_share'] = df['Violent'] / df['Total_categorized']
# df['Theft_share'] = df['Theft'] / df['Total_categorized']
# df['Economic_share'] = df['Economic'] / df['Total_categorized']
# df['Vandal_share'] = df['Vandal'] / df['Total_categorized']
# df['Alc_Drug_share'] = df['Alc/Drug'] / df['Total_categorized']

# Exempel: topp brott ett år
year = st.slider("Välj år", min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), value=2008)

row = df[df['Year'] == year]
categories = ['Våldsbrott', 'Stöldbrott', 'Ekonomiska brott', 'Vandalisering', 'Under influenser']
values = [
    row['Violent'].values[0],
    row['Theft'].values[0],
    row['Economic'].values[0],
    row['Vandal'].values[0],
    row['Alc/Drug'].values[0]
]

# Plotly pie chart
fig = px.pie(names=categories, values=values, title=f'Brottsandelar år {year}')
fig.update_traces(textinfo='percent+label')

st.plotly_chart(fig, use_container_width=True)
