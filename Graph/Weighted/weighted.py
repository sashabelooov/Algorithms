

class WeightedGraph:
    """A Google Maps-style graph — every road has a distance.

    Each connection stores not just WHERE it goes,
    but HOW FAR it is (the weight).

    Attributes:
        graph: Dict mapping each city to list of (neighbor, weight) tuples.
    """

    def __init__(self) -> None:
        """Create an empty map — no cities, no roads yet."""
        self.graph: dict[str, list[tuple[str, int]]] = {}


    def add_node(self, node: str) -> None:
        """Add a new city to the map — no roads yet.

        Args:
            node: The city name to add.

        Raises:
            ValueError: If city name is empty.
        """
        if not node:
            raise ValueError("Node name cannot be empty")
        
        if node not in self.graph:
            self.graph[node] = []


    def add_edge(self, node1: str, node2: str, weight: int) -> None:
        """Build a road between two cities with a distance.

        Road goes both ways with the same distance (undirected).

        Args:
            node1: First city.
            node2: Second city.
            weight: Distance/cost of the road. Must be positive.

        Raises:
            KeyError: If either city doesn't exist.
            ValueError: If self-loop or negative weight or already connected.
        """
        if node1 == node2:
            raise ValueError("No self-loops allowed")

        if weight < 0:
            raise ValueError("Weight cannot be negative")

        if node1 not in self.graph:
            raise KeyError(f"'{node1}' not found in graph")

        if node2 not in self.graph:
            raise KeyError(f"'{node2}' not found in graph")

        for neighbor, _ in self.graph[node1]:         # Check if road already exists
            if neighbor == node2:
                raise ValueError(f"Edge already exists between '{node1}' and '{node2}'")

        self.graph[node1].append((node2, weight))     # Baku → (Tbilisi, 5)
        self.graph[node2].append((node1, weight))     # Tbilisi → (Baku, 5)


    def display(self) -> None:
        """
        Print the map — each city and its roads with distances.
        Shows each connection as neighbor(weight).
        """
        for node, neighbors in self.graph.items():
            neighbors_str = ", ".join(f"{n}({w})" for n, w in neighbors)
            print(f"{node} --> {neighbors_str}")


    def remove_edge(self, node1: str, node2: str) -> None:
        """Demolish a road between two cities.

        Removes from both sides since roads are two-way.

        Args:
            node1: First city.
            node2: Second city.

        Raises:
            KeyError: If either city doesn't exist.
            ValueError: If no road exists between them.
        """
        if node1 not in self.graph:
            raise KeyError(f"'{node1}' not found in graph")

        if node2 not in self.graph:
            raise KeyError(f"'{node2}' not found in graph")

        edge_found = False
        for neighbor, weight in self.graph[node1]:
            if neighbor == node2:
                self.graph[node1].remove((node2, weight))    # Remove from side 1
                self.graph[node2].remove((node1, weight))    # Remove from side 2
                edge_found = True
                break

        if not edge_found:
            raise ValueError(f"No edge between '{node1}' and '{node2}'")


    def remove_node(self, node: str) -> None:
        """Remove a city and ALL its roads.

        Visit every neighbor and tear down the road
        that leads back to this city.

        Args:
            node: The city to remove.

        Raises:
            KeyError: If the city doesn't exist.
        """
        if node not in self.graph:
            raise KeyError(f"'{node}' not found in graph")

        for neighbor, weight in self.graph[node]:               # My roads
            self.graph[neighbor].remove((node, weight))         # Remove me from their list

        del self.graph[node]                                    # Delete my city


    def has_node(self, node: str) -> bool:
        """Check if a city exists on the map.

        Args:
            node: The city to look for.

        Returns:
            True if found, False otherwise.
        """
        return node in self.graph
    

    def has_edge(self, node1: str, node2: str) -> bool:
        """Check if a road exists between two cities.

        Args:
            node1: First city.
            node2: Second city.

        Returns:
            True if a road exists, False otherwise.
        """
        if node1 not in self.graph or node2 not in self.graph:
            return False

        for neighbor, _ in self.graph[node1]:
            if neighbor == node2:
                return True

        return False
    

    def get_neighbors(self, node: str) -> list[tuple[str, int]]:
        """Get all roads from a city with their distances.

        Args:
            node: The city to check.

        Returns:
            List of (neighbor, weight) tuples.

        Raises:
            KeyError: If the city doesn't exist.
        """
        if node not in self.graph:
            raise KeyError(f"'{node}' not found in graph")

        return self.graph[node]


    def get_weight(self, node1: str, node2: str) -> int:
        """Get the distance between two directly connected cities.

        Like asking Google Maps 'how far from A to B?'

        Args:
            node1: Starting city.
            node2: Destination city.

        Returns:
            The weight of the road.

        Raises:
            KeyError: If either city doesn't exist.
            ValueError: If no direct road exists.
        """
        if node1 not in self.graph:
            raise KeyError(f"'{node1}' not found in graph")

        if node2 not in self.graph:
            raise KeyError(f"'{node2}' not found in graph")

        for neighbor, weight in self.graph[node1]:
            if neighbor == node2:
                return weight

        raise ValueError(f"No edge between '{node1}' and '{node2}'")


    def __str__(self) -> str:
        """Return a string showing the map with distances.

        Returns:
            Formatted string of all cities and their roads.
        """
        lines: list[str] = []

        for node, neighbors in self.graph.items():
            neighbors_str = ", ".join(f"{n}({w})" for n, w in neighbors)
            lines.append(f"{node} --> {neighbors_str}")

        return "\n".join(lines)



