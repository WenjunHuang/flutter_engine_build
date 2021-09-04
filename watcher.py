import os
import subprocess
import sys

import time
from rx import operators as ops
from rx import subject as s
from rxpy_backpressure import BackPressure
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class RebuildAndRunTestObserver(Observer):
    def on_next(self, event):
        print(f"{event.src_path} has been modified")

        env = os.environ.copy()
        is_win = sys.platform.startswith('win')
        if is_win:
            # visual studio 2019
            vs_path = r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community"
            # windows kits
            winsdk_path = r"C:\Program Files (x86)\Windows Kits\10"
            env["DEPOT_TOOLS_WIN_TOOLCHAIN"] = "0"
            env["GYP_MSVS_OVERRIDE_PATH"] = vs_path
            env["WINDOWSSDKDIR"] = winsdk_path

        depot_tools_path = os.path.join(os.getcwd(), "depot_tools")
        engine_path = os.path.join(os.getcwd(), "engine")

        env["HTTP_PROXY"] = "http://127.0.0.1:9798"  # 设置代理
        env["HTTPS_PROXY"] = "http://127.0.0.1:9798"  # 设置代理
        env["PATH"] = depot_tools_path + os.pathsep + env["PATH"]

        try:
            output = os.path.join(engine_path, "src", "out", "host_debug_unopt")
            # first recompile
            subprocess.run([os.path.join(depot_tools_path, "ninja" + (".exe" if is_win else "")),
                            "-C",
                            output,
                            ], env=env,
                           check=True)

            # then run unit tests
            # unittest_name = "tonic_native_dart_class"
            unittest_name = "my_smartpointer"
            subprocess.run([os.path.join(output, unittest_name + "_unittests" + (".exe" if is_win else "")),
                            "--gtest_filter=-*TimeSensitiveTest*",
                            "--gtest_shuffle", ],
                           check=True)
        except:
            pass

    def on_error(self, error: Exception):
        pass

    def on_completed(self):
        pass


build_subject = s.Subject()
build_subject.pipe(
    ops.debounce(0.2)
).subscribe(BackPressure.DROP(RebuildAndRunTestObserver(), 1))


def on_created(event):
    build_subject.on_next(event)


def on_deleted(event):
    build_subject.on_next(event)


def on_modified(event):
    build_subject.on_next(event)


patterns = ["*.c", "*.cc", "*.h", "*.gn", "*.dart"]
event_handler = PatternMatchingEventHandler(patterns, None, False, True)
event_handler.on_created = on_created
event_handler.on_deleted = on_deleted
event_handler.on_modified = on_modified

observer = Observer()
engine_path = os.path.join(os.getcwd(), "engine", "src", "flutter")
observer.schedule(event_handler, engine_path, recursive=True)
observer.start()
try:
    while True:
        time.sleep(1)
finally:
    observer.stop()
    observer.join()
