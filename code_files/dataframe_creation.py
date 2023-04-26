from re import U
from altair.vegalite.v4.api import value
from django.forms import ModelForm
import streamlit as st
import numpy as np
import pandas as pd 
import dashboard_display
import altair as alt
import dashboard_display
import xlsxwriter
from io import BytesIO
from datetime import datetime

@st.cache
def create_dataframe():
    """this function create the dataframe frame containing the data for the project using
    DT file and DriveAway2PCritieria file
    
    Creation and modification:
    Creation date               : 04/05/2020
    Last modification date      : 16/11/2022

    @author                     : Rym Otsmane -a044390
    @author last modification   : Rym Otsmane -a044390
    """

    df_dt = pd.read_excel(r"I:\_All_Sites\LARDY_(F-KHEPRI)\_sharediao\DEAM\ESSAIS_AGR\BDD_Objectivation\Dashboard\Dashboard_DriveAway_New_V1.1\code_files\allDT.xlsx")
    my_set = {'Energy', 'HYB_Architecture','Type_Transmission','Class','Body',
     'Maker','Model', 'Fabrication_Year' ,'Emission_Standards_Regulation_Compliant',
     'PWT_Power_max', 'Cmax (N.m)', 'V1000_BV1', 'Vmax (km/h)', 'Usefull_Battery_Capacity',
      'km full EV pour HYB', 'Declared range on WLTC (km)', 'Curb weight (MVODM)', 'PTW (MMAC) [F2]',
     'PTW + trailer (MTR) [F3]','ICE_Starter', 'ICE_Cylinders_nb', 'ICE_Capacity','ICE_Power_max',
     'ICE_Torque_max','Marché','name'}

    df_dt= df_dt[df_dt.columns.intersection(my_set)]

    df_criteria= pd.read_csv("I:\_All_Sites\LARDY_(F-KHEPRI)\_sharediao\DEAM\ESSAIS_AGR\BDD_Objectivation\Dashboard\Dashboard_DriveAway_New_V1.1\Dashboard_DriveAway_Criteria_Updated.csv",encoding='windows-1251',sep=',')
    df_criteria.rename(columns={"G70kph": "G70","G03" : "G0-3", "G90kph" : "G90", "G50kph": "G50"}, inplace=True)

    dt_both  = pd.merge(df_dt, df_criteria, on='name')
    dt_both["mode"] .replace({"Mode_S": "Mode_SPORT", "Mode_E": "Mode_ECO","Mode_N": "Mode_NORMAL",
                            "Mode_Normal": "Mode_NORMAL", "Mode_Standard" :"Mode_NORMAL","Mode_Electric": "Mode_ELECTRIC", "Mode_Electrique" : "Mode_ELECTRIC",
                            "Mode_EV" : "Mode_ELECTRIC","Mode_Hybrid": "Mode_HYBRID", "Mode_Hybride" : "Mode_HYBRID",
                            "Mode_Mid":"Mode_NORMAL","Mode_Pure": "Mode_ELECTRIC", "Mode_Confort" : "Mode_COMFORT" }, inplace=True)
    dt_both["mode"] = dt_both["mode"].str.upper()
    dt_both["Maker"] = dt_both["Maker"].str.upper()
    dt_both["Maker"].replace({"CITROEN": "CITROËN"}, inplace=True)

    dt_both["ICE_Power_max"] = pd. to_numeric(dt_both["ICE_Power_max"], errors='coerce' )
    dt_both["ICE_Torque_max"] = pd. to_numeric(dt_both["ICE_Torque_max"], errors='coerce' )
    dt_both["Usefull_Battery_Capacity"] = pd. to_numeric(dt_both["Usefull_Battery_Capacity"], errors='coerce' )
    dt_both["ICE_Cylinders_nb"] = pd. to_numeric(dt_both["ICE_Cylinders_nb"], errors='coerce' )
    dt_both["PTW + trailer (MTR) [F3]"] = pd. to_numeric(dt_both["PTW + trailer (MTR) [F3]"], errors='coerce' )
    dt_both["PWT_Power_max"] = pd. to_numeric(dt_both["PWT_Power_max"], errors='coerce' )
    dt_both["V1000_BV1"] = pd. to_numeric(dt_both["V1000_BV1"], errors='coerce' )
    dt_both["Curb weight (MVODM)"] = pd. to_numeric(dt_both["Curb weight (MVODM)"], errors='coerce' )
    dt_both["PTW (MMAC) [F2]"] = pd. to_numeric(dt_both["PTW (MMAC) [F2]"], errors='coerce' )

    dt_both = dt_both.astype({"Model": str})
    dt_both["annee"] = dt_both["annee"].astype(str)
    # dt_both["First_Fabrication_Year"] = dt_both["First_Fabrication_Year"].astype(str)
    dt_both["Fabrication_Year"] = dt_both["Fabrication_Year"].astype(str)
    # dt_both["First_Fabrication_Year"] = dt_both["First_Fabrication_Year"].str.replace('.0', '', regex=False)
    dt_both["Fabrication_Year"] = dt_both["Fabrication_Year"].str.replace('.0', '',regex=False)

    dt_both['PWT_Power_max'] = dt_both['PWT_Power_max'].fillna(0)
    dt_both['Curb weight (MVODM)'] = dt_both['Curb weight (MVODM)'].fillna(0)
    dt_both['PTW (MMAC) [F2]'] = dt_both['PTW (MMAC) [F2]'].fillna(0)
    dt_both['ICE_Capacity'] = dt_both['ICE_Capacity'].fillna(0)
    dt_both['ICE_Power_max'] = dt_both['ICE_Power_max'].fillna(0)
    dt_both['ICE_Torque_max'] = dt_both['ICE_Torque_max'].fillna(0)
    dt_both['V1000_BV1'] = dt_both['V1000_BV1'].fillna(0)
    dt_both['Usefull_Battery_Capacity'] = dt_both['Usefull_Battery_Capacity'].fillna(0)
    dt_both['PTW + trailer (MTR) [F3]'] = dt_both['PTW + trailer (MTR) [F3]'].fillna(0)
    dt_both['ICE_Cylinders_nb'] = dt_both['ICE_Cylinders_nb'].fillna(0)

    df_dt = df_dt[['Energy'] + ['HYB_Architecture'] + ['ICE_Starter'] +  ['Type_Transmission'] +  ['Class'] + ['Body'] + 
    ['Maker']+['Model']+ ['Fabrication_Year'] +['Emission_Standards_Regulation_Compliant'] +
    ['name'] + [ col for col in df_dt.columns if col not in my_set] ]


    name_columns = (df_dt.columns.delete(-1))

    return dt_both, name_columns


