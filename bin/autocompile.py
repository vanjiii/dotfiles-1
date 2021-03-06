#!/usr/bin/env python
#
# Usage:
#   ./autocompile.py path ext1,ext2,extn cmd
#
# Blocks monitoring |path| and its subdirectories for modifications on
# files ending with suffix |extk|. Run |cmd| each time a modification
# is detected. |cmd| is optional and defaults to 'make'.
#
# Example:
#   ./autocompile.py /my-latex-document-dir .tex,.bib "make pdf"
#
import subprocess
import sys

import pyinotify


class OnWriteHandler(pyinotify.ProcessEvent):
    def my_init(self, cwd, extension, cmd):
        self.cwd = cwd
        self.extensions = extension.split(',')
        self.cmd = cmd

    def _run_cmd(self):
        print('==> Modification detected')
        subprocess.call(self.cmd.split(' '), cwd=self.cwd)

    def process_IN_CLOSE_WRITE(self, event):
        if all(not event.pathname.endswith(ext) for ext in self.extensions):
            return
        self._run_cmd()


def auto_compile(path, extension, cmd):
    wm = pyinotify.WatchManager()
    handler = OnWriteHandler(cwd=path, extension=extension, cmd=cmd)
    notifier = pyinotify.Notifier(wm, default_proc_fun=handler)
    wm.add_watch(path, pyinotify.IN_CLOSE_WRITE, rec=True, auto_add=True)
    print('==> Start monitoring %s (type c^c to exit)' % path)
    notifier.loop(clear_burst)


def clear_burst(notifier):
    if notifier.check_events(timeout=10):
        notifier.read_events()

    notifier._eventq.clear()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Command line error: missing argument(s).", file=sys.stderr)
        sys.exit(1)

    # Required arguments
    path = sys.argv[1]
    extension = sys.argv[2]

    # Optional argument
    cmd = 'make'
    if len(sys.argv) == 4:
        cmd = sys.argv[3]

    # Blocks monitoring
    auto_compile(path, extension, cmd)
