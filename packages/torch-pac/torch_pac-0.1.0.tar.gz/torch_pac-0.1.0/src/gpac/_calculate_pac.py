#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2025-05-17 16:09:00 (ywatanabe)"
# File: /ssh:sp:/home/ywatanabe/proj/gPAC/src/gpac/_calculate_pac.py
# ----------------------------------------
import os
__FILE__ = (
    "./src/gpac/_calculate_pac.py"
)
__DIR__ = os.path.dirname(__FILE__)
# ----------------------------------------

import math
import warnings
from typing import Optional, Tuple, Union

import numpy as np
import torch
import torch.nn as nn

from ._PAC import PAC


# --- User-facing Function ---
def calculate_pac(
    signal: torch.Tensor | np.ndarray,
    fs: float,
    pha_start_hz: float = 2.0,
    pha_end_hz: float = 20.0,
    pha_n_bands: int = 50,
    amp_start_hz: float = 60.0,
    amp_end_hz: float = 160.0,
    amp_n_bands: int = 30,
    n_perm: Optional[int] = None,
    trainable: bool = False,
    fp16: bool = False,
    amp_prob: bool = False,
    mi_n_bins: int = 18,
    filter_cycle: int = 3,
    device: Optional[str | torch.device] = None,
    chunk_size: Optional[int] = None,
    average_channels: bool = False,
    return_dist: bool = False,
) -> Union[
    # Standard return (no distribution): pac_values, pha_freqs, amp_freqs
    Tuple[torch.Tensor, np.ndarray, np.ndarray],
    # With distribution: pac_values, surrogate_dist, pha_freqs, amp_freqs
    Tuple[torch.Tensor, torch.Tensor, np.ndarray, np.ndarray],
]:
    """
    High-level function to calculate Phase-Amplitude Coupling (PAC).

    Args:
        signal: Input signal as tensor or numpy array
        fs: Sampling frequency in Hz
        pha_start_hz: Lowest phase frequency to analyze
        pha_end_hz: Highest phase frequency to analyze
        pha_n_bands: Number of phase frequency bands
        amp_start_hz: Lowest amplitude frequency to analyze
        amp_end_hz: Highest amplitude frequency to analyze
        amp_n_bands: Number of amplitude frequency bands
        n_perm: Number of permutations for surrogate testing (None to skip)
        trainable: Whether to use trainable frequency bands
        fp16: Use half precision (float16)
        amp_prob: Calculate amplitude probability instead of modulation index
        mi_n_bins: Number of bins for modulation index calculation
        filter_cycle: Number of cycles for filter design
        device: Computation device ("cuda", "cpu", or torch.device)
        chunk_size: Process in chunks of this size (None for no chunking)
        average_channels: Whether to average across channels in the output
        return_dist: Whether to return the full distribution of surrogate PAC values

    Returns:
        When return_dist=False:
            Tuple containing:
                - PAC values tensor with shape (B, C, F_pha, F_amp) or (B, F_pha, F_amp)
                  if average_channels=True
                - Phase frequencies as numpy array
                - Amplitude frequencies as numpy array

        When return_dist=True and n_perm is not None:
            Tuple containing:
                - PAC values tensor with shape (B, C, F_pha, F_amp) or (B, F_pha, F_amp)
                - Surrogate distribution tensor with shape (n_perm, B, C, F_pha, F_amp)
                  or (n_perm, B, F_pha, F_amp) if average_channels=True
                - Phase frequencies as numpy array
                - Amplitude frequencies as numpy array

    Examples:
        Basic PAC calculation:

        >>> import torch
        >>> import numpy as np
        >>> from gpac import calculate_pac
        >>>
        >>> # Generate sample data: 1 channel, 10 second signal at 1000 Hz
        >>> fs = 1000
        >>> t = np.arange(0, 10, 1/fs)
        >>> pha_freq = 5  # Hz
        >>> amp_freq = 80  # Hz
        >>>
        >>> # Create signal with PAC: phase of 5 Hz modulates amplitude of 80 Hz
        >>> pha = np.sin(2 * np.pi * pha_freq * t)
        >>> amp = np.sin(2 * np.pi * amp_freq * t)
        >>> signal = np.sin(2 * np.pi * pha_freq * t) + (1 + 0.8 * pha) * amp * 0.2
        >>> signal = signal.reshape(1, 1, 1, -1)  # [batch, channel, segment, time]
        >>>
        >>> # Standard PAC calculation
        >>> pac_values, pha_freqs, amp_freqs = calculate_pac(
        ...     signal,
        ...     fs=fs,
        ...     pha_start_hz=2,
        ...     pha_end_hz=20,
        ...     pha_n_bands=10,
        ...     amp_start_hz=60,
        ...     amp_end_hz=120,
        ...     amp_n_bands=10,
        ...     n_perm=200  # Use permutation testing
        ... )

        Get the full permutation test distribution:

        >>> # Get the distribution of surrogate values
        >>> pac_values, surrogate_dist, pha_freqs, amp_freqs = calculate_pac(
        ...     signal,
        ...     fs=fs,
        ...     pha_start_hz=2,
        ...     pha_end_hz=20,
        ...     pha_n_bands=10,
        ...     amp_start_hz=60,
        ...     amp_end_hz=120,
        ...     amp_n_bands=10,
        ...     n_perm=200,
        ...     return_dist=True  # Return the full distribution
        ... )
        >>>
        >>> # Visualize the PAC values
        >>> import matplotlib.pyplot as plt
        >>>
        >>> # Plot the PAC values
        >>> plt.figure(figsize=(10, 4))
        >>> plt.subplot(121)
        >>> plt.imshow(pac_values[0, 0], aspect='auto', origin='lower')
        >>> plt.xlabel('Amplitude Frequency (Hz)')
        >>> plt.ylabel('Phase Frequency (Hz)')
        >>> plt.title('PAC Z-Scores')
        >>> plt.colorbar(label='Z-score')
        >>>
        >>> # Get indices of max coupling
        >>> max_idx = pac_values[0, 0].argmax()
        >>> max_pha_idx, max_amp_idx = np.unravel_index(max_idx, pac_values[0, 0].shape)
        >>>
        >>> # Plot the surrogate distribution for the max coupling
        >>> plt.subplot(122)
        >>> surrogate_values = surrogate_dist[:, 0, 0, max_pha_idx, max_amp_idx].numpy()
        >>> observed_value = pac_values[0, 0, max_pha_idx, max_amp_idx].item()
        >>> plt.hist(surrogate_values, bins=20, alpha=0.8)
        >>> plt.axvline(observed_value, color='r', linestyle='--',
        ...             label=f'Observed: {observed_value:.2f}')
        >>> plt.xlabel('PAC Value')
        >>> plt.ylabel('Count')
        >>> plt.title('Surrogate Distribution')
        >>> plt.legend()
        >>> plt.tight_layout()
        >>> plt.show()

        Custom statistical analysis using the surrogate distribution:

        >>> # Calculate p-values manually
        >>> def calculate_pvalues(observed, surrogates):
        ...     # One-sided p-value: proportion of surrogates >= observed
        ...     return ((surrogates >= observed).sum(axis=0) / len(surrogates))
        >>>
        >>> # Convert tensors to numpy arrays
        >>> pac_array = pac_values[0, 0].numpy()
        >>> surr_array = surrogate_dist[:, 0, 0].numpy()
        >>>
        >>> # Calculate p-values
        >>> pvalues = calculate_pvalues(pac_array, surr_array)
        >>>
        >>> # Apply multiple comparison correction (FDR)
        >>> from statsmodels.stats.multitest import multipletests
        >>> pvals_flat = pvalues.flatten()
        >>> significant, pvals_corr, _, _ = multipletests(pvals_flat, method='fdr_bh')
        >>> pvals_corr = pvals_corr.reshape(pvalues.shape)
        >>>
        >>> # Find significant couplings after correction
        >>> significant_mask = pvals_corr < 0.05
    """
    # 1. Device Handling
    if device is None:
        resolved_device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
    elif isinstance(device, str):
        resolved_device = torch.device(device)
    else:
        resolved_device = device

    # 2. Input Preparation
    if isinstance(signal, np.ndarray):
        try:
            dtype = np.float32 if signal.dtype == np.float64 else signal.dtype
            signal_tensor = torch.from_numpy(signal.astype(dtype))
        except TypeError as e:
            raise TypeError(
                f"Could not convert numpy array to tensor: {e}"
            ) from e
    elif isinstance(signal, torch.Tensor):
        signal_tensor = signal
    else:
        raise TypeError("Input signal must be a torch.Tensor or numpy.ndarray")

    signal_tensor = signal_tensor.to(resolved_device)
    signal_4d = ensure_4d_input(signal_tensor)
    batch_size, n_chs, n_segments, seq_len = signal_4d.shape
    target_dtype = torch.float16 if fp16 else torch.float32
    signal_4d = signal_4d.to(target_dtype)

    # 3. Model Instantiation
    model = PAC(
        seq_len=seq_len,
        fs=fs,
        pha_start_hz=pha_start_hz,
        pha_end_hz=pha_end_hz,
        pha_n_bands=pha_n_bands,
        amp_start_hz=amp_start_hz,
        amp_end_hz=amp_end_hz,
        amp_n_bands=amp_n_bands,
        n_perm=n_perm,
        trainable=trainable,
        fp16=fp16,
        amp_prob=amp_prob,
        mi_n_bins=mi_n_bins,
        filter_cycle=filter_cycle,
        return_dist=return_dist,
    ).to(resolved_device)

    if not trainable:
        model.eval()

    # 4. Calculation (Chunked or Full)
    num_traces = batch_size * n_chs * n_segments
    process_in_chunks = (
        chunk_size is not None and chunk_size > 0 and num_traces > chunk_size
    )

    # Validate return_dist and n_perm combination
    if return_dist and n_perm is None:
        warnings.warn(
            "return_dist=True has no effect when n_perm is None. "
            "No distribution will be returned."
        )
        return_dist = False

    # Validate n_perm when it's provided
    if n_perm is not None and n_perm < 10:
        warnings.warn(
            f"Using n_perm={n_perm} which is very low for permutation testing. "
            "Consider using at least 200 for stable statistical results."
        )

    # Additional warning for return_dist with low permutation count
    if return_dist and n_perm is not None and n_perm < 50:
        warnings.warn(
            f"Using n_perm={n_perm} with return_dist=True may not provide "
            "a reliable distribution for statistical analysis. "
            "Consider using at least 100-200 permutations."
        )

    if not process_in_chunks:
        grad_context = torch.enable_grad() if trainable else torch.no_grad()
        with grad_context:
            result = model(signal_4d)
            # Extract surrogate distribution if it was returned
            if isinstance(result, tuple) and len(result) == 2:
                pac_results, surrogate_dist = result
            else:
                pac_results = result
    else:
        print(
            f"Processing {num_traces} traces in chunks of size {chunk_size}..."
        )
        num_chunks = math.ceil(num_traces / chunk_size)
        all_pac_results_chunks = []
        all_surrogate_dist_chunks = (
            [] if return_dist and n_perm is not None else None
        )
        signal_flat = signal_4d.reshape(num_traces, seq_len)

        grad_context = torch.enable_grad() if trainable else torch.no_grad()
        with grad_context:
            for i_chunk in range(num_chunks):
                start_idx = i_chunk * chunk_size
                end_idx = min((i_chunk + 1) * chunk_size, num_traces)
                current_chunk_trace_count = end_idx - start_idx

                # Reshape chunk for model: (ChunkTraces, 1 Chan, 1 Seg, Time)
                signal_chunk = signal_flat[start_idx:end_idx].reshape(
                    current_chunk_trace_count, 1, 1, seq_len
                )
                chunk_result = model(signal_chunk)

                # Handle distribution if returned
                if isinstance(chunk_result, tuple) and len(chunk_result) == 2:
                    chunk_pac, chunk_surrogate = chunk_result
                    all_pac_results_chunks.append(chunk_pac)
                    if all_surrogate_dist_chunks is not None:
                        all_surrogate_dist_chunks.append(chunk_surrogate)
                else:
                    all_pac_results_chunks.append(chunk_result)

                if resolved_device.type == "cuda":
                    torch.cuda.empty_cache()

        # Concatenate and reshape results
        pac_results_flat = torch.cat(all_pac_results_chunks, dim=0)
        result_shape_suffix = pac_results_flat.shape[2:]
        target_shape_unavg = (
            batch_size,
            n_chs,
            n_segments,
        ) + result_shape_suffix
        pac_results = pac_results_flat.view(target_shape_unavg)

        # Surrogate distributions handling for chunked processing
        surrogate_dist = None
        if (
            all_surrogate_dist_chunks is not None
            and len(all_surrogate_dist_chunks) > 0
        ):
            try:
                # Concatenate surrogate distributions along the appropriate dimension (batch dim=1)
                surrogate_dist_flat = torch.cat(
                    all_surrogate_dist_chunks, dim=1
                )

                # Get the shape suffix to reconstruct the full tensor
                dist_shape_suffix = surrogate_dist_flat.shape[
                    3:
                ]  # Skip n_perm, flat_batch, flat_chan dims

                # Create the target shape for the reshaped distribution
                target_shape_dist = (
                    surrogate_dist_flat.shape[0],  # n_perm
                    batch_size,
                    n_chs,
                    n_segments,
                ) + dist_shape_suffix

                # Reshape to the target shape
                surrogate_dist = surrogate_dist_flat.view(target_shape_dist)
            except Exception as e:
                warnings.warn(
                    f"Error reshaping surrogate distributions in chunked mode: {e}. "
                    "Returning PAC values without distribution."
                )
                # Make sure we don't return a partial/broken distribution
                surrogate_dist = None
                return_dist = False

        print("Chunk processing complete.")

    # Average across channels if requested
    if average_channels and pac_results.shape[1] > 1:
        pac_results = pac_results.mean(dim=1)
        if surrogate_dist is not None and surrogate_dist.shape[2] > 1:
            surrogate_dist = surrogate_dist.mean(dim=2)

    # 5. Prepare Outputs
    # Ensure frequencies are numpy arrays on CPU
    if isinstance(model.PHA_MIDS_HZ, nn.Parameter):
        freqs_pha_np = model.PHA_MIDS_HZ.detach().cpu().numpy()
    else:
        freqs_pha_np = model.PHA_MIDS_HZ.cpu().numpy()

    if isinstance(model.AMP_MIDS_HZ, nn.Parameter):
        freqs_amp_np = model.AMP_MIDS_HZ.detach().cpu().numpy()
    else:
        freqs_amp_np = model.AMP_MIDS_HZ.cpu().numpy()

    # Return appropriate output based on whether distribution was requested and available
    if return_dist and surrogate_dist is not None:
        return pac_results, surrogate_dist, freqs_pha_np, freqs_amp_np
    else:
        return pac_results, freqs_pha_np, freqs_amp_np

# EOF
