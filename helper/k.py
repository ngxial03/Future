import pandas as pd
import chart_studio.plotly as py
import plotly.offline as pyoff
import plotly.graph_objs as go
from plotly.figure_factory import np


def draw(date):
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
    # fig.show()
    pyoff.plot(fig)
