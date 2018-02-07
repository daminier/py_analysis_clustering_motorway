import pandas as pd
import csv
import random
import sys
import string
from datetime import datetime 
import numpy as np
import matplotlib.pyplot as plt

# * Documentation: look at README.md for any further information

seed=54647
size = 1 

def read_file(file_name,reduction_factor=1,csv_flag=False) :
    #this function read a file using pandas. You can use reduction_factor (default=1) if you you want to reduce the number of lines 
    #(size=lines/reduction_factor). You can use csv_flag=True if you want to read a well structured csv file.
    global seed
    global size
    num_lines = sum(1 for l in open(file_name)) 
    size = int(num_lines /reduction_factor)
    print "["+file_name+"]" + " size: "+str(size)
    if reduction_factor!=1: 
        random.seed(seed)
        skip_idx = random.sample(range(1, num_lines), num_lines - size)
        file= pd.read_csv(file_name,skiprows=skip_idx, sep=';',index_col=None, usecols=[0,1])
    else :
        if csv_flag :
            file= pd.read_csv(file_name, sep=',',index_col=None)
        else:
            file= pd.read_csv(file_name, sep=';',index_col=None, usecols=[0,1])
    return file

def clean(lista):
    #a cleaning function, which allows you to get a well structured path (1-2-4-)
    result= ""
    for x in lista : 
        result = str(x) +"-"+result 
    return result   

def progress(count, total, status=''):
    #this function allows you to see status and progress of the program that is running
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()
    
def initialize(file_name,file): 
    #given a file .csv already opened, this function initialize a new well structured file (targa,tratta,volte).
    start_time = datetime.now()
    global size
    
    try:
        output = open(file_name, "w")
        previuos_plate = ""
        counter=0
        rows=0 
        output.write("targa,tratta,volte\n")
        for plate in file['targa'] :
            progress(counter,size)        
            if previuos_plate != plate :
                output.write(str(plate)+","+str(clean(file.loc[file['targa']==plate,'varco'].values))+","+str(1)+"\n")
                rows+=1
            previuos_plate = plate 
            counter+=1
            
   
    finally:
        output.close()
        print "\n ["+file_name+"] size: "+ str(rows)+"\n"
        time_elapsed = datetime.now() - start_time 
        print(' Time elapsed (hh:mm:ss.ms) {}\n'.format(time_elapsed))

def initialize_unique(file_name,file): 
    #given a file .csv already opened, this function initialize a new well structured file (targa,tratta,volte).
    #it's optimized compared to the initialize function. 
    start_time = datetime.now()
    try:
        output = open(file_name, "w")
        #counter=0
        output.write("targa,tratta,volte\n")
        unique_plates = file['targa'].unique()
        size = len(unique_plates)
        for plate in unique_plates:
            #progress(counter,size)        
            output.write(str(plate)+","+str(clean(file.loc[file['targa']==plate,'varco'].values))+","+str(1)+"\n")
            #counter+=1
   
    finally:
        output.close()
        print "["+file_name+"] size: "+ str(size)
        time_elapsed = datetime.now() - start_time 
        print(' Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))
       
def update(ifile_name,file_df) :
    start_time = datetime.now()
    try:
        init_file= pd.read_csv(ifile_name, sep=',',index_col=None)
        ifile = init_file.values
        print('['+str(ifile_name)+'] size: '+str(len(ifile)))
        file=file_df.values
        #size= len(file) 
        #counter = 0
        matches=0
        for record in file :
            # progress(counter,size)
            # counter+=1  
            paths =ifile[np.where(ifile[:,0] == record[0]),1]
            if len(paths[0]) != 0 : 
                count_path=0
                for path in paths[0] : 
                    if record[1] == path :                       
                        matches+=1
                        ifile[np.where((ifile[:,0] == record[0])&(ifile[:,1] == record[1])),2] =  ifile[np.where((ifile[:,0] == record[0])&(ifile[:,1] == record[1])),2]  +  1                              
                    else:  
                        count_path+=1 
                        if count_path==len(paths[0]) :                            
                            ifile = np.append(ifile,[record],axis=0)                                                                   
            else :
                ifile = np.append(ifile,[record],axis=0)            
    finally :
        pd.DataFrame(ifile,columns=['targa','tratta','volte']).to_csv(ifile_name,index=False)       
        print(' number of matches:'+str(matches))
        time_elapsed = datetime.now() - start_time 
        print('Time elapsed (hh:mm:ss.ms) {}\n'.format(time_elapsed))          
           
def sort(file_name,sort_by,kind="mergesort") : 
     print("\nsorting file "+file_name+"...")
     file = read_file(file_name,1,True)
     result = file.sort_values(sort_by,kind=kind)
     result.to_csv(file_name,index=False)

def get_patterns(file_name,times=1,show_plates=False,plates_threshold=0) :
    pattern_map = {} 
    try :
        df= pd.read_csv(file_name, sep=',',index_col=None)
        df= df.loc[df['volte']>=times]
        print "\nSelected subset (times >= "+str(times)+"):" 
        for tratta in df['tratta'].unique():
            if  len(tratta.split('-')) <= plates_threshold :    
                continue
            plates = df.loc[df['tratta']==tratta,'targa'].values
            if show_plates : 
                pattern_map[tratta] = list(plates)
            else :
                pattern_map[tratta] = len(plates)
        return pattern_map

    finally:
        print "path\tplates"
        for k,v in pattern_map.items():
            print k,"\t",v

def plot(file_name,times=1,plates_threshold=0):
    myDictionary= get_patterns(file_name,times,False,plates_threshold)
    plt.bar(myDictionary.keys(), myDictionary.values(),color='b')
    plt.xticks(rotation='vertical')
    plt.ylabel("number of cars")
    plt.xlabel("path")
    plt.title("Number of cars, which have driven across a path more than or equal to "+str(times)+" times")
    plt.show()
