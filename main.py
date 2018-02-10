import trap17
import os 
import sys
from datetime import datetime
import argparse

def parseArguments() :
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--update", help="update file.", type=bool, default=False)
    parser.add_argument("-f", "--file_name", help="file path, default is /init.csv ", type=str, default='init.csv')
    parser.add_argument("-s", "--sort_by", help="sort by column, must be tratta, targa or volte", type=str, default=None)
    parser.add_argument("-p", "--plot", help="plot patterns.", type=bool, default=False)
    parser.add_argument("-t", "--times_filter", help="minimum number of times to filter.", type=int, default=1)
    parser.add_argument("-pt", "--plates_threshold", help="minimum number of gates in a path.", type=int, default=1)
    parser.add_argument("-sp", "--show_plates", help="show plates.", type=bool, default=False)
    parser.add_argument("--version", action="version", version='%(prog)s - Version 1.0')
    args = parser.parse_args()
    return args

def main(file_name='init.csv',update=False,sort_by=None,plot=False,times_filter=1,show_plates=False,plates_threshold=0) :
    start_time = datetime.now() 
    
    if update :
        files= os.listdir(os.getcwd()+"/converted")
        for file in files :
            if file.endswith(".csv") :
                f = trap17.read_file("converted/"+str(file),1,True)
                trap17.update(file_name,f)            
    if sort_by=='targa' or sort_by=='tratta' or sort_by=='volte' :
        trap17.sort(file_name,sort_by)
    if show_plates :
        trap17.get_patterns(file_name,times_filter,True,plates_threshold)    
    if plot :
        trap17.plot(file_name,times_filter,plates_threshold)
    
    time_elapsed = datetime.now() - start_time 
    print('\nTotal time elapsed (hh:mm:ss.ms) {}\n'.format(time_elapsed)) 


if __name__== "__main__" :
    args = parseArguments() 
    main(args.file_name,args.update,args.sort_by,args.plot,args.times_filter,args.show_plates,args.plates_threshold)