if __name__ == "__main__":
    # === Test 1: Create empty graph ===
    g = WeightedGraph()
    assert g.graph == {}, "Graph should start empty"
    print("✓ Test 1: Empty graph created")

    # === Test 2: Add nodes ===
    g.add_node("Baku")
    g.add_node("Tbilisi")
    g.add_node("Yerevan")
    g.add_node("Tehran")
    assert g.has_node("Baku"), "Baku should exist"
    assert not g.has_node("Mars"), "Mars should not exist"
    print("✓ Test 2: Nodes added correctly")

    # === Test 3: Duplicate node does nothing ===
    g.add_node("Baku")
    assert len(g.graph) == 4, "Should still be 4 nodes"
    print("✓ Test 3: Duplicate node ignored")

    # === Test 4: Add weighted edges ===
    g.add_edge("Baku", "Tbilisi", 5)
    g.add_edge("Tbilisi", "Yerevan", 2)
    g.add_edge("Baku", "Tehran", 3)
    assert g.has_edge("Baku", "Tbilisi"), "Baku-Tbilisi road should exist"
    assert g.has_edge("Tbilisi", "Baku"), "Tbilisi-Baku should also work (undirected!)"
    print("✓ Test 4: Weighted edges added both directions")

    # === Test 5: Get weight ===
    assert g.get_weight("Baku", "Tbilisi") == 5, "Baku-Tbilisi should be 5"
    assert g.get_weight("Tbilisi", "Baku") == 5, "Same distance both ways!"
    assert g.get_weight("Tbilisi", "Yerevan") == 2, "Tbilisi-Yerevan should be 2"
    print("✓ Test 5: Weights are correct")

    # === Test 6: Get neighbors (with weights!) ===
    baku_neighbors = g.get_neighbors("Baku")
    assert ("Tbilisi", 5) in baku_neighbors, "Baku should connect to Tbilisi(5)"
    assert ("Tehran", 3) in baku_neighbors, "Baku should connect to Tehran(3)"
    print("✓ Test 6: Neighbors include weights")

    # === Test 7: Remove edge ===
    g.remove_edge("Baku", "Tbilisi")
    assert not g.has_edge("Baku", "Tbilisi"), "Road should be gone"
    assert not g.has_edge("Tbilisi", "Baku"), "Gone from both sides!"
    assert g.has_edge("Tbilisi", "Yerevan"), "Other roads untouched"
    print("✓ Test 7: Edge removed from both sides")

    # === Test 8: Remove node ===
    g.remove_node("Yerevan")
    assert not g.has_node("Yerevan"), "Yerevan should be gone"
    for neighbor, _ in g.get_neighbors("Tbilisi"):
        assert neighbor != "Yerevan", "Yerevan gone from all lists"
    print("✓ Test 8: Node removed + cleaned from all lists")

    # === Test 9: Display and __str__ ===
    print("✓ Test 9: Display output:")
    g.display()
    print(f"  __str__: {g}")

    # === Test 10: Edge cases — Fail Fast ===
    try:
        g.add_node("")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Test 10a: Empty node name rejected")

    try:
        g.add_edge("Baku", "Baku", 5)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Test 10b: Self-loop rejected")

    try:
        g.add_edge("Baku", "Mars", 5)
        assert False, "Should have raised KeyError"
    except KeyError:
        print("✓ Test 10c: Edge to non-existent node rejected")

    try:
        g.add_edge("Baku", "Tehran", -3)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Test 10d: Negative weight rejected")

    try:
        g.get_weight("Baku", "Tbilisi")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Test 10e: Weight of non-existent edge rejected")

    try:
        g.add_edge("Baku", "Tehran", 10)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Test 10f: Duplicate edge rejected")

    print("\n🎉 ALL TESTS PASSED! Your weighted graph is solid!")
