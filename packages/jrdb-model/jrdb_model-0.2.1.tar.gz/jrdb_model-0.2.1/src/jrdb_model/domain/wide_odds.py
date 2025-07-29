from ..sessioncontroll import (
    baseobj,
    colobj,
    fkyobj,
    intobj,
    jsonobj,
    strobj,
)


class WideOddsData(baseobj):
    __tablename__ = "wide_odds"
    racekey = colobj(strobj, fkyobj("bangumi.racekey"), primary_key=True)
    data_kbn = colobj(intobj)
    registered_horses = colobj(intobj)
    ran_horses = colobj(intobj)
    sold_flg = colobj(intobj)
    all_odds = colobj(jsonobj)
    sum_of_all_bought_count = colobj(intobj)
