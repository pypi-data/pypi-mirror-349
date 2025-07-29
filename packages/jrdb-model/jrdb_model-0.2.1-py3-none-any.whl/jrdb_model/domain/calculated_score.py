from ..sessioncontroll import baseobj, colobj, fkyobj, floatobj, strobj


class CalculatedScoreData(baseobj):
    __tablename__ = "calculated_score"
    racehorsekey = colobj(strobj, fkyobj("racehorse.racehorsekey"), primary_key=True)
    waku_win_rate = colobj(floatobj)
    waku_rentai_rate = colobj(floatobj)
