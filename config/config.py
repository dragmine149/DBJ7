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
    prefix = "g!"


git_repo = (
    subprocess.check_output("git config --get remote.origin.url".split(" "))
    .decode("ascii")
    .strip()
)

git_repo = git_repo[:-4] if ".git" in git_repo else git_repo
