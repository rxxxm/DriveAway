from re import U
from altair.vegalite.v4.api import value
from django.forms import ModelForm
import streamlit as st
import numpy as np
import pandas as pd 
import dashboard_display
import altair as alt
import dashboard_display
import dataframe_creation

def multiselect_checkbox(df):
    repertoires = df["name"].unique()
    options = st.multiselect("Choisir les répertoires  à mettre en evidence:", repertoires)
    return options

def run():
    """this function calls the actions needed to display the TakeOff tabs
    
    Creation and modification:
    Creation date               : 04/05/2020

    Last modification date      : 09/12/2022

    @author                     : Rym Otsmane -a044390
    @author last modification   : Cyril Meunier -a008177
    """

    dt_both, name_columns = dataframe_creation.create_dataframe()
    multiselect_filters = {}
    rangeKey = 0

    searchfor = ['Repet','REPET','repeat','Repeat','REPEAT']
    dt_both = dt_both[~dt_both.name_file.str.contains('|'.join(searchfor))]
    dt_both = dt_both[((dt_both['AccPdlTarget'] >=95.0) & (dt_both['AccPdlTarget'] <=105.0)
              & (dt_both['slope'] == 0))]

    dt_og = dt_both.copy()

    with st.sidebar:
        dataframe_creation.to_excel(dt_both, "idm")
        st.info(
            "Sélectionner les filtres pour obtenir une liste de véhicule "
        )
        for name in  name_columns : 
                    newlist = [x for x in  set(dt_both[name])  if pd.isnull(x) == False]
                    multiselect_filters[name] = st.multiselect(name ,newlist)
                    
        dt_both =      dataframe_creation.range_filter(dt_both,"PWT_Power_max", 10, rangeKey)
        dt_both =      dataframe_creation.range_filter(dt_both,"V1000_BV1", 0.5, rangeKey+1)
        dt_both =      dataframe_creation.range_filter(dt_both,"Curb weight (MVODM)", 100, rangeKey+2)
        dt_both =      dataframe_creation.range_filter(dt_both,"PTW (MMAC) [F2]", 100, rangeKey+3)
        # dt_both =      dataframe_creation.range_filter(dt_both,"PTW + trailer (MTR) [F3]", 1, rangeKey+4)
        dt_both =      dataframe_creation.range_filter(dt_both,"ICE_Cylinders_nb", 1, rangeKey+10)
        dt_both =      dataframe_creation.range_filter(dt_both,"ICE_Capacity", 100, rangeKey+5)
        dt_both =      dataframe_creation.range_filter(dt_both,"ICE_Power_max", 10, rangeKey+6)
        dt_both =      dataframe_creation.range_filter(dt_both,"ICE_Torque_max", 20, rangeKey+7)
        dt_both =      dataframe_creation.range_filter(dt_both,"Usefull_Battery_Capacity", 1, rangeKey+9)

    for key,value in multiselect_filters.items():
        if value :
            dt_both = dt_both.query(f"{key} == @value")


    dt_both = dataframe_creation.average_points(dt_both,0)
    dt_og = dataframe_creation.average_points(dt_og,0)

    dt_full_hyb_n = dt_both[(dt_both['Energy'] == "gasoline hybrid") &
                      ((dt_both['mode'] == "MODE_NORMAL")  |
                     ( dt_both['mode'] == "MODE_MYSENSE") | 
                     ( dt_both['mode'] == "MODE_4WD") |
                      (dt_both['mode'] == "MODE_COMFORT"))] 


    dt_og_full_hyb_n = dt_og[(dt_og['Energy'] == "gasoline hybrid")  &
                     ((dt_og['mode'] == "MODE_NORMAL")  |
                     ( dt_og['mode'] == "MODE_MYSENSE") | 
                     ( dt_og['mode'] == "MODE_4WD") |
                      (dt_og['mode'] == "MODE_COMFORT"))] 

    dt_full_hyb_s = dt_both[
                    ((dt_both['mode'] == "MODE_SPORT") | 
                    (dt_both['mode'] == "MODE_POWER")) 
                    & (dt_both['Energy'] == "gasoline hybrid" )] 

    dt_og_full_hyb_s = dt_og[
                    ((dt_og['mode'] == "MODE_SPORT") |
                    (dt_og['mode'] == "MODE_POWER")) 
                    & (dt_og['Energy'] == "gasoline hybrid" )] 

    dt_full_hyb_125 = dt_og[((dt_og['mode'] == "MODE_SPORT") | 
                    (dt_og['mode'] == "MODE_POWER")) 
                    & (dt_og['Energy'] == "gasoline hybrid" )] 

    dt_og_hyb_125 = dt_og[((dt_og['mode'] == "MODE_SPORT") |
                    (dt_og['mode'] == "MODE_POWER")) 
                    & (dt_og['Energy'] == "gasoline hybrid" )] 

    i = 1


    with st.container():
        st.title("Targets HYB")
        st.header("100% Accel mode Nominal :")
        st.write(dt_full_hyb_n)

        st.write("##")
        if dt_full_hyb_n.empty:
            st.write("#")
        else : 

            repertoire= st.multiselect("Choisir les répertoires  à mettre en evidence:", dt_full_hyb_n["name"].unique(), key = 1)

            dashboard_display.graphique_idm_v2("PWT_Power_max", 'Gmax', 'Gmax vs Pmax',dt_full_hyb_n,dt_og_full_hyb_n,'Class',repertoire, i)
            dashboard_display.graphique_idm_v2("PWT_Power_max", 'G0-3', 'G0-3 vs Pmax',dt_full_hyb_n,dt_og_full_hyb_n,'Class',repertoire, i +1)
            dashboard_display.graphique_idm_v2("PWT_Power_max", 'G50', 'G50 vs Pmax',dt_full_hyb_n,dt_og_full_hyb_n,'Class',repertoire, i +2)
            dashboard_display.graphique_idm_v2("PWT_Power_max", 'G70', 'G70 vs Pmax',dt_full_hyb_n,dt_og_full_hyb_n,'Class',repertoire, i + 3)
            dashboard_display.graphique_idm_v2("PWT_Power_max", 'G90', 'G90 vs Pmax',dt_full_hyb_n,dt_og_full_hyb_n,'Class',repertoire, i + 4)
            
            st.header("100% Accel Mode Pleine Perfo :")
            st.write(dt_full_hyb_s)
            st.write("##")
            if dt_full_hyb_s.empty:
                st.write("#")
            else : 

                repertoire= st.multiselect("Choisir les répertoires  à mettre en evidence:", dt_full_hyb_s["name"].unique(), key = 2)

                dashboard_display.graphique_idm_v2("PWT_Power_max", 'Gmax', 'Gmax vs Pmax',dt_full_hyb_s,dt_og_full_hyb_s,'Class',repertoire, i +5)
                dashboard_display.graphique_idm_v2("PWT_Power_max", 'G0-3', 'G0-3 vs Pmax',dt_full_hyb_s,dt_og_full_hyb_s,'Class',repertoire, i + 6)
                dashboard_display.graphique_idm_v2("PWT_Power_max", 'G50', 'G50 vs Pmax',dt_full_hyb_s,dt_og_full_hyb_s,'Class',repertoire, i + 7)
                dashboard_display.graphique_idm_v2("PWT_Power_max", 'G70', 'G70 vs Pmax',dt_full_hyb_s,dt_og_full_hyb_s,'Class',repertoire, i + 8)
                dashboard_display.graphique_idm_v2("PWT_Power_max", 'G90', 'G90 vs Pmax',dt_full_hyb_s,dt_og_full_hyb_s,'Class',repertoire, i + 9)


            st.header("125% Accel Mode Pleine Perfo :")
            st.write(dt_full_hyb_s)
            st.write("##")
            if dt_full_hyb_s.empty:
                st.write("#")
            else : 

                repertoire= st.multiselect("Choisir les répertoires  à mettre en evidence:", dt_full_hyb_125["name"].unique(), key = 3)


                dashboard_display.graphique_idm_v2("PWT_Power_max", 'Gmax', 'Gmax vs Pmax',dt_full_hyb_125,dt_og_hyb_125,'Class',repertoire, i +10)
                dashboard_display.graphique_idm_v2("PWT_Power_max", 'G0-3', 'G0-3 vs Pmax',dt_full_hyb_125,dt_og_hyb_125,'Class',repertoire, i + 11)
                dashboard_display.graphique_idm_v2("PWT_Power_max", 'G50', 'G50 vs Pmax',dt_full_hyb_125,dt_og_hyb_125,'Class',repertoire, i + 12)
                dashboard_display.graphique_idm_v2("PWT_Power_max", 'G70', 'G70 vs Pmax',dt_full_hyb_125,dt_og_hyb_125,'Class',repertoire, i + 13)
                dashboard_display.graphique_idm_v2("PWT_Power_max", 'G90', 'G90 vs Pmax',dt_full_hyb_125,dt_og_hyb_125,'Class',repertoire, i + 14)


        dt_full_ev = dt_both[ (dt_both['Energy'] == 'electric' ) & ((dt_both['mode'] == 'Mode_SPORT') | (dt_both['mode'] == 'MODE_NORMAL') )] 
        dt_og_full_ev = dt_og[ (dt_og['Energy'] == 'electric' ) & ((dt_og['mode'] == 'Mode_SPORT') | (dt_og['mode'] == 'MODE_NORMAL') )] 

        st.title("Targets EV")
        st.write(dt_full_ev)
        st.write("##")
        if dt_full_ev.empty:
            st.write("#")
        else : 
            repertoire= st.multiselect("Choisir les répertoires  à mettre en evidence:", dt_full_ev["name"].unique(), key = 4)
            dashboard_display.graphique_idm_v2("PWT_Power_max", 'Gmax', 'Gmax vs Pmax',dt_full_ev,dt_og_full_ev,'mode',repertoire, i + 15)
            dashboard_display.graphique_idm_v2("PWT_Power_max", 'G0-3', 'G0-3 vs Pmax',dt_full_ev,dt_og_full_ev,'mode',repertoire, i + 16)
            dashboard_display.graphique_idm_v2("PWT_Power_max", 'G50', 'G50 vs Pmax',dt_full_ev,dt_og_full_ev,'mode',repertoire, i + 17)
            dashboard_display.graphique_idm_v2("PWT_Power_max", 'G70', 'G70 vs Pmax',dt_full_ev,dt_og_full_ev,'mode',repertoire, i + 18)
            dashboard_display.graphique_idm_v2("PWT_Power_max", 'G90', 'G90 vs Pmax',dt_full_ev,dt_og_full_ev,'mode',repertoire, i + 19)


