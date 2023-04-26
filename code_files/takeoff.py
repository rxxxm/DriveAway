from altair.vegalite.v4.api import value
from django.forms import ModelForm
import streamlit as st
import numpy as np
import pandas as pd 
import dashboard_display
import dataframe_creation

def filter(df_dt) :

    df_dt['mode']=df_dt['mode'].astype(str).str.replace("<", "None")

    #CHOIX MODE
    choix_select_mode  = list(set(list(df_dt["mode"].values)))
    choix_select_mode.sort()
    choix_select_mode = ["*"]+choix_select_mode
    choix_mode = st.multiselect("Choisir les modes :", choix_select_mode, default="*")

    if "*" in choix_mode:
        choix_mode =choix_select_mode 
    ou     = df_dt["mode"].isin(choix_mode)  

    #CHOIX REPERTOIRE
    choix_select_repertoire  = list(set(list(df_dt.loc[ou]["name"].values)))
    choix_select_repertoire.sort()
    choix_select_repertoire = ["*"]+choix_select_repertoire
    choix_repertoire = st.multiselect("Choisir les répertoires :", choix_select_repertoire, default="*")

    if "*" in choix_repertoire:
        choix_repertoire =choix_select_repertoire 
    ou     = df_dt["mode"].isin(choix_mode)  & df_dt["name"].isin(choix_repertoire)  

    return df_dt.loc[ou]


def run(active_tab):

    """this function calls the actions needed to display the takeoff tabs
    
    Creation and modification:
    Creation date               : 04/05/2020
    Last modification date      : 16/11/2022

    @author                     : Rym Otsmane -a044390
    @author last modification   : Cyril Meunier - a008177
    """
    dt_both, name_columns = dataframe_creation.create_dataframe()

    searchfor = ['Repet','REPET','repeat','Repeat']
    dt_both = dt_both[~dt_both.name_file.str.contains('|'.join(searchfor))]

    if active_tab == "TakeOff Pleine Charge":
        dt_both = dt_both[(dt_both['AccPdlTarget'] >= 95.0) & (dt_both['AccPdlTarget'] <= 105.0)] 
    elif active_tab == "TakeOff Charge Partielle":
        dt_both = dt_both[dt_both['AccPdlTarget'] < 95]

    multiselect_filters = {}
    rangeKey = 10
    with st.sidebar:
        dataframe_creation.to_excel(dt_both, "takeoff")

        st.info(
            "Sélectionner les filtres pour obtenir une liste de véhicule "
        )
        for name in  name_columns : 
                    newlist = [x for x in  set(dt_both[name])  if pd.isnull(x) == False]
                    multiselect_filters[name] = st.multiselect(name ,newlist)
                    
        dt_both =      dataframe_creation.range_filter(dt_both,"PWT_Power_max", 10, rangeKey)
        dt_both =      dataframe_creation.range_filter(dt_both,"V1000_BV1", 0.5, rangeKey+1) #0.5
        dt_both =      dataframe_creation.range_filter(dt_both,"Curb weight (MVODM)", 100, rangeKey+2)
        dt_both =      dataframe_creation.range_filter(dt_both,"PTW (MMAC) [F2]", 100, rangeKey+3)
        dt_both =      dataframe_creation.range_filter(dt_both,"PTW + trailer (MTR) [F3]", 1, rangeKey+4)
        dt_both =      dataframe_creation.range_filter(dt_both,"ICE_Cylinders_nb", 1, rangeKey+10)
        dt_both =      dataframe_creation.range_filter(dt_both,"ICE_Capacity", 100, rangeKey+5)
        dt_both =      dataframe_creation.range_filter(dt_both,"ICE_Power_max", 10, rangeKey+6)
        dt_both =      dataframe_creation.range_filter(dt_both,"ICE_Torque_max", 20, rangeKey+7)
        dt_both =      dataframe_creation.range_filter(dt_both,"Usefull_Battery_Capacity", 1, rangeKey+9)

        with st.expander("slope"):
            options_list = np.arange(-2,51,1)
            start_value, end_value = st.select_slider(
            "", options= options_list, value=(-2, 2), key= rangeKey)
        dt_both =  dt_both[(dt_both["slope"] >= start_value) & (dt_both["slope"] <= end_value)]

    for key,value in multiselect_filters.items():
        if value :
            dt_both = dt_both.query(f"{key} == @value")

    dt_partial = dt_both.copy()
    st.title("Résultat des filtres : ")

    if active_tab == "TakeOff Pleine Charge":
        dt_both = dataframe_creation.average_points(dt_both,0)
        st.write(dt_both.astype(str))

        st.write("###")
        dt_both= filter(dt_both)
        st.write("#")

        if (dt_both['Energy'] == dt_both.iloc[0]['Energy']).all() and dt_both.iloc[0]['Energy'] == 'electric':
            energy = 1
        elif (dt_both['Energy'] == dt_both.iloc[0]['Energy']).all() and dt_both.iloc[0]['Energy'] == 'gasoline hybrid':
            energy = 2
        else :
            energy = 0
        dashboard_display.create_t80_tg01_graph(energy,dt_both)
        dashboard_display.graph_static_v3(dt_both)
        dashboard_display.dynamic_graph(dt_both)

    elif active_tab == "TakeOff Charge Partielle":
        dt_partial = dataframe_creation.average_points(dt_partial,1)

        st.write(dt_partial.astype(str))
        st.write("###")
        dt_partial= filter(dt_partial)

        st.write("#")
        dashboard_display.graph_static_partial (dt_partial)
        dashboard_display.dynamic_graph(dt_partial)
