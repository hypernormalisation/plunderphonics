-- Table: public.users

-- DROP TABLE public.users;

CREATE TABLE public.users
(
    id serial,
    username text COLLATE pg_catalog."default" unique,
    password text COLLATE pg_catalog."default",
    email_address text COLLATE pg_catalog."default",
    date_modified timestamp,
    date_created timestamp default current_timestamp,
    CONSTRAINT users_pk PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.users
    OWNER to admin;