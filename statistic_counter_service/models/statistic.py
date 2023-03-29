from decimal import Decimal

from sqlalchemy import Column, BigInteger, CheckConstraint, Integer, DECIMAL, Date
from sqlalchemy import case, and_
from sqlalchemy.ext.hybrid import hybrid_property

from .base import Base


class Statistic(Base):
    __tablename__ = "statistic"
    __table_args__ = (
        CheckConstraint("views >= 0"),
        CheckConstraint("clicks >= 0"),
        CheckConstraint("cost >= 0"),
    )

    id = Column(BigInteger, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    views = Column(Integer)
    clicks = Column(Integer)
    cost = Column(DECIMAL(7, 2))

    @hybrid_property
    def cpc(self) -> Decimal:
        """cost/clicks (средняя стоимость клика)"""
        if self.cost is None or self.clicks == 0:
            return Decimal(0)

        return Decimal(self.cost / self.clicks)

    @cpc.expression
    def cpc(cls):
        return case((and_(cls.cost > 0, cls.clicks > 0), cls.cost / cls.clicks),
                    else_=0.0)

    @hybrid_property
    def cpm(self) -> Decimal:
        """cost/views * 1000 (средняя стоимость 1000 показов)"""
        if self.cost is None or self.views == 0:
            return Decimal(0)

        return Decimal(self.cost / self.views * 1000)

    @cpm.expression
    def cpm(cls):
        return case((and_(cls.cost > 0, cls.views > 0), cls.cost / cls.views * 1000),
                    else_=0.0)
