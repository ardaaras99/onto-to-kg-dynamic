from base_ontology.node import BaseNode
from base_ontology.relation import BaseRelation
from pyvis.network import Network


class KnowledgeGraphVisualizer:
    """Class for visualizing knowledge graphs using pyvis Network."""

    def __init__(self, height: str = "750px", width: str = "1500px") -> None:
        """Initialize the visualizer.

        Args:
            height: Height of the visualization
            width: Width of the visualization
        """
        self.height = height
        self.width = width
        self.color_map = {
            "SözleşmeNode": "#FF9999",  # Light red
            "TarafNode": "#99FF99",  # Light green
            "TaşınmazNode": "#9999FF",  # Light blue
            "KiraSüresiNode": "#FF99FF",  # Light purple
            "FesihMaddesiNode": "#FFFF99",  # Light yellow
            "FinansalUnsurNode": "#99FFFF",  # Light cyan
            "TeminatMaddesiNode": "#FFCC99",  # Light orange
        }

    def create_visualization(self, nodes: list[BaseNode], relations: list[BaseRelation], output_path: str = "kg_visualization.html") -> None:
        net = Network(notebook=False, height=self.height, width=self.width, directed=True)

        # Add nodes with labels and colors
        for node in nodes:
            label = node.__class__.__name__
            if node.__class__.__name__ == "TarafNode":
                label = f"{node.__class__.__name__}"
            node_color = self.color_map.get(node.__class__.__name__, "#97C2FC")
            title = "\n".join([f"{k}: {v}" for k, v in node.__dict__.items()])
            net.add_node(node.id, label=label, title=title, color=node_color)

        # Add edges based on relations
        for relation in relations:
            source_node = relation.source_node
            target_node = relation.target_node
            relation_type = relation.label

            if hasattr(source_node, "id") and hasattr(target_node, "id"):
                net.add_edge(source_node.id, target_node.id, label=relation_type, title=relation.reason)

        # Enable physics and configure options
        net.show_buttons(filter_=["physics"])

        # Save the network to an HTML file
        net.save_graph(output_path)
