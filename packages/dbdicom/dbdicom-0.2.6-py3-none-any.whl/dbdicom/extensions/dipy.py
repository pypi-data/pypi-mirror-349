import numpy as np
from dipy.align.imwarp import SymmetricDiffeomorphicRegistration
from dipy.align.metrics import CCMetric, EMMetric, SSDMetric
from dipy.align.imaffine import MutualInformationMetric, AffineRegistration, transform_centers_of_mass
from dipy.align.transforms import (
    TranslationTransform2D, RigidTransform2D, AffineTransform2D,
    TranslationTransform3D, RigidTransform3D, AffineTransform3D)
from dipy.align import center_of_mass
from dipy.align.vector_fields import (
    warp_3d_nn, 
    warp_3d, 
    warp_2d_nn,
    warp_2d, 
    invert_vector_field_fixed_point_3d, 
    invert_vector_field_fixed_point_2d,
)

from dipy.segment.mask import median_otsu as median_otsu_np
import dbdicom.extensions.vreg as vreg


def median_otsu(series, **kwargs):

    # Get arrays for fixed and moving series
    array, headers = series.array('SliceLocation', pixels_first=True)

    # Apply Otsu
    mask = np.empty(array.shape)
    cnt=0
    for z in range(array.shape[2]):
        for k in range(array.shape[3]):
            cnt+=1
            series.status.progress(cnt, array.shape[2]*array.shape[3], 'Applying Otsu segmentation..')
            image = np.squeeze(array[:,:,z,k])
            array[:,:,z,k], mask[:,:,z,k] = median_otsu_np(image, **kwargs)

    # Create new series
    masked_series = series.new_sibling(suffix='masked')
    otsu_mask = series.new_sibling(suffix ='otsu mask')

    # Set values and return
    masked_series.set_array(array, headers, pixels_first=True)
    otsu_mask.set_array(mask, headers, pixels_first=True)
    return masked_series, otsu_mask


def align_center_of_mass_3d(moving, fixed):

    # Get arrays for fixed and moving series
    array_moving, headers_moving = moving.array(sortby='SliceLocation', pixels_first=True, first_volume=True)
    array_fixed = vreg.array(fixed, on=moving, sortby='SliceLocation', pixels_first=True, first_volume=True)

    # Coregister fixed and moving slice-by-slice
    identity = np.eye(4)
    array_moving, _ = center_of_mass(array_moving, array_fixed, static_affine=identity, moving_affine=identity)

    # Create new series
    moved = moving.new_sibling(suffix='aligned')
    moved.set_array(array_moving, headers_moving, pixels_first=True)

    return moved


def coregister_translation_3d(moving, fixed):

    # Get arrays for fixed and moving series
    array_moving, headers_moving = moving.array(sortby='SliceLocation', pixels_first=True, first_volume=True)
    array_fixed = vreg.array(fixed, on=moving, sortby='SliceLocation', pixels_first=True, first_volume=True)

    # Set up coregistration
    metric = MutualInformationMetric(nbins=32, sampling_proportion=None,)
    affreg = AffineRegistration(
        metric = metric,
        level_iters = [10000, 1000, 100],
        sigmas = [3.0, 1.0, 0.0],
        factors = [4, 2, 1],
    )
    transform = TranslationTransform3D()
    params0 = None

    # Perform coregistration
    moving.message('Performing coregistration..')
    mapping = affreg.optimize(array_fixed, array_moving, transform, params0)
    coregistered = mapping.transform(array_moving, 'linear')

    # Save as DICOM
    coreg = moving.new_sibling(suffix='translated')
    coreg.set_array(coregistered, headers_moving, pixels_first=True)

    return coreg


def coregister_rigid_3d(moving, fixed):

    # Get arrays for fixed and moving series
    array_moving, headers_moving = moving.array(sortby='SliceLocation', pixels_first=True, first_volume=True)
    array_fixed = vreg.array(fixed, on=moving, sortby='SliceLocation', pixels_first=True, first_volume=True)

    # Setup coregistration
    metric = MutualInformationMetric(nbins=32, sampling_proportion=None)
    affreg = AffineRegistration(
        metric = metric,
        level_iters = [10000, 1000, 100],
        sigmas = [3.0, 1.0, 0.0],
        factors = [4, 2, 1],
    )
    transform = RigidTransform3D()
    params0 = None

    # Perform coregistration
    moving.message('Performing coregistration..')
    mapping = affreg.optimize(array_fixed, array_moving, transform, params0)
    coregistered = mapping.transform(array_moving, 'linear')

    # Save as DICOM
    coreg = moving.new_sibling(suffix='rigid transform')
    coreg.set_array(coregistered, headers_moving, pixels_first=True)
    return coreg



