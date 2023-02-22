import pandas as pd
from pandas import to_datetime
from pandas.plotting import register_matplotlib_converters
import numpy as np
from pathlib import Path
import base64
from datetime import date, datetime


import altair as alt
from PIL import Image
from vega_datasets import data
import pandas_datareader as pdr
import streamlit as st
import yfinance as yahooFinance





from htbuilder import HtmlElement, div, hr, a, p, img, styles
from htbuilder.units import percent, px
import seaborn as sns
import matplotlib.pyplot as plt
register_matplotlib_converters()


from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
import pmdarima as pm


sns.set(style="whitegrid")
pd.set_option('display.max_rows', 15)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
st.set_option('deprecation.showPyplotGlobalUse', False)











st.set_page_config(
    page_title="NYU - Finance Prediction App ", layout="wide", page_icon="./images/flask.png"
)

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded



def main():
    def _max_width_():
        max_width_str = f"max-width: 1000px;"
        st.markdown(
            f"""
        <style>
        .reportview-container .main .block-container{{
            {max_width_str}
        }}
        </style>
        """,
            unsafe_allow_html=True,
        )


    # Hide the Streamlit header and footer
    def hide_header_footer():
        hide_streamlit_style = """
                    <style>
                    footer {visibility: hidden;}
                    </style>
                    """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # increases the width of the text and tables/figures
    _max_width_()

    # hide the footer
    hide_header_footer()

image_edhec = Image.open('images/nyu.png')
st.image(image_edhec, width=200)

st.sidebar.header("Dashboard")
st.sidebar.markdown("---")

st.sidebar.header("Select Stock Symbol")
list_symbols = ['AAPL', 'AMZN', 'IBM','MSFT','TSLA','NVDA',
                    'PG','JPM','WMT','CVX','BAC','PFE','GOOG','FB',
                'ADBE','AXP','BBY','BA','CSCO','C','DIS','EBAY','ETSY','GE','INTC','JPM']
dictionary_symbols = {
    'AAPL':'Apple',
    'AMZN':'Amazon',
    'IBM':'IBM',
    'MSFT':'Microsoft',
    'TSLA':'Tesla',
    'NVDA':'Nvidia',
    'PG':'Procter & Gamble',
    'JPM':'J&P Morgan',
    'WMT':'Wallmart',
    'CVX':'Chevron Corporation',
    'BAC':'Bank of America',
    'PFE':'Pfizer',
    'GOOG':'Alphabet',
    'FB':'Meta',
    'ADBE':'Adobe',
    'AXP':'American Express',
    'BBY':'Best Buy',
    'BA':'Bpeing',
    'CSCO': 'Cisco',
    'C': 'Citigroup',
    'DIS': 'Disney',
    'EBAY': 'eBay',
    'ETSY': 'Etsy',
    'GE': 'General Electric',
    'INTC': 'Intel',
    'JPM': 'JP Morgan Chase',
}
symbols = st.sidebar.multiselect("", list_symbols, list_symbols[:5])


st.sidebar.header("Select Stock KPI")
list_kpi = ['High', 'Low','Open','Close','Volume']
kpi = st.sidebar.selectbox("", list_kpi)





@st.cache_data
def get_data():
    source = data.stocks()
    source = source[source.date.gt("2004-01-01")]
    return source


