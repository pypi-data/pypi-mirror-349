import pandas as pd
import plotly.graph_objects as go
from .helpers import (
    build_combined_annotation_text,
    get_trace_and_initialize_storage,
    group_clicked_data_by_trace_and_mz,
    extract_reference_data,
    restore_original_markers,
    update_marker_symbols_and_colors,
)
from ..spectrum.plots import SpectrumPlotter, collect_spectrum_traces
from ..sample_timeseries.plots import (
    SampleTimeSeriesPlotter,
    collect_sample_timeseries_traces,
)
from ..logging_config import logger  # Import the shared logger


# Callback function
def display_reference_table(
    clicked_point: dict, callback_context: dict, update_markers: bool = True
) -> pd.DataFrame:
    """
    Returns the reference table for the clicked point.

    This function processes the clicked point data and updates the
    reference table accordingly. It also updates the markers on the clicked
    point in the plot if specified. The reference table contains information
    about the clicked point, including its trace name and other relevant
    data.

    :param clicked_point: Dictionary containing clicked point data.
    :rtype clicked_point: dict
    :param callback_context: Dictionary containing the callback context.
    :rtype callback_context: dict
    :param update_markers: Flag to indicate whether to update markers or not.
    :type update_markers: bool
    :return: DataFrame containing the reference table for the clicked point.
    :rtype: pd.DataFrame
    """
    # Extract trace name and context from the clicked point
    context = callback_context
    trace_name = clicked_point["trace_name"]
    try:
        trace = get_trace_and_initialize_storage(trace_name, context)
    except ValueError:
        print(f"Trace '{trace_name}' not found.")
        return
    selected_data = extract_reference_data(clicked_point, context)
    if selected_data.empty:
        print(f"No matching data for trace '{trace_name}'.")
        logger.debug(
            f"No matching data for trace '{trace_name}' at "
            f"x={clicked_point.get('x_value')}, y={clicked_point.get('y_value')}."
        )
        if update_markers:
            restore_original_markers(
                trace_name,
                trace,
                context["fig"],
                context["original_symbols"],
                context["original_colors"],
            )
        return
    # Store clicked data points and marker indices
    context["clicked_dots_data"][trace_name].append(selected_data)
    context["marker_points_idx"][trace_name].append(clicked_point["point_index"])
    if update_markers:
        update_marker_symbols_and_colors(
            trace_name,
            trace,
            context["marker_points_idx"],
            context["original_symbols"],
            context["original_colors"],
            context["fig"],
        )
    # Display part of the reference table
    clicked_points_compound_trace_df = pd.concat(
        context["clicked_dots_data"][trace_name], ignore_index=True
    ).drop_duplicates()

    return clicked_points_compound_trace_df


# Callback function
def display_spectrum(
    clicked_point: dict, callback_context: dict, update_markers: bool = True
) -> go.FigureWidget:
    """
    Process and return spectrum traces from clicked dot.

    This function processes the clicked point data and builds the
    corresponding spectrum traces.
    It also updates the markers on the clicked point in the plot
    if specified.

    :param clicked_point: Dictionary containing clicked point data.
    :type clicked_point: dict
    :param callback_context: Dictionary containing the callback context.
    :type callback_context: dict
    :param update_markers: Flag to indicate whether to update markers or not.
    :type update_markers: bool
    :return: FigureWidget containing the spectrum traces.
    :rtype: go.FigureWidget
    """
    # Extract trace name and context from the clicked point
    context = callback_context
    trace_name = clicked_point["trace_name"]  # Extract trace name
    if not hasattr(context["dataset"], "get_spectrum_data"):
        raise AttributeError(
            "The dataset object does not have the required method 'get_spectrum_data'. "
            "Please ensure the dataset is extended with SpectrumDataExtension."
        )

    try:
        trace = get_trace_and_initialize_storage(trace_name, context)
    except ValueError:
        print(f"Trace '{trace_name}' not found.")
        logger.debug(f"Trace '{trace_name}' not found in the dataset.")
        return
    selected_data = extract_reference_data(clicked_point, context)
    if selected_data.empty:
        print(f"No matching data for trace '{trace_name}'.")
        logger.debug(
            f"No matching data for trace '{trace_name}' at "
            f"x={clicked_point.get('x_value')}, y={clicked_point.get('y_value')}."
        )
        if update_markers:
            restore_original_markers(
                trace_name,
                trace,
                context["fig"],
                context["original_symbols"],
                context["original_colors"],
            )
        return

    # Collect reference data for the clicked point
    point_idx = clicked_point["point_index"]
    if trace_name not in context["clicked_dots_data"] or not isinstance(
        context["clicked_dots_data"][trace_name], dict
    ):
        context["clicked_dots_data"][trace_name] = {}
    if trace_name not in context["marker_points_idx"]:
        context["marker_points_idx"][trace_name] = []
    if point_idx not in context["clicked_dots_data"][trace_name]:
        context["clicked_dots_data"][trace_name][point_idx] = selected_data
        context["marker_points_idx"][trace_name].append(point_idx)

    if update_markers:
        update_marker_symbols_and_colors(
            trace_name,
            trace,
            context["marker_points_idx"],
            context["original_symbols"],
            context["original_colors"],
            context["fig"],
        )

    spectrum_plotter = SpectrumPlotter(dataset=context["dataset"])
    spectrum_fig = spectrum_plotter.base_spectrum_figure()
    required_columns = ["target_compound_id", "sample_item_id", "mz"]

    plot_data = group_clicked_data_by_trace_and_mz(
        context["clicked_dots_data"], context, required_columns, trace_name
    )

    for (trace_name, mz_val), merged_dfs in plot_data.items():
        for merged_df in merged_dfs:
            spectrum_traces = collect_spectrum_traces(
                merged_df, trace_name, mz_val, context, spectrum_plotter
            )
            spectrum_fig.add_traces(spectrum_traces)

    combined_text = build_combined_annotation_text(plot_data)
    spectrum_fig.update_layout(title=trace_name)

    return spectrum_fig, combined_text


