# Importing annotations to handle or sign in import type hints
from __future__ import annotations

import timeit
import os
import numpy as np
import nibabel as nib
import pandas as pd
import matplotlib.pyplot as plt
import vreg


from dbdicom.record import Record
from dbdicom.ds.create import new_dataset
import dbdicom.utils.image as image


class Instance(Record):

    name = 'SOPInstanceUID'

    def keys(self):
        return [self.key()]

    def parent(self):
        #uid = self.manager.register.at[self.key(), 'SeriesInstanceUID']
        uid = self.manager._at(self.key(), 'SeriesInstanceUID')
        return self.record('Series', uid, key=self.key())

    def children(self, **kwargs):
        return

    def new_child(self, **kwargs): 
        return

    def _copy_from(self, record, **kwargs):
        return

    def copy_to_series(self, series):
        uid = self.manager.copy_instance_to_series(self.key(), series.keys(), series)
        return self.record('Instance', uid)

    def pixel_values(self):
        return self.get_pixel_array()

    def set_pixel_values(self, array):
        self.set_pixel_array(array)
        
    def set_dataset(self, dataset):
        self._key = self.manager.set_instance_dataset(self.uid, dataset, self.key())

    def map_to(self, target):
        return map_to(self, target)

    def map_mask_to(self, target):
        return map_mask_to(self, target)


    def export_as_png(self, path, center=None, width=None, colormap=None):
        # Export image in png format.
        if center is None or width is None:
            c, w = self.window
        if center is None:
            center = c
        if width is None:
            width = w
        if colormap is None:
            colormap = self.colormap
        if colormap is None:
            colormap = 'gray'

        vmin = center - width/2
        vmax = center + width/2
        array = np.transpose(self.array())
        plt.imshow(array, cmap=colormap, vmin=vmin, vmax=vmax)
        cBar = plt.colorbar()
        cBar.minorticks_on()
        filename = self.label()
        filename = os.path.join(path, filename + '.png')
        plt.savefig(fname=filename)
        plt.close()


    def export_as_csv(self, path):
        # Export 2D pixel Array in csv format
        table = np.transpose(self.array())
        cols = ['Column' + str(x) for x in range(table.shape[0])]
        rows = ['Row' + str(y) for y in range(table.shape[1])]
        filepath = self.label()
        filepath = os.path.join(path, filepath + '.csv')
        df = pd.DataFrame(table, index=rows, columns=cols)
        df.to_csv(filepath)


    def export_as_nifti(self, path, affine=None):
        # Export series as a single Nifty file
        ds = self.get_dataset()
        if affine is None:
            affine = ds.get_values('affine_matrix')
        array = self.array()
        dicomHeader = nib.nifti1.Nifti1DicomExtension(2, ds)
        niftiObj = nib.Nifti1Image(array, image.affine_to_RAH(affine))
        niftiObj.header.extensions.append(dicomHeader)
        filepath = self.label()
        filepath = os.path.join(path, filepath + '.nii')
        nib.save(niftiObj, filepath)


    def export_as_npy(self, path):
        # Export instance as a single NPY file
        array = self.array()
        filepath = self.label()
        filepath = os.path.join(path, filepath + '.npy')
        with open(filepath, 'wb') as f:
            np.save(f, array)


    def BGRA_array(self):
        return image.BGRA(
            self.get_pixel_array(),
            self.lut, 
            width = self.WindowWidth,
            center = self.WindowCenter,
        )
    
    def volume(self):
        return vreg.volume(self.pixel_values(), 
                           self.affine())
    
    def set_volume(self, volume:vreg.Volume3D):
        self.set_pixel_values(np.squeeze(volume.values))
        self.set_affine(volume.affine)
    
    def affine(self):
        return image.affine_matrix(self.ImageOrientationPatient, 
                                   self.ImagePositionPatient, 
                                   self.PixelSpacing, 
                                   self.SliceThickness)
    
    def set_affine(self, affine):
        p = image.dismantle_affine_matrix(affine)
        self.read()
        #self.SpacingBetweenSlices = p['SpacingBetweenSlices']
        self.SliceThickness = p['SliceThickness']
        self.PixelSpacing = p['PixelSpacing']
        self.ImageOrientationPatient = p['ImageOrientationPatient']
        self.ImagePositionPatient = p['ImagePositionPatient']
        self.SliceLocation = np.dot(p['ImagePositionPatient'], p['slice_cosine'])
        self.clear()


    # OBSOLETE API

    def array(self):  # obsolete replace by pixel_values
        return self.get_pixel_array()

    def get_pixel_array(self):  # obsolete replace by pixel_values
        ds = self.get_dataset()
        return ds.get_pixel_array()

    def set_array(self, array): # obsolete replace by set_pixel_values
        self.set_pixel_array(array)

    def set_pixel_array(self, array): # obsolete replace by set_pixel_values
        ds = self.get_dataset()
        if ds is None:
            ds = new_dataset('MRImage')
        ds.set_pixel_array(array)
        in_memory = self.key() in self.manager.dataset
        self.set_dataset(ds) 
        # This bit added ad-hoc because set_dataset() places the datset in memory
        # So if the instance is not in memory, it needs to be written and removed again
        if not in_memory:
            self.clear()      


def map_to(source, target):
    """Map non-zero image pixels onto a target image.
    
    Overwrite pixel values in the target"""

    dss = source.get_dataset()
    dst = target.get_dataset()

    # Create a coordinate array for all pixels in the source
    coords = np.empty((dss.Rows*dss.Columns, 3), dtype=np.uint16)
    for x in range(dss.Columns):
        for y in range(dss.Rows):
            coords[x*dss.Columns+y,:] = [x,y,0]

    # Apply coordinate transformation from source to target
    affineSource = dss.get_affine_matrix()
    affineTarget = dst.get_affine_matrix()
    sourceToTarget = np.linalg.inv(affineTarget).dot(affineSource)
    coords_target = nib.affines.apply_affine(sourceToTarget, coords)

    # Interpolate (nearest neighbour) and extract inslice coordinates
    coords_target = np.round(coords_target, 3).astype(int)
    xt = tuple([c[0] for c in coords_target if c[2] == 0])
    yt = tuple([c[1] for c in coords_target if c[2] == 0])
    xs = tuple([c[0] for c in coords])
    ys = tuple([c[1] for c in coords])

    ## COORDINATES DO NOT MATCH UP because of c[2] = 0 condition
    ## Needs a different indexing approach

    # Set values in the target image
    source_array = dss.get_pixel_array()
    target_array = np.zeros((dst.Columns, dst.Rows))
    target_array[(xt, yt)] = source_array[(xs, ys)]
    # for masking map values to {0, 1}
    result = source.new_sibling()
    result.set_pixel_array(target_array)

    return result

# Obsolete
def map_mask_to(record, target):
    """Map non-zero image pixels onto a target image.
    Overwrite pixel values in the target"""
    dsr = record.get_dataset()
    dst = target.get_dataset()
    array = dsr.map_mask_to(dst)
    result = target.copy_to(record.parent()) # inherit geometry header from target
    result.set_pixel_array(array)
    return result





