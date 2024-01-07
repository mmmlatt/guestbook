import os

os.environ["SECRET_KEY"] = "testsecretkey"
os.environ["DJANGO_TEST_DB_HOST"] = "localhost"
os.environ["POSTGRES_PASSWORD"] = "" #Add your local db password here