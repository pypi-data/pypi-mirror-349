import numpy as np
import pandas as pd

from . import LOG
from .sampler import DirichletSampler, NormalSampler, UniformSampler


class CorrelationSampler:
    def __init__(self, seed=None, **kwargs):
        self.rng = np.random.RandomState(seed)
        # self.df = None
        # self.corr_mat = None
        self._low_factor = float(kwargs.get("low_factor", 0.8))
        self._high_factor = float(kwargs.get("high_factor", 1.2))
        self._corr_threshold = float(kwargs.get("threshold", 0.85))
        self._iter_max = int(kwargs.get("iter_max", 256))
        self._iter_max_loc = float(kwargs.get("iter_max_loc", 0.9))
        self._iter_max_scale = float(kwargs.get("iter_max_scale", 0.1))
        self._uniform_low = float(kwargs.get("uniform_low", 0.0))
        self._uniform_high = float(kwargs.get("uniform_high", 1.01))
        self._dirichlet_alpha = float(kwargs.get("dirichlet_alpha", 1.2))
        self._sampler_name = kwargs.get("distribution", "uniform")

    def sample(
        self,
        data: pd.DataFrame,
        cm: np.ndarray,
        n_samples: int,
        data_is_normalized: bool = False,
    ):
        if data_is_normalized:
            df = data
        else:
            df = (data - data.min()) / (data.max() - data.min())
        if self._sampler_name == "uniform":
            sampler = UniformSampler(
                df,
                cm,
                n_samples,
                self._uniform_low,
                self._uniform_high,
                seed=self.rng.randint(2**32 - 1),
            )
        elif self._sampler_name == "dirichlet":
            sampler = DirichletSampler(
                df,
                cm,
                n_samples,
                self._dirichlet_alpha,
                seed=self.rng.randint(2**32 - 1),
            )
        elif self._sampler_name == "normal":
            sampler = NormalSampler(
                df, cm, n_samples, seed=self.rng.randint(2**32 - 1)
            )
        else:
            raise ValueError(f"Unsupported Sampler: {self._sampler_name}")

        tmin = df.sum(axis=1).min() * self._low_factor
        tmax = df.sum(axis=1).max() * self._high_factor
        n_inputs = len(df.columns)
        design = self.rng.rand(n_samples, n_inputs)
        cmin = tmin
        cmax = tmax
        for idx in range(n_samples):
            cmin = tmin
            cmax = tmax
            drow_sum = design[idx, :].sum()
            threshold = self._corr_threshold
            iter_cnt = 0
            LOG.info(
                f"Calculating sample {idx} row_sum={drow_sum}, min={tmin}, "
                f"max={tmax}..."
            )
            while iter_cnt == 0 or not cmin < drow_sum < cmax:
                iter_cnt += 1
                if iter_cnt >= self._iter_max:
                    # TODO do stuff
                    break

                design[idx, :] = sampler.sample(
                    threshold, drow_sum, cmin, cmax, idx
                )
                drow_sum = design[idx, :].sum()
                LOG.debug(
                    f"Attempt #{iter_cnt}: row_sum={drow_sum}, min={cmin}, "
                    f"max={cmax}, threshold={threshold}"
                )
                if iter_cnt % 10 == 0:
                    cmin *= 0.999
                    cmax *= 1.001
                if iter_cnt % 20 == 0:
                    threshold += 0.01
                if threshold > 1.0:
                    threshold = self._corr_threshold
                    cmin *= 0.9
                    cmax *= 1.1
        # LOG.warning(
        #     "Created %d samples with min=%.3f (%.3f), max=%.3f (%.3f)",
        #     n_samples,
        #     tmin,
        #     cmin,
        #     tmax,
        #     cmax,
        # )
        # Column scaling
        # for col in range(design.shape[1]):
        #     source_mean = np.median(df.values[:,col])
        #     if np.isnan(source_mean):
        #         continue
        #     design_mean = np.median(design[:, col])
        #     design[:, col] *= source_mean/design_mean * 2

        if data_is_normalized:
            res = pd.DataFrame(design, columns=data.columns)
        else:
            res = data.min() + pd.DataFrame(design, columns=data.columns) * (
                data.max() - data.min()
            )
        return res
