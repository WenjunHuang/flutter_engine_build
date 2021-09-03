import os
import subprocess

base_path = os.getcwd()
engine_path = os.path.join(os.getcwd(), "engine")
depot_tools_path = os.path.join(os.getcwd(), "depot_tools")

vs_path = r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community"
winsdk_path = r"C:\Program Files (x86)\Windows Kits\10"

env = os.environ.copy()
env["DEPOT_TOOLS_WIN_TOOLCHAIN"] = "0"
env["GYP_MSVS_OVERRIDE_PATH"] = vs_path
env["WINDOWSSDKDIR"] = winsdk_path
env["PATH"] = "%s;" % depot_tools_path + env["PATH"]
env["HTTP_PROXY"] = "http://127.0.0.1:9798"
env["HTTPS_PROXY"] = "http://127.0.0.1:9798"

os.chdir(engine_path)
# subprocess.run([os.path.join(depot_tools_path, "gclient.bat"), "sync"], env=env)

os.chdir(os.path.join(engine_path, "src"))
# subprocess.run(["python", os.path.join(engine_path,"src","flutter","tools","gn"),"--unoptimized"],env=env)
subprocess.run(
    [os.path.join(depot_tools_path, "python.bat"), os.path.join(engine_path, "src", "flutter", "tools", "gn"),
     "--unoptimized", "--target-os", 'win', "--windows-cpu", "x64"], env=env)
# subprocess.run([os.path.join(depot_tools_path,"ninja.exe"),"-C",os.path.join(engine_path,"src","out","host_debug_unopt"),"-t","clean"],env=env)
subprocess.run(
    [os.path.join(depot_tools_path, "ninja.exe"), "-C", os.path.join(engine_path, "src", "out", "win_debug_unopt")],
    env=env)
