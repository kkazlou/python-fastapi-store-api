from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
from myapp import crud, models, schemas
from myapp.database import SessionLocal, engine
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import contextlib
from datetime import datetime
import time

models.Base.metadata.create_all(bind=engine)

# Create the APScheduler instance
scheduler = AsyncIOScheduler()


def periodic_task():
    print("Start Time:", datetime.now().time())
    time.sleep(70)
    print("End Time:", datetime.now().time())


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Add job and start the scheduler
    scheduler.add_job(periodic_task, "interval", minutes=1)
    scheduler.start()
    yield
    # Shutdown: Gracefully shutdown the scheduler
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/stores", response_model=schemas.StoreRead, tags=["stores"])
def create_store(store: schemas.StoreCreate, db: Session = Depends(get_db)):
    return crud.create_store(db=db, store=store)


@app.get("/stores", response_model=List[schemas.StoreRead], tags=["stores"])
def read_stores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_stores(db=db, skip=skip, limit=limit)


@app.put(
    "/stores/{store_id}",
    response_model=schemas.StoreRead,
    tags=["stores"],
)
def update_store(
    store_id: int, store: schemas.StoreCreate, db: Session = Depends(get_db)
):
    db_store = crud.update_store(db=db, store_id=store_id, store=store)
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")
    return db_store


@app.get("/stores/{store_id}", response_model=schemas.StoreRead, tags=["stores"])
def read_store(store_id: int, db: Session = Depends(get_db)):
    db_store = crud.get_store(db=db, store_id=store_id)
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")
    return db_store


@app.delete(
    "/stores/{store_id}",
    response_model=schemas.StoreRead,
    tags=["stores"],
)
def delete_store(store_id: int, db: Session = Depends(get_db)):
    db_store = crud.delete_store(db=db, store_id=store_id)
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")
    return db_store


@app.post("/items", response_model=schemas.ItemRead, tags=["items"])
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)


@app.get("/items", response_model=List[schemas.ItemRead], tags=["items"])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_items(db=db, skip=skip, limit=limit)


@app.put(
    "/items/{item_id}",
    response_model=schemas.ItemRead,
    tags=["items"],
)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.update_item(db=db, item_id=item_id, item=item)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.get("/items/{item_id}", response_model=schemas.ItemRead, tags=["items"])
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db=db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.delete(
    "/items/{item_id}",
    response_model=schemas.ItemRead,
    tags=["items"],
)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db=db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.post("/tags", response_model=schemas.TagRead, tags=["tags"])
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    return crud.create_tag(db=db, tag=tag)


@app.get("/tags", response_model=List[schemas.TagRead], tags=["tags"])
def read_tags(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_tags(db=db, skip=skip, limit=limit)


@app.put(
    "/tags/{tag_id}",
    response_model=schemas.TagRead,
    tags=["tags"],
)
def update_tag(tag_id: int, tag: schemas.TagCreate, db: Session = Depends(get_db)):
    db_tag = crud.update_tag(db=db, tag_id=tag_id, tag=tag)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@app.get("/tags/{tag_id}", response_model=schemas.TagRead, tags=["tags"])
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = crud.get_tag(db=db, tag_id=tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@app.delete(
    "/tags/{tag_id}",
    response_model=schemas.TagRead,
    tags=["tags"],
)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = crud.delete_tag(db=db, tag_id=tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@app.get("/import_stores", tags=["import"])
def import_stores(db: Session = Depends(get_db)):
    try:
        with open("stores.json", "r") as file:
            stores = json.load(file)

        for store_data in stores:
            store = schemas.StoreCreate(**store_data)
            crud.create_store(db=db, store=store)

        return {
            "status": "success",
            "message": "Stores imported successfully",
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="stores.json file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post(
    "/stores/{store_id}/items/{item_id}",
    response_model=schemas.StoreRead,
    tags=["stores"],
)
def add_item_to_store(store_id: int, item_id: int, db: Session = Depends(get_db)):
    store = crud.add_item_to_store(db=db, store_id=store_id, item_id=item_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store or Item not found")
    return store


@app.delete(
    "/stores/{store_id}/items/{item_id}",
    response_model=schemas.StoreRead,
    tags=["stores"],
)
def remove_item_from_store(store_id: int, item_id: int, db: Session = Depends(get_db)):
    return crud.remove_item_from_store(db=db, store_id=store_id, item_id=item_id)


@app.post(
    "/items/{item_id}/tags/{tag_id}",
    response_model=schemas.ItemRead,
    tags=["items"],
)
def add_tag_to_item(item_id: int, tag_id: int, db: Session = Depends(get_db)):
    item = crud.add_tag_to_item(db=db, item_id=item_id, tag_id=tag_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item or Tag not found")
    return item


@app.delete(
    "/items/{item_id}/tags/{tag_id}",
    response_model=schemas.ItemRead,
    tags=["items"],
)
def remove_tag_from_item(item_id: int, tag_id: int, db: Session = Depends(get_db)):
    item = crud.remove_tag_from_item(db=db, item_id=item_id, tag_id=tag_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item or Tag not found")
    return item
