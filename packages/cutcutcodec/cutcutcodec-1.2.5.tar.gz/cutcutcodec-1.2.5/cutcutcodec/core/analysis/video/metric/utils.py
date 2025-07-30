#!/usr/bin/env python3

"""Helper for metrics."""

import functools
import typing

import torch
import numpy as np


def batched_frames(func: callable) -> callable:
    """Decorate to vectorize the metrics.

    The signature of the metric has to be:
    ``metric(ref: torch.Tensor, dis: torch.Tensor, *args, **kwargs) -> torch.Tensor``
    With ref.shape == dis.shape == (batch, height, width, channels).
    The returned type is based on ``dis`` parameter.
    """

    @functools.wraps(func)
    def batched_metric(
        ref: torch.Tensor | np.ndarray | typing.Iterable[torch.Tensor | np.ndarray],
        dis: torch.Tensor | np.ndarray | typing.Iterable[torch.Tensor | np.ndarray],
        *args,
        **kwargs,
    ) -> torch.Tensor | np.ndarray | typing.Iterable:
        # cast to torch tensor and back to homogeneous returned type
        ref = torch.asarray(ref)
        match dis:
            case np.ndarray():
                return batched_metric(ref, torch.from_numpy(dis), *args, **kwargs).numpy(force=True)
            case list():
                return batched_metric(ref, torch.asarray(dis), *args, **kwargs).tolist()
            case tuple() | set() | frozenset():
                return dis.__class__(batched_metric(ref, list(dis), *args, **kwargs))
            case _:
                assert isinstance(dis, torch.Tensor), dis.__class__.__name__

        # set shape
        while ref.ndim < 3:
            ref = ref.unsqueeze(-1)
        while dis.ndim < 3:
            dis = dis.unsqueeze(-1)
        ref, dis = torch.broadcast_tensors(ref, dis)
        *batch, height, width, channels = dis.shape
        ref = ref.reshape(-1, height, width, channels)
        dis = dis.reshape(-1, height, width, channels)

        # apply func
        res = func(ref, dis, *args, **kwargs)

        # back to unfolded shape
        res = res.reshape(batch)
        return res

    return batched_metric
