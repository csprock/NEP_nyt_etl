-- create New York Times article database
CREATE TABLE Article(
	id			CHAR(24) UNIQUE,
	headline	TEXT,
	lead		TEXT,
	date		DATE,
	page		INT,
	wordcount	INT,
	url			TEXT, 
	section		TEXT,
	subsection	TEXT,
	desk		TEXT,
	material	TEXT,
	abstract	TEXT,
	snippet		TEXT,
	source		TEXT,
	PRIMARY KEY (id));

CREATE TABLE Tags(
	id		CHAR(24) REFERENCES Article(id),
	tag		VARCHAR(30),
	keyword		TEXT,
	PRIMARY KEY (ID,Tag,keyword));


CREATE TABLE byline(
	id			CHAR(24) REFERENCES Article(id),
	name		VARCHAR(75),
	PRIMARY KEY(ID, name));









