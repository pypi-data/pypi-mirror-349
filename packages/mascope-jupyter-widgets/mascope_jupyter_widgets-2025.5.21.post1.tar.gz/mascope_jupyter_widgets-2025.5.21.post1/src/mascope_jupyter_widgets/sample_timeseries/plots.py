from typing import List
import plotly.graph_objects as go
import pandas as pd
from colorcet import glasbey as colorvector
from ..mascope_data.wrapper import MascopeDataWrapper
from ..plot_tools import hover_string, auto_trace_name
from ..logging_config import logger


class SampleTimeSeriesPlotter:
    """
    Class containing functions to build sample-level timeseries-related traces
    by utilizing a dataset with SampleTimeSeriesExtension.
    """

    def __init__(self, dataset: MascopeDataWrapper):
        """
        Initialize the dataset.

        :param dataset: MascopeDataWrapper - dataset with
        SampleTimeSeriesExtension extension.
        :type dataset: MascopeDataWrapper
        """
        self.dataset = dataset
        self.hoverbox_columns = [
            "mz",
            "sample_item_id",
            "time",
            "height",
            "datetime",
            "sample_item_name",
            "sample_item_type",
            "instrument",
        ]  # List of HoverBox columns

    def get_sample_timeseries_traces(
        self,
        peak_mz: float,
        sample_file_id: str | None = None,
        peak_mz_tolerance_ppm: float | None = None,
    ) -> List[go.Scatter]:
        """
        Get sample-level timeseries traces for a specific peak.

        This method retrieves the timeseries data for a given peak m/z value
        and sample file ID (if provided). It then creates Plotly Scatter traces
        for each sample file, assigning a unique color to each trace.

        :param peak_mz: The m/z value of the peak to retrieve.
        :type peak_mz: float
        :param sample_file_id: The ID of the sample file to retrieve, defaults to None.
        :type sample_file_id: str | None
        :param peak_mz_tolerance_ppm: The tolerance in ppm for the peak m/z, defaults to None.
        :type peak_mz_tolerance_ppm: float | None
        :return: A list of Plotly Scatter traces for the timeseries data.
        :rtype: List[go.Scatter]
        """

        # Fetch the timeseries data using the SampleTimeSeriesExtension
        timeseries_df = self.dataset.get_sample_peak_timeseries(
            peak_mz=peak_mz,
            sample_file_id=sample_file_id,
            peak_mz_tolerance_ppm=peak_mz_tolerance_ppm,
        )
        # Assign colors to each sample_file_id
        sample_file_ids = sorted(self.dataset.match_samples["sample_file_id"].unique())
        color_map = {
            sample_file_id: colorvector[i % len(colorvector)]
            for i, sample_file_id in enumerate(sample_file_ids)
        }
        traces = []
        for sample_id, group in timeseries_df.groupby("sample_file_id"):
            sample_name = group["sample_item_name_datetime"].iloc[0]
            color = color_map[sample_id]
            trace = self.sample_timeseries_trace(
                df_group=group,
                group_name=sample_name,
                color=color,
            )
            traces.append(trace)

        return traces

    def base_timeseries_figure(self) -> go.FigureWidget:
        """
        Build a base FigureWidget and set up the layout.

        :return: A Plotly FigureWidget ready for adding traces.
        :rtype: go.FigureWidget
        """
        fig = go.FigureWidget()
        layout = self.build_layout()
        fig.update_layout(layout)
        return fig

    def sample_timeseries_trace(
        self,
        df_group: pd.DataFrame,
        group_name: str,
        color: str,
    ) -> go.Scatter:
        """
        Build a single trace for the timeseries data.

        :param df_group: DataFrame containing sample-level timeseries data
        for specific sample.
        :type df_group: pd.DataFrame
        :param group_name: Sample name.
        :type group_name: str
        :param color: The color to assign to the trace.
        :type color: str
        :return: A Plotly Scatter trace.
        :rtype: go.Scatter
        """
        hover_items = hover_string(self.hoverbox_columns)
        return go.Scatter(
            x=df_group["time"],
            y=df_group["height"],
            mode="lines+markers",
            name=group_name,
            showlegend=True,
            marker={"color": color, "symbol": "circle"},
            customdata=df_group[self.hoverbox_columns],
            hovertemplate=hover_items,
            visible=True,
        )

    def build_layout(self) -> dict:
        """
        Build the layout of the figure and return it.

        :return: A dictionary defining the layout of the figure.
        :rtype: dict
        """
        layout_dict = {
            "title": "Sample Timeseries",
            "xaxis": {
                "title": "Time",
                "showline": True,
                "linewidth": 1,
                "linecolor": "black",
                "ticks": "outside",
                "tickwidth": 1,
                "tickcolor": "black",
                "ticklen": 5,
            },
            "yaxis": {
                "title": "Signal intensity counts/s",
                "showline": True,
                "linewidth": 1,
                "linecolor": "black",
                "ticks": "outside",
                "tickwidth": 1,
                "tickcolor": "black",
                "ticklen": 5,
            },
            "showlegend": True,
        }
        return layout_dict


