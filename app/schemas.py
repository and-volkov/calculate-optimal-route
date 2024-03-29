from typing import List

from pydantic import BaseModel


class Point(BaseModel):
    lat: float
    lng: float


class Route(BaseModel):
    id: int
    points: List[Point]


class RouteCreate(BaseModel):
    points: List[Point]

    @classmethod
    def __init__(cls, **values):
        if "points" not in values or not values["points"]:
            raise ValueError("Points list must not be empty")
        super().__init__(**values)

    @staticmethod
    def validate_points(cls, v):
        for point in v:
            if (
                not isinstance(point, dict)
                or "lat" not in point
                or "lng" not in point
            ):
                raise ValueError(
                    "Each point must have 'lat' and 'lng' attributes"
                )
        return v
