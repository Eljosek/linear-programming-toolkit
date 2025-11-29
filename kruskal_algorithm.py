"""
Algoritmo de Kruskal - Árbol de Expansión Mínima (MST)
Encuentra el árbol de expansión mínima de un grafo no dirigido ponderado.

Autor: José Miguel Herrera Gutiérrez
Universidad Tecnológica de Pereira
"""

from typing import Dict, List, Tuple
import math


class UnionFind:
    """Estructura de datos Union-Find (Disjoint Set) para Kruskal"""
    
    def __init__(self, nodes: List[int]):
        """Inicializa Union-Find"""
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}
    
    def find(self, node: int) -> int:
        """Encuentra el representante (raíz) del conjunto"""
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])  # Compresión de camino
        return self.parent[node]
    
    def union(self, node1: int, node2: int) -> bool:
        """
        Une dos conjuntos
        
        Returns:
            True si se unieron (estaban en conjuntos diferentes)
            False si ya estaban en el mismo conjunto
        """
        root1 = self.find(node1)
        root2 = self.find(node2)
        
        if root1 == root2:
            return False  # Ya están en el mismo conjunto (formarían ciclo)
        
        # Union por rango
        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
        elif self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
        else:
            self.parent[root2] = root1
            self.rank[root1] += 1
        
        return True


class KruskalGraph:
    """Implementación del algoritmo de Kruskal"""
    
    def __init__(self, edges: List[Tuple[int, int, float]]):
        """
        Inicializa el grafo
        
        Args:
            edges: Lista de tuplas (nodo1, nodo2, peso)
        """
        self.edges = edges
        self.nodes = set()
        self.iterations = []
        
        # Recolectar todos los nodos
        for u, v, w in edges:
            self.nodes.add(u)
            self.nodes.add(v)
        
        self.nodes = sorted(list(self.nodes))
    
    def solve(self) -> Dict:
        """
        Ejecuta el algoritmo de Kruskal
        
        Returns:
            Diccionario con resultados
        """
        if not self.edges:
            return {
                'success': False,
                'error': 'El grafo no tiene aristas.'
            }
        
        if len(self.nodes) < 2:
            return {
                'success': False,
                'error': 'El grafo debe tener al menos 2 nodos.'
            }
        
        # Ordenar aristas por peso (ascendente)
        sorted_edges = sorted(self.edges, key=lambda x: x[2])
        
        # Inicializar Union-Find
        uf = UnionFind(self.nodes)
        
        # MST resultante
        mst_edges = []
        total_weight = 0
        iteration = 0
        
        # Procesar cada arista
        for u, v, w in sorted_edges:
            # Verificar si agregar esta arista forma un ciclo
            if uf.union(u, v):
                # No forma ciclo, agregar al MST
                mst_edges.append((u, v, w))
                total_weight += w
                
                self._save_iteration(iteration, u, v, w, True, 
                                   mst_edges.copy(), total_weight)
                iteration += 1
                
                # Si ya tenemos n-1 aristas, terminamos
                if len(mst_edges) == len(self.nodes) - 1:
                    break
            else:
                # Forma ciclo, rechazar
                self._save_iteration(iteration, u, v, w, False, 
                                   mst_edges.copy(), total_weight)
                iteration += 1
        
        # Verificar si el grafo es conexo
        if len(mst_edges) != len(self.nodes) - 1:
            return {
                'success': False,
                'error': f'El grafo no es conexo. Se encontraron {len(mst_edges)} aristas, '
                        f'pero se necesitan {len(self.nodes) - 1} para un árbol de expansión.'
            }
        
        return {
            'success': True,
            'mst_edges': [(u, v, round(w, 2)) for u, v, w in mst_edges],
            'total_weight': round(total_weight, 2),
            'num_nodes': len(self.nodes),
            'num_edges': len(mst_edges),
            'iterations': self.iterations,
            'graph_data': self._get_graph_data(),
            'mst_graph_data': self._get_mst_graph_data(mst_edges),
            'sorted_edges': [(u, v, round(w, 2)) for u, v, w in sorted_edges]
        }
    
    def _save_iteration(self, iteration: int, u: int, v: int, weight: float,
                       accepted: bool, current_mst: List, current_weight: float):
        """Guarda el estado de una iteración"""
        self.iterations.append({
            'iteration': iteration,
            'edge': (u, v),
            'weight': round(weight, 2),
            'accepted': accepted,
            'reason': 'Agregada al MST' if accepted else 'Rechazada (forma ciclo)',
            'mst_edges': [(u, v, round(w, 2)) for u, v, w in current_mst],
            'num_edges_in_mst': len(current_mst),
            'total_weight': round(current_weight, 2)
        })
    
    def _get_graph_data(self) -> Dict:
        """Prepara datos del grafo original para visualización"""
        nodes = [{'id': node, 'label': str(node)} for node in self.nodes]
        
        edges = []
        for u, v, w in self.edges:
            edges.append({
                'from': u,
                'to': v,
                'label': str(round(w, 2)),
                'weight': w
            })
        
        return {'nodes': nodes, 'edges': edges}
    
    def _get_mst_graph_data(self, mst_edges: List[Tuple[int, int, float]]) -> Dict:
        """Prepara datos del MST para visualización"""
        nodes = [{'id': node, 'label': str(node)} for node in self.nodes]
        
        edges = []
        for u, v, w in mst_edges:
            edges.append({
                'from': u,
                'to': v,
                'label': str(round(w, 2)),
                'weight': w,
                'color': '#10b981'  # Emerald color for MST edges
            })
        
        return {'nodes': nodes, 'edges': edges}


def solve_kruskal(edges: List[Tuple[int, int, float]]) -> Dict:
    """
    Wrapper function para resolver Kruskal
    
    Args:
        edges: Lista de aristas (nodo1, nodo2, peso)
    
    Returns:
        Diccionario con resultados
    """
    try:
        graph = KruskalGraph(edges)
        return graph.solve()
    except Exception as e:
        return {
            'success': False,
            'error': f'Error al ejecutar Kruskal: {str(e)}'
        }
