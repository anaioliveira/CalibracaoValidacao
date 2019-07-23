##################################################################
#
#     Developed by: Ana Isabel Oliveira
#     Project: Water4Ever
#     Date: MARETEC IST, 16/07/2018
#
##################################################################


#!/usr/bin/python
# -*- coding: utf-8 -*-

# Imports
import os
import sys

def read_file(input_file):

    fin = open(input_file)

    for lin in fin:
    
        try:
            aux_line = lin.split(':', 1)
            keyword = aux_line[0]
            if keyword[0] == '#':
                pass
            else:
                value = aux_line[1].replace('\n','')
                value = value.split(' ', 1)[-1]
                if '#' in value:
                    value = value.split('#')[0]

                if "BEGIN_DATE" in keyword:
                    global begin_date
                    begin_date = value
                    
                elif "END_DATE" in keyword:
                    global end_date
                    end_date = value
                    
                elif "TIME_STEP" in keyword:
                    global time_step
                    time_step = int(value)
                    
                elif "OBSERVED_DATA" in keyword:
                    global observed_data
                    observed_data = value.lower()
                    
                elif "MODELLED_DATA" in keyword:
                    global modelled_data
                    modelled_data = value.lower()
                    
                elif "FOLDER_NAME_DATE_TYPE" in keyword:
                    global date_type
                    date_type = value.lower()
                    
                elif "STATIONS_LIST" in keyword:
                    global stations_list
                    stations_list = value.lower()
                    
                elif "TIMESERIES_SUFFIX" in keyword:
                    global timeseries_suffix
                    timeseries_suffix = value.lower()
                    
                elif "OBSERVED_COLUMN" in keyword:
                    global observed_column
                    observed_column = int(value)
                    
                elif "MODELLED_COLUMN" in keyword:
                    global modelled_column
                    modelled_column = int(value)
                    
                elif "GRAPHS_FOLDER" in keyword:
                    global graphs_folder
                    graphs_folder = value.lower()
                
                else:
                    pass
        except:
            pass

    fin.close()
    
    return

def check_variables():

    if not 'begin_date' in globals():
        print ('\n   ERROR:      Please define keyword BEGIN_DATE. \n')
        sys.exit()
        
    if not 'end_date' in globals():
        print ('\n   ERROR:      Please define keyword END_DATE. \n')
        sys.exit()
        
    if not 'time_step' in globals():
        print ('\n   ERROR:      Please define keyword TIME_STEP. \n')
        sys.exit()
        
    if not 'observed_data' in globals():
        print ('\n   ERROR:      Please define keyword OBSERVED_DATA. \n')
        sys.exit()
        
    if not 'modelled_data' in globals():
        print ('\n   ERROR:      Please define keyword MODELLED_DATA. \n')
        sys.exit()
        
    if not 'date_type' in globals():
        print ('\n   ERROR:      Please define keyword FOLDER_NAME_DATE_TYPE. \n')
        sys.exit()
        
    if not 'stations_list' in globals():
        print ('\n   ERROR:      Please define keyword STATIONS_LIST. \n')
        sys.exit()
        
    if not 'timeseries_suffix' in globals():
        print ('\n   ERROR:      Please define keyword TIMESERIES_SUFFIX. \n')
        sys.exit()
        
    if not 'observed_column' in globals():
        print ('\n   ERROR:      Please define keyword OBSERVED_COLUMN. \n')
        sys.exit()
        
    if not 'modelled_column' in globals():
        print ('\n   ERROR:      Please define keyword MODELLED_COLUMN. \n')
        sys.exit()
        
    if not 'graphs_folder' in globals():
        print ('\n   ERROR:      Please define keyword GRAPHS_FOLDER. \n')
        sys.exit()
        
    else:
        pass

    return
    
def init():

    print ('\n   WARNING: Be carefull!!! Do not use spaces and special characters in the names and directories!!!\n')
    
    input_file = 'input.dat'
    
    # Define_global_variables()
    read_file(input_file)
    check_variables()