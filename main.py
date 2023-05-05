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
st.set_page_config(layout='wide', initial_sidebar_state='expanded',page_title='☕Coffee around the world☕')
st.write('<style>div.block-container{padding-top:1rem;gap:0rem}</style>', unsafe_allow_html=True)
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
            return f'{col} - Total Production(K 60kg bags) over area in 1000 sq km2'
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
        scope='world',
    )
    # Update the layout of the figure
    fig.update_layout(
        title=graph_title(column),
        margin={'t':30},
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
        scope='world',
    )
    # Update the layout of the figure
    fig.update_layout(
        title=graph_title('Imports'),
        margin={'t': 30},
    )
    # Show the figure
    return fig

def create_world_plot(chart_option):
    match chart_option:
        case 'Production':
            return prod_plot(df_totals,chart_option,'Blues')
        case 'Domestic Consumption':
            return prod_plot(df_totals,chart_option,'Blues')
        case 'Gross Openings':
            return prod_plot(df_totals,chart_option,'Blues')
        case 'Exports':
            return prod_plot(df_totals,chart_option,'Blues')
        case 'Imports':
            return imports_plot('Blues')
        case 'Production Over Area':
            return prod_plot(df_totals,chart_option,'Blues')
        case 'Dom. Consumption Ratio':
            return prod_plot(df_totals,chart_option,'Blues')
        case _:
            return prod_plot(df_totals,chart_option,'Blues')
        
def top10s(column):
    if column=='Imports':
        top10 = df_imports[['Country','Code','Totals']].sort_values(by='Totals', ascending=False).head(10)
        top10 = top10.sort_values(by='Totals', ascending=True)
        top10.columns = ['Country','Code','Imports']
        return top10
    else:
        top10 = df_totals[['Country','Code',column]].sort_values(by=column, ascending=False).head(10)
        top10 = top10.sort_values(by=column, ascending=True)
        return top10
    
def lineplot_production(country):
    '''Create a line plot of imports for a given country code'''
    country_prod = df_production[df_production['Country'] == country].iloc[:,2:-3]
    country_prod=country_prod.T
    country_prod.rename(columns={country_prod.columns[0]:f'{country} Production in thousands 60kg bags'},inplace=True)
    country_prod['Dom. consumption in thousands 60kg bags']= df_consumption[df_consumption['Country'] == country].iloc[:,2:-3].T
    st.line_chart(data=country_prod,height=300,use_container_width=True)

def lineplot_imports(country):
    '''Create a line plot of imports for a given country code'''
    country_imports = df_imports[df_imports['Country'] == country].iloc[:,1:-5].T
    country_imports.rename(columns={country_imports.columns[0]:f'{country} Imports in thousands 60kg bags'},inplace=True)
    st.line_chart(data=country_imports,height=300,use_container_width=True)

            
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

######################################################################################

# Create a sidebar for the streamlit dashboard
st.sidebar.header('☕Coffee around the world☕')
st.sidebar.write('Data analysis of coffee production and consumption, and its impact on these regions. Datasets downloaded from https://www.ico.org/new_historical.asp.')
# Select one of the charts to print
chart_option = st.sidebar.selectbox(
    'Please select one of the charts below:',('Production','Production Over Area','Domestic Consumption','Dom. Consumption Ratio','Gross Openings','Exports','Imports'))
# Creates selectbox for the line chart
if chart_option == 'Imports':
    line_option = st.sidebar.selectbox(
        'See imports behavior of this country:',df_imports['Country']
    )
else:
    line_option = st.sidebar.selectbox(
        'See production behavior of this country:',df_totals['Country']
    )    
#Create columns of the dashboard
col1,col2 = st.columns([3,1])
my_fig=create_world_plot(chart_option)
col1.plotly_chart(my_fig,use_container_width=True)
top10_chart=top10s(chart_option)
col2.plotly_chart(go.Figure(go.Bar(y=top10_chart['Country'],x=top10_chart[chart_option],orientation='h')).update_layout(title=graph_title('Top 10 countries'),margin={'t':30}),
                  use_container_width=True)
# Creates a lineplot depending on the option selected
if chart_option == 'Imports': lineplot_imports(line_option)
else: lineplot_production(line_option)
    

# Shows the data summarized
st.markdown('Check the data here:')
with st.expander('Exporting countries consolidated data'):
    st.dataframe(df_totals.style.highlight_max(axis=0))
with st.expander('Importing countries data'):
    st.dataframe(df_imports.style.highlight_max(axis=0))



