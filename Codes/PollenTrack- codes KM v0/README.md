![Logo PI PollenTrack (1)](https://github.com/user-attachments/assets/2b89f491-86c7-4b91-8bda-1eb77a85acd4)

## Introduction
Dans le cadre de mon cursus en école d'ingénieur à Telecom Physique Strasbourg, j'ai du en deuxième année prendre part à un projet ingénieur. Ce projet a été proposé par un client à l'école qui nous l'a ensuite proposé. Je fais donc partie d'une équipe de 5 étudiants dans laquelle je suis responsable de la partie software.

## Client
Le client est Eric Herber, ingénieur qualité de l'air à ATMO Grand Est.

## Présentation du projet et enjeu
Notre projet s’intitule POLLENTRACK. Ce projet a pour but de réaliser un capteur de pollens capable d'effectuer le prélèvement du pollen de manière autonome et d'acquérir des image à l'aide d'un microscope embarqué du prélèvement. 

Une reconnaissance des grains de pollens via une intelligence artificielle permettra alors une analyse plus complète qui donnera ensuite une indication sur le taux et le type de pollens dans l’air. Cette reconnaissance par intelligence artificielle est réalisée par une entreprise extérieure, nous ne serons donc pas responsables de cette tâche. 

L'enjeu de cet outil embarqué est de pouvoir prévenir les populations en cas de forte quantité de pollen dan l'air pour éviter des désagréments aux personnes sensibles.

## Architecture du projet
Le projet prend la forme d'une boîte dans laquelle sont disposés deux modules :

- Une partie liée au captage du pollen constituée d'une cheminée où un ventilateur créant un flux d'air de 10L/min (~respiration humaine) entraine le pollen vers une bande adhésive sur laquelle celui ci est piégé.

- Une partie liée à l'acquisition d'image de ce pollen avec un microscope embarqué. Le microscope embarqué utilisé est le Microscope Openflexure 1.6.5 qui est donc relié à la caméra Raspberry pi V2.

Ces deux parties sont reliées entre elles par un moteur qui se chargera du déplacement du scotch entre les deux.

Le cerveau du système est un raspberry pi 4B .
## Algorithme d'autofocus du microscope
Le problème majeur est de réussir à prendre une photo qui n’est pas floue. Je souhaiterai donc créer un code qui permet de faire le focus d’une image. 

Pour déterminer si une image est nette ou pas, on s’intéresse au bord des objets qui se trouvent dans l’image. On les reconnait par une subite forte variation de l’intensité des pixels. Plus la variation est forte, plus l’image est nette. Au contraire, plus la variation est “diffuse”, moins l’image est nette. On a donc affaire à un problème de traitement d’image.

Il existe de nombreux algorithmes de détection de bord comme ‘canny’ par exemple qui sont déjà implémenté en python dans le module opencv.

- On ne veut pas faire le focus de l’image mais se focus sur une partie de l’image seulement qui est la zone où on a détecté un grain de pollen.
Il faudrait donc commencer par détecter un grain de pollen dans l’image puis se concentrer sur cette zone. Pour cela j'effectue la détection des contours de l'image afin de pouvoir ensuite déterminer l'objet le plus grand (jugé plus pertinent). Je découpe maintenant le tour de l'objet et j'obtient ainsi une sous-image qui est celle sur laquelle on déterminera si la photo est floue. Toutes les opérations se feront sur celle-ci.
- Une fois cette zone trouvée, on veut savoir à quel point elle est floue. Pour cela, il faut d’abord créer un algo qui détermine “le taux de netteté” d’une image. Pour l'instant j'utilise la variance du filtre laplacien comme taux de netteté (l'objectif est de maximiser cette variance pour avoir un taux de netteté maximum) mais ce système détermine le taux de netteté en parti en se basant sur les auréoles autour des grains de pollen. Je n'obtient donc pas forcément la meilleure netteté sur le grain de pollen en lui-même. Il semblerait que les auréoles soient causées par une réaction chimique le scotch et les grains de pollen. Une solution peut-être de réaliser plusieurs acquisitions avec différents focus : c'est à dire qu'une fois que le focus est fait, on capture des images en dezoomant un peu et zoomant un peu.
- Connaissant cela, il faut maintenant y aller à tatillon : on actionne le moteur pour zoomer quelque peu (déterminer de combien on bouge) la caméra et à chaque itération on regarde si le taux de netteté est meilleure que précédemment. Si le taux est meilleur, on zoom et si il est pire on dézoom. On itère jusqu’à un taux qui nous convient.
- On peut ainsi prendre la photo.
## Résultat
![436609042_297606970101523_3743437641338467726_n](https://github.com/user-attachments/assets/3ab35bfc-065f-4dd0-8f17-8bd58c4edf4a)
