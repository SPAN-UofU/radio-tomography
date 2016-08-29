This repository contains the open source radio tomography software toolchain for usage with the Texas Instruments CC2530 SoC. The toolchain is developed by researchers from Leiden University and CWI Amsterdam and contains software from Texas Instruments and the University of Utah amongst others. Please refer to the references section below for an extensive list of sources.

This is a branch off of the CWI Amsterdam repo.

Prerequisites
=============

In order to be able to use the toolchain, you must install the following software on your system. The software has been developed for Linux, but can also be made to work on Windows or any other operating system since all prerequisites are also present for those operating systems.

* Git 1.9.0 (other versions might also work)
* SDCC 3.3.0 (other versions might also work)
* Python 2.7 with the following packages (package names may differ per operating system):
    * `python2-pyserial`
    * `python2-pyqt4`
    * `python2-numpy`
    * `python2-scipy`
    * `python2-pyqtgraph`
    * `python2-opengl`
    * `python2-matplotlib`
* Vim or any other code editor
* `boost` and `boost-libs` (package names may differer per operating system)

For all commands in this file, replace `python` by `python2` if your operating system uses that to distinguish between Python 2.x and Python 3.x and replace `vim` by any other code editor you might be using.

Configuring cc-tools


Compiling the software
======================

Now that you have a copy of the software, you can compile the software. The software consists of two parts: software for the listener node (USB dongle) and software for the RF nodes. Both must be compiled individually using the steps outlined below.

We hereby release multi-Spin 3.0. The changelog for version 3.0 in comparison with version 2.0 is as follows:

- Full support has been added for the open source SDCC compiler (you cannot compile with the commercial tool IAR Embedded Workbench anymore).
- Correlation values are implemented into Spin packets.
- Spin clock code has been rewritten and the code style has been made consistent.

In order to be able to flash the HEX files onto the nodes later on, we must first compile cc-tool. Note that compiling from source is necessary because the software has been patched for usage with the CC2530 nodes. Run the following commands to compile cc-tool.

Linux:

    $ cd tools/cc-tool

MacOS:

    $ git clone https://github.com/SPAN-UofU/cc-tool.git
    $ cd cc-tool

then:

    $ ./configure
    $ make
    $ make install

Channels
--------

The listen node(s) and RF nodes must agree on which channels to communicate on. You can edit the channel list by editting the file "channels.h" under the following directory:

    $ cd ~/path/to/radio-tomography/libraries/multi-spin-3.0/xpand2531

Edit the number of channels macro and the channel sequence array. Channels 11 - 26 are available to use. Save the file after updating.

USB Dongles or CC2530
---------------------

The USB Dongles use the CC2531 chip whereas the boards with the SMA connector use the CC2530. Open the file "Makefile" under the following directory

    $ cd ~/path/to/radio-tomography/software/rf-node/

To program the USB dongles, give -Dchip the value 2531 as shown below.

    CFLAGS += $(INCLUDES) -DNDEBUG -Dchip=2531 --model-large --Werror --opt-code-size

To program the CC2530s, give -Dchip the value 2530 as shown below.

    CFLAGS += $(INCLUDES) -DNDEBUG -Dchip=2530 --model-large --Werror --opt-code-size


Listener and RF node
--------------------

Before compiling the listener and RF node software, you must update the number of RF nodes in your sensor network. You can do this as follows:

    $ cd ~/path/to/radio-tomography
    $ make

Then enter the number of nodes in the sensor network. Listener nodes do not count toward this number.

Flashing the software
=====================

The next step is to flash the Intel HEX files onto the USB dongle or the RF nodes. This process is described below.

Listener node
-------------

To flash the listener node, supply power to the USB dongle and connect the CCdebugger to the computer. Use the ribbon cable to connect the CCdebugger to the listener node and press the Reset button on the CCdebugger. The light should be green. If the devices are properly connected, run the following commands.

    $ cd ~/path/to/radio-tomography/software/listener-node/
    $ sudo make prog

Once the process is complete, the listener node is flashed. Repeat this process if you want multiple listener nodes

RF nodes
--------

