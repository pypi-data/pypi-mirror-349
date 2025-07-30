from itertools import chain
from pathlib import Path

import finesse
import pygraphviz
from finesse.components.general import Connector
from finesse.components.node import Node, NodeType, Port

# model = finesse.Model()

# kat = """
# l l1
# s s1 l1.p1 m1.p1
# m m1 R=0.5 T=0.5
# s s2 m1.p2 mirror2.p1
# m mirror2 R=0.5 T=0.5

# pd circ mirror2.p1.o
# pd trans mirror2.p2.o
# pd refl m1.p1.o

# ad ad_circ mirror2.p1.o f=0
# ad ad_trans mirror2.p2.o f=0
# ad ad_refl m1.p1.o f=0
# """
# # kat = (LAYOUTS / "virgo_test" / "layout.kat").read_text()
# model.parse(kat)


# TODO somehow the order of the cluster gets messed up, meaning it won't be neatly left
# to right. The subclusters in the dotfile need to appear in the correct order
def write_node_overview(model: finesse.Model, root_comp: Connector, path: Path):
    nodes_to_keep = []
    edges_to_keep = []
    # TODO maybe just pass this in as well
    kat = model.unparse()

    for node in model.optical_network.nodes:
        if node.startswith(f"{root_comp.name}."):
            nodes_to_keep.append(node)
            for edge in chain(
                model.optical_network.in_edges(node),
                model.optical_network.out_edges(node),
            ):
                edges_to_keep.append(edge)
                for node in edge:
                    nodes_to_keep.append(node)
    edges_to_keep = set(edges_to_keep)
    nodes_to_keep = set(nodes_to_keep)

    A = pygraphviz.AGraph(directed=True, strict=True, rankdir="LR", newrank=True)
    A.node_attr["style"] = "filled"
    A.node_attr["fillcolor"] = "lightcoral"

    def comp_sorter(key: Connector) -> int:
        return kat.index(key.name)

    A.add_edges_from(edges_to_keep)

    for comp in sorted(model.components, key=comp_sorter):
        comp: Connector
        comp_cluster = A.add_subgraph(
            name=f"cluster_{comp.name}", label=comp.name, bgcolor="lightblue"
        )
        for port in sorted(comp.ports, key=lambda c: c.name):
            if port.type is not NodeType.OPTICAL:
                continue
            port: Port
            port_cluster = comp_cluster.add_subgraph(
                name=f"cluster_{port.name}",
                label=port.name,
                bgcolor="lightyellow",
                rank="same",
            )
            for node in port.nodes:
                node: Node
                if node.type is NodeType.OPTICAL and node.full_name in nodes_to_keep:
                    port_cluster.add_node(node.full_name, label=node.name)

    A.draw(path, format="svg", prog="dot")
