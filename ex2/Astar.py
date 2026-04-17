class Graph:
    def __init__(self):
        self.adj = {}

    def add_node(self, node):
        if node not in self.adj:
            self.adj[node] = []
            print(f"Node {node} successfully added.")
        else:
            print("Error: Node already exists.")

    def delete_node(self, node):
        if node in self.adj:
            for i in self.adj:
                self.adj[i] = [x for x in self.adj[i] if x[0] != node]
            del self.adj[node]
            print(f"Node {node} removed.")
        else:
            print("Error: Node not found.")

    def add_edge(self, n1, n2, cost):
        if n1 in self.adj and n2 in self.adj:
            self.delete_edge(n1, n2)
            self.adj[n1].append((n2, cost))
            self.adj[n2].append((n1, cost))
            print(f"Link created: {n1} to {n2} (cost {cost})")
        else:
            print("Error: Nodes must exist.")

    def delete_edge(self, n1, n2):
        if n1 in self.adj and n2 in self.adj:
            self.adj[n1] = [x for x in self.adj[n1] if x[0] != n2]
            self.adj[n2] = [x for x in self.adj[n2] if x[0] != n1]
        else:
            print("Error: Nodes not found.")

    def display(self):
        print("\n--- Current Graph ---")
        for i in self.adj:
            print(f" {i} -> {self.adj[i]}")

def a_star(graph, start, goal):
    if start not in graph.adj or goal not in graph.adj:
        print("Error: Starting or Target node is missing.")
        return None

    print(f"\n[Heuristic Input for Goal {goal}]")
    heuristics = {node: int(input(f" Enter h for {node}: ")) for node in graph.adj}

    queue = [[heuristics[start], 0, start, [start]]]
    closed_list = []
    round_num = 1

    print("\n--- A* Calculation Trace ---")

    while queue:
        queue.sort(key=lambda x: x[0])
        current_open = [item[2] for item in queue]

        f, g, current, path = queue.pop(0)

        print(f"\nRound {round_num}")
        print(f" Open Nodes   : {current_open}")
        print(f" Closed Nodes : {closed_list}")
        print(f" Processing   : {current} (f={f}, g={g}, h={heuristics[current]})")

        if current == goal:
            print("\n*** SUCCESS ***")
            print(f" Best Path : {' >> '.join(path)}")
            print(f" Total Cost: {g}")
            return path, g

        if current not in closed_list:
            closed_list.append(current)
            for neighbor, weight in graph.adj[current]:
                if neighbor in closed_list:
                    continue

                new_g = g + weight
                new_f = new_g + heuristics[neighbor]

                found_in_queue = False
                for i in range(len(queue)):
                    if queue[i][2] == neighbor:
                        found_in_queue = True
                        if new_g < queue[i][1]:
                            queue[i] = [new_f, new_g, neighbor, path + [neighbor]]
                        break

                if not found_in_queue:
                    queue.append([new_f, new_g, neighbor, path + [neighbor]])
        round_num += 1

    print("\nNo path discovered.")
    return None

# Simple Interface
graph = Graph()
try:
    num = int(input("Total nodes: "))
    for _ in range(num):
        graph.add_node(input("Node: "))
    edg = int(input("Total edges: "))
    for _ in range(edg):
        u, v, c = input("Node 1: "), input("Node 2: "), int(input("Cost: "))
        graph.add_edge(u, v, c)
except ValueError:
    print("Invalid input.")

while True:
    print("\n1.Add Node | 2.Del Node | 3.Add Edge | 4.Del Edge | 5.Show | 6.A* | 7.Exit")
    choice = input("Choice: ")
    if choice == '1': graph.add_node(input("Node: "))
    elif choice == '2': graph.delete_node(input("Node: "))
    elif choice == '3': graph.add_edge(input("N1: "), input("N2: "), int(input("Cost: ")))
    elif choice == '4': graph.delete_edge(input("N1: "), input("N2: "))
    elif choice == '5': graph.display()
    elif choice == '6': a_star(graph, input("Start: "), input("Goal: "))
    elif choice == '7': break
