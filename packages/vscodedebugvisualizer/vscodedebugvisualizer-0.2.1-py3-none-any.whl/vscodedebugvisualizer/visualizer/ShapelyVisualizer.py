from vscodedebugvisualizer.visualizer.PlotlyVisualizer import PlotlyVisualizer

import random

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.graph_objs._figure import Figure


class ShapelyVisualizer(PlotlyVisualizer):
    def checkType(self, t):
        try:
            import shapely
        except ImportError:
            return False

        return isinstance(t, shapely.geometry.base.BaseGeometry)

    def visualize(self, data):
        traces = self._geomToTraces(data, data.geom_type)
        fig = self._getFigureForTraces(traces)
        return self.visualizeFigure(fig)

    def visualizeList(self, data):
        traces = []
        hue_offset = random.randrange(0, 256, 1)
        for i, geom in enumerate(data):
            hue = (round(255 * i / len(data)) + hue_offset) % 255
            traces.extend(self._geomToTraces(geom, str(i), hue=hue))
        fig = self._getFigureForTraces(traces)
        return self.visualizeFigure(fig)

    def visualizeFigure(self, fig):
        return super().visualize(fig)

    def _getFigureForTraces(self, traces) -> Figure:
        fig = make_subplots()
        fig.update_yaxes(
            scaleanchor="x",
            scaleratio=1,
        )
        fig.add_traces(traces)
        return fig

    def _geomToTraces(self, geom, geomName = None, hue: int | None = None):
        """
        Convert a Shapely geometry into a list of Plotly traces.
        """
        if hue is None:
            hue = random.randrange(0, 256, 1)

        color = f"hsla({hue}, 100%, 50%, 0.5)"
        fillColor = f"hsla({hue}, 100%, 50%, 0.1)"
        namePrefix = ""
        if geomName is not None:
            namePrefix = f"{geomName}: "
        traces = []
        geomType = geom.geom_type.lower()

        if geom.is_empty:
            return traces

        if geomType == "point":
            x, y = geom.x, geom.y
            traces.append(
                go.Scatter(
                    x = [x],
                    y = [y],
                    mode = "markers",
                    marker = {"color": color},
                    name = namePrefix + "Point"
                )
            )

        elif geomType == "linestring" or geomType == "linearring":
            if geomType == "linestring":
                x, y = self._coordsToXY(geom.coords, False)
            else:
                x, y = self._coordsToXY(geom.coords)
            traces.append(
                go.Scatter(
                    x = x,
                    y = y,
                    mode = "lines",
                    line = {"color": color},
                    name = namePrefix + geom.__class__.__name__
                )
            )

        elif geomType == "polygon":
            # Exterior ring
            exteriorX, exteriorY = self._coordsToXY(geom.exterior.coords)
            traces.append(
                go.Scatter(
                    x = exteriorX,
                    y = exteriorY,
                    mode = "lines",
                    fill = "toself",    # fill the polygon
                    fillcolor = fillColor,
                    line = {"color": color},
                    name = namePrefix + "Polygon Exterior"
                )
            )

            # Interiors
            for i, interior in enumerate(geom.interiors):
                interiorX, interiorY = self._coordsToXY(interior.coords)
                traces.append(
                    go.Scatter(
                        x = interiorX,
                        y = interiorY,
                        mode = "lines",
                        fill = "tonext",  # subtract from previous fill
                        fillcolor = fillColor,
                        line = {"color": color, "dash": "dot"},
                        name = f"    |-  Hole {i}"
                    )
                )

        elif geomType.startswith("multi") or geomType == "geometrycollection":
            # MultiPoint, MultiLineString, MultiPolygon, or GeometryCollection
            for i, part in enumerate(geom.geoms):
                if geomName is None:
                    geomName = geom.__class__.__name__
                traces.extend(self._geomToTraces(part, geomName = f"{geomName}.{i}"))

        return traces

    def _coordsToXY(self, coords, close = True):
        if len(coords) > 1 and coords[0] != coords[-1]:
            if close:
                coords = list(coords) + [coords[0]]

        xs, ys = zip(*coords)
        return list(xs), list(ys)
