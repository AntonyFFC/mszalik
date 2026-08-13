import os
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from htmltopdf import save_html_as_pdf

WATCH_DIR = os.path.dirname(os.path.abspath(__file__))
DEBOUNCE_SECONDS = 1.0


class HtmlChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self._last_run = {}

    def on_modified(self, event):
        self._handle(event)

    def on_created(self, event):
        self._handle(event)

    def _handle(self, event):
        if event.is_directory:
            return
        path = event.src_path
        if not path.lower().endswith(".html"):
            return

        name = os.path.basename(path)
        stem, _ = os.path.splitext(name)
        if not stem.isdigit():
            return

        now = time.time()
        if now - self._last_run.get(name, 0) < DEBOUNCE_SECONDS:
            return
        self._last_run[name] = now

        pdf_name = f"{stem}.pdf"
        print(f"[watch] {name} changed -> rendering {pdf_name} ...", flush=True)
        try:
            save_html_as_pdf(name, pdf_name)
        except Exception as exc:
            print(f"[watch] FAILED to render {name}: {exc}", flush=True)


def main():
    handler = HtmlChangeHandler()
    observer = Observer()
    observer.schedule(handler, WATCH_DIR, recursive=False)
    observer.start()
    print(f"[watch] Watching {WATCH_DIR} for changes to N.html files. Ctrl+C to stop.", flush=True)
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
