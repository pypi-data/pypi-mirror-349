import unittest
import json
from vscodedebugvisualizer import globalVisualizationFactory

# Define a simple Person class for testing
class Person:
    def __init__(self, name, parents=None) -> None:
        self.name = name
        self.parents = [] if parents is None else parents

    def addParent(self, parent: "Person"):
        self.parents.append(parent)

# Define a custom visualizer for Person
class PersonVisualizer:
    def checkType(self, t):
        return isinstance(t, Person)

    def visualizePerson(self, person, nodes=None, edges=None):
        if nodes is None:
            nodes = []
        if edges is None:
            edges = []
            
        if person.name in [n["id"] for n in nodes]:
            return nodes, edges

        nodes.append({
            "id": person.name,
            "label": person.name,
        })

        for p in person.parents:
            nodes, edges = self.visualizePerson(p, nodes, edges)
            edges.append({
                "from": p.name,
                "to": person.name,
            })

        return nodes, edges

    def visualize(self, person):
        jsonDict = {
            "kind": {"graph": True},
            "nodes": [],
            "edges": [],
        }

        self.visualizePerson(person, jsonDict["nodes"], jsonDict["edges"])
        return json.dumps(jsonDict)

class TestCustomVisualizer(unittest.TestCase):
    def setUp(self):
        # Create a new factory to avoid affecting the global one
        self.factory = globalVisualizationFactory.__class__()
        self.factory.addVisualizer(PersonVisualizer())
        
    def test_person_visualizer(self):
        # Create a family tree
        grandparent = Person("Grandparent")
        parent1 = Person("Parent1", [grandparent])
        parent2 = Person("Parent2")
        child = Person("Child", [parent1, parent2])
        
        # Visualize the child (which should include the entire family tree)
        result = self.factory.visualize(child)
        
        # Parse the result and check it
        data = json.loads(result)
        
        # Check structure
        self.assertIn("kind", data)
        self.assertIn("graph", data["kind"])
        self.assertIn("nodes", data)
        self.assertIn("edges", data)
        
        # Check nodes
        node_names = [node["id"] for node in data["nodes"]]
        self.assertIn("Child", node_names)
        self.assertIn("Parent1", node_names)
        self.assertIn("Parent2", node_names)
        self.assertIn("Grandparent", node_names)
        
        # Check edges
        edge_pairs = [(edge["from"], edge["to"]) for edge in data["edges"]]
        self.assertIn(("Parent1", "Child"), edge_pairs)
        self.assertIn(("Parent2", "Child"), edge_pairs)
        self.assertIn(("Grandparent", "Parent1"), edge_pairs)

if __name__ == '__main__':
    unittest.main()
