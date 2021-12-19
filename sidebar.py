import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from matplotlib import pyplot as plt

st.set_page_config(page_title='BWS')
st.header('Data Result')

plt.style.use("ggplot")

data = {
    "num": [x for x in range(1, 11)],
    "square": [x**2 for x in range(1, 11)],
    "twice": [x*2 for x in range(1, 11)],
    "thrice": [x*3 for x in range(1, 11)]
}

rad = st.sidebar.radio("Navigation", ["Home", "Data1", "Data2"])

if rad == "Home":
    df = pd.DataFrame(data=data)

    col = st.sidebar.multiselect("Select a Column ", df.columns)

    plt.plot(df['num'], df[col])

    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

if rad == "Data1":
    excel_file = 'data.xlsx'
    sheet_name = 'Penjualan Kopi 2016-2018'

    df = pd.read_excel(excel_file,
                       sheet_name=sheet_name,
                       usecols='A:D',
                       header=0)

    # df_participants.dropna(inplace=True)

    kota = df['Kota'].unique().tolist()
    sales = df['Sales'].unique().tolist()

    sales_selection = st.slider('sales:',
                                min_value=min(sales),
                                max_value=max(sales),
                                value=(min(sales), max(sales)))

    kota_selection = st.multiselect('Kota:',
                                    kota,
                                    default=kota)

    mask = (df['Sales'].between(*sales_selection)
            ) & (df['Kota'].isin(kota_selection))
    number_of_result = df[mask].shape[0]
    st.markdown(f'*Available Result: {number_of_result}*')

    df_grouped = df[mask].groupby(by=['Rating']).count()[['Sales']]
    df_grouped = df_grouped.rename(columns={'Sales': 'Votes'})
    df_grouped = df_grouped.reset_index()

    st.dataframe(df[mask])

    bar_chart = px.bar(df_grouped,
                       x='Rating',
                       y='Votes',
                       text='Votes',
                       color_discrete_sequence=['#F63366']*len(df_grouped),
                       template='plotly_white')
    st.plotly_chart(bar_chart)


if rad == "Data2":
    df_participants = pd.read_excel('Data2.xlsx',
                                    sheet_name='Data2',
                                    usecols='A:B',
                                    header=0)

    col1, col2 = st.columns(2)
    image = Image.open('images/bws.png')
    col1.image(image,
               caption='Bank Woori Saudara',
               #  use_column_width=True)
               width=200)
    col2.dataframe(df_participants)

    pie_chart = px.pie(df_participants,
                       title='Total No. of Participants',
                       values='Total',
                       names='Nama')
    st.plotly_chart(pie_chart)
