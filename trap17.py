import pandas as pd
import csv
import random
import sys
import string
from datetime import datetime 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.cm as cm


# * Documentation: look at README.md for any further information

seed=54647
size = 1 

def read_file(file_name,reduction_factor=1,csv_flag=False) :
    """
    This function can reduce the number of plates considered, but it does not lose any information and
    it helps you to read both csv files (targa;varco;corsia;timestamp;nazione or targa,tratta,volte).
    You need to set the parameter csv_flag=True if you want to read a csv file structured as “ targa,tratta,volte ”. 
    Therefore you can set the reduction factor parameter in order to reduce the file size. It is set a seed for being able to 
    reproduce the sample. The reduction factor must be an int. 
    The desired number of plates it is calculated as size= total_plates / reduction_factor.
    
     - **parameters**, **types**, **return** and **return types**::
          :param file_name: file name
          :param reduction_factor: the number of total plates it will divided by this number  
          :param csv_flag: if True you are reading a csv file with seperator = ','
          :type file_name: string
          :type reduction_factor: int
          :type csv_flag: Boolean 
          :return: return the file readed 
          :rtype: Pandas.DataFrame 
    """
    global seed
    if csv_flag :
            file= pd.read_csv(file_name, sep=',',index_col=None)
    else:
        file= sample_file(pd.read_csv(file_name, sep=';',index_col=None, usecols=[0,1]),reduction_factor)
    return file

def sample_file(file,reduction_factor=1) :
    global seed
    global size 
    unique_plates = file['targa'].unique()
    print "found plates :" + str(len(unique_plates))
    size = int(len(unique_plates)/reduction_factor)
    random.seed(seed)
    selected_plates= random.sample(unique_plates, size)
    print "selected plates : "+ str(len(selected_plates))
    temp = pd.DataFrame([],columns=['targa','varco'])
    for plate in selected_plates :
        temp= temp.append(file.loc[file['targa']==plate], ignore_index=True)
    return temp   

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

'''    
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
'''

def initialize_unique(file_name,file):
    
    """
     which allows you to initialize a csv file structured in this way: “targa,tratta,volte” (file_name is the file name to initialize). 
     Given a csv file from the dataset, this function generates the path according to the definition,
     which is explained in Preprocessing section.
    
     - **parameters**, **types**, **return** and **return types**::
          :param file_name: file name 
          :param file: it is a DataFrame 
          :type file_name: string
          :type file: Pandas.DataFrame        
          :return: None 
          :rtype: None   
    """
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
    
     """
      given a file, which has been already initialized, this function update an initialized file. Basically it refreshes the 
      column “volte” (times) of aninitialized file. When a new plate is found, the function adds a new record. When a plate
      (which compares in both file but with different path) is found, the function add a new record with the different path.   
    
    - **parameters**, **types**, **return** and **return types**::
          :param ifile_name: an initialized file name 
          :param file_df: a DataFrame 
          :type file_name: string
          :type file: Pandas.DataFrame        
          :return: None 
          :rtype: None  
    """ 
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
     """
    this function selects from the dataset the items which have times value greater than a certain threshold 
    (the parameter to set this threshold is “times”). By setting the parameter show_plates=True, 
    it shows a table of a selected path and the associated plates. It is possible to set the minimum number
    of gates in a path through the parameter "plates_threshold".   
    
    - **parameters**, **types**, **return** and **return types**::
          :param file_name: the inizialized file name 
          :param times: number of times 
          :param show_plates: show the associated plates
          :param plates_threshold : the minimum numbe of gates 
          :type file_name: string
          :type times:  int
          :type show_plates:  Boolean
          :type plates_threshold:  int
          :return: dictionary of path and the associated plates or the total number of plates
          :rtype: dictionary
    
    """
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
    
    """
      it plots an histogram about the number of cars which have driven across a path more than a certain threshold. 
      It uses the function “get_patterns”.      
    
    - **parameters**, **types**, **return** and **return types**::
          :param file_name: the initialized file name 
          :param times: number of times 
          :param plates_threshold : the minimum numbe of gates 
          :type file_name: string
          :type times:  int  
          :type plates_threshold:  int
          :return: None 
          :rtype: None
    """
    
    myDictionary= get_patterns(file_name,times,False,plates_threshold)
    plt.bar(myDictionary.keys(), myDictionary.values(),color='b')
    plt.xticks(rotation='vertical')
    plt.ylabel("number of cars")
    plt.xlabel("path")
    plt.title("Number of cars, which have driven across a path more than or equal to "+str(times)+" times\nand path length > "+ str(plates_threshold))

    
