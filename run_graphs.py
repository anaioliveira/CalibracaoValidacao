##################################################################
#
#     Developed by: Ana Isabel Oliveira
#     Project: HazRunoff
#     Date: MARETEC IST, 27/07/2018
#
##################################################################


#!/usr/bin/python
# -*- coding: utf-8 -*-

# Imports
import os
import sys
import datetime
import dateutil
import shutil
import read_input_file
import pandas
import numpy
import math
# Matplotlib
import matplotlib.pyplot as plt
from matplotlib import pyplot as mp
import matplotlib.dates as mdates
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage, AnnotationBbox)

def manage_dates(date_original_string, py, mo):

    # Transform original date into python date
    if py == 1:
        python_date = datetime.datetime.strptime(date_original_string, '%Y %m %d %H %M %S')
    
    # Date string to write in MOHID files
    if mo == 1:
        mohid_date = datetime.date.strftime(python_date, '%Y %m %d %H %M %S')

    if py == 1 and mo == 1:
        return python_date, mohid_date
    elif py == 1 and mo == 0:
        return python_date
    elif py == 0 and mo == 1:
        return mohid_date
    else:
        print ('Attention!! You have an error in dates variables!!')

def check_folders(begin_python_date, end_python_date, date_type, modelled_data):
    
    # Dealing with dates
    begin_year = begin_python_date.year
    begin_month = begin_python_date.month
    begin_day = begin_python_date.day
    
    end_year = end_python_date.year
    end_month = end_python_date.month
    end_day = end_python_date.day

    date_string = ""
    for l in date_type:
        if "y" == l and not "%Y" in date_string:
            date_string = date_string + "%Y"
        elif "m" == l and not "%m" in date_string:
            date_string = date_string + "%m"
        elif "d" == l and not "%d" in date_string:
            date_string = date_string + "%d"
        elif l != "y" and l != "m" and l != "d":
            date_string = date_string + l
        else:
            pass

    begin_folder = datetime.datetime(begin_year, begin_month, begin_day).strftime(date_string)
    end_folder = datetime.datetime(end_year, end_month, end_day).strftime(date_string)
   
    # Dealing with folders
    folders_list = os.listdir(modelled_data)
    folders_list.sort()
    
    folders_to_check = []
    for folder in folders_list:
        if folder == begin_folder:
            folders_to_check.append(modelled_data + folder)
        elif folder == end_folder:
            folders_to_check.append(modelled_data + folder)
            break
        else:
            folders_to_check.append(modelled_data + folder)

    return folders_to_check
    
def get_modelled_stations_list(stations_list, timeseries_suffix, modelled_folder_data):

    if stations_list != "all":
        stations_list_ = stations_list.split()
    
    stations_in_folder = os.listdir(modelled_folder_data)
    
    stations_to_draw = []
    for sf in stations_in_folder:
        if timeseries_suffix in sf and stations_list == "all":
            stations_to_draw.append(sf)
        elif timeseries_suffix in sf:
            for sl in stations_list_:
             if sl in sf:
                stations_to_draw.append(sf)
        else:
            pass

    return stations_to_draw
    
def get_observed_stations_list(modelled_stations_to_draw, observed_data):

    stations_to_draw = []
    for s in modelled_stations_to_draw:
        for root, directories, filenames in os.walk(observed_data):
            for f in filenames:
                s_ = s.split("_")[1]
                s__ = s_.split(".")[0]
                if s__ in f:
                    stations_to_draw.append(root + '/' + f)
                    

    return stations_to_draw

