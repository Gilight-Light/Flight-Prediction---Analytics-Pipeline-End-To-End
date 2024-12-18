import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import time
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objs as go
# from query import query ## Use this when you want query to db
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from joblib import load
import numpy as np




st.set_page_config(
    page_title="Flight Analytics And Prediction",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

alt.themes.enable("dark")

# load data from database
## df = query() 

# load data from csv for streamlit cloud
file_path = 'data/Clean_Dataset.csv'
df = pd.read_csv(file_path)

df["date"] = pd.to_datetime(df["date"]).dt.date
unique_dates = df["date"].unique()  

# Sidebar
with st.sidebar:
    st.markdown('<h1 style="color:blue;">🏂 Flight Prediction Dashboard</h1>', unsafe_allow_html=True)
    # year_list = list(df.date.unique())[::-1]
    
    # selected_year = st.selectbox('Select a year', year_list)
    # df_selected = df[df.airline == selected_year]
    # df_selected_year_sorted = df_selected.sort_values(by="date", ascending=False)
    selected_date_range = st.date_input(
        "Select a date range",
        value=(pd.to_datetime("2022-02-11"), pd.to_datetime("2022-03-31")),
        min_value=df['date'].min(),  # Giới hạn ngày bắt đầu
        max_value=df['date'].max()   # Giới hạn ngày kết thúc
    )

    class_options = ['Economy', 'Business', 'Both']
    selected_class = st.selectbox('Select a class', class_options, index=2)

    if len(selected_date_range) == 2:  # Đảm bảo người dùng đã chọn đủ 2 ngày
        start_date, end_date = selected_date_range
        df_selected = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        df_selected = df_selected.sort_values(by="date", ascending=False)
        if selected_class != 'Both':
            df_selected = df_selected[df_selected['class'] == selected_class]
    else:
        st.warning("Please select a valid date range.")


    st.title('🔍Input To Flight Prediction Dashboard🔍')
    airline = st.selectbox('Select Airline', df['airline'].unique(), index=1)
    source_city = st.selectbox('Select Source City', df['source_city'].unique(), index=1)
    departure_time = st.selectbox('Select Departure Time', df['departure_time'].unique(), index=1)
    stops = st.selectbox('Select Number of Stops', ['zero', 'one', 'two or more'], index=1)
    arrival_time = st.selectbox('Select Arrival Time', df['arrival_time'].unique(), index=1)
    destination_city = st.selectbox('Select Destination City', df['destination_city'].unique(), index=1)
    class_type = st.selectbox('Select Class', ['Economy', 'Business'], index=1)
    duration = st.number_input('Enter Flight Duration (hours)', min_value=0.1, value=2.0)
    predict_button = st.button("Predict Price")

    

st.header("ANALYTICAL PROCESSING, KPI & PREDICTIONS FLIGHT ✈️✈️✈️")

def Home():
    """
    Display the home page with various analytical metrics and visualizations.
    """
    with st.expander("VIEW EXCEL DATASET"):
        showData = st.multiselect('Filter: ', df_selected.columns.tolist(), default=df_selected.columns.tolist())
        st.dataframe(df_selected[showData], use_container_width=True)

    count_flight = float(pd.Series(df_selected['flight']).count())
    most_price = float(df_selected['price'].max())
    lowest_price = float(df_selected['price'].min())
    economy_most_flights = (df[df['class'] == 'Economy'])['airline'].value_counts().idxmax()
    business_most_flights = (df[df['class'] == 'Business'])['airline'].value_counts().idxmax()
    average_price = float(pd.Series(df_selected['price']).mean())
    investment_median = float(pd.Series(df_selected['price']).median()) 

    total1, total2, total3, total4, total5, total6 = st.columns(6, gap='small')
    with total1:
        st.info('Count Flight', icon="💰")
        st.metric(label="Count Flight", value=f"{count_flight:,.0f}")

    with total2:
        st.info('Most Price Ticket', icon="💰")
        st.metric(label="Most Price", value=f"{most_price:,.0f}")

    with total3:
        st.info('Lowest Price Ticket', icon="💰")
        st.metric(label="Lowest Price", value=f"{lowest_price:,.0f}")

    with total4:
        st.info('Average Price Ticket', icon="💰")
        st.metric(label="Average Price", value=f"{average_price:,.0f}")
    
    with total5:
        st.info('Best Airline Of Business', icon="💰")
        st.metric(label="Business", value=f"{business_most_flights}")
    
    with total6:
        st.info('Best Airline Of Economy', icon="💰")
        st.metric(label="Economy", value=f"{economy_most_flights}")

    style_metric_cards(background_color="#FFFFFF", border_left_color="#686664", border_color="#000000", box_shadow="#F71938")

    with st.expander("DISTRIBUTIONS BY FREQUENCY"):
        columns_to_plot = ['date', 'duration', 'days_left', 'price']
    
        fig, ax = plt.subplots(figsize=(16, 8))
        
        df_selected[columns_to_plot].hist(ax=ax, color='#898784', zorder=2, rwidth=0.9, legend=['Investment'])
        
        st.pyplot(fig)

Home()
freq_table = (
    df_selected.groupby(by=["airline"]).size()
    .reset_index(name="Frequency")
    .sort_values(by="Frequency", ascending=False)
)
freq_table["Percent"] = (freq_table["Frequency"] / freq_table["Frequency"].sum()) * 100

# create chart with Plotly
fig_airline = px.bar(
    freq_table,
    x="airline",
    y="Frequency",
    color="Frequency",
    text=freq_table.apply(lambda row: f"{row['Frequency']} ({row['Percent']:.1f}%)", axis=1),
    title="<b>Percent Airline</b>",
    color_discrete_sequence=["#0083b8"] * len(freq_table),
    template="plotly_white",
)

# config chart
fig_airline.update_traces(textposition="outside")
fig_airline.update_layout(
    xaxis=dict(title="Airline", tickmode="linear", tickangle=45),
    yaxis=dict(title="Frequency", showgrid=False),
    plot_bgcolor="rgba(0,0,0,0)",
)




col = st.columns((2, 3, 2), gap='medium')
with col[2]:
    counts = df_selected['stops'].value_counts()
    labels_stops = ['One Stop', 'Zero Stops', 'Two Or More']

    # create chart with plotly
    fig_stops = px.pie(
        values=counts.values,
        names=labels_stops,
        title="<b>Stop Distribution</b>",
        color_discrete_sequence=['#A1DFF7', '#F4A259', '#85C88A'],  # Màu sắc hiện đại
    )

    # config chart
    fig_stops.update_traces(
        textinfo='percent+label',  # Hiển thị phần trăm và nhãn
        hole=0.3,  # Tạo hiệu ứng "donut chart"
        pull=[0.1 if i == 0 else 0 for i in range(len(counts))]  # Làm nổi bật phần tử đầu tiên
    )

    fig_stops.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",  # Nền trong suốt
        paper_bgcolor="rgba(0,0,0,0)",  # Nền giấy trong suốt
        font=dict(color="black"),  # Màu chữ
        legend=dict(x=0.9, y=0.9),  # Đặt vị trí chú thích
    )

    st.plotly_chart(fig_stops, use_container_width=True)
    