def clustering_2(df,n_clusters=2,times_thr=1) :
    
    start_time = datetime.now()
    if times_thr >1:
     df = df.loc[csv['volte']>=times_thr]

    dictionry_path = {}
    data = np.zeros(shape=(len(df['tratta'].values),2), dtype = np.int8)
    counter_path = 0

    for count,element in enumerate(df.values): 
        if element[1] in dictionry_path :
            data[count,0] = dictionry_path[element[1]]
            data[count,1] = element[2]
        else :
            counter_path+=1
            dictionry_path[element[1]]= counter_path
            data[count,0] = counter_path
            data[count,1] = element[2]

    print "size:"+ str(data.size)
    
    clusterer= KMeans(n_clusters=n_clusters, random_state=10)
    kmeans = clusterer.fit(data)
    cluster_labels = clusterer.fit_predict(data)
    silhouette_avg = silhouette_score(data, cluster_labels)
    print "\nFor n_clusters =", n_clusters,"The average silhouette_score is :", silhouette_avg
    time_elapsed = datetime.now() - start_time 
    print('Time elapsed (hh:mm:ss.ms) {}\n'.format(time_elapsed))                      
    sample_silhouette_values = silhouette_samples(data, cluster_labels)                  
    fig, (ax1,ax2) = plt.subplots(1, 2)
    fig.set_size_inches(18, 7)
    ax2.set_title("The visualization of the clustered data.")
    ax2.set_xlabel("Feature space for the 1st feature")
    ax2.set_ylabel("Feature space for the 2nd feature")
    colors = cm.spectral(cluster_labels.astype(float) / n_clusters)
    ax2.scatter(data[:, 0], data[:, 1], marker='.', s=30, lw=0, alpha=0.7,c=colors, edgecolor='k')
    centers = clusterer.cluster_centers_
    ax2.scatter(centers[:, 0], centers[:, 1], marker='o',c="white", alpha=1, s=200, edgecolor='k')
    for i, c in enumerate(centers):
        ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1, s=50, edgecolor='k')
    plt.suptitle(("KMeans clustering on sample data "
                  "with n_clusters = %d\nThe average silhouette_score is %0.6f" % (n_clusters,silhouette_avg)),
                 fontsize=14, fontweight='bold')
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
    plates = np.array([],dtype=int) 
    lista = [x for x in lista if len(x)>1]
    for x in lista :
        plates = np.append(plates,x[0]) 
        
    data = np.zeros(shape=(len(lista),len(total_paths)), dtype = np.int8)
    print "selected plates: "+str(plates)+"\nselected paths: " + str(total_paths)+"\nmatrix shape: " + str(data.shape) 
    for count,element in enumerate(lista) :
        i=1
        while i <  len(element) :
            index = total_paths.tolist().index(element[i])
            data[count,index] = element[i+1]
            i+=2
    print data 
    
    clusterer= KMeans(n_clusters=n_clusters, random_state=10)
    kmeans = clusterer.fit(data)
    cluster_labels = clusterer.fit_predict(data)
    silhouette_avg = silhouette_score(data, cluster_labels)
    print "For n_clusters =", n_clusters,"The average silhouette_score is :", silhouette_avg
    sample_silhouette_values = silhouette_samples(data, cluster_labels)
    clusters_map = {}
    for cluster in kmeans.labels_ :
        clusters_map[cluster] = []
    for i,plate in enumerate(lista) :
        clusters_map[kmeans.labels_[i]].append(plate[0])
    print "\ncluster\tplates"
    for k,v in clusters_map.items():
             print k,"\t",v
    fig, (ax1,ax2) = plt.subplots(1, 2)
    fig.set_size_inches(18, 7)
    ax2.set_title("The visualization of the clustered data.")
    ax2.set_xlabel("Feature space for the 1st feature")
    ax2.set_ylabel("Feature space for the 2nd feature")
    colors = cm.spectral(cluster_labels.astype(float) / n_clusters)
    ax2.scatter(data[:, 0], data[:, 1], marker='.', s=30, lw=0, alpha=0.7,c=colors, edgecolor='k')
    centers = clusterer.cluster_centers_
    ax2.scatter(centers[:, 0], centers[:, 1], marker='o',c="white", alpha=1, s=200, edgecolor='k')
    for i, c in enumerate(centers):
        ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1, s=50, edgecolor='k')
    plt.suptitle(("KMeans clustering on sample data "
                  "with n_clusters = %d\nThe average silhouette_score is %0.4f" % (n_clusters,silhouette_avg)),
                 fontsize=14, fontweight='bold')
    ax1.bar(clusters_map.keys(),[len(clusters_map[x]) for x in clusters_map.keys() ],color='r')
    ax1.set_ylabel("number of cars")
    ax1.set_xlabel("clusters")
    ax1.set_title("K-Means clustering")
    plt.show()
