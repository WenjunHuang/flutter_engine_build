import os
import subprocess

import time
from rx import operators as ops
from rx import subject as s
from rxpy_backpressure import BackPressure
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class ConsumerObserver(Observer):
    def on_next(self, event) -> None:
        print(f"{event.src_path} has been modified")
        # visual studio 2019安装路径
        vs_path = r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community"
        # windows kits 安装路径
        winsdk_path = r"C:\Program Files (x86)\Windows Kits\10"
        depot_tools_path = os.path.join(os.getcwd(), "depot_tools")
        env = os.environ.copy()
        env["DEPOT_TOOLS_WIN_TOOLCHAIN"] = "0"
        env["GYP_MSVS_OVERRIDE_PATH"] = vs_path
        env["WINDOWSSDKDIR"] = winsdk_path
        env["HTTP_PROXY"] = "http://127.0.0.1:9798"  # 设置代理
        env["HTTPS_PROXY"] = "http://127.0.0.1:9798"  # 设置代理
        env["PATH"] = "%s;" % depot_tools_path + env["PATH"]

        engine_path = os.path.join(os.getcwd(), "engine")
        depot_tools_path = os.path.join(os.getcwd(), "depot_tools")
        subprocess.run([os.path.join(depot_tools_path, "ninja.exe"), "-C",
                        os.path.join(engine_path, "src", "out", "host_debug_unopt")], env=env, shell=True, check=True)

        unittest_path = os.path.join(engine_path, "src", "out", "host_debug_unopt")
        subprocess.run([os.path.join(unittest_path, "tonic_unittests.exe"),
                        "--gtest_filter=-*TimeSensitiveTest*",
                        "--gtest_repeat=2", "--gtest_shuffle", ],
                       shell=True,
                       check=True)

    def on_error(self, error: Exception) -> None:
        pass

    def on_completed(self) -> None:
        pass


if __name__ == "__main__":
    build_subject = s.Subject()
    build_subject.pipe(
        ops.debounce(0.2)
    ).subscribe(BackPressure.DROP(ConsumerObserver(), 0))


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
