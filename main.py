from mimetypes import read_mime_types
import streamlit as st
import pandas as pd
import plotter
st.set_page_config(
     page_title="Covid-19 Roseto",
     page_icon="assets/favicon.ico",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://github.com/Emeierkeio/roseto-covid/issues',
         'Report a bug': "https://github.com/Emeierkeio/roseto-covid/issues",
         'About': '''Dashboard realizzata da [Mirko Tritella](https://www.github.com/Emeierkeio) utilizzando i dati pubblicati quotidianamente sulla pagina Facebook [Città di Roseto degli Abruzzi](https://www.facebook.com/cittadiroseto).
         Licenza dati: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).''',
     }
 )

@st.cache
def load_data():
    data = pd.read_csv('roseto.csv')
    data.data = pd.to_datetime(data.data, format='%Y-%m-%d')
    # Handle NaN values
    data = data.interpolate(method='bfill', limit_direction='backward', axis=0)
    return data


raw_data = load_data()

twoDaysMeasures = raw_data.tail(2)
threeDaysMeasures = raw_data.tail(3)

oggi = twoDaysMeasures.tail(1)
ieri = twoDaysMeasures.head(1)
ieriancora = threeDaysMeasures.head(1)

header = st.container()
metrics = st.container()
graph = st.container()

with header:
    st.title('COVID-19 a Roseto degli Abruzzi (TE)')
    st.subheader('Dati aggiornati al ' + str(raw_data.data.max())[:10])


with metrics:
    col1, col2, col3 = st.columns(3)
    col1.metric("Attualmente Positivi", int(oggi.attualmente_positivi.values[0]), int(oggi.attualmente_positivi.values[0] - ieri.attualmente_positivi.values[0]), delta_color="inverse")
    col2.metric("Ricoverati", int(oggi.ricoverati.values[0]), int(oggi.ricoverati.values[0] - ieri.ricoverati.values[0]), delta_color="inverse")
    col3.metric("Fine Sorveglianza", int(oggi.fine_sorveglianza.values[0]))


    col_1, col_2 = st.columns(2)
    if col_1.checkbox('Mostra dati'):
        st.dataframe(raw_data)
        
    with open('roseto.csv') as f:
        col_2.download_button('Scarica dati', f)
        




with graph:
    days = st.slider('Seleziona la quantità di giorni di cui vuoi visualizzare i dati', 0, len(raw_data.index), 120)

    st.subheader('Attualmente Positivi')
    st.caption('Ciascun giorno mostra il numero totale di positivi in quel giorno.')
    st.plotly_chart(plotter.plotlyAreaChart(raw_data.tail(days), 'attualmente_positivi'), use_container_width=True)

    st.subheader('Nuovi positivi giornalieri')
    st.caption('Ciascun giorno mostra i nuovi casi segnalati dal giorno precedente.')
    st.plotly_chart(plotter.plotlyAreaChart(raw_data.tail(days), 'nuovi_positivi'), use_container_width=True)

    st.subheader('Numero di ricoverati')
    st.caption('Ciascun giorno mostra il numero di persone ricoverate in quel giorno residenti nel comune di Roseto degli Abruzzi.')
    st.plotly_chart(plotter.plotlyAreaChart(raw_data.tail(days), 'ricoverati'), use_container_width=True)

