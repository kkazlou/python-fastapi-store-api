from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from myapp.database import Base

store_item_association = Table(
    "store_item",
    Base.metadata,
    Column("store_id", Integer, ForeignKey("stores.id"), primary_key=True),
    Column("item_id", Integer, ForeignKey("items.id"), primary_key=True),
)

item_tag_association = Table(
    "item_tag",
    Base.metadata,
    Column("item_id", Integer, ForeignKey("items.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    items = relationship(
        "Item", secondary=store_item_association, back_populates="stores"
    )


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    stores = relationship(
        "Store", secondary=store_item_association, back_populates="items"
    )
    tags = relationship("Tag", secondary=item_tag_association, back_populates="items")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    items = relationship("Item", secondary=item_tag_association, back_populates="tags")