To flash the listener node, supply power to the USB dongle that will be "Node 1" and connect the CCdebugger to the computer. Use the ribbon cable to connect the CCdebugger to Node 1 and press the Reset button on the CCdebugger. The light should be green. If the devices are properly connected, run the following commands.

    $ cd ~/path/to/radio-tomography/software/rf-node/
    $ sudo make prog

Enter the number "1" for node 1. Once the process is complete, Node 1 has been flashed. Repeat this process for nodes 2 through N, replacing "1" with the current node number.

Tools
=====

The network should be up and running now. To inspect the network, the toolchain provides several useful tools that are outlined below.

Sniffer
-------

The sniffer allows you to capture all Spin packets received by the listener node from the serial connection. It will show each received Spin packet in a readable format. You can pipe the output to a file, however it is recommended to use the measurement framework described below for that. You can run the sniffer using the following command:

    $ cd ../../tools
    $ sudo python sniffer.py

Plotter
-------

The toolchain provides a realtime 2D line plotter. You can use the plotter only for a sensor network consisting of two nodes. Running the command

    $ sudo python plotter.py 26

will open a plot window with two line plots: one for the RSS values and one for the correlation values. The last parameter, 26 in this case, is the channel for which the RSS and correlation values are plotted.

Measurement framework
---------------------

The measurement framework is a framework for performing experiments with the sensor network. It can fetch packets directly from the serial connection, filter them according to rules given by the reseacher and export the results as text files or LaTeX plot files (using the `pgfplots` package). First, you must run

    $ vim measurement_framework.py

to adapt the `main` function to your own wishes. Example usage for a simple experiment is:

    # Get packets for five seconds
    sniffer = Sniffer()
    sniffer.start(5)
    sniffer.stop()
    packets = sniffer.getPackets()

    # Only keep packets from node 1 to node 2
    filter = Filter(packets)
    packets = filter.where('fromNode', 1)
    packets = filter.where('toNode', 2)
    
    # Write the results to a text file and create two LaTeX plots
    export = Export(packets)
    export.txt('measurements.txt')
    export.tex('plot_rssi.tex', 'rssi', channels)
    export.tex('plot_corr.tex', 'corr', channels)

After adapting the `measurement_framework.py` file, you can run the experiment using

    $ sudo python measurement_framework.py 11 16 21 26

Again, the parameters indicate the channels to use for the experiment.

Authors
=======

* Folkert Bleichrodt (CWI Amsterdam, @3cHeLoN)
* Tim van der Meij (Leiden University, @timvandermeij)
* Alyssa Milburn (Leiden University, @fuzzie)

License
=======

The toolchain itself is licensed under a GPL v3 license. Please refer to the `LICENSE` file for more information. However, the external libraries used (like cc-tool, the CC USB firmware or multi-Spin) are licensed under their own licenses. Refer to their individual license files for more information. multi-Spin 3.0 has the same license as multi-Spin 2.0.

If you use this material in your own work, please properly cite the papers indicated below, which describe the protocol from the original authors of multi-Spin:

* _M. Bocca, O. Kaltiokallio, and N. Patwari. "Radio Tomographic Imaging for Ambient Assisted Living", in S. Chessa and S. Knauth (Eds.): EvAAL 2012, Communications in Computer and Information Science (CCIS) 362, pp. 108-130, Springer (2013)._

* _O. Kaltiokallio, M. Bocca, and N. Patwari. "Enhancing the Accuracy of Radio Tomographic Imaging Using Channel Diversity", 9th IEEE Int. Conference on Mobile Ad Hoc Sensor Systems (IEEE MASS 2012), October 8-10, 2012, Las Vegas, NV, USA._

References
==========

This software in this toolchain uses or is based on the following sources.

* multi-Spin 2.0: https://sites.google.com/site/boccamaurizio/home/software-data
* Texas Instruments CC USB library: http://www.ti.com/lit/zip/swrc088
* cc-tool: http://sourceforge.net/projects/cctool/files
* smartdoor: http://code.google.com/p/smartdoor/source/browse/trunk/rfap
