


CREATE TABLE Messages (
  id INTEGER PRIMARY KEY,
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

CREATE TABLE UserProfiles (
    id INTEGER PRIMARY KEY,
    user_id TEXT UNIQUE,
    post_pools INTEGER
);



CREATE TABLE Posts (
    id INTEGER PRIMARY KEY,
    post_headline TEXT UNIQUE,
    post_content INTEGER,
    post_comments INTEGER
);


