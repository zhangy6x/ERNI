import _plot_functions
import _functions
import matplotlib.pyplot as plt
import periodictable as pt
from periodictable import constants
import numpy as np


# Parameters

_input = 'UO3'
_natural_ele = 'Y'
thick_mm = 0.26  # mm
# ratios = [[0, 0, 15, 85], [1, 0, 0]]
sample_density = 0.7875  #2  # 0.7875  # pt.elements.isotope(element).density  # g/cm3  https://en.wikipedia.org/wiki/Cadmium

_database = 'ENDF_VIII'
energy_max = 300  # max incident energy in eV
energy_min = 0  # min incident energy in eV
energy_sub = 100
sub_x = energy_sub * (energy_max - energy_min)  # subdivided new x-axis
_multi_element = 'N'
_energy_x_axis = 'Y'  # 1 means plot x-axis as energy in eV
_trans_y_axis = 'N'  # 1 means plot y-axis as transmission
_plot_each_iso_contribution = 'N'  # 1 means plot each isotope's contribution
_plot_each_ele_contribution = 'Y'  # 1 means plot each element's contribution
_plot_mixed = 'Y'  # 1 means plot mixed resonance

formula, natural_mix_dict, ratio_array = _functions.input2formula(_input, _natural_ele)  # Function called to parse input formula and return elements and ratios
elements = list(dict.keys(formula))
ratios = list(dict.values(formula))
for _each_ in elements:
    ratio_array[_each_] = []
print(ratio_array)
mass_iso_ele_dict = {}  # For number of atoms per cm3 calculation
y_i_iso_ele_dicts = {}  # For transmission calculation at isotope lever
y_i_iso_ele_sum_dict = {}  # For transmission calculation at element lever
df_raw_dict = {}  # Raw sigma data for elements and isotopes
isotopes_dict = {}  # List all isotopes for each element involved
for _each_ in elements:
    _element = _each_
    ele_at_ratio = formula[_each_] / sum(ratios)
    # Get pre info (isotopes, abundance, mass, density) of each element from the formula
    isotopes_dict[_each_], iso_abundance, iso_density, iso_mass, abundance_dict, density_dict, mass_dict, file_names = \
        _plot_functions.get_pre_data(_database, _element)

    mass_iso_ele_dict[_each_] = _plot_functions.get_atom_per_cm3(iso_abundance, iso_mass, ele_at_ratio,
                                                                 natural_mix_dict[_each_], ratio_array[_each_])

    x_energy, y_i_iso_ele_dict, y_i_iso_ele_sum, df_raw_dict[_each_] = \
        _plot_functions.get_xy(isotopes_dict[_each_], file_names, energy_min, energy_max, iso_abundance,
                               sub_x, ele_at_ratio, natural_mix_dict[_each_], ratio_array[_each_])
    y_i_iso_ele_dicts[_each_] = y_i_iso_ele_dict #list(dict.values(y_i_iso_ele_dict))
    y_i_iso_ele_sum_dict[_each_] = y_i_iso_ele_sum

print(mass_iso_ele_dict)
# Get Number of atoms per unit volume (#/cm^3)
# mixed_atoms_per_cm3_dict = {}
# for _each_ in elements:
#     mixed_atoms_per_cm3_dict[_each_] = sample_density[_each_] * pt.constants.avogadro_number/mass_iso_ele_dict[_each_]
mass_iso_ele_list = list(dict.values(mass_iso_ele_dict))
mass_iso_ele_sum = sum(np.array(mass_iso_ele_list))
mixed_atoms_per_cm3 = sample_density * pt.constants.avogadro_number/mass_iso_ele_sum
# Use function: mixed_atoms_per_cm3 = _functions.atoms_per_cm3(density=sample_density, mass=mass_iso_ele_sum)


# print(y_i_iso_ele_dicts.items())
# print(y_i_iso_ele_sum_dict)
# print(df_raw_dict)
keys = list(dict.keys(y_i_iso_ele_sum_dict))
yi_values = list(dict.values(y_i_iso_ele_sum_dict))
yi_values_sum = sum(yi_values)
# print(y_i_iso_ele_dicts['U'])
print(isotopes_dict)
trans_sum = _functions.sig2trans_quick(thick_mm, mixed_atoms_per_cm3, yi_values_sum)
y_trans_tot = trans_sum

if _plot_each_iso_contribution == 'N':
    _plot_functions.plot_xy(elements, _energy_x_axis, _trans_y_axis, _plot_each_ele_contribution, _plot_mixed,
                            x_energy, y_trans_tot, thick_mm, mixed_atoms_per_cm3, y_i_iso_ele_sum_dict)
else:
    for _each_ in elements:
        isotopes = isotopes_dict[_each_]
        _plot_functions.plot_xy(isotopes, _energy_x_axis, _trans_y_axis, _plot_each_iso_contribution, _plot_mixed,
                                x_energy, y_trans_tot, thick_mm, mixed_atoms_per_cm3, y_i_iso_ele_dicts[_each_])



