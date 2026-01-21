df_opd_2559 = pd.read_excel('../add_data/dataset/OPD/OPD2559.xls')
df_opd_2559

df_opd_2559 = df_opd_2559.loc[0:3]
df_opd_2559

len(df_opd_2559.columns)

df_opd_2559 = df_opd_2559.drop(columns=[f'Unnamed: {i}' for i in range(3,len(df_opd_2559.columns),2)])
df_opd_2559

df_opd_2559 = df_opd_2559.loc[1:3:2]
df_opd_2559

df_opd_2559.columns

df_opd_2559 = df_opd_2559.drop(columns=df_opd_2559.columns[0])
df_opd_2559

df_opd_2559 = df_opd_2559.drop(columns=['Unnamed: 1', 'Unnamed: 2'])
df_opd_2559

prov_2559 = df_opd_2559.loc[1].values
prov_2559

len(prov_2559)

no_patient_2559 = df_opd_2559.loc[3].values
no_patient_2559

df_2559 = pd.DataFrame(data={'Province':prov_2559,
                            'total_OPD': no_patient_2559})
df_2559

df_2559['Year'] = 2559
df_2559

new_df = pd.concat([new_df, df_2559], ignore_index=True)
new_df

# Test
new_df.loc[new_df['Province']=='พระนครศรีอยุธยา']


###################################################################################################################


df_opd_2562 = pd.read_excel('../add_data/dataset/OPD/OPD2562.xlsx')
df_opd_2562

df_opd_2562 = df_opd_2562.loc[0:2]
df_opd_2562

len(df_opd_2562.columns)

df_opd_2562 = df_opd_2562.drop(columns=[f'Unnamed: {i}' for i in range(4,len(df_opd_2562.columns),2)])
df_opd_2562

df_opd_2562 = df_opd_2562.loc[0:2:2]
df_opd_2562

df_opd_2562.columns

df_opd_2562 = df_opd_2562.drop(columns=df_opd_2562.columns[0])
df_opd_2562

df_opd_2562 = df_opd_2562.drop(columns=['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3'])
df_opd_2562

prov_2562 = df_opd_2562.loc[0].values
prov_2562

len(prov_2562)

no_patient_2562 = df_opd_2562.loc[2].values
no_patient_2562

df_2562 = pd.DataFrame(data={'Province':prov_2562,
                            'total_OPD': no_patient_2562})
df_2562

df_2562['Year'] = 2562
df_2562

new_df = pd.concat([new_df, df_2562], ignore_index=True)
new_df


#########################################################################################################################


df_opd_2563 = pd.read_excel('../add_data/dataset/OPD/OPD2563.xlsx')
df_opd_2563

df_opd_2563 = df_opd_2563.loc[1:3]
df_opd_2563

len(df_opd_2563.columns)

df_opd_2563 = df_opd_2563.drop(columns=[f'Unnamed: {i}' for i in range(4,len(df_opd_2563.columns),2)])
df_opd_2563

df_opd_2563 = df_opd_2563.loc[1:3:2]
df_opd_2563

df_opd_2563 = df_opd_2563.drop(columns=df_opd_2563.columns[0])
df_opd_2563

df_opd_2563 = df_opd_2563.drop(columns=['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3'])
df_opd_2563

prov_2563 = df_opd_2563.loc[1].values
prov_2563

len(prov_2563)

no_patient_2563 = df_opd_2563.loc[3].values
no_patient_2563

df_2563 = pd.DataFrame(data={'Province':prov_2563,
                            'total_OPD': no_patient_2563})
df_2563

df_2563['Year'] = 2563
df_2563

new_df = pd.concat([new_df, df_2563], ignore_index=True)
new_df


#####################################################################################################################

### IPD2556

df_ipd_2556 = pd.read_excel('../add_data/dataset/IPD/IPD2556.xls')
df_ipd_2556

df_ipd_2556 = df_ipd_2556.loc[2:4:2]
df_ipd_2556

df_ipd_2556.columns

df_ipd_2556 = df_ipd_2556.drop(columns=[df_ipd_2556.columns[0]])
df_ipd_2556

df_ipd_2556 = df_ipd_2556.drop(columns=[f'Unnamed: {i}' for i in range(4,len(df_ipd_2556.columns)+1,2)])
df_ipd_2556

df_ipd_2556 = df_ipd_2556.drop(columns=['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3'])
df_ipd_2556

prov_2556 = df_ipd_2556.loc[2].values
prov_2556

no_patient_2556 = df_ipd_2556.loc[4].values
no_patient_2556

df_2556 = pd.DataFrame(data={'Province':prov_2556,
                            'total_IPD': no_patient_2556})
df_2556

df_2556['Year'] = 2556
df_2556

df_year_province = df_year_province.merge(df_2556[['Province', 'Year', 'total_IPD']], left_on=['จังหวัด', 'ปี'], right_on=['Province', 'Year'], how='left')
df_year_province

new_df = pd.concat([new_df, df_2559], ignore_index=True)
new_df

df_year_province = df_year_province.drop(columns=['Province', 'Year'])
df_year_province

# Test
df_year_province.loc[(df_year_province['ปี']==2556) & (df_year_province['จังหวัด']=='ภูเก็ต')]




