# ROBAIR avec vision par ordinateur

## Introduction
Ce repositoire contient le projet de l'implementation de vision par ordinateur avec ROS et OpenCV 3 pour être utilisé sur un Raspberry Pi dans un robot.

## Organisation du Repertoire
* Le repositoire principal **catkin_ws** est initialisé par ROS. Donc, il contient les fichiers nécessaires pour le fonctionnement sur un réseaux ROS, et aussi le code principal de vision par ordinateur. Le script principal est **vision_objects.py**
* Les autres fichiers sont des tests avec des autres fonctionnalités .
* Les fichiers MobileNetSSD contiennent les bases de données pour l'implementation de l'aprentissage machine sur le noeud **vision_objects.py**

## Pour exectuer le projet
D'abord, il faut faire le *source* du repertoire ROS
```
source catkin_ws/devel/setup.bash
```
Ensuite, il faut ouvrir un *roscore* (s'il n'est déjà ouvert)
```
roscore
```
Finalement, on peut éxecuter le noeud de vision
```
rosrun robair_opencv vision_objects.py
```
