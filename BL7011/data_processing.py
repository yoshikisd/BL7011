"""
    This file contains functions to process various CCD data acquired at
    the COSMIC Scattering BL7.0.1.1

    Stuff to add at some point:
    - Q conversion
    - Peak finding function
    - Peak broadening function
    - Consider making some kind of class out of calculate_dichroism

    Authors: Dayne Sasaki
"""
from typing import Tuple, Any

import numpy as np
from numpy import floating, half, ndarray, dtype
from numpy._typing import _16Bit

from BL7011 import file_processing as fp
import h5py
from scipy import ndimage as ndi

def calculate_dichroism(
        image_pol_a: np.ndarray,
        image_pol_b: np.ndarray,
        mode: str = 'difference'
) -> np.ndarray:
    """
    Calculates the dichroism image using two CCD images of different
    polarizations. This function assumes that you're using the appropriate
    pair of polarization images to calculate with (i.e., same dimensions,
    using both circular or linear polarized light)

    PARAMETERS
    -----
    image_pol_a: np.ndarray
        The first M x N polarization image
    image_pol_b: np.ndarray
        The second M x N polarization image
    mode: str
        The type of dichroism calculation to perform
        - 'difference': Calculates image as (image_pol_A - image_pol_B)
        - 'asymmetry': Calculates image as
                      (image_pol_A - image_pol_B) / (image_pol_A + image_pol_B)

    RETURNS
    -----
    np.ndarray of the calculated dichroism image
    """
    image_dichroism = image_pol_a - image_pol_b
    if mode is 'difference':
        return image_dichroism
    elif mode is 'asymmetry':
        return image_dichroism / (image_pol_a + image_pol_b)
    else:
        raise ValueError(
            'A calculation mode other than difference or asymmetry was '
            'specified')


def calculate_dichroism_from_file(file_pol_a: str,
                                  file_pol_b: str,
                                  *,
                                  mode: str = 'difference',
                                  correction: str = '',
                                  variable_stack: bool = False
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Calculates a dichroism image using two opposite polarization images loaded
    from HDF5 files.

    Parameters
    ----------
    file_pol_a: str
        File path of the first polarization image
    file_pol_b: str
        File path of the second polarization image
    mode: str
        The type of dichroism calculation to perform
        - 'difference': Calculates image as (image_pol_A - image_pol_B)
        - 'asymmetry': Calculates image as
                (image_pol_A - image_pol_B) / (image_pol_A + image_pol_B)
    correction: str
        Type of intensity correction to perform on the CCD image 'ccd_image'
            - Nothing : Return the raw ccd image
            - 'i0 blade' : Normalize ccd image by the right blade current
            - 'i0 rlrl' : Normalized by the XS111 RLRL diode (what is this?)
            - 'cps' : Normalize ccd image by acquisition time (counts per sec)
    variable_stack: bool
        Setting this to False will make the function calculate an average
        of an image stack (i.e., each frame in the stack represents multiple
        "redundant" camera exposure and do not have any parameters varying)


    Returns a tuple containing...
    -------
    im_dichro: np.ndarray
        The calculated dichroism image
    im_pol_a: np.ndarray
        The first polarization image
    im_pol_b: np.ndarray
        The second polarization image
    """
    # Load the two polarization images
    im_pol_a = fp.load_h5_image(file_pol_a, correction)
    im_pol_b = fp.load_h5_image(file_pol_b, correction)

    # If the user sets variable_stack = False, then average the
    # entire image stack to a single image
    if not variable_stack:
        im_pol_a = np.average(im_pol_a, axis=0)
        im_pol_b = np.average(im_pol_b, axis=0)

    # Calculate dichroism
    im_dichro = calculate_dichroism(im_pol_a, im_pol_b, mode=mode)

    return im_dichro, im_pol_a, im_pol_b


def align_detector_images(im_ref: str,
                          im_move: str,
                          path_ref: str,
                          path_move: str) -> tuple[np.ndarray]:
    """
    Aligns pairs of detector images given their respective detector translate
     and 2theta values stored in the 'instrument_1' dataset of the original
     h5 file.

    Parameters
    ----------
    im_ref: The reference image with size M x N
    im_move: The image that will be aligned to im_ref, with size M x N
    path_ref: The path to the HDF5 dataset associated with im_ref
        (i.e., h5_file['entry1']['instrument_1')
    path_move: The path to the HDF5 dataset associated with im_move

    Returns
    -------
    An M x N array containing the shifted im_move

    Thoughts: Implement theta, sample translate, and sample lift at some point
    """

    # Define a function to grab the different datasets from the HDF5 file
    def metadata_grabber(path:str) -> dict:
        # First, define an empty dictionary
        metadata = {}

        # Open up the h5 file and store the datasets in 'metadata'
        with h5py.File(path, 'r') as file:
            # Create a variable for the parent group that the datasets are
            # stored within
            grp = file['entry1']['instrument_1']
            metadata['det_translate'] = grp['labview_data']['det_translate'][0] * 1e-3
            metadata['detector_rotate'] = np.deg2rad(grp['labview_data']['detector_rotate'][0])
            metadata['detector_distance'] = grp['detector_1']['distance'][()]
            metadata['x_pixel_size'] = grp['detector_1']['x_pixel_size'][()]
            metadata['y_pixel_size'] = grp['detector_1']['y_pixel_size'][()]

        return metadata

    # Pull out the detector translate and 2theta positions
    md_ref = metadata_grabber(path_ref)
    md_move = metadata_grabber(path_move)

    # We assume here that the x and y pixel sizes are identical... complain
    # if they are not.
    if md_ref['x_pixel_size'] != md_ref['y_pixel_size']:
        raise ValueError('The x- and y-pixel sizes are not identical.')

    # Check that the parameters are consistent between the two images...
    # complain if they are not.
    if not ((md_ref['detector_distance'] == md_move['detector_distance'])
            or (md_ref['x_pixel_size'] == md_move['x_pixel_size'])):

        raise ValueError('Alignment cannot be performed between images with'
                         'two different sample-detector distances or pixel '
                         'sizes.')

    # Calculate the pixel shift needed to align the two images
    d = md_ref['detector_distance']
    tth_ref = md_ref['detector_rotate']
    tth_move = md_move['detector_rotate']
    pixel_size = md_ref['x_pixel_size']
    trans_ref = md_ref['det_translate']
    trans_move = md_move['det_translate']

    shift_translate = np.round((trans_move - trans_ref) / pixel_size)
    shift_tth = np.round((d * (np.sin(tth_move) - np.sin(tth_ref)))
                         / (np.cos(tth_ref) * pixel_size))

    # Apply the shift to the image
    return shift_tth, shift_translate