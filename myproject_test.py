from myproject import app  # Flask instance of the API

@pytest.fixture()
def app():
    app = app()
    app.config.update({
        "TESTING": True,
        "SECRET_KEY": os.getenv('AUTH0_CLIENT_SECRET')
    })
    yield app

def test_index_route():
    response = app.test_client().get("/")

    assert response.status_code == 200
    # assert response.data.decode('utf-8') == 'Testing, Flask!'


def test_login_route():
    response = app.test_client().get("/login")
    # login is a redirect
    assert response.status_code == 302


def test_loginout_route():
    response = app.test_client().get("/logout")
    # logout is a redirect
    assert response.status_code == 302


def test_news_route(app):
    response = app.test_client().get("/news")

    assert response.status_code == 200


def test_Admin_route():
    response = app.test_client().get("/UserProfiles")

    assert response.status_code == 200


def test_profile_route():
    response = app.test_client().get("/Profile")

    assert response.status_code == 200


#def test_Database():
   # ID = 1
   # con = sqlite3.connect("dislikedArticles.db")
   # cursor = con.execute("DELETE FROM items WHERE id IN (1)")
   # items = cursor.fetchall()
   # cursor.close()

    #Email = 1
    #con = sqlite3.connect("likedArticles.db")
    #cursor = con.execute("SELECT id, email, title, url FROM items")
    #items = cursor.fetchall()
    #cursor.close()

    ##assert response.status_code


#def test_get_close_db(app):
  #  with app.app_context():
   ##    assert db is get_db()

    #with pytest.raises(sqlite3.ProgrammingError) as e:
     #   db.execute("SELECT 1")

    #assert "closed" in str(e.value)
