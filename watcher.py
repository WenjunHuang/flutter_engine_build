import os
import subprocess
import sys
import argparse
import time
from settings import *
from rx import operators as ops
from rx import subject as s
from rxpy_backpressure import BackPressure
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class RebuildAndRunTestObserver(Observer):
    def __init__(self, unittest_name, filter):
        super().__init__()
        self.unittest_name = unittest_name
        self.filter = filter
        self.engine_path = os.path.join(os.getcwd(), "engine")
        self.source_path = os.path.join(self.engine_path,"src")
        self.output = os.path.join(self.engine_path, "src", "out", "host_debug_unopt")
        self.depot_tools_path = os.path.join(os.getcwd(), "depot_tools")
        self.is_win = sys.platform.startswith('win')

    def on_next(self, event):
        print(f"{event.src_path} has been modified")

        try:
            env = set_env(self.depot_tools_path, self.engine_path)
            # first recompile
            subprocess.run(
                [os.path.join(self.depot_tools_path, "ninja" + (".bat" if self.is_win else "")), "-C", self.output],
                cwd=self.source_path,
                check=True,
                env=env)

            # then run unit tests
            unittest_name = self.unittest_name
            pattern = self.filter
            subprocess.run([os.path.join(self.output, unittest_name + "_unittests" + (".exe" if self.is_win else "")),
                            "--gtest_filter=" + (f"*{pattern}*:" if pattern is not None else "")
                            + "-*TimeSensitiveTest*",
                            "--gtest_shuffle", ],
                           cwd=self.output,
                           check=True)
        except Exception as e:
            print(e)

    def on_error(self, error: Exception):
        print(error)

    def on_completed(self):
        pass


cmd_parser = argparse.ArgumentParser(description="Watch file change and run unittest")
cmd_parser.add_argument("test_name", type=str)
cmd_parser.add_argument("--filter", type=str, required=False)
args = cmd_parser.parse_args()

build_subject = s.Subject()
build_subject.pipe(
    ops.debounce(0.2)
).subscribe(BackPressure.DROP(RebuildAndRunTestObserver(args.test_name, args.filter), 1))


def on_created(event):
    build_subject.on_next(event)


def on_deleted(event):
    build_subject.on_next(event)


def on_modified(event):
    build_subject.on_next(event)


patterns = ["*.c", "*.cc", "*.cpp", "*.h", "*.gn", "*.dart"]
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
except Exception as err:
    print(Exception, err)
finally:
    observer.stop()
    observer.join()
