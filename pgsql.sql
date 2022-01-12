CREATE DATABASE history;

CREATE TABLE readings(
    temperature double precision not null,
    humidity double precision not null,
    datetime timestamp with time zone default now()
);
