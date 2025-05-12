# Robotisation d’un aéroport

## Mise en contexte

Dans un contexte criant de pénurie de main d'œuvre, l’aéroport de Montréal peine à maintenir ses activités et à suivre l’horaire. Le gestionnaire de l’aéroport envisage de robotiser les activités de chargement et de déchargement des bagages. On désire procéder à une étude de simulation afin de déterminer le nombre de robots à acquérir.

Le gestionnaire a observé que le temps entre deux arrivées d’avions (temps inter-arrivées) ainsi que le temps de chargement/chargement d’un avion se comportent selon deux lois exponentielles. Le temps moyen entre deux arrivées d’avion est de **12.3 minutes**. Le temps moyen nécessaire pour charger et décharger un avion varie en fonction du nombre de robots y travaillant. Le tableau suivant présente le temps moyen nécessaire pour charger et décharger un avion en fonction du nombre de robots qui y travaillent (on ne peut décharger et charger qu’un seul avion à la fois).

| Nombre de robots | Temps moyen pour charger et décharger un avion (minutes) |
| ---------------- | -------------------------------------------------------- |
| 2                | 9.0                                                      |
| 3                | 7.0                                                      |
| 5                | 5.5                                                      |
| 8                | 4.5                                                      |
| 12               | 4.2                                                      |

Nous simulerons **40 000 minutes d’activités en régime permanent**, et cela pour chacun des scénarios. Les indicateurs de performance à considérer sont les suivants: (1) le nombre d’avions chargés/déchargés par heure, (2) le nombre d’avions dans la file d’attente, (3) le temps d’attente d’un avion dans la file d’attente, ainsi que (4) le taux d’occupation des robots.

## Activités

1. Déterminez la durée de la **période d'échauffement** (durée du régime transitoire + période tampon) pour chacun des scénarios.

   - Pour ce faire, pour chaque indicateur et pour chaque scénario, produisez un graphique présentant la valeur de l'indicateur en fonction du temps pour toute la durée l'horizon de simulation. Pour chaque indicateur vous avez le choix d'afficher sur le graphique la valeur instantanée en fonction du temps (ex : nombre d'avion dans la file d'attente au temps t) ou encore sa valeur moyenne depuis le début de la simulation au temps t. L'un de ces deux graphiques sera plus parlant que l'autre; à vous de déterminer lequel.
   - Pour chaque scénario, vous observez quand le système semble tomber en régime permanent (par l'observation des 4 graphiques). Ajoutez une période tampon et cela défini votre période d'échauffement.
   - Représentez cette valeur par une barre verticale sur les graphiques.
   - Finalement, pouvez conserver une valeur différente pour chaque scénario ou conserver la plus grande des 5. Justifiez votre choix parmi ces deux options (il n'y a priori pas de mauvaise réponse).

2. Pour chacun des 5 scénarios, mesurez la performance avec un intervalle de confiance (95%) sur l'horizon de simulation (mesuré après la période d'échauffement). Assurez-vous d'avoir un horizon de simulation assez long et un nombre de réplications suffisamment élevé pour départager les différents scénarios. Fournir un tableau comportant une ligne par indicateur et une colonne par scénario et inscrivez l'intervalle de confiance.

3. Discuter des résultats et formuler des recommandations pour le gestionnaire (avec justifications).

4. Supposons maintenant que l'aéroport a la possibilité d'augmenter sa capacité d'accueil d'avions. À l'aide d'expériences complémentaires, déterminer le nombre d'avions que l'aéroport pourrait traiter tout en demeurant performant, mais en se limitant à 12 robots. Autrement dit : si j'ai 12 robots, de combien puis-je augmenter l'arrivage des avions tout en ayant une bonne performance? (avec justifications)

## Consignes

- Vous devez programmer votre simulation en faisant usage des concepts de la simulation à événements discrets : chaque événement survient à un moment précis et cause un changement à l'état du système. Entre ceux-ci, rien ne change et l'horloge peut donc être avancée au prochain événement.
- Les langages de programmation permis sont Java, Python, C++ et C#
- Vous pouvez utiliser le générateur de nombres pseudo-aléatoires fourni avec le langage choisi (optionnellement, vous pouvez coder une approche plus avancée).
- Vous devez programmer votre générateur de variable aléatoire (qui fera usage du générateur de nombres pseudo-aléatoires mentionné au point précédent)
- La fonction racine de votre programme (ex : main) est simplement constituée d'une série d'appels à une fonction (un appel par scénario et par réplication) réalisant la simulation du scénario en question.
- La simulation doit s'exécuter sans erreur et sans intervention de la part du correcteur (il n'a pas à changer manuellement les paramètres de la simulation)
- Lorsque le programme s'exécute, il doit imprimer dans la console les résultats complets (indicateur pour chaque avion, pour chaque heure, etc.)
- La production des graphiques et de l'analyse statistique peut être faite, à votre choix, dans le code ou en utilisant un outil tel qu'Excel.

## À remettre

- Une archive zip contenant tout le code permettant d'exécuter la simulation et votre rapport en format pdf (résumant la démarche point par point, les graphiques, tableaux et analyses).
