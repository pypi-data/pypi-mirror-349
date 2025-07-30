import torch
import torch.nn as nn
import torch.nn.functional as F
from ._blocks import PSP_Pooling, Reconstruction, get_resblock
from ._rdnet import RDNet
from ..util import _force_list

class RDResUNet(nn.Module):
    def __init__(
            self,
            channels : list[int] = 1,
            hidden : list[int] = [1024, 1024, 512, 256],
            scale : int = 4,
            depth : int = 3,
            dilations : list[list[int]] = None,
            pool_sizes : list[int] = None,
            encoder_pool : bool = False,
            rdnet_init : int = 128,
            growth_rates : list[int] = [64, 104, 128, 128, 128, 128, 224],
            ds_blocks : list[bool] = [False, True, True, False, False, False, True],
            ese_blocks : list[bool] = [False, False, True, True, True, True, True],
            n_blocks : list[int] = [3, 3, 3, 3, 3, 3, 3],
            patch_size : int = 2,
            bottleneck : int = 4,
            compression : float = 0.5,
            drop_rate : float = 0,
        ):
        r"""A RDNet (Revitalized DenseNet) encoder and ResUNet decoder with an additional image upscaling block. RDNet is detailed in Kim et al., 2024.
        If ``dilations`` is provided, the decoder is instead a Atrous Residual UNet as detailed in Diakogiannis et al., 2019.

        Skip connections from the RDNet encoder to the ResUNet decoder are created before each downsampling layer.

        Channel sizes hidden[0] (and hidden[-1] if encoder_pool is True) must be divisible by pool_sizes if provided.

        Args:
            channels (list[int]) : Number of channels in image data. Can also be a list of in channels (low-resolution) and out channels (high-resolution) respectively.

            hidden (list[int]) : Elementwise list of hidden layer channels of ResUNet decoder. Each element must have a corresponding skip connection in the RDNet encoder, provided after each downsample block.

            scale (int) : Upscaling factor for predictions. Choose a power of 2 for best results. Default is 4.

            depth (int) : Number of hidden layers per decoder residual block. Default is 3.
            
            dilations (list[list[int]]) : List of dilation values per layer. If value is None, atrous convolutions will not be used. Default is None.

            pool_sizes (list[int]) : Pooling ratios for PSP pooling. If value is None, PSP pooling will not be used. Default is None.

            encoder_pool (bool) : Whether to include additional PSP pooling layer at end of encoder. Should not be used if last layer has a size of less than 16 pixels. Default is False.

            rdnet_init (int) : Number of channels in first RDNet layer. Channels grow from this each layer according to growth parameters. Default is 128.

            growth_rates (list[int]) : Growth rates for each RDNet layer, compounding over each layer.

            ds_blocks (list[bool]) : Specifies which RDNet layers downsample image space. Number of downsampling blocks must be one less than ResUNet hidden layers.

            ese_blocks (list[bool]) : Specifies which RDNet layers are ESE blocks.

            n_blocks (list[int]) : Number of blocks per RDNet layer. Can also be an integer to be held constant across all layers. Default is 3.

            patch_size (int) : Patch size for initial patch embedding. Default is 2.

            bottleneck (int) : Bottleneck width ratio for all blocks. Default is 4.

            compression (float) : Transition compression ratio to offset growth. Default is 0.5.

            drop_rate (float) : Dropout rate for DropPath. Default is 0.
        """
        super().__init__()
        channels = _force_list(channels)
        channels = channels*2 if len(channels) == 1 else channels

        if dilations and len(dilations) != len(hidden): raise ValueError(f"Amount of dilations must equal amount of hidden residual blocks. Given values are {len(dilations)} and {len(hidden)} respectively.")

        if pool_sizes:
            if hidden[0] % len(pool_sizes) != 0: raise ValueError(f"hidden[0] must be divisible by len(pool_sizes). Given values are {hidden[0]} and {len(pool_sizes)} respectively.")
            if encoder_pool and hidden[-1] % len(pool_sizes) != 0: raise ValueError(f"hidden[-1] must be divisible by len(pool_sizes) if encoder_pool is True. Given values are {hidden[-1]} and {len(pool_sizes)} respectively.")
        else:
            if encoder_pool: raise ValueError(f"encoder_pool cannot be True if pool_sizes are not provided.")

        self.norm = nn.BatchNorm2d(channels[0]) if not dilations else None

        if sum(ds_blocks) != len(hidden)-1: raise ValueError(f"Number of downsampling blocks must be one less than ResUNet hidden layers. Given {sum(ds_blocks)} downsampling blocks but {len(hidden)} hidden layers.")

        self.encoder = RDNet(channels[0], rdnet_init, patch_size, growth_rates, ds_blocks, ese_blocks, n_blocks, bottleneck, drop_rate, compression)
        skips = [feature["num_chs"] for feature in self.encoder.feature_info]
        skips.reverse()

        if len(skips) != len(hidden): raise ValueError(f"Each encoder skip connection must have a corresponding decoder hidden layer. There are {len(skips)} skip connections but {len(hidden)} hidden layers.")
        
        self.ratios = [1] + [2]*(len(skips)-1) + [patch_size]

        layers = [0, *hidden]
        self.decoder = nn.ModuleList()
        for layer_idx in range(len(layers)-1):
            self.decoder.append(get_resblock(in_channels=layers[layer_idx]//self.ratios[layer_idx]**2+skips[layer_idx], out_channels=layers[layer_idx+1], dilations=dilations[layer_idx] if dilations else None, depth=depth))

        self.encoder_pool = PSP_Pooling(skips[0], pool_sizes) if pool_sizes and encoder_pool else None
        self.reconstruction_pool = PSP_Pooling(hidden[-1]//self.ratios[-1]**2, pool_sizes) if pool_sizes else None

        self.reconstruction = Reconstruction(channels[0], channels[1], hidden[-1]//self.ratios[-1]**2, scale)

        self.skips = skips

    def forward(self, x):
        x = x / 128 - 1 # Scale input approx from [0, 255] to [-1, 1]
        if self.norm is not None:
            x = self.norm(x)

        skips = [x]
        skips.extend(self.encoder(x))

        if self.encoder_pool is not None:
            skips[-1] = self.encoder_pool(skips[-1])

        for idx, layer in enumerate(self.decoder):
            x = torch.cat([x, skips.pop()], dim=1) if idx != 0 else skips.pop()
            x = layer(x)

            x = F.pixel_shuffle(x, self.ratios[idx+1])
        
        if self.reconstruction_pool is not None:
            x = self.reconstruction_pool(x)
        
        x = torch.cat([x, skips.pop()], dim=1)
        if len(skips) != 0: raise IndexError(f"Skip connection mismatch between encoder and decoder. {len(skips)} skip connections are unused.")

        x = self.reconstruction(x)

        x = x * 128 + 128 # Scale output approx from [-1, 1] to [0, 255]
        return x

    def extra_repr(self):
        return f"{'Atrous ' if self.norm is None else ''}RDResUNet with {self.reconstruction.scale}x upscaling\n{len(self.decoder)} residual blocks with {self.decoder[0].depth} hidden layers each\nSkip connection sizes: {self.skips}\nPSP pooling {'enabled' if self.reconstruction_pool else 'disabled'}"

class RDResUNetA():
    def __new__(cls,
            channels : int = 1,
            hidden : list[int] = [1024, 1024, 512, 256],
            scale : int = 4,
            depth : int = 3,
            dilations : list[list[int]] = [[1],[1],[1,3],[1,3,15]],
            pool_sizes : list[int] = [1, 2, 4, 8],
            encoder_pool : bool = False,
            rdnet_init : int = 128,
            growth_rates : list[int] = [64, 104, 128, 128, 128, 128, 224],
            ds_blocks : list[bool] = [False, True, True, False, False, False, True],
            ese_blocks : list[bool] = [False, False, True, True, True, True, True],
            n_blocks : list[int] = [3, 3, 3, 3, 3, 3, 3],
            patch_size : int = 2,
            bottleneck : int = 4,
            compression : float = 0.5,
            drop_rate : float = 0,
        ):
        r""":class:`RDResUNet` wrapper of Atrous Residual UNet as detailed in Diakogiannis et al., 2019.
        Provides alternative default arguments for an atrous network.

        Skip connections from the RDNet encoder to the ResUNet decoder are created before each downsampling layer.

        Channel sizes hidden[0] (and hidden[-1] if encoder_pool is True) must be divisible by pool_sizes if provided.

        Args:
            channels (int) : Number of channels in image data. Can also be a list of in channels and out channels respectively.

            hidden (list[int]) : Elementwise list of hidden layer channels of ResUNet decoder. Each element must have a corresponding skip connection in the RDNet encoder, provided after each downsample block.

            scale (int) : Upscaling factor for predictions. Choose a power of 2 for best results. Default is 4.

            depth (int) : Number of hidden layers per decoder residual block. Default is 3.
            
            dilations (list[list[int]]) : List of dilation values per layer. If value is None, atrous convolutions will not be used. Default is None.

            pool_sizes (list[int]) : Pooling ratios for PSP pooling. If value is None, PSP pooling will not be used. Default is None.

            encoder_pool (bool) : Whether to include additional PSP pooling layer at end of encoder. Should not be used if last layer has a size of less than 16 pixels. Default is False.

            rdnet_init (int) : Number of channels in first RDNet layer. Channels grow from this each layer according to growth parameters. Default is 128.

            growth_rates (list[int]) : Growth rates for each RDNet layer, compounding over each layer.

            ds_blocks (list[bool]) : Specifies which RDNet layers downsample image space. Number of downsampling blocks must be one less than ResUNet hidden layers.

            ese_blocks (list[bool]) : Specifies which RDNet layers are ESE blocks.

            n_blocks (list[int]) : Number of blocks per RDNet layer. Can also be an integer to be held constant across all layers. Default is 3.

            patch_size (int) : Patch size for initial patch embedding. Default is 2.

            bottleneck (int) : Bottleneck width ratio for all blocks. Default is 4.

            compression (float) : Transition compression ratio to offset growth. Default is 0.5.

            drop_rate (float) : Dropout rate for DropPath. Default is 0.
        """
        return RDResUNet(
            channels,
            hidden,
            scale,
            depth,
            dilations,
            pool_sizes,
            encoder_pool,
            rdnet_init,
            growth_rates,
            ds_blocks,
            ese_blocks,
            n_blocks,
            patch_size,
            bottleneck,
            compression,
            drop_rate,
        )
