#!/usr/bin/env python
# coding: utf-8

# # Evaluating CLM Simulations at NEON Tower Sites -- Tutorial -- Interactive Plots
# 
# This tutorial provides a tool for interacive evaluations and analysis of CLM at NEON tower sites.  This tool is based on Bokeh python package.
# 
# **⚠️ Note: Before starting this tutorial, please make sure you successfully completed a simulation using the `NEON_Simulation_Tutorial` . Please use the same NEON site/sites here that you've already completed simulations for.**
# ***

# __In this tutorial :__
# 
# The notebook provide tools for interactive plotting and analysis of CLM at NEON tower sites.  Below you will find steps to: 
# 1. Create interactive app for showing tseries 
# 1. Create interactive app for scatter plots and statitical summary 

# Please use the same NEON site/sites that you've already completed the simulations for.

# In[1]:


neon_sites = ["ABBY","BART", "BLAN", "CPER", "DCFS","DSNY"]
#neon_site = neon_sites[0]


# Please make sure that you've succesfully completed the CLM simulations for these sites. When a simulation completes, the data are transferred to the `archive` directory.
# 
# Similar to the previous tutorials, you can check the history output files in the `archive` folder. 

# In[2]:


get_ipython().system('ls /Users/negins/Desktop/Simulations/archive/{neon_sites[0]}.transient/lnd/hist/*2018*.nc |head -20')


# ### 1- Import Python Libraries
# 
# Run the below code to import the required python libraries for this notebook:

# In[3]:


#Import Libraries
get_ipython().run_line_magic('matplotlib', 'inline')

import os
import sys
import time

import numpy as np
import pandas as pd
import xarray as xr

from glob import glob
from os.path import join, expanduser

import matplotlib
import matplotlib.pyplot as plt

from scipy import stats

from neon_utils import download_eval_files


# In[4]:


#Specify the year
year = "2018"


# ## 2- Load Pre-processed data:

# In[5]:


df_list =[]
for neon_site in neon_sites[0:2]:

    pkl_dir = '/Users/negins/Desktop/Simulations/tutorials/processed_data'
    pkl_name = neon_site+'_'+year+'df_all.pkl'
    processed_data = os.path.join(pkl_dir,pkl_name)

    df_all = pd.read_pickle(processed_data).reset_index()
    df_all['site']=neon_site
    df_list.append(df_all)
    
    
df_all_sites = pd.concat(df_list)
print (df_all_sites)

print (df_all_sites[df_all_sites['site']=='ABBY'])


# In[6]:


df_all = df_all_sites


# In[7]:


#-- extract year, month, day, hour information from time
df_all['year'] = df_all['time'].dt.year
df_all['month'] = df_all['time'].dt.month
df_all['day'] = df_all['time'].dt.day
df_all['hour'] = df_all['time'].dt.hour


# ## 3) Time-Series Visualization
# ### 3.1) Time-Series Dashboard with Scatterplots

# In[8]:


#time-series with Dropdown menu for values
from scipy import stats

import yaml
from bokeh.themes import Theme
from bokeh.models import ColumnDataSource, Slider , Dropdown, Select, PreText, Label, Slope
from bokeh.layouts import row,column
# make a simple plot time-series

from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from neon_bokeh_utils import simple_tseries

import os
os.environ['BOKEH_RESOURCES'] = 'inline'

from bokeh.resources import INLINE
import bokeh.io
from bokeh import *
bokeh.io.output_notebook(INLINE)

#time-series with Dropdown menu for values
from scipy import stats

import yaml
from bokeh.themes import Theme
from bokeh.models import ColumnDataSource, Slider , Dropdown, Select, PreText, Label, Slope
from bokeh.layouts import row,column
# make a simple plot time-series

from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
#from neon_bokeh_utils import simple_tseries

import os
os.environ['BOKEH_RESOURCES'] = 'inline'

from bokeh.resources import INLINE
import bokeh.io
from bokeh import *
bokeh.io.output_notebook(INLINE)


# In[9]:


freq_list = ['all','hourly','daily','monthly']


# In[13]:


