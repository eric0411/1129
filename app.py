import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# 讀取 CSV 資料
df = pd.read_csv('mag-7-rolling-past-10-years-close-prices.csv')

# 轉換日期格式
df['Date'] = pd.to_datetime(df['Date'])

# 股票名稱列表
stocks = ['AAPL', 'AMZN', 'GOOGL', 'META', 'MSFT', 'NVDA', 'TSLA']

# 初始化 Dash 應用程式
app = dash.Dash(__name__)

server = app.server

# 應用程式的佈局
app.layout = html.Div([
    html.H1("Ten-Year Stock Price Trend Dashboard", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='stock-dropdown',
        options=[{'label': stock, 'value': stock} for stock in stocks],
        multi=True,  # 可以選擇多個股票
        placeholder="Select one or more stocks",
        value=stocks  # 預設選擇全部股票
    ),
    dcc.Graph(id='stock-line-chart')
])

# 回調函數
@app.callback(
    Output('stock-line-chart', 'figure'),
    [Input('stock-dropdown', 'value')]
)
def update_chart(selected_stocks):
    if not selected_stocks:
        selected_stocks = stocks  # 如果未選擇，顯示所有股票
    
    # 使用選擇的股票資料繪製折線圖
    fig = px.line(
        df,
        x="Date",
        y=selected_stocks,
        title="Ten-year stock price trend chart"
    )
    
    # 更新圖表布局
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        legend_title="Stock"
    )
    return fig

# 啟動伺服器
if __name__ == '__main__':
    app.run(debug=True)
