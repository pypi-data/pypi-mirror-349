#!/usr/bin/env python3

"""Image metrics."""

from fractions import Fraction
import math
import numbers
import pathlib
import typing

import numpy as np
import torch
import tqdm

from cutcutcodec.core.analysis.stream.rate_video import optimal_rate_video
from cutcutcodec.core.analysis.stream.shape import optimal_shape_video
from cutcutcodec.core.classes.colorspace import Colorspace
from cutcutcodec.core.io import read
from cutcutcodec.core.io.read_ffmpeg import ContainerInputFFMPEG
from cutcutcodec.core.opti.parallel import map as threaded_map, starmap
from .utils import batched_frames
from .vmaf import vmaf


__all__ = ["psnr", "ssim", "vmaf"]


def _batch_frames(frames: typing.Iterable[tuple]) -> tuple:
    """Gather frames in 256 MB batches."""
    nb_pix = 0  # the number of pixel in one frame
    batch_ref, batch_dis = [], []
    for frame_ref, frame_dis in frames:
        if not nb_pix:
            nb_pix = frame_ref.shape[0] * frame_ref.shape[1]
        batch_ref.append(frame_ref.unsqueeze(0))
        batch_dis.append(frame_dis.unsqueeze(0))
        # 256e6 (MB) / 3 (channels) / 4 (bytes per float32) / 2 (batches)
        if len(batch_ref) >= math.ceil(1.067e7 / nb_pix):
            yield torch.cat(batch_ref, dim=0), torch.cat(batch_dis, dim=0)
            batch_ref, batch_dis = [], []
    if batch_ref:
        yield torch.cat(batch_ref, dim=0), torch.cat(batch_dis, dim=0)


def _compare(batch_ref: torch.Tensor, batch_dis: torch.Tensor, kwargs: dict) -> dict:
    """Compare the 2 batches with the different metrics."""
    # the factors comes from https://github.com/fraunhoferhhi/vvenc/wiki/Encoder-Performance
    res = {}
    if kwargs.get("psnr", False):
        res["psnr"] = psnr(batch_ref, batch_dis, weights=(6, 1, 1)).tolist()
    if kwargs.get("ssim", False):
        res["ssim"] = ssim(batch_ref, batch_dis, weights=(6, 1, 1), data_range=1.0).tolist()
    if kwargs.get("vmaf", False):
        res["vmaf"] = vmaf(batch_ref, batch_dis).tolist()
    return res


def _yield_frames(ref: pathlib.Path, dis: pathlib.Path) -> tuple:
    """Read frames 2 by 2."""
    # find colorspace
    with ContainerInputFFMPEG(ref) as cont_ref:
        stream_ref = cont_ref.out_select("video")[0]
        colorspace = stream_ref.colorspace
    colorspace = Colorspace("y'pbpr", colorspace.primaries, colorspace.transfer)
    with (
        read(ref, colorspace=colorspace) as cont_ref,
        read(dis, colorspace=colorspace) as cont_dis,
    ):
        stream_ref = cont_ref.out_select("video")[0]
        stream_dis = cont_dis.out_select("video")[0]
        rate = optimal_rate_video(stream_ref) or Fraction(3000, 1001)
        shape = optimal_shape_video(stream_ref) or (720, 1080)
        duration = min(stream_ref.duration, stream_dis.duration)
        times = np.arange(0.5/rate, float(duration), 1.0/rate).tolist()
        yield from tqdm.tqdm(
            threaded_map(
                lambda t: (stream_ref.snapshot(t, shape), stream_dis.snapshot(t, shape)),
                times,
            ),
            desc="compare",
            total=len(times),
            unit="img",
        )


def compare(
    ref: pathlib.Path | str | bytes, dis: pathlib.Path | str | bytes, **kwargs
) -> dict[str, list[float]]:
    """Compare 2 video files with differents metrics.

    Parameters
    ----------
    ref : pathlike
        The reference video file.
    dis : pathlike
        The distorted video.
    psnr : bool, dafault=False
        If True, compute the psnr (very fast).
    ssim : bool, default=False
        If True, compute the ssim (slow).
    vmaf : bool, default=False
        If True, compute the vmaf (medium).

    Returns
    -------
    metrics : dict[str, list[float]]
        Each metric name is associated with the scalar value of each frame.

    Notes
    -----
    Frames are converted to yuv if not already converted,
    then the distorted video is converted to the color space of the reference video.

    Examples
    --------
    >>> import pprint
    >>> from cutcutcodec.core.analysis.video.metric import compare
    >>> res = compare("media/video/intro.webm", "media/video/intro.webm", psnr=True, ssim=True)
    >>> pprint.pprint(res)  # doctest: +ELLIPSIS
    {'psnr': [100.0,
              100.0,
              ...,
              100.0,
              100.0],
     'ssim': [1.0,
              1.0,
              ...,
              1.0,
              1.0]}
    >>>
    """
    ref = pathlib.Path(ref).expanduser()
    dis = pathlib.Path(dis).expanduser()
    metrics = {}
    for batch_metrics in starmap(
        _compare,
        ((r, d, kwargs) for r, d in _batch_frames(_yield_frames(ref, dis))),
    ):
        if not metrics:
            metrics = batch_metrics
        else:
            for key, metric in metrics.items():
                metric.extend(batch_metrics[key])
    return metrics