def get_data (df, var, freq, site):
    df[df['site']==neon_site]
    #var_name = var
    sim_var_name = "sim_"+var
    #print (var)
    #print (sim_var_name)
    if freq=="monthly":
        df = df.groupby(['year','month']).mean().reset_index()
        df["day"]=15
        df['time']=pd.to_datetime(df[["year", "month","day"]])

    elif freq=="daily":
        df = df.groupby(['year','month','day']).mean().reset_index()
        df['time']=pd.to_datetime(df[["year", "month", "day"]])

    elif freq=="hourly" or freq=="all":
        df = df.groupby(['year','month','day','hour']).mean().reset_index()
        df['time']=pd.to_datetime(df[["year", "month", "day","hour"]])
    
    
    df_new = pd.DataFrame({'time':df['time'],'NEON':df[var],'CLM':df[sim_var_name]})
    #print(df_new)
    return df_new

def find_regline(df, var, sim_var_name):
        # find the trendline:
        #sim_var_name = "sim_"+var
        #print (var)
        #print (sim_var_name)

        df_temp = df[[var, sim_var_name]]#.dropna()
        
        #df_temp = pd.DataFrame(df, columns)
        df_temp.dropna(inplace=True)
        #print (df_temp)

        #z = np.polyfit(df_temp[var], df_temp[sim_var_name], 1)
        #p = np.poly1d(z)
        
        #-----
        slope, intercept, r_value, p_value, std_err = stats.linregress(df_temp[var], df_temp[sim_var_name])
        return slope, intercept, r_value, p_value, std_err
    
    
    
plot_vars =['FSH','EFLX_LH_TOT','Rnet','NEE','GPP']


# In[14]:


def simple_tseries(doc):
    
    df_new = get_data(df_all, 'EFLX_LH_TOT','hourly','ABBY')
    
    source = ColumnDataSource(df_new)

    #-- what are tools options
    tools = "hover, box_zoom, undo, crosshair"

    p = figure(tools=tools, x_axis_type="datetime", title= "Neon Time-Series "+neon_site)

    
    p.line('time', 'NEON', source=source, alpha=0.8, line_width=4, color="navy", legend_label="NEON")
    p.line('time', 'CLM',source=source , alpha=0.8, line_width=3, color="red", legend_label="CLM")
    #p.circle('time', 'var', source=source, alpha=0.8, color="navy")

    p.xaxis.major_label_text_color = 'dimgray'
    p.xaxis.major_label_text_font_size = '15px'
    p.yaxis.major_label_text_color = 'dimgray'
    p.yaxis.major_label_text_font_size = '15px'
    
    p.xaxis.axis_label_text_font_size = "15pt"
    p.axis.axis_label_text_font_style = "bold"
    p.grid.grid_line_alpha = 0.5
    p.title.text_font_size = '15pt'
    p.xaxis.axis_label = 'Time'


    
    def scatter_plot(q):
        q.circle('NEON', 'CLM', source=source, alpha=0.8, color="navy",fill_alpha=0.2, size=10)

        q.xaxis.major_label_text_color = 'dimgray'
        q.xaxis.major_label_text_font_size = '15px'
        q.yaxis.major_label_text_color = 'dimgray'
        q.yaxis.major_label_text_font_size = '15px'
    
        q.xaxis.axis_label_text_font_size = "13pt"
        q.yaxis.axis_label_text_font_size = "13pt"

        q.axis.axis_label_text_font_style = "bold"
        q.grid.grid_line_alpha = 0.5
        q.title.text_font_size = '15pt'
        q.xaxis.axis_label = 'NEON'
        q.yaxis.axis_label = 'CLM'

        
        #x = range(0,500)
        #y = range(0,500)

        #q.line(x, y,alpha=0.8, line_width=4, color="gray")
        
    
    q_width = 350
    q_height = 350
    q = figure(tools=tools,width=350, height=350)
    scatter_plot(q)
    
    p.add_tools(
        HoverTool(
            tooltips=[('value','@value{2.2f}'), 
                      ('index', '@index')]
        )
    )
    
    stats = PreText(text='', width=500)

    
    menu = Select(options=plot_vars,value='EFLX_LH_TOT', title='Variable') 
    
    def update_variable (attr, old, new):
        
        #print (menu.value)
        #print (menu_freq.value)
        df_new = get_data(df_all, menu.value, menu_freq.value, menu_site.value)

        #slope, intercept, r_value, p_value, std_err = find_regline(df_new, 'NEON','CLM')
        #print (r_value)
        #slope_label = "y="+"{:.2f}".format(slope)+"+"+"{:.2f}".format(intercept)+"x"+" (R2="+"{:.2f}".format(r_value)+")"
        #mytext = Label(text=slope_label , x=0+20, y=q_height-100, 
        #       x_units="screen", y_units='screen', text_align="left")
        
        #regression_line = Slope(gradient=slope, y_intercept=intercept, line_color="red")

        #print(slope_label)
        #q.add_layout(mytext)
        #q.add_layout(regression_line)
        
        
        source.data =df_new
        #source.stream(df_new)


    def update_site (attr, old, new):
        p.title.text = "Neon Time-Series " +menu_site.value

    menu.on_change('value', update_variable)


    menu_freq = Select(options=freq_list,value='all', title='Frequency') 

    menu_freq.on_change('value', update_variable)


    menu_site = Select(options=neon_sites,value='ABBY', title='Neon Site') 
    menu_site.on_change('value', update_site)

    
    #layout = row(column(menu, menu_freq, menu_site, q),  p)
    layout = row(p, column( menu, menu_freq, menu_site, q))
    doc.add_root(layout)
    
    doc.theme = Theme(json=yaml.load("""
        attrs:
            Figure:
                background_fill_color: "#FFFFFF"
                outline_line_color: white
                toolbar_location: above
                height: 550
                width: 1100
            Grid:
                grid_line_dash: [6, 4]
                grid_line_color: gray
    """, Loader=yaml.FullLoader))
    


