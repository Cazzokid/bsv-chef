import pytest
import unittest.mock as mock
from src.controllers.recipecontroller import RecipeController


@pytest.mark.unit
@pytest.fixture
def recipe_controller():
    mock_dao = mock.Mock()
    controller = RecipeController(mock_dao)
    return controller

@pytest.mark.unit
# Test 1: Zero min quality, returns +0 items. 
def test_zero_min_quantity(recipe_controller):
    recipe_controller.get_all = mock.Mock(return_value=[
        {"name": "sugar", "quantity": 2, "unit": "grams"},
        {"name": "flour", "quantity": 0, "unit": "grams"}
    ])

    result = recipe_controller.get_available_items(0)

    assert result == {"sugar": 2}

@pytest.mark.unit
# Test 2: Nagative min quality, returns all items. 
def test_negative_min_quantity(recipe_controller):
    recipe_controller.get_all = mock.Mock(return_value=[
        {"name": "sugar", "quantity": 2, "unit": "grams"},
        {"name": "flour", "quantity": 0, "unit": "grams"}
    ])

    result = recipe_controller.get_available_items(-1)

    assert result == {"sugar": 2, "flour": 0}

@pytest.mark.unit
# Test 3: Positive min quality, returns only items with quantity above min quality.
def test_positive_min_quantity(recipe_controller):
    recipe_controller.get_all = mock.Mock(return_value=[
        {"name": "sugar", "quantity": 2, "unit": "grams"},
        {"name": "flour", "quantity": 5, "unit": "grams"},
        {"name": "salt", "quantity": 1, "unit": "grams"}
    ])

    result = recipe_controller.get_available_items(2)

    assert result == {"sugar": 2, "flour": 5}

@pytest.mark.unit
# Test 4: Empty pantry, returns no items.
def test_get_all_throws_exception(recipe_controller):
    recipe_controller.get_all = mock.Mock(side_effect=Exception("Database error"))

    result = recipe_controller.get_available_items(-1)

    assert result is None
