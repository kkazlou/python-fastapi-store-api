from sqlalchemy.orm import Session
from myapp import models, schemas


def create_store(db: Session, store: schemas.StoreCreate):
    db_store = models.Store(name=store.name)
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_stores(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Store).offset(skip).limit(limit).all()


def get_store(db: Session, store_id: int):
    return db.query(models.Store).filter(models.Store.id == store_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_tags(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Tag).offset(skip).limit(limit).all()


def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()


def add_item_to_store(db: Session, store_id: int, item_id: int):
    store = db.query(models.Store).filter(models.Store.id == store_id).first()
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not store or not item:
        return None
    store.items.append(item)
    db.commit()
    return store


def add_tag_to_item(db: Session, item_id: int, tag_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not item or not tag:
        return None
    if tag not in item.tags:
        item.tags.append(tag)
        db.commit()
        db.refresh(item)
    return item


def remove_item_from_store(db: Session, store_id: int, item_id: int):
    store = db.query(models.Store).filter(models.Store.id == store_id).first()
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not store or not item:
        return None
    store.items.remove(item)
    db.commit()
    return store


def remove_tag_from_item(db: Session, item_id: int, tag_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not item or not tag:
        return None
    if tag in item.tags:
        item.tags.remove(tag)
        db.commit()
        db.refresh(item)
    return item


def update_store(db: Session, store_id: int, store: schemas.StoreCreate):
    db_store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if db_store:
        db_store.name = store.name
        db.commit()
        db.refresh(db_store)
    return db_store


def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db_item.name = item.name
        db.commit()
        db.refresh(db_item)
    return db_item


def update_tag(db: Session, tag_id: int, tag: schemas.TagCreate):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if db_tag:
        db_tag.name = tag.name
        db.commit()
        db.refresh(db_tag)
    return db_tag


def delete_store(db: Session, store_id: int):
    db_store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if db_store:
        db.delete(db_store)
        db.commit()
    return db_store


def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item


def delete_tag(db: Session, tag_id: int):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if db_tag:
        db.delete(db_tag)
        db.commit()
    return db_tag
