import base64
import logging
import re
import typing
from pathlib import Path
from re import Match

import lxml.etree as ET

from excel2moodle.core import etHelpers
from excel2moodle.core.category import Category
from excel2moodle.core.exceptions import QNotParsedException
from excel2moodle.core.globals import (
    DFIndex,
    TextElements,
    XMLTags,
    questionTypes,
)
from excel2moodle.logger import LogAdapterQuestionID

loggerObj = logging.getLogger(__name__)


class Question:
    standardTags: typing.ClassVar[dict[str, str | float]] = {
        "hidden": 0,
    }

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        subclassTags = getattr(cls, "standartTags", {})
        superclassTags = super(cls, cls).standardTags
        mergedTags = superclassTags.copy()
        mergedTags.update(subclassTags)
        cls.standardTags = mergedTags

    @classmethod
    def addStandardTags(cls, key, value) -> None:
        cls.standardTags[key] = value

    def __init__(
        self,
        category: Category,
        rawData: dict[str, float | str | int | list[str]],
        parent=None,
        points: float = 0,
    ) -> None:
        self.rawData = rawData
        self.category = category
        self.katName = self.category.name
        self.name: str = self.rawData.get(DFIndex.NAME)
        self.number: int = self.rawData.get(DFIndex.NUMBER)
        self.parent = parent
        self.qtype: str = self.rawData.get(DFIndex.TYPE)
        self.moodleType = questionTypes[self.qtype]
        self.points = points if points != 0 else self.category.points
        self.element: ET.Element | None = None
        self.picture: Picture
        self.id: str
        self.qtextParagraphs: list[ET.Element] = []
        self.bulletList: ET.Element | None = None
        self.answerVariants: list[ET.Element] = []
        self.variants: int | None = None
        self.variables: dict[str, list[float | int]] = {}
        self.setID()
        self.logger = LogAdapterQuestionID(loggerObj, {"qID": self.id})
        self.logger.debug("Sucess initializing")

    def __repr__(self) -> str:
        li: list[str] = []
        li.append(f"Question v{self.category.version}")
        li.append(f"{self.id=}")
        li.append(f"{self.parent=}")
        return "\n".join(li)

    def assemble(self, variant: int = 1) -> None:
        textElements: list[ET.Element] = []
        textElements.extend(self.qtextParagraphs)
        self.logger.debug("Starting assembly")
        if self.element is not None:
            mainText = self.element.find(XMLTags.QTEXT)
            self.logger.debug(f"found existing Text in element {mainText=}")
            txtele = mainText.find("text")
            if txtele is not None:
                mainText.remove(txtele)
                self.logger.debug("removed previously existing questiontext")
        else:
            msg = "Cant assamble, if element is none"
            raise QNotParsedException(msg, self.id)
        if self.variants is not None:
            textElements.append(self.getBPointVariant(variant - 1))
        elif self.bulletList is not None:
            textElements.append(self.bulletList)
        if hasattr(self, "picture") and self.picture.ready:
            textElements.append(self.picture.htmlTag)
            mainText.append(self.picture.element)
        mainText.append(etHelpers.getCdatTxtElement(textElements))
        # self.element.insert(3, mainText)
        self.logger.debug("inserted MainText to element")
        if len(self.answerVariants) > 0:
            ans = self.element.find(XMLTags.ANSWER)
            if ans is not None:
                self.element.remove(ans)
                self.logger.debug("removed previous answer element")
            self.element.insert(5, self.answerVariants[variant - 1])

    def setID(self, id=0) -> None:
        if id == 0:
            self.id: str = f"{self.category.id}{self.number:02d}"
        else:
            self.id: str = str(id)

    def getBPointVariant(self, variant: int) -> ET.Element:
        if self.bulletList is None:
            return None
        # matches {a}, {some_var}, etc.
        varPlaceholder = re.compile(r"{(\w+)}")

        def replaceMatch(match: Match[str]) -> str | int | float:
            key = match.group(1)
            if key in self.variables:
                value = self.variables[key][variant]
                return f"{value}".replace(".", ",\\!")
            return match.group(0)  # keep original if no match

        unorderedList = TextElements.ULIST.create()
        for li in self.bulletList:
            listItemText = li.text or ""
            bullet = TextElements.LISTITEM.create()
            bullet.text = varPlaceholder.sub(replaceMatch, listItemText)
            self.logger.debug(f"Inserted Variables into List: {bullet}")
            unorderedList.append(bullet)
        return unorderedList


class Picture:
    def __init__(self, picKey: str, imgFolder: Path, question: Question) -> None:
        self.pic = picKey
        self.ready: bool = False
        self.question = question
        self.logger = LogAdapterQuestionID(loggerObj, {"qID": self.question.id})
        self.imgFolder = (imgFolder / question.katName).resolve()
        self.htmlTag: ET.Element
        self.path: Path
        self._setPath()
        if hasattr(self, "picID"):
            self.ready = self.__getImg()

    def _setPath(self) -> None:
        if self.pic == 1:
            self.picID = self.question.id
        else:
            selectedPic = self.pic[2:]
            self.logger.debug("Got the picture key: %s", selectedPic)
            try:
                self.picID = f"{self.question.category.id}{int(selectedPic):02d}"
            except ValueError as e:
                self.logger.warning(
                    msg=f"Bild-ID konnte aus dem Key: {self.pic} nicht festgestellt werden",
                    exc_info=e,
                )

    def _getBase64Img(self, imgPath):
        with open(imgPath, "rb") as img:
            return base64.b64encode(img.read()).decode("utf-8")

    def _setImgElement(self, dir: Path, picID: int) -> None:
        """Gibt das Bild im dirPath mit dir qID als base64 encodiert mit den entsprechenden XML-Tags zurück."""
        self.path: Path = (dir / str(picID)).with_suffix(".svg")
        self.element: ET.Element = ET.Element(
            "file",
            name=f"{self.path.name}",
            path="/",
            encoding="base64",
        )
        self.element.text = self._getBase64Img(self.path)

    def __getImg(self) -> bool:
        try:
            self._setImgElement(self.imgFolder, int(self.picID))
            self.htmlTag = ET.Element(
                "img",
                src=f"@@PLUGINFILE@@/{self.path.name}",
                alt=f"Bild {self.path.name}",
                width="500",
            )
            return True
        except FileNotFoundError as e:
            self.logger.warning(
                msg=f"Bild {self.picID} konnte nicht gefunden werden ",
                exc_info=e,
            )
            self.element = None
            return False
