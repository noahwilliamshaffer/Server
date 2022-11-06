CREATE TABLE if not exists users
   (UserId INTEGER PRIMARY KEY,
    email TEXT Not Null,
    name TEXT NOT NULL);

CREATE TABLE if not exists likedArt
   (	ID TEXT NOT NULL,
	title TEXT NOT NULL,
    	url TEXT NOT NULL,
    	FOREIGN KEY (ID) REFERENCES users(UserId)
    	ON DELETE CASCADE);
