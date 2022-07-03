# Planar Baluns

- [Introduction](#introduction)
  * [Balun decomposition](#balun-Decomposition)   
- [Balun parts](#balun-parts)
  * [Crossovers](#crossovers)
- [Graph representation of baluns](#graph-representation-of-baluns)
  * [Key observations of the graph representation](#key-observations-of-the-graph-representation)
- [Common balun topologies](#common-balun-topologies)
  * [_X_ crossover](#_x_-crossover)
  * [_XX_ crossover](#_xx_-crossover)
  * [_XI_ crossover](#_xi_-crossover)  
- [Python scripts](#python-scripts)
  * [Requirements](#requirements)
  * [Script outputs](#script-outputs)
    
## Introduction 

Shown here is an example of a 1:2 planar balun.  The red and blue represent two unique metal layers and the cyan represents their via. 
A complete balun might require additional capacitors to 'tune' the balun to the intended frequency.  There will be no additional discussion on the 
electrical behavior of the balun.  Other then that the turn ratios mentioned here are only to account for the physical turns, and will not always 
give the same expected electrical effect.   

<img src="Balun_Images/6T-2-1A2-1.png" alt="alt text" width=600>

### Balun Decomposition 
The balun shown above can be decomposed into a primary winding and a secondary winding. 
These are shown respectively from left to right.

<img src="Balun_Images/6T-2-1_split_A2-1.png" alt="alt text" >

___

## Balun parts 
Just so we are on the same page, the naming convention used for the various parts of the balun is shown here.
In all the balun figures, only the secondary center-tap is shown.

<img src="Balun_Images/6T-2-1B2-1.png" alt="alt text">|<img src="Balun_Images/6T-2-1D2-1.png" alt="alt text">
:---:|:---:
_Tracks_|_Ports_

<img src="Balun_Images/6T-2-1C2-1.png" alt="alt text">|<img src="Balun_Images/6T-2-1E2-1.png" alt="alt text">
:---:|:---:
_Crossovers_|Secondary _Center-tap_

### Crossovers 
The various crossover structures are further broken down below, along with their naming convention. 
To preserve balun symmetry, only symmetrical crossovers such as _-_, _X_, _XX_, and _Asterisk_ 
can be placed along the y-axis or the axis of the ports. 
This here, is definitely not an exhaustive collection of crossovers.

<img src="Balun_Images/XO_-_2.png" alt="alt text">|<img src="Balun_Images/XO_1x_2.png" alt="alt text">|<img src="Balun_Images/XO_2x_2.png" alt="alt text">
:---:|:---:|:---:
_Jumper_ or _-_|_X_|_XX_

<img src="Balun_Images/XO_2x2_2.png" alt="alt text">|<img src="Balun_Images/XO_3x_2.png" alt="alt text">|<img src="Balun_Images/XO_3x-_2.png" alt="alt text">
:---:|:---:|:---:
unnamed|_XI_|*_Asterisk_

##### *Note on the _Asterisk_:
Care is needed for the expansion of connections of this structure. 
As more connections are added, more metal layers are needed, and the structure approaches the following:  
<img src="Balun_Images/BOC.jpg" alt="asshole" width=80> 

___

## Graph representation of baluns 
So far, we have only dealt with the physical layout of the balun. 
We can represent the balun in graph form with vertices and edges to ease their analysis and synthesis. 
We start by replacing the tracks with vertices and the crossovers with edges. 
Then we utilize the symmetry and fold the vertices and edges about the y-axis.  These steps are illustrated below.

<img src="Balun_Images/6T-2-1F-1.png" alt="alt text" width=900>|<img src="Balun_Images/6T-2-1G2-1.png" alt="alt text">
:---:|:---:
Balun with vertices and edges superimposed|Graph representation

### Key observations of the graph representation 
Some somewhat obvious observations/rules are listed below.
    
|Graph with emphasized portion in red|Notes|
|---|:---:|
|<img src="Balun_Images/6T-2-1H-1.png" alt="alt text" width=1000>|These vertices with a single edge are the ports.|
|<img src="Balun_Images/6T-2-1I-1.png" alt="alt text" width=1000>|These vertices with a self loop are the center-tap locations.|
|<img src="Balun_Images/6T-2-1J-1.png" alt="alt text" width=1000>|The upper row and lower row form two sets.  With the exception of the port vertices, each vertex has exactly one edge to each set.|
|<img src="Balun_Images/6T-2-1K-1.png" alt="alt text" width=1000>|These connected vertices form a path that is the secondary winding.  The number of vertices in a set along a path is the number of turns in that winding.|

**_Believe it or not, this graph representation simplifies analysis and synthesis of planar baluns._**

___

## Common balun topologies
### _X_ crossover
This class of balun is generally used as a 1:1 balun.  Although ratios such as 1:2 can be realized, 
the distribution of the tracks may not result in a good electrical 1:2.
The center-tap location is at the inner most winding, this may be inconvenient to access.
Some examples are shown below:


<img src="Balun_Images/L_G_1T-1-1X-1.png" alt="alt text" width=600>|<img src="Balun_Images/G_1T-1-1X-1.png" alt="alt text">
:---:|:---:
1 Turn 1:1 Layout|1 Turn 1:1 Graph

<img src="Balun_Images/L_G_2T-1-1X-1.png" alt="alt text" width=600>|<img src="Balun_Images/G_2T-1-1X-1.png" alt="alt text">
:---:|:---:
2 Turn 1:1 Layout|2 Turn 1:1 Graph

<img src="Balun_Images/L_G_3T-1-1X-1.png" alt="alt text" width=600>|<img src="Balun_Images/G_3T-1-1X-1.png" alt="alt text">
:---:|:---:
3 Turn 1:1 Layout|3 Turn 1:1 Graph

<img src="Balun_Images/SCI-106.png" alt="alt text" width=600>|<img src="Balun_Images/G_SCI-106-1.png" alt="alt text">
:---:|:---:
3:5 Turn Layout|3:5 Turn Graph

### _XX_ crossover
This class of balun is probably best used as a 1:1 balun.  Although ratios such as 1:2 can be realized, the distribution of the tracks may not result in a good electrical 1:2.  
The center-tap location can be chosen on the second outermost winding.  This is a convenient location and can be accessed without vias.
The minimum turns is 2.  Also, for non 1:1 ratios, the turns on each winding must be even. 

<img src="Balun_Images/L_G_2T-1-1XX-1.png" alt="alt text" width=600>|<img src="Balun_Images/G_2T-1-1XX-1.png" alt="alt text">
:---:|:---:
2 Turn 1:1 Layout|2 Turn 1:1 Graph

<img src="Balun_Images/L_G_3T-1-1XX-1.png" alt="alt text" width=600>|<img src="Balun_Images/G_3T-1-1XX-1.png" alt="alt text">
:---:|:---:
3 Turn 1:1 Layout|3 Turn 1:1 Graph

<img src="Balun_Images/L_G_4T-1-1XX-1.png" alt="alt text" width=600>|<img src="Balun_Images/G_4T-1-1XX-1.png" alt="alt text">
:---:|:---:
4 Turn 1:1 Layout|4 Turn 1:1 Graph

<img src="Balun_Images/L_G_4T-4-6XX-1.png" alt="alt text" width=600>|<img src="Balun_Images/G_4T-4-6XX-1.png" alt="alt text">
:---:|:---:
4:6 Turn Layout|4:6 Turn Graph

### _XI_ crossover
This class of balun is probably best used as a 1:2 balun.  Although ratios such as 1:1 can be realized, the distribution of the tracks may not result in a good electrical 1:1.  
The center-tap location for one winding can be chosen on the second outermost winding. 
See the docstring in Balun_XI_Example for turn ratio limitations.
  
<img src="Balun_Images/L_G_1-2XY-1.png" alt="alt text" width=600>|<img src="Balun_Images/G_1-2XY-1.png" alt="alt text">
:---:|:---:
1:2 Turn Layout|1:2 Turn Graph

<img src="Balun_Images/L_G_2-4XY_1-1.png" alt="alt text" width=600>|<img src="Balun_Images/G_2-4XY_1-1.png" alt="alt text">
:---:|:---:
2:4 Turn Layout|2:4 Turn Graph

<img src="Balun_Images/L_G_2-4XY_2-1.png" alt="alt text" width=600>|<img src="Balun_Images/G_2-4XY_2-1.png" alt="alt text">
:---:|:---:
2:4 Turn Non-Expandable Layout|2:4 Turn Non-Expandable Graph

<img src="Balun_Images/L_G_4-4XY-1.png" alt="alt text" width=600>|<img src="Balun_Images/G_4-4XY-1.png" alt="alt text">
:---:|:---:
4 Turn 1:1 Layout|4 Turn 1:1 Graph

___

## Python scripts (updated for gdspy 1.6.12)
The motivation for these scripts is to simplify the generation of these complex structures for electromagnetic simulations.
There are probably infinite ways to realize these types of baluns. Three of which are explicated with the example scripts. 

### Requirements
* [Python 3.x](http://www.python.org/) 
* [Gdspy 1.6.12](https://github.com/heitzmann/gdspy)

### Script outputs

```sh
python3 Balun_X_Example.py
```
<img src="Balun_Images/Balun_X_Example.jpg" alt="alt text" >

```sh
python3 Balun_XX_Example.py
```
<img src="Balun_Images/Balun_XX_Example.jpg" alt="alt text" >

```sh
python3 Balun_XI_Example.py
```
<img src="Balun_Images/Balun_XI_Example.jpg" alt="alt text" >
