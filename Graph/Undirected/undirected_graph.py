
class UndirectedGraph:
    """A friendship map — every connection goes both ways.

    Think of it as a phone book where if you have someone's number,
    they also have yours.

    Attributes:
        graph: A graph is a way to show connections between things.
    """
    def __init__(self) -> None:
        """Create an empty friend group — no people, no friendships yet."""
        self.graph: dict[str, list[str]] = {}

    def add_node(self, node: str) -> None:
        """Add a new person to the neighborhood.

        Like a new kid moving in — they start with zero friends.
        If they already live here, do nothing (no duplicates).

        Args:
            node: The name of the person to add.

        Raises:
            ValueError: If node name is empty.
        """

        if not node:
            raise ValueError("Node name cannot be empty")
        
        if node not in self.graph:
            self.graph[node] = []
            print(f"self.graph: {self.graph}")

    def add_edge(self, node1: str, node2: str) -> None:
        """Make two people friends (two-way connection).

        Like a handshake — both people add each other
        to their friend lists.

        Args:
            node1: First person.
            node2: Second person.

        Raises:
            KeyError: If either person doesn't exist in the graph.
            ValueError: If trying to befriend yourself.
        """
        if node1 == node2:                          # Can't be your own friend!
            raise ValueError("No self-loops allowed")

        if node1 not in self.graph:                 # Person 1 must exist
            raise KeyError(f"'{node1}' not found in graph")

        if node2 not in self.graph:                 # Person 2 must exist
            raise KeyError(f"'{node2}' not found in graph")

        if node2 not in self.graph[node1]:          # Not already friends?
            self.graph[node1].append(node2)         # You add Tommy
            self.graph[node2].append(node1)         # Tommy adds You
            print(f"self.graph added edges: {self.graph}")



    def display(self) -> None:
        """Print the neighborhood map — who is friends with who.

        Each line shows one person and all their friends,
        like reading a phone book page by page.
        """

        for node, neighbors in self.graph.items():
            neighbors_str = ", ".join(neighbors)
            print(f"{node} --> {neighbors_str}")



    def remove_node(self, node: str) -> None:
        """Remove a person and ALL their friendships.

        Like someone moving out of town — erase them from
        every friend's list, then delete their phone book page.

        Args:
            node: The person to remove.

        Raises:
            KeyError: If the person doesn't exist in the graph.
        """
        if node not in self.graph:
            raise KeyError(f"'{node}' not found in graph")

        for neighbor in self.graph[node]:           # Visit each of Tommy's friends
            self.graph[neighbor].remove(node)       # Cross Tommy out of their list

        del self.graph[node]                        # Delete Tommy's page entirely


    def remove_edge(self, node1: str, node2: str) -> None:
        """Break a friendship — remove connection from both sides.

        Like tearing a page from both phone books at once.

        Args:
            node1: First person.
            node2: Second person.

        Raises:
            KeyError: If either person doesn't exist in the graph.
            ValueError: If they are not friends.
        """
        if node1 not in self.graph:
            raise KeyError(f"'{node1}' not found in graph")

        if node2 not in self.graph:
            raise KeyError(f"'{node2}' not found in graph")

        if node2 not in self.graph[node1]:              # Are they even friends?
            raise ValueError(f"No edge between '{node1}' and '{node2}'")

        self.graph[node1].remove(node2)                 # You remove Tommy
        self.graph[node2].remove(node1)                 # Tommy removes You

    def has_node(self, node: str) -> bool:
        """Check if a person lives in the neighborhood.

        Like flipping through the phone book — is their name there?

        Args:
            node: The person to look for.

        Returns:
            True if found, False otherwise.
        """
        return node in self.graph


    def has_edge(self, node1: str, node2: str) -> bool:
        """Check if two people are friends.

        Like checking one person's phone book page
        for the other person's name.

        Args:
            node1: First person.
            node2: Second person.

        Returns:
            True if they are friends, False otherwise.
        """
        if node1 not in self.graph or node2 not in self.graph:
            return False                                # Can't be friends if you don't exist

        return node2 in self.graph[node1]               # Is Tommy in Your list?


    def get_neighbors(self, node: str) -> list[str]:
        """Get all friends of a person.

        Like reading one page of the phone book —
        shows everyone this person is connected to.

        Args:
            node: The person whose friends you want.

        Returns:
            List of all friends.

        Raises:
            KeyError: If the person doesn't exist.
        """
        if node not in self.graph:
            raise KeyError(f"'{node}' not found in graph")

        return self.graph[node]


    def __str__(self) -> str:
        """Return a string showing the neighborhood map.

        Called automatically when you do print(graph).
        Like display(), but returns text instead of printing it.

        Returns:
            A formatted string of all nodes and their neighbors.
        """
        lines: list[str] = []

        for node, neighbors in self.graph.items():
            neighbors_str = ", ".join(neighbors)
            lines.append(f"{node} --> {neighbors_str}")

        return "\n".join(lines)


