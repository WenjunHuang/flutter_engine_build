import os
import shutil
import subprocess

import sys

depot_tools_path = os.path.join(os.getcwd(), "depot_tools")
engine_path = os.path.join(os.getcwd(), "engine")
if os.path.exists(engine_path) and os.path.isdir(engine_path):
    shutil.rmtree(engine_path)

print("Fetching engine")

try:
    os.makedirs(engine_path)
except OSError:
    print("Creation of the directory %s failed" % engine_path)
    quit()

shutil.copy("gclientconfig", os.path.join(engine_path, ".gclient"))

isWin = True if sys.platform.startswith('win') else False

env = os.environ.copy()
path = depot_tools_path + (";" if isWin else ":") + env["PATH"]
env["PATH"] = path
print(path)
env["HTTP_PROXY"] = "http://127.0.0.1:9798"
env["HTTPS_PROXY"] = "http://127.0.0.1:9798"

gclient_sufix = ""
if isWin:
    env["DEPOT_TOOLS_WIN_TOOLCHAIN"] = "0"
    gclient_sufix = '.bat'

os.chdir(engine_path)
revision = ["-r", sys.argv[1]] if len(sys.argv) > 1 else []
subprocess.run([os.path.join(depot_tools_path, "gclient" + gclient_sufix), "sync"] + revision, env=env)
