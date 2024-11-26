import pandas as pd
import pytest
from langflow.schema.data import Data
from langflow.schema.data_set import DataSet


@pytest.fixture
def sample_data_objects() -> list[Data]:
    """Fixture providing a list of sample Data objects."""
    return [
        Data(data={"name": "John", "age": 30, "city": "New York"}),
        Data(data={"name": "Jane", "age": 25, "city": "Boston"}),
        Data(data={"name": "Bob", "age": 35, "city": "Chicago"}),
    ]


@pytest.fixture
def sample_dataset(sample_data_objects) -> DataSet:
    """Fixture providing a sample DataSet instance."""
    return DataSet.from_data_list(sample_data_objects)


def test_from_data_list_basic():
    """Test basic functionality of from_data_list."""
    data_objects = [Data(data={"name": "John", "age": 30}), Data(data={"name": "Jane", "age": 25})]
    dataset = DataSet.from_data_list(data_objects)

    assert isinstance(dataset, DataSet)
    assert isinstance(dataset, pd.DataFrame)
    assert len(dataset) == 2
    assert list(dataset.columns) == ["name", "age"]
    assert dataset.iloc[0]["name"] == "John"
    assert dataset.iloc[1]["age"] == 25


def test_from_data_list_empty():
    """Test from_data_list with empty input."""
    dataset = DataSet.from_data_list([])
    assert isinstance(dataset, DataSet)
    assert len(dataset) == 0


def test_from_data_list_missing_fields():
    """Test from_data_list with inconsistent data fields."""
    data_objects = [
        Data(data={"name": "John", "age": 30}),
        Data(data={"name": "Jane", "city": "Boston"}),  # Missing age
    ]
    dataset = DataSet.from_data_list(data_objects)

    assert isinstance(dataset, DataSet)
    assert set(dataset.columns) == {"name", "age", "city"}
    assert pd.isna(dataset.iloc[1]["age"])
    assert pd.isna(dataset.iloc[0]["city"])


def test_from_data_list_nested_data():
    """Test from_data_list with nested dictionary data."""
    data_objects = [
        Data(data={"name": "John", "address": {"city": "New York", "zip": "10001"}}),
        Data(data={"name": "Jane", "address": {"city": "Boston", "zip": "02108"}}),
    ]
    dataset = DataSet.from_data_list(data_objects)

    assert isinstance(dataset, DataSet)
    assert isinstance(dataset["address"][0], dict)
    assert dataset["address"][0]["city"] == "New York"


def test_to_data_list_basic(sample_dataset, sample_data_objects):
    """Test basic functionality of to_data_list."""
    result = sample_dataset.to_data_list()

    assert isinstance(result, list)
    assert all(isinstance(item, Data) for item in result)
    assert len(result) == len(sample_data_objects)

    # Check if data is preserved
    for original, converted in zip(sample_data_objects, result, strict=False):
        assert original.data == converted.data


def test_to_data_list_empty():
    """Test to_data_list with empty DataFrame."""
    empty_dataset = DataSet()
    result = empty_dataset.to_data_list()
    assert isinstance(result, list)
    assert len(result) == 0


def test_to_data_list_modified_data(sample_dataset):
    """Test to_data_list after DataFrame modifications."""
    # Modify the dataset
    sample_dataset["new_column"] = [1, 2, 3]
    sample_dataset.iloc[0, sample_dataset.columns.get_loc("age")] = 31

    result = sample_dataset.to_data_list()

    assert isinstance(result, list)
    assert all(isinstance(item, Data) for item in result)
    assert result[0].data["new_column"] == 1
    assert result[0].data["age"] == 31


def test_dataset_pandas_operations(sample_dataset):
    """Test that pandas operations work correctly on DataSet."""
    # Test filtering
    filtered = sample_dataset[sample_dataset["age"] > 30]
    assert isinstance(filtered, DataSet), f"Expected DataSet, got {type(filtered)}"
    assert len(filtered) == 1
    assert filtered.iloc[0]["name"] == "Bob"

    # Test aggregation
    mean_age = sample_dataset["age"].mean()
    assert mean_age == 30

    # Test groupby
    grouped = sample_dataset.groupby("city").agg({"age": "mean"})
    assert isinstance(grouped, pd.DataFrame)
    assert len(grouped) == 3


def test_dataset_with_null_values():
    """Test handling of null values in DataSet."""
    data_objects = [Data(data={"name": "John", "age": None}), Data(data={"name": None, "age": 25})]
    dataset = DataSet.from_data_list(data_objects)

    assert pd.isna(dataset.iloc[0]["age"])
    assert pd.isna(dataset.iloc[1]["name"])

    # Test that null values are preserved when converting back
    result = dataset.to_data_list()
    assert pd.isna(result[0].data["age"]), f"Expected NaN, got {result[0].data['age']}"
    assert pd.isna(result[1].data["name"]), f"Expected NaN, got {result[1].data['name']}"


def test_dataset_type_preservation():
    """Test that data types are preserved through conversion."""
    data_objects = [
        Data(
            data={
                "int_val": 1,
                "float_val": 1.5,
                "str_val": "test",
                "bool_val": True,
                "list_val": [1, 2, 3],
                "dict_val": {"key": "value"},
            }
        )
    ]
    dataset = DataSet.from_data_list(data_objects)
    result = dataset.to_data_list()

    assert isinstance(result[0].data["int_val"], int)
    assert isinstance(result[0].data["float_val"], float)
    assert isinstance(result[0].data["str_val"], str)
    assert isinstance(result[0].data["bool_val"], bool)
    assert isinstance(result[0].data["list_val"], list)
    assert isinstance(result[0].data["dict_val"], dict)
