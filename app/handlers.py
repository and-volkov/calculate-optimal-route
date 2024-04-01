import csv
import logging
import math
from io import StringIO

from fastapi import HTTPException, UploadFile

logger = logging.getLogger(__name__)


class TSPHandler:
    def __init__(self, file: UploadFile):
        self.file = file

    def read_coordinates_from_csv(self) -> list[dict[str, float]]:
        """
        Read coordinates from a CSV file and return a list of dictionaries

        Args:
            file: A file object

        Returns:
            A list of dictionaries with "lat" and "lng" keys
        """
        coordinates = []
        content = self.file.file.read()
        buffer = StringIO(content.decode("utf-8"))
        reader = csv.DictReader(buffer)
        for row in reader:
            try:
                coordinates.append(
                    {"lat": float(row["lat"]), "lng": float(row["lng"])}
                )
            except KeyError:
                logger.error(
                    f"Invalid keys in CSV file, {self.file.filename} "
                )
        self.file.file.close()
        return coordinates

    def distance(
        self, coord1: dict[str, float], coord2: dict[str, float]
    ) -> float:
        """
        Calculate the Euclidean distance between two coordinates

        Args:
            coord1: A dictionary with "lat" and "lng" keys
            coord2: A dictionary with "lat" and "lng" keys

        Return:
            The Euclidean distance between the two coordinates
        """
        return math.sqrt(
            (coord1["lat"] - coord2["lat"]) ** 2
            + (coord1["lng"] - coord2["lng"]) ** 2
        )

    def nearest_neighbor(self, coordinates) -> list[int]:
        """
        Find the nearest neighbor of each coordinate

        Args:
            coords: A list of dictionaries with "lat" and "lng" keys

        Return:
            A list of indexes representing the optimal path
        """
        unvisited = set(range(len(coordinates)))
        current_point = 0  # Start from the first point
        path = [current_point]
        unvisited.remove(current_point)

        while unvisited:
            nearest_point = min(
                unvisited,
                key=lambda x: self.distance(
                    coordinates[current_point], coordinates[x]
                ),
            )
            path.append(nearest_point)
            unvisited.remove(nearest_point)
            current_point = nearest_point

        return path

    def sort_coordinates(
        self, coordinates: list[dict[str, float]]
    ) -> list[dict[str, float]]:
        """
        Sort a list of coordinates by latitude and longitude

        Args:
        A list of indexes representing the optimal path

        Returns:
        A sorted list of dictionaries
        """
        optimal_path = self.nearest_neighbor(coordinates)
        return [coordinates[i] for i in optimal_path]

    def process(self) -> list[dict[str, float]]:
        """
        Process the uploaded file and return a sorted list of coordinates
        """
        try:
            coordinates = self.read_coordinates_from_csv()
            return self.sort_coordinates(coordinates)
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=500, detail="Internal Server Error"
            )
