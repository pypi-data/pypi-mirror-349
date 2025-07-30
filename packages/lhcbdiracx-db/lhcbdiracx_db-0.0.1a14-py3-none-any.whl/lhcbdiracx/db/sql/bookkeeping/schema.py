from diracx.db.sql.utils import Column
from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Configuration(Base):
    __tablename__ = "configurations"

    configurationid = Column(Integer, primary_key=True)
    configname = Column(String(128), nullable=False)
    configversion = Column(String(128), nullable=False)

    __table_args__ = (
        UniqueConstraint("configname", "configversion", name="configuration_uk"),
    )