# Helper function
def collect_sample_timeseries_traces(
    merged_df: pd.DataFrame,
    trace_name: str,
    mz_val: float,
    context: dict,
    sample_timeseries_plotter: SampleTimeSeriesPlotter,
) -> list:
    """
    Collect sample timeseries traces for a merged DataFrame.

    This helper function iterates through the unique sample_file_ids in the
    merged DataFrame and collects sample timeseries traces for each one.
    It checks if the traces are already cached in the context and reuses them
    if available. If not, it generates new traces using the
    SampleTimeSeriesPlotter instance and caches them in the context.
    The traces are generated with a specified peak_mz and peak_mz_tolerance_ppm.
    The peak_mz is taken from the merged DataFrame, and the tolerance is set to 0.
    The collected traces are returned as a list.

    :param merged_df: Merged DataFrame containing sample timeseries data.
    :type merged_df: pd.DataFrame
    :param trace_name: Name of the trace.
    :type trace_name: str
    :param mz_val: Mz value for the sample timeseries.
    :type mz_val: float
    :param context: Callback context containing the sample timeseries cache.
    :type context: dict
    :param sample_timeseries_plotter: SampleTimeSeriesPlotter instance for generating traces.
    :type sample_timeseries_plotter: SampleTimeSeriesPlotter
    :return: List of sample timeseries traces.
    :rtype: list
    """
    traces = []
    key = (trace_name, mz_val)
    if "figure_stash" not in context:
        context["figure_stash"] = {}
    if key not in context["figure_stash"]:
        context["figure_stash"][key] = {}
    for sample_file_id in merged_df["sample_file_id"].unique():
        if sample_file_id in context["figure_stash"][key]:
            traces.extend(context["figure_stash"][key][sample_file_id])
        else:
            if "sample_peak_mz" in merged_df.columns and pd.notnull(
                merged_df["sample_peak_mz"].iloc[0]
            ):
                peak_mz = merged_df["sample_peak_mz"].iloc[0]
            else:
                peak_mz = merged_df["mz"].iloc[0]
            new_traces = sample_timeseries_plotter.get_sample_timeseries_traces(
                peak_mz=peak_mz, sample_file_id=sample_file_id, peak_mz_tolerance_ppm=0
            )
            if not new_traces:
                logger.debug(
                    f"No sample-level timeseries trace generated for trace '{trace_name}',"
                    f" sample_file_id '{sample_file_id}', peak_mz {peak_mz}."
                )
            else:
                # Set unique legend name only if needed
                for trace_obj in new_traces:
                    trace_obj.name = auto_trace_name(trace_obj.name, mz_val, trace_name)
                traces.extend(new_traces)
            context["figure_stash"][key][sample_file_id] = new_traces
    return traces
