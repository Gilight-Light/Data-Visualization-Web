from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = Dash()
server = app.server

def fix_km(x):
    return x.replace(" Km","").replace(",","")

# Đọc dữ liệu từ file car.csv
car_df = pd.read_csv("D:\PyThon\car.csv", delimiter="|", on_bad_lines="skip")
car_df["km"] = car_df["km"].apply(fix_km)
pd.set_option('display.max_columns', None)
print(car_df.head())

# Tạo ra 1 list hãng xe để đưa vào combo
car_brand_list = []
car_br_df = car_df.groupby(["car_model"]).size().reset_index(name='count')
car_br_df = car_br_df.sort_values('count', ascending = False)
for brand in car_br_df['car_model']:
    car_brand_list.append({
        "label": brand,
        "value": brand
    })

# Tạo ra 1 list gồm All, Nhập khẩu, trong nươc
imp_exp_list = []
imp_exp_df = car_df.groupby(["imp_exp"]).size().reset_index(name='count')
imp_exp_df = imp_exp_df.sort_values('count', ascending = False)
imp_exp_list.append({
        "label": "All",
        "value": "All"
    })

for imp_exp in imp_exp_df['imp_exp']:
    imp_exp_list.append({
        "label": imp_exp,
        "value": imp_exp
    })

# Tạo ra 1 list gồm All các tỉnh
From_area_list = []
fr_area_df = car_df.groupby(["area"]).size().reset_index(name='count')
fr_area_df = fr_area_df.sort_values('count', ascending = False)
for area in fr_area_df['area']:
    From_area_list.append({
        "label": area,
        "value": area
    })


# Tầm nhìn sale
def split_km(x):
    a = x.split();
    a[0] = a[0].replace(',', '')
    return a[0]

# list hàng chọn color
sm_color_out = ['Đen', 'Bạc', 'Trắng', 'Kem']
sm_color_in = ['Đen', 'Bạc', 'Trắng', 'Kem', 'Cát']
sm_area = ['Hầ Nội', 'TP HCM', 'Đà Nẵng', 'Nha Trang', 'Cần Thơ', 'Gia Lai']
sm_seat = ['7 chỗ',  '8 chỗ']

sm_km_list = []
for sm in car_df['km']:
    a = split_km(sm)
    if (int(a) > int(10000)):
        sm_km_list.append(float(1))
    else:
        sm_km_list.append(float(1.5))

car_df['sm_km'] = sm_km_list

car_df['sm_color_out'] = car_df['out_color'].apply(lambda x: float(1) if x in sm_color_out else float(0.5))

car_df['sm_color_in'] = car_df['in_color'].apply(lambda x: float(1) if x in sm_color_in else float(0.5))

car_df['sm_imp_exp'] = car_df['imp_exp'].apply(lambda x: float(1) if x == 'Nhập khẩu' else float(0.5))

car_df['sm_area'] = car_df['area'].apply(lambda x: float(1.5) if x in sm_area else float(1))

car_df['sm_seat'] = car_df['seat_num'].apply(lambda x: float(1.5) if x in sm_seat else float(1))

car_df['sm_type'] = car_df['new_old'].apply(lambda x: float(2) if x == "Xe mới" else float(1))

car_df['sum_sm'] = car_df['sm_km'] + car_df['sm_color_out'] + car_df['sm_color_in'] + car_df['sm_imp_exp'] + car_df['sm_area'] + car_df['sm_seat'] + car_df['sm_type']


print(car_df.head())

