import numpy as np
import matplotlib.pyplot as plt


class SpectralWidth(object):
    def __init__(self, name, model):

        self._name = name

        self._model = model

        self._energy_range = np.logspace(np.log10(8.), np.log10(40000.), 1E5)

        self._function = self._model.point_sources[self._name].spectrum.main

        try:

            self._alpha = self._model.point_sources[
                self._name].spectrum.main.Band.alpha.value

            self._beta = self._model.point_sources[
                self._name].spectrum.main.Band.beta.value

            self._xp = self._model.point_sources[
                self._name].spectrum.main.Band.xp.value

            self._spectral_difference = self._alpha - self._beta

            self._is_band = True

        except:

            self._is_band = False

        self._vfv_spectrum = self._energy_range**2 * self._function(
            self._energy_range)

        self._calculate_width()

    def _calculate_width(self):

        #fig, ax = plt.subplots()

        self._max = self._vfv_spectrum.max()
        self._idx_max = self._vfv_spectrum.argmax()
        self._half_max = 0.5 * self._max

        self._idx1 = abs(self._vfv_spectrum[:self._idx_max] -
                         self._half_max).argmin()
        self._idx2 = abs(self._vfv_spectrum[self._idx_max:] -
                         self._half_max).argmin() + self._idx_max

        self._e1 = self._energy_range[self._idx1]
        self._e2 = self._energy_range[self._idx2]

        self._width = np.log10(self._e2 / self._e1)

    def display_width(self):

        fig, ax = plt.subplots()

        ax.loglog(self._energy_range, self._vfv_spectrum)
        ax.vlines(
            self._energy_range[self._idx_max],
            self._half_max,
            self._max,
            linestyles="--")

        ax.hlines(
            self._half_max,
            self._energy_range[self._idx1],
            self._energy_range[self._idx2],
            colors='r')

        ax.set_xlabel(r'Energy [keV]')

        ax.set_ylabel(r'$\nu F_{\nu}$')

    @property
    def name(self):

        return self._name

    @property
    def width(self):

        return self._width

    @property
    def spectral_difference(self):

        if self._is_band:

            return self._spectral_difference

    @property
    def alpha(self):

        return self._alpha

    @property
    def beta(self):

        return self._beta

    @property
    def xp(self):

        return self._xp
