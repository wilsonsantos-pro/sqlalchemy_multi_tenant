from sqlalchemy_multi_tenant import config


def test_sqlalchemy_uri() -> None:
    assert (
        config.settings.SQLALCHEMY_DATABASE_URI
        == "postgresql://wsp:abc123@localhost:54321/test"
    )
