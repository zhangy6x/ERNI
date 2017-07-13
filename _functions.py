import numpy as np
import periodictable as pt
from periodictable import constants
import re
import os
import glob
import pandas as pd


def ev2lamda(energy_ev):  # function to convert energy in eV to angstrom
    energy_miliev = energy_ev * 1000
    lamda = np.sqrt(81.787/energy_miliev)
    return lamda


def time2lamda(time_tot_s, delay_us, source_to_detector_cm):  # function to convert time in us to angstrom
    time_tot_us = 1e6 * time_tot_s + delay_us
    lamda = 0.3956 * time_tot_us/source_to_detector_cm
    return lamda


def lamda2ev(lamda):  # function to convert angstrom to eV
    energy_miliev = 81.787/(lamda ** 2)
    energy_ev = energy_miliev/1000
    return energy_ev


def time2ev(time_tot_s, delay_us, source_to_detector_cm):  # function to convert time in us to energy in eV
    time_tot_us = 1e6 * time_tot_s + delay_us
    energy_miliev = 81.787/(0.3956 * time_tot_us/source_to_detector_cm) ** 2
    energy_ev = energy_miliev/1000
    return energy_ev


def atoms_per_cm3(density, mass):
    n_atoms = density * pt.constants.avogadro_number/mass
    print('Number of atoms per unit volume (#/cm^3): {}'.format(n_atoms))
    return n_atoms


def sig2trans(_thick_cm, _atoms_per_cm3, _ele_atomic_ratio, _sigma_b, _iso_atomic_ratio):
    neutron_transmission = np.exp(-1 * _thick_cm * _atoms_per_cm3 *
                                  _ele_atomic_ratio * _sigma_b * 1e-24 * _iso_atomic_ratio)
    return neutron_transmission


def sig2trans_quick(_thick_cm, _atoms_per_cm3, _sigma_portion_sum):
    neutron_transmission = np.exp(-1 * _thick_cm * _atoms_per_cm3 * 1e-24 * _sigma_portion_sum)
    return neutron_transmission


def sigl2trans_quick(_atoms_per_cm3, _sigma_l_portion_sum):
    neutron_transmission = np.exp(-1 * _atoms_per_cm3 * 1e-24 * _sigma_l_portion_sum)
    return neutron_transmission


def get_isotope_dict(_database, _element):
    main_dir = os.path.dirname(os.path.abspath(__file__))
    isotope_dicts = {}
    for _each in _element:
        path = main_dir + '/data_web/' + _database + '/' + _each + '*.csv'
        file_names = glob.glob(path)
        isotope_dict = {}
        for _i, file in enumerate(file_names):
            # Obtain element, z number from the basename
            _basename = os.path.basename(file)
            _name_number_csv = _basename.split('.')
            _name_number = _name_number_csv[0]
            _name = _name_number.split('-')
            _symbol = _name[1] + '-' + _name[0]
            isotope = str(_symbol)
            isotope_dict[isotope] = isotope
        isotopes = list(dict.values(isotope_dict))
        isotope_dicts[_each] = isotopes
    return isotope_dicts


def input2formula(_input):
    _input_parsed = re.findall(r'([A-Z][a-z]*)(\d*)', _input)
    _formula = {}
    # _natural_ele_boo_dict = {}
    # _natural_mix = {}
    # _ratio_array = {}
    for _element in _input_parsed:
        _element_list = list(_element)
        if _element_list[1] == '':
            _element_list[1] = 1
        _element_list[1] = int(_element_list[1])
        _formula[_element_list[0]] = _element_list[1]
        # _natural_ele_boo_dict[_element_list[0]] = 'Y'
    print('Parsed chemical formula: {}'.format(_formula))
    return _formula


def dict_key_list(_formula_dict):
    _elements = list(dict.keys(_formula_dict))
    return _elements


def dict_value_list(_formula_dict):
    _ratios = list(dict.values(_formula_dict))
    return _ratios


