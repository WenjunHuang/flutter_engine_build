import os
import subprocess
import sys
from settings import *
base_path = os.getcwd()
engine_path = os.path.join(os.getcwd(), "engine")
depot_tools_path = os.path.join(os.getcwd(), "depot_tools")
is_win = sys.platform.startswith('win')
env = set_env(depot_tools_path, engine_path)



os.chdir(os.path.join(engine_path, "src"))
# subprocess.run(
#     [os.path.join(depot_tools_path, "python.bat"), os.path.join(engine_path, "src", "flutter", "tools", "gn"),
#      "--unoptimized", "--target-os", 'win', "--windows-cpu", "x64"], env=env)
subprocess.run(
    [os.path.join(depot_tools_path, "vpython3" + (".bat" if is_win else "")),
     os.path.join(engine_path, "src", "flutter", "tools", "gn"),
     "--unoptimized"], env=env)
# subprocess.run([os.path.join(depot_tools_path,"ninja.exe"),"-C",os.path.join(engine_path,"src","out","host_debug_unopt"),"-t","clean"],env=env)
subprocess.run(
    [os.path.join(depot_tools_path, "ninja" + (".bat" if is_win else "")), "-C",
     os.path.join(engine_path, "src", "out", "host_debug_unopt")],
    env=env)
