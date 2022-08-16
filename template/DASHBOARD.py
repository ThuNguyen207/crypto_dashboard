# setup
# from matplotlib.pyplot import margins
import streamlit as st
import pandas as pd
import numpy as np
import cryptocompare as cc
from datetime import datetime
import plotly.graph_objects as go
from datetime import date
from PIL import Image
import plotly.express as px
from requests import Request, Session
from bs4 import BeautifulSoup
import requests
import json


#set variable
coinlist=np.array(['BTC','ETH','BUSD','USDC','SOL','USDT','XRP','BNB','MATIC','ADA'])
# api_key="631999bf0b5310a37e876c6773310f46c097dddcb6fdeb252ca3c17e25f0bf81"
api_key = "3ad6c9b5d03a59cc3c76d3dce0e851ab1884f79949ae13ecd2fc3a1155ebd96b"
ccobj=cc.cryptocompare._set_api_key_parameter(api_key)

#url coinmarketcap:
cmc = requests.get('https://coinmarketcap.com')
soup = BeautifulSoup(cmc.content, 'html.parser')

## Function to plot line chart, candlesticks chart for price, and bar chart for volume
def myplot(df, time_period, margin_setup, C, sma_name, ema_name):
    ## C = chart type, sma_no = SMA indecator
    if C=='Candlestick chart':
        ##candelstick-price
        figprice = go.Figure(data=[go.Candlestick(name='Prices', x=time_period, open=df['open'], high=df['high'],low=df['low'], close=df['close'])])
        figprice.add_trace(go.Scatter(name=sma_name, x=time_period, y=df[sma_name],line_color='#2e6902'))
        figprice.add_trace(go.Scatter(name=ema_name, x=time_period, y=df[ema_name],line_color='#d1025c'))
        figprice.update_layout(xaxis_rangeslider_visible=False, width=1000, height=500, hovermode='x unified', margin=margin_setup)
    elif C=='Line chart':
        ##linechart-price
        figprice=go.Figure(go.Scatter(name='Prices', x=time_period, y=df['close'],line_color='#100269'))
        figprice.add_trace(go.Scatter(name=sma_name, x=time_period, y=df[sma_name],line_color='#2e6902'))
        figprice.add_trace(go.Scatter(name=ema_name, x=time_period, y=df[ema_name],line_color='#d1025c'))
        figprice.update_layout(xaxis_rangeslider_visible=False, width=1000, height=500,hovermode='x unified', margin=margin_setup)

    ##barchar-volumn
    figvol=px.bar(df, x=time_period, y=df['volumeto'])
    figvol.update_layout(xaxis_rangeslider_visible=False,width=1000, height=300, hovermode='x unified', margin=margin_setup)
    return figprice, figvol

## Function to add SMA and EMA indecators on dataframe of coin historical prices
def sma_ema(df, sma_no, ema_no):
    ## calculate SMA: Simple Moving Average
    sma_name = 'SMA'+str(sma_no)
    df[sma_name] = df.close.rolling(sma_no).mean()
    ## calculate ema: Exponential Moving Average
    ema_name = 'EMA'+str(ema_no)
    df[ema_name] = df.close.ewm(span=ema_no, adjust=False).mean()
    return df, sma_name, ema_name

# Plot 1h
def plot_1h(coin, margin_setup, C, sma_no, ema_no):
    ## C = chart type, sma_no = SMA indecator
    df = pd.DataFrame(cc.get_historical_price_minute(coin,'USD',limit=59, exchange='CCCAGG',toTs=datetime.now()))
    time_period=[]
    for i in range(df.shape[0]):
        time_period.append(datetime.fromtimestamp(df.iloc[i,0]))
    ## add SMA and EMA indecators on current dataframe
    df, sma_name, ema_name = sma_ema(df, sma_no, ema_no)

    figprice, figvol = myplot(df, time_period, margin_setup, C, sma_name, ema_name)
    
    return figprice, figvol



