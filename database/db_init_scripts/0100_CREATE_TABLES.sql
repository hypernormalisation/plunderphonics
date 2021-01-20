-- users tables
CREATE TABLE public.users
(
    id serial,
    username text COLLATE pg_catalog."default" unique,
    hashed_password text COLLATE pg_catalog."default",
    email text COLLATE pg_catalog."default",
    date_modified timestamp default current_timestamp,
    date_created timestamp default current_timestamp,
    CONSTRAINT users_pk PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.users
    OWNER to admin;


-- original tracks table
CREATE TABLE public.original_tracks
(
    id serial,
    user_id integer NOT NULL,
    url text COLLATE pg_catalog."default",
    name text COLLATE pg_catalog."default",
    date_modified timestamp default current_timestamp,
    date_created timestamp default current_timestamp,
    CONSTRAINT original_tracks_pk PRIMARY KEY (id),
    CONSTRAINT "ORIGINAL_TRACKS_USERS_FK" FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE public.original_tracks
    OWNER to admin;


CREATE INDEX "fki_ORIGINAL_TRACKS_USERS_FK"
    ON public.original_tracks USING btree
    (user_id ASC NULLS LAST)
    TABLESPACE pg_default;