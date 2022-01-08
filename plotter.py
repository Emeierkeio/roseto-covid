import plotly.express as px
import plotly.graph_objects as go

def plotlyAreaChart(df):
    fig = px.area(df, x = 'data', y= 'attualmente_positivi')
    
    fig.update_layout(
        dragmode=False,
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


def plotlyAreaChartwithMean(df, measure):
    fig = px.area(df, x = 'data', y = measure)
    # Add a line chart that displays the new_cases column
    fig.add_trace(
        go.Scatter(
            x=df.data,
            y=df[measure+'_weekly'],
            name='Media mobile settimanale',
            line=dict(
                color='#FF0000',
                width=2,
                dash='dot'
            )
        )
    )

    fig.update_layout(
        dragmode=False,
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
