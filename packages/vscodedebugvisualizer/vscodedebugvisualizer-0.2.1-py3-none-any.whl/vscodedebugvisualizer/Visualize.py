from vscodedebugvisualizer.visualizer.ListVisualizer import ListVisualizer
from vscodedebugvisualizer.visualizer.NumpyVisualizer import NumpyVisualizer
from vscodedebugvisualizer.visualizer.PandasVisualizer import PandasVisualizer
from vscodedebugvisualizer.visualizer.PrimitiveVisualizer import PrimitiveVisualizer
from vscodedebugvisualizer.visualizer.PyTorchVisualizer import PyTorchVisualizer
from vscodedebugvisualizer.visualizer.TensorflowVisualizer import TensorflowVisualizer
from vscodedebugvisualizer.visualizer.DirectVisualizer import DirectVisualizer
from vscodedebugvisualizer.visualizer.ShapelyVisualizer import ShapelyVisualizer
from vscodedebugvisualizer.visualizer.GeoPandasVisualizer import GeoPandasVisualizer


class Visualize:
    visualizers = []

    def addVisualizer(self, vis):
        self.visualizers.append(vis)

    def visualize(self, data):
        for v in reversed(self.visualizers):
            if v.checkType(data):
                return v.visualize(data)
        print("No Visualizer found for specified Type: %s" % type(data))
        return None


class Visualizer:
    def checkType(self, type):
        raise Exception("checkType() needs to be overwritten")

    def visualize(self, data):
        raise Exception("visualize() needs to be overwritten")


globalVisualizationFactory = Visualize()
globalVisualizationFactory.addVisualizer(DirectVisualizer())
globalVisualizationFactory.addVisualizer(PrimitiveVisualizer())
globalVisualizationFactory.addVisualizer(ListVisualizer())
globalVisualizationFactory.addVisualizer(NumpyVisualizer())
globalVisualizationFactory.addVisualizer(PyTorchVisualizer())
globalVisualizationFactory.addVisualizer(TensorflowVisualizer())
globalVisualizationFactory.addVisualizer(ShapelyVisualizer())
globalVisualizationFactory.addVisualizer(GeoPandasVisualizer())  # check instance gdf before regular df
globalVisualizationFactory.addVisualizer(PandasVisualizer())


def visualize(d):
    return globalVisualizationFactory.visualize(d)
