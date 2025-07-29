from dataclasses import dataclass

import lmfit as lm
import numpy as np
from numpy import linspace,exp
from scipy.special import erf
import scipy.constants as scc
import pySWXF.refl_funs as refl_funs
import pySWXF.xray_utils as xray_utils




def get_prof(amp, zcen, sig):
    '''
    get_prof(zcen, amp, sig)
    function to return real space profile from
    arrays of zcenters, amplitudes and widths
    '''
    zspan = max(zcen) - min(zcen)
    zmin = min(zcen)-2*zspan
    zmax = max(zcen) +2*zspan
    zrange = linspace(zmin, zmax, 2**10)
    prof = zrange*0
    for thisz, thisa, thiss in zip(zcen, amp, sig):
        prof += thisa*exp(-(zrange-thisz)**2/2/thiss**2)
    return zrange, prof

def get_dprof(amp, zcen, sig):
    '''
    get_prof(zcen, amp, sig)
    function to return real space profile from
    arrays of zcenters, amplitudes and widths
    '''
    zspan = max(zcen) - min(zcen)
    zmin = min(zcen)-2*zspan
    zmax = max(zcen) +2*zspan
    zrange = linspace(zmin, zmax, 2**10)
    prof = zrange*0
    lasta = amp[0]
    prof = np.abs(prof) + lasta
    for  thisz, thisa, thiss  in zip(zcen, amp[1:], sig):
        prof += (thisa-lasta)*(erf((thisz-zrange)/thiss)+1)/2
        lasta = thisa
    return zrange, prof

@dataclass
class BiReflParams:
    I0: float
    dalpha: float
    res: float
    alpha_foot: float
    sig_sio2: float
    rho_h: float
    rho_a: float
    d_b: float
    d_h: float
    d_m: float
    sig: float
    d_sio2: float

def get_layers(params: BiReflParams) -> list:
    """
    Generates a list of layers with their properties for use in X-ray reflectivity simulations.

    Parameters:
    - params (BiReflParams): Data class containing the parameters for the layers.

    Returns:
    - list: A list of tuples representing each layer and its properties.
    """
    d_a = (params.d_b - 2 * params.d_h - params.d_m) / 2
    # Define constants
    d_sio = 1.0  # Thickness of the SiO layer in angstroms
    sig_sio = 1.5  # Roughness of the SiO layer
    sig_si = 1.5  # Roughness of the Si layer

    # Define the layers
    layers = [
        ('H2O', 1, 0, 0),
        ('CH2', params.rho_h, params.d_h, params.sig),
        ('CH2', params.rho_a, d_a, params.sig),
        ('CH2', 0.1, params.d_m, params.sig),
        ('CH2', params.rho_a, d_a, params.sig),
        ('CH2', params.rho_h, params.d_h, params.sig),
        ('SiO2', 2.30, params.d_sio2, params.sig_sio2),
        ('SiO', 1.86, d_sio, sig_sio),
        ('Si', 2.34, 0, sig_si)
    ]

    return layers

def bi_refl(params: BiReflParams, alpha: np.ndarray, E0: float) -> np.ndarray:
    """
    Calculates the bilayer reflectivity.

    Parameters:
    - params (BiReflParams): Data class containing all parameters for the reflectivity calculation.
    - alpha (np.ndarray): Incident angles.
    - E0 (float): Incident energy.

    Returns:
    - np.ndarray: Reflectivity as a function of incident angle.
    """
    layers = get_layers(params)
    npt = int(np.ceil(4 * params.res / np.min(np.diff(alpha))))
    if params.res == 0:
        _, refl, _,_= refl_funs.reflection_matrix(alpha - params.dalpha, E0, layers)
        y = params.I0 * np.abs(refl[:, 0])**2
    else:
        res_points = np.linspace(-1.5 * params.res, 1.5 * params.res, npt)
        norm = 0
        psum = 0
        for dres in res_points:
            A = np.exp(-dres**2 / 2 / params.res**2)
            norm += A
            x = alpha - params.dalpha - dres
            _, refl, _, _ = refl_funs.reflection_matrix(x, E0, layers)
            psum += np.abs(refl[:, 0])**2
        y = psum * params.I0 / norm
        y[alpha - params.dalpha < params.alpha_foot] *= alpha[alpha - params.dalpha < params.alpha_foot] / params.alpha_foot
    return y

def bi_refl_wrapper(alpha, E0, **params_dict):
    params = BiReflParams(**{k: v for k, v in params_dict.items()})
    return bi_refl(params, alpha, E0)

# Define the lmfit model
bi_refl_model = lm.Model(bi_refl_wrapper, independent_vars=['alpha', 'E0'])

# Define function to print out real space profile
def get_bi_realspace(params,  E0):
    birefl_param_names = set(BiReflParams.__annotations__.keys())
    lay_params_dict = {k: v.value for k, v in params.items() if k in birefl_param_names}
    lay_params = BiReflParams(**lay_params_dict)
    layers = get_layers(lay_params)
    print(layers)
    amp = []
    zcen = []
    sig_i = []
    for lay in layers:
        amp.append(xray_utils.rho_to_rhoe(lay[0], lay[1], E0) * scc.angstrom**3)
        if len(zcen) > 0:
            zcen.append(zcen[-1] - lay[2])
        else:
            zcen.append(lay[2])
        sig_i.append(lay[3])
    zcen = np.array(zcen)
    amp = np.array(amp)
    sig_i = np.array(sig_i)
    print(zcen)
    print(amp)
    print(sig_i)
    zrange, prof = get_dprof(amp , zcen[:-1] , sig_i[1:] )
    return zrange, prof, amp, zcen, sig_i, layers

# def print_bi_edensity(params,E0):
#     rho_H = params['rho_H'].value
#     rho_A = params['rho_A'].value
#     rho_e_H = xray_utils.rho_to_rhoe('CH2',rho_H,E0)*scc.angstrom**3
#     rho_e_A = xray_utils.rho_to_rhoe('CH2',rho_A,E0)*scc.angstrom**3
#     print(f'Acyl density = {rho_A:5.2f} electron density = {rho_e_A:5.2f}')
#     print('Headgroup density = {rho_H:5.2f} electron density = {rho_e_H:5.2f}')