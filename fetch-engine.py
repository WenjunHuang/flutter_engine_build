import os
import shutil
import subprocess
import sys

depot_tools_path  = os.path.join(os.getcwd(),"depot_tools")
engine_path = os.path.join(os.getcwd(),"engine")
if os.path.exists(engine_path) and os.path.isdir(engine_path):
    shutil.rmtree(engine_path)

print("Fetching engine")

try:
    os.makedirs(engine_path)
except  OSError:
    print ("Creation of the directory %s failed" % engine_path)
    quit()

shutil.copy("gclientconfig",os.path.join(engine_path,".gclient"))

env = os.environ.copy()
env["PATH"] = env["PATH"]+ ";%s" % depot_tools_path
env["HTTP_PROXY"] = "http://127.0.0.1:9798"
env["HTTPS_PROXY"] = "http://127.0.0.1:9798"
env["DEPOT_TOOLS_WIN_TOOLCHAIN"] = "0"
os.chdir(engine_path)
revision = sys.argv[1] if len(sys.argv) > 1 else ""
subprocess.run([os.path.join(depot_tools_path,"gclient.bat"),"sync","-r",revision],env=env)