# Dựng layout
app.layout = html.Div(
    [
        html.H1("Data Visualization Web From Craw Data bonbanh.com",
                style={ "textAlign": "center",
                    "color": "#1877F2",
                    "fontFamily": "Helvetica Neue,Helvetica,Arial,sans-serif",
                    "fontSize": "48px",
                    "fontWeight": "bold",
                    "textTransform": "uppercase",
                    "letterSpacing": "1px",
                    "margin": "20px" }),
        html.Div(
            [
                html.Div("Brand of Car : ",
                         style={ "textAlign": "center",
                                "color": "#1877F2",
                                "fontFamily": "Helvetica Neue,Helvetica,Arial,sans-serif",
                                "fontSize": "28px",
                                "fontWeight": "bold",
                                "textTransform": "uppercase",
                                "letterSpacing": "1px",
                                "margin": "20px"}),
                dcc.Dropdown(
                    id="car_brand_dropdown",
                    multi=True,
                    style={"display": "block", "margin-left": "auto",
                            "margin-right": "auto", "width": "60%"},
                    options= car_brand_list,
                    value= [car_brand_list[0]['value']]# Gia tri chon mac dinh luc dau
                ),
                html.Div("Type of Car : ",
                         style={ "textAlign": "center",
                                "color": "#1877F2",
                                "fontFamily": "Helvetica Neue,Helvetica,Arial,sans-serif",
                                "fontSize": "28px",
                                "fontWeight": "bold",
                                "textTransform": "uppercase",
                                "letterSpacing": "1px",
                                "margin": "20px"}),
                dcc.Dropdown(
                    id="car_type_dropdown",
                    style={"display": "block", "margin-left": "auto",
                            "margin-right": "auto", "width": "60%"},
                    options= imp_exp_list,
                    value= imp_exp_list[0]['value']# Gia tri chon mac dinh luc dau
                ),
                html.Div("Distribution Area : ",
                         style={ "textAlign": "center",
                                "color": "#1877F2",
                                "fontFamily": "Helvetica Neue,Helvetica,Arial,sans-serif",
                                "fontSize": "28px",
                                "fontWeight": "bold",
                                "textTransform": "uppercase",
                                "letterSpacing": "1px",
                                "margin": "20px"}),
                dcc.Dropdown(
                    id="from_are_dropdown",
                    style={"displat":"block", "margin-left":"auto",
                           "margin-right":"auto", "width":"60%"},
                    options= From_area_list,
                    value= From_area_list[0]['value']# Gia tri chon mac dinh luc dau
                ),
                html.Br(),
                html.Div(
                    [
                        html.Span(
                            [
                                html.Span('Từ năm:', style={"textAlign": "center"}),
                                dcc.Input(id='from_year', value='1900', type='number',debounce = True)
                            ]
                        ),
                        html.Span(' '),
                        html.Span(
                            [
                                html.Span('Đến năm:', style={"textAlign": "center"}),
                                dcc.Input(id='to_year', value='2023', type='number',debounce = True)
                            ]
                        )
                    ], style={"textAlign": "center"}
                ),
                html.Div("Chart showing the number of vehicles and mileage traveled ",
                         style={"textAlign": "center",
                                "color": "#1877F2",
                                "fontFamily": "Helvetica Neue,Helvetica,Arial,sans-serif",
                                "fontSize": "28px",
                                "fontWeight": "bold",
                                "textTransform": "uppercase",
                                "letterSpacing": "1px",
                                "margin": "20px"}),
                dcc.Graph(id="histogram_chart"),
                html.Div("Color Category Scale Chart",
                         style={"textAlign": "center",
                                "color": "#1877F2",
                                "fontFamily": "Helvetica Neue,Helvetica,Arial,sans-serif",
                                "fontSize": "28px",
                                "fontWeight": "bold",
                                "textTransform": "uppercase",
                                "letterSpacing": "1px",
                                "margin": "20px"}),
                dcc.Graph(id="pie_chart"),
                html.Div("Color Category Scale Chart",
                         style={"textAlign": "center",
                                "color": "#1877F2",
                                "fontFamily": "Helvetica Neue,Helvetica,Arial,sans-serif",
                                "fontSize": "28px",
                                "fontWeight": "bold",
                                "textTransform": "uppercase",
                                "letterSpacing": "1px",
                                "margin": "20px"}),
                dcc.Graph(id="pie_chart_from"),
                html.Div("Sales rate based on sales promotion criteria",
                         style={"textAlign": "center",
                                "color": "#1877F2",
                                "fontFamily": "Helvetica Neue,Helvetica,Arial,sans-serif",
                                "fontSize": "28px",
                                "fontWeight": "bold",
                                "textTransform": "uppercase",
                                "letterSpacing": "1px",
                                "margin": "20px"}),
                dcc.Graph(id="pie_chart_sale")
            ]
        )

    ]
)

# Phần Callback
@app.callback(
    Output('histogram_chart', 'figure'), Output('pie_chart', 'figure'), Output('pie_chart_from', 'figure'),Output('pie_chart_sale', 'figure'),
    Input('car_brand_dropdown','value'),Input('car_type_dropdown','value'),Input('from_are_dropdown','value'),Input('from_year','value'),Input('to_year','value')
)
def update_charts(car_brand_dropdown,car_type_dropdown,from_are_dropdown,from_year,to_year):
    f_df = car_df[car_df.car_year != "< 1990"]
    if len(car_brand_dropdown) > 0:
        f_df = f_df[f_df.car_model.isin(car_brand_dropdown)]

    if car_type_dropdown!="All":
        f_df = f_df[f_df.imp_exp ==car_type_dropdown]

    if from_are_dropdown!="ALL":
        f_df = f_df[f_df.area ==from_are_dropdown]

    if from_year!="":
        f_df = f_df[f_df.car_year.astype(int) >= int(from_year)]

    if to_year!="":
        f_df = f_df[f_df.car_year.astype(int) <= int(to_year)]

    fig_histogram = px.histogram(f_df, x = "km",labels={'x': 'KM ĐÃ ĐI', 'y': 'SỐ LƯỢNG XE'})

    g_df = f_df.groupby(["out_color"]).size().reset_index(name='count')
    fig_pie = px.pie(g_df, values="count", names="out_color")

    fr_df = f_df.groupby(["imp_exp"]).size().reset_index(name='count')
    fig_pie_from = px.pie(fr_df , values='count', names="imp_exp")
    # # Tầm nhìn sale
    sale_df = f_df.groupby(["sum_sm"]).size().reset_index(name='count')
    sum_sale = float(0)
    count = float(0)
    for sale in sale_df['sum_sm'] :
        count+= 1
        sum_sale += sale
    sale_list = [sum_sale / count, float(10) - (sum_sale/count)]
    labels = ["Tỷ lệ bán được", "Tỷ lệ không bán được"]
    data= {'labels': labels, 'sale_list': sale_list}
    df = pd.DataFrame(data)
    fig_pie_sale = px.pie(df, values = 'sale_list', names ='labels')


    return fig_histogram, fig_pie, fig_pie_from, fig_pie_sale


app.run_server(debug=True)