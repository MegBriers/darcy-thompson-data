import plotly.graph_objects as go


def plot(coords):
    fig = go.Figure(go.Scattermapbox(
        lat=[pair[0] for pair in coords],
        lon=[pair[1] for pair in coords],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9
        ),
        text=[pair[2] for pair in coords],
    ))

    fig.update_layout(
        hovermode='closest',
        mapbox=dict(
            accesstoken="secret",
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=57,
                lon=3
            ),
            pitch=0,
            zoom=4
        )
    )

    fig.write_html('plotted_coords.html',
                   auto_open=True)
