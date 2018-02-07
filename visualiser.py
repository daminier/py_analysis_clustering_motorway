import trap17
import sys



def main(file_name,times_filter,path_lenght) :
    
    trap17.get_patterns(file_name,int(times_filter),True,int(path_lenght))
    trap17.plot(file_name,int(times_filter),int(path_lenght))

if __name__== "__main__" :
    if len(sys.argv)==4 :
        main(sys.argv[1],sys.argv[2],sys.argv[3])
    else :
        print("usage: "+sys.argv[0]+" [file name] [threshold] [path lenght]")