def compute_values(station, observed_column, time_step, data_type):
    
    dates_list = []
    values_list = []
    
    # Get values from file
    if data_type == 'observed':
        fin = open(station, 'r')
        s_lines = fin.readlines()
        d_ = s_lines[0].split(',')[0]
        d = d_.replace('"','')
        v_ = s_lines[0].split(',')[observed_column-1]
        v__ = v_.replace('"','')
        v = v__.replace('\n','')
        fin.close()
    
        # Load data from csv file
        data = pandas.read_csv(station)

        if time_step == 1:
            aux = data.to_numpy()
            for i in range(len(aux)):
                dates_list.append(aux[i][0])
                values_list.append(aux[i][1])
        
        elif time_step == 2:
            # Convert date from string to date times
            data[d] = pandas.to_datetime(data[d])
            
            # Get year and month of each day
            data['year'] = data[d].dt.year
            data['month'] = data[d].dt.month

            monthly_means = data.groupby(['year', 'month'])[v].mean()
            aux = monthly_means.to_numpy()
            
            months = monthly_means.reset_index()['month']
            years = monthly_means.reset_index()['year']

            # Construct dates and values lists
            for i in range(len(aux)):
                year = str(years[i])
                month = str(months[i])
                day = '01'
                dates_list.append(year + '-' + month.zfill(2) + '-' + day)
                values_list.append(aux[i])
    
    elif data_type == 'modelled':

        fin = open(station, 'r')
        s_lines = fin.readlines()
        headers = s_lines[7].split()
        fin.close()

        v = headers[observed_column-1]

        colspecs_=[[4,14], [15,19], [21,23], [25,27], [29,31], [33,35], [37,44],
                  [70,89], [114,133], [158,177], [202,221], [246,265], [290,309],
                  [334,353], [378,397], [422,441], [466,485], [510,529], [554,573]]
        
        data = pandas.read_fwf(station,colspecs=colspecs_,header=None,names=headers,skiprows=9,skipfooter=7,engine='python')

        if time_step == 1:
            daily_means = data.groupby(['YY', 'MM', 'DD'])[v].mean()
            aux_daily_means = daily_means.to_numpy()
            
            days = daily_means.reset_index()['DD']
            months = daily_means.reset_index()['MM']
            years = daily_means.reset_index()['YY']

            for i in range(len(aux_daily_means)):
                year = str(years[i])
                month = str(months[i])
                day = str(days[i])
                dates_list.append(year + '-' + month.zfill(2) + '-' + day.zfill(2))
                values_list.append(aux_daily_means[i])
        
        elif time_step == 2:
            # Convert date from string to date times
            monthly_means = data.groupby(['YY', 'MM'])[v].mean()
            aux = monthly_means.to_numpy()
            
            months = monthly_means.reset_index()['MM']
            years = monthly_means.reset_index()['YY']
            
            for i in range(len(aux)):
                year = str(years[i])
                month = str(months[i])
                day = '01'
                dates_list.append(year + '-' + month.zfill(2) + '-' + day)
                values_list.append(aux[i])

    return dates_list, values_list

def compute_r2(modelled_dates, modelled_values, observed_dates, observed_values):

    dates = []
    obs_values = []
    mod_values = []
    for i1 in range(len(modelled_dates)):
        try:
            i2 = observed_dates.index(modelled_dates[i1])
            if not (math.isnan(observed_values[i2])):
                dates.append(modelled_dates[i1])
                obs_values.append(observed_values[i2])
                mod_values.append(modelled_values[i1])
            else:
                pass
        except:
            pass

    if dates != []:
        obs_mean = numpy.mean(obs_values)
        mod_mean = numpy.mean(mod_values)
        
        n1 = 0  
        d1 = 0  
        d2 = 0        
        for j in range(len(obs_values)):
            n1 = n1 + ((obs_values[j]-obs_mean)*(mod_values[j]-mod_mean))
            d1 = d1 + ((obs_values[j]-obs_mean)**2)
            d2 = d2 + ((mod_values[j]-mod_mean)**2)
            
        r2 = (n1/((d1**(0.5))*(d2**(0.5))))**2
        
        return r2
        
    else:
        print "This station hasn't observed values to the analyzed period!"
        r2 = 0
        return r2

def compute_rmse(modelled_dates, modelled_values, observed_dates, observed_values):

    dates = []
    obs_values = []
    mod_values = []
    for i1 in range(len(modelled_dates)):
        try:
            i2 = observed_dates.index(modelled_dates[i1])
            if not (math.isnan(observed_values[i2])):
                dates.append(modelled_dates[i1])
                obs_values.append(observed_values[i2])
                mod_values.append(modelled_values[i1])
            else:
                pass
        except:
            pass
    
    if dates != []:
        n1 = 0
        d1 = 0
        for j in range(len(obs_values)):
            n1 = n1 + (obs_values[j]-mod_values[j])**2
            d1 = d1 + 1

        rmse = (n1/d1)**(0.5)
        
        return rmse
        
    else:
        print "This station hasn't observed values to the analyzed period!"
        rmse = 0
        return rmse  
        
