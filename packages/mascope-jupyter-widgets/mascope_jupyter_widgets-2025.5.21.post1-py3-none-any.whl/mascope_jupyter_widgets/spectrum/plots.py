from typing import List
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from colorcet import glasbey as colorvector

from ..plot_tools import hover_string, auto_trace_name
from ..mascope_data.wrapper import MascopeDataWrapper
from ..logging_config import logger


class SpectrumPlotter:
    """
    Class containing functions to build spectrum related traces
    by utlizing dataset with SpectrumDataExtension -extension."""

    def __init__(self, dataset: MascopeDataWrapper):
        """
        Initialize SpectrumPlotter with given dataset.
        This class is designed to build spectrum traces
        and setup layout for Plotly figures.
        It requires a dataset with SpectrumDataExtension -extension.

        :param dataset: MascopeDataWrapper -dataset with
        SpectrumDataExtension- extension.
        :type dataset: MascopeDataWrapper
        """
        self.dataset = dataset
        self.hoverbox_columns = [
            "sample_item_id",
            "intensity",
            "unit",
            "datetime",
            "sample_item_name",
            "sample_item_type",
            "instrument",
        ]  # List of HoverBox columns

    def get_spectrum_traces(
        self,
        sample_file_id: str,
        mz_min: float = None,
        mz_max: float = None,
        t_min: float = None,
        t_max: float = None,
    ) -> List[go.Scatter]:
        """
        Get spectrum traces for a specific sample file id.

        :param sample_file_id: sample file id
        :type sample_file_id: str
        :param mz_min: mz range low end, defaults to None
        :type mz_min: float, optional
        :param mz_max: mz range high end, defaults to None
        :type mz_max: float, optional
        :param t_min: time starting point, defaults to None
        :type t_min: float, optional
        :param t_max: time ending point, defaults to None
        :type t_max: float, optional
        :raises ValueError: if sample file id can't be found
        from match_samples
        :return: spectrum trace
        :rtype: go.Scatter
        """

        traces = []
        sample_file_ids = self.dataset.match_samples.sample_file_id.unique()

        match sample_file_id:
            case _ if sample_file_id in sample_file_ids:
                spectrum_df = self.dataset.get_spectrum_data(
                    sample_file_id=sample_file_id,
                    mz_min=mz_min,
                    mz_max=mz_max,
                    t_min=t_min,
                    t_max=t_max,
                )
                # Get sample name and order number for colorcoding
                sample_name, sample_order = self._get_sample_name_and_order_number(
                    sample_file_id=sample_file_id
                )
                spectrum_trace = self.spectrum_trace(
                    df_group=spectrum_df,
                    group_name=sample_name,
                    color=colorvector[sample_order],
                )
                traces.append(spectrum_trace)
            case _:  # Handle unknown sample values
                raise ValueError(f"Sample {sample_name} not found in match_samples.")

        return traces

    def base_spectrum_figure(
        self,
    ) -> go.FigureWidget:
        """
        Build base FigureWidget and setup layout.

        :return: figurewidget which is ready for adding traces
        :rtype: go.FigureWidget
        """

        fig = go.FigureWidget()
        layout = self.build_layout()
        fig.update_layout(layout)
        return fig

    def spectrum_trace(
        self,
        df_group: pd.DataFrame,
        group_name: str,
        color: str = None,
    ) -> go.Scatter:
        """
        Builds spectrum traces

        :param df_group: dataframe containing at least columns:
        -'mz'
        -'intensity'
        - and columns in self.hoverbox_columns
        :type df_group: pd.DataFrame
        :param group_name: trace-group name
        :type group_name: str
        :param color: color for trace-group, defaults to None
        :type color: str, optional
        :return: scatter spectrum traces
        :rtype: go.Scatter
        """

        hover_items = hover_string(self.hoverbox_columns)
        df_group = df_group.sort_values(by="mz", ascending=True)
        if df_group["intensity"].sum() != 0:
            spectrum = go.Scatter(
                x=df_group["mz"],
                y=df_group["intensity"],
                mode="lines",
                name=str(group_name),
                marker={"symbol": np.repeat("circle", len(df_group))},
                customdata=df_group[self.hoverbox_columns],
                hovertemplate=hover_items,
                line={"color": color} if color else {},
                visible=True,
            )
            return spectrum

    def build_layout(
        self,
    ) -> dict:
        """
        Build the layout of the figure and return layout.

        :param fig: plotly-figure containing traces
        :type fig: go.FigureWidget
        :return: layout dictionary to be applied to the figure
        :rtype: dict
        """
        # Check if intensity_unit is available
        intensity_unit = getattr(self.dataset, "intensity_unit", None)
        yaxis_title = (
            f"Signal intensity ({intensity_unit})"
            if intensity_unit
            else "Signal intensity"
        )
        layout_dict = {
            "showlegend": True,
            "xaxis": {
                "showspikes": True,
                "spikecolor": "black",
                "showline": True,
                "linewidth": 1,
                "linecolor": "black",
                "ticks": "outside",
                "tickwidth": 1,
                "tickcolor": "black",
                "ticklen": 5,
                "rangeslider_visible": True,
            },
            "yaxis": {
                "showspikes": True,
                "spikecolor": "black",
                "showline": True,
                "linewidth": 1,
                "linecolor": "black",
                "ticks": "outside",
                "tickwidth": 1,
                "tickcolor": "black",
                "ticklen": 5,
                "title_text": yaxis_title,
            },
            "updatemenus": [
                {
                    "buttons": [
                        {
                            "label": "Linear Scale",
                            "method": "relayout",
                            "args": ["yaxis.type", "linear"],
                        },
                        {
                            "label": "Log Scale",
                            "method": "relayout",
                            "args": ["yaxis.type", "log"],
                        },
                    ],
                    "direction": "down",
                    "showactive": True,
                    "x": 0.05,
                    "y": 1.5,
                }
            ],
        }

        return layout_dict

    def _get_sample_name_and_order_number(self, sample_file_id: str) -> list[str, int]:
        """
        Get sample name and alphapetical order number by using
        'sample_file_id' and 'match_samples' -dataframe.

        :param sample_file_id: mascope database 'sample_file_id' value
        for sample under intrest
        :type sample_file_id: str
        :return: sample_item_name_datetime and alphapetical order number of
        'sample_file_id' (can be used for colorcoding trace-groups)
        :rtype: list[str, int]
        """

        sample_name = self.dataset.match_samples["sample_item_name_datetime"][
            self.dataset.match_samples.sample_file_id == sample_file_id
        ].unique()[0]
        sample_order = {
            v: i + 1
            for i, v in enumerate(
                sorted(self.dataset.match_samples.sample_file_id.unique())
            )  # Create dictionary with order number for each sample file id
        }.get(
            sample_file_id
        )  # Get the integer order number for the given target compound i

        return sample_name, sample_order


