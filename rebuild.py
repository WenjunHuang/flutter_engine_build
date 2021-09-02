import os
import shutil
import subprocess
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler
import rx
from rx import operators as ops
from rx import subject as s


if __name__ == "__main__":
    build_subject = s.Subject()
    build_subject.pipe(
        ops.debounce(0.2)
    ).subscribe(lambda value: rebuild())
    def on_created(event):
        print(f"{event.src_path} has been created!")
        build_subject.on_next(1)

    def on_deleted(event):
        print(f"Someone deleted {event.src_path}!")
        build_subject.on_next(1)

    def on_modified(event):
        print(f"{event.src_path} has been modified")
        build_subject.on_next(1)

    # def on_moved(event):
    #     print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")

    def rebuild():
        engine_path = os.path.join(os.getcwd(),"engine")
        depot_tools_path = os.path.join(os.getcwd(),"depot_tools")
        subprocess.run([os.path.join(depot_tools_path,"ninja.exe"),"-C",os.path.join(engine_path,"src","out","win_debug_unopt")])

        unittest_path = os.path.join(engine_path,"src","out","host_debug_unopt")
        subprocess.run([os.path.join(unittest_path,"fml_unittests.exe"),"--gtest_filter=RefCountedTest.*:-*TimeSensitiveTest*","--gtest_repeat=2","--gtest_shuffle"])

    patterns= ["*.c","*.cc","*.h"]
    event_handler= PatternMatchingEventHandler(patterns,None,False,True)
    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    # event_handler.on_moved = on_moved


    engine_path = os.path.join(os.getcwd(),"engine","src")
    observer = Observer()
    observer.schedule(event_handler, engine_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()


