import pandas as pd
import csv
import random
import sys
import string
from datetime import datetime 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# * Documentation: look at README.md for any further information

seed=54647
size = 1 

def read_file(file_name,reduction_factor=1,csv_flag=False) :
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
    result= ""
    for x in lista : 
        result = str(x) +"-"+result 
    return result   

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()
    
def initialize(file_name,file): 
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
                        times=ifile[np.where((ifile[:,0] == record[0])&(ifile[:,1] == record[1])),2] 
                        ifile[np.where((ifile[:,0] == record[0])&(ifile[:,1] == record[1])),2] = times  +  1                              
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
    
def clustering(file_name,times_thr, path_thr,n_clusters) : 
    """
    This function return a dictionary, which contains a cluster (as a key) and 
    the associated plates (as values of that key) 
    
     - **parameters**, **types**, **return** and **return types**::

          :param file_name: file name
          :param times_thr: threshold of times, it is going to select greater values
          :param path_thr: threshold of the lenght of the paths, it is going to select greater values
          :param n_cluster: number of clusters for Kmeans algorithm
          :type file_name: string
          :type times_thr: int
          :type path_thr: int 
          :type n_cluster: int
          :return: return a dictionary, which contains a cluster (as a key) and the associated plates (as values of that key) 
          :rtype: dictionary (int, [int,..])
    
    """
    
    csv= pd.read_csv(file_name, sep=',',index_col=None)
    csv = csv.loc[csv['volte']>=times_thr]
    sorted_csv = csv.sort_values('targa')
    csv_np  = sorted_csv.values
    plates = sorted_csv['targa'].unique()
    lista = list()
    total_paths = np.array([])

    for count,plate in enumerate(plates) :      
        paths =csv_np[np.where(csv_np[:,0] == plate),1][0]
        volte =csv_np[np.where(csv_np[:,0] == plate),2][0]     
        lista.insert(count, [plate])
        i=0
        while i < len(paths) :
            if  len(paths[i].split('-')) <= path_thr : 
                i+=1   
                continue       
            lista[count].append(paths[i])
            total_paths= np.append(total_paths,paths[i])
            lista[count].append(volte[i])
            i+=1
    total_paths = np.unique(total_paths)
    data = np.zeros(shape=(len(lista),len(total_paths)), dtype = np.int8)
    plates = np.array([],dtype=int)
    for i,e in enumerate(lista) :
        plates = np.append(plates,e[0])
    print "selected plates: "+str(plates)+"\nselected paths: " + str(total_paths)+"\nmatrix shape: " + str(data.shape) 
    for count,element in enumerate(lista) :
        i=1
        while i <  len(element) :
            index = total_paths.tolist().index(element[i])
            data[count,index] = element[i+1]
            i+=2
    print data 
    kmeans = KMeans(n_clusters=n_clusters).fit(data)
    clusters_map = {}
    for cluster in kmeans.labels_ :
        clusters_map[cluster] = []

    for i,plate in enumerate(lista) :
        clusters_map[kmeans.labels_[i]].append(plate[0])

    print "\ncluster\tplates"
    for k,v in clusters_map.items():
             print k,"\t",v    
    
    
    
    
    
