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
st.set_page_config(layout='wide', initial_sidebar_state='expanded',page_title='☕Coffee around the world☕')
st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def graph_title(col):
    match col:
        case 'Production':
            return f'{col} - Total 60kg bags in thousands'
        case 'Domestic Consumption':
            return f'{col} - Total 60kg bags in thousands'
        case 'Gross Openings':
            return f'{col} - Total 60kg bags in thousands'
        case 'Exports':
            return f'{col} - Total 60kg bags in thousands'
        case 'Imports':
            return f'{col} - Total 60kg bags in thousands'
        case 'Production Over Area':
            return f'{col} - Total Production(K 60kg bags) over area in sq km2'
        case 'Dom. Consumption Ratio':
            return f'{col} - Domestic Consumption(K 60kg bags) over total production'
        case _:
            return f'{col} - Total'

# Define a function to plot the choroplets
def prod_plot(df,column,color_scale):
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
        title=graph_title(column),
        margin={'r': 0, 't': 40, 'l': 0, 'b': 10},
    )

    # Show the figure
    return fig

def imports_plot(color_scale):
    fig = px.choropleth(
        df_imports,
        locations='Code',
        color='Totals',
        hover_name='Country',
        color_continuous_scale=color_scale,
        #range_color=(0, 1500000),
        scope='world',
    )
    # Update the layout of the figure
    fig.update_layout(
        title=graph_title('Imports'),
        margin={'r': 0, 't': 20, 'l': 0, 'b': 0},
    )
    # Show the figure
    return fig

def create_world_plot(chart_option):
    match chart_option:
        case 'Production':
            return prod_plot(df_totals,chart_option,'Greens')
        case 'Domestic Consumption':
            return prod_plot(df_totals,chart_option,'Reds')
        case 'Gross Openings':
            return prod_plot(df_totals,chart_option,'Purples')
        case 'Exports':
            return prod_plot(df_totals,chart_option,'Blues')
        case 'Imports':
            return imports_plot('Oranges')
        case 'Production Over Area':
            return prod_plot(df_totals,chart_option,'Greens')
        case 'Dom. Consumption Ratio':
            return prod_plot(df_totals,chart_option,'Reds')
        case _:
            return prod_plot(df_totals,chart_option,'Greens')
                
######################################################################################################

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
df_totals['Dom. Consumption Ratio'] = df_totals['Domestic Consumption']/df_totals['Production']
df_totals['Area'] = df_totals['Country'].map(country_areas)
df_totals['Production Over Area'] = 1000*df_totals['Production']/df_totals['Area']
df_totals['Latitude']=df_totals['Country'].map(latitudes)
# Update data loading
#data_load_state.text('Loading data...done!')



# Create a sidebar for the streamlit dashboard
st.sidebar.header('☕Coffee around the world☕')
# Select one of the charts to print
chart_option = st.sidebar.selectbox(
    'Please select one of the charts below:',('Production','Production Over Area','Domestic Consumption','Dom. Consumption Ratio','Gross Openings','Exports','Imports'))
my_fig=create_world_plot(chart_option)
#Create columns of the dashboard
col1,col2 = st.columns([4,1])
col1.plotly_chart(my_fig,use_container_width=True)
#col2.top10_chart(chart_option)
st.markdown('Check the data here:')
with st.expander('Exporting countries consolidated data'):
    st.dataframe(df_totals.style.highlight_max(axis=0))
with st.expander('Importing countries data'):
    st.dataframe(df_imports.style.highlight_max(axis=0))


