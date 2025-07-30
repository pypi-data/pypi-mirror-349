import os
import tempfile
from unittest import main
from unittest import TestCase

import cftime
import numpy as np
import xarray as xr
from hypothesis import given
from hypothesis import settings
from hypothesis import strategies as st

import optim_esm_tools as oet
from optim_esm_tools.analyze.combine_variables import VariableMerger


class TestPreprocessing(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.TemporaryDirectory()

    @classmethod
    def tearDownClass(cls) -> None:
        """Removes test data after tests are done."""
        cls.temp_dir.cleanup()

    @property
    def temp_path(self):

        return self.temp_dir.name

    def setup_dummy_dataset(self, file_name='data.nc', **kw):
        setup_kw = dict(
            len_x=10,
            len_y=30,
            len_time=20,
            start_year=2000,
            add_nans=False,
        )
        setup_kw.update(**kw)
        path = os.path.join(self.temp_path, file_name)
        if os.path.exists(path):
            return
        ds = oet._test_utils.complete_ds(**setup_kw)
        ds.attrs.update(dict(file=path))
        ds.to_netcdf(path)

    def test_simple_read_ds(self):
        raw = 'merged.nc'
        self.setup_dummy_dataset(raw)
        ds = oet.read_ds(self.temp_path, add_history=False, _skip_folder_info=True)

    def test_read_ds_wo_dask(self):
        raw = 'merged.nc'
        self.setup_dummy_dataset(raw)
        ds = oet.read_ds(self.temp_path, add_history=False, _skip_folder_info=True)
        ds2 = oet.read_ds(
            self.temp_path,
            add_history=False,
            _skip_folder_info=True,
            _inferred_fields_kw=dict(use_dask=False),
        )
        assert ds.equals(ds2)

    def test_read_ds_with_history(self):
        raw = 'merged.nc'
        self.setup_dummy_dataset(raw, len_time=20, start_year=2000)

        historical = 'hist.nc'
        self.setup_dummy_dataset(historical, len_time=20, start_year=2000 - 20)

        ds = oet.read_ds(
            self.temp_path,
            add_history=True,
            _skip_folder_info=True,
            _historical_path=os.path.join(self.temp_path, historical),
        )
        assert len(ds['time']) == 40

    def test_read_ds_with_history_with_overlaps(self):
        raw = 'merged.nc'
        self.setup_dummy_dataset(raw, len_time=20, start_year=2000)

        historical = 'hist_overlap.nc'
        self.setup_dummy_dataset(historical, len_time=30, start_year=2000 - 20)

        ds = oet.read_ds(
            self.temp_path,
            add_history=True,
            _skip_folder_info=True,
            _historical_path=os.path.join(self.temp_path, historical),
        )
        assert len(ds['time']) == 40

    def test_drop_duplicates(self):
        raw = 'merged.nc'
        self.setup_dummy_dataset(raw, len_time=20, start_year=2000)

        historical = 'hist_overlap.nc'
        self.setup_dummy_dataset(historical, len_time=30, start_year=2000 - 20)

        ds = xr.concat(
            [
                oet.load_glob(os.path.join(self.temp_path, raw)),
                oet.load_glob(os.path.join(self.temp_path, historical)),
            ],
            'time',
        ).sortby('time')
        ds.to_netcdf(path := os.path.join(self.temp_path, 'overlapping.nc'))
        ds.to_netcdf(path2 := os.path.join(self.temp_path, 'overlapping2.nc'))
        ds2 = oet.load_glob(path2)

        oet.analyze.pre_process._quick_drop_duplicates(ds, 39, 50, path)
        assert os.path.exists(f := os.path.join(self.temp_path, 'faulty_merged.nc'))
        os.remove(f)

        oet.analyze.pre_process._drop_duplicates_carefully(ds2, 39, 50, path2)
        assert os.path.exists(f := os.path.join(self.temp_path, 'faulty_merged.nc'))
        os.remove(f)

        assert oet.load_glob(path).equals(oet.load_glob(path2))

    def test_remap(self):
        raw = 'merged.nc'
        self.setup_dummy_dataset(raw)
        file = os.path.join(self.temp_path, raw)
        regrid_ds = oet.analyze.pre_process.remap(path=file, target_grid='n30')
        assert isinstance(regrid_ds, xr.Dataset)

        regrid_ds2 = oet.analyze.pre_process.remap(
            data_set=oet.load_glob(file),
            target_grid='n30',
        )
        assert isinstance(regrid_ds2, xr.Dataset)
        assert regrid_ds2.equals(regrid_ds)

        out_file = os.path.join(self.temp_path, 'merged_n30.nc')
        regrid_ds3_path = oet.analyze.pre_process.remap(
            path=file,
            target_grid='n30',
            out_file=out_file,
        )
        assert isinstance(regrid_ds3_path, str)
        assert oet.load_glob(regrid_ds3_path).equals(regrid_ds)


if __name__ == '__main__':
    main()