def range_filter(df,column,step, rangeKey):
    #Function that creates filters that range from the min value
    #of the column to the max with the step referenced in the arguments
    #Parameters
        #the dataframe
        #the column
        #the step
        #a unique key for streamlit
    #Creation and modification:
    #Creation date               : 04/09/2022
    #Last modification date      : 25/12/2022
    
    #@author                     : Rym Otsmanne - a044390
    #@author last modification   : Rym Otsmanne - a044390

    mini = int(df[column].min())
    mini = round(mini, -2)
    maxi = int(df[column].max()) 
    maxi +=step
    options_list = np.arange(mini,maxi,step)
    with st.expander(column):
        start_value, end_value = st.select_slider(
        "", options= options_list, value=(options_list[0], options_list[-1]), key= rangeKey)
        return df[(df[column] >= start_value) & (df[column] <= end_value)]




def to_excel(df, type):
    #Function that styles the dataframe and exports it into excel
    #Parameters
        #the dataframe
    #Creation and modification:
    #Creation date               : 04/09/2022
    #Last modification date      : 06/09/2022
    
    #@author                     : Rym Otsmanne - a044390
    #@author last modification   : Rym Otsmanne - a044390

    date = (datetime.today().strftime('%d_%m_%Y'))

    if type == "idm" :
        df = df[["name","PWT_Power_max",  "Gmax",
                    "G0-3", "G50", "G70", "G90"]]
        excel_name = "IDM_Data_" +date + ".xlsx"

    else : 
            df = df[["name","Maker", "Model", "Energy", "Class", "Body", "Type_Transmission","PWT_Power_max", 
            "Curb weight (MVODM)" , "mode","SOC", "slope","AccPdlActual","tG01","t80Gmax","G1", "G2", "G0-3","Gmax", "G0-3", "G50", "G70", "G90"
            ,"zero50", "zero100", "dur90GmaxD","Gpp", "freqGpp"]]

            excel_name = "DriveAway_Criteria_" +date + ".xlsx"



    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    df_xlsx = output.getvalue()
    st.download_button(label='Télecharger DriveAway Criteria',
                                    data=df_xlsx ,
                                    file_name= excel_name)

@st.cache(allow_output_mutation=True)

def average_points(df, partial):
    #Function that styles that determines an average 
    #of the criterias for all similar try-outs on the same car
    #Parameters
        #the dataframe
        #partial : a parameter that determines if we want a dataframe with full charge or partial
    #Creation and modification:
    #Creation date               : 02/02/2023
    #Last modification date      : 02/02/2023
    
    #@author                     : Rym Otsmanne - a044390
    #@author last modification   : Rym Otsmanne - a044390

    if partial == 0:
        grouped_df = df.groupby([ 'Type_Transmission', 'Class','Body', 'Energy', 'HYB_Architecture',
                            'Maker', 'Model', 'PWT_Power_max', 'essai', 'prestation', 'mode', 'Curb weight (MVODM)',
                            "Usefull_Battery_Capacity", "name"],as_index=False, dropna=False)[['slope','PWT_Power_max',
                            'Gmax',"G0-3", "G50", "G70", "G90","tG01", "t80Gmax", "Gpp", "freqGpp" ]].mean()
    else :
        grouped_df = df.groupby([ 'Type_Transmission', 'Class','Body', 'Energy', 'HYB_Architecture',
                    'Maker', 'Model', 'PWT_Power_max', 'essai', 'prestation', 'mode', 'Curb weight (MVODM)',
                    "Usefull_Battery_Capacity", "name","AccPdlTarget"],as_index=False, dropna=False)[['slope','PWT_Power_max',
                    'Gmax',"G0-3", "G50", "G70", "G90","tG01", "t80Gmax", "Gpp", "freqGpp"]].mean()

    return grouped_df