with col[1]:
    st.plotly_chart(fig_airline, use_container_width=True)
with col[0]:
    source_city_counts = df_selected['source_city'].value_counts()
    fig_pie = px.pie(
        source_city_counts,
        values=source_city_counts.values,
        names=source_city_counts.index,
        title="<b>Source City Distribution</b>",
        color_discrete_sequence=px.colors.sequential.Viridis,
    )
    fig_pie.update_traces(
        textinfo='percent+label',
        hole=0.3,  # layout"donut chart"
        pull=[0.1 if i == len(source_city_counts) - 1 else 0 for i in range(len(source_city_counts))],
    )
    fig_pie.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black"),
        legend=dict(x=1, y=1),
    )
    st.x_chart(fig_pie, use_container_width=True)

    # chart boxplot (Price Distribution by Source City)
fig_boxplot = px.box(
        df,
        x="source_city",
        y="price",
        title="<b>Price Distribution by Source City</b>",
        color_discrete_sequence=["#0083B8"],
        template="plotly_white",
    )
fig_boxplot.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black"),
        yaxis=dict(showgrid=True, gridcolor="#cecdcd"),
        xaxis=dict(showgrid=True, gridcolor="#cecdcd"),
        xaxis_title="Source City",
        yaxis_title="Price",
    )
st.plotly_chart(fig_boxplot, use_container_width=True)

def make_prediction():
    """
    Make a prediction for the flight price based on user input.
    """
    # Tiền xử lý dữ liệu
    input_data = {
        'airline': airline,
        'source_city': source_city,
        'departure_time': departure_time,
        'stops': stops,
        'arrival_time': arrival_time,
        'destination_city': destination_city,
        'class': class_type,
        'duration': duration
    }

    label_encoder = LabelEncoder()
    loaded_model = load('gradient_boosting_model.joblib')  # Tải mô hình đã huấn luyện

    # Mã hóa dữ liệu đầu vào (trừ duration)
    encoded_input = input_data.copy()
    columns_to_encode = ['airline', 'source_city', 'departure_time', 'stops', 'arrival_time', 'destination_city', 'class']
    df_pre = df.drop(columns='date')  # Đảm bảo loại bỏ cột ngày khi mã hóa
    for col in columns_to_encode:
        encoded_input[col] = label_encoder.fit(df_pre[col]).transform([input_data[col]])[0]

    # Chuyển dữ liệu đã mã hóa thành DataFrame để đưa vào mô hình
    encoded_input_df = pd.DataFrame([encoded_input])

    # Dự đoán giá vé với mô hình đã huấn luyện
    predicted_price = loaded_model.predict(encoded_input_df)[0]

    # Hiển thị kết quả dự đoán
    total1, total2, total3, total4, total5, total6, total7 = st.columns(7, gap='small')
    with total1:
        st.info('AirLine', icon="💰")
        st.metric(label="AirLine", value=f"{airline}")

    with total2:
        st.info('Souce City', icon="💰")
        st.metric(label="Souce City", value=f"{source_city}")
    
    with total3:
        st.info('Destination City', icon="💰")
        st.metric(label="Destination City", value=f"{destination_city}")

    with total4:
        st.info('Departure Time', icon="💰")
        st.metric(label="Departure Time", value=f"{departure_time}")

    with total5:
        st.info('Number of Stops', icon="💰")
        st.metric(label="Number of Stops", value=f"{stops}")
    
    with total6:
        st.info('Arrival Time', icon="💰")
        st.metric(label="Arrival Time", value=f"{arrival_time}")
    
    with total7:
        st.info('Class', icon="💰")
        st.metric(label="Class", value=f"{class_type}")
    

    style_metric_cards(background_color="#FFFFFF", border_left_color="#686664", border_color="#000000", box_shadow="#F71938")

    st.markdown(f"""
    <div style="background-color:#4CAF50; padding:20px; border-radius:10px; 
                text-align:center; font-size:30px; color:white; 
                font-weight:bold; box-shadow:0 4px 8px rgba(0, 0, 0, 0.2);">
        <h1>Predicted Price: {predicted_price:,.0f} $</h1>
    </div>
    """, unsafe_allow_html=True)

# Chỉ khi người dùng nhấn nút "Predict Price", mới thực hiện dự đoán
if predict_button:
    make_prediction()