# Plot 1day
def plot_1day(coin, margin_setup, C, sma_no, ema_no):
    ## C = chart type, sma_no = SMA indecator
    df = pd.DataFrame(cc.get_historical_price_minute(coin,'USD',limit=1440, exchange='CCCAGG',toTs=datetime.now()))
    time_period=[]
    for i in range(df.shape[0]):
        time_period.append((datetime.fromtimestamp(df.iloc[i,0])))
    ## add SMA and EMA indecators on current dataframe
    df, sma_name, ema_name = sma_ema(df, sma_no, ema_no)

    figprice, figvol = myplot(df, time_period, margin_setup, C, sma_name, ema_name)    
    return figprice, figvol



# Plot 1week
def plot_1week(coin, margin_setup, C, sma_no, ema_no):
    ## C = chart type, sma_no = SMA indecator
    df = pd.DataFrame(cc.get_historical_price_hour(coin,'USD',limit=167, exchange='CCCAGG',toTs=datetime.now()))
    time_period=[]
    for i in range(df.shape[0]):
        time_period.append((datetime.fromtimestamp(df.iloc[i,0])))
    ## add SMA and EMA indecators on current dataframe
    df, sma_name, ema_name = sma_ema(df, sma_no, ema_no)

    figprice, figvol = myplot(df, time_period, margin_setup, C, sma_name, ema_name)    
    return figprice, figvol


# Plot 1month
def plot_1month(coin, margin_setup, C, sma_no, ema_no):
    ## C = chart type, sma_no = SMA indecator
    df = pd.DataFrame(cc.get_historical_price_hour(coin,'USD',limit=720, exchange='CCCAGG',toTs=datetime.now()))
    time_period=[]
    for i in range(df.shape[0]):
        time_period.append((datetime.fromtimestamp(df.iloc[i,0])))
    ## add SMA and EMA indecators on current dataframe
    df, sma_name, ema_name = sma_ema(df, sma_no, ema_no)

    figprice, figvol = myplot(df, time_period, margin_setup, C, sma_name, ema_name)    
    return figprice, figvol


# Plot 6 months
def plot_6months(coin, margin_setup, C, sma_no, ema_no):
    ## C = chart type, sma_no = SMA indecator
    df = pd.DataFrame(cc.get_historical_price_day(coin,'USD',limit=181,exchange='CCCAGG',toTs=datetime.now()))
    time_period=[]
    for i in range(df.shape[0]):
        time_period.append((datetime.fromtimestamp(df.iloc[i,0])))
    ## add SMA and EMA indecators on current dataframe
    df, sma_name, ema_name = sma_ema(df, sma_no, ema_no)

    figprice, figvol = myplot(df, time_period, margin_setup, C, sma_name, ema_name)    
    return figprice, figvol


# Plot 1 year
def plot_1year(coin, margin_setup, C, sma_no, ema_no):
    ## C = chart type, sma_no = SMA indecator
    df = pd.DataFrame(cc.get_historical_price_day(coin,'USD',limit=364,exchange='CCCAGG',toTs=datetime.now()))
    time_period=[]
    for i in range(df.shape[0]):
        time_period.append((datetime.fromtimestamp(df.iloc[i,0])))
    ## add SMA and EMA indecators on current dataframe
    df, sma_name, ema_name = sma_ema(df, sma_no, ema_no)

    figprice, figvol = myplot(df, time_period, margin_setup, C, sma_name, ema_name)    
    return figprice, figvol


