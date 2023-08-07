import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
tesla=yf.Ticker("TSLA")
# tesla.info["country"]
# tesla.info["sector"]
tesla_data = tesla.history(period="max")
# tesla_data.head()
url_tesla = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
data_tesla  = requests.get(url_tesla).text
soup_tesla = BeautifulSoup(data_tesla, 'html5lib')
read_html_pandas_data_tesla = pd.read_html(str(soup_tesla))
tesla_revenue=read_html_pandas_data_tesla[1]
# tesla_revenue.head()
tesla_revenue.columns = ["Date", "Revenue"]
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
# tesla_revenue.tail()
import plotly.graph_objects as go
from plotly.subplots import make_subplots
tesla_data=tesla_data.reset_index(inplace=True)
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
print(make_graph(tesla_data,tesla_revenue, "Tesla"))