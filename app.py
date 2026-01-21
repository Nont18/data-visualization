# from dash import Dash, html, dcc, callback, Output, Input
# import plotly.express as px
# import pandas as pd
# import geopandas as gpd
# import pythainlp
# from pythainlp.transliterate import romanize

# df = pd.read_csv('./dataset/3/1.csv')
# df2 = pd.read_csv('./dataset/3/total_nurses.csv')

# app = Dash()

# # Requires Dash 2.17.0 or later
# app.layout = [
#     html.H1(children='Number of nurses', style={'textAlign':'center'}),
#     dcc.Dropdown(df['ปี'].unique(), id='dropdown-selection'),
#     dcc.Graph(id='graph-content')
# ]


# @callback(
#     Output('graph-content', 'figure'),
#     Input('dropdown-selection', 'value')
# )
# def update_graph(value):

#     # if value is None:
#     #     value = df['ปี'].min()

#     df_year_province = (
#         df.groupby(['ปี', 'จังหวัด'])['จำนวน']
#         .sum()
#         .reset_index()
#     )

#     df_year = df_year_province[df_year_province['ปี'] == value]

#     def Th2En(provinces):
#         province_lst = {province : romanize(province, engine='tltk') for province in provinces}
#         return province_lst

#     province_mapping = Th2En(df['จังหวัด'].unique())
#     df['จังหวัด'] = df['จังหวัด'].replace(province_mapping)

#     # Load provinces.geojson
#     world = gpd.read_file('./dataset/3/provinces.geojson')

#     for i, province in enumerate(world['pro_en']):
#         # print(province.lower())
#         world['pro_en'][i] = province.strip().lower()

#     def world_Th2En(provinces):
#         province_lst = {world['pro_en'][i].strip():romanize(province, engine='tltk') for i, province in enumerate(provinces)}
#         print(province_lst)
#         return province_lst
    
#     world_mapping = world_Th2En(world['pro_th'])
#     world['pro_en'] = world['pro_en'].replace(world_mapping)

#     fig = px.choropleth(
#         df_year,
#         geojson= world,
#         locations='จังหวัด',
#         featureidkey='properties.pro_en',
#         color='จำนวน',
#         color_continuous_scale='OrRd',
#         title=f'Number of nurses in {value}'
#     )

#     fig.update_geos(fitbounds="locations", visible=False)

#     return fig

# if __name__ == '__main__':
#     app.run(debug=True)



from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import geopandas as gpd
from pythainlp.transliterate import romanize

# =========================
# 1) LOAD & PREPROCESS DATA (ทำครั้งเดียว)
# =========================

# df = pd.read_csv('./dataset/3/1.csv')
df = pd.read_csv('../3/1.csv')
# df_year_province = pd.read_csv('./dataset/3/df_year_province.csv')
df_year_province = pd.read_csv('../3/df_year_province.csv')
new_df = pd.read_csv('../3/all_OPD.csv')

# รวมข้อมูล ปี–จังหวัด
df_year_province = (
    df.groupby(['ปี', 'จังหวัด'])['จำนวน']
    .sum()
    .reset_index()
)

# # สร้าง mapping ไทย → อังกฤษ (romanize)
# province_mapping = {
#     p: romanize(p, engine='tltk').strip().lower()
#     for p in df_year_province['จังหวัด'].unique()
# }

# print(df_year_province['จังหวัด'].unique())

