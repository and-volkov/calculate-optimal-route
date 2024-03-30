from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import handlers, models


def create_route(db: Session, file) -> models.Route:
    tsp_handler = handlers.TSPHandler(file)
    points = tsp_handler.process()
    db_route = models.Route(points=points)
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route


def get_route(db: Session, route_id: int) -> models.Route:
    db_route = (
        db.query(models.Route).filter(models.Route.id == route_id).first()
    )
    if db_route is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Route not found"
        )
    return db_route