# In[16]:


output_notebook()

show(simple_tseries, notebook_handle=True)


# ## 3.2) Time-Series DashBoard with Statistics
# 

# In[19]:


def stats_tseries(doc):
    
    df_new = get_data(df_all, 'EFLX_LH_TOT','hourly','ABBY')
    
    source = ColumnDataSource(df_new)

    #-- what are tools options
    tools = "hover, box_zoom, undo, crosshair"

    def timeseries_plot (p):
        p.line('time', 'NEON', source=source, alpha=0.8, line_width=4, color="navy", legend_label="NEON")
        p.line('time', 'CLM',source=source , alpha=0.8, line_width=3, color="red", legend_label="CLM")
        #p.circle('time', 'var', source=source, alpha=0.8, color="navy")

        p.xaxis.major_label_text_color = 'dimgray'
        p.xaxis.major_label_text_font_size = '15px'
        p.yaxis.major_label_text_color = 'dimgray'
        p.yaxis.major_label_text_font_size = '15px'
    
        p.xaxis.axis_label_text_font_size = "15pt"
        p.axis.axis_label_text_font_style = "bold"
        p.grid.grid_line_alpha = 0.5
        p.title.text_font_size = '15pt'
        p.xaxis.axis_label = 'Time'

    
    def scatter_plot(q):
        q.circle('NEON', 'CLM', source=source, alpha=0.8, color="navy",fill_alpha=0.2, size=10)
        print (df_new)
        q.xaxis.major_label_text_color = 'dimgray'
        q.xaxis.major_label_text_font_size = '15px'
        q.yaxis.major_label_text_color = 'dimgray'
        q.yaxis.major_label_text_font_size = '15px'
    
        q.xaxis.axis_label_text_font_size = "13pt"
        q.yaxis.axis_label_text_font_size = "13pt"

        q.axis.axis_label_text_font_style = "bold"
        q.grid.grid_line_alpha = 0.5
        q.title.text_font_size = '15pt'
        q.xaxis.axis_label = 'NEON'
        q.yaxis.axis_label = 'CLM'
        
        slope, intercept, r_value, p_value, std_err = find_regline(df_new, 'NEON','CLM')
        #print (r_value)
        slope_label = "y="+"{:.2f}".format(slope)+"+"+"{:.2f}".format(intercept)+"x"+" (R2="+"{:.2f}".format(r_value)+")"
        mytext = Label(text=slope_label , x=0+20, y=q_height-100, 
                        x_units="screen", y_units='screen', text_align="left")
        
        regression_line = Slope(gradient=slope, y_intercept=intercept, line_color="red")

        #q.add_layout(mytext)
        q.add_layout(regression_line)
        print ("slope_label:", slope_label)
        q.title.text = slope_label


        
        #x = range(0,500)
        #y = range(0,500)

        #q.line(x, y,alpha=0.8, line_width=4, color="gray")
        
    
    p = figure(tools=tools, x_axis_type="datetime", title= "Neon Time-Series "+neon_site)
    timeseries_plot(p)
    
    q_width = 350
    q_height= 350
    q = figure(tools=tools,width=q_width, height=q_height)
    scatter_plot(q)
    
    p.add_tools(
        HoverTool(
            tooltips=[('value','@value{2.2f}'), 
                      ('index', '@index')]))
    

    
    def update_variable (attr, old, new):
        
        #print (menu.value)
        #print (menu_freq.value)
        df_new = get_data(df_all, menu.value, menu_freq.value, menu_site.value)
        
        #print ("=======================================")
        #print ("Statistics summary for var: "+menu.value)
        #print (df_new.describe())
        #print ("----------------")
        #print(slope_label)
        #print ("R2      = "+"{:.2f}".format(r_value))
        #print ("p-value = "+"{:.2f}".format(p_value))
        #print ("std-err = "+"{:.1f}".format(p_value))
        #print ("=======================================")

        
        #source.data =df_new
        source.data.update(df_new)


        #scatter_plot(q)
        #source.stream(df_new)
        #slope, intercept, r_value, p_value, std_err = find_regline(df_new, 'NEON','CLM')
        #print (r_value)
        #slope_label = "y="+"{:.2f}".format(slope)+"+"+"{:.2f}".format(intercept)+"x"+" (R2="+"{:.2f}".format(r_value)+")"
        #mytext = Label(text=slope_label , x=0+20, y=q_height-100, 
        #                x_units="screen", y_units='screen', text_align="left")
        
        #regression_line = Slope(gradient=slope, y_intercept=intercept, line_color="red")

        #q.add_layout(mytext)
        #print (q)
        #q.title.text = slope_label
        #q.add_layout(regression_line)
        #print ("slope_label:", slope_label)
        
        
        slope, intercept, r_value, p_value, std_err = find_regline(df_new, 'NEON','CLM')
        #print (r_value)
        slope_label = "y="+"{:.2f}".format(slope)+"+"+"{:.2f}".format(intercept)+"x"+" (R2="+"{:.2f}".format(r_value)+")"
        mytext = Label(text=slope_label , x=0+20, y=q_height-100, 
                        x_units="screen", y_units='screen', text_align="left")
        
        regression_line = Slope(gradient=slope, y_intercept=intercept, line_color="red")

        #q.add_layout(mytext)
        print ("slope_label:", slope_label)
        q.title.text = slope_label
        

    def update_site (attr, old, new):
        p.title.text = "Neon Time-Series " +menu_site.value

        
    menu = Select(options=plot_vars,value='EFLX_LH_TOT', title='Variable') 

    menu.on_change('value', update_variable)


    menu_freq = Select(options=freq_list,value='all', title='Frequency') 

    menu_freq.on_change('value', update_variable)


    menu_site = Select(options=neon_sites,value='HARV', title='Neon Site') 
    menu_site.on_change('value', update_site)

    
    #layout = row(column(menu, menu_freq, menu_site, q),  p)
    layout = row(p, column( menu, menu_freq, menu_site, q))
    doc.add_root(layout)
    
    doc.theme = Theme(json=yaml.load("""
        attrs:
            Figure:
                background_fill_color: "#FFFFFF"
                outline_line_color: white
                toolbar_location: above
                height: 550
                width: 1100
            Grid:
                grid_line_dash: [6, 4]
                grid_line_color: gray
    """, Loader=yaml.FullLoader))


# In[20]:


output_notebook()

show(stats_tseries)


# ## Congratulations! You have:
# * Created two time-seires dashboard for analyzing neon data.

# In[ ]:




