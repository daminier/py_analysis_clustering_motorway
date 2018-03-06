# Project Work on Data Mining

Data preprocessing, data analysis and clustering.

  - [About](#about)
  - [Dataset](#dataset)
  - [Features](#features)
  	- [Sampling](#sampling)
	- [Preprocessing](#preprocessing)
	- [Data overview](#data-overview)
  - [Quick Start](#quick-start)
  - [Function details](#function-details)
  - [Clustering](#clustering)
  - [Experiments](#experiments)
  - [Considerations](#considerations)
  - [References](#references)

## About

This is a project work on Data Mining. The goal of this project is to find interesting patterns (such as the number of cars which have driven across the same path more than a certain number of times) in a large dataset. In order to do that we need to sample the data, to transform the data in useful structures. Moreover, minining the meaningful information and finally clustering the data. 
The Dataset we considered is the Trap 17 Dataset, which contains the plates of cars that have driven through a motorway section. 
For further information about the dataset see the Dataset section and [the map](/map.pdf) .

## Dataset

The dataset is made up of several files: totally there are 7 months and there is a file (ex. 01.06.2016.csv) for each day of the month, which is about 500.000 records. 
A record is structured in this way: 

```
targa;varco;corsia;timestamp;nazione
559784;18;1.0;2016-06-07 10:22:59;IT
```

The headers of the dataset are reported in italian language. Then, the translation follows in order to make clear to any researcher the meaning of every column of the dataset.

targa -> plate
varco -> gate
corsia -> lane
timestamp -> timestamp
nazione -> nationality

Some csv files contains "parziale" in the name. It means "partial", indicating that some problems occurred in that day, causing out-of-service moments.

**N.B.** the dataset folder contains just an example. 

## Features

### Sampling

It is possible to set a reduction factor in order to decrease the total number of considered data. The sample is chosen randomly and it is also possible to fix a random state (a seed) for the reproducibility. You can change it by setting the global variable "seed" in trap17.py .  
For further details look at the Function details. 

### Preprocessing

In order to best represent the most significant attribute (and to avoid to generate a sparse dataset),  it is necessary to change the csv file structure.
The chosen structure is:	targa, tratta, volte  (which means: plate, path, times)
* the plate is the same as before
* the path is the time sorted combination of the gate (separate by an hyphen) that a car goes through, in a single day.
	
  ```
	targa;varco;corsia;timestamp;nazione 
	559784;23;1.0;2016-06-07 10:33:05;IT 
	559784;18;1.0;2016-06-07 10:22:59;IT 
	559784;9;1.0;2016-06-07 09:58:06;IT
	```
	it is transformed into:
	```
	targa,tratta,volte 
	559784,9-18-23-,1  
	 ```
* the field “times” is the number of times that a car drives through the same gates in different days. 

Observations:
* the path is a string 
* in this way the collected data of each day is reduced to about one third.
* the hyphen is necessary in order to distinguish this kind of paths: 11-1 and 1-11.
* in this case the other fields are not interesting.  

### Data overview 

The interesting and meaningful patterns are all of those cars which have driven across a path more than a certain number of times.
Even more interesting event is when more than one car have driven across the same path more than a certain number of times.
In order to do that, it is necessary to analyze the new well structured file (init.csv): basically we first select a subset of the file, which contains just the records with a certain number of time (greater than a chosen threshold), and then we need to plot the data in a clear and meaningful way.
 
An example:
![Alt text](/images/image1.png)

You can display the plates which are associated with the paths :

<p align="center">
<img src="/images/image2.png" width="809" height="440" />
</p>


## Quick Start

1.	Firstly you need to convert each file of the trap17 dataset:

	```
	python convert.py 10
	```

	 the parameter 10 is the chosen reduction factor, the file’s size is divided by 10. 

2.	 Secondly you need to aggregate all the converted files in a single file, init.csv :
	
	  ```
	  python main.py -u True
	  ```

	  This operation normally takes long, depending on the size of the dataset.  

3.	 Thirdly, once the update of init.csv has successfully done, you can use the other parameters to view the 	most interesting patterns:
	 
	
  * you can sort init.csv considering a column, which must be “targa”,”tratta” or ”volte” : 
   
    ```
	   python main.py -s targa
	   ```

  *	you can plot the number of plates of the cars which have driven across a path more than 3 times :

     ```
	   python main.py -p True -t 3
	   ```

  * you can display the paths and the corresponding plates of the cars which have driven across the same path more than 3 times :
  
     ```
	   python main.py -sp True -t 3
	   ```
	   
  * you can set a threshold for selecting the lenght of the path (the minimum number of gates) : 
  
  	 ```
	   python main.py -p true -t 4 -pt 2 
	   python main.py -sp true -t 4 -pt 2 
	   ```
	   
  * if you need to work on another file  : 
  
  	 ```
	   python main.py -f path_file
	   
	   ```
  * for clustering the data using Kmeans (-c [number of clusters] ): 
  	
  	 ```
	   python main.py -c 4
	   
	   python main.py -t 3 -pt 2 -c 4
	   
	   ```
	
	   
4.	 If you need help :

     ```
	   python main.py -h 
	   ```
	   
## Function details 

Trap17.py contains several functions, which allow to work with trap17 dataset. It based mostly on pandas library and numpy library, more specifically:

*	 read_file(file_name,reduction_factor=1,csv_flag=False), which reduce the number of plates considered, but it does not lose any information. This function helps you to read both csv files (targa;varco;corsia;timestamp;nazione  or  targa,tratta,volte). You need to set the parameter csv_flag=True if you want to read a csv file structured as “ targa,tratta,volte ”. Therefore you can set the reduction factor parameter in order to reduce the file size. It is set a seed for being able to reproduce the sample. The reduction factor must be an int. The desired number of plates it is calculated as size= total_plates / reduction_factor.

*  initialize(file_name,file), which allows you to initialize a csv file structured in this way: “targa,tratta,volte” (file_name is the file name to initialize).  Given a csv file from the dataset, this function generates the path according to the definition, which is explained in Preprocessing section. 

*	 initialize_unique(file_name,file), better performances than the initialize(), using pandas.Series.unique (so to skip the records with same plates) and avoiding to show the progress bar.

*	 update(init_file_name,file), given a file, which has been already initialized, this function update an initialized file. Basically it refreshes the column “volte” (times) of an initialized file. When a new plate is found, the function adds a new record. When a plate (which compares in both file but with different path) is found, the function add a new record with the different path.  

*	 sort(file_name,sort_by,kind="mergesort"), if you need to sort the result, you can do it through this function. The parameter “sort_by” must be string or a list of strings which represents the column to take into account. It uses a “mergesort” algorithm by default. 

*	 get_patterns(file_name,times=1,show_plates=False,plates_threshold=0), this function selects from the dataset the items which have times value greater than a certain threshold (the parameter to set this threshold is “times”). By setting the parameter show_plates=True, it shows a table of a selected path and the associated plates. It is possible to set the minimum number of gates in a path through the parameter "plates_threshold".

*	 plot(file_name,times=1,plates_threshold=0), it plots an histogram about the number of cars which have driven across a path more than a certain threshold. It uses the function “get_patterns”.

The elapsed time and the status of each operation is a significant information, which is why it is always shown as an output in the shell.


## Clustering 

Unfortunately, we aren't able to cluster properly with the previous two csv structures, so in order to clustering and to show up some significant featerus, we need to trasform the data. 

### The process 

The data is represented as a matrix with number of columns equal to the number of selected paths and number of rows equal to the number of selected elements :  
 ```	
#[plate,path1,times1,...,pathN,timesN]
selected_dataset = [[2638,3-6-7-,2], [4252,1-2-,2,3-6-7-,2], [5262,4-6-9-,3]]
selected_paths = [1-2-, 3-6-7-, 4-8-9-]
	
# K-Means data input:
#[1-2-, 3-6-7-, 4-8-9-]
data = [[0,2,0],
 	[2,2,0],
 	[0,0,3]]
 
 KMeans(n_clusters=n_clusters).fit(data)

  ```

Then we use Kmeans algorithm, which is provided by [scikit-learn](http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html), in order to cluster the data. 

For sorting out which is the best number of clusters, it is used the Silhouette index. In addition, it is also shown a bar chart (the number of elements in each cluster), the rappresention of the clustered data and their centroids. 

## Experiments

In the experiment folder you can find several files, which have been already updated.
By considering the months of June, July and March :
*	conversion time: 6 min
*	updating time: 57 min
*	init.csv size: about 347,000 records
*	reduction factor: 50 

Output:

```
 python main.py -t 3 -pt 2 -p True
  ```
 ![Alt text](/images/image6.png)

 ```
 python main.py -t 3 -pt 2 -c 90
  ```
  ![Alt text](/images/image7.png)


matrix shape : 296 x 73
  
<p align="center">
<img src="/images/image9.png"/>
</p>

Silhouette index:

![Alt text](/images/image8.png)


## Considerations

All in all, I would say that the second goal of this activiy is to get familiar with some techniques, methodologies and libraries of the data mining environment. 
The model was not complicated on purpose, however it is clear that it is easy to add to the model more details, such as the velocity. It is also possibile to consider other way of defining the path, for istance considering just the last and first gate of a path. 
Furthermore, an interesting way to explore is the biclustering tecnique, which allows us to cluster simultaneusly two attribute, in this case "targa" (plate) and "tratta" (path).


## References 

Visit the websites for a brief introduction :

* http://www.poliziadistato.it/articolo/1659f0710955574304581936
* https://www.youtube.com/watch?v=aCPWz_8slvk


