-- Create Dellstore 2 database
CREATE TABLESPACE dbspace LOCATION '/data/dbs';
CREATE USER sqlinjection WITH PASSWORD '3FS-DI';
CREATE DATABASE dellstore2 OWNER sqlinjection TABLESPACE dbspace;
ALTER USER sqlinjection WITH SUPERUSER;