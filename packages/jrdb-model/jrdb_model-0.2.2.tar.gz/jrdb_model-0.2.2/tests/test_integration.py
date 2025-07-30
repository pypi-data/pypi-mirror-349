"""DBと接続する統合テスト."""


def test_kaisai():
    """開催データのジョインロードのテスト."""
    # import os
    from typing import List

    from sqlalchemy.orm import joinedload

    from jrdb_model import KaisaiData, create_app

    # os.environ["DB"] = mariadb+pymysql://user:pass@host/database
    app = create_app()
    with app.app_context():
        kaisais: List[KaisaiData] = (
            KaisaiData.query.filter(
                KaisaiData.ymd >= 20220101, KaisaiData.ymd <= 20220130
            )
            .options(joinedload("*"))
            .all()
        )
        assert len(kaisais) == 26
