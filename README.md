# Développement d'une application CRM B2B en Flask


> CRM est l'abréviation de _Customer Relationship Management_,
> c'est-à-dire gestion de la relation client. La relation client englobe
> toutes les interactions entre une entreprise et ses clients existants
> ou potentiels. L'objectif d'un CRM est d'entretenir les relations avec
> les clients en offrant des interactions les plus personnelles et
> individuelles possible.

## Présentation du projet: 

L'entreprise AVP a aujourd'hui une problématique de structuration et de sécurisation de la donnée de ses clients. L'objectif du projet est d'optimiser la configuration de la partie data pour que l'entreprise gagne en efficacité. 

Le projet se découpe en deux parties: 

 - l'une est la **création d'un outil CRM pour stocker/archiver** de manière structurée l'ensemble des données de l'entreprise AVP. 
 - l'autre partie du projet, est de créer un outil de type **Dashboard pour obtenir un suivi des performances de l'ensemble des KPI's** de la société. Idéalement cette étape sera automatisée et affichera en temps réel l'évolution des éléments.

## Cahier des charges

### 1. Le contexte

L'entreprise AVP- AnneVachonProduction a été créée en 2010 par Anne Vachon, entrepreneur basée à Lyon. Aujourd'hui suite à un besoin d'aide à l'organisation et de sécurisation des données générées par la structure, cela a été pour moi l'occasion de réaliser mon projet de fin de formation en mettant mes compétences acquises au service d'un veritable projet pour une utilisation concrète. 

 - **Enjeux** :  
	 - Développer l’action commerciale en simplifiant et organisant la donnée 
	 - Organiser le reporting, le suivi de la performance
 - **Stratégies**: 
	 - Centraliser les échanges / informations dans un CRM pour faciliter la recherche et l'enregistrement de nouvelles données par l'utilisateur. 
	 - Réaliser une analyse de performances en suivant l’évolution des différents indicateurs de performance à travers le temps afin de faciliter la prise de décision.
 - **Domaine d'application**: 
	 - La gestion des comptes clefs depuis une interface web. Ici nous entendons par comptes clefs les clients, prospect, chruner et prestataire. 
	 - L’historique et l’analyse des ventes depuis une interface web.
	 - Organisation d'une migration de l'historique des ventes et de la gestion clients dans l'outil.
- **Features à développer pour l'évolution produit**:
	- Création d'une base de donnée répertoriant l'ensemble des images achetées, en création un système de recherche simplifié par mots clés.
	- Création d'une base de donnée pour la partie production de la société qui référencerait l'ensemble des repérage / lieux loués avec recherche simplifiée également via l'interface web.
	- Le développement d'un système de facturation intégré interconnecté à la base pour une automatisation du remplissage des informations clients. 


### 2. Les objectifs 

#### Objectifs de la conception d'un CRM 

 1. *Moins de processus administratifs, plus d'activités commerciales*
Ici il s'agit d'augmenter la productivité globale en standardisant les processus et automatisant certaines tâches. L'intérêt également est de centraliser l'historique de chaque client pour qu'il soit visible en un coup d'œil.

 2. *Une organisation efficace, sans tableau Excel*
 Certaines entreprises tentent de résoudre la question de l'organisation des données en les centralisant sur un fichier Excel statique. Cette solution sert à récolter certaines données pertinentes, mais elle ne règle qu'une partie du problème. Un fichier statique ne vous permet pas d'analyser en profondeur l'impact de chacune des interactions. De plus, le CRM  est un outil facilement évolutif et dynamique.

#### Objectifs de la conception d'un Dashboard

 1. *Une vue d'ensemble du processus de vente*
 Notamment avec les transactions conclues, l'historique des transactions pour mieux visualiser les performances commerciales du mois en cours. La répartition des ventes par secteur, taille d'entreprise. Egalement étudier la saisonnalité pour mieux comprendre et appréhender les futures transactions. 



### 3. Les contraintes

 1. *Le délais*
 Premier projet d'envergure il est difficile d'estimer le temps pour chacune des tâches et d'anticiper les actions. 
 2. *Le format des donnés*
 Difficulté à l'exploitation du format .vcf des contacts. 
 3. *L'étendu du projet*
 Beaucoup de chose est possible d'entreprendre sur ce projet la difficulté sera de se tenir à des éléments réalisable dans le temps imparti. 

