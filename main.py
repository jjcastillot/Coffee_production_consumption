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

# Define a function to plot the choropleths
def prod_plot(df, column, color_scale):
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
        margin={'t': 60},  # Increased top margin to ensure title visibility
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
        margin={'t': 60},  # Increased top margin to ensure title visibility
    )
    # Show the figure
    return fig

def create_world_plot(chart_option):
    match chart_option:
        case 'Production':
            return prod_plot(df_totals, chart_option, 'Blues')
        case 'Domestic Consumption':
            return prod_plot(df_totals, chart_option, 'Blues')
        case 'Gross Openings':
            return prod_plot(df_totals, chart_option, 'Blues')
        case 'Exports':
            return prod_plot(df_totals, chart_option, 'Blues')
        case 'Imports':
            return imports_plot('Blues')
        case 'Production Over Area':
            return prod_plot(df_totals, chart_option, 'Blues')
        case 'Dom. Consumption Ratio':
            return prod_plot(df_totals, chart_option, 'Blues')
        case _:
            return prod_plot(df_totals, chart_option, 'Blues')

def top10s(column):
    if column == 'Imports':
        top10 = df_imports[['Country', 'Code', 'Totals']].sort_values(by='Totals', ascending=False).head(10)
        top10 = top10.sort_values(by='Totals', ascending=True)
        top10.columns = ['Country', 'Code', 'Imports']
        return top10
    else:
        top10 = df_totals[['Country', 'Code', column]].sort_values(by=column, ascending=False).head(10)
        top10 = top10.sort_values(by=column, ascending=True)
        return top10

def lineplot_production(country):
    '''Create a line plot of imports for a given country code'''
    country_prod = df_production[df_production['Country'] == country].iloc[:, 2:-3]
    country_prod = country_prod.T
    country_prod.rename(columns={country_prod.columns[0]: f'{country} Production in thousands 60kg bags'}, inplace=True)
    country_prod['Dom. consumption in thousands 60kg bags'] = df_consumption[df_consumption['Country'] == country].iloc[:, 2:-3].T
    st.line_chart(data=country_prod, height=300, use_container_width=True)

def lineplot_imports(country):
    '''Create a line plot of imports for a given country code'''
    country_imports = df_imports[df_imports['Country'] == country].iloc[:, 1:-5].T
    country_imports.rename(columns={country_imports.columns[0]: f'{country} Imports in thousands 60kg bags'}, inplace=True)
    st.line_chart(data=country_imports, height=300, use_container_width=True)

######################################################################################################

# Import excel files after initial row cleaning
# @st.cache_d
