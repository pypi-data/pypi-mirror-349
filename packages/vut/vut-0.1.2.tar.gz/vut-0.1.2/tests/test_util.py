import os
import tempfile

import numpy as np
import pytest
import torch

from vut.util import (
    get_dirs,
    init_seed,
    load_list,
    load_np,
    load_tensor,
    save,
    save_list,
    save_np,
    save_tensor,
    to_list,
    to_np,
    to_tensor,
    unique,
)


def test_init_seed__same_values():
    init_seed(42)
    data = np.random.rand(1000)
    init_seed(42)
    expected = np.random.rand(1000)
    assert np.array_equal(data, expected), (
        "Random data should be the same after re-initializing the seed"
    )


def test_init_seed__different_values():
    init_seed(42)
    data1 = np.random.rand(1000)
    init_seed(43)
    data2 = np.random.rand(1000)
    assert not np.array_equal(data1, data2), (
        "Random data should be different after changing the seed"
    )


test_case_unique = [
    # empty
    ([], []),
    # single element
    ([1], [1]),
    # multiple elements
    ([1, 2, 3], [1, 2, 3]),
    # duplicates
    ([1, 2, 2, 3], [1, 2, 3]),
    ([1, 1, 1], [1]),
    # mixed types
    ([1, 2.0, 3], [1, 2.0, 3]),
    # order preservation
    ([3, 1, 2, 1], [3, 1, 2]),
    ([1, 3, 1, 2, 4, 3, 2], [1, 3, 2, 4]),
]


@pytest.mark.parametrize(
    "data, expected",
    test_case_unique,
)
def test_unique__list(data, expected):
    assert unique(data) == expected


@pytest.mark.parametrize(
    "data, expected",
    test_case_unique,
)
def test_unique__ndarray(data, expected):
    data = np.array(data)
    expected = np.array(expected)
    assert np.array_equal(unique(data), expected)


@pytest.mark.parametrize(
    "data, expected",
    test_case_unique,
)
def test_unique__tensor(data, expected):
    data = torch.tensor(data)
    expected = torch.tensor(expected)
    assert torch.equal(unique(data), expected)


def test_unique__unsupported_type():
    with pytest.raises(TypeError):
        unique("unsupported type")


def test_get_dirs__non_recursive():
    path = os.path.dirname(__file__)
    dirs = get_dirs(path, recursive=False)
    assert all(os.path.isdir(d) for d in dirs), "All items should be directories"


def test_get_dirs__recursive():
    path = os.path.dirname(__file__)
    dirs = get_dirs(path, recursive=True)
    assert all(os.path.isdir(d) for d in dirs), "All items should be directories"


def test_get_dirs__empty_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        dirs = get_dirs(temp_dir, recursive=False)
        assert dirs == [], "Empty directory should return an empty list"


def test_get_dirs__non_existent_path():
    with tempfile.TemporaryDirectory() as temp_dir:
        non_existent_path = os.path.join(temp_dir, "non_existent")
        dirs = get_dirs(non_existent_path, recursive=False)
        assert dirs == [], "Non-existent path should return an empty list"


def test_to_list__list():
    data = [1, 2, 3]
    result = to_list(data)
    assert result == data, "Should return the same list"


def test_to_list__ndarray():
    data = np.array([1, 2, 3])
    result = to_list(data)
    assert result == data.tolist(), "Should return the same list"


def test_to_list__tensor():
    data = torch.tensor([1, 2, 3])
    result = to_list(data)
    assert result == data.tolist(), "Should return the same list"


def test_to_list__unsupported_type():
    with pytest.raises(TypeError):
        to_list("unsupported type")


def test_to_np__list():
    data = [1, 2, 3]
    result = to_np(data)
    assert np.array_equal(result, np.array(data)), "Should return the same numpy array"


def test_to_np__ndarray():
    data = np.array([1, 2, 3])
    result = to_np(data)
    assert np.array_equal(result, data), "Should return the same numpy array"


