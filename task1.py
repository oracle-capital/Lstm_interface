import streamlit as st
import pandas as pd 
import yfinance as yf
import plotly.express as px
import investpy as ipy
from monte_carlo import get_prediction
from logo_scraper import get_logo


apptitle = 'Monte Carlo Prediction'

st.set_page_config(page_title=apptitle, page_icon=":chart_with_upwards_trend:")

st.title('Monte Carlo Prediction')

st.sidebar.markdown("## Selectioner le titre et la periode ")

dropdown = st.sidebar.selectbox("Choose a stock", ipy.get_stocks(country='united states').name)

start = st.sidebar.date_input('Debut', value =pd.to_datetime('07-01-2022'))
end = st.sidebar.date_input('Fin', value = pd.to_datetime('today'))

start = start.strftime('%Y-%m-%d')
end = end.strftime('%Y-%m-%d')

stocks = ipy.get_stocks(country='united states') 

stocks.set_index("name", inplace = True)
ticker =  stocks.loc[dropdown,'symbol']
st.write(ticker)

url = get_logo(ticker)
url = str(url)

st.markdown('__________________________________________________________')
st.markdown('<center>  '+dropdown+'                <img src="'+url+'" alt="stock logo"></center>', unsafe_allow_html=True)
st.markdown('__________________________________________________________')

df = yf.download(tickers=ticker, start=start, end=end, interval='1m')['Close']


predictions, future_price = get_prediction(df) 
st.write('Future Price : ', round(future_price,2))
fig = px.line(predictions)
st.plotly_chart(fig, use_container_width=False, sharing="streamlit")


