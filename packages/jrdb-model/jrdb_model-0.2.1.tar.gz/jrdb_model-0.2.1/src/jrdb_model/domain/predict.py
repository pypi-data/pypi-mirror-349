from ..sessioncontroll import baseobj, colobj, fkyobj, floatobj, strobj


class PredictData(baseobj):
    __tablename__ = "predict"
    racehorsekey = colobj(strobj, fkyobj("racehorse.racehorsekey"), primary_key=True)
    pp_icchaku = colobj(floatobj)
    pp_nichaku = colobj(floatobj)
    pp_sanchaku = colobj(floatobj)
    rentai_rate = colobj(floatobj)
    fukusho_rate = colobj(floatobj)
    tansho_odds = colobj(floatobj)
    fukusho_odds = colobj(floatobj)
