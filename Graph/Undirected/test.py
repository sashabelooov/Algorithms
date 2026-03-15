

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
            

    def remove_node(self, node: str) -> None:
        if node not in self.graph:
            raise KeyError(f"'{node}' not found in graph")

        for neighbor in self.graph[node]:           # Visit each of Tommy's friends
            self.graph[neighbor].remove(node)       # Cross Tommy out of their list

        del self.graph[node]                        # Delete Tommy's page entirely


    def remove_edge(self, node1: str, node2: str) -> None:
        if node1 not in self.graph:
            raise KeyError(f"'{node1}' not found in graph")

        if node2 not in self.graph:
            raise KeyError(f"'{node2}' not found in graph")

        if node2 not in self.graph[node1]:              # Are they even friends?
            raise ValueError(f"No edge between '{node1}' and '{node2}'")

        self.graph[node1].remove(node2)                 # You remove Tommy
        self.graph[node2].remove(node1)                 # Tommy removes You

    def has_node(self, node: str) -> bool:
        return node in self.graph


    def has_edge(self, node1: str, node2: str) -> bool:
        if node1 not in self.graph or node2 not in self.graph:
            return False                                # Can't be friends if you don't exist

        return node2 in self.graph[node1]               # Is Tommy in Your list?


    def get_neighbors(self, node: str) -> list[str]:
        if node not in self.graph:
            raise KeyError(f"'{node}' not found in graph")

        return self.graph[node]


    def __str__(self) -> str:
        lines: list[str] = []

        for node, neighbors in self.graph.items():
            neighbors_str = ", ".join(neighbors)
            lines.append(f"{node} --> {neighbors_str}")

        return "\n".join(lines)

