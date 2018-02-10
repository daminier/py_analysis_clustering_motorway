import os
import sys
import trap17
from datetime import datetime

def main(reduction_factor) :
    start_time = datetime.now()  
    print("\ninitializing files...\n")
    files= os.listdir(os.getcwd()+"/dataset")
    files_csv = []
    for file in files :
        if file.endswith(".csv"):
           files_csv.append(str(file))
    
    init = trap17.read_file("dataset/"+str(files_csv[0]),int(reduction_factor))
    trap17.initialize_unique('init.csv',init)
    count=0
    for file in files_csv[1:] :
        count+=1
        print('------------------'+str(count)+'/'+str(len(files_csv)-1)+'-----------------------')
        f = trap17.read_file("dataset/"+str(file),int(reduction_factor))
        trap17.initialize_unique("converted/"+str(file),f)

    time_elapsed = datetime.now() - start_time 
    print('\nTotal time elapsed (hh:mm:ss.ms) {}\n'.format(time_elapsed)) 
    

if __name__== "__main__" :
    if len(sys.argv)==2 :
        main(sys.argv[1])
    else :
        print "usage: "+sys.argv[0]+" [int] \nhelp: [int] is the reduction factor you want to set."
