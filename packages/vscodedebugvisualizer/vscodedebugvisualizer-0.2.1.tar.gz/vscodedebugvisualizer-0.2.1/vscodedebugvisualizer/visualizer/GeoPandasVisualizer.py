from vscodedebugvisualizer.visualizer.ShapelyVisualizer import ShapelyVisualizer
from plotly.subplots import make_subplots
import plotly.graph_objects as go


class GeoPandasVisualizer(ShapelyVisualizer):
    def checkType(self, t):
        try:
            import geopandas
        except ImportError:
            return False

        return isinstance(t, (geopandas.GeoDataFrame, geopandas.GeoSeries))

    def visualize(self, data):
        from geopandas import GeoDataFrame, GeoSeries
        if isinstance(data, GeoDataFrame):
            return self.visualizeGdf(data)
        
        if isinstance(data, GeoSeries):
            return super().visualizeList(data)


    def visualizeGdf(self, gdf):
        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=False,
            vertical_spacing=0.1,
            specs=[
                [{"type": "scatter"}],
                [{"type": "table"}],
            ],
        )
        fig.update_yaxes(
            scaleanchor="x",
            scaleratio=1,
        )
        
        traces = []
        # take the first column as the name for the geometry in scatter plot
        [traces.extend(self._geomToTraces(gdf.values[i][-1], str(gdf.values[i][0]))) for i, geom in enumerate(gdf.values)]
        fig.add_traces(
            traces,
            rows=1,
            cols=1
        )

        cellList = []
        for i in range(len(gdf.values)):
            cell = []
            for ii in range(len(gdf.values[i])):
                value = gdf.values[ii][i]
                if hasattr(value, "geom_type"):
                    value = value.geom_type
                cell.append(str(value))
            cellList.append(cell)
        
        fig.add_trace(
            go.Table(
                header=dict(
                    values=[[colName] for colName in gdf.columns],
                ),
                cells=dict(
                    values=cellList,
                ),
            ),
            row=2,
            col=1,
        )
        
        return self.visualizeFigure(fig)
