import plotly.express as px

def plotlyAreaChart(df, measure):
    fig = px.area(df, x = 'data', y= measure)
    
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
