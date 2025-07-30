import pandas as pd
from .schemas import sample_peak_timeseries_schema
from ..logging_config import logger  # Import the shared logger
from ..mascope_data.access import (
    get_mjw_mode,
)

MJW_DEV_MODE = get_mjw_mode()  # Get the MJW_DEV_MODE environment variable


class SampleTimeSeriesExtension:
    """
    Sample-level timeseries related extension
    for MascopeDataWrapper -dataset.
    """

    def __init__(self):
        self.sample_timeseries_cache = {}

    def get_sample_peak_timeseries(
        self,
        peak_mz: float,
        sample_file_id: str | None = None,
        peak_mz_tolerance_ppm: float | None = None,
    ) -> pd.DataFrame:
        """
        Get the peak timeseries for a given sample_file_id and peak m/z.
        If sample_file_id is None, it retrieves the timeseries for all sample files in the dataset
        for given peak_mz in tolerance.
        The sample-level timeseries data is cached to avoid redundant fetches.

        :param peak_mz: The m/z value of the peak to retrieve.
        :param sample_file_id: The ID of the sample file to retrieve.
        :param peak_mz_tolerance_ppm: The tolerance in ppm for the peak m/z.
        :return: A DataFrame containing the peak timeseries data.
        """

        def fetch_and_cache_timeseries(
            peak_mz: float, sample_file_id: str, peak_mz_tolerance_ppm: float | None
        ) -> pd.DataFrame:
            """
            Fetch and cache timeseries data for a given sample_file_id and peak m/z.
            """
            tol = peak_mz_tolerance_ppm or 0.0
            print(
                f"Fetching timeseries for sample_file_id={sample_file_id},"
                f" peak_mz={peak_mz}, tolerance={tol}"
            )
            # Prepare cache structure
            cache = self.sample_timeseries_cache.setdefault(sample_file_id, {})
            cache_mz = cache.setdefault(peak_mz, {})

            # Try to find a cached tolerance that is <= requested tolerance
            available_tols = sorted(
                cache_mz.keys()
            )  # Sort available tolerances low to high
            best_tol = None
            # Find the nearest available tolerance that is <= requested tolerance
            for cached_tol in available_tols:
                if float(cached_tol) <= tol:
                    best_tol = cached_tol
            if best_tol is not None:
                logger.debug(
                    f"Using cached data for peak_mz={peak_mz}, tolerance={best_tol} in "
                    f"sample_file_id={sample_file_id} (requested tolerance: {tol}).",
                )
                return cache_mz[best_tol]

            # Fetch data using the data-source browser
            timeseries = self.data_source.load_sample_file_peak_timeseries(  # pylint: disable=E1101
                sample_file_id=sample_file_id,
                peak_mz=peak_mz,
                peak_mz_tolerance_ppm=peak_mz_tolerance_ppm,
            )
            if not timeseries.empty:
                cache_mz[tol] = timeseries
                logger.debug(
                    "Cached data for peak_mz=%s, tolerance=%s in sample_file_id=%s.",
                    peak_mz,
                    tol,
                    sample_file_id,
                )
            return timeseries

        if sample_file_id is None:
            logger.debug(
                "Fetching timeseries for all sample files for peak_mz=%s", peak_mz
            )
            sample_timeseries_list = []

            for (
                sample_id
            ) in self.match_samples.sample_file_id.unique():  # pylint: disable=E1101
                logger.debug("Fetching timeseries for sample_file_id=%s", sample_id)
                sample_timeseries = fetch_and_cache_timeseries(
                    peak_mz=peak_mz,
                    sample_file_id=sample_id,
                    peak_mz_tolerance_ppm=peak_mz_tolerance_ppm,
                )
                if not sample_timeseries.empty:
                    sample_timeseries_list.append(sample_timeseries)

            if sample_timeseries_list:
                combined_timeseries = pd.concat(
                    sample_timeseries_list, axis=0, ignore_index=True
                )
                if MJW_DEV_MODE:
                    return sample_peak_timeseries_schema.validate(combined_timeseries)
                return combined_timeseries

            return pd.DataFrame()

        logger.debug(
            "Fetching timeseries for sample_file_id=%s and peak_mz=%s",
            sample_file_id,
            peak_mz,
        )
        timeseries = fetch_and_cache_timeseries(
            peak_mz=peak_mz,
            sample_file_id=sample_file_id,
            peak_mz_tolerance_ppm=peak_mz_tolerance_ppm,
        )
        if MJW_DEV_MODE:
            return sample_peak_timeseries_schema.validate(timeseries)
        return timeseries
