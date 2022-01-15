import plotly.express as px
import plotly.graph_objects as go

def plotlyAreaChart(df):
    fig = px.area(df, x = 'data', y= 'attualmente_positivi')
    
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title= 'Attualmente positivi',
        dragmode=False,
        yaxis_range=[0, df.attualmente_positivi.max() + df.attualmente_positivi.max()/10],
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
    fig.add_trace(go.Scatter(
        x=['2021-12-24','2021-12-31'],
        y=[5000, 5000],
        hoverinfo="skip",
        fill = 'tonexty',
        mode = 'none',
        fillcolor='rgba(255,255,0,0.3)',
        showlegend=False
    ))

    fig.add_annotation(text="Festività 2021",
        textangle=90,
        font=dict(
            family="Courier New, Times New Roman, serif",
            size=22,
            color="#ffffff"
            ),
        x='2021-12-28',
        y=df.attualmente_positivi.max()/2,
        showarrow=False
    )

    return fig


def plotlyAreaChartwithMean(df, measure):
    fig = px.area(df, x = 'data', y = measure)


    fig.add_trace(go.Scatter(
        x=['2021-12-24','2021-12-31'],
        y=[5000, 5000],
        hoverinfo="skip",
        fill = 'tonexty',
        mode = 'none',
        fillcolor='rgba(255,255,0,0.3)',
        showlegend=False
    ))

    fig.add_annotation(text="Festività 2021",
        textangle=90,
        font=dict(
            family="Courier New, Times New Roman, serif",
            size=22,
            color="#ffffff"
            ),
        x='2021-12-28',
        y= df[measure].max()/2,
        showarrow=False
    )

    # Add a line chart that displays the new_cases column
    fig.add_trace(
        go.Scatter(
            x=df.data,
            y=df[measure+'_weekly'],
            name='Media mobile settimanale',
            hoverinfo="skip",
            line=dict(
                color='#FF0000',
                width=2,
                dash='dot'
            )
        )
    )

    fig.update_layout(
        yaxis_range=[0, df[measure].max() + df[measure].max()/10],
        xaxis_title="Data",
        yaxis_title= measure.capitalize().replace('_', ' '),
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
