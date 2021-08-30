import os
import shutil
import subprocess

base_path = os.getcwd()
engine_path = os.path.join(os.getcwd(),"engine")
depot_tools_path = os.path.join(os.getcwd(),"depot_tools")
outpath_path = os.path.join(os.getcwd(),"engine_out")
if not os.path.exists(outpath_path):
    os.makedirs(outpath_path)

vs_path = r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community"
winsdk_path = r"C:\Program Files (x86)\Windows Kits\10"

subprocess.run([os.path.join(depot_tools_path,"ninja.exe"),"-C",os.path.join(engine_path,"src","out","win_debug_unopt")])
