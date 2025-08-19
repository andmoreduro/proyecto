import os

from PyQt6.QtCore import QFileSystemWatcher, QPointF, QTimer
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from globals import output_path


class OutputSection(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.pdf_viewer = PDFViewer(output_path)

        layout.addWidget(self.pdf_viewer)


class PDFViewerViewState:
    def __init__(self, page: int, location: QPointF, zoom: float):
        self.page = page
        self.location = location
        self.zoom = zoom


class PDFViewer(QWidget):
    def __init__(self, pdf_path: str):
        super().__init__()

        self.pending_view_state = None
        self.pdf_path = pdf_path

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.document = QPdfDocument(self)
        self.pdf_view = QPdfView(self)
        self.pdf_view.setDocument(self.document)
        self.pdf_view.setPageMode(QPdfView.PageMode.MultiPage)

        layout.addWidget(self.pdf_view)

        self.document.statusChanged.connect(self._on_document_status_changed)

        self.reload_timer = QTimer(self)
        self.reload_timer.setSingleShot(True)
        self.reload_timer.timeout.connect(self._on_file_changed)

        self.file_watcher = QFileSystemWatcher(self)
        self.setup_file_watching()

        self.load_document_if_exists()

    def _delay_on_file_changed(self, path):
        self.reload_timer.stop()
        self.reload_timer.start(100)

    def _on_file_changed(self):
        try:
            if os.path.exists(self.pdf_path):
                # Ensure we're watching the file (not just directory)
                if self.pdf_path not in self.file_watcher.files():
                    # Remove directory watching if we were doing that
                    directory = os.path.dirname(self.pdf_path)
                    if directory in self.file_watcher.directories():
                        self.file_watcher.removePath(directory)
                    # Add file watching
                    self.file_watcher.addPath(self.pdf_path)

                # Save current view state
                self.pending_view_state = self.get_view_state()

                # Reload the document
                self.document.load(self.pdf_path)
            else:
                # File was deleted - switch back to directory watching
                self.setup_file_watching()
                # Clear the document
                self.document.close()
        except Exception as e:
            print(f"Error reloading PDF: {e}")

    def _on_directory_changed(self, directory):
        if os.path.exists(self.pdf_path):
            # File was created - switch from directory watching to file watching
            self.file_watcher.removePath(directory)
            self.file_watcher.addPath(self.pdf_path)
            # Load the newly created file
            self._delay_on_file_changed(self.pdf_path)

    def _on_document_status_changed(self, status):
        if status == QPdfDocument.Status.Ready and self.pending_view_state:
            self.restore_view_state(self.pending_view_state)
            self.pending_view_state = None

    def setup_file_watching(self):
        if os.path.exists(self.pdf_path):
            # File exists - watch it directly
            if self.pdf_path not in self.file_watcher.files():
                self.file_watcher.addPath(self.pdf_path)
        else:
            # File doesn't exist - watch the directory instead
            directory = os.path.dirname(self.pdf_path)
            if (
                os.path.exists(directory)
                and directory not in self.file_watcher.directories()
            ):
                self.file_watcher.addPath(directory)

        # Connect to both file and directory change signals
        self.file_watcher.fileChanged.connect(self._delay_on_file_changed)
        self.file_watcher.directoryChanged.connect(self._on_directory_changed)

    def load_document_if_exists(self):
        if os.path.exists(self.pdf_path):
            self.document.load(self.pdf_path)
        else:
            # Clear the document to show blank state
            self.document.close()

    def get_view_state(self) -> PDFViewerViewState:
        navigator = self.pdf_view.pageNavigator()
        if navigator is None:
            return PDFViewerViewState(0, QPointF(0, 0), 1.0)
        current_view_state = PDFViewerViewState(
            navigator.currentPage(),
            navigator.currentLocation(),
            navigator.currentZoom(),
        )
        return current_view_state

    def restore_view_state(self, state: PDFViewerViewState):
        navigator = self.pdf_view.pageNavigator()
        if navigator is None:
            return PDFViewerViewState(0, QPointF(0, 0), 1.0)
        navigator.jump(state.page, state.location, state.zoom)
