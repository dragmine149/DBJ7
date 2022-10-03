from dotenv import load_dotenv

load_dotenv()
import os
import subprocess

token = os.getenv("TOKEN")
prefix = os.getenv("PREFIX")

if prefix is None:
    prefix = "a!"


git_repo = (
    subprocess.check_output("git config --get remote.origin.url".split(" "))
    .decode("ascii")
    .strip()
)[:-4]
