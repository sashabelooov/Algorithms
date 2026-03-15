

class DirectedGraph:
    """An Instagram-style map — connections go ONE way only.

    If You follow Celebrity, that doesn't mean
    Celebrity follows You back!

    Attributes:
        graph: Dict mapping each person to who they FOLLOW.
    """

    def __init__(self) -> None:
        """Create an empty follow list — no people, no follows yet."""
        self.graph: dict[str, list[str]] = {}


    def add_node(self, node: str) -> None:
        """A new person joins Instagram — zero follows.

        If they already have an account, do nothing.

        Args:
            node: The person to add.

        Raises:
            ValueError: If node name is empty.
        """
        if not node:
            raise ValueError("Node name cannot be empty")

        if node not in self.graph:
            self.graph[node] = []


    def add_edge(self, from_node: str, to_node: str) -> None:
        """Follow someone — one-way connection only.

        from_node follows to_node, but NOT the other way around.
        Like hitting the Follow button on Instagram.

        Args:
            from_node: The person who follows.
            to_node: The person being followed.

        Raises:
            KeyError: If either person doesn't exist.
            ValueError: If trying to follow yourself.
        """
        if from_node == to_node:
            raise ValueError("Cannot follow yourself")

        if from_node not in self.graph:
            raise KeyError(f"'{from_node}' not found in graph")

        if to_node not in self.graph:
            raise KeyError(f"'{to_node}' not found in graph")

        if to_node not in self.graph[from_node]:
            self.graph[from_node].append(to_node)       # You follow Celebrity. Done!


    def display(self) -> None:
        """Print who follows who.

        Each line shows one person and everyone they follow.
        """
        for node, neighbors in self.graph.items():
            neighbors_str = ", ".join(neighbors)
            print(f"{node} --> {neighbors_str}")


    def remove_node(self, node: str) -> None:
        """Delete account — remove person and ALL connections to them.

        Must check EVERY person's list because in a directed graph
        anyone could be following you, not just your neighbors.

        Args:
            node: The person to remove.

        Raises:
            KeyError: If the person doesn't exist.
        """
        if node not in self.graph:
            raise KeyError(f"'{node}' not found in graph")

        for other_node in self.graph:                    # Check EVERY person
            if node in self.graph[other_node]:           # Are they following me?
                self.graph[other_node].remove(node)      # Remove me from their list

        del self.graph[node]                             # Delete my account



    def remove_edge(self, from_node: str, to_node: str) -> None:
        """Unfollow someone — remove one-way connection.

        Args:
            from_node: The person who unfollows.
            to_node: The person being unfollowed.

        Raises:
            KeyError: If either person doesn't exist.
            ValueError: If the follow doesn't exist.
        """
        if from_node not in self.graph:
            raise KeyError(f"'{from_node}' not found in graph")

        if to_node not in self.graph:
            raise KeyError(f"'{to_node}' not found in graph")

        if to_node not in self.graph[from_node]:
            raise ValueError(f"No edge from '{from_node}' to '{to_node}'")

        self.graph[from_node].remove(to_node)       # Only ONE side! That's it!



    def has_node(self, node: str) -> bool:
        """Check if a person has an account.

        Args:
            node: The person to look for.

        Returns:
            True if found, False otherwise.
        """
        return node in self.graph


    def has_edge(self, from_node: str, to_node: str) -> bool:
        """Check if from_node follows to_node.

        Direction matters! A→B does NOT mean B→A.

        Args:
            from_node: The person who might follow.
            to_node: The person who might be followed.

        Returns:
            True if from_node follows to_node.
        """
        if from_node not in self.graph or to_node not in self.graph:
            return False

        return to_node in self.graph[from_node]



    def get_neighbors(self, node: str) -> list[str]:
        """Get everyone this person follows.

        Args:
            node: The person to check.

        Returns:
            List of everyone they follow.

        Raises:
            KeyError: If the person doesn't exist.
        """
        if node not in self.graph:
            raise KeyError(f"'{node}' not found in graph")

        return self.graph[node]


    def __str__(self) -> str:
        """Return a string showing who follows who.

        Returns:
            Formatted string of all nodes and their connections.
        """
        lines: list[str] = []

        for node, neighbors in self.graph.items():
            neighbors_str = ", ".join(neighbors)
            lines.append(f"{node} --> {neighbors_str}")

        return "\n".join(lines)



if __name__ == "__main__":
    # === Test 1: Create empty graph ===
    g = DirectedGraph()
    assert g.graph == {}, "Graph should start empty"
    print("✓ Test 1: Empty graph created")

    # === Test 2: Add nodes ===
    g.add_node("You")
    g.add_node("Celebrity")
    g.add_node("Tommy")
    g.add_node("News Page")
    assert g.has_node("You"), "You should exist"
    assert g.has_node("Celebrity"), "Celebrity should exist"
    assert not g.has_node("Ghost"), "Ghost should not exist"
    print("✓ Test 2: Nodes added correctly")

    # === Test 3: Duplicate node does nothing ===
    g.add_node("You")
    assert len(g.graph) == 4, "Should still be 4 nodes"
    print("✓ Test 3: Duplicate node ignored")

    # === Test 4: Add edges (ONE direction!) ===
    g.add_edge("You", "Celebrity")
    g.add_edge("You", "Tommy")
    g.add_edge("Tommy", "News Page")
    g.add_edge("Celebrity", "News Page")
    assert g.has_edge("You", "Celebrity"), "You → Celebrity should exist"
    assert not g.has_edge("Celebrity", "You"), "Celebrity → You should NOT exist!"
    assert g.has_edge("Tommy", "News Page"), "Tommy → News Page should exist"
    assert not g.has_edge("News Page", "Tommy"), "News Page → Tommy should NOT exist!"
    print("✓ Test 4: Edges are ONE-WAY only!")

    # === Test 5: Get neighbors (who do I follow?) ===
    assert set(g.get_neighbors("You")) == {"Celebrity", "Tommy"}, "You follows 2 people"
    assert g.get_neighbors("News Page") == [], "News Page follows nobody"
    print("✓ Test 5: Neighbors correct")

    # === Test 6: Remove edge (unfollow) ===
    g.remove_edge("You", "Celebrity")
    assert not g.has_edge("You", "Celebrity"), "You unfollowed Celebrity"
    assert g.has_edge("Celebrity", "News Page"), "Celebrity still follows News Page"
    print("✓ Test 6: Edge removed from ONE side only")

    # === Test 7: Remove node (delete account) ===
    g.remove_node("Tommy")
    assert not g.has_node("Tommy"), "Tommy should be gone"
    assert "Tommy" not in g.get_neighbors("You"), "Tommy gone from You's list"
    print("✓ Test 7: Node removed + cleaned from ALL lists")

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
        print("✓ Test 9b: Self-follow rejected")

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
        g.remove_edge("You", "News Page")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Test 9e: Remove non-existent edge rejected")

    # === Test 10: Two-way follow (mutual follow) ===
    g.add_node("BestFriend")
    g.add_edge("You", "BestFriend")
    g.add_edge("BestFriend", "You")
    assert g.has_edge("You", "BestFriend"), "You → BestFriend"
    assert g.has_edge("BestFriend", "You"), "BestFriend → You"
    print("✓ Test 10: Mutual follow works as TWO separate edges")

    print("\n🎉 ALL TESTS PASSED! Your directed graph is solid!")
