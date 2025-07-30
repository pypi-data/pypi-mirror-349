import sys
import subprocess
import os
from pathlib import Path
import time

def animate(text, duration=1.5):
    for _ in range(3):
        for dot in ['.', '..', '...']:
            print(f"{text}{dot}", end='\r')
            time.sleep(duration / 6)
    print(f"{text}... done!")

def create_project_structure():
    Path("src/my_lib").mkdir(parents=True, exist_ok=True)
    with open("src/my_lib/my_lib.py", "w", encoding="utf-8") as f:
        f.write("""\
### Your Lib Script

class my_lib:
    pass
""")
    with open("src/my_lib/__init__.py", "w", encoding="utf-8") as f:
        f.write("""\
# init exemple:
# from .my_lib import function
""")
    with open("pyproject.toml", "w", encoding="utf-8") as f:
        f.write("""\
[project]
name = "name"
version = "0.1.0"
description = ""
authors = [
    { name = "", email = "" }
]
requires-python = ">=3.10"
license = {text = "MIT"}

readme = "README.md"
keywords = []
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
]
dependencies = [
    "aiohttp>=3.8.0"
]

[project.urls]
Homepage = "https://github.com"
Repository = "https://github.com/"
Issues = "https://github.com/"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
""")

def Pypck():
    if len(sys.argv) < 2:
        print("Usage: PyPck (-build, -upload, -buildlib, -update)")
        sys.exit(1)

    command = sys.argv[1]

    if command == "-build":
        print("🔨 Building project...")
        animate("Generating files")
        create_project_structure()
        print("✅ Build Finish")

    elif command == "-upload":
        print('Directory Path:')
        dir_path = input('>> ')
        print('Do you already have build lib for your project? (y/n)')
        build_state = input('>> ')
        if build_state != 'y':
            subprocess.run(["python", "-m", "build"])
        os.chdir(dir_path)
        os.system('twine upload dist/*')

    elif command == "-buildlib":
        subprocess.run(["python", "-m", "build"])

    elif command == "-update":
        print('Have you already modified your project? (y/n)')
        state = input(">> ")
        if state == 'y':
            os.system('twine upload dist/*')
        else:
            subprocess.run(["pip", "install", "-e", "."])
            print('You can now edit your project. When you are done, run: Pypck -upload')

    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)
