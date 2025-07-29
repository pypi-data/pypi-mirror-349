from ..sessioncontroll import (
    baseobj,
    colobj,
    fkyobj,
    jsonobj,
    strobj,
)


class PredictRaceData(baseobj):
    __tablename__ = "predict_race"
    racekey = colobj(strobj, fkyobj("bangumi.racekey"), primary_key=True)
    umaren = colobj(jsonobj)
    wide = colobj(jsonobj)
    wakuren = colobj(jsonobj)
