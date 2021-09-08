# TFG de Informática 2021 (Joan Nadal)

PREDICCIÓ D'INTERACCIÓ DE PROTEÏNES DE VIRUS-HOSTE I LA SEVA FUNCIÓ

Els virus són patògens amb genomes bastant compactes que, no obstant,proporcionen eines moleculars molt versàtils capaces de causar una gran diversitat de canvis en els processos cel·lulars. Aquesta versatilitat pot ser degut a l’àmplia varietat de dominis codificats pels virus, així com, els seus mecanismes d’evolució molecular. El mecanisme d’infecció dels virus és per mitjà d’interaccions proteiques entre les proteïnes de virus i les de l’hoste. Per tant, és de gran interès conèixer aquestes interaccions per desenvolupar noves estratègies per inhibir les PPIs virus-hoste i, d’aquesta manera, evitar la infecció. També, obtenir més coneixement per explicar l’expansió de la virulència dels patògens i la gamma d’hostes dels virus causants de malalties.

En el següent treball s’ha desenvolupat una eina que permet obtenir les funcions d’un conjunt de famílies de proteïnes (VPFs) a partir de l’assignació a cada model de proteïnes víriques de la base de dades d’UniProt. A més, també determina les PPIs virus-hoste, així com, la informació de les funcions de les proteïnes hoste. A partir d’aquesta classificació, es pot fer la predicció de les PPIs virus-hoste i les funcions d’una nova proteïna vírica associada a un model VPF de la qual en desconeixem informació.

Per la gestió de dades, s’ha creat una base de dades PostgreSQL i s’ha fet ús de l’ORM SQLAlchemy per accedir a la base de dades i guardar-hi les dades. Tota l’execució del projecte es realitza en un contenedor Docker per facilitar el desplegament de l’aplicació.

Pel que fa als resultats, un 36,4% dels models té proteïnes de la base de dades d'UniProt assignades de les quals només un 43,6% de les assignacions són fiables al tenir un e-value < 0.001. De les proteïnes víriques assignades a models, un 35,2% té interaccions amb proteïnes d’hoste, sent l’hoste majoritariàment un animal, especialment l’espècie humana.



Viruses are pathogens with fairly compact genomes. Nevertheless, they provide very versatile molecular tools capable of causing a wide variety of changes in cellular processes. This versatility may be due to the wide variety of domains encoded by viruses, as well as their mechanisms of molecular evolution. The mechanism of virus infection in a host is through protein interactions. It is of great interest to get acquainted with these interactions to develop new strategies to inhibit virus-host PPIs to prevent infection and gain more knowledge to explain the expansion of the virulence of pathogens and the range of hosts in disease-causing viruses.

In this work, a tool to classify viral protein families (VPFs) has been developed. The tool assigns viral proteins from the UniProt database to each model in order  to infer the model’s biological functions. In addition, it also determines the virus-host PPIs as well as the functions of the host proteins. From this classification, it is possible to predict the virus-host PPIs and the biological functions of new viral proteins via its assignment to a classified VPF.

For data management, a PostgreSQL database has been created. The ORM SQLAlchemy has been used to access and save data to the created database. All project execution has been done in a Docker container to facilitate the deployment of the application.

In terms of results, 36,4% of the models have assigned proteins from UniProt database. Among them, only 43,6% of the assignments are reliable with an e-value < 0.001. 35.2% of these viral proteins assigned to models have interactions with host proteins, being the host mostly an animal, especially the human species.



Existeix arxiu Makefile per facilitar l'execució del programa. Aquest fitxer conté les següents instruccions:

	- download-files: descarregar fitxers

	- build-test: construir els contenedors per realitzar el test
	- run-test: execució del test
	- clean-test: borrar contenedors, images i volums

	- build-app: construir els contenedors per executar el codi
	- run-app: execució del codi
	- clean-app: borrar contenedors, images i volums



A continuació, s'explica com executar el programa des d'una màquina pròpia seguint els següents punts:

	1- Instal·lar totes les dependències de Python i Docker necessàries per a la correcte execució.

	2- Descarregar el codi font de GitHub: "https://github.com/joannadal4/TFGInformatica".

	3- Executar make download-files per tal de descarregar els fitxers utilitzats pel programa.

	4- Executar make build-app per construir els contenedors Docker necessaris.

	5- Executar make run-app per iniciar l'execució del codi.
