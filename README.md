# FabricNDNVideo
NDN Video streaming on the Fabric testbed using a custom dynamic/adaptive algorithm, and experiments comnparing results to DASH


Code is ran by, first running the fabric notebook in

NDN Project/Experiment1/InitialSetup.ipynb

At the bottom of the notebook is a test, where the connection between nodes over IP is tested. Sometimes due to inconsistencies, this does not pass and the ping fails. If this happens, you can delete the slice and rerun the notebook. Otherwise do not delete the slice (do not run the final cell).

After running this notebook, you have to ssh into all 7 machines and run the command ./install_ndn.sh

Then, after the install script finishes, you can run nfd-start on each machine and they will all be ready


Then, the next notebook to run is the NDNTests.ipynb notebook.

This notebook creates a dictionary to make it easier to do operations quickly on various nodes, by storing important parts of them. Then, the notebook creates static routing rules between the consumers and the producer by going through the routers. 

Then, the notebook runs ndnpeek/ndnpoke on each of the consumers and the producer node to make sure that every node is reachable. Finally, it runs a test python program consumer_test.py and producer_test.py, which just publish and receive the data "content" at the namespace /producer/test/msg2


The notebook to run the experiments is 
NDN Project/Experiment1/NDNVideo.ipynb

The notebook assembles the same dictionary representing the nodes and their information first. Then, it uploads the producer and consumer video programs, video_producer.py and video_consumer.py. It then runs the video producer.
The remaining cells are the actual experiment. First, the experiment variables are set. Then, the next cell starts each consumer and sets the rate limit. The next cell waits for each consumer to finish and saves its results. Then the next cell runs all of the clients using DASH streaming, and the cell after that waits for them to finish and saves the results. The 2nd to last cell is only sometimes ran, as it clears the cache. If you are doing a second run of the experiment, do not run it, simply rerun the experiment variable setting with run_number=2, then run the next 2 cells. When changing the latency or number of consuemrs, this 2nd to last cell is ran, as it clears the cahce contents. Finally, there is a cell which is simply there to demonstrate how to add rate limits to the nodes, and then a cell to delete the slice.



The notebook for analyzing results is NDN Project/Analysis.ipynb, and contains several graphs of the results
