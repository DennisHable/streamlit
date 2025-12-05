import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title='Covid19 data explorer',
    page_icon=None,
    layout='centered',
    initial_sidebar_state='expanded')

@st.cache_data
def load_data(date):
    confirmed = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
    deaths    = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
    recovered = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
    date_columns = [x for x in confirmed][4:]

    confirmed = confirmed.groupby(['Country/Region'])[date_columns].sum().reset_index()
    deaths    = deaths.groupby(['Country/Region'])[date_columns].sum().reset_index()
    recovered = recovered.groupby(['Country/Region'])[date_columns].sum().reset_index()

    countries = confirmed['Country/Region'].to_list()

    confirmed.rename(columns={'Country/Region':'Country'}, inplace=True)
    deaths.rename(columns={'Country/Region':'Country'}, inplace=True)
    recovered.rename(columns={'Country/Region':'Country'}, inplace=True)

    confirmed = confirmed.set_index(confirmed.Country)[date_columns].T
    deaths = deaths.set_index(deaths.Country)[date_columns].T
    recovered = recovered.set_index(recovered.Country)[date_columns].T
    countries = [x for x in confirmed]

    return countries, date_columns, confirmed, recovered, deaths

@st.cache_data
def get_plotly_object(selected_countries, date_from, date_to, show_confirmed, show_deaths, show_recovered, show_legend, logaritmic):
    date_from = date_from.strftime('%-m/%-d/%y')
    date_to = date_to.strftime('%-m/%-d/%y')

    fig=go.Figure()


    for x in selected_countries:

        if show_confirmed:
            fig.add_trace(
                go.Scatter(
                    y=confirmed.loc[date_from:date_to, x].to_list(),
                    x=dates[dates.index(date_from):dates.index(date_to)],
                    name=x+' confirmed'
                )
            )

        if show_deaths:
            fig.add_trace(
                go.Scatter(
                    y=deaths.loc[date_from:date_to, x].to_list(),
                    x=dates[dates.index(date_from):dates.index(date_to)],
                    name=x+' deaths'
                )
            )

        if show_recovered:
            fig.add_trace(
                go.Scatter(
                    y=recovered.loc[date_from:date_to, x].to_list(),
                    x=dates[dates.index(date_from):dates.index(date_to)],
                    name=x+' recovered'
                )
            )

    if logaritmic:
        ya = 'log'
    else:
        ya = 'linear'

    fig.update_layout(
        title="Number of COVID19 confirmed cases, deaths and recovered",
        xaxis_title="Date",
        yaxis_title="Cases (logarithmic scale)",
        yaxis_type=ya, # switch log scale on for y axis
        hovermode='x', # compare data on hoover by default
        showlegend=show_legend
      )

    return fig


countries, dates, confirmed, recovered, deaths = load_data(datetime.today().strftime('%Y-%m-%d'))

st.title('Covid19 data explorer')

# sidebar
selected_countries = st.sidebar.multiselect(
    "Select countries",
    options=countries,
    default='Czechia',
    key='ms_1'
)

date_from = st.sidebar.date_input(
    "Date from",
    min_value = datetime.strptime(dates[0], '%m/%d/%y'),
    max_value = datetime.strptime(dates[-1], '%m/%d/%y'),
    value=datetime.strptime(dates[0], '%m/%d/%y'),
    key="date_from"
)

date_to = st.sidebar.date_input(
    "Date to",
    min_value = datetime.strptime(dates[0], '%m/%d/%y'),
    max_value = datetime.strptime(dates[-1], '%m/%d/%y'),
    value=datetime.strptime(dates[-1], '%m/%d/%y'),
    key="date_to"
)

show_confirmed = st.sidebar.checkbox("Show confirmed cases", value=True, key='check_1')
show_deaths = st.sidebar.checkbox("Show deaths", value=True, key='check_2')
show_recovered = st.sidebar.checkbox("Show recovered", value=True, key='check_3')
show_legend = st.sidebar.checkbox("Show legend", value=True, key='check_4')
logaritmic = st.sidebar.checkbox("Log scale", value=True, key='check_5')

# use data to generate plot

plotly_fig = get_plotly_object(selected_countries, date_from, date_to,show_confirmed,show_deaths,show_recovered,show_legend,logaritmic)
st.write(plotly_fig)
