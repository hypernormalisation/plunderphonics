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


-- original tracks table
CREATE TABLE public.original_tracks
(
    track_id serial,
    uploaded_by_user_id integer NOT NULL,
    track_link text COLLATE pg_catalog."default",
    track_name text COLLATE pg_catalog."default",
    date_modified timestamp,
    date_created timestamp default current_timestamp,
    CONSTRAINT original_tracks_pk PRIMARY KEY (track_id),
    CONSTRAINT "ORIGINAL_TRACKS_USERS_FK" FOREIGN KEY (uploaded_by_user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE public.original_tracks
    OWNER to admin;

-- DROP INDEX public."fki_ORIGINAL_TRACKS_USERS_FK";

CREATE INDEX "fki_ORIGINAL_TRACKS_USERS_FK"
    ON public.original_tracks USING btree
    (uploaded_by_user_id ASC NULLS LAST)
    TABLESPACE pg_default;