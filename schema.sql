


CREATE TABLE Messages (
  id INTEGER PRIMARY KEY,
  comments_section INTEGER,
  message_target INTEGER,
  message_content INTEGER,
  message_time TEXT
);

CREATE TABLE MessageContents (
    id INTEGER PRIMARY KEY,
    content TEXT
);

CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);


CREATE TABLE Posts (
    id INTEGER PRIMARY KEY,
    poster INTEGER,
    post_pool INTEGER,
    post_headline TEXT
);

CREATE TABLE PostContents (
    id INTEGER PRIMARY KEY,
    post INTEGER,
    content TEXT
);

CREATE TABLE CommentsSections (
    id INTEGER PRIMARY KEY,
    post INTEGER
);



CREATE TABLE PostPools (
    id INTEGER PRIMARY KEY,
    owner INTEGER,
    post_pool_title TEXT
);


