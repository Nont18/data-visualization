from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import geopandas as gpd
from pythainlp.transliterate import romanize

# =========================
# 1) LOAD & PREPROCESS DATA
# =========================

df = pd.read_csv('./dataset/3/1.csv')
df_year_province = pd.read_csv('./dataset/3/df_year_province.csv')
new_df = pd.read_csv('./dataset/3/all_OPD.csv')

df_total_pop = pd.read_excel('./dataset/3/add_data/01_nurse_midpop_area_province.xlsx')

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

# Create new column
df_year_province['province_en'] = df_year_province['จังหวัด'].map(province_mapping)


# โหลด geojson 
world = gpd.read_file('./dataset/3/provinces.geojson')
# area_region = gpd.read_file('./dataset/3/reg_nesdb.geojson')

# convert string to lower character.
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






province_mapping2 = {'Bangkok':'กรุงเทพมหานคร', 'Chiang Rai':'เชียงราย', 'Chiang Mai':'เชียงใหม่', 'Nan':'น่าน', 'Phayao':'พะเยา', 'Phrae':'แพร่',
       'Mae Hong Son':'แม่ฮ่องสอน', 'Lampang':'ลำปาง', 'Lamphun':'ลำพูน', 'Tak':'ตาก', 'Phitsanulok':'พิษณุโลก',
       'Phetchabun':'เพชรบูรณ์', 'Sukhothai':'สุโขทัย', 'Uttaradit':'อุตรดิตถ์', 'Kamphaeng Phet':'กำแพงเพชร',
       'Chai Nat':'ชัยนาท', 'Nakhon Sawan':'นครสวรรค์', 'Phichit':'พิจิตร', 'Uthai Thani':'อุทัยธานี',
       'Nakhon Nayok':'นครนายก', 'Nonthaburi':'นนทบุรี', 'Pathum Thani':'ปทุมธานี',
       'Phra Nakhon Si Ayutthaya':'พระนครศรีอยุธยา', 'Lopburi':'ลพบุรี', 'Saraburi':'สระบุรี', 'Sing Buri':'สิงห์บุรี',
       'Ang Thong':'อ่างทอง', 'Kanchanaburi':'กาญจนบุรี', 'Nakhon Pathom':'นครปฐม',
       'Prachuap Khiri Khan':'ประจวบคีรีขันธ์', 'Phetchaburi':'เพชรบุรี', 'Ratchaburi':'ราชบุรี',
       'Samut Songkhram':'สมุทรสงคราม', 'Samut Sakhon':'สมุทรสาคร', 'Suphan Buri':'สุพรรณบุรี', 'Chanthaburi':'จันทบุรี',
       'Chachoengsao':'ฉะเชิงเทรา', 'Chonburi':'ชลบุรี', 'Trat':'ตราด', 'Prachinburi':'ปราจีนบุรี', 'Rayong':'ระยอง',
       'Samut Prakan':'สมุทรปราการ', 'Sa Kaeo':'สระแก้ว', 'Kalasin':'กาฬสินธุ์', 'Khon Kaen':'ขอนแก่น', 'Maha Sarakham':'มหาสารคาม',
       'Roi Et':'ร้อยเอ็ด', 'Nakhon Phanom':'นครพนม', 'Bueng Kan':'บึงกาฬ', 'Loei':'เลย', 'Sakon Nakhon':'สกลนคร',
       'Nong Khai':'หนองคาย', 'Nong Bua Lamphu':'หนองบัวลำภู', 'Udon Thani':'อุดรธานี', 'Chaiyaphum':'ชัยภูมิ',
       'Nakhon Ratchasima':'นครราชสีมา', 'Buriram':'บุรีรัมย์', 'Surin':'สุรินทร์', 'Mukdahan':'มุกดาหาร', 'Yasothon':'ยโสธร',
       'Sisaket':'ศรีสะเกษ', 'Amnat Charoen':'อำนาจเจริญ', 'Ubon Ratchathani':'อุบลราชธานี', 'Krabi':'กระบี่',
       'Chumphon':'ชุมพร', 'Nakhon Si Thammarat':'นครศรีธรรมราช', 'Phang Nga':'พังงา', 'Phuket':'ภูเก็ต', 'Ranong':'ระนอง',
       'Surat Thani':'สุราษฎร์ธานี', 'Trang':'ตรัง', 'Narathiwat':'นราธิวาส', 'Pattani':'ปัตตานี', 'Phatthalung':'พัทลุง',
       'Yala':'ยะลา', 'Songkhla':'สงขลา', 'Satun':'สตูล'}

df_total_pop['province_eng'] = df_total_pop['province_eng'].replace(province_mapping2)



year_mapping = {2024:2567, 2023:2566, 2022:2565, 2021:2564, 2020:2563, 2019:2562, 2018:2561, 2017:2560, 2016:2559, 2015:2558, 2014:2557,
                2013:2556, 2012:2555, 2011:2554}

df_total_pop['year'] = df_total_pop['year'].replace(year_mapping)


df_year_province = df_year_province.merge(
    df_total_pop[['year', 'province_eng', 'Total_population']],
    left_on=['ปี', 'จังหวัด'],
    right_on=['year', 'province_eng'],
    how='left'
)

df_year_province = df_year_province.drop(columns=['province_eng', 'year'])








# =========================
# 2) DASH APP
# =========================

app = Dash()

app.layout = [
    html.H1('Thailand Visualization', style={'textAlign': 'center'}),

    dcc.Dropdown(
        options=sorted(df_year_province['ปี'].unique()),
        value=df_year_province['ปี'].min(),
        id='dropdown-selection'
    ),
    dcc.RadioItems(['จำนวน', 'density', 'area_sqkm', 'total_OPD', 'OPD_per_nurse', 'Total_population', 'nurse_to_population_ratio'], 'จำนวน', id='dropdown-selection2', labelStyle={'display': 'inline-block', 'marginTop': '5px'}),

    dcc.Graph(id='graph-content', responsive=True, style={'width': '100%', 'height': '95vh'})
]

# =========================
# 3) CALLBACK (user interaction)
# =========================

@callback(
    Output('graph-content', 'figure'),
    # Input('world-selection', 'value'),
    Input('dropdown-selection', 'value'),
    Input('dropdown-selection2', 'value'),
)
def update_graph(value, choice):

    df_year = df_year_province[df_year_province['ปี'] == value]

    df_year.loc[:, 'density'] = df_year['จำนวน'] *100 / df_year['area_sqkm']

    df_year.loc[:, 'OPD_per_nurse'] = df_year['total_OPD'] / df_year['จำนวน'] # บ่งบอกถึงภาระงานของพยาบาล

    df_year.loc[:, 'nurse_to_population_ratio'] = df_year['จำนวน'] / df_year['Total_population']

    if world_choice == 'world':
        world_choice = world
    elif world_choice == 'area_region':
        world_choice = area_region

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

    hover_name='province_en',
    hover_data={
        'province_en': False,  
        'area_sqkm': ':.2f',  
        'density': ':.4f',   
        'จำนวน': True,     
        'total_OPD': True,
        # 'nurse_per_OPD': True,
        'OPD_per_nurse': True,
        'Total_population': True,
        'nurse_to_population_ratio': True,
    },

    color=choice,
    color_continuous_scale='OrRd',
    title=f'{choice} ในปี {value}'
    )

    fig.update_geos(fitbounds="locations", visible=False)

    return fig


if __name__ == '__main__':
    app.run(debug=True)
 
    # ขณะที่จังหวัดที่มีพื้นที่กว้างอาจประสบปัญหาการเข้าถึงบริการในเชิงภูมิศาสตร์”