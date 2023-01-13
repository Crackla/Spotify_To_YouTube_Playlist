import os

script_list = ["Spotify.py", "YouTube1.py", "YouTube2.py"]

for script in script_list:
    if os.path.isfile(script):
        os.system(f"python {script}")
    else:
        print(f"{script} does not exist in the current directory.")