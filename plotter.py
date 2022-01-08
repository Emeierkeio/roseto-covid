import plotly.express as px
import pandas as pd
import streamlit as st

# Open roseto.csv and plot the daily cases
def main():
    df = pd.read_csv('roseto.csv')
    df.data = pd.to_datetime(df.data, format='%Y-%m-%d')
    plot_daily_cases(df)


def plot_daily_cases(df, measure):
    fig = px.area(df, x = 'data', y= measure)


    fig.update_layout(
        legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.3,
                xanchor="center",
                x=0.5
        ),
        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        ),
    )
    return fig

if __name__ == '__main__':
    main()