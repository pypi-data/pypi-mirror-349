class AMSRDownloader(Downloader):
    def __init__(self,
                 *args,
                 chunk_size: int = 10,
                 dates: object = (),
                 delete_tempfiles: bool = True,
                 download: bool = True,
                 dtype: object = np.float32,
                 **kwargs):
        super().__init__(*args, identifier="amsr2_3125", **kwargs)

        self._chunk_size = chunk_size
        self._dates = dates
        self._delete = delete_tempfiles
        self._download = download
        self._dtype = dtype

    def download(self):
        """

        """



###
        # HAMBURG FTP download code

#         while len(dt_arr):
#             el = dt_arr.pop()
# 
#             date_str = el.strftime("%Y_%m_%d")
#             temp_path = os.path.join(
#                 self.get_data_var_folder(var, append=[str(el.year)]),
#                 "{}.nc.gz".format(date_str))
#             nc_path = temp_path[:-3]
# 
#             if not self._download:
#                 if os.path.exists(temp_path) and not os.path.exists(nc_path):
#                     logging.info("Decompressing {} to {}".
#                                  format(temp_path, nc_path))
#                     with open(nc_path, "wb") as fh_out:
#                         with gzip.open(temp_path, "rb") as fh_in:
#                             fh_out.write(fh_in.read())
#                     data_files.append(nc_path)
#             else:
#                 if not os.path.isdir(os.path.dirname(nc_path)):
#                     os.makedirs(os.path.dirname(nc_path), exist_ok=True)
# 
#                 if os.path.exists(temp_path) and not os.path.exists(nc_path):
#                     logging.info("Decompressing {} to {}".
#                                  format(temp_path, nc_path))
#                     with open(nc_path, "wb") as fh_out:
#                         with gzip.open(temp_path, "rb") as fh_in:
#                             fh_out.write(fh_in.read())
#                     data_files.append(nc_path)
#                     continue
# 
#                 if os.path.exists(nc_path):
#                     logging.debug("{} file exists, skipping".format(date_str))
#                     data_files.append(nc_path)
#                     continue
# 
#                 if not ftp:
#                     logging.info("FTP opening")
#                     ftp = FTP("ftp-projects.cen.uni-hamburg.de")
#                     ftp.login()
# 
#                 try:
#                     ftp.cwd(chdir_path)
# 
#                     if chdir_path not in cache:
#                         cache[chdir_path] = ftp.nlst()
# 
#                     cache_match = "{}_{}{:02d}{:02d}_res3.125_pyres.nc".\
#                         format(hemi_str, el.year, el.month, el.day)
#                     ftp_files = [el for el in cache[chdir_path]
#                                  if fnmatch.fnmatch(el, cache_match)
#                                  or fnmatch.fnmatch(el, "{}.gz".format(cache_match))]
# 
#                     if not len(ftp_files):
#                         logging.warning("File is not available: {}".
#                                         format(cache_match))
#                         continue
#                 except ftplib.error_perm:
#                     logging.warning("FTP error, possibly missing month chdir "
#                                     "for {}".format(date_str))
#                     continue
# 
#                 with open(temp_path, "wb") as fh:
#                     ftp.retrbinary("RETR {}".format(ftp_files[0]), fh.write)
# 
#                 is_gzipped = True
#                 with open(temp_path, "rb") as fh:
#                     if fh.read(2).decode("latin-1") == "CD":
#                         is_gzipped = False
# 
#                 if is_gzipped:
#                     logging.debug("Downloaded {}, decompressing to {}".
#                                   format(temp_path, nc_path))
#                     with open(nc_path, "wb") as fh_out:
#                         with gzip.open(temp_path, "rb") as fh_in:
#                             fh_out.write(fh_in.read())
#                 else:
#                     os.rename(temp_path, nc_path)
# 
#                 data_files.append(nc_path)
# 
#         if ftp:
#             ftp.quit()






        logging.debug("Files being processed: {}".format(data_files))

        if len(data_files):
            ds = xr.open_mfdataset([df for df in data_files
                                    if os.stat(df).st_size > 0],
                                   combine="nested",
                                   concat_dim="time",
                                   data_vars=["sea_ice_concentration"],
                                   drop_variables=var_remove_list,
                                   engine="netcdf4",
                                   chunks=dict(time=self._chunk_size,),
                                   parallel=True)

            logging.debug("Processing out extraneous data")

            da = ds.resample(time="1D").mean().sea_ice_concentration

            # Remove land mask @ 115 and invalid mask at 125
            da = da.where(da <= 100, 0.)
            da /= 100.  # Convert from SIC % to fraction

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

