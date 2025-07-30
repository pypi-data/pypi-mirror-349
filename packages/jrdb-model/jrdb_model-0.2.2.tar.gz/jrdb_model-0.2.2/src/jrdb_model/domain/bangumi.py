from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from ..sessioncontroll import db


class BangumiData(db.Model):
    __tablename__ = "bangumi"
    racekey: Mapped[str] = mapped_column(primary_key=True)
    # 親に対して
    kaisaikey: Mapped[str] = mapped_column(ForeignKey("kaisai.kaisaikey"))
    # 子に対して
    racehorses: Mapped[List["RacehorseData"]] = relationship(
        "RacehorseData", backref=backref("bangumi"), innerjoin=True
    )

    # 1:1
    returninfo: Mapped[List["ReturninfoData"]] = relationship(
        "ReturninfoData", uselist=False, backref=backref("bangumi")
    )
    umaren_odds: Mapped[List["UmarenOddsData"]] = relationship(
        "UmarenOddsData", uselist=False, backref=backref("bangumi")
    )
    wide_odds: Mapped[List["WideOddsData"]] = relationship(
        "WideOddsData", uselist=False, backref=backref("bangumi")
    )
    wakuren_odds: Mapped[List["WakurenOddsData"]] = relationship(
        "WakurenOddsData", uselist=False, backref=backref("bangumi")
    )
    predict_race: Mapped[List["PredictRaceData"]] = relationship(
        "PredictRaceData", uselist=False, backref=backref("bangumi")
    )
    ymd: Mapped[str] = mapped_column()
    start_time: Mapped[str] = mapped_column()
    distance: Mapped[int] = mapped_column()
    tdscode: Mapped[int] = mapped_column()
    right_left: Mapped[int] = mapped_column()
    in_out: Mapped[int] = mapped_column()
    shubetsu: Mapped[int] = mapped_column()
    joken: Mapped[str] = mapped_column()
    kigo: Mapped[int] = mapped_column()
    horse_kind_joken: Mapped[int] = mapped_column()
    horse_sex_joken: Mapped[int] = mapped_column()
    inter_race_joken: Mapped[int] = mapped_column()
    juryo: Mapped[int] = mapped_column()
    grade: Mapped[int] = mapped_column()
    race_name: Mapped[str] = mapped_column()
    kai: Mapped[str] = mapped_column()
    num_of_all_horse: Mapped[int] = mapped_column()
    course: Mapped[int] = mapped_column()
    kaisai_kbn: Mapped[int] = mapped_column()
    race_name_short: Mapped[str] = mapped_column()
    race_name_9char: Mapped[str] = mapped_column()
    data_kbn: Mapped[int] = mapped_column()
    money1st: Mapped[int] = mapped_column()
    money2nd: Mapped[int] = mapped_column()
    money3rd: Mapped[int] = mapped_column()
    money4th: Mapped[int] = mapped_column()
    money5th: Mapped[int] = mapped_column()
    sannyu_money1st: Mapped[int] = mapped_column()
    sannyu_money2nd: Mapped[int] = mapped_column()
    sellflg_tansho: Mapped[int] = mapped_column()
    sellflg_fukusho: Mapped[int] = mapped_column()
    sellflg_wakuren: Mapped[int] = mapped_column()
    sellflg_umaren: Mapped[int] = mapped_column()
    sellflg_umatan: Mapped[int] = mapped_column()
    sellflg_wide: Mapped[int] = mapped_column()
    sellflg_sanrenpuku: Mapped[int] = mapped_column()
    sellflg_sanrentan: Mapped[int] = mapped_column()
    yobi: Mapped[int] = mapped_column()
    win5flg: Mapped[int] = mapped_column()