def coregister_affine_3d(moving, fixed):

    # Get arrays for fixed and moving series
    array_moving, headers_moving = moving.array(sortby='SliceLocation', pixels_first=True, first_volume=True)
    array_fixed = vreg.array(fixed, on=moving, sortby='SliceLocation', pixels_first=True, first_volume=True)

    # Setup coregistration
    metric = MutualInformationMetric(nbins=32, sampling_proportion=None)
    affreg = AffineRegistration(
        metric = metric,
        level_iters = [10000, 1000, 100],
        sigmas = [3.0, 1.0, 0.0],
        factors = [4, 2, 1],
    )
    transform = AffineTransform3D()
    params0 = None

    # Perform coregistration
    moving.message('Performing coregistration..')
    mapping = affreg.optimize(array_fixed, array_moving, transform, params0)
    coregistered = mapping.transform(array_moving, 'linear')

    # Save as DICOM
    coreg = moving.new_sibling(suffix='rigid transform')
    coreg.set_array(coregistered, headers_moving, pixels_first=True)
    return coreg


def coregister_deformable_3d(moving, fixed, **kwargs):

    # Get arrays for fixed and moving series
    array_moving, headers_moving = moving.array(sortby='SliceLocation', pixels_first=True, first_volume=True)
    array_fixed = vreg.array(fixed, on=moving, sortby='SliceLocation', pixels_first=True, first_volume=True)

    # Perform coregistration
    moving.status.message('Performing coregistration..')
    array_moving, deformation = _coregister_arrays(array_fixed, array_moving, **kwargs)

    # Create new series
    coreg = moving.new_sibling(suffix='registered')
    deform = moving.new_sibling(suffix='deformation field')

    # Set arrays
    coreg.set_array(array_moving, headers_moving, pixels_first=True)
    for dim in range(deformation.shape[-1]):
        deform.set_array(deformation[...,dim], headers_moving, pixels_first=True)

    # Return coregistered images and deformation field
    return coreg, deform


def align_center_of_mass_2d(moving, fixed):

    # Get arrays for fixed and moving series
    zaxis = 'SliceLocation'
    array_moving = moving.pixel_values(zaxis)
    array_fixed = vreg.pixel_values(fixed, zaxis, on=moving)

    # Coregister fixed and moving slice-by-slice
    id = np.eye(3)
    for z in range(array_moving.shape[2]):
        moving.progress(z+1, array_moving.shape[2], 'Performing coregistration..')
        c_of_mass = transform_centers_of_mass(array_fixed[:,:,z], id, array_moving[:,:,z], id)
        array_moving[:,:,z] = c_of_mass.transform(array_moving[:,:,z])

    # Save as DICOM (new API)
    coreg = moving.copy(SeriesDescription=moving.SeriesDescription + ' [coreg]')
    coreg.set_pixel_values(array_moving, coords=moving.coords(zaxis))
    return coreg



def coregister_translation_2d(moving, fixed):

    # # Get arrays for fixed and moving series (old API)
    # array_moving, headers_moving = moving.array(sortby='SliceLocation', pixels_first=True, first_volume=True)
    # array_fixed = vreg.array(fixed, on=moving, sortby='SliceLocation', pixels_first=True, first_volume=True)

    # Get arrays for fixed and moving series (new API)
    #zaxis = ('SliceLocation',)
    zaxis = 'SliceLocation'
    array_moving = moving.pixel_values(zaxis)
    array_fixed = vreg.pixel_values(fixed, zaxis, on=moving)

    # Set up coregistration
    metric = MutualInformationMetric(nbins=32, sampling_proportion=None)
    affreg = AffineRegistration(
        metric = metric,
        level_iters = [10000, 1000, 100],
        sigmas = [3.0, 1.0, 0.0],
        factors = [4, 2, 1],
    )
    transform = TranslationTransform2D()

    # Coregister fixed and moving slice-by-slice
    for z in range(array_moving.shape[2]):
        moving.progress(z+1, array_moving.shape[2], 'Performing coregistration..')
        # Coregister slice
        params0 = None
        mapping = affreg.optimize(array_fixed[:,:,z], array_moving[:,:,z], transform, params0)
        array_moving[:,:,z] = mapping.transform(array_moving[:,:,z], 'linear')

    # # Save as DICOM (old API)
    # coreg = moving.new_sibling(suffix= 'registered')
    # coreg.set_array(array_moving, headers_moving, pixels_first=True)

    # Save as DICOM (new API)
    coreg = moving.copy(SeriesDescription=moving.SeriesDescription + ' [coreg]')
    coreg.set_pixel_values(array_moving, coords=moving.coords(zaxis))
    return coreg


