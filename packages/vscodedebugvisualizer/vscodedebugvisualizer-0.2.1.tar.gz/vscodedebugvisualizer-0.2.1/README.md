This package adds python support to the [Debug Visualizer](https://marketplace.visualstudio.com/items?itemName=hediet.debug-visualizer).

## Installation Instructions

The  [Debug Visualizer](https://marketplace.visualstudio.com/items?itemName=hediet.debug-visualizer) is required. To install the extension for python, your're required to install the package within your debug enviroment:

`pip install vscodedebugvisualizer`

## supported Types

### Numpy Array / PyTorch Tensors / Tensorflow Tensors

All Tensors are converted to numpy arrays and treated alike.

If there multiple dimensions only the last 2 dimensons are visualized, the longer dimension ist treated as x axis. The X axe is downsampled to 1000 points and the y axe only shows the first 10 rows.

![](docs/np-array.png)

### Dataframes

Dataframes are transformed to data tables.

![](docs/dataframes.png)

## Add your own representation/data extractor

Asuming you have a specific Type in your project you want to visualize. You can create a file `debugvisualizer.py` in your project root directory, that will be injected into the debug process.

Asuming we want to visualize the class `Person`:

```python
class Person:
    def __init__(self, name, parents=None) -> None:
        self.name = name
        self.parents = [] if parents is None else parents

    def addParent(self, parent: "Person"):
        self.parents.append(parent)

```

In `debugvisualizer.py` you can access all available visualizer with the `from vscodedebugvisualizer import globalVisualizationFactory`. To support your Type you need to create an class that has `checkType(anytype) -> Boolean` and `visualize(self, data) -> None` defined.
`checkType` should return `True` if the given object is supported by the Visualizer.
`visualize` returns a json string that is supported by the visualizer client (see playground).

Finally you need to add the visualizer to the `globalVisualizationFactory` with `globalVisualizationFactory.addVisualizer(YourVisualizer())`.

For the Person-Example:

```python
from Person import Person
from pandas.io import json
from vscodedebugvisualizer import globalVisualizationFactory


class PersonVisualizer:
    def checkType(self, t):
        """ checks if the given object `t` is an instance of Person """
        return isinstance(t, Person)

    def visualizePerson(self, person: Person, nodes=[], edges=[]):
        if person.name in [n["id"] for n in nodes]:
            return nodes, edges

        nodes.append(
            {
                "id": person.name,
                "label": person.name,
            }
        )

        for p in person.parents:
            nodes, edges = self.visualizePerson(p, nodes, edges)
            edges.append(
                {
                    "from": p.name,
                    "to": person.name,
                }
            )

        return nodes, edges

    def visualize(self, person: Person):
        jsonDict = {
            "kind": {"graph": True},
            "nodes": [],
            "edges": [],
        }

        self.visualizePerson(person, jsonDict["nodes"], jsonDict["edges"])

        return json.dumps(jsonDict)


globalVisualizationFactory.addVisualizer(PersonVisualizer())
```

![](docs/PersonDebug.png)


For more visualization examples check out the [visualizer playground](https://hediet.github.io/visualization/?darkTheme=1)