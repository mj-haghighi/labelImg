from typing import List
from ..caseModel import CaseModel
from ..SingletonMeta import SingletonMeta


class CaseRepository(metaclass=SingletonMeta):

    def __init__(self):
        self._nameToCase = {}

    @property
    def items(self) -> List[CaseModel]:
        """ all cases
        """
        return self._nameToCase.values()

    def getCase(self, name: str) -> CaseModel:
        """ Return case with 'name' if exist
        """
        if name not in self._nameToCase.keys():
            return None

        return self._nameToCase[name]

    def addCase(self, case: CaseModel):
        """ Add 'case' to repository
        """
        self._nameToCase[case.name] = case

    def clear(self):
        """ Clear repository
        """
        self._nameToCase = {}
