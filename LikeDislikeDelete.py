def ClearLikedArt():
    connection = sqlite3.connect('likedArticles.db')

    cur = connection.cursor()
    cur.execute(" DELETE FROM items")
    connection.commit()
    connection.close()
ClearLikedArt()



def ClearDislikedArt():
    connection = sqlite3.connect('dislikedArticles.db')

    cur = connection.cursor()
    cur.execute(" DELETE FROM items")
    connection.commit()
    connection.close()
ClearDislikedArt()