# Helper function
def collect_spectrum_traces(
    merged_df: pd.DataFrame,
    trace_name: str,
    mz_val: float,
    context: dict,
    spectrum_plotter: SpectrumPlotter,
) -> list:
    """
    Collect spectrum traces for each sample_file_id in the merged DataFrame.

    This helper function iterates through the unique sample_file_ids in the
    merged DataFrame and collects spectrum traces for each one.
    It checks if the traces are already cached in the context and reuses them
    if available. If not, it generates new traces using the
    SpectrumPlotter instance and caches them in the context.
    The traces are generated with a specified mz_min and mz_max range
    based on the minimum and maximum mz values in the merged DataFrame.
    The mz_min and mz_max are adjusted by ±0.05 to ensure a proper range.
    The collected traces are returned as a list.
    The function also initializes the figure stash in the context if it
    doesn't exist.

    :param merged_df: Merged DataFrame containing spectrum data.
    :type merged_df: pd.DataFrame
    :param trace_name: Name of the trace.
    :type trace_name: str
    :param mz_val: Mz value for the spectrum.
    :type mz_val: float
    :param context: Callback context containing the spectrum cache.
    :type context: dict
    :param spectrum_plotter: SpectrumPlotter instance for generating traces.
    :type spectrum_plotter: SpectrumPlotter
    :return: List of spectrum traces.
    :rtype: list
    """
    spectrum_traces = []
    key = (trace_name, mz_val)
    if key not in context["figure_stash"]:
        context["figure_stash"][key] = {}
    for sample_file_id in merged_df["sample_file_id"].unique():
        if sample_file_id in context["figure_stash"][key]:
            spectrum_traces.extend(context["figure_stash"][key][sample_file_id])
        else:
            round_df = merged_df[merged_df["sample_file_id"] == sample_file_id]
            mz_min, mz_max = (round_df.mz.min() - 0.05), (round_df.mz.max() + 0.05)
            new_traces = spectrum_plotter.get_spectrum_traces(
                sample_file_id,
                mz_min=mz_min,
                mz_max=mz_max,
            )
            if not new_traces:
                logger.debug(
                    f"No spectrum trace generated for trace '{trace_name}', "
                    f"sample_file_id '{sample_file_id}', mz range [{mz_min}, {mz_max}]."
                )
            else:
                for trace_obj in new_traces:
                    trace_obj.name = auto_trace_name(trace_obj.name, mz_val, trace_name)
                spectrum_traces.extend(new_traces)
            context["figure_stash"][key][sample_file_id] = new_traces
    return spectrum_traces
