# coding: utf-8
from sqlalchemy import Column, Date, JSON, String, Table
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata



class LEI(Base):
    __tablename__ = 'LEIS'

    LEI = Column(String(20, 'utf32_bin'), primary_key=True, comment='20位LEI码')
    Entity = Column(JSON, comment='主体信息')
    Registration = Column(JSON, comment='注册机构信息')
    Extension = Column(JSON, comment='其他信息')