@st.cache_data(ttl=60 * 60 * 24)
def get_chart(data):
    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Evolution of stock prices")
        .mark_line()
        .encode(
            x="date",
            y=kpi,
            color="symbol",
            # strokeDash="symbol",
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(date)",
            y=kpi,
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("date", title="Date"),
                alt.Tooltip(kpi, title="Price (USD)"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()


st.title("NYU - Finance Prediction App 📈")

st.markdown(
    """
    [<img src='data:image/png;base64,{}' class='img-fluid' width=25 height=25>](https://github.com/gaetanbrison/app-predictive-analytics) <small> app-predictive-analytics 1.0.0 | June 2022</small>""".format(
        img_to_bytes("./images/github.png")
    ),
    unsafe_allow_html=True,
)




start_date = st.date_input(
        "Select start date",
        date(2017, 8, 1),
        min_value=datetime.strptime("2017-08-01", "%Y-%m-%d"),
        max_value=datetime.now(),
    )









list_dataframes = []
for i in range(0,len(symbols)):
    df = yahooFinance.Ticker(symbols[i])
    df_data = df.history()
    df_inter = pd.DataFrame(
        {'symbol': [symbols[i]]*len(list(df_data.index)),
        'date': list(df_data.index),
        kpi: list(df_data[kpi])
        })
    list_dataframes.append(df_inter)

df_master = pd.concat(list_dataframes).reset_index(drop=True)
list_date = df_master['date'].to_list()
list_date_new = [i.replace(tzinfo=None) for i in list_date]
df_master['date'] = list_date_new
df_master = df_master[df_master['date'] > pd.to_datetime(start_date)]


st.subheader(" ")
st.subheader("01 - Show  Selected Stocks Time Series ")
st.subheader(" ")




chart = get_chart(df_master)
st.altair_chart((chart).interactive(), use_container_width=True)

if st.button('Display  📦  used in code  🔍  '):

    snippet = f"""
    
    ## Import Packages    
    
    import pandas as pd
    from pandas import to_datetime
    from pandas.plotting import register_matplotlib_converters
    import numpy as np
    from pathlib import Path
    import base64
    from datetime import date, datetime
    
    
    import altair as alt
    import streamlit as st
    from PIL import Image
    from vega_datasets import data
    import pandas_datareader as pdr
    
    
    from htbuilder import HtmlElement, div, hr, a, p, img, styles
    from htbuilder.units import percent, px
    import seaborn as sns
    import matplotlib.pyplot as plt
    register_matplotlib_converters()
    
    
    from statsmodels.tsa.seasonal import seasonal_decompose
    from statsmodels.tsa.stattools import adfuller
    import statsmodels.api as sm
    import pmdarima as pm
    
    
    sns.set(style="whitegrid")
    pd.set_option('display.max_rows', 15)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    
    """
    code_header_placeholder = st.empty()
    snippet_placeholder = st.empty()
    snippet_placeholder.code(snippet)

    st.write('Here is the list of packages used in this example:')

snippet = f"""

## Create interactive graph based on input dataset

chart = get_chart(df_master)
st.altair_chart((chart).interactive(), use_container_width=True)


"""
code_header_placeholder = st.empty()
snippet_placeholder = st.empty()
code_header_placeholder.markdown(f"##### Code")
snippet_placeholder.code(snippet)

st.subheader(" ")
st.subheader("02 - Show  Dataset")
st.subheader(" ")

head = st.radio('View from top (head) or bottom (tail)', ('Head', 'Tail'))

if head == 'Head':
    st.dataframe(df_master.reset_index(drop=True).head(100))
else:
    st.dataframe(df_master.reset_index(drop=True).tail(100))



snippet = f"""

## Display datasets of stocks concatenated in one dataframe

if head == 'Head':
    st.dataframe(df_master.reset_index(drop=True).head(100))
else:
    st.dataframe(df_master.reset_index(drop=True).tail(100))


"""
code_header_placeholder = st.empty()
snippet_placeholder = st.empty()
code_header_placeholder.markdown(f"##### Code")
snippet_placeholder.code(snippet)









st.subheader(" ")
st.subheader("03 - Select One Stock for the Analysis")
st.subheader(" ")

st.header("Select Symbol to Forecast")
symbol_forecast = st.selectbox("", symbols)
st.success(f'You have selected {dictionary_symbols[symbol_forecast]} stock. Here are the top 5 rows from dataset')

df_2 = yahooFinance.Ticker(symbols[i])
df_data_2 = df_2.history()
df_inter_2 = pd.DataFrame(
         {'symbol': [symbol_forecast]*len(list(df_data_2.index)),
         'date': list(df_data_2.index),
         kpi: list(df_data_2[kpi])
         })

df_inter_2 = pd.concat(list_dataframes).reset_index(drop=True)
list_date = df_inter_2['date'].to_list()
list_date_new = [i.replace(tzinfo=None) for i in list_date]
df_inter_2['date'] = list_date_new
df_inter_2 = df_inter_2[df_inter_2['date'] > pd.to_datetime(start_date)]


df_inter_3 = df_inter_2[['date', kpi]]
df_inter_3.columns = ['date', kpi]
df_inter_3 = df_inter_3.rename(columns={'date': 'ds', kpi: 'y'})
df_inter_3['ds'] = to_datetime(df_inter_3['ds'])
st.dataframe(df_inter_3.head())


df_final = df_inter_3.copy()
df_final['ds'] = pd.to_datetime(df_final['ds'],infer_datetime_format=True)
df_final = df_final.set_index(['ds'])


df_final2 = df_final.asfreq(pd.infer_freq(df_final.index))

start_date = datetime(2018,1,2)
end_date = datetime(2022,6,1)
df_final3 = df_final2[start_date:end_date]


df_final4 = df_final3.interpolate(limit=2, limit_direction="forward")
df_final5 = df_final4.interpolate(limit=2, limit_direction="backward")

plt.figure(figsize=(14,4))
plt.plot(df_final5)
plt.title(f'Variation of {dictionary_symbols[symbol_forecast]} Stock overtime', fontsize=20)
plt.ylabel('Stock value in ($)', fontsize=16)
st.pyplot()



snippet = f"""

## Display time serie of selected stock

df_data_2 = pdr.get_data_yahoo(symbol_forecast)
df_inter_2 = pd.DataFrame(
        'symbol': [symbol_forecast]*len(list(df_data_2.index)),
         'date': list(df_data_2.index),
         kpi: list(df_data_2[kpi])
         )


df_inter_3 = df_inter_2[['date', kpi]]
df_inter_3.columns = ['date', kpi]
df_inter_3 = df_inter_3.rename(columns='date': 'ds', kpi: 'y')
df_inter_3['ds'] = to_datetime(df_inter_3['ds'])
st.dataframe(df_inter_3.head())


df_final = df_inter_3.copy()
df_final['ds'] = pd.to_datetime(df_final['ds'],infer_datetime_format=True)
df_final = df_final.set_index(['ds'])


df_final2 = df_final.asfreq(pd.infer_freq(df_final.index))

start_date = datetime(2018,1,2)
end_date = datetime(2022,6,1)
df_final3 = df_final2[start_date:end_date]


df_final4 = df_final3.interpolate(limit=2, limit_direction="forward")
df_final5 = df_final4.interpolate(limit=2, limit_direction="backward")

plt.figure(figsize=(14,4))
plt.plot(df_final5)
plt.title(f'Variation of Stock overtime', fontsize=20)
plt.ylabel('Stock value in ($)', fontsize=16)
st.pyplot()


"""
code_header_placeholder = st.empty()
snippet_placeholder = st.empty()
code_header_placeholder.markdown(f"##### Code")
snippet_placeholder.code(snippet)







st.subheader(" ")
st.subheader(f"04 - Decomposition of the {dictionary_symbols[symbol_forecast]} Stock Time Serie")
st.subheader(" ")

plt.rc('figure',figsize=(14,8))
plt.rc('font',size=15)
result = seasonal_decompose(df_final5,model='additive')
fig = result.plot()
st.pyplot()

st.subheader(" ")
st.subheader("05 - Mathematic Recap of the SARIMA Model")
st.subheader(" ")

st.write("An autoregressive integrated moving average, or ARIMA, is a statistical analysis model that uses"
         " time series data to either better understand the data set or to predict future trends."
"A statistical model is autoregressive if it predicts future values based on past values. For example, an ARIMA model"
" might seek to predict a stock's future prices based on its past performance or forecast a company's"
" earnings based on past periods.")

st.markdown("**KEY TAKEAWAYS**")

st.markdown("* Autoregressive integrated moving average (ARIMA) models predict future values based on past values.")
st.markdown("* ARIMA makes use of lagged moving averages to smooth time series data.")
st.markdown("* They are widely used in technical analysis to forecast future security prices.")
st.markdown("* Autoregressive models implicitly assume that the future will resemble the past.")
st.markdown("* Therefore, they can prove inaccurate under certain market conditions, such as financial crises or periods of rapid technological change.")


image_arima = Image.open('images/arima.png')
st.image(image_arima, width=1000)

st.subheader(" ")
st.subheader(f"06 - Summary of SARIMA Model Fitted on {dictionary_symbols[symbol_forecast]}  Stock")
st.subheader(" ")


mod = sm.tsa.statespace.SARIMAX(df_final5.y,
                                order=(0, 0, 1),
                                seasonal_order=(1, 1, 1, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod.fit()
st.write(results.summary())


snippet = f"""

## Output Summary of SARIMA Model

mod = sm.tsa.statespace.SARIMAX(df_final5.y,
                                order=(0, 0, 1),
                                seasonal_order=(1, 1, 1, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod.fit()
st.write(results.summary())


"""
code_header_placeholder = st.empty()
snippet_placeholder = st.empty()
code_header_placeholder.markdown(f"##### Code")
snippet_placeholder.code(snippet)



st.subheader(" ")
st.subheader(f"07 - One Step Ahead forecast of {dictionary_symbols[symbol_forecast]}  stock using ARIMA Model")
st.subheader(" ")


pred = results.get_prediction(start=pd.to_datetime('2018-06-01'), dynamic=False)
pred_ci = pred.conf_int()
ax = df_final5.y['2018':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 4))
ax.fill_between(pred_ci.index,
               pred_ci.iloc[:, 0],
               pred_ci.iloc[:, 1], color='k', alpha=.2)
ax.set_xlabel('Date')
ax.set_ylabel('Retail_sold')
plt.legend()
plt.show()
st.pyplot()

snippet = f"""

## Run of one step ahead forecast


pred = results.get_prediction(start=pd.to_datetime('2018-06-01'), dynamic=False)
pred_ci = pred.conf_int()
ax = df_final5.y['2018':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 4))
ax.fill_between(pred_ci.index,
               pred_ci.iloc[:, 0],
               pred_ci.iloc[:, 1], color='k', alpha=.2)
ax.set_xlabel('Date')
ax.set_ylabel('Retail_sold')
plt.legend()
plt.show()
st.pyplot()


"""
code_header_placeholder = st.empty()
snippet_placeholder = st.empty()
code_header_placeholder.markdown(f"##### Code")
snippet_placeholder.code(snippet)


st.subheader(" ")
st.write("##### MSE and RMSE are kpis used to judge on how well our ARIMA model performed in the prediction"
         f"of future {dictionary_symbols[symbol_forecast]} stock values")
st.subheader(" ")

y_forecasted = pred.predicted_mean
y_truth = df_final5.y['2018-06-01':]
mse = ((y_forecasted - y_truth) ** 2).mean()
st.success('The Mean Squared Error is {}'.format(round(mse, 2)))
st.success('The Root Mean Squared Error is {}'.format(round(np.sqrt(mse), 2)))


snippet = f"""

## Calculate goodness of predictions

y_forecasted = pred.predicted_mean
y_truth = df_final5.y['2018-06-01':]
mse = ((y_forecasted - y_truth) ** 2).mean()
st.success('The Mean Squared Error is '.format(round(mse, 2)))
st.success('The Root Mean Squared Error is '.format(round(np.sqrt(mse), 2)))

"""
code_header_placeholder = st.empty()
snippet_placeholder = st.empty()
code_header_placeholder.markdown(f"##### Code")
snippet_placeholder.code(snippet)

st.subheader(" ")
st.write('##### Display of last 10 predictions ')
st.subheader(" ")
y_forecasted = pred.predicted_mean
st.dataframe(y_forecasted.tail(10))


snippet = f"""

## Display Last 10 Predictions 

y_forecasted = pred.predicted_mean
st.dataframe(y_forecasted.tail(10))

"""
code_header_placeholder = st.empty()
snippet_placeholder = st.empty()
code_header_placeholder.markdown(f"##### Code")
snippet_placeholder.code(snippet)



st.markdown("### Congrats you know how ARIMA model works and how to code it 🎉")




if __name__=='__main__':
    main()

st.markdown(" ")
st.markdown("### 👨🏼‍💻 **App Contributors:** ")
st.image(['images/gaetan.png'], width=100,caption=["Gaëtan Brison"])

st.markdown(f"####  Link to Project Website [here]({'https://github.com/gaetanbrison/app-predictive-analytics'}) 🚀 ")
st.markdown(f"####  Feel free to contribute to the app and give a ⭐️")


def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;background - color: white}
     .stApp { bottom: 80px; }
    </style>
    """
    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1,

    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)

def footer2():
    myargs = [
        " Made by ",
        link("https://www.edhec.edu/en", "EDHEC - Gaëtan Brison"),
        "👨🏼‍💻"
    ]
    layout(*myargs)


if __name__ == "__main__":
    footer2()

