import csv
import heapq
import logging
import math
from io import StringIO

logger = logging.getLogger(__name__)


def read_coordinates_from_csv(file) -> list[dict[str, float]]:
    """
    Read coordinates from a CSV file and return a list of dictionaries

    Args:
        file: A file object

    Returns:
        A list of dictionaries with "lat" and "lng" keys
    """
    coordinates = []
    content = file.file.read()
    buffer = StringIO(content.decode("utf-8"))
    reader = csv.DictReader(buffer)
    for row in reader:
        try:
            coordinates.append(
                {"lat": float(row["lat"]), "lng": float(row["lng"])}
            )
        except KeyError:
            pass
    file.file.close()
    return coordinates


def sort_coordinates(
    coordinates: list[dict[str, str]],
) -> list[dict[str, str]]:
    """
    Sort a list of coordinates by latitude and longitude

    Args:
        coordinates: A list of dictionaries with "lat" and "lng" keys

    Returns:
        A sorted list of dictionaries
    """
    return nearest_neighbor(coordinates)


def distance(coord1, coord2):
    """
    Calculate the distance between two coordinates using the Haversine formula.
    """
    R = 6371  # Radius of the Earth in kilometers
    lat1, lon1 = coord1["lat"], coord1["lng"]
    lat2, lon2 = coord2["lat"], coord2["lng"]
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(
        math.radians(lat1)
    ) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def nearest_neighbor(coordinates):
    """
    Find the route using the nearest neighbor algorithm.
    """
    start_len = len(coordinates)
    unvisited = coordinates.copy()
    start_coord = unvisited.pop(0)
    route = [start_coord]
    heap = [(distance(start_coord, coord), coord) for coord in unvisited]
    heapq.heapify(heap)

    while heap:
        _, nearest = heapq.heappop(heap)
        route.append(nearest)
        try:
            unvisited.remove(nearest)
        except ValueError:
            continue

        if unvisited:
            for i, coord in enumerate(unvisited):
                heapq.heappushpop(heap, (distance(nearest, coord), coord))

    result_len = len(route)
    logger.info(f"Start length: {start_len}, result length: {result_len}")
    return route
