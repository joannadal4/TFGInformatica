# TFG de Informática 2021 (Joan Nadal)

PREDICCIÓ D'INTERACCIÓ DE PROTEÏNES DE VIRUS-HOSTE I LA SEVA FUNCIÓ

Els virus són patògens amb genomes bastant compactes que, no obstant, proporcionen eines moleculars molt versàtils capaces de causar una gran diversitat de canvis en els processos cel·lulars. Aquesta versatilitat pot ser degut a l’àmplia varietat de dominis codificats pels virus, així com, els seus mecanismes d’evolució molecular. 

El mecanisme d’infecció dels virus és per mitjà d’interaccions proteiques entre les proteïnes de virus i les de l’hoste. Per tant, és de gran interès conèixer aquestes interaccions per desenvolupar noves estratègies per inhibir les PPIs virus-hoste i, d’aquesta manera, evitar la infecció. També, obtenir més coneixement per explicar l’expansió de la virulència dels patògens i la gamma d’hostes dels virus causants de malalties.

En el següent treball s’ha desenvolupat una eina que permet obtenir les funcions d’un conjunt de famílies (o models) de proteïnes (VPFs) a partir de  l’assignació a cada model de proteïnes víriques de la base de dades d’UniProt.  A més, també determina les PPIs virus-hoste, així com, la informació de les funcions de les proteïnes hoste. A partir d’aquesta classificació, es pot fer la predicció de les PPIs virus-hoste i les funcions d’una nova proteïna vírica associada a un model VPF de la qual en desconeixem informació.

Per la gestió de dades, s’ha creat una base de dades PostgreSQL i s’ha fet ús de l’ORM SQLAlchemy per accedir a la base de dades i guardar-hi les dades. Tota l’execució del projecte es realitza en un contenedor Docker per facilitar el desplegament de l’aplicació.


A continuació, s'explica com executar el programa des d'una màquina pròpia seguint els següents punts:
	1- Instal·lar totes les dependències de Python i Docker necessàries per a la correcte execució.
	
	2- Descarregar el codi font de GitHub: "https://github.com/joannadal4/TFGInformatica".
	
	3- Executar download.py per tal de descarregar els fitxers utilitzats pel programa.
	
	4- Crear el contenidor de Docker mitjançant: "docker-compose build".
	
	5- Encendre el servidor de Docker executant la comanda: "docker-compose up".
	
	6- Actualitzar l'estat de la base de dades: "docker-compose run modelvpf alembic upgrade head".
	
	7- Executar novament 'docker-compose up' amb la base de dades actualitzada.
	
	8- A una nova terminal, executar: "psql -p 1234 -h localhost -U postgres -d modelvpf" i contrasenya: "postgres" per accedir a la base de dades per fer consultes. 
