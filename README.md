# GRB spectral width calculator
asdfadf
The is a simple class to read 3ML models and compute the spectral width as defined in [Axelsson et al. (2015)](https://www.google.de/url?sa=t&rct=j&q=&esrc=s&source=web&cd=6&cad=rja&uact=8&ved=0ahUKEwjk16Dx4enTAhXkIJoKHQL7BVMQFghAMAU&url=http%3A%2F%2Fmnras.oxfordjournals.org%2Fcontent%2F447%2F4%2F3150.full.pdf&usg=AFQjCNH_8tNkwPmkVjkard_TBgYYHmmsaw&sig2=uJKobN1Tk-GMkFGiVtSt2w) and [Yu et al. 2015](https://www.google.de/url?sa=t&rct=j&q=&esrc=s&source=web&cd=3&cad=rja&uact=8&ved=0ahUKEwiE3fSL4unTAhVLGZoKHaf3DP0QFggyMAI&url=https%3A%2F%2Fwww.aanda.org%2Farticles%2Faa%2Fabs%2F2015%2F11%2Faa27015-15%2Faa27015-15.html&usg=AFQjCNGCsfuQiWDi20sKpsE83XXfQZRSsw&sig2=aZTep4JMZaUtvvzvEdDcbw). 

## Install

```
$> git clone https://github.com/grburgess/width_calculator
$> cd width_calculator
$> python setup.py install
```

## Example usage

The width calculator works on either 3ML models from spectral catalogs or from fits.

```python

from threeML import *
from width_calculator import *

# create a toy model

band = Band()
model = Model( PointSource('test',0,0,spectral_shape=band))

wc = WidthCalculator(model=model)

wc.angle
wc.width

```

## Citing

If you find this code useful in your research, please consider citing the authors of the original work linked above as well as 



