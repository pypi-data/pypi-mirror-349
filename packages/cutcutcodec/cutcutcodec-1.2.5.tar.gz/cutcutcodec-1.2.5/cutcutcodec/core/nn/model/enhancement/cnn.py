#!/usr/bin/env python3

"""Implement a convolutive network for video enhancement."""

import torch

from cutcutcodec.core.filter.video.resize import resize
from cutcutcodec.core.nn.start import load


class CNN(torch.nn.Module):
    """Improve RGB image quality keeping the resolution."""

    def __init__(self, **kwargs):
        super().__init__()
        self.layer1 = torch.nn.Sequential(  # (n, 1, 3*c, h, w) -> (n, 3*4, c, h, w)
            torch.nn.Conv3d(
                1, 12, (9, 3, 3), padding=(4, 1, 1), padding_mode="replicate", stride=(3, 1, 1)
            ),
            torch.nn.PReLU(),
            torch.nn.Dropout(0.1),
            torch.nn.Conv3d(12, 12, (1, 3, 3), padding=(0, 1, 1)),
            torch.nn.ELU(),
            torch.nn.Dropout(0.1),
        )
        self.layer2 = torch.nn.Sequential(  # (n, 3*4, c, h, w) -> (n, 3*8, c, h/2, w/2)
            torch.nn.Conv3d(12, 24, (1, 5, 5), padding=(0, 2, 2), stride=(1, 2, 2)),
            torch.nn.ELU(),
            torch.nn.Dropout(0.1),
            torch.nn.Conv3d(24, 24, (1, 3, 3), padding=(0, 1, 1)),
            torch.nn.ELU(),
            torch.nn.Dropout(0.1),
        )
        self.middle = torch.nn.Sequential(
            # (n, 3*8, c/2, h/2, w) -> (n, 3*16, c, h/4, w/4)
            torch.nn.Conv3d(24, 48, (1, 5, 5), padding=(0, 2, 2), stride=(1, 2, 2)),
            torch.nn.ELU(),
            torch.nn.Dropout(0.1),
            # temporal exploration
            torch.nn.Conv3d(48, 48, (3, 3, 3), padding=(1, 1, 1)),
            torch.nn.ELU(),
            torch.nn.Dropout(0.1),
            # (n, 3*16, c/4, h/4, w) -> (n, 3*8, c, h/2, w/2)
            torch.nn.ConvTranspose3d(48, 24, (1, 4, 4), padding=(0, 1, 1), stride=(1, 2, 2)),
            torch.nn.ELU(),
            torch.nn.Dropout(0.1),
        )
        self.layer2rev = torch.nn.Sequential(  # (n, 3*8+3*8, c, h/2, w/2) -> (n, 3*4, c, h, w)
            torch.nn.ConvTranspose3d(48, 24, (1, 4, 4), padding=(0, 1, 1), stride=(1, 2, 2)),
            torch.nn.ELU(),
            torch.nn.Dropout(0.1),
            torch.nn.Conv3d(24, 12, (1, 3, 3), padding=(0, 1, 1)),
            torch.nn.ELU(),
            torch.nn.Dropout(0.1),
        )
        self.layer1rev = torch.nn.Sequential(  # (n, 3*4+3*4, c, h, w) -> (n, 1, 3*c, h, w)
            torch.nn.ConvTranspose3d(24, 12, (9, 5, 5), padding=(3, 2, 2), stride=(3, 1, 1)),
            torch.nn.PReLU(),
            torch.nn.Dropout(0.1),
            torch.nn.Conv3d(12, 9, (1, 3, 3), padding=(0, 1, 1)),
            torch.nn.ELU(),
            torch.nn.Dropout(0.1),
            torch.nn.Conv3d(9, 1, (1, 3, 3), padding=(0, 1, 1)),
            # torch.nn.Sigmoid(),
        )
        # torch.nn.init.xavier_uniform_(self.layer1.weight)
        load(self, kwargs.get("weights", None))

    def forward(self, video: torch.Tensor) -> torch.Tensor:  # pylint: disable=W0221
        """Improve the quality of the middle frame of the 5 consecutives rgb frames.

        Parameters
        ----------
        video : torch.Tensor
            The contanenation of 5 video batched frames in RGB format of shape (n, h, w, 15).

        Returns
        -------
        middle_frame : torch.Tensor
            The enhanced third frame of the sequence, of shape (n, h, w, 3).

        Examples
        --------
        >>> import torch
        >>> from cutcutcodec.core.nn.model.enhancement.cnn import CNN
        >>> CNN()(torch.rand((2, 720, 1080, 15))).shape
        torch.Size([2, 720, 1080, 15])
        >>>
        """
        assert isinstance(video, torch.Tensor), video.__class__.__name__
        assert video.dtype.is_floating_point, video.dtype
        assert video.ndim >= 3, video.shape
        if video.ndim != 4:
            return self.forward(video.reshape(-1, *video.shape[-3:])).reshape(*video.shape)
        assert video.shape[-1] % 3 == 0, video.shape

        # multiple of 4
        shape = (video.shape[0], 4*(video.shape[1]//4), 4*(video.shape[2]//4))
        lat0 = resize(video, shape, copy=False)
        lat0 = lat0.movedim(-1, -3)[..., None, :, :, :]  # (n, h, w, 3*c) -> (n, 1, 3*c, h, w)
        lat1 = self.layer1(lat0)
        lat2 = self.layer2(lat1)
        lat3 = self.middle(lat2)
        lat2 = self.layer2rev(torch.cat([lat3, lat2], dim=-4))
        lat1 = self.layer1rev(torch.cat([lat2, lat1], dim=-4))
        residu = lat1[..., 0, :, :, :].movedim(-3, -1)  # (n, 1, 3*c, h, w) -> (n, h, w, 3*c)
        residu = resize(residu, video.shape, copy=False)
        return video + residu
