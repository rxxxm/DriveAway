from altair.vegalite.v4.schema.channels import Tooltip
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

def create_graph(title, axe_x, axe_y ,df) :
    """
    Create a graph with parameters as arguments
    Parameters:
        title : title of the graph
        axe_x : abscissa for the graph
        axe_y : ordenate for the graph
        df : dataframe which contains the data for the graph
    Returns: 
    Creation and modification:
    Creation date               : 28/07/2020
    Last modification date      : 07/09/2021

    @author                     : Stephane Sanches - a041860
    @author last modification   : Stephane Sanches  - a041860
    """
    st.title(title)
    graph =  alt.Chart(df).mark_point().encode(
        x=axe_x, y=axe_y, color='name', shape = 'mode', tooltip=['name','Class','Body','Energy','mode', axe_x,axe_y] ).interactive()
    
    st.altair_chart(graph, use_container_width=True)

def graph_static_partial (df):
    create_graph("G03 en fonction de l'appui pédale", "AccPdlTarget", "G0-3",df)
    create_graph("Gmax en fonction de l'appui pédale", "AccPdlTarget", "Gmax",df)

def graph_static_v3(df):
    """
    Allows you to obtain several statistical graphs

    Parameters:
        df : dataframe 
     
    Returns: 
    Creation and modification:
    Creation date               : 28/06/2022
    Last modification date      : 28/06/2022

    @author                     : Rym Otsmane  - a044390
    @author last modification   : Rym Otsmane  - a044390
    """
    create_graph("freqGpp en fonction de  Gpp", "Gpp", "freqGpp",df)
    create_graph("Gmax en fonction de  tG01", "tG01", "Gmax",df)
    create_bar_graph("Histogramme du critère Gmax", "Gmax",df)
    create_bar_graph("Histogramme du critère G50", "G50",df)
    create_bar_graph("Histogramme du critère G70", "G70",df)
    create_bar_graph("Histogramme du critère G90", "G90",df)
    create_bar_graph("Histogramme du critère G0-3", "G0-3",df)

def create_t80_tg01_graph(energy,df):

    if energy == 1: 
        box = pd.DataFrame({'x1': [0.0], 'x2': [0.18], 'y1': [0.0], 'y2': [0.3]})

    elif energy == 2:
        box = pd.DataFrame({'x1': [0.0], 'x2': [0.18], 'y1': [0.0], 'y2': [0.4]})

    else :
        box = pd.DataFrame({'x1': [0.0], 'x2': [0.0], 'y1': [0.0], 'y2': [0.0]})

    st.title("t80Gmax en fonction de tG01")


    graph =  alt.Chart(df).mark_circle().encode(
        x="tG01", y="t80Gmax", color='name', tooltip=['name','Class','Body','Energy', "tG01", "t80Gmax"]
    ).interactive()

    box_graph = alt.Chart(box).mark_rect(fill='green', stroke='green', opacity=0.3).encode(
        alt.X('x1', scale=alt.Scale(domain=(-1, 1)), title = 'tG01 [m/s²]'),
        alt.Y('y1', scale=alt.Scale(domain=(-1, 1)), title = 't80 Gmax [m/s²]'),
        x2='x2',
        y2='y2'
    )

    st.altair_chart(graph + box_graph ,use_container_width=True)    

def create_bar_graph(title, axe_y ,df):
    st.title(title)
    graph = alt.Chart(df).mark_bar().encode(

        x = alt.X('count()', title = 'count of ' + axe_y),
        y = alt.Y(axe_y + ":Q", bin=True,title = axe_y)

    )

    st.altair_chart(graph,use_container_width=True)  

def graph_dynamic_v2(df, axe_x, axe_y):
    """
    Allows you to obtain a dynamics graph
    Parameters:
        df : dataframe 
        axe_x : the name of the acquisition file
        axe_y : the path of the new repository 
    Returns: 

        Creation and modification:
        Creation date               : 

        @author                     : Rym Otsmane  - a044390
        @author last modification   : Rym Otsmane  - a044390
    """


    create_graph(axe_x + " en fonction de " + axe_y, axe_x, axe_y, df)


