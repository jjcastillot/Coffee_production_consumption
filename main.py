# Import required libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from countries_dataset import countries
from codes import country_codes
from country_surface_area import country_areas
from country_latitudes import latitudes

st.set_page_config(layout='wide', initial_sidebar_state='expanded', page_title='☕Coffee around the world☕')
st.write('<style>div.block-container{padding-top:1rem;gap:0rem}</style>', unsafe_allow_html=True)
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def graph_title(col):
    match col:
        case 'Production':
            return f'{col} - Total 60kg bags in thousands'
        case 'Domestic Consumption':
            return f'{col} - Total 60kg bags in thousands'
        c
