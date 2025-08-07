from collections import deque, defaultdict

class Graph:
    def __init__(self):
        self.graph = defaultdict(dict)
        self.flow_result = []

    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity
        if v not in self.graph or u not in self.graph[v]:
            self.graph[v][u] = 0  # зворотна дуга для залишкової мережі

    def bfs(self, source, sink, parent):
        visited = set()
        queue = deque([source])
        visited.add(source)

        while queue:
            u = queue.popleft()
            for v, capacity in self.graph[u].items():
                if v not in visited and capacity > 0:
                    visited.add(v)
                    parent[v] = u
                    if v == sink:
                        return True
                    queue.append(v)
        return False

    def edmonds_karp(self, source, sink):
        max_flow = 0
        flow_dict = defaultdict(lambda: defaultdict(int))

        while True:
            parent = {}
            if not self.bfs(source, sink, parent):
                break

            path_flow = float('inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            max_flow += path_flow

            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                flow_dict[u][v] += path_flow
                v = parent[v]

        self.flow_result = flow_dict
        return max_flow

    def print_terminal_to_store_flows(self):
        print("\n Фактичні потоки від терміналів до магазинів:\n")
        print(f"{'Термінал':<12} {'Магазин':<10} {'Фактичний Потік':>20}")
        print("-" * 44)
        for terminal in ['T1', 'T2']:
            for store in [f'M{i}' for i in range(1, 15)]:
                flow = self._find_terminal_to_store_flow(terminal, store)
                if flow > 0:
                    print(f"{terminal:<12} {store:<10} {flow:>20}")

    def _find_terminal_to_store_flow(self, terminal, store):
        # Рекурсивний пошук шляху термінал → склад → магазин
        total_flow = 0
        for warehouse in self.flow_result[terminal]:
            for dest in self.flow_result[warehouse]:
                if dest == store:
                    total_flow += min(
                        self.flow_result[terminal][warehouse],
                        self.flow_result[warehouse][store]
                    )
        return total_flow


# Побудова графа
g = Graph()

# Джерело та стік
g.add_edge('SOURCE', 'T1', float('inf'))
g.add_edge('SOURCE', 'T2', float('inf'))
for i in range(1, 15):
    g.add_edge(f'M{i}', 'SINK', float('inf'))

# Термінали → Склади
g.add_edge('T1', 'S1', 25)
g.add_edge('T1', 'S2', 20)
g.add_edge('T1', 'S3', 15)
g.add_edge('T2', 'S3', 15)
g.add_edge('T2', 'S4', 30)
g.add_edge('T2', 'S2', 10)

# Склади → Магазини
g.add_edge('S1', 'M1', 15)
g.add_edge('S1', 'M2', 10)
g.add_edge('S1', 'M3', 20)

g.add_edge('S2', 'M4', 15)
g.add_edge('S2', 'M5', 10)
g.add_edge('S2', 'M6', 25)

g.add_edge('S3', 'M7', 20)
g.add_edge('S3', 'M8', 15)
g.add_edge('S3', 'M9', 10)

g.add_edge('S4', 'M10', 20)
g.add_edge('S4', 'M11', 10)
g.add_edge('S4', 'M12', 15)
g.add_edge('S4', 'M13', 5)
g.add_edge('S4', 'M14', 10)

# Обчислення максимального потоку
max_flow = g.edmonds_karp('SOURCE', 'SINK')
print(f"\n Максимальний потік: {max_flow} одиниць")

# Вивід фактичних потоків до магазинів
g.print_terminal_to_store_flows()
