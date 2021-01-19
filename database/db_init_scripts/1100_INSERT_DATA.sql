INSERT INTO USERS (
    username,
    password,
    email_address,
    date_modified
) VALUES(
    'admin',
    '$2b$12$Yc2qjXGtOsFqR6ck6v2ruOCIM6FRjIpsnf5zL54H/CPnmt7KhldHO',
    'dev@pomeron.com',
    timestamp '2021-01-01 00:00'
);

INSERT INTO USERS (
    username,
    password,
    email_address,
    date_modified
) VALUES(
    'john',
    '$2b$12$TJKlMJUjGf/T.5jh9mGEW.yZIdobSfMysTzvG3mHDW7kJ5G6ZyuHe',
    'john@pomeron.com',
    timestamp '2021-01-02 10:00'
);

INSERT INTO ORIGINAL_TRACKS (
    user_id,
    url,
    name
) VALUES(
    1,
    'file:///some_dummy.wav',
    'my_track'
);

INSERT INTO ORIGINAL_TRACKS (
    user_id,
    url,
    name
) VALUES(
    1,
    'file:///some_other_file.wav',
    'my_track_2'
);

INSERT INTO ORIGINAL_TRACKS (
    user_id,
    url,
    name
) VALUES(
    2,
    'file:///johns_track.wav',
    'johns_track'
);
