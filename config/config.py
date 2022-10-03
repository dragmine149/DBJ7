from dotenv import load_dotenv

load_dotenv()
import os
import subprocess

token = os.getenv("LEVEL_TOKEN")
prefix = os.getenv("LEVEL_PREFIX")
database_host = os.getenv("LEVEL_DATABASE_HOST")
database_port = os.getenv("LEVEL_DATABASE_PORT")
database_name = os.getenv("LEVEL_DATABASE_NAME")
database_user = os.getenv("LEVEL_DATABASE_USER")
database_password = os.getenv("LEVEL_DATABASE_PASSWORD")
database_ssl = True if bool(int(os.getenv("LEVEL_DATABASE_SSL"))) else False
database_url = "postgresql://{}:{}@{}:{}/{}".format(
    database_user, database_password, database_host, database_port, database_name
)
git_repo = (
    subprocess.check_output("git config --get remote.origin.url".split(" "))
    .decode("ascii")
    .strip()
)[:-4]
