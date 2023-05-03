# Import required libraries
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
from countries_dataset import countries
from codes import country_codes
from country_surface_area import country_areas
from country_latitudes import latitudes
sns.set_theme()
st.set_page_config(layout="wide")

# Define a function to plot the choroplets
def world_plot2(df,column,color_scale):
    fig = px.choropleth(
        df,
        locations='Code',
        color=column,
        hover_name='Country',
        
        color_continuous_scale=color_scale,
        #range_color=(0, 1500000),
        scope='world',
    )

    # Update the layout of the figure
    fig.update_layout(
        title='Totals by Country',
        margin={'r': 0, 't': 40, 'l': 0, 'b': 10},
    )

    # Show the figure
    return fig
    #fig.show()

# Create a title for the streamlit dashboard
st.title('Coffee around the world')
#data_load_state = st.text('Loading data...')

#Import excel files after initial row cleaning
#@st.cache_data
#Production data in thousands 60kg bags
df_production = pd.read_excel('datasets/1a - Total production.xlsx',skiprows=3,skipfooter=3) 
df_production['Country'] = df_production['Country'].str.lstrip()
df_production['Code'] = df_production['Country'].map(country_codes)
df_production['Continent'] = df_production['Country'].map(countries)
#Domestic Consumption data in thousands 60kg bags
df_consumption = pd.read_excel('datasets/1b - Domestic consumption.xlsx',skiprows=3,skipfooter=3) 
df_consumption['Country'] = df_consumption['Country'].str.lstrip()
df_consumption['Code'] = df_consumption['Country'].map(country_codes)
df_consumption['Continent'] = df_consumption['Country'].map(countries)
#Gross Openings 
df_openings = pd.read_excel('datasets/1d - Gross Opening stocks.xlsx',skiprows=3,skipfooter=3) 
df_openings['Country'] = df_openings['Country'].str.lstrip()
df_openings['Code'] = df_openings['Country'].map(country_codes)
df_openings['Continent'] = df_openings['Country'].map(countries)
#Exports in thousands 60kg bags
df_exports = pd.read_excel('datasets/1e - Exports - crop year.xlsx',skiprows=3,skipfooter=3) 
df_exports['Country'] = df_exports['Country'].str.lstrip()
df_exports['Code'] = df_exports['Country'].map(country_codes)
df_exports['Continent'] = df_exports['Country'].map(countries)
#Imports in thousands 60kg bags
df_imports = pd.read_excel('datasets/2b - Imports.xlsx',skiprows=3,skipfooter=3) 
df_imports['Country'] = df_imports['Country'].str.lstrip()
df_imports['Code'] = df_imports['Country'].map(country_codes)
df_imports['Continent'] = df_imports['Country'].map(countries)
df_imports['Area'] = df_imports['Country'].map(country_areas)
df_imports['Latitude'] = df_imports['Country'].map(latitudes)
# Create a dataframe with the 'Totals' columns from this 4 dataframes: df_production, df_consumption, df_openings and df_exports. Create exports to production ratio
df_totals = pd.concat([df_production[['Country','Code','Continent','Totals']],df_consumption['Totals'],df_exports['Totals'],df_openings['Totals'],],axis=1)
df_totals.columns=['Country','Code','Continent','Production','Domestic Consumption','Exports','Gross Openings']
df_totals['Imports Offset'] = -df_totals['Production'] + df_totals['Domestic Consumption'] + df_totals['Exports'] + df_totals['Gross Openings']
df_totals['Exports Ratio'] = df_totals['Exports']/df_totals['Production']
df_totals['Domestic Consump Ratio'] = df_totals['Domestic Consumption']/df_totals['Production']
df_totals['Area'] = df_totals['Country'].map(country_areas)
df_totals['Production/Area1000'] = 1000*df_totals['Production']/df_totals['Area']
df_totals['Latitude']=df_totals['Country'].map(latitudes)
# Update data loading
#data_load_state.text('Loading data...done!')

# Select one of the charts to print
chart_option = st.selectbox(
    'Please select one of the charts below:',('Production','Domestic Consumption','Gross Openings','Exports','Imports'))
prod_fig=world_plot2(df_totals,chart_option,px.colors.sequential.Reds)
st.plotly_chart(prod_fig,use_container_width=True)
# Create a dictionary that maps each pf the previous options with a dataframe
options = {'Production':df_production,'Domestic Consumption':df_consumption,'Gross Openings':df_openings,'Exports':df_exports,'Imports':df_imports}
# Map one dataframe to the streamlit dashboard
st.subheader('Check the data here:')
with st.expander('Exporting countries consolidateddata'):
    st.dataframe(df_totals.style.highlight_max(axis=0,subset=['Production','Domestic Consumption','Exports','Openings','Offset','Exports Ratio',
                                                          'Domestic Consump Ratio','Production/Area1000']))
with st.expander('Importing countries data'):
    st.dataframe(df_imports.style.highlight_max(axis=0))



