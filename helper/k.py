import pandas as pd
# import chart_studio.plotly as py
import plotly.offline as pyoff
import plotly.graph_objs as go
from plotly.figure_factory import np
from plotly.subplots import make_subplots


def draw2(date):
    d = date[:6]
    print(dir)
    df = pd.read_csv('tx5_data/' + d + '/' + date + '.txt')
    # print(df)
    # df = df.iloc[::-1]
    print(df)
    fig = go.Figure(data=[go.Candlestick(x=df.Time,
                                         open=df.Open,
                                         high=df.High,
                                         low=df.Low,
                                         close=df.Close,
                                         name=date,
                                         increasing_line_color='red', decreasing_line_color='green')],
                    layout=go.Layout(
                        title=go.layout.Title(text=date)
                    )
                    )

    # fig2.show()
    pyoff.plot(fig)


def draw(date):
    d = date[:6]
    # print(dir)
    df = pd.read_csv('tx5_data/' + d + '/' + date + '.txt')
    print(df)
    # Create figure with secondary y-axis
    # fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.03,
                        row_width=[0.2, 0.7])
    fig['layout']['title'] = date

    fig.add_trace(go.Candlestick(x=df["Time"], open=df["Open"], high=df["High"],
                                 low=df["Low"], close=df["Close"], showlegend=False),
                  row=1, col=1
                  )

    fig.add_trace(go.Bar(x=df['Time'], y=df['Volume'], showlegend=False), row=2, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.show()
