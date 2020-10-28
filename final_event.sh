#!/bin/bash

nohup python3 EventoFinal/Parks/parque_sul.py & \
 nohup python3 EventoFinal/Parks/parque_norte.py &\
  nohup python3 EventoFinal/People/palco_meo.py &\
   nohup python3 EventoFinal/People/palco_vodafone.py &\
    nohup python3 EventoFinal/Queues/entrance.py &\
     nohup python3 EventoFinal/Queues/WC.py &\
      nohup python3 EventoFinal/Sells/bilhetes.py &\
       nohup python3 EventoFinal/Sells/cachorros.py &\
        nohup python3 EventoFinal/Sells/cervejas.py &\
         nohup python3 EventoFinal/Wcs/wcm1.py &\
          nohup python3 EventoFinal/Wcs/wcm2.py &\
           nohup python3 EventoFinal/Wcs/wcm3.py &\
            nohup python3 EventoFinal/Wcs/wcw1.py & \
            nohup python3 EventoFinal/Wcs/wcw2.py & \
            nohup python3 EventoFinal/Wcs/wcw3.py & \ 
             nohup python3 EventoFinal/Activities/palco_meo.py & \
             nohup python3 EventoFinal/Activities/palco_vodafone.py & \
             nohup python3 EventoFinal/GPS/gps.py &
