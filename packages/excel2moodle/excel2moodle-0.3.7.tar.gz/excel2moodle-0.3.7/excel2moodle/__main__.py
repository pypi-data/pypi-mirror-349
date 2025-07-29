"""Main Function to make the Package executable."""

import signal

from PySide6 import QtWidgets, sys

from excel2moodle import e2mMetadata, mainLogger
from excel2moodle.core import dataStructure
from excel2moodle.ui import appUi as ui
from excel2moodle.ui.settings import Settings


def main() -> None:
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtWidgets.QApplication(sys.argv)
    settings = Settings()
    database: dataStructure.QuestionDB = dataStructure.QuestionDB(settings)
    window = ui.MainWindow(settings, database)
    database.window = window
    window.show()
    for k, v in e2mMetadata.items():
        msg = f"{k:^14s}:  {v}"
        mainLogger.info(msg)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
