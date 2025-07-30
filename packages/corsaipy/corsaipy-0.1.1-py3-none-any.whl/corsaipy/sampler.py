import logging
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

LOG = logging.getLogger(__name__)


class BaseSampler(ABC):
    def __init__(self, df, pcm, n_samples, seed):
        self.df = df
        self.n_inputs = len(df.columns)
        self.pcm = pcm
        self.n_samples = n_samples
        self.rng = np.random.RandomState(seed)

    @abstractmethod
    def sample(self, threshold, drow_sum, cmin, cmax, idx):
        raise NotImplementedError()

    def reset(self):
        pass

    def apply_correlations(self, drow, pcm, threshold):
        """Apply correlations to the design.

        Parameters
        ----------
        drow: np.ndarray
            The current row of the design.
        pcm: np.ndarray
            Partial correlation matrix.
        threshold: float
            The (absolute) threshold value for correlations. If a
            correlation is (absolutely) lower than the threshold, it will
            be ignored.

        """
        for ith in range(len(drow) - 1):
            for jth in range(ith + 1, len(drow)):
                pc_ = pcm[ith][jth]  # partial correlation
                # if np.isnan(pc_):
                #     print("correlation is NaN")
                # if -threshold < pc_ < threshold:
                #     continue
                if abs(pc_) == 1.0:
                    continue
                # elif self.rng.uniform() < 0.1:
                #     continue
                if pc_ < -threshold:
                    factor = -1 if self.rng.uniform() < 0.5 else 1
                    new_value = 1 - drow[ith] + drow[jth] * (1 + pc_) * factor
                elif pc_ > threshold:
                    factor = -1 if self.rng.uniform() < 0.5 else 1
                    new_value = drow[ith] + drow[jth] * (1 - pc_) * factor
                else:
                    continue
                # print(new_value)
                drow[jth] = new_value * self.rng.uniform(low=0.95, high=1.05)
        return drow


class UniformSampler(BaseSampler):
    def __init__(self, df, pcm, n_samples, rnd_low, rnd_high, seed=None):
        super().__init__(df, pcm, n_samples, seed)
        self._rnd_low_base = rnd_low
        self._rnd_high_base = rnd_high
        self.rnd_low = self._rnd_low_base
        self.rnd_high = self._rnd_high_base

    def sample(self, threshold, drow_sum, cmin, cmax, idx):
        # if drow_sum < cmin:
        #     self.rnd_low += 0.01
        # if drow_sum > cmax:
        #     self.rnd_high -= 0.01
        new_drow = self.rng.uniform(self.rnd_low, self.rnd_high, self.n_inputs)

        # Apply the correlations
        new_drow = self.apply_correlations(new_drow, self.pcm, threshold)
        # new_drow *= (self.df.mean().mean() / new_drow.mean() * 2)
        # new_drow = new_drow.clip(0, 1)
        return new_drow

    def reset(self):
        self.rnd_low = self._rnd_low_base
        self.rnd_high = self._rnd_high_base


class DirichletSampler(BaseSampler):
    def __init__(self, df, pcm, n_samples, alpha=1.2, seed=None):
        super().__init__(df, pcm, n_samples, seed)
        self.alpha = alpha

    def sample(self, threshold, drow_sum, cmin, cmax, idx):
        sample = (
            self.rng.dirichlet(np.ones(self.n_inputs // 2) * self.alpha, 2)
            * self.n_inputs
            // 2
            * self.rng.random((2, 1))
        )
        if idx <= self.n_samples // 4:
            sample = -sample + 1
        elif idx <= self.n_samples // 2:
            sample[0, :] = -sample[0, :] + 1
        elif idx <= self.n_samples // 4 * 3:
            sample[1, :] = -sample[1, :] + 1

        new_drow = sample.flatten(order="F")

        # Apply the correlations
        new_drow = self.apply_correlations(new_drow, self.pcm, threshold)

        # return new_drow / new_drow.max() * 1.5
        return (new_drow * 0.5).clip(-1.25, 1.25)


class NormalSampler(BaseSampler):
    def __init__(self, df, pcm, n_samples, seed=None):
        super().__init__(df, pcm, n_samples, seed)

    def sample(self, threshold, drow_sum, cmin, cmax, idx):
        sample = self.rng.normal(
            loc=0, scale=self.df.std().std() * 2, size=self.n_inputs
        )
        sample.clip(-1.25, 1.25)
        # sample = self.rng.multivariate_normal()
        # self.rng.multivariate_normal(self.df.mean().fillna(0).values,np.corrcoef(self.df.values.transpose()))
        sample = self.apply_correlations(sample, self.pcm, threshold)
        return sample


class DistributionSampler(BaseSampler):
    def __init__(self, df, pcm):
        super().__init__(df, pcm)

    def sample(self, threshold, drow_sum, cmin, cmax, idx):
        pass
