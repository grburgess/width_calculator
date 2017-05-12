__author__='grburgess'

import numpy as np
import matplotlib.pyplot as plt


class WidthCalculator(object):
    def __init__(self, model=None, results=None, with_errors=False):
        """
        Calculates the spectral width of a model based of the papers
        by Yu et al. 2015 and Axelsson et al. 2015.
        
        Can use a general model or a fitted model.

        :param results: 3ML analysis results
        :param model: 3ML likelihood model
        :param with_errors: (switch) calculate with errors, EXPERIMENTAL
        """

        # decide which type of input we have


        
        if model is None:
            assert results is None, 'Can only input model or results. Not both!'
            
            self._model = results.optimized_model

        elif model is not None:

            self._model = model

        else:

            raise RuntimeError('Your inputs make no sense!')

        self._with_errors = with_errors

        if with_errors:
            # Gather the parameter variates

            arguments = {}

            for par in self._model.parameters.values():

                if par.free:

                    this_name = par.name

                    this_variate = results.get_variates(par.path)

                    # Do not use more than 1000 values (would make computation too slow for nothing)

                    if len(this_variate) > 1000:

                        this_variate = np.random.choice(
                            this_variate, size=1000)

                    arguments[this_name] = this_variate

            # Prepare the error propagator function

            # energy range to calculate the width over

        self._energy_range = np.logspace(np.log10(8.), np.log10(40000.), 1E3)

        # get the point source flux (only one source)
        if with_errors:
            self._function = results.propagate(
                self._model.point_sources[self._model.get_point_source_name(
                    0)].spectrum.main.shape.evaluate_at, **arguments)

        else:

            self._function = lambda ee: self._model.get_point_source_fluxes(0, ee)

        # the vFv spectrum of the model

        self._vfv_spectrum = self._energy_range**2 * self._model.get_point_source_fluxes(
            0, self._energy_range)

        self._calculate_width_axelsson()
        self._calculate_width_yu()

    def _calculate_width_axelsson(self):
        """
        Calculates the width based off of Axelsson et al. 2015

        """

        # get the maximum flux and its location. The calculate
        # the half way point
        
        max_flux = self._vfv_spectrum.max()
        idx_max = self._vfv_spectrum.argmax()
        half_max = 0.5 * max_flux

        # now find at which energy the halfway point hits
        
        idx1 = abs(self._vfv_spectrum[:idx_max] - half_max).argmin()
        idx2 = abs(self._vfv_spectrum[idx_max:] - half_max).argmin() + idx_max

        e1 = self._energy_range[idx1]
        e2 = self._energy_range[idx2]

        # calculate the width
        # in the paper they have written base e, but then I
        # cannot reporduce the width
        
        self._width = np.log10(e2 / e1)

    def _calculate_width_yu(self):
        """
        Calculates the width based off of Yu et al. 2015
        """
        # again find the max flux and its location
        
        max_flux = self._vfv_spectrum.max()
        idx_max = self._vfv_spectrum.argmax()

        # we explicitly define the peak as the
        # max vFv point
        
        ep = self._energy_range[idx_max]

        # normalize the energies
        
        e_left = ep * .1
        e_right = ep * 3.

        # find the vFv point of those energies
        
        vFv_left = e_left**2 * self._function(e_left)
        vFv_right = e_right**2 * self._function(e_right)

        # now switch to log space
        # Yu et al. use base e log
        
        x_left = np.log(e_left / ep)
        y_left = np.log(vFv_left / max_flux)

        x_right = np.log(e_right / ep)
        y_right = np.log(vFv_right / max_flux)

        # now construct the triangle
        
        d2 = (x_right - x_left)**2 + (y_right - y_left)**2
        a2 = (np.log(1) - x_left)**2 + (np.log(1) - y_left)**2
        b2 = (np.log(1) - x_right)**2 + (np.log(1) - y_right)**2

        # get the angle
        
        arg = -((d2 - a2 - b2) / (2. * np.sqrt(a2) * np.sqrt(b2)))

        angle = np.arccos(arg)

        self._angle = np.rad2deg(angle)

    @property
    def width(self):
        """
        :return: the width of the spectrum
        """

        return self._width

    @property
    def angle(self):
        """
        :return: the angle in degrees
        """
        return self._angle
