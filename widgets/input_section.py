from PyQt6.QtCore import QProcess, QTimer
from PyQt6.QtWidgets import QSizePolicy, QSpacerItem, QVBoxLayout, QWidget

from globals import (
    default_affiliation,
    default_author,
    default_course,
    default_instructor,
    default_title,
    input_path,
    typst_process_arguments,
    typst_process_name,
)
from system import write_to_file
from typst import TypstCoverPage, TypstDocument, TypstSections
from widgets.core import MultiLineTextInputGroup, SingleLineTextInputGroup


class CoverPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setLayout(QVBoxLayout())

        self.title_input_group = SingleLineTextInputGroup("Title", default_title)
        self.author_input_group = SingleLineTextInputGroup("Author", default_author)
        self.affiliation_input_group = SingleLineTextInputGroup(
            "Affiliation", default_affiliation
        )
        self.course_input_group = SingleLineTextInputGroup("Course", default_course)
        self.instructor_input_group = SingleLineTextInputGroup(
            "Instructor", default_instructor
        )

        self.layout().addWidget(self.title_input_group)
        self.layout().addWidget(self.author_input_group)
        self.layout().addWidget(self.affiliation_input_group)
        self.layout().addWidget(self.course_input_group)
        self.layout().addWidget(self.instructor_input_group)

        self.layout().addItem(
            QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        self.title_input_group.input.textChanged.connect(self._on_title_input_changed)
        self.author_input_group.input.textChanged.connect(self._on_author_input_changed)
        self.affiliation_input_group.input.textChanged.connect(
            self._on_affiliation_input_changed
        )
        self.course_input_group.input.textChanged.connect(self._on_course_input_changed)
        self.instructor_input_group.input.textChanged.connect(
            self._on_instructor_input_changed
        )

        self.typst_cover_page = TypstCoverPage()

    def _on_title_input_changed(self, text):
        self.typst_cover_page.set_title(text)
        self.parent()._delay_update_typst_file()

    def _on_author_input_changed(self, text):
        self.typst_cover_page.set_author(text)
        self.parent()._delay_update_typst_file()

    def _on_affiliation_input_changed(self, text):
        self.typst_cover_page.set_affiliation(text)
        self.parent()._delay_update_typst_file()

    def _on_course_input_changed(self, text):
        self.typst_cover_page.set_course(text)
        self.parent()._delay_update_typst_file()

    def _on_instructor_input_changed(self, text):
        self.typst_cover_page.set_instructor(text)
        self.parent()._delay_update_typst_file()


class Sections(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setLayout(QVBoxLayout())

        self.section_input_group = MultiLineTextInputGroup(
            "Content", "Write here whatever you need to write."
        )

        self.layout().addWidget(self.section_input_group)

        self.layout().addItem(
            QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        self.section_input_group.input.textChanged.connect(
            self._on_content_input_changed
        )

        self.typst_sections = TypstSections()

    def _on_content_input_changed(self):
        text = self.section_input_group.input.toPlainText()
        self.typst_sections.set_content(text)
        self.parent()._delay_update_typst_file()


class InputSection(QWidget):
    def __init__(self):
        super().__init__()

        self.typst_process = QProcess(self)
        self.typst_process.setProgram(typst_process_name)
        self.typst_process.setArguments(typst_process_arguments)

        self.setLayout(QVBoxLayout())

        self.cover_page = CoverPage(self)
        self.sections = Sections(self)

        self.layout().addWidget(self.cover_page)
        self.layout().addWidget(self.sections)

        self.typst_document = TypstDocument(
            self.cover_page.typst_cover_page, self.sections.typst_sections
        )

        self.write_timer = QTimer(self)
        self.write_timer.setSingleShot(True)
        self.write_timer.timeout.connect(self._update_typst_file)

        self._update_typst_file()
        self.start_typst_watch()

    def _delay_update_typst_file(self):
        self.write_timer.stop()
        self.write_timer.start(100)

    def _update_typst_file(self):
        content = str(self.typst_document)
        write_to_file(input_path, content)

    def start_typst_watch(self):
        self.typst_process.start()
