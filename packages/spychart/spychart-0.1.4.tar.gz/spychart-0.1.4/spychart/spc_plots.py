import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
import seaborn as sns


def seaborn_chart(data, figure_title=None, yaxis_label="Measure", figsize=(15, 5)):
    """
    Seaborn SPC plotter.
    """

    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=figsize, dpi=600)

    sns.lineplot(
        data=data,
        x=data.index,
        y="process",
        ax=ax,
        label="Observed process",
        color="#00789c",
        linewidth=2,
    )

    ax.plot(data.index, data["CL"], color="#66a182", label="Center Line", linewidth=2)
    ax.plot(
        data.index, data["UCL"], color="#d1495b", label="Control Limits", linestyle="--"
    )
    ax.plot(data.index, data["LCL"], color="#d1495b", label=None, linestyle="--")

    out_of_control = _filter_out_of_control(data)
    ax.scatter(
        out_of_control.index,
        out_of_control["process"],
        s=100,
        facecolors="none",
        edgecolors="#d1495b",
        linewidth=2,
        label="Out-of-Control",
    )

    if "period" in data.columns:
        process_change_dates = data["period_name"].dropna().index.to_list()
        for date in process_change_dates:
            label = data.loc[date]["period_name"]
            ax.axvline(x=date, color="#27374D", linestyle="--")
            ax.text(
                date,
                ax.get_ylim()[1],
                label,
                rotation=90,
                verticalalignment="bottom",
                fontsize=10,
                color="black",
            )

    ax.set_title(figure_title)
    ax.set_xlabel(None)
    ax.set_ylabel(yaxis_label, fontsize=12)
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),
        ncol=4,
        frameon=False,
        fontsize=12,
    )
    ax.set_xlim(data.index.min(), data.index.max())
    fig.tight_layout()

    return fig, ax


def plotly_chart(data, figure_title=None, yaxis_label="Measure"):
    """
    Plotly SPC plotter.
    """

    fig = go.Figure()

    out_of_control = _filter_out_of_control(data)
    _add_out_of_control_points(fig, out_of_control, "process")
    _add_process_lines(fig, data, "process", line_name="Process")
    _add_control_lines(fig, data)

    fig.update_layout(
        title=figure_title,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
        ),
        hovermode="x unified",
        xaxis=dict(
            title=None,
            showgrid=True,
            gridcolor="#dde6ed",
            range=[data.index.min(), data.index.max()],
        ),
        yaxis=dict(
            title=yaxis_label,
            showgrid=True,
            gridcolor="#dde6ed",
        ),
    )

    return fig


def _filter_out_of_control(data):
    """
    Filter SPC data only for points "out of control".
    """

    df_rules = data.filter(regex="^Rule ", axis=1)
    out_of_control = data[df_rules.sum(axis=1) > 0]
    return out_of_control


def _add_control_lines(fig, data):
    """
    Add control/upper/lower lines to Plotly trace.
    """
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["CL"],
            mode="lines",
            line=dict(color="#66a182", dash="dash"),
            name="Center Line",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["UCL"],
            mode="lines",
            line=dict(color="#d1495b", dash="dot"),
            name="Control Limits",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["LCL"],
            mode="lines",
            line=dict(color="#d1495b", dash="dot"),
            name=None,
            showlegend=False,
        )
    )


def _add_process_lines(fig, data, y_col, line_name):
    """
    Add target measure to Plotly trace (line chart).
    """
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data[y_col],
            mode="lines",
            line=dict(color="#00789c", width=2),
            name=line_name,
        )
    )


def _add_out_of_control_points(fig, signals_data, y_col):
    """
    Add out of control points to Plotly trace.
    """

    rule_columns = [col for col in signals_data.columns if col.startswith("Rule")]

    fig.add_trace(
        go.Scatter(
            x=signals_data.index,
            y=signals_data[y_col],
            mode="markers",
            marker=dict(
                size=12,
                color="rgba(209, 73, 91, 0.25)",
                line=dict(color="rgba(209, 73, 91, 0.6)", width=2),
            ),
            name="Out-of-Control",
            hoverinfo="text",
            hovertext=[
                "Out of Control<br>"
                f"Violations: {', '.join([rule for rule in rule_columns if row[rule] == 1])}"
                for _, row in signals_data.iterrows()
            ],
        )
    )
