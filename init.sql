CREATE DATABASE flaskDB;
\c flaskDB;
CREATE TABLE "user" (
	id SERIAL PRIMARY KEY,
	username VARCHAR(80) UNIQUE NOT NULL,
	email VARCHAR(120) UNIQUE NOT NULL
);
