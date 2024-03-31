#  type: ignore
from unittest.mock import Mock

import pytest

from app.handlers import TSPHandler


@pytest.fixture
def mock_file():
    # Mock an uploaded CSV file
    content = "lat,lng\n1,2\n3,4\n5,6\n"
    file = Mock()
    file.file.read.return_value = content.encode("utf-8")
    file.file.close.return_value = None
    return file


def test_read_coordinates_from_csv(mock_file):
    tsp_handler = TSPHandler(mock_file)
    expected_coordinates = [
        {"lat": 1.0, "lng": 2.0},
        {"lat": 3.0, "lng": 4.0},
        {"lat": 5.0, "lng": 6.0},
    ]
    assert tsp_handler.read_coordinates_from_csv() == expected_coordinates


def test_sort_coordinates():
    tsp_handler = TSPHandler(None)
    coordinates = [
        {"lat": 1, "lng": 2},
        {"lat": 5, "lng": 6},
        {"lat": 3, "lng": 4},
        {"lat": 7, "lng": 8},
    ]
    expected_sorted_coordinates = [
        {"lat": 1, "lng": 2},
        {"lat": 3, "lng": 4},
        {"lat": 5, "lng": 6},
        {"lat": 7, "lng": 8},
    ]
    assert (
        tsp_handler.sort_coordinates(coordinates)
        == expected_sorted_coordinates
    )


def test_distance():
    tsp_handler = TSPHandler(None)
    coord1 = {"lat": 1, "lng": 2}
    coord2 = {"lat": 4, "lng": 6}
    expected_distance = 5.0
    assert tsp_handler.distance(coord1, coord2) == expected_distance


def test_nearest_neighbor():
    tsp_handler = TSPHandler(None)
    coordinates = [
        {"lat": 1, "lng": 2},
        {"lat": 3, "lng": 4},
        {"lat": 5, "lng": 6},
    ]
    expected_optimal_path = [0, 1, 2]
    assert tsp_handler.nearest_neighbor(coordinates) == expected_optimal_path


def test_process(mock_file):
    tsp_handler = TSPHandler(mock_file)
    expected_sorted_coordinates = [
        {"lat": 1.0, "lng": 2.0},
        {"lat": 3.0, "lng": 4.0},
        {"lat": 5.0, "lng": 6.0},
    ]
    assert tsp_handler.process() == expected_sorted_coordinates
