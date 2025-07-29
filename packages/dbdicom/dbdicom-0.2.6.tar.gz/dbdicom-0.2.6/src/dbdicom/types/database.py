# Importing annotations to handle or sign in import type hints
from __future__ import annotations

from dbdicom.record import Record
from dbdicom.utils.files import gif2numpy

class Database(Record):

    name = 'Database'

    def loc(self):
        return self.manager._dbloc()
        # df = self.manager.register
        # return df.removed==False

    def _set_key(self):
        #if not self.manager.register.empty:
        if not self.manager._empty():
            self._key = self.manager._keys(0)
            #self._key = self.manager.register.index[0]
        else:
            self._key = None

    def close(self):
        return self.manager.close()

    def set_path(self,path):
        # Used in example of clear
        self.manager.path=path

    def parent(self):
        return

    def children(self, **kwargs):
        return self.patients(**kwargs)

    def new_child(self, dataset=None, **kwargs): 
        attr = {**kwargs, **self.attributes}
        return self.new_patient(**attr)
    
    def new_sibling(self, suffix=None, **kwargs):
        msg = 'You cannot create a sibling from a database \n'
        msg += 'You can start a new database with db.database()'
        raise RuntimeError(msg)

    def save(self, path=None):
        #self.manager.save('Database')
        self.manager.save()
        self.write(path)

    def restore(self, path=None):
        self.manager.restore()
        self.write(path)

    def open(self, path):
        self.manager.open(path)

    def close(self):
        return self.manager.close()

    def scan(self):
        self.manager.scan()

    def import_dicom(self, files):
        uids = self.manager.import_datasets(files)
        return uids is not None

    def import_nifti(self, files):
        self.manager.import_datasets_from_nifti(files)

    def import_gif(self, files):
        study = self.new_patient().new_study()
        for file in files:
            array = gif2numpy(file)
            series = study.new_series()
            series.set_array(array)
        return study

    def _copy_from(self, record):
        uids = self.manager.copy_to_database(record.uid, **self.attributes)
        if isinstance(uids, list):
            return [self.record('Patient', uid, **self.attributes) for uid in uids]
        else:
            return self.record('Patient', uids, **self.attributes)

    def zeros(*args, **kwargs): # OBSOLETE - remove
        return zeros(*args, **kwargs)

    # def export_as_dicom(self, path): 
    #     for child in self.children():
    #         child.export_as_dicom(path)

    # def export_as_png(self, path): 
    #     for child in self.children():
    #         child.export_as_png(path)

    # def export_as_csv(self, path): 
    #     for child in self.children():
    #         child.export_as_csv(path)


def zeros(database, shape, dtype='mri'): # OBSOLETE - remove
    study = database.new_study()
    return study.zeros(shape, dtype=dtype)