def boo_dict(_key_list, _y_or_n):
    _boo_dict = {}
    for key in _key_list:
        _boo_dict[key] = _y_or_n
    return _boo_dict


def thick_dict(_key_list, _thick_mm):
    _thick_dict = {}
    for key in _key_list:
        _thick_dict[key] = _thick_mm
    return _thick_dict


def density_dict(_key_list):
    _density_dict = {}
    for key in _key_list:
        _density_dict[key] = pt.elements.isotope(key).density
        # key can be element ('Co') or isotopes ('59-Co')
        # Unit: g/cm3
    return _density_dict


def empty_dict(_key_list):
    _empty_dicts = {}
    _empty_dict = {}
    for key in _key_list:
        _empty_dicts[key] = _empty_dict
    return _empty_dicts


def boo_dict_invert_by_key(_key_list, _boo_dict):
    for key in _key_list:
        if _boo_dict[key] == 'Y':
            _boo_dict[key] = 'N'
        else:
            _boo_dict[key] = 'Y'
    return _boo_dict


def dict_replace_value_by_key(_dict, _key_list, _value_list):
    p = 0
    for key in _key_list:
        _dict[key] = _value_list[p]
        p = p + 1
    return _dict


def formula_ratio_array(_input, _all_ele_boo_dict, ratios_dict):
    _natural_ele = {}
    _ratio_array = {}
    for _element in _input:
        _natural_ele[_element] = _all_ele_boo_dict[_element]
        if _all_ele_boo_dict[_element] == 'Y':
            _ratio_array[_element] = []
        else:
            _ratio_array[_element] = ratios_dict[_element]
    print('Natual elements? ', _natural_ele)
    print('Isotope ratio array: ', _ratio_array)
    return _ratio_array


def get_normalized_data(_filename):
    df = pd.read_csv(_filename, header=None, skiprows=1)
    data_array = np.array(df[1])
    data = data_array[:int(len(data_array)/2)]
    ob = data_array[int(len(data_array)/2):]
    normalized_array = data/ob
    # OB at the end of 2773
    return normalized_array


def get_normalized_data_slice(_filename, _slice):
    df = pd.read_csv(_filename, header=None, skiprows=1)
    data_array = np.array(df[1])
    data = data_array[:int(len(data_array)/2)]
    ob = data_array[int(len(data_array)/2):]
    normalized_array = data/ob
    normalized_array = normalized_array[_slice:]
    # OB at the end of 2773
    return normalized_array


def get_spectra(_filename, time_lamda_ev_axis, delay_us, source_to_detector_cm):
    df_spectra = pd.read_csv(_filename, sep='\t', header=None)
    time_array = (np.array(df_spectra[0]))
    # flux_array = (np.array(df_spectra[1]))
    if time_lamda_ev_axis == 'lamda':
        lamda_array = time2lamda(time_array, delay_us, source_to_detector_cm)
        return lamda_array
    if time_lamda_ev_axis == 'eV':
        ev_array = time2ev(time_array, delay_us, source_to_detector_cm)
        return ev_array
    if time_lamda_ev_axis == 'lamda':
        return time_array

def get_spectra_slice(_filename, time_lamda_ev_axis, delay_us, source_to_detector_cm, _slice):
    df_spectra = pd.read_csv(_filename, sep='\t', header=None)
    time_array = (np.array(df_spectra[0]))
    # flux_array = (np.array(df_spectra[1]))
    if time_lamda_ev_axis == 'lamda':
        lamda_array = time2lamda(time_array, delay_us, source_to_detector_cm)
        return lamda_array
    if time_lamda_ev_axis == 'eV':
        ev_array = time2ev(time_array, delay_us, source_to_detector_cm)
        ev_array = ev_array[_slice:]
        return ev_array
    if time_lamda_ev_axis == 'lamda':
        return time_array