# ต้อง map ระหว่าง df_year_province['จังหวัด'].unique() : world['pro_en'].unique()
province_mapping = {
    'กระบี่':'krabi', 'กรุงเทพมหานคร':'bangkok', 'กาญจนบุรี':'kanchanaburi', 'กาฬสินธุ์':'kalasin', 'กำแพงเพชร':'kamphaeng phet', 'ขอนแก่น':'khon kaen',
 'จันทบุรี':'chanthaburi', 'ฉะเชิงเทรา':'chachoengsao', 'ชลบุรี':'chonburi', 'ชัยนาท':'chainat', 'ชัยภูมิ':'chaiyaphum', 'ชุมพร':'chumphon', 'ตรัง':'trang', 'ตราด':'trat',
 'ตาก':'tak', 'นครนายก':'nakhon nayok', 'นครปฐม':'nakhon pathom', 'นครพนม':'nakhon phanom', 'นครราชสีมา':'nakhon ratchasima', 'นครศรีธรรมราช':'nakhon si thammarat',
 'นครสวรรค์':'nakhon sawan', 'นนทบุรี':'nonthaburi', 'นราธิวาส':'narathiwat', 'น่าน':'nan', 'บึงกาฬ':'bueng kan', 'บุรีรัมย์':'buriram', 'ปทุมธานี':'pathum thani',
 'ประจวบคีรีขันธ์':'prachuap khiri khan', 'ปราจีนบุรี':'prachin buri', 'ปัตตานี':'pattani', 'พระนครศรีอยุธยา':'phra nakhon si ayutthaya', 'พะเยา':'phayao',
 'พังงา':'phang nga', 'พัทลุง':'phatthalung', 'พิจิตร':'phichit', 'พิษณุโลก':'phitsanulok', 'ภูเก็ต':'phuket', 'มหาสารคาม':'maha sarakham', 'มุกดาหาร':'mukdahan',
 'ยะลา':'yala', 'ยโสธร':'yasothon', 'ระนอง':'ranong', 'ระยอง':'rayong', 'ราชบุรี':'ratchaburi', 'ร้อยเอ็ด':'roi et', 'ลพบุรี':'lopburi', 'ลำปาง':'lampang',
 'ลำพูน':'lamphun', 'ศรีสะเกษ':'sisaket', 'สกลนคร':'sakon nakhon', 'สงขลา':'songkhla', 'สตูล':'satun', 'สมุทรปราการ':'samut prakan', 'สมุทรสงคราม':'samut songkhram',
 'สมุทรสาคร':'samut sakhon', 'สระบุรี':'saraburi', 'สระแก้ว':'sa kaeo', 'สิงห์บุรี':'sing buri', 'สุพรรณบุรี':'suphan buri', 'สุราษฎร์ธานี':'surat thani',
 'สุรินทร์':'surin', 'สุโขทัย':'sukhothai', 'หนองคาย':'nong khai', 'หนองบัวลำภู':'nong bua lamphu', 'อำนาจเจริญ':'amnat charoen', 'อุดรธานี':'udon thani',
 'อุตรดิตถ์':'uttaradit', 'อุทัยธานี':'uthai thani', 'อุบลราชธานี':'ubon ratchathani', 'อ่างทอง':'ang thong', 'เชียงราย':'chiang rai', 'เชียงใหม่':'chiang mai',
 'เพชรบุรี':'phetchaburi', 'เพชรบูรณ์':'phetchabun', 'เลย':'loei', 'แพร่':'phrae', 'แม่ฮ่องสอน':'mae hong son'
}

# ❗ ไม่แก้ df ต้นฉบับ → สร้าง column ใหม่
df_year_province['province_en'] = df_year_province['จังหวัด'].map(province_mapping)


# โหลด geojson ครั้งเดียว
# world = gpd.read_file('./dataset/3/provinces.geojson')
world = gpd.read_file('../3/provinces.geojson')
# area_region = gpd.read_file('./dataset/3/reg_nesdb.geojson')

# แก้ SettingWithCopyWarning + normalize ตัวอักษร
world['pro_en'] = world['pro_en'].str.strip().str.lower()

# Check ว่า มีจังหวัดไหนเขียนไม่ตรงกันหรือไม่ ดดยเราจะเปลี่ยน df_year_province['province_en'] ให้ตรงกับ world['pro_en'] แต่ส่วนนี้คือ check รายชื่อจังหวัดที่ไม่ตรงกับ world['pro_en'] เฉย
for item in world['pro_en'].unique():
    if item not in df_year_province['province_en'].unique():
        print(item)

# เปลี่ยน ให้ df_year_province['province_en'] ให้ตรงกับ world['pro_en'] เพื่อเพิ่ม column ชื่อ area_sqkm ใน df_year_province
change_df_year_province_to_world_mapping = {'phranakhonsi-ayutthaya':'phranakhonsiayutthaya',
                                            'Angthong':'angthong',
                                            'roi-et':'roiet',
                                            'chachoengthrao':'chachoengsao',
                                            'utradit':'uttaradit'}

df_year_province['province_en'] = df_year_province['province_en'].replace(change_df_year_province_to_world_mapping)

# เพิ่ม column ['area_sqkm'] ลงใน df_year_province 
for i, province in enumerate(df_year_province['province_en']):
    # print(province)
    for temp_value in world['pro_en']:
        if province == temp_value:
            # df_year_province['area_sqkm'][i] = world.loc[world['pro_en']==province]['area_sqkm']
            # df_year_province.loc[i, "area_sqkm"] = world.loc[world['pro_en']==province]['area_sqkm']
            df_year_province.loc[i, "area_sqkm"] = world.loc[world['pro_en']==province, 'area_sqkm'].values[0]
            # print(world.loc[world['pro_en']==province]['area_sqkm'].values)
            # print(world.loc[world['pro_en']==province]['area_sqkm'].values[0])

            