def compute_pbias(modelled_dates, modelled_values, observed_dates, observed_values):

    dates = []
    obs_values = []
    mod_values = []
    for i1 in range(len(modelled_dates)):
        try:
            i2 = observed_dates.index(modelled_dates[i1])
            if not (math.isnan(observed_values[i2])):
                dates.append(modelled_dates[i1])
                obs_values.append(observed_values[i2])
                mod_values.append(modelled_values[i1])
            else:
                pass
        except:
            pass
    
    if dates != []:
        n1 = 0
        d1 = 0
        for j in range(len(obs_values)):
            n1 = n1 + (obs_values[j]-mod_values[j])*100
            d1 = d1 + obs_values[j]

        pbias = n1/d1
        
        return pbias
        
    else:
        print "This station hasn't observed values to the analyzed period!"
        pbias = 0
        return pbias  
        
def compute_nse(modelled_dates, modelled_values, observed_dates, observed_values):

    dates = []
    obs_values = []
    mod_values = []
    for i1 in range(len(modelled_dates)):
        try:
            i2 = observed_dates.index(modelled_dates[i1])
            if not (math.isnan(observed_values[i2])):
                dates.append(modelled_dates[i1])
                obs_values.append(observed_values[i2])
                mod_values.append(modelled_values[i1])
            else:
                pass
        except:
            pass
    
    if dates != []:
        obs_mean = numpy.mean(obs_values)
        
        n1 = 0
        d1 = 0
        for j in range(len(obs_values)):
            n1 = n1 + (obs_values[j]-mod_values[j])**2
            d1 = d1 + (obs_values[j]-obs_mean)**2

        nse = 1 - n1/d1
        
        return nse
        
    else:
        print "This station hasn't observed values to the analyzed period!"
        nse = 0
        return nse  
    
def draw_graph_values_vs_time(modelled_dates, modelled_values, observed_dates, observed_values, name, p1, p2, p3):

    dates = []
    obs_values = []
    mod_values = []
    for i1 in range(len(modelled_dates)):
        if modelled_dates[i1] in observed_dates:
            i2 = observed_dates.index(modelled_dates[i1])
            if not (math.isnan(observed_values[i2])):
                dates.append(datetime.datetime.strptime(modelled_dates[i1], '%Y-%m-%d'))
                obs_values.append(observed_values[i2])
                mod_values.append(modelled_values[i1])
            else:
                pass
        else:
            obs_values.append(numpy.nan)
            mod_values.append(modelled_values[i1])
            dates.append(datetime.datetime.strptime(modelled_dates[i1], '%Y-%m-%d'))

    fig, axs = plt.subplots(figsize=(12, 6))
    # Plot observed values
    obs_serie = axs.plot(dates, obs_values, 'black')
    # Plot modelled values
    mod_serie = axs.plot(dates, mod_values, 'red')
    # Set axis tittles
    axs.set_xlabel('Date')
    axs.set_ylabel(r'Flow [$m^{3}$/s]')
    
    ## XAxis
    yearsFmt = mdates.DateFormatter('%Y-%m-%d')

    axs.xaxis.set_major_formatter(yearsFmt)

    # Set max and min of x axis
    axs.set_xlim(numpy.min(dates), numpy.max(dates))

    axs.format_xdata = mdates.DateFormatter('%Y-%m-%d')

    # Rotate x labels
    plt.xticks(rotation=45)

    # Activate axis grid
    axs.grid(True)
    
    # Legend
    fig.legend(['Observed','Modelled'],loc='upper left', bbox_to_anchor=(0.070, 0.95))
    
    # Box with statistic parameters
    textstr = 'RMSE = %.2f' % (p1, ) + '\nPBIAS = %.2f' % (p2, ) + '\nNSE = %.2f' % (p3, )
    
    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)

    # place a text box in upper left in axes coords
    axs.text(0.85, 0.95, textstr, transform=axs.transAxes, fontsize=13, verticalalignment='top', bbox=props)

    fig.tight_layout()
    mp.savefig(name+'.png')
        
    return
    