def coregister_rigid_2d(moving, fixed):

    # Get arrays for fixed and moving series
    array_moving, headers_moving = moving.array(sortby='SliceLocation', pixels_first=True, first_volume=True)
    array_fixed = vreg.array(fixed, on=moving, sortby='SliceLocation', pixels_first=True, first_volume=True)

    # Set up coregistration
    metric = MutualInformationMetric(nbins=32, sampling_proportion=None)
    affreg = AffineRegistration(
        metric = metric,
        level_iters = [10000, 1000, 100],
        sigmas = [3.0, 1.0, 0.0],
        factors = [4, 2, 1],
    )
    transform = RigidTransform2D()

    # Coregister fixed and moving slice-by-slice
    for z in range(array_moving.shape[2]):
        moving.status.progress(z+1, array_moving.shape[2], 'Performing coregistration..')
        # Coregister slice
        params0 = None
        mapping = affreg.optimize(array_fixed[:,:,z], array_moving[:,:,z], transform, params0)
        array_moving[:,:,z] = mapping.transform(array_moving[:,:,z], 'linear')

    # Save as DICOM
    coreg = moving.new_sibling(suffix= 'registered')
    coreg.set_array(array_moving, headers_moving, pixels_first=True)
    return coreg


def coregister_affine_2d(moving, fixed):

    # Get arrays for fixed and moving series
    array_moving, headers_moving = moving.array(sortby='SliceLocation', pixels_first=True, first_volume=True)
    array_fixed = vreg.array(fixed, on=moving, sortby='SliceLocation', pixels_first=True, first_volume=True)

    # Set up coregistration
    metric = MutualInformationMetric(nbins=32, sampling_proportion=None)
    affreg = AffineRegistration(
        metric = metric,
        level_iters = [10000, 1000, 100],
        sigmas = [3.0, 1.0, 0.0],
        factors = [4, 2, 1],
    )
    transform = AffineTransform2D()

    # Coregister fixed and moving slice-by-slice
    for z in range(array_moving.shape[2]):
        moving.status.progress(z+1, array_moving.shape[2], 'Performing coregistration..')
        # Coregister slice
        params0 = None
        mapping = affreg.optimize(array_fixed[:,:,z], array_moving[:,:,z], transform, params0)
        array_moving[:,:,z] =mapping.transform(array_moving[:,:,z], 'linear')

    # Save as DICOM
    coreg = moving.new_sibling(suffix= 'registered')
    coreg.set_array(array_moving, headers_moving, pixels_first=True)
    return coreg



def coregister_deformable_2d(moving, fixed, **kwargs):

    # Get arrays for fixed and moving series
    array_moving, headers_moving = moving.array(sortby='SliceLocation', pixels_first=True, first_volume=True)
    array_fixed = vreg.array(fixed, on=moving, sortby='SliceLocation', pixels_first=True, first_volume=True)

    # Coregister fixed and moving slice-by-slice
    deformation = np.empty(array_moving.shape + (2,))
    for z in range(array_moving.shape[2]):
        moving.status.progress(z+1, array_moving.shape[2], 'Performing coregistration..')
        coreg, deform = _coregister_arrays(array_fixed[:,:,z], array_moving[:,:,z], **kwargs)
        array_moving[:,:,z] = coreg
        deformation[:,:,z,:] = deform

    # Create new series
    coreg = moving.new_sibling(suffix= 'registered')
    deform = moving.new_sibling(suffix='deformation field')

    # Set values & return
    coreg.set_array(array_moving, headers_moving, pixels_first=True)
    for dim in range(deformation.shape[-1]):
        deform.set_array(deformation[...,dim], headers_moving, pixels_first=True)
    return coreg, deform