def dashboard(coin: str):
    #### download data from coinmarketcap
    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    coin_data = json.loads(data.contents[0])

    listings = json.loads(coin_data['props']['initialState'])['cryptocurrency']['listingLatest']['data']
    market_cap_name = 'quote.USD.marketCap'
    for i in listings[1:]:
        coin_symbol = i[[k for k, j in enumerate(listings[0]['keysArr']) if j == 'symbol'][0]]
        if coin_symbol==coin:
            coin_vol24h = '$' + f"{round(i[[k for k, j in enumerate(listings[0]['keysArr']) if j == 'quote.USD.volume24h'][0]],1):,}"        
            coin_cap = i[[k for k, j in enumerate(listings[0]['keysArr']) if j == market_cap_name][0]]
            coin_cap_pct = round(i[[k for k, j in enumerate(listings[0]['keysArr']) if j == 'quote.USD.dominance'][0]],3)
            break
    coin_cap_pct=str(f"{coin_cap_pct}" + "%")
    coin_cap='$'+str(f"{round(coin_cap/1e9,3):,}" + 'B')

    #----infor part
    pricecoin='$'+str(f"{cc.get_price(coin,currency='USD')[coin]['USD']:,}")
    change24h=str(f"{round(cc.get_avg(coin, currency='USD')['CHANGEPCT24HOUR'], 3):,}") + ' %'
    highprice='$'+str(f"{cc.get_avg(coin, currency='USD')['HIGH24HOUR']:,}")
    lowprice='$'+ str(f"{cc.get_avg(coin, currency='USD')['LOW24HOUR']:,}")
    volume24h =coin_vol24h

    # Introduction:
    icon, sym_alg, price, vol, cap, cap_pct = st.columns([1,1,1,1,1,1])
    img_path = './icons/'+ coin + '.jpg'
    icon.image(Image.open(img_path))
    
    sym_alg.text('Symbol:' + coin)
    
    coin_list=cc.get_coin_list()
    sym_alg.text('Algo:' + coin_list[coin]['Algorithm'])
    

    price.metric(label='Price', value= pricecoin, delta=change24h)
    vol.metric(label='Volume 24h', value=coin_vol24h)

    cap.metric(label='Coin market cap', value=coin_cap)
    cap_pct.metric(label='Market cap proportion', value=coin_cap_pct)

    Description = st.checkbox('Description')
    if Description:
        st.write(coin_list[coin]['Description'])

    
    #Summary column a1 : information
    st.markdown(
      """
      <h1>Coin price statistics and pairs</h1>
      """
    , unsafe_allow_html=True)

    infor, pair = st.columns(2)
    
    infordata=pd.DataFrame({'Information':['Price','Change 24h','Highest price 24h','Lowest price 24h','Volume 24h','Coin market cap','Total market cap proportion'],
    'Value':[pricecoin,change24h,highprice,lowprice,volume24h,coin_cap,coin_cap_pct]})
    infor.subheader(coin + ' Price Statistics')
    infor.table(infordata)
    
    #----pair part:
    currencyunit=np.setdiff1d(coinlist, coin)
    Pairs=[]
    Prices=[]
    for i in range(7):
        Pairs.append(coin+'/'+currencyunit[i])
        Prices.append(f"{round(cc.get_price(coin,currency=currencyunit[i])[coin][currencyunit[i]],2):,}")
    pairprice=pd.DataFrame({'Pairs':Pairs,'Price':Prices})
    pair.subheader(coin + ' Price Pairs')
    pair.table(pairprice)

    # Chart
    title="Historical Data of " + coin
    st.title(title)


    Time, Chart, sma_indecators, ema_indecators = st.columns(4)
    T = Time.selectbox('Select time',('1 Hour','1 Day','1 Week','1 Month','6 Months','1 Year'))
    C = Chart.selectbox('Select chart type',('Candlestick chart','Line chart'))
    sma_inde = sma_indecators.selectbox('SMA indecators',('SMA 5','SMA 10', 'SMA 20', 'SMA 30', 'SMA 60'))
    ema_inde = ema_indecators.selectbox('EMA indecators',('EMA 5','EMA 12', 'EMA 26', 'EMA 50'))
    sma_no = int(sma_inde[3:])
    ema_no = int(ema_inde[3:])

    margin_setup = dict(l=20, r=20, t=40, b=20)
    if T == '1 Hour':
        figprice, figvol = plot_1h(coin, margin_setup, C, sma_no, ema_no)
    elif T=='1 Day':
        figprice, figvol = plot_1day(coin, margin_setup, C, sma_no, ema_no)
    elif T=='1 Week':
        figprice, figvol = plot_1week(coin, margin_setup, C, sma_no, ema_no)
    elif T=='1 Month':
        figprice, figvol = plot_1month(coin, margin_setup, C, sma_no, ema_no)
    elif T=='6 Months':
        figprice, figvol = plot_6months(coin, margin_setup, C, sma_no, ema_no)
    else:
        figprice, figvol = plot_1year(coin, margin_setup, C, sma_no, ema_no)
        
    st.markdown(
        """
        <h2>Historical Price</h2>
        """
    , unsafe_allow_html=True)

    st.plotly_chart(figprice, use_container_width=True)

    st.markdown(
        """
        <h2>Volume</h2>
        """
    , unsafe_allow_html=True)
    st.plotly_chart(figvol,use_container_width=True)