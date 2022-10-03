from dotenv import load_dotenv

load_dotenv()
import os
import subprocess
import sys

if not os.path.exists(".env"):
    sys.exit("Please make sure you have a .env file!")

token = os.getenv("TOKEN")
prefix = os.getenv("PREFIX")

if prefix is None:
    prefix = "a!"


git_repo = (
    subprocess.check_output("git config --get remote.origin.url".split(" "))
    .decode("ascii")
    .strip()
)[:-4]
