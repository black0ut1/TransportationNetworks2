import sys
from typing import List
from queue import Queue


def read_net_and_check_duplicate_edges(lines: List[str]) -> (dict, int):
    edges = {}
    nodes = 0

    i = 0
    for line in lines:
        i += 1

        spl = line.split(':')
        if spl[0] == "NODES":
            nodes = int(spl[1])

        if line.startswith("END"):
            break

    print("Checking duplicate edges...")
    duplicates = False

    for line in lines[i:]:
        split = line.split()
        start = int(split[0])
        end = int(split[1])
        capacity = float(split[2])
        freeflow = float(split[3])

        if (start, end) in edges:
            print(f"Edge ({start}, {end}) has duplicate")
            duplicates = True
        else:
            edges[(start, end)] = [capacity, freeflow]

    if not duplicates:
        print("No duplicates")

    return edges, nodes


def is_graph_complete(edges: dict, nodes: int):
    q = Queue()
    visited = [False] * nodes

    print("Checking graph completeness...")

    q.put(0)
    while not q.empty():
        node = q.get()
        if visited[node]:
            continue

        visited[node] = True

        neighbors = [v for u, v in edges.keys() if u == node]
        for neighbor in neighbors:
            q.put(neighbor)

    print(f"Graph is {'not ' if False in visited else ''}complete")


def check_mirror_edges(edges: dict):
    print("Checking mirror edges...")

    ok = True
    for u, v in edges:
        if (v, u) not in edges:
            print(f"Edge {u}->{v} does not have mirror edge")
            ok = False

    if ok:
        print("OK")



def properties(net_file: str):
    with open(net_file, 'r') as net:
        edges, nodes = read_net_and_check_duplicate_edges(net.readlines())
    is_graph_complete(edges, nodes)
    check_mirror_edges(edges)


if __name__ == '__main__':
    properties(sys.argv[1])