import pandas as pd
import csv
import random
import sys
import string
from datetime import datetime 
import numpy as np
import matplotlib.pyplot as plt

# Resources
# ---------
# * Documentation: look at README.txt for any further information

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
       
        
def update(init_file_name,file) :
    #given two files, which have been already initialized, this function update the init_file:
    #-adding new plates
    #-adding same plates with different path
    #-refreshing the field "volte" (times) if there is a match (same plate,same path)  
    start_time = datetime.now()
    try:
        init_file= pd.read_csv(init_file_name, sep=',',index_col=None)
        size= len(file['targa']) 
        counter = 0
        count_path=0
        matches=0

        for plate in file['targa'] :
            progress(counter,size)
            counter+=1
            plates = init_file.loc[init_file['targa']==plate]
            if  not plates.empty :               
                paths = init_file.loc[init_file['targa']==plate,'tratta'].values 
                count_paths=0 
                for path in paths :                     
                    if (file.loc[file['targa']==plate,'tratta'].values)[0] == path :
                        matches+=1                       
                        times = init_file.loc[init_file['targa']==plate,'volte'].values
                        times[0]+=1 
                        init_file.loc[init_file['targa']==plate,'volte'] = times[0]
                        init_file.to_csv(init_file_name,index=False)
                    else:
                        count_paths+=1 
                        if count_paths==len(paths) :                        
                            fr = open(init_file_name, "a")
                            path = file.loc[file['targa']==plate,'tratta'].values
                            fr.write(str(plate)+","+str(path[0])+","+str(1)+"\n")  
                            fr.close()               
            else :
                fr = open(init_file_name, "a") 
                path = file.loc[file['targa']==plate,'tratta'].values
                fr.write(str(plate)+","+str(path[0])+","+str(1)+"\n")
                fr.close()
    finally :
        print('\n number of matches:'+str(matches))
        time_elapsed = datetime.now() - start_time 
        print('Time elapsed (hh:mm:ss.ms) {}\n'.format(time_elapsed))                      

def sort(file_name,sort_by,kind="mergesort") : 
     print("\nsorting file "+file_name+"...")
     file = read_file(file_name,1,True)
     result = file.sort_values(sort_by,kind=kind)
     result.to_csv(file_name,index=False)

def get_patterns(file_name,times=1,show_plates=False) :
    pattern_map = {}
    try :
        df= pd.read_csv(file_name, sep=',',index_col=None)
        df= df.loc[df['volte']>times]
        print "\nSelected subset (times > "+str(times)+"):" 
        for tratta in df['tratta'].unique():
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


def plot(file_name,times=1):
    myDictionary= get_patterns(file_name,times)
    plt.bar(myDictionary.keys(), myDictionary.values(),color='b')
    plt.ylabel("number of cars")
    plt.xlabel("path")
    plt.title("Number of cars, which have driven across a path more than "+str(times)+" times")
    plt.show()



# get_patterns('init_Luglio_Giugno_25.csv',3,True)
# plot('init_Luglio_Giugno_25.csv',3)


# file = read_file('init_Luglio_Giugno_25.csv',1,True)
# df= file.loc[file['volte']>5]
# print df
# df.plot(kind='bar')
# plt.show()

# print("\ninitializing file init\n")
#file = read_file('03.07.2016.csv') #change here the path, reduction_factor=1 by default 
# initialize_unique('file_init.csv',file)

# print("\ninitializing file day 2\n")
# file = read_file('init_Luglio_Giugno_25.csv',1,True)
# file.loc[file['volte']>5,['tratta','volte']]
# plt.figure()
# file.plot.hist()

# initialize_unique('file_day_2.csv',file)

# print("\nupdating file init\n")
#file = read_file('init_Luglio_Giugno_25.csv',1,True)
#print file.loc[file['volte']>6,'tratta'].unique()

# update('file_init.csv',file)

# sort('init_Luglio_50.csv',['targa','tratta'])
# sort('init_Luglio_50_targa.csv','targa')
#sort('init_Luglio_Giugno_25.csv','tratta')

#get_patterns('init_Luglio_Giugno_25.csv',3)
# myDictionary= get_patterns('init_Luglio_Giugno_25.csv',5)
# plt.bar(myDictionary.keys(), myDictionary.values(),color='g')
# plt.show()



# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import matplotlib.path as path

# fig, ax = plt.subplots()

# # Fixing random state for reproducibility
# np.random.seed(19680801)


# # histogram our data with numpy

# data = np.random.randn(1000)
# n, bins = np.histogram(data, 50)

# file = read_file('init_Luglio_Giugno_25.csv',1,True)
# data= file.loc[file['volte']>5,['tratta']]
# n, bins = np.histogram(data, 50)
# # get the corners of the rectangles for the histogram
# left = np.array(bins[:-1])
# right = np.array(bins[1:])
# bottom = np.zeros(len(left))
# top = bottom + n


# # we need a (numrects x numsides x 2) numpy array for the path helper
# # function to build a compound path
# XY = np.array([[left, left, right, right], [bottom, top, top, bottom]]).T

# # get the Path object
# barpath = path.Path.make_compound_path_from_polys(XY)

# # make a patch out of it
# patch = patches.PathPatch(barpath)
# ax.add_patch(patch)

# # update the view limits
# ax.set_xlim(left[0], right[-1])
# ax.set_ylim(bottom.min(), top.max())

# plt.show()