### 4. Périmètre

Collaboration avec Anne Vachon, Dirigeante de l'entreprise AVP pour la récupération des données, le recueil du besoin spécifique lié à l'activité. Elle sera également la future utilisatrice de l'outil. Moi-même serait en charge de la création, de la mise en place de l'outil selon le besoin client. 

Quels sont les processus concernés par le projet CRM ?

 - Commercial : 
	 ◦ gestion des comptes ou sociétés et des contacts par l'ajout, modification ou suppression d'informations
	 ◦ cycle de vente en attribuant un statut à chaque contact pour déterminé sa maturité
 - Administration des ventes :
	 - grâce à la fonctionnalité dashboard ```(KPI à définir)```

### Modèle conceptuel des données 
 
 Le  *MCD*  est une représentation graphique de haut niveau qui permet facilement de comprendre comment les différents éléments sont liés entre eux à l’aide de diagrammes codifiés dont les éléments suivants font partie :

-   Les  entités (1 rectangle = 1 objet) ;
-   Les propriétés (la liste des données de l’entité) ;
-   Les relations qui expliquent et précisent comment les entités sont reliées entre elles ;
-   Les cardinalités (les petits chiffres ou icône au niveau des « pattes »).
 
 [MCD réaliser avec l'outil dbschema interconnecté à ma base Postegresql](https://picasaweb.google.com/112605649790783837489/6761385938055172881#6761385936890824962)

### Modèle organisationnel des données



    A compléter

### Import de données

Les données sont déjà existante, ici il n'y aura pas de création d'un dataset. Nous utiliserons l'existant. 

Les données sont fournis par l'entreprise.

Vcard metada: [https://en.wikipedia.org/wiki/VCard](https://en.wikipedia.org/wiki/VCard)

````python
{'adr': {'box': <class 'str'>,
         'city': <class 'str'>,
         'code': <class 'str'>,
         'country': <class 'str'>,
         'extended': <class 'str'>,
         'region': <class 'str'>,
         'street': <class 'str'>},
 'bday': <class 'str'>,
 'categories': <class 'list'>,
 'email': <class 'str'>,
 'fn': <class 'str'>,
 'n': {'additional': <class 'str'>,
       'family': <class 'str'>,
       'given': <class 'str'>,
       'prefix': <class 'str'>,
       'suffix': <class 'str'>},
 'nickname': <class 'str'>,
 'note': <class 'str'>,
 'org': <class 'list'>,
 'photo': <class 'bytes'>,
 'prodid': <class 'str'>,
 'tel': <class 'str'>,
 'title': <class 'str'>,
 'uid': <class 'str'>,
 'url': <class 'str'>,
 'version': <class 'str'>,
 'x-abadr': <class 'str'>,
 'x-ablabel': <class 'str'>,
 'x-abrelatednames': <class 'str'>,
 'x-abshowas': <class 'str'>,
 'x-abuid': <class 'str'>,
 'x-apple-subadministrativearea': <class 'str'>,
 'x-imagehash': <class 'str'>,
 'x-imagetype': <class 'str'>,
 'x-socialprofile': <class 'str'>}
 ````
### Requêtes

    A compléter sous forme de liste

### Interface

    Réalisation d'une maquette à définir
L'idée est de créer une application Flask, nous auront un système de recherche (ex: par nom, prénom, email, date...) puis une possibilité de mettre à jour l'outil en insérant des données fraîches dans une fiche client existant ou en créant une nouvelle fiche. 

La partie dashboard permettra de simplement visualiser des graphiques représentatif de l'activité. 

### Conclusion 



### Aide mémoire 
```py   
# trouver les valeurs dans le json selon une clé défini  
for i, elem in enumerate(x):  
    print(x[i]['n'][0]['suffix'])  
  
# etudier les numéro de tel  
for i, elem in enumerate(x):  
    print(i)  
    phone = x[i]['tel']  
    print(phone)  
    print()  
    if phone in x:  
        print(len(phone))  
    else:  
        print(f'no phone for {org}')  
        print()```

# compter le nbr d'élement dans une entitée

from pprint import pprint as pp
for y in x.list_contact:
    if 'email' in y:
        print(len(y['email']))
    else:
        print('nop')
        
#**kwargs 
for n in list_n:  
    n_ = N(**n)