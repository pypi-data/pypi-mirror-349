import numpy as np
import torch


def add(x: int, y: int) -> int:

    return np.add(x, y)


def matmul(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    """Performs matrix multiplication between two tensors.

    Args:
        x (torch.Tensor): The first input tensor (matrix).
        y (torch.Tensor): The second input tensor (matrix).

    Returns:
        torch.Tensor: The result of the matrix multiplication of x and y.
    """
    return x.matmul(y)
