from jvcore import Communicator, SkillBase
from .currtime import CurrTimeSkill


def getSkill(communicator: Communicator) -> SkillBase:
    return CurrTimeSkill(communicator)

def test(comm: Communicator):
    skill = getSkill(comm)
    skill.getDate('')