if __name__ == "__main__":
    # === Test 1: Create empty graph ===
    g = UndirectedGraph()
    assert g.graph == {}, "Graph should start empty"
    print("✓ Test 1: Empty graph created")

    # === Test 2: Add nodes ===
    g.add_node("You")
    g.add_node("Tommy")
    g.add_node("Sara")
    assert g.has_node("You"), "You should exist"
    assert g.has_node("Tommy"), "Tommy should exist"
    assert g.has_node("Sara"), "Sara should exist"
    assert not g.has_node("Ghost"), "Ghost should not exist"
    print("✓ Test 2: Nodes added correctly")

    # === Test 3: Duplicate node does nothing ===
    g.add_node("You")
    assert len(g.graph) == 3, "Should still be 3 nodes"
    print("✓ Test 3: Duplicate node ignored")

    # === Test 4: Add edges ===
    g.add_edge("You", "Tommy")
    g.add_edge("You", "Sara")
    assert g.has_edge("You", "Tommy"), "You-Tommy should be friends"
    assert g.has_edge("Tommy", "You"), "Tommy-You should also work (undirected!)"
    assert not g.has_edge("Tommy", "Sara"), "Tommy-Sara not friends yet"
    print("✓ Test 4: Edges added correctly (both directions!)")

    # === Test 5: Get neighbors ===
    assert set(g.get_neighbors("You")) == {"Tommy", "Sara"}, "You should have 2 friends"
    assert g.get_neighbors("Tommy") == ["You"], "Tommy has 1 friend"
    print("✓ Test 5: Neighbors correct")

    # === Test 6: Remove edge ===
    g.add_edge("Tommy", "Sara")
    g.remove_edge("You", "Tommy")
    assert not g.has_edge("You", "Tommy"), "Friendship should be gone"
    assert not g.has_edge("Tommy", "You"), "Gone from both sides!"
    assert g.has_edge("Tommy", "Sara"), "Tommy-Sara still friends"
    print("✓ Test 6: Edge removed from both sides")

    # === Test 7: Remove node ===
    g.remove_node("Sara")
    assert not g.has_node("Sara"), "Sara should be gone"
    assert "Sara" not in g.get_neighbors("You"), "Sara gone from You's list"
    assert "Sara" not in g.get_neighbors("Tommy"), "Sara gone from Tommy's list"
    print("✓ Test 7: Node removed + cleaned from all lists")

    # === Test 8: Display and __str__ ===
    print("✓ Test 8: Display output:")
    g.display()
    print(f"  __str__: {g}")

    # === Test 9: Edge cases — Fail Fast ===
    try:
        g.add_node("")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Test 9a: Empty node name rejected")

    try:
        g.add_edge("You", "You")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Test 9b: Self-loop rejected")

    try:
        g.add_edge("You", "Ghost")
        assert False, "Should have raised KeyError"
    except KeyError:
        print("✓ Test 9c: Edge to non-existent node rejected")

    try:
        g.remove_node("Ghost")
        assert False, "Should have raised KeyError"
    except KeyError:
        print("✓ Test 9d: Remove non-existent node rejected")

    try:
        g.remove_edge("You", "Tommy")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Test 9e: Remove non-existent edge rejected")

    print("\n🎉 ALL TESTS PASSED! Your undirected graph is solid!")
