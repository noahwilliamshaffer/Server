CREATE TABLE users
   (email TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email, TEXT NOT NULL);

CREATE TABLE likedArt
   (title TEXT NOT NULL,
    url TEXT NOT NULL,
    FOREIGN KEY (email) REFERENCES users
    ON DELETE CASCADE)
