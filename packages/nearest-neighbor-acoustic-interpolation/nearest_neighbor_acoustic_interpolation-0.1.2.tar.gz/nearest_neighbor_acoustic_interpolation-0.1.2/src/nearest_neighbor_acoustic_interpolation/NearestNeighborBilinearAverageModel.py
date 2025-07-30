# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 14:37:06 2020

@author: frankmobley

"""

import numpy as np
import pandas as pd
from scipy import ndimage as nd


def bi_linear_average(starting_mesh, tolerance, measured_data, m_x_idx, m_y_idx, x, y):
    """
    This computes the bi-linear average of the mesh until the RMSE reaches the
    tolerance passed as an argument.

    Parameters
    ----------
    starting_mesh : double array-like
        the starting dense matrix determined from the nearest neighbor
    tolerance : double
        The minimum error level to finish the averaging
    measured_data : DataFrame
        A data frame with the X, Y, La values for each of the measured points
    m_x_idx : array-like double
        The X indices for where to insert the measured levels
    m_y_idx : array-like double
        The X indices for where to insert the measured levels
    x : array-like double
        The array of x values
    y : array-like double
        The array of y values

    Returns
    -------
    The dense matrix smoothed

    """

    zz = starting_mesh.copy()

    #   Perform the iterative smoothing
    rmse = 100
    i = 0

    zz_last = zz.copy()

    while rmse > tolerance:
        #   Replace the data with the measured information
        zz[m_y_idx, m_x_idx] = measured_data.iloc[:, 2].values

        print('Starting iteration {}'.format(i + 1))

        #   Loop through the array and create an approximate of the
        #   interpolation
        print('iterating over the surface')

        npts = 3
        for xidx in range(len(x)):
            for yidx in range(len(y)):

                #   Add the central point
                nn_mean = 0  # zz[yidx,xidx]

                #   Set the count for the points in the average
                n = 0

                #   Determine the span in each direction
                span = int((npts - 1) / 2)

                #   Try to determine the value for the lower index of the y-axis
                ylo, yhi = _check_y_indices(y, yidx-span, yidx + span)

                #   Now the x-axis
                xlo, xhi = _check_y_indices(x, xidx-span, xidx + span)

                for p in range(ylo, yhi + 1):
                    for q in range(xlo, xhi + 1):
                        nn_mean += zz[p, q]
                        n += 1

                zz[yidx, xidx] = nn_mean / n

        #   Compute the error between this and the previous surface
        rmse = np.std(np.std(zz - zz_last, axis=1))

        print('RMSE:{:.5f}\n***************************'.format(rmse))

        #   Copy the current surface to the previous surface
        zz_last = zz.copy()
        i += 1
    return zz, i, rmse


def _check_y_indices(array, lo_idx, hi_idx):
    if lo_idx < 0:
        lo_idx = 0

    if hi_idx >= len(array):
        hi_idx = len(array) - 1

    return lo_idx, hi_idx


def nearest_neighbor_near_field_model(x, y, z, measured_data, smoothing_error_tolerance: float = 1e-5):
    """
    This will build the nearest neighbor model through application of the image
    processing and then bi-linear smoothing

    Parameters
    ----------
    :param smoothing_error_tolerance: The error tolerance that terminate the smoothing
    :type smoothing_error_tolerance: double
    :param x: The values of the dependent axis
    :type x : double, array-like
    :param y: The values of the independent axis
    :type y : double, array-like
    :param z: the 2-D surface with the values set to z[y,x]
    :type z : double, array-like
    :param measured_data: Contains sparse measured data for the replacement within the smoothing
        algorithm
    :type measured_data: Pandas DataFrame

    Returns
    -------
    Model of the surface levels


    """

    #   Find the index within the desired mesh where these data fall
    measured_x_index = np.zeros(shape=(measured_data.shape[0],), dtype=int)
    measured_y_index = np.zeros(shape=(measured_data.shape[0],), dtype=int)

    #   Find the indices for the measured data
    for i in range(measured_data.shape[0]):
        try:
            xidx = np.nonzero(x - measured_data.iloc[i, 0] >= 0)[0][0]
            yidx = np.nonzero(y - measured_data.iloc[i, 1] >= 0)[0][0]

            z[yidx, xidx] = measured_data.iloc[i, 2]

            measured_x_index[i] = xidx
            measured_y_index[i] = yidx
        except IndexError:
            print('Error at the {}th element'.format(i))

    #   Perform the nearest neighbor approximation
    invalid = np.isin(z, -999)
    ind = nd.distance_transform_edt(
        invalid,
        return_distances=False,
        return_indices=True
        )

    #   Assign the value based on the selected indices
    z = z[tuple(ind)]

    #   Smooth the coarse surface
    smoothed_zz, iterations, error = bi_linear_average(
        z,
        smoothing_error_tolerance,
        measured_data,
        measured_x_index,
        measured_y_index,
        x,
        y
        )

    #   Return a dictionary of the data that was calculated within the model
    return {'x': x,
            'y': y,
            'surface': smoothed_zz,
            'coarse_surface': z,
            'iterations': iterations,
            'RMSE_error': error}
