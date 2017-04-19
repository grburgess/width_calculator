import numpy as np
import matplotlib.pyplot as plt


class WidthCalculator(object):
    def __init__(self,model=None, results=None, with_errors=False):
        """
        
        Calculates the spectral width of a model based of the papers...

        :param name: model name
        :param model: 3ML likelihood model
        """

        if model is None:
        
            self._model = results.optimized_model

        elif model is not None:

            self._model = model
            
            
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

                        this_variate = np.random.choice(this_variate, size=1000)

                    arguments[this_name] = this_variate

            # Prepare the error propagator function


        # energy range to calculate the width over

        self._energy_range = np.logspace(np.log10(8.), np.log10(40000.), 1E3)

        # get the point source flux (only one source)
        if with_errors:
            self._function = results.propagate(self._model.point_sources[self._model.get_point_source_name(0)].spectrum.main.shape.evaluate_at, **arguments)

        else:

            self._function = lambda ee: self._model.get_point_source_flux(0,ee)
            
        # the vFv spectrum of the model

        self._vfv_spectrum = self._energy_range**2 * self._model.get_point_source_flux(0,self._energy_range)

        self._calculate_width_axelsson()
        self._calculate_width_yu()
        

    def _calculate_width_axelsson(self):


        max_flux = self._vfv_spectrum.max()
        idx_max = self._vfv_spectrum.argmax()
        half_max = 0.5 * max_flux

        idx1 = abs(self._vfv_spectrum[:idx_max] -
                         half_max).argmin()
        idx2 = abs(self._vfv_spectrum[idx_max:] -
                         half_max).argmin() + idx_max

        e1 = self._energy_range[idx1]
        e2 = self._energy_range[idx2]

        self._width = np.log10(e2 / e1)


    def _calculate_width_yu(self):

        max_flux = self._vfv_spectrum.max()
        idx_max = self._vfv_spectrum.argmax()
        
        ep = self._energy_range[idx_max]

        
        e_left   = ep * .1
        e_right =  ep * 3.

        vFv_left = e_left**2 * self._function(e_left)

        vFv_right = e_right**2 * self._function(e_right)

        x_left = np.log(e_left / ep)
        y_left = np.log(vFv_left / max_flux)

        x_right = np.log(e_right / ep)
        y_right = np.log(vFv_right / max_flux)

        d2 = (x_right - x_left)**2 + (y_right - y_left)**2
        a2 = (np.log(1) - x_left)**2 + (np.log(1)-y_left)**2
        b2 = (np.log(1) - x_right)**2 + (np.log(1)-y_right)**2
        
      

        arg = -((d2 - a2 - b2)/(2. * np.sqrt(a2)* np.sqrt(b2)))
        
       
        angle = np.arccos(arg)

        self._angle = np.rad2deg(angle)
        
        
        #fig, ax = plt.subplots()
        
        
        #ax.plot(np.log(self._energy_range/ep),np.log(self._vfv_spectrum/max_flux))
        #ax.plot([x_left,x_right,np.log(1.),x_left],[y_left,y_right,np.log(1.),y_left],'-')

 
    @property
    def width(self):

        return self._width

    @property
    def angle(self):

        return self._angle

  
