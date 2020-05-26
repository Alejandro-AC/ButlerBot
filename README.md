# ButlerBot
Robotics Course - Simulation of a robot and it's different modules

Descripció

L'objectiu del nostre projecte ha estat simular un robot capaç de realitzar la cerca d'objectes dins d'un espai desconegut

Requeriments:

Python 3.6

Llibreries:

-pygame

-pyaudio

-speech_regonition

-pillow

-opencv-python

Arxius:

yolov3.weights(Afegir a la carpeta yolo) 


Execució
Clonar repositori
Instal·lar les llibreries necessaries (pip install [llibreria]). Afegir l’arxiu yolov3—— link: https://pjreddie.com/darknet/yolo/
Executar el programa fer un “Run”

Resultat Execució:

Comandes de veu demanant-li que mostri on es troba la poma

![1](https://github.com/Alejandro-AC/ButlerBot/blob/master/Imagenes/conversa.PNG)


Dibuix que representa l'escena d'acció

![2](https://github.com/Alejandro-AC/ButlerBot/blob/master/Imagenes/mapa.PNG)


La simulació del recorregut que realitza l'algoritme RRT per l’exploració, es mostra mitjançant les línies de color blau i el recorregut que realitza el robot fins a arribar l’objecte és el camí que es mostra de color verd

![3](https://github.com/Alejandro-AC/ButlerBot/blob/master/Imagenes/mapaExecucio.PNG)


Diagrama de flux

![4](https://github.com/Alejandro-AC/ButlerBot/blob/master/Imagenes/speechRecognition.PNG)

Execució Completa

![5](https://github.com/Alejandro-AC/ButlerBot/blob/master/Imagenes/ExecucioTotal.PNG)


Contribució: 

El Butlerbot, és un robot d’ajuda a persones d’edat avançada o amb problemes de visió, ja que a través de comandes de veu poden demanar un objecte que requereixen trobar. El robot és capaç de processar aquesta informació, identificar i trobar aquest objecte dins d’un mapa que desconeix inicialment, fent ús de l'algoritme RRT i els sensors de proximitat. Un  cop trobat, aquest objecte, el robot torna a la posició inicial per informar a la persona que ja coneix la posició d’aquest. De tal manera que proporciona una ajuda en la recerca d’objectes a persones amb dificultats.

Autors: 

Marta Aguilera Sorrives (1335167)


Alejandro Aznar Cortés (1393192)


Judit Boladeras Guillaumes (1459355) 


Jordi Jané Besora (1462196)
