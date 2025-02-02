import pprint
from resonance import Resonance
import _utilities

# Global parameters
_energy_min = 1e-5
_energy_max = 800
_energy_step = 0.01
# Input sample name or names as str, case sensitive
_layer_1 = 'IAg'
_thickness_1 = 0.025 # mm
# _density_1 = 8 # g/cm3 deviated due to porosity

_layer_2 = 'Ag'
_thickness_2 = 0.025 # mm

o_reso = Resonance(energy_min=_energy_min, energy_max=_energy_max, energy_step=_energy_step)
o_reso.add_layer(formula=_layer_1, thickness=_thickness_1)
# o_reso.add_layer(formula=_layer_2, thickness=_thickness_2)

pprint.pprint(o_reso)
o_reso.plot(all_elements=True, transmission=False)
