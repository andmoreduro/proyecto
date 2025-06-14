from datetime import datetime

from globals import (
    default_affiliation,
    default_author,
    default_course,
    default_instructor,
    default_title,
)


class TypstCoverPage:
    def __init__(
        self,
        title: str = "",
        author: str = "",
        affiliation: str = "",
        course: str = "",
        instructor: str = "",
    ):
        self.set_title(title)
        self.set_author(author)
        self.set_affiliation(affiliation)
        self.set_course(course)
        self.set_instructor(instructor)

    def __str__(self) -> str:
        return f"""#import "versatile-apa/lib.typ": *

#show math.equation: set text(font: "STIX Two Math", size: 12pt)
#show raw: set text(font: "Fira Mono", size: 10pt)

#show: versatile-apa.with(
  title: [{self.__title}],
  authors: (
    (
      name: [{self.__author}],
      affiliations: ("{self.__affiliation}",),
    ),
  ),
  affiliations: (
    (
      name: [{self.__affiliation}],
      id: "{self.__affiliation}",
    ),
  ),
  course: [{self.__course}],
  instructor: [{self.__instructor}],
  due-date: [{datetime.now().date()}],
  font-family: "STIX Two Text",
  region: "co",
  language: "es",
  paper-size: "a4",
)
"""

    def set_title(self, title: str) -> None:
        self.__title = title if title != "" else default_title

    def set_author(self, author: str) -> None:
        self.__author = author if author != "" else default_author

    def set_affiliation(self, affiliation: str) -> None:
        self.__affiliation = affiliation if affiliation != "" else default_affiliation

    def set_course(self, course: str) -> None:
        self.__course = course if course != "" else default_course

    def set_instructor(self, instructor: str) -> None:
        self.__instructor = instructor if instructor != "" else default_instructor


class TypstSections:
    def __init__(self, content: str = ""):
        self.set_content(content)

    def __str__(self) -> str:
        return f"{self.__content}"

    def set_content(self, content) -> None:
        self.__content = content


class TypstDocument:
    def __init__(self, cover_page: TypstCoverPage, sections: TypstSections):
        self.cover_page = cover_page
        self.sections = sections

    def __str__(self) -> str:
        return f"""{self.cover_page}
{self.sections}
"""
