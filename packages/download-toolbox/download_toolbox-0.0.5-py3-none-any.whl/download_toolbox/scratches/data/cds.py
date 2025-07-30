def _single_toolbox_download(self,
                             var_config: object,
                             req_dates: object,
                             download_path: object):
    """Implements a single download from CDS Toolbox API

    :param var:
    :param level: the pressure level to download
    :param req_dates: the request dates
    :param download_path:
    """

    logging.debug("Processing {} dates".format(len(req_dates)))
    var_prefix, level = var_config.prefix, var_config.level

    params_dict = {
        "realm": "c3s",
        "project": "app-c3s-daily-era5-statistics",
        "version": "master",
        "workflow_name": "application",
        "kwargs": {
            "dataset": "reanalysis-era5-single-levels",
            "product_type": "reanalysis",
            "variable": self.dataset.cdi_map[var_prefix],
            "pressure_level": "-",
            "statistic": "daily_mean",
            "year": req_dates[0].year,
            "month": sorted(list(set([r.month for r in req_dates]))),
            "frequency": "1-hourly",
            "time_zone": "UTC+00:00",
            "grid": "0.25/0.25",
            "area": {
                "lat": [min([self.dataset.location.bounds[0],
                             self.dataset.location.bounds[2]]),
                        max([self.dataset.location.bounds[0],
                             self.dataset.location.bounds[2]])],
                "lon": [min([self.dataset.location.bounds[1],
                             self.dataset.location.bounds[3]]),
                        max([self.dataset.location.bounds[1],
                             self.dataset.location.bounds[3]])],
            },
        },
    }

    if level:
        params_dict["kwargs"]["dataset"] = \
            "reanalysis-era5-pressure-levels"
        params_dict["kwargs"]["pressure_level"] = level

    logging.debug("params_dict: {}".format(pformat(params_dict)))
    result = self.client.service(
        "tool.toolbox.orchestrator.workflow",
        params=params_dict)

    try:
        logging.info("Downloading data for {}...".format(var_config.name))
        logging.debug("Result: {}".format(result))

        location = result[0]['location']
        res = requests.get(location, stream=True)

        logging.info("Writing data to {}".format(download_path))

        with open(download_path, 'wb') as fh:
            for r in res.iter_content(chunk_size=1024):
                fh.write(r)

        logging.info("Download completed: {}".format(download_path))

    except Exception as e:
        logging.exception("{} not deleted, look at the "
                          "problem".format(download_path))
        raise RuntimeError(e)
s