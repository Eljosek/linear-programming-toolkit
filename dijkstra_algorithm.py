"""
Algoritmo de Dijkstra - Camino más corto
Encuentra el camino más corto desde un nodo origen a todos los demás nodos
o a un nodo destino específico en un grafo ponderado.

Autor: José Miguel Herrera Gutiérrez
Universidad Tecnológica de Pereira
"""

import heapq
from typing import Dict, List, Tuple, Optional
import math


class DijkstraGraph:
    """Implementación del algoritmo de Dijkstra"""
    
    def __init__(self, edges: List[Tuple[int, int, float]], directed: bool = False):
        """
        Inicializa el grafo
        
        Args:
            edges: Lista de tuplas (origen, destino, peso)
            directed: Si es True, el grafo es dirigido; si es False, no dirigido
        """
        self.edges = edges
        self.directed = directed
        self.graph = {}
        self.nodes = set()
        self.iterations = []
        
        # Construir lista de adyacencia
        for u, v, w in edges:
            self.nodes.add(u)
            self.nodes.add(v)
            
            if u not in self.graph:
                self.graph[u] = []
            self.graph[u].append((v, w))
            
            # Si no es dirigido, agregar la arista inversa
            if not directed:
                if v not in self.graph:
                    self.graph[v] = []
                self.graph[v].append((u, w))
        
        # Asegurar que todos los nodos estén en el grafo
        for node in self.nodes:
            if node not in self.graph:
                self.graph[node] = []
    
    def solve(self, start: int, end: Optional[int] = None) -> Dict:
        """
        Ejecuta el algoritmo de Dijkstra
        
        Args:
            start: Nodo de inicio
            end: Nodo de destino (opcional). Si no se especifica, calcula caminos a todos
        
        Returns:
            Diccionario con resultados
        """
        if start not in self.nodes:
            return {
                'success': False,
                'error': f'El nodo de inicio {start} no existe en el grafo.'
            }
        
        if end is not None and end not in self.nodes:
            return {
                'success': False,
                'error': f'El nodo de destino {end} no existe en el grafo.'
            }
        
        # Inicializar distancias y predecesores
        distances = {node: math.inf for node in self.nodes}
        distances[start] = 0
        predecessors = {node: None for node in self.nodes}
        visited = set()
        
        # Cola de prioridad: (distancia, nodo)
        pq = [(0, start)]
        
        iteration = 0
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            # Si ya visitamos este nodo, continuar
            if current in visited:
                continue
            
            visited.add(current)
            
            # Guardar iteración
            self._save_iteration(iteration, current, current_dist, distances.copy(), 
                               visited.copy(), predecessors.copy())
            iteration += 1
            
            # Si llegamos al destino y se especificó uno, podemos terminar
            if end is not None and current == end:
                break
            
            # Explorar vecinos
            for neighbor, weight in self.graph.get(current, []):
                if neighbor not in visited:
                    new_dist = current_dist + weight
                    
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        predecessors[neighbor] = current
                        heapq.heappush(pq, (new_dist, neighbor))
        
        # Construir resultados
        if end is not None:
            # Camino específico
            if distances[end] == math.inf:
                return {
                    'success': False,
                    'error': f'No existe un camino desde {start} hasta {end}.'
                }
            
            path = self._reconstruct_path(start, end, predecessors)
            
            return {
                'success': True,
                'start': start,
                'end': end,
                'distance': round(distances[end], 2),
                'path': path,
                'all_distances': {k: round(v, 2) if v != math.inf else 'INF' 
                                 for k, v in distances.items()},
                'iterations': self.iterations,
                'graph_data': self._get_graph_data(),
                'path_edges': self._get_path_edges(path),
                'directed': self.directed
            }
        else:
            # Todos los caminos
            paths = {}
            for node in self.nodes:
                if node != start and distances[node] != math.inf:
                    paths[node] = self._reconstruct_path(start, node, predecessors)
            
            return {
                'success': True,
                'start': start,
                'end': None,
                'distances': {k: round(v, 2) if v != math.inf else 'INF' 
                            for k, v in distances.items()},
                'paths': paths,
                'iterations': self.iterations,
                'graph_data': self._get_graph_data(),
                'directed': self.directed
            }
    
    def _reconstruct_path(self, start: int, end: int, predecessors: Dict) -> List[int]:
        """Reconstruye el camino desde start hasta end"""
        path = []
        current = end
        
        while current is not None:
            path.append(current)
            current = predecessors[current]
        
        path.reverse()
        return path
    
    def _save_iteration(self, iteration: int, current: int, current_dist: float,
                       distances: Dict, visited: set, predecessors: Dict):
        """Guarda el estado de una iteración"""
        self.iterations.append({
            'iteration': iteration,
            'current_node': current,
            'current_distance': round(current_dist, 2) if current_dist != math.inf else 'INF',
            'distances': {k: round(v, 2) if v != math.inf else 'INF' 
                         for k, v in distances.items()},
            'visited': sorted(list(visited)),
            'unvisited': sorted(list(self.nodes - visited))
        })
    
    def _get_graph_data(self) -> Dict:
        """Prepara datos del grafo para visualización"""
        nodes = [{'id': node, 'label': str(node)} for node in sorted(self.nodes)]
        
        edges = []
        seen = set()
        for u, v, w in self.edges:
            edge_id = f"{u}-{v}"
            reverse_id = f"{v}-{u}"
            
            # Evitar duplicados en grafos no dirigidos
            if not self.directed and reverse_id in seen:
                continue
            
            edges.append({
                'from': u,
                'to': v,
                'label': str(round(w, 2)),
                'weight': w
            })
            seen.add(edge_id)
        
        return {'nodes': nodes, 'edges': edges}
    
    def _get_path_edges(self, path: List[int]) -> List[Tuple[int, int]]:
        """Obtiene las aristas que forman el camino"""
        edges = []
        for i in range(len(path) - 1):
            edges.append((path[i], path[i + 1]))
        return edges


def solve_dijkstra(edges: List[Tuple[int, int, float]], start: int, 
                  end: Optional[int] = None, directed: bool = False) -> Dict:
    """
    Wrapper function para resolver Dijkstra
    
    Args:
        edges: Lista de aristas (origen, destino, peso)
        start: Nodo inicial
        end: Nodo final (opcional)
        directed: Si el grafo es dirigido
    
    Returns:
        Diccionario con resultados
    """
    try:
        graph = DijkstraGraph(edges, directed)
        return graph.solve(start, end)
    except Exception as e:
        return {
            'success': False,
            'error': f'Error al ejecutar Dijkstra: {str(e)}'
        }