df_year_province = df_year_province.merge(
    new_df[['Province', 'Year', 'total_OPD']],
    left_on=['จังหวัด', 'ปี'],
    right_on=['Province', 'Year'],
    how='left'
)

df_year_province = df_year_province.drop(columns=['Province', 'Year'])




# =========================
# 2) DASH APP
# =========================

app = Dash()

app.layout = [
    html.H1('Thailand Visualization', style={'textAlign': 'center'}),

    # dcc.RadioItems(['world', 'area_region'], 'world', id='world-selection', labelStyle={'display': 'inline-block', 'marginTop': '5px'}),

    dcc.Dropdown(
        options=sorted(df_year_province['ปี'].unique()),
        value=df_year_province['ปี'].min(),
        id='dropdown-selection'
    ),
    # dcc.Dropdown(['จำนวน', 'density', 'area_sqkm', 'total_OPD', 'OPD_per_nurse'], id='dropdown-selection2'),
    dcc.RadioItems(['จำนวน', 'density', 'area_sqkm', 'total_OPD', 'OPD_per_nurse'], 'จำนวน', id='dropdown-selection2', labelStyle={'display': 'inline-block', 'marginTop': '5px'}),

    # dcc.Graph(id='graph-content', responsive=True, style={'width': '1200px', 'height': '900px'})
    dcc.Graph(id='graph-content', responsive=True, style={'width': '100%', 'height': '95vh'})
]

# =========================
# 3) CALLBACK (เหลือเฉพาะ logic แสดงผล)
# =========================

@callback(
    Output('graph-content', 'figure'),
    # Input('world-selection', 'value'),
    Input('dropdown-selection', 'value'),
    Input('dropdown-selection2', 'value'),
)
def update_graph(value, choice):

    df_year = df_year_province[df_year_province['ปี'] == value]

    # df_year['density'] = df_year['จำนวน'] / df_year['area_sqkm']
    df_year.loc[:, 'density'] = df_year['จำนวน'] *100 / df_year['area_sqkm']

    # df_year.loc[:, 'nurse_per_OPD'] = df_year['จำนวน'] / df_year['total_OPD']
    df_year.loc[:, 'OPD_per_nurse'] = df_year['total_OPD'] / df_year['จำนวน'] # บ่งบอกถึงภาระงานของพยาบาล

    # if world_choice == 'world':
    #     world_choice = world
    # elif world_choice == 'area_region':
    #     world_choice = area_region

    # fig = px.choropleth(
    #     df_year,
    #     geojson=world,
    #     locations='province_en',
    #     featureidkey='properties.pro_en',
    #     hover_name = 'area_sqkm',
    #     hover_data = 'density',
    #     color='จำนวน',
    #     color_continuous_scale='OrRd',
    #     title=f'Number of nurses in {value}'
    # )

    fig = px.choropleth(
    df_year,
    geojson=world,
    locations='province_en',
    featureidkey='properties.pro_en',

    hover_name='province_en',   # ชื่อหลักด้านบน
    hover_data={
        'province_en': False,   # ไม่ต้องซ้ำ
        'area_sqkm': ':.2f',    # พื้นที่ (km²)
        'density': ':.4f',      # ความหนาแน่น
        'จำนวน': True,           # จะแสดงหรือไม่ก็ได้
        'total_OPD': True,
        # 'nurse_per_OPD': True,
        'OPD_per_nurse': True,
    },

    color=choice,
    color_continuous_scale='OrRd',
    title=f'{choice} ในปี {value}'
    )

    fig.update_geos(fitbounds="locations", visible=False)

    return fig


if __name__ == '__main__':
    app.run(debug=True)
    # “กรุงเทพมหานครมีความหนาแน่นของพยาบาลต่อพื้นที่สูงกว่าเชียงใหม่อย่างมาก
    # ซึ่งสะท้อนให้เห็นถึงการกระจุกตัวของบุคลากรทางการแพทย์ในเขตเมือง
    # ขณะที่จังหวัดที่มีพื้นที่กว้างอาจประสบปัญหาการเข้าถึงบริการในเชิงภูมิศาสตร์”