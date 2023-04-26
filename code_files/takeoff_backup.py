from altair.vegalite.v4.api import value
from django.forms import ModelForm
import streamlit as st
import numpy as np
import pandas as pd 
import dashboard_display
import takeoff
import idm_ev_hyb

@st.cache
def create_dataframe():
    # return  pd.read_excel("I:\_All_Sites\LARDY_(F-KHEPRI)\_sharediao\DEAM\ESSAIS_AGR\BDD_Objectivation\\DT.xlsx")
    return  pd.read_excel("I:\_All_Sites\LARDY_(F-KHEPRI)\_sharediao\DEAM\ESSAIS_AGR\BDD_Objectivation\Dashboard\Dashboard_DriveAway_New_V1.1\code_files\DT_backup.xlsx")

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
    ###########################################################################################

    return df_dt.loc[ou]

def run(active_tab):

    df_dt = create_dataframe()
    df_criteria= pd.read_csv("I:\_All_Sites\LARDY_(F-KHEPRI)\_sharediao\DEAM\ESSAIS_AGR\BDD_Objectivation\DriveAway2P_Criteria.csv",encoding='windows-1251',sep=';')
    searchfor = ['Repet','REPET','repeat','Repeat']
    df_dt.rename(columns={"ICE_Power_max": "Power_max" }, inplace=True)
    df_criteria.rename(columns={"ICE_Power_max": "Power_max","G70kph": "G70","G03" : "G0-3", "G90kph" : "G90"}, inplace=True)


    if active_tab == "TakeOff Pleine Charge":
        df_criteria = df_criteria[df_criteria['pedale_press'] == 100.0]

    elif active_tab == "TakeOff Charge Partielle":
        df_criteria = df_criteria[df_criteria['pedale_press'] != 100.0]
    df_criteria = df_criteria[~df_criteria.name_file.str.contains('|'.join(searchfor))]
    df_criteria = df_criteria[~df_criteria.name_file.str.contains('|'.join(searchfor))]

    dt_both  = pd.merge(df_dt, df_criteria, on='name')

    name_columns = (df_dt.columns)

    multiselect_filters = {}
    with st.sidebar:
        st.info(
            "Sélectionner les filtres pour obtenir une liste de véhicule "
        )
        type_graphic = st.checkbox("Graphique dynamique")
        for name in  name_columns : 
                    newlist = [x for x in  set(dt_both[name])  if pd.isnull(x) == False]
                    multiselect_filters[name] = st.multiselect(name ,newlist)
        
    for key,value in multiselect_filters.items():
        if value :
            dt_both = dt_both.query(f"{key} == @value")

    dt_both.drop(columns=['ICE', 'ICE_Rpm_torque_max'], inplace=True)
    dt_both = dt_both.astype({"Model": str})
    dt_both["mode"].replace({"Mode_S": "Mode_SPORT", "Mode_E": "Mode_ECO","Mode_N": "Mode_NORMAL",
                            "Mode_Normal": "Mode_NORMAL", "Mode_Standard" :"Mode_NORMAL","Mode_Electric": "Mode_ELECTRIC", "Mode_Electrique" : "Mode_ELECTRIC",
                            "Mode_EV" : "Mode_ELECTRIC","Mode_Hybrid": "Mode_HYBRID", "Mode_Hybride" : "Mode_HYBRID",
                            "Mode_Mid":"Mode_NORMAL","Mode_Pure": "Mode_PURE", "Mode_Confort" : "Mode_COMFORT" }, inplace=True)

    st.title("Résultat des filtres : ")
    st.write(dt_both.astype(str))
    a = list(dt_both.columns)
    del a[1:7]
    if type_graphic:
        axe_x = st.selectbox("Axe : abscisse", a)
        a = [None] + a
        axe_y = st.selectbox("Axe : ordonée", a)

    if active_tab == "TakeOff Pleine Charge":
        st.write("###")
        dt_both= filter(dt_both)
        st.write("#")

        if (dt_both['Energy'] == dt_both.iloc[0]['Energy']).all() and dt_both.iloc[0]['Energy'] == 'electric':
            energy = 1
        elif (dt_both['Energy'] == dt_both.iloc[0]['Energy']).all() and dt_both.iloc[0]['Energy'] == 'gasoline hybrid':
            energy = 2
        else :
            energy = 0
        if type_graphic:
            if axe_y == None :
                dashboard_display.create_bar_graph("Histogramme du critère" + axe_x,axe_x,dt_both)

            else :
                dashboard_display.graph_dynamic_v2(dt_both,axe_x, axe_y)
        else :
            dashboard_display.create_t80_tg01_graph(energy,dt_both)
            dashboard_display.graph_static_v3(dt_both)

    elif active_tab == "TakeOff Charge Partielle":
            st.write("###")
            dt_both= filter(dt_both)
            st.write("#")
            if type_graphic:
                if axe_y == None :
                    dashboard_display.create_bar_graph("Histogramme du critère" + axe_x,axe_x,dt_both)
                else :
            
                    dashboard_display.graph_dynamic_v2(dt_both,axe_x, axe_y)
            else :
                dashboard_display.graph_static_partial (dt_both)

