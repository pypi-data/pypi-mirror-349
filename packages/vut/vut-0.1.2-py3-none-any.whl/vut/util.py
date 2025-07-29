import os
import random
from pathlib import Path

import numpy as np
import torch
from numpy.typing import NDArray
from torch import Tensor


def init_seed(seed: int = 42) -> None:
    """Initialize the random seed for reproducibility.

    Args:
        seed (int, optional): Seed value for random number generation. Defaults to 42.
    """
    torch.backends.cudnn.enabled = True
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.cuda.manual_seed(seed)


def unique(lst: list | NDArray | Tensor) -> list | NDArray | Tensor:
    """Return unique elements from the input list, NDArray, or Tensor while preserving order.

    Args:
        lst (list | NDArray | Tensor): Input list, NDArray, or Tensor to find unique elements from. Dimension size must be 1.

    Returns:
        list | NDArray | Tensor: Unique elements.
    """
    if isinstance(lst, list):
        return list(dict.fromkeys(lst))

    if isinstance(lst, np.ndarray):
        assert lst.ndim == 1, "Only 1D arrays are supported"
        _, indices = np.unique(lst, return_index=True)
        return lst[np.sort(indices)]

    if isinstance(lst, torch.Tensor):
        assert lst.ndim == 1, "Only 1D tensors are supported"
        # TODO: implement a more efficient way to get unique elements using torch
        return torch.tensor(
            list(dict.fromkeys(lst.cpu().tolist())),
            dtype=lst.dtype,
            device=lst.device,
        )

    raise TypeError(
        f"Unsupported type: {type(lst)}. Supported types are list, NDArray, and Tensor."
    )


def get_dirs(path: str | Path, recursive: bool = False) -> list[Path]:
    """Get directories from the specified path.

    Args:
        path (str | Path): The path to search for directories.
        recursive (bool, optional): Whether to search directories recursively. Defaults to False.

    Returns:
        list[Path]: A list of directories found.
    """
    path = str(path)
    dirs = set()

    if not os.path.exists(path):
        return []

    if not recursive:
        dirs = [
            os.path.join(path, d)
            for d in os.listdir(path)
            if os.path.exists(os.path.join(path, d))
            and os.path.isdir(os.path.join(path, d))
        ]
        return [Path(d) for d in dirs]

    for path, _, files in os.walk(path):
        if len(files) > 0:
            dirs.add(path)

    return sorted([Path(d) for d in dirs])


def to_list(x: list | NDArray | Tensor) -> list:
    """Convert input to list.

    Args:
        x (list | NDArray | Tensor): Input to convert.

    Returns:
        list: Converted list.
    """
    if isinstance(x, list):
        return x

    if isinstance(x, np.ndarray):
        return x.tolist()

    if isinstance(x, torch.Tensor):
        return x.cpu().tolist()

    raise TypeError(
        f"Unsupported type: {type(x)}. Supported types are list, NDArray, and Tensor."
    )


def to_np(x: list | NDArray | Tensor) -> NDArray:
    """Convert input to numpy array.

    Args:
        x (list | NDArray | Tensor): Input to convert.

    Returns:
        NDArray: Converted numpy array.
    """
    if isinstance(x, list):
        return np.array(x)

    if isinstance(x, np.ndarray):
        return x

    if isinstance(x, torch.Tensor):
        return x.detach().cpu().numpy()

    raise TypeError(
        f"Unsupported type: {type(x)}. Supported types are list, NDArray, and Tensor."
    )


def to_tensor(x: list | NDArray | Tensor) -> Tensor:
    """Convert input to PyTorch tensor.

    Args:
        x (list | NDArray | Tensor): Input to convert.

    Returns:
        Tensor: Converted PyTorch tensor.
    """
    if isinstance(x, list):
        return torch.tensor(x)

    if isinstance(x, np.ndarray):
        return torch.from_numpy(x)

    if isinstance(x, torch.Tensor):
        return x

    raise TypeError(
        f"Unsupported type: {type(x)}. Supported types are list, NDArray, and Tensor."
    )


def save_list(lst: list, path: str | Path, callback=None) -> None:
    """Save a list to a file.

    Args:
        lst (list): List to save.
        path (str | Path): Path to save the list.
        callback (callable, optional): A function to apply to each item before saving. Defaults to None.
    """
    if callback is not None:
        lst = [callback(item) for item in lst]
    with open(path, "w") as f:
        f.writelines(f"{item}\n" for item in lst)


def save_np(arr: NDArray, path: str | Path) -> None:
    """Save a numpy array to a file.

    Args:
        arr (NDArray): Numpy array to save.
        path (str | Path): Path to save the numpy array.
    """
    np.save(path, arr)


def save_tensor(tensor: Tensor, path: str | Path) -> None:
    """Save a PyTorch tensor to a file.

    Args:
        tensor (Tensor): PyTorch tensor to save.
        path (str | Path): Path to save the tensor.
    """
    torch.save(tensor, path)


def save(x: list | NDArray | Tensor, path: str | Path) -> None:
    """Save a list, numpy array, or PyTorch tensor to a file.

    Args:
        x (list | NDArray | Tensor): Input to save.
        path (str | Path): Path to save the input.
    """
    if isinstance(x, list):
        save_list(x, path)
    elif isinstance(x, np.ndarray):
        save_np(x, path)
    elif isinstance(x, torch.Tensor):
        save_tensor(x, path)
    else:
        raise TypeError(
            f"Unsupported type: {type(x)}. Supported types are list, NDArray, and Tensor."
        )


def load_list(path: str | Path, callback=None) -> list:
    """Load a list from a file.

    Args:
        path (str | Path): Path to load the list from.
        callback (callable, optional): A function to apply to each item after loading. Defaults to None.

    Returns:
        list: Loaded list.
    """
    with open(path, "r") as f:
        loaded_list = [line.strip() for line in f.readlines() if line.strip()]
    if callback is not None:
        loaded_list = [callback(item) for item in loaded_list]
    return loaded_list


def load_np(path: str | Path) -> NDArray:
    """Load a numpy array from a file.

    Args:
        path (str | Path): Path to load the numpy array from.

    Returns:
        NDArray: Loaded numpy array.
    """
    return np.load(path)


def load_tensor(path: str | Path) -> Tensor:
    """Load a PyTorch tensor from a file.

    Args:
        path (str | Path): Path to load the tensor from.

    Returns:
        Tensor: Loaded PyTorch tensor.
    """
    return torch.load(path)