def draw_graph_obs_vs_mod(modelled_dates, modelled_values, observed_dates, observed_values, name, p1):

    obs_values = []
    mod_values = []
    for i1 in range(len(modelled_dates)):
        try:
            i2 = observed_dates.index(modelled_dates[i1])
            if not (math.isnan(observed_values[i2])):
                obs_values.append(observed_values[i2])
                mod_values.append(modelled_values[i1])
            else:
                pass
        except:
            pass

    if obs_values != []:
        fig, axs = plt.subplots()
        axs.scatter(obs_values, mod_values,c='black')
        axs.set_xlim(numpy.min(obs_values), numpy.max(obs_values))
        axs.set_xlabel(r'Observed flow [$m^{3}$/s]')
        axs.set_ylabel(r'Modelled flow [$m^{3}$/s]')
        axs.grid(True)
        
        # Box with statistic parameters
        textstr = r'$R^{2}$ = %.2f' % (p1, )
        
        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='white', alpha=0.5)

        # place a text box in upper left in axes coords
        axs.text(0.80, 0.95, textstr, transform=axs.transAxes, fontsize=13, verticalalignment='top', bbox=props)
        
        fig.tight_layout()
        mp.savefig(name+'_r2.png')
    else:
        print 'Impossible to graph R2 for this station. Observed values do not exist.'

    return
    
    
if __name__ == '__main__':

    read_input_file.init()
    
    ####### Get keywords values #######
    # Manage dates
    begin_date = read_input_file.begin_date
    begin_python_date = manage_dates(begin_date, 1, 0)
    time_step = read_input_file.time_step
    
    end_date = read_input_file.end_date
    end_python_date = manage_dates(end_date, 1, 0)
    
    observed_data = read_input_file.observed_data
    observed_column = read_input_file.observed_column
    modelled_data = read_input_file.modelled_data
    modelled_column = read_input_file.modelled_column
    date_type = read_input_file.date_type
    
    stations_list = read_input_file.stations_list
    timeseries_suffix = read_input_file.timeseries_suffix
    
    graphs_folder = read_input_file.graphs_folder
    
    # Get folders path to the right files and folders dates
    modelled_folders_data = check_folders(begin_python_date, end_python_date, date_type, modelled_data)
    modelled_stations_to_draw = get_modelled_stations_list(stations_list, timeseries_suffix, modelled_folders_data[0])
    observed_stations_to_draw = get_observed_stations_list(modelled_stations_to_draw, observed_data)
    
    for station in modelled_stations_to_draw:
        print 'Working on station ' + station + '.'
    
        # Get values
        modelled_dates = []
        modelled_values = []
        for f in modelled_folders_data:
            file = f + '/' + station
            modelled_dates_, modelled_values_ = compute_values(file, modelled_column, time_step, 'modelled')
        
            modelled_dates = modelled_dates + modelled_dates_
            modelled_values = modelled_values + modelled_values_
        
        name_ = station.split('_')[1]
        name = name_.replace('.' + timeseries_suffix, '')
        
        station = ''
        for s in observed_stations_to_draw:
            if name in s:
                station = s
                
        if station != '':
            observed_dates, observed_values = compute_values(station, observed_column, time_step, 'observed')

            # Compute R2, RMSE, PBIAS and NSE
            r2 = compute_r2(modelled_dates, modelled_values, observed_dates, observed_values)
            rmse = compute_rmse(modelled_dates, modelled_values, observed_dates, observed_values)
            pbias = compute_pbias(modelled_dates, modelled_values, observed_dates, observed_values)
            nse = compute_nse(modelled_dates, modelled_values, observed_dates, observed_values)
            
            # Draw graph values vs time_step
            draw_graph_values_vs_time(modelled_dates, modelled_values, observed_dates, observed_values, graphs_folder+name, rmse, pbias, nse)
            
            # Draw graph observed vs modelled
            draw_graph_obs_vs_mod(modelled_dates, modelled_values, observed_dates, observed_values, graphs_folder+name, r2)
        else:
            print 'Station ' + station + 'has not a match.'
            pass