# Callback function
def display_sample_timeseries(
    clicked_point: dict, callback_context: dict, update_markers: bool = True
) -> pd.DataFrame:
    """
    Process and returns sample timeseries traces from clicked dot.

    This function processes the clicked point data and builds the
    corresponding sample timeseries traces.
    It also updates the markers on the clicked point in the plot
    if specified.

    :param clicked_point: Dictionary containing clicked point data.
    :type clicked_point: dict
    :param callback_context: Dictionary containing the callback context.
    :type callback_context: dict
    :param update_markers: Flag to indicate whether to update markers or not.
    :type update_markers: bool
    :return: FigureWidget containing the sample timeseries traces.
    :rtype: go.FigureWidget
    """

    # Extract trace name and context from the clicked point
    context = callback_context
    trace_name = clicked_point["trace_name"]
    print(trace_name)
    if not hasattr(context["dataset"], "get_sample_peak_timeseries"):
        raise AttributeError(
            "The dataset object does not have the required method 'get_sample_peak_timeseries'. "
            "Please ensure the dataset is extended with SampleTimeSeriesExtension."
        )

    try:
        trace = get_trace_and_initialize_storage(trace_name, context)
    except ValueError:
        print(f"Trace '{trace_name}' not found.")
        logger.debug(f"Trace '{trace_name}' not found in the dataset.")
        return

    selected_data = extract_reference_data(clicked_point, context)
    if selected_data.empty:
        print(f"No matching data for trace '{trace_name}'.")
        logger.debug(
            f"No matching data for trace '{trace_name}' at "
            f"x={clicked_point.get('x_value')}, y={clicked_point.get('y_value')}."
        )
        if update_markers:
            restore_original_markers(
                trace_name,
                trace,
                context["fig"],
                context["original_symbols"],
                context["original_colors"],
            )
        return

    # Collect reference data for the clicked point
    point_idx = clicked_point["point_index"]
    if trace_name not in context["clicked_dots_data"] or not isinstance(
        context["clicked_dots_data"][trace_name], dict
    ):
        context["clicked_dots_data"][trace_name] = {}
    if trace_name not in context["marker_points_idx"]:
        context["marker_points_idx"][trace_name] = []
    if point_idx not in context["clicked_dots_data"][trace_name]:
        context["clicked_dots_data"][trace_name][point_idx] = selected_data
        context["marker_points_idx"][trace_name].append(point_idx)

    if update_markers:
        update_marker_symbols_and_colors(
            trace_name,
            trace,
            context["marker_points_idx"],
            context["original_symbols"],
            context["original_colors"],
            context["fig"],
        )

    sample_timeseries_plotter = SampleTimeSeriesPlotter(dataset=context["dataset"])
    timeseries_fig = sample_timeseries_plotter.base_timeseries_figure()
    required_columns = ["sample_peak_mz", "mz", "sample_file_id"]

    plot_data = group_clicked_data_by_trace_and_mz(
        context["clicked_dots_data"], context, required_columns, trace_name
    )

    for (trace_name, mz_val), merged_dfs in plot_data.items():
        for merged_df in merged_dfs:
            timeseries_traces = collect_sample_timeseries_traces(
                merged_df, trace_name, mz_val, context, sample_timeseries_plotter
            )
            timeseries_fig.add_traces(timeseries_traces)

    combined_text = build_combined_annotation_text(plot_data)
    timeseries_fig.update_layout(title="Sample Timeseries")

    return timeseries_fig, combined_text
