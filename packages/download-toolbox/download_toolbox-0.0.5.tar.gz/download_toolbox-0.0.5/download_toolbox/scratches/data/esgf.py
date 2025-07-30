class CMIP6PyESGFDownloader(Downloader):
    """Climate downloader to provide CMIP6 reanalysis data from ESGF APIs

    Useful CMIP6 guidance: https://pcmdi.llnl.gov/CMIP6/Guide/dataUsers.html

    :param identifier: how to identify this dataset
    :param source: source ID in ESGF node
    :param member: member ID in ESGF node
    :param nodes: list of ESGF nodes to query
    :param experiments: experiment IDs to download
    :param frequency: query parameter frequency
    :param table_map: table map for
    :param grid_map:
    :param grid_override:
    :param exclude_nodes:

    "MRI-ESM2-0", "r1i1p1f1", None
    "EC-Earth3", "r2i1p1f1", "gr"

    """

    # HTTP 500 search_node: object = "https://esgf.ceda.ac.uk/esg-search"

    def __init__(self,
                 *args,
                 search_node: object = "https://esgf-data.dkrz.de/esg-search",
                 **kwargs):
        super().__init__(*args, **kwargs)

        self._connection = None
        self._search_node = search_node

        lm = LogonManager()
        lm.logoff()
        lm.is_logged_on()

    def _single_download(self,
                         var_config: object,
                         req_dates: object,
                         download_path: object):
        """Overridden CMIP implementation for downloading from DAP server

        Due to the size of the CMIP set and the fact that we don't want to make
        1850-2100 yearly requests for all downloads, we have a bespoke and
        overridden download implementation for this.

        :param var_prefix:
        :param level:
        :param req_dates:
        """

        var, level = var_config.prefix, var_config.level

        query = {
            'source_id': self.dataset.source,
            'member_id': self.dataset.member,
            'frequency': self.dataset.frequency,
            'variable_id': var,
            'table_id': self.dataset.table_map[var],
            'grid_label': self.dataset.grid_map[var],
        }

        results = []
        self._connection = SearchConnection(self._search_node, distrib=True)

        for experiment_id in self.dataset.experiments:
            logging.info("Querying ESGF for experiment {} for {}".format(experiment_id, var))
            query['experiment_id'] = experiment_id
            ctx = self._connection.new_context(facets="variant_label,data_node", **query)
            ds = ctx.search()[0]
            results = ds.file_context().search()

            if len(results) > 0:
                logging.info("Found {} {} {} results from ESGF search".format(len(results), experiment_id, var))
                results = [f.download_url for f in results]
                break

        if len(results) == 0:
            logging.warning("NO RESULTS FOUND for {} from ESGF search".format(var))
        else:
            cmip6_da = None

            logging.info("\n".join(results))

            try:
                # http://xarray.pydata.org/en/stable/user-guide/io.html?highlight=opendap#opendap
                # Avoid 500MB DAP request limit
                cmip6_da = xr.open_mfdataset(results,
                                             combine='by_coords',
                                             chunks={'time': '499MB'}
                                             )[var]

                cmip6_da = cmip6_da.sel(time=slice(req_dates[0],
                                                   req_dates[-1]))

                # TODO: possibly other attributes, especially with ocean vars
                if level:
                    cmip6_da = cmip6_da.sel(plev=int(level) * 100)

                cmip6_da = cmip6_da.sel(lat=slice(self.dataset.location.bounds[2],
                                                  self.dataset.location.bounds[0]))
            except OSError as e:
                logging.exception("Error encountered: {}".format(e),
                                  exc_info=False)
            else:
                self.save_temporal_files(var_config, cmip6_da)
                cmip6_da.close()

        self._connection.close()
