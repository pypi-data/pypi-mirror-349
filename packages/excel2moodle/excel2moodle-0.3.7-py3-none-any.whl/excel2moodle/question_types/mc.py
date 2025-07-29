"""Multiple choice Question implementation."""

from typing import ClassVar

import lxml.etree as ET

import excel2moodle.core.etHelpers as eth
from excel2moodle.core import stringHelpers
from excel2moodle.core.globals import (
    DFIndex,
    TextElements,
    XMLTags,
    feedbackStr,
)
from excel2moodle.core.parser import QuestionParser
from excel2moodle.core.question import Question


class MCQuestion(Question):
    """Multiple-choice Question Implementation."""

    standardTags: ClassVar[dict[str, str | float]] = {
        "single": "false",
        "shuffleanswers": "true",
        "answernumbering": "abc",
        "showstandardinstruction": "0",
        "shownumcorrect": "",
    }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class MCQuestionParser(QuestionParser):
    """Parser for the multiple choice Question."""

    def __init__(self) -> None:
        super().__init__()
        self.genFeedbacks = [
            XMLTags.CORFEEDB,
            XMLTags.PCORFEEDB,
            XMLTags.INCORFEEDB,
        ]

    def getAnsElementsList(
        self,
        answerList: list,
        fraction: float = 50,
        format="html",
    ) -> list[ET.Element]:
        elementList: list[ET.Element] = []
        for ans in answerList:
            p = TextElements.PLEFT.create()
            p.text = str(ans)
            text = eth.getCdatTxtElement(p)
            elementList.append(
                ET.Element(XMLTags.ANSWER, fraction=str(fraction), format=format),
            )
            elementList[-1].append(text)
            if fraction < 0:
                elementList[-1].append(
                    eth.getFeedBEle(
                        XMLTags.ANSFEEDBACK,
                        text=feedbackStr["wrong"],
                        style=TextElements.SPANRED,
                    ),
                )
            elif fraction > 0:
                elementList[-1].append(
                    eth.getFeedBEle(
                        XMLTags.ANSFEEDBACK,
                        text=feedbackStr["right"],
                        style=TextElements.SPANGREEN,
                    ),
                )
        return elementList

    def setAnswers(self) -> list[ET.Element]:
        ansStyle = self.rawInput[DFIndex.ANSTYPE]
        true = stringHelpers.getListFromStr(self.rawInput[DFIndex.TRUE])
        trueAnsList = stringHelpers.texWrapper(true, style=ansStyle)
        self.logger.debug(f"got the following true answers \n {trueAnsList=}")
        false = stringHelpers.getListFromStr(self.rawInput[DFIndex.FALSE])
        falseAnsList = stringHelpers.texWrapper(false, style=ansStyle)
        self.logger.debug(f"got the following false answers \n {falseAnsList=}")
        truefrac = 1 / len(trueAnsList) * 100
        falsefrac = 1 / len(trueAnsList) * (-100)
        self.tmpEle.find(XMLTags.PENALTY).text = str(round(truefrac / 100, 4))
        ansList = self.getAnsElementsList(trueAnsList, fraction=round(truefrac, 4))
        ansList.extend(
            self.getAnsElementsList(falseAnsList, fraction=round(falsefrac, 4)),
        )
        return ansList
