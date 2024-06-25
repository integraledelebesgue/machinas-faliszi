from typing import Self
from collections.abc import Generator
from functools import cached_property, cache
from itertools import combinations
from copy import deepcopy


type Edge = tuple[int, int]
type NeighborList = dict[int, set[int]]


def parse(input: str) -> 'Graph':
    vertices: NeighborList = dict()

    for line in input.split('\n'):
        match line.split():
            case []:
                continue

            case ['c', *_]:
                continue

            case ['p', _, str(n_vertices), *_]:
                for i in range(int(n_vertices) + 1):
                    vertices[i] = set()

            case ['e', str(start), str(end), *_]:
                start = int(start)
                end = int(end)

                vertices[start].add(end)
                vertices[end].add(start)

            case other:
                raise RuntimeError(
                    f'Invalid record format encountered: {other}'
                )
            
    return Graph(vertices)


class Graph:
    topology: NeighborList

    def __init__(self, vertices: NeighborList) -> None:
        self.topology = vertices

    def __len__(self) -> int:
        return len(self.topology)
    
    @cached_property
    def edges(self) -> list[Edge]:
        return list(sum(map(
            lambda u: [(u, v) for v in self.topology[u]],
            self.topology.keys()
        ), start=[]))
    
    @cache
    def degree(self, vertex: int) -> int:
        return len(self.topology[vertex])
    
    @staticmethod
    def load(path: str) -> 'Graph':
        with open(path, 'r') as file:
            return parse(file.read())
        
    def drop(self, vertex: int) -> Self:
        topology = deepcopy(self.topology)
        neighbours = topology.pop(vertex)
        topology[vertex] = set()

        for neighbour in neighbours:
            topology[neighbour].remove(vertex)

        return Graph(topology)
    
    def drop_in_place(self, vertex: int) -> Self:
        neighbours = self.topology.pop(vertex)
        self.topology[vertex] = set()

        for neighbour in neighbours:
            self.topology[neighbour].remove(vertex)

        return self
    
    def has_edge(self) -> bool:
        return any(
            len(neighbours) > 0 
            for neighbours in self.topology.values()
        )
    
    def is_vertex_cover(self, subgraph: set[int]) -> bool:
        for (u, v) in self.edges:
            if u not in subgraph and v not in subgraph:
                return False
            
        return True
    
    def copy(self) -> Self:
        return Graph(deepcopy(self.topology))


def subsets(graph: Graph, cardinality: int) -> Generator[set[int], None, None]:
    vertices = graph.topology.keys()

    for comb in combinations(vertices, cardinality):
        yield set(comb)


def drop_vertex(edges: list[Edge], vertex: int) -> list[Edge]:
    return [
        (x, y)
        for x, y in edges
        if x != vertex and y != vertex
    ]


def drop_subset(edges: list[Edge], subset: set[int]) -> list[Edge]:
    return [
        (x, y)
        for x, y in edges
        if x not in subset
        and y not in subset
    ]