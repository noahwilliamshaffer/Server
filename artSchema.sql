CREATE TABLE if not exists users
   (email TEXT PRIMARY KEY,
    name TEXT NOT NULL);

CREATE TABLE if not exists likedArt
   (title TEXT NOT NULL,
    url TEXT NOT NULL,
    FOREIGN KEY (email) REFERENCES users
    ON DELETE CASCADE)
