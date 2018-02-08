# Project Work on Data Mining

Data preprocessing and data analysis

  - [About](#about)


## About

This is a project work on Data Mining. The goal of this project is to find interesting patterns (such as the number of cars which have driven across the same path more than a certain number of times) in a large dataset. In order to do that we need to sample the data, to transform the data in a useful structures and in the end to mine the meaningful information.
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

### Data analysis 

The interesting and meaningful patterns are all of those cars which have driven across a path more than a certain number of times.
Even more interesting event is when more than one car have driven across the same path more than a certain number of times.
In order to do that, it is necessary to analyze the new well structured file (init.csv): basically we first select a subset of the file, which contains just the records with a certain number of time (greater than a chosen threshold), and then we need to plot the data in a clear and meaningful way.
 
An example:
![Alt text](/images/image1.png)
![Alt text](/images/image2.png)

## Quick Start

1.	Firstly you need to convert each file of the trap17 dataset:

	```
	python convert.py 10
	```

	 the parameter 10 is the chosen reduction factor, the file’s size is divide by 10. 

2.	 Secondly you need to aggregate all of the converted files in a single file, init.csv :
	
	  ```
	  python main.py -u True
	  ```

	  This operation normally takes some time.  

3.	 Thirdly, once the update of init.csv has successfully done, you can use the other parameters to view the 	most interesting patterns:
	 
	
  * you can sort init.csv considering a column, which must be “targa”,”tratta”or ”volte” : 
   
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
  
4.	 If you need help :

     ```
	   python main.py -h 
	   ```
	   
## Function details 

Trap17.py contains several functions, which allow to work with trap17 dataset. It based mostly on pandas library and numpy library, more specifically:

*	 read_file(file_name,reduction_factor=1,csv_flag=False), which helps you to read both csv files (targa;varco;corsia;timestamp;nazione  or  targa,tratta,volte); you need to set the parameter csv_flag=True if you want to read a csv file structured as “ targa,tratta,volte ”. Therefore you can set the reduction factor parameter in order to reduce the file size, skipping randomly some rows. It is set a seed for being able to reproduce the sample. The reduction factor must be an int. The desired size it is calculated as size= total_lines / reduction_factor  .

*  initialize(file_name,file), which allows you to initialize a csv file structured in this way: “targa,tratta,volte” (file_name is the file name to initialize).  Given a csv file from the dataset, this function generates the path according to the definition, which is explained in Preprocessing section. 

*	 initialize_unique(file_name,file), better performances than the initialize(), using pandas.Series.unique (so to skip the records with same plates) and avoiding to show the progress bar.

*	 update(init_file_name,file), given a file, which has been already initialized, this function update an initialized file. Basically it refreshes the column “volte” (times) of an initialized file. When a new plate is found, the function adds a new record. When a plate (which compares in both file but with different path) is found, the function add a new record with the different path.  

*	 sort(file_name,sort_by,kind="mergesort"), if you need to sort the result, you can do it through this function. The parameter “sort_by” must be string or a list of strings which represents the column to take into account. It uses a “mergesort” algorithm by default. 

*	 get_patterns(file_name,times=1,show_plates=False,plates_threshold=0), this function selects from the dataset the items which have times value greater than a certain threshold (the parameter to set this threshold is “times”). By setting the parameter show_plates=True, it shows a table of a selected path and the associated plates. It is possible to set the minimum number of gates in a path through the parameter "plates_threshold".

*	 plot(file_name,times=1,plates_threshold=0), it plots an histogram about the number of cars which have driven across a path more than a certain threshold. It uses the function “get_patterns”.

The elapsed time and the status of each operation is a significant information, which is why it is always shown as an output in the shell.


## References 

Visit the websites for a brief introduction :

* http://www.poliziadistato.it/articolo/1659f0710955574304581936
* https://www.youtube.com/watch?v=aCPWz_8slvk


