
import os
import sys

def set_env(depot_tools_path,engine_path):
    env = os.environ.copy()
    is_win = sys.platform.startswith('win')
    if is_win:
        # visual studio 
        vs_path = r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools"
        # windows kits
        winsdk_path = r"C:\Program Files (x86)\Windows Kits\10"
        env["DEPOT_TOOLS_WIN_TOOLCHAIN"] = "0"
        env["GYP_MSVS_OVERRIDE_PATH"] = vs_path
        env["WINDOWSSDKDIR"] = winsdk_path


    env["HTTP_PROXY"] = "http://127.0.0.1:9799"  # 设置代理
    env["HTTPS_PROXY"] = "http://127.0.0.1:9799"  # 设置代理
    env["PATH"] = depot_tools_path + os.pathsep + env["PATH"]
    return env