def test_to_np__tensor():
    data = torch.tensor([1, 2, 3])
    result = to_np(data)
    assert np.array_equal(result, data.numpy()), "Should return the same numpy array"


def test_to_np__unsupported_type():
    with pytest.raises(TypeError):
        to_np("unsupported type")


def test_to_tensor__list():
    data = [1, 2, 3]
    result = to_tensor(data)
    assert torch.equal(result, torch.tensor(data)), "Should return the same tensor"


def test_to_tensor__ndarray():
    data = np.array([1, 2, 3])
    result = to_tensor(data)
    assert torch.equal(result, torch.tensor(data)), "Should return the same tensor"


def test_to_tensor__tensor():
    data = torch.tensor([1, 2, 3])
    result = to_tensor(data)
    assert torch.equal(result, data), "Should return the same tensor"


def test_to_tensor__unsupported_type():
    with pytest.raises(TypeError):
        to_tensor("unsupported type")


def test_save_list():
    data = [1, 2, 3]
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        save_list(data, file_path)
    with open(file_path, "r") as f:
        content = f.read()
    assert content == "1\n2\n3\n", "File content should match the list"
    os.remove(file_path)


def test_save_list_with_callback():
    data = [1, 2, 3]
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        save_list(data, file_path, callback=lambda x: f"{x}0")
    with open(file_path, "r") as f:
        content = f.read()
    assert content == "10\n20\n30\n", "File content should match the list"
    os.remove(file_path)


def test_save_np():
    data = np.array([1, 2, 3])
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name + ".npy"
        save_np(data, file_path)
    loaded_data = np.load(file_path)
    assert np.array_equal(loaded_data, data), (
        "Loaded data should match the original array"
    )
    os.remove(file_path)


def test_save_tensor():
    data = torch.tensor([1, 2, 3])
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        save_tensor(data, file_path)
    loaded_data = torch.load(file_path)
    assert torch.equal(loaded_data, data), (
        "Loaded data should match the original tensor"
    )
    os.remove(file_path)


def test_save__list():
    data = [1, 2, 3]
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        save(data, file_path)
    with open(file_path, "r") as f:
        content = f.read()
    assert content == "1\n2\n3\n", "File content should match the list"
    os.remove(file_path)


def test_save__ndarray():
    data = np.array([1, 2, 3])
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name + ".npy"
        save(data, file_path)
    loaded_data = np.load(file_path)
    assert np.array_equal(loaded_data, data), (
        "Loaded data should match the original array"
    )


def test_save__tensor():
    data = torch.tensor([1, 2, 3])
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        save(data, file_path)
    loaded_data = torch.load(file_path)
    assert torch.equal(loaded_data, data), (
        "Loaded data should match the original tensor"
    )


def test_save__unsupported_type():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        with pytest.raises(TypeError):
            save("unsupported type", file_path)


def test_load_list():
    data = [1, 2, 3]
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        file_path = temp_file.name
        temp_file.writelines(f"{item}\n" for item in data)
    loaded_data = load_list(file_path)
    assert loaded_data == [str(i) for i in data], (
        "Loaded data should match the original list"
    )
    os.remove(file_path)


def test_load_list_with_callback():
    data = [1, 2, 3]
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        file_path = temp_file.name
        temp_file.writelines(f"{item}\n" for item in data)
    loaded_data = load_list(file_path, callback=int)
    assert loaded_data == data, "Loaded data should match the original list"
    os.remove(file_path)


def test_load_np():
    data = np.array([1, 2, 3])
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name + ".npy"
        np.save(file_path, data)
    loaded_data = load_np(file_path)
    assert np.array_equal(loaded_data, data), (
        "Loaded data should match the original array"
    )
    os.remove(file_path)


def test_load_tensor():
    data = torch.tensor([1, 2, 3])
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        torch.save(data, file_path)
    loaded_data = load_tensor(file_path)
    assert torch.equal(loaded_data, data), (
        "Loaded data should match the original tensor"
    )
    os.remove(file_path)