@batched_frames
def psnr(ref: torch.Tensor, dis: torch.Tensor, *args, **kwargs) -> torch.Tensor:
    """Compute the peak signal to noise ratio of 2 images.

    Parameters
    ----------
    ref, dis : arraylike
        The 2 images to be compared, of shape ([*batch], height, width, channels).
        Supported types are float32 and float64.
    weights : iterable[float], optional
        The relative weight of each channel. By default, all channels have the same weight.
    threads : int, optional
        Defines the number of threads.
        The value -1 means that the function uses as many calculation threads as there are cores.
        The default value (0) allows the same behavior as (-1) if the function
        is called in the main thread, otherwise (1) to avoid nested threads.
        Any other positive value corresponds to the number of threads used.

    Returns
    -------
    psnr : arraylike
        The global peak signal to noise ratio,
        as a ponderation of the mean square error of each channel.
        It is batched and clamped in [0, 100] db.

    Notes
    -----
    * It is optimized for C contiguous tensors.
    * If device is cpu and gradient is not required, a fast C code is used instead of torch code.

    Examples
    --------
    >>> import numpy as np
    >>> from cutcutcodec.core.analysis.video.metric import psnr
    >>> np.random.seed(0)
    >>> ref = np.random.random((720, 1080, 3))  # It could also be a torch array list...
    >>> dis = 0.8 * ref + 0.2 * np.random.random((720, 1080, 3))
    >>> psnr(ref, dis).round(1)
    np.float64(21.8)
    >>>
    """
    if (
        ref.requires_grad or dis.requires_grad
        or ref.device.type != "cpu" or dis.device.type != "cpu"
    ):
        from .psnr_torch import psnr_torch
        return psnr_torch(ref, dis, *args, **kwargs)
    from .metric import psnr as psnr_c
    return torch.asarray(
        [psnr_c(r, d, *args, **kwargs) for r, d in zip(ref.numpy(), dis.numpy())],
        dtype=ref.dtype,
    )


@batched_frames
def ssim(ref: torch.Tensor, dis: torch.Tensor, *args, stride: int = 1, **kwargs) -> torch.Tensor:
    """Compute the Structural similarity index measure of 2 images.

    Parameters
    ----------
    ref, dis : arraylike
        The 2 images to be compared, of shape ([*batch], height, width, channels).
        Supported types are float32 and float64.
    data_range : float, default=1.0
        The data range of the input image (difference between maximum and minimum possible values).
    weights : iterable[float], optional
        The relative weight of each channel. By default, all channels have the same weight.
    sigma : float, default=1.5
        The standard deviation of the gaussian. It has to be strictely positive.
    stride : int, default=1
        The stride of the convolving kernel.
    threads : int, optional
        Defines the number of threads.
        The value -1 means that the function uses as many calculation threads as there are cores.
        The default value (0) allows the same behavior as (-1) if the function
        is called in the main thread, otherwise (1) to avoid nested threads.
        Any other positive value corresponds to the number of threads used.

    Returns
    -------
    ssim : arraylike
        The ponderated structural similarity index measure of each layers.

    Notes
    -----
    * It is optimized for C contiguous tensors.
    * If device is cpu, gradient is not required and stride != 1, a fast C code is used.

    Examples
    --------
    >>> import numpy as np
    >>> from cutcutcodec.core.analysis.video.metric import ssim
    >>> np.random.seed(0)
    >>> ref = np.random.random((720, 1080, 3))  # It could also be a torch array list...
    >>> dis = 0.8 * ref + 0.2 * np.random.random((720, 1080, 3))
    >>> ssim(ref, dis).round(2)
    np.float64(0.95)
    >>>
    """
    assert isinstance(stride, numbers.Integral), stride.__class__.__name__
    if stride == 1:
        from .ssim_torch import ssim_fft_torch
        return ssim_fft_torch(ref, dis, *args, **kwargs)
    if (
        ref.requires_grad or dis.requires_grad
        or ref.device.type != "cpu" or dis.device.type != "cpu"
    ):
        from .ssim_torch import ssim_conv_torch
        return ssim_conv_torch(ref, dis, *args, stride=stride, **kwargs)
    from .metric import ssim as ssim_c
    return torch.asarray(
        [ssim_c(r, d, *args, stride=stride, **kwargs) for r, d in zip(ref.numpy(), dis.numpy())],
        dtype=ref.dtype,
    )
