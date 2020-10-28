install opencv on raspberry:
- follow this guides https://pimylifeup.com/raspberry-pi-opencv/

install requirements:
$pip3 install -r requirements

some examples of how to run:
<---input video--->
$python3 People_Counter/people.py --prototxt mobilenet_ssd/MobileNetSSD_deploy.prototxt --model mobilenet_ssd/MobileNetSSD_deploy.caffemodel --input ../videos/People_Example_01.mp4

<---input from camera--->
$python3 People_Counter/people.py --prototxt mobilenet_ssd/MobileNetSSD_deploy.prototxt --model mobilenet_ssd/MobileNetSSD_deploy.caffemodel

note: People_Counter/people.py can always be replaced by Queue_Detection/queue.py

https://www.pyimagesearch.com/2018/08/13/opencv-people-counter/