def graphique_idm_v2 (axe_x, axe_y, title, df, df_og, color_condt,repertoire,unique_key) :
    """Allows you to obtain a  statistical graph with linear regression line
        over a grah with marks

        Parameters:
            axe_x : abscissa for the graph
            axe_y : ordenate for the graph
            title : title of the graph 
            df : dataframe 
            color_condt : condition on which the color of the points change
        Returns: 
        Creation and modification:
        Creation date               : 28/06/2022
        Last modification date      : 15/11/2022

        @author                     : Rym Otsmane  - a044390
        @author last modification   : Rym Otsmane  - a044390
        """

    st.markdown("**" + title +"**")
    show_text = st.checkbox("Afficher les noms des véhicules mis en évidence", key = unique_key)
    df['highlight'] =  np.where(df['name'].isin(repertoire), 1, 0)

    graph =  alt.Chart(df).mark_point( filled = True, opacity = 1).encode(
        x=alt.X(axe_x),
        y=alt.Y(axe_y),
        color=alt.Color(color_condt),
        tooltip=['name','Class','Body',axe_x, axe_y],
        size=alt.Size('highlight', scale=alt.Scale(range=[70, 500]), legend=None))

    graph_og =  alt.Chart(df_og).mark_point( filled = True, opacity =1).encode(
        x=alt.X(axe_x),
        y=alt.Y(axe_y))

    text = alt.Chart(df[df['name'].isin(repertoire)]).mark_text(
        align='left',
        baseline='middle',
        dx=3,
    ).encode(
        x=alt.X(axe_x),
        y=alt.Y(axe_y),
        color=alt.Color(color_condt),
        text='name'
    )

    graph.encoding.x.title = axe_x + ' [kW]'
    graph.encoding.y.title = axe_y + ' [m/s²]'

    reg = graph.transform_regression(axe_x ,axe_y).mark_line( opacity = 1, strokeDash=[5, 5]).transform_fold(
        ["linear regression selected bench"], 
        as_=["Regression", "y"]
        ).encode(alt.Color("Regression:N")).interactive()

    reg_og = graph_og.transform_regression(axe_x ,axe_y).mark_line( opacity = 1).transform_fold(
        ["linear regression all bench"], 
        as_=["Regression", "y"]
        ).encode(alt.Color("Regression:N"))

    params = alt.Chart(df).transform_regression(
        axe_x ,axe_y, params=True
    ).transform_calculate(
        intercept='round(datum.coef[0] * 100) / 100',
        slope='round(datum.coef[1] * 1000) / 1000',
    ).transform_calculate(
      text= "[selected bench] y = " + alt.datum.slope + "x + " + alt.datum.intercept

    ).mark_text(
        baseline="top",
        align="left" 
    ).encode(
        x=alt.value(20),  # pixels from left
        y=alt.value(20),  # pixels from top

        text='text:N',
  )

    params_og = alt.Chart(df_og).transform_regression(
        axe_x ,axe_y, params=True
    ).transform_calculate(
        intercept='round(datum.coef[0] * 100) / 100',
        slope='round(datum.coef[1] * 1000) / 1000',
    ).transform_calculate(
      text= "[full bench] y = " + alt.datum.slope + "x + " + alt.datum.intercept

    ).mark_text(
        baseline="top",
        align="left"
    ).encode(
        x=alt.value(20),  # pixels from left
        y=alt.value(40),  # pixels from top

        text='text:N',
  )

    if show_text : 
        st.altair_chart( graph + reg + params+ params_og + reg_og + text ,use_container_width=True)    
    else :
        st.altair_chart( graph + reg + params+  params_og + reg_og,use_container_width=True) 


def graphique_idm (axe_x, axe_y, title, df, color_condt,repertoire,unique_key) :
    """Allows you to obtain a  statistical graph with linear regression line
        over a grah with marks

        Parameters:
            axe_x : abscissa for the graph
            axe_y : ordenate for the graph
            title : title of the graph 
            df : dataframe 
            color_condt : condition on which the color of the points change
        Returns: 
        Creation and modification:
        Creation date               : 28/06/2022
        Last modification date      : 15/11/2022

        @author                     : Rym Otsmane  - a044390
        @author last modification   : Rym Otsmane  - a044390
        """

    st.markdown("**" + title +"**")
    show_text = st.checkbox("Afficher les noms des véhicules mis en évidence", key = unique_key)
    df['highlight'] =  np.where(df['name'].isin(repertoire), 1, 0)

    graph =  alt.Chart(df).mark_point( filled = True, opacity = 0.3).encode(
        x=alt.X(axe_x),
        y=alt.Y(axe_y),
        color=alt.Color(color_condt),
        tooltip=['name','Class','Body','AccPdlTarget'],
        size=alt.Size('highlight', scale=alt.Scale(range=[70, 500]), legend=None))

    text = alt.Chart(df[df['name'].isin(repertoire)]).mark_text(
        align='left',
        baseline='middle',
        dx=3,
    ).encode(
        x=alt.X(axe_x),
        y=alt.Y(axe_y),
        color=alt.Color(color_condt),
        text='name'
    )

    graph.encoding.x.title = axe_x + ' [kW]'
    graph.encoding.y.title = axe_y + ' [m/s²]'

    reg = graph.transform_regression(axe_x ,axe_y).mark_line(strokeDash=[2,2]).transform_fold(
        ["linear regression"], 
        as_=["Lines", "y"]
        ).encode(alt.Color("Lines:N")).interactive()

    if show_text : 
        st.altair_chart( graph + reg + text ,use_container_width=True)    
    else :
        st.altair_chart( graph + reg,use_container_width=True) 

def dynamic_graph(dt_both):
    """
    Create a graph with parameters as arguments
    Parameters:
        title : title of the graph
        axe_x : abscissa for the graph
        axe_y : ordenate for the graph
        df : dataframe which contains the data for the graph
    Returns: 
    Creation and modification:
    Creation date               : 15/11/2022
    Last modification date      : 15/11/2022
    
    @author                     : Rym Otsmane - a041860
    @author last modification   : Rym Otsmane  - a041860
    """

    with st.expander("Obtenir un graphique dynamique"):
        a = list(dt_both.columns)
        del a[1:7]

        axe_x = st.selectbox("Axe : abscisse", a)
        a = [None] + a
        axe_y = st.selectbox("Axe : ordonnée", a)

        if axe_y == None :
            create_bar_graph("Histogramme du critère " + axe_x,axe_x,dt_both)

        else :
            graph_dynamic_v2(dt_both,axe_x, axe_y)






