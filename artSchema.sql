CREATE TABLE if not exists users
   (email TEXT PRIMARY KEY,
    name TEXT NOT NULL);

CREATE TABLE if not exists likedArt
   (	Users_Id TEXT NOT NULL,
	title TEXT NOT NULL,
    	url TEXT NOT NULL,
    	FOREIGN KEY (User_Id) REFERENCES users (email)
    	ON DELETE CASCADE);