def invert_deformation_field(deformation_field, **kwargs):

    # Get array
    array, headers = deformation_field.array('SliceLocation', pixels_first=True)

    # Invert
    array = _invert_deformation_field_array(array, deformation_field.status, **kwargs)

    # Create new series
    inv = deformation_field.new_sibling(suffix='inverse')
    inv.set_array(array, headers, pixels_first=True)

    return inv


def warp(image, deformation_field, **kwargs):

    # Get arrays
    array, headers = image.array('SliceLocation', pixels_first=True, first_volume=True)
    array_deform = vreg.array(deformation_field, on=image, sortby='SliceLocation', pixels_first=True)

    # Perform warping
    array = _warp_array(array, array_deform, image.status, **kwargs)

    # Create new series
    warped = image.new_sibling(suffix='warped')
    warped.set_array(array, headers, pixels_first=True)

    return warped



### ARRAY functions




def _invert_deformation_field_array(array, status, max_iter=10, tolerance=0.1):
    status.message('Inverting deformation field..')
    dim = array.shape[-1]
    d_world2grid = np.eye(dim+1)
    spacing = np.ones(dim)
    if dim==3:
        return invert_vector_field_fixed_point_3d(array, d_world2grid, spacing, max_iter, tolerance)
    elif dim==2:
        nslices = array.shape[2]
        for z in range(nslices):
            status.progress(z+1, nslices, 'Inverting deformation field..')
            array[:,:,z] = invert_vector_field_fixed_point_2d(array[:,:,z], d_world2grid, spacing, max_iter, tolerance)
        return array
    else:
        msg = 'This series is not a deformation field.'
        msg += 'A deformation field must have either 2 or 3 components.'
        raise ValueError(msg)


def _warp_array(array, deform, status, interpolate=True):
    status.message('Warping array..')
    dim = deform.shape[-1]
    if dim==3:
        if interpolate:
            return warp_3d(array, deform)
        else:
            return warp_3d_nn(array, deform)
    elif dim==2:
        nslices = deform.shape[2]
        for z in range(nslices):
            status.progress(z+1, nslices, 'Warping array..')
            if interpolate:
                array[:,:,z] = warp_2d(array[:,:,z], deform[:,:,z,:])
            else:
                array[:,:,z] = warp_2d_nn(array[:,:,z], deform[:,:,z,:])
        return array
    else:
        msg = 'This series is not a deformation field.'
        msg += 'A deformation field must have either 2 or 3 components.'
        raise ValueError(msg)

      
def _coregister_arrays(fixed, moving, transformation='Symmetric Diffeomorphic', metric="Cross-Correlation"):
    """
    Coregister two arrays and return coregistered + deformation field 
    """

    dim = fixed.ndim

    # 3D registration does not seem to work with smaller slabs
    # Exclude this case
    if dim == 3:
        if fixed.shape[-1] < 6:
            msg = 'The 3D volume does not have enough slices for 3D registration. \n'
            msg += 'Try 2D registration instead.'
            raise ValueError(msg)
        
    # Define the metric
    if metric == "Cross-Correlation":
        sigma_diff = 3.0    # Gaussian Kernel
        radius = 4          # Window for local CC
        metric = CCMetric(dim, sigma_diff, radius)
    elif metric == 'Expectation-Maximization':
        metric = EMMetric(dim, smooth=1.0)
    elif metric == 'Sum of Squared Differences':
        metric = SSDMetric(dim, smooth=4.0)
    else:
        msg = 'The metric ' + metric + ' is currently not implemented.'
        raise ValueError(msg) 

    # Define the deformation model
    if transformation == 'Symmetric Diffeomorphic':
        level_iters = [200, 100, 50, 25]
        sdr = SymmetricDiffeomorphicRegistration(metric, level_iters, inv_iter=50)
    else:
        msg = 'The transform ' + transformation + ' is currently not implemented.'
        raise ValueError(msg) 

    # Perform the optimization, return a DiffeomorphicMap object
    mapping = sdr.optimize(fixed, moving)

    # Get forward deformation field
    deformation_field = mapping.get_forward_field()

    # Warp the moving image
    warped_moving = mapping.transform(moving, 'linear')

    return warped_moving, deformation_field
