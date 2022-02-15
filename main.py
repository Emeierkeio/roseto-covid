from datetime import datetime, timedelta
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

# Create a new column with the weekly number of new cases
def addMeans(df):
    df['nuovi_positivi_weekly'] = df['nuovi_positivi'].rolling(7).mean()
    df['ricoverati_weekly'] = df['ricoverati'].rolling(7).mean()
    return df

@st.cache(ttl=60*60*10)
def load_data():
    data = pd.read_csv('data/roseto.csv')
    data.data = pd.to_datetime(data.data, format='%Y-%m-%d')
    # Handle NaN values
    data = data.interpolate(method='bfill', limit_direction='backward', axis=0)
    addMeans(data)
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
    st.title('Roseto degli Abruzzi (TE)')
    st.markdown('**Dati COVID-19 aggiornati al {}**'.format(str(raw_data.data.max())[:10]))
    with open('data/roseto.csv') as f:
        st.download_button('Download data', f)

# Gestisce i casi in cui il giorno prima non ho avuto i dati
positiviDaAggiungere = oggi.attualmente_positivi.values[0] - ieri.attualmente_positivi.values[0]
if positiviDaAggiungere == 0:
    positiviDaAggiungere = oggi.nuovi_positivi.values[0]

ricoveratiDaAggiungere = oggi.ricoverati.values[0] - ieri.ricoverati.values[0]
if ricoveratiDaAggiungere == 0:
    ricoveratiDaAggiungere = oggi.ricoverati.values[0] - ieriancora.ricoverati.values[0]

if ieri.attualmente_positivi.values[0]:
    fine_sorveglianza = oggi.nuovi_positivi.values[0] - (oggi.attualmente_positivi.values[0] - ieri.attualmente_positivi.values[0])
else:
    fine_sorveglianza = oggi.fine_sorveglianza_ufficiali.values[0]


if fine_sorveglianza < 0:
    fine_sorveglianza = 0
with metrics:
    st.markdown('##')
    st.markdown('##')
    col1, col2, col3 = st.columns(3)
    col1.metric("Attualmente Positivi", int(oggi.attualmente_positivi.values[0]), int(positiviDaAggiungere), delta_color="inverse")
    col2.metric("Ricoverati", int(oggi.ricoverati.values[0]), int(ricoveratiDaAggiungere), delta_color="inverse")
    col3.metric("Fine Sorveglianza", int(fine_sorveglianza))




with graph:
    # Create a date picker in streamlit
    st.markdown('##')
    st.markdown('##')
    day = st.date_input('Selezione la data da cui far partire le visualizzazioni:', datetime(2021, 11, 16))
    st.write('Verranno mostrati i dati dal', day, 'a oggi')
    yesterday = datetime.today() - timedelta(days=1)
    yesterday = yesterday.date()
    days = (yesterday - day).days + 1
    print(days)
    if days < 2:
        st.error('Puoi selezionare solamente date antecedenti ad oggi')
    elif(days > len(raw_data)):
        st.error('Non ci sono dati per la data selezionata')
    else:
        st.markdown('##')
    print("x:", raw_data.tail(days))
    st.subheader('Attualmente Positivi')
    st.caption('Ciascun giorno mostra il numero totale di positivi.')
    st.plotly_chart(plotter.plotlyAreaChart(raw_data.tail(days)), use_container_width=True)
    st.markdown('##')
    st.subheader('Nuovi positivi giornalieri')
    st.caption('Ciascun giorno mostra i nuovi casi segnalati dal giorno precedente e la relativa media mobile rispetto ai sette giorni precedenti.')
    st.plotly_chart(plotter.plotlyAreaChartwithMean(raw_data.tail(days), 'nuovi_positivi'), use_container_width=True)
    st.markdown('##')
    st.subheader('Numero di ricoverati')
    st.caption('Ciascun giorno mostra il numero di persone ricoverate residenti nel comune di Roseto degli Abruzzi e la relativa media mobile rispetto ai sette giorni precedenti.')
    st.plotly_chart(plotter.plotlyAreaChartwithMean(raw_data.tail(days), 'ricoverati'), use_container_width=True)

