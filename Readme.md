# Benchmarking_SLAM

Tools and files to evaluate map and localization quality of SLAM technologies

Project by Paul Asquin for Awabot - Summer 2018 paul.asquin@gmail.com

# [map_crop.py](map_crop.py)  

With [map_crop.py](map_crop.py), you can automatically crop pgm files to the exact size used by the map.
To do so, create a folder named _maps_ and copy there your .pgm and .yaml files generated with [map_server map_server](http://wiki.ros.org/map_server#map_saver).  
Then, run 
```
sudo python3 map_crop.py
```

# [metrics.py](metrics.py)

[metrics.py](metrics.py) will return the proportion of occupied pixels (black pixels = obstacles) of every map under the _maps_ folder.  
Run  
```
sudo python3 metrics.py
```

# [plot_top.py](plot_top.py)

With [plot_top.py](plot_top.py), you can plot the use of CPU and RAM of wanted processes using a top.txt file.  
In order to generate this file under a GNU/Linux OS, you can start your processes then run 
```
top -b -d 1 > top.txt
```   

By default, the script will listen to processes containing the names "hector", "gmapping" and "cartographer_no". 
You can change them by editing the SELECT_PROCESS global parameter in the script.  

In the end, you will be able to plot graph like this one : 

![Graph clean benchmarking](docs/clean_benchmarking_load.png)
Graph of CPU and RAM use of Hector SLAM, GMapping and Google Cartographer