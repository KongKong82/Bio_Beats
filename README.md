# Bio_Beats
ME 570 Project

This project utilizes a rapsberry pi pico 2 W. The 2 W starts its own network and acts as an access point (AP). The pico will be collecting data from a thermistor, as well as a pulse oximeter. This data will be streamed to a TCP port as the sensor apparatus is designed to be portable. A computer will connect to the network published by the pico, and will run a python script to recieve, process, and export data.
