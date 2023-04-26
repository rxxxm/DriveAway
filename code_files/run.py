from altair.vegalite.v4.api import value
from django.forms import ModelForm
import streamlit as st
import numpy as np
import pandas as pd 
import dashboard_display
import takeoff
import idm_ev_hyb

def interface_choice():
    """this function sets the layout of the app, and handles the selection of the tabs
    
    Creation and modification:
    Creation date               : 4/05/2020

    Last modification date      : 09/12/2022

    @author                     : Rym Otsmane -a044390
    @author last modification   : Cyril Meunier -a008177
    """

    st.set_page_config(layout="wide",page_title="DriveAway2P",page_icon = "code_files/logo.png" )
    col1, col2 = st.columns([10,1])

    with col1:
        st.title("      **Visualisation des critères DriveAway2P**")

        with col2:
            st.image("code_files/logo.png",width = 50)
    st.markdown("""
    <style>
    .stTextInput > label {
    font-size:105%; 
    color:blue;
    }

    .stMultiSelect > label {
    font-size:105%; 
    } 
    </style>
    """, unsafe_allow_html=True)


    st.markdown(
        """
    <style>
    .streamlit-expanderHeader {
        font-size: large;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True,
    )
    query_params = st.experimental_get_query_params()
    tabs = ["IDM EV-HYB", "TakeOff Pleine Charge", "TakeOff Charge Partielle"]
    if "tab" in query_params:
        active_tab = query_params["tab"][0]
    else:
        active_tab = "IDM EV-HYB"

    if active_tab not in tabs:
        st.experimental_set_query_params(tab="IDM EV-HYB")
        active_tab = "IDM EV-HYB"

    li_items = "".join(
        f"""
        <li class="nav-item">
            <a class="nav-link{' active' if t==active_tab else ''}" href="/?tab={t}">{t}</a>
        </li>
        """
        for t in tabs
    )
    tabs_html = f"""
        <ul class="nav nav-tabs">
        {li_items}
        </ul>
    """

    st.markdown(tabs_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    run(active_tab)


def run(active_tab):
    """this function calls the actions needed to display the TakeOff tabs
    
    Creation and modification:
    Creation date               : 07/07/2022

    Last modification date      : 07/07/2022

    @author                     : Rym Otsmane -a044390
    @author last modification   : Rym Otsmane -a044390
    """
    if active_tab == "IDM EV-HYB":
        idm_ev_hyb.run()

    else :
        takeoff.run(active_tab)

if __name__ == "__main__":
    interface_choice()