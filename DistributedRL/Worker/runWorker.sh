sudo docker run --rm -v /home/boubin/SoftwarePilot/DistributedRL/Data/Worker$1_$2:/home/mydata:Z -v /home/boubin/Images/:/home/imageData:Z -it --network "host" -e SERVERNUM=0 -e WORKERNUM=0 worker /bin/bash
