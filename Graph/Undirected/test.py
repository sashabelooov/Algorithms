

class UndirectedGraph:
    def __init__(self) -> None:
        self.graph: dict[str, list[str]] = {}


    def add_node(self, node: str) -> None:
        if not node:
            raise ValueError("Node name cannot be empty")
        if node not in self.graph:
            self.graph[node] = []
            print(f"self.graph: {self.graph}\n")


    def add_edges(self, node1: str, node2: str) -> None:
        if node1 == node2:
            raise ValueError("No self-loop allowed")

        if node1 not in self.graph:
            raise KeyError(f"{node1} not found  in graph")

        if node2 not in self.graph:
            raise KeyError(f"{node2} not found  in graph")
        
        if node2 not in self.graph[node1]:
            self.graph[node1].append(node2)
            self.graph[node2].append(node1)
            print(f"self.graph added edges: {self.graph}")


    def display(self) -> None:
        for node, neighbors in self.graph.items():
            neighbors_str = ", ".join(neighbors)
            print(f"{node} --> {neighbors_str}")
            

