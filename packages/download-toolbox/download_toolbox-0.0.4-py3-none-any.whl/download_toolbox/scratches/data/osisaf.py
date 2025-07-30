    def __init__(self,
                 *args,
                 additional_invalid_dates: object = (),
                 chunk_size: int = 10,
                 dates: object = (),
                 delete_tempfiles: bool = True,
                 download: bool = True,
                 dtype: object = np.float32,
                 **kwargs):
        super().__init__(*args, identifier="osisaf", **kwargs)

        self._chunk_size = chunk_size
        self._dates = dates
        self._delete = delete_tempfiles
        self._download = download
        self._dtype = dtype



    def download(self):
        """

        """

        ds = xr.open_mfdataset(data_files,
                               combine="nested",
                               concat_dim="time",
                               data_vars=["ice_conc"],
                               drop_variables=var_remove_list,
                               engine="netcdf4",
                               chunks=dict(time=self._chunk_size, ),
                               parallel=True)

        logging.debug("Processing out extraneous data")

        ds = ds.drop_vars(var_remove_list, errors="ignore")
        da = ds.resample(time="1D").mean().ice_conc

        da = da.where(da < 9.9e+36, 0.)  # Missing values
        da /= 100.  # Convert from SIC % to fraction

        for coord in ['lat', 'lon']:
            if coord not in da.coords:
                logging.warning("Adding {} vals to coords, as missing in "
                                "this the combined dataset".format(coord))
                da.coords[coord] = self._get_missing_coordinates(var,
                                                                 hs,
                                                                 coord)

        for date in da.time.values:
            day_da = da.sel(time=slice(date, date))

            if np.sum(np.isnan(day_da.data)) > 0:
                logging.warning("NaNs detected, adding to invalid "
                                "list: {}".format(date))
                self._invalid_dates.append(pd.to_datetime(date))

        var_folder = self.get_data_var_folder(var)
        group_by = "time.year"

        for year, year_da in da.groupby(group_by):
            req_date = pd.to_datetime(year_da.time.values[0])

            year_path = os.path.join(
                var_folder, "{}.nc".format(getattr(req_date, "year")))
            old_year_path = os.path.join(
                var_folder, "old.{}.nc".format(getattr(req_date, "year")))

            if os.path.exists(year_path):
                logging.info("Existing file needs concatenating: {} -> {}".
                             format(year_path, old_year_path))
                os.rename(year_path, old_year_path)
                old_da = xr.open_dataarray(old_year_path)
                year_da = year_da.drop_sel(time=old_da.time,
                                           errors="ignore")
                year_da = xr.concat([old_da, year_da],
                                    dim="time").sortby("time")
                old_da.close()
                os.unlink(old_year_path)

            logging.info("Saving {}".format(year_path))
            year_da.compute()
            year_da.to_netcdf(year_path)


        self.missing_dates()

        if self._delete:
            for fpath in data_files:
                os.unlink(fpath)

