"""
Module to make some auxillary Plotly plots to compliment Fracman
Objective is to save static .html files for interactive visualizations
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def make_3d_plot(is_df, stage_locs, surveys, surfaces, plot_bounds):
    """
    Massive plot function to make a 3D plot
    Yes, I recognize this isn't documented and a very poor function =)
    """

    fig = go.Figure()

    st_grouper = is_df.sort_values("datetime").groupby("well_stage")
    tt = [g.well_stage.values[0] for n, g in st_grouper]
    xx = [g.x.values for n, g in st_grouper]
    yy = [g.y.values for n, g in st_grouper]
    zz = [g.z.values for n, g in st_grouper]
    ss = [(g.mag.values + 1) * 10 for n, g in st_grouper]

    # Frames generation
    frames = []
    for i in range(len(xx)):
        scatter = go.Scatter3d(
            x=xx[i],
            y=yy[i],
            z=zz[i],
            name=tt[i],
            mode="markers",
            marker=dict(size=ss[i], color="blue"),
        )
        stage = stage_locs[stage_locs.well_stage == tt[i].replace("F", "")].iloc[0, :]
        stage_pt = go.Scatter3d(
            x=stage[["x_top_m", "x_bottom_m"]].to_list(),
            y=stage[["y_top_m", "y_bottom_m"]].to_list(),
            z=stage[["z_top_m", "z_bottom_m"]].to_list(),
            name=tt[i] + " Stage",
            mode="lines",
            line=dict(width=40, color="black"),
        )

        frame = go.Frame(data=[scatter, stage_pt], name=tt[i])
        frames.append(frame)

    # Assign frames to fig
    fig.frames = frames

    updatemenus = [
        dict(
            buttons=[
                dict(
                    args=[
                        None,
                        {
                            "frame": {"duration": 200, "redraw": True},
                            "fromcurrent": True,
                            "transition": {"duration": 200},
                        },
                    ],
                    label="Play",
                    method="animate",
                ),
                dict(
                    args=[
                        [None],
                        {
                            "frame": {"duration": 0, "redraw": True},
                            "fromcurrent": True,
                            "mode": "immediate",
                            "transition": {"duration": 0},
                        },
                    ],
                    label="Pause",
                    method="animate",
                ),
            ],
            direction="left",
            pad={"r": 10, "t": 80},
            showactive=False,
            type="buttons",
            x=0.1,
            xanchor="right",
            y=0.2,
            yanchor="top",
        )
    ]

    sliders = [
        dict(
            steps=[
                dict(
                    method="animate",
                    args=[
                        [tt[k]],
                        dict(
                            mode="immediate",
                            frame=dict(duration=200, redraw=True),
                            transition=dict(duration=0),
                        ),
                    ],
                    label=tt[k],
                )
                for k in range(len(xx))
            ],
            active=0,
            transition=dict(duration=0),
            x=0,
            y=0,
            currentvalue=dict(
                font=dict(size=12), prefix="frame: ", visible=True, xanchor="center"
            ),
            len=1.0,
        )
    ]

    fig.update_layout(
        width=1000,
        height=1000,
        updatemenus=updatemenus,
        sliders=sliders,
        autosize=False,
        scene=dict(
            xaxis=dict(
                nticks=4, range=[plot_bounds.get("min_x"), plot_bounds.get("max_x")]
            ),
            yaxis=dict(
                nticks=4, range=[plot_bounds.get("min_y"), plot_bounds.get("max_y")]
            ),
            zaxis=dict(
                nticks=4, range=[plot_bounds.get("max_z"), plot_bounds.get("min_z")]
            ),
        ),
        scene_camera=dict(eye=dict(x=0, y=-1, z=0.25)),
    )

    # add well paths
    for well in ["A2", "A4", "A2", "A4", "A6"]:
        well_survey = surveys.query("well==@well").query("z < @min_z")
        fig.add_trace(
            go.Scatter3d(
                x=well_survey.x.values,
                y=well_survey.y.values,
                z=well_survey.z.values,
                mode="lines",
                name=well,
            )
        )

    # add surfaces for geological reference
    for surf_name in surfaces.keys():
        fig.add_trace(
            go.Mesh3d(
                x=surfaces[surf_name]["df"].x.values,
                y=surfaces[surf_name]["df"].y.values,
                z=surfaces[surf_name]["df"].z.values,
                color=surfaces[surf_name]["col"],
                name=surf_name,
                opacity=0.1,
            )
        )

    return fig
