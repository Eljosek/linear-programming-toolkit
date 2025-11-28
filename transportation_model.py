"""
Modelo de Transporte - Tres Métodos de Solución
- Esquina Noroeste (Northwest Corner)
- Costo Mínimo (Minimum Cost)
- Aproximación de Vogel (Vogel's Approximation Method - VAM)

Autor: José Miguel Herrera Gutiérrez
Universidad Tecnológica de Pereira
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from copy import deepcopy


def balance_problem(costs: List[List[float]], supply: List[float], demand: List[float]) -> Tuple:
    """
    Balancea un problema de transporte desbalanceado agregando fila/columna dummy.
    
    Args:
        costs: Matriz de costos m×n
        supply: Vector de oferta (m elementos)
        demand: Vector de demanda (n elementos)
    
    Returns:
        Tuple: (costs_balanced, supply_balanced, demand_balanced, balancing_info)
    """
    total_supply = sum(supply)
    total_demand = sum(demand)
    
    balancing_info = {
        'was_balanced': False,
        'dummy_type': None,
        'original_dimensions': (len(supply), len(demand)),
        'difference': 0
    }
    
    # Si ya está balanceado, retornar sin cambios
    if abs(total_supply - total_demand) < 1e-6:
        balancing_info['was_balanced'] = True
        return costs, supply, demand, balancing_info
    
    # Copiar datos originales
    costs_balanced = [row[:] for row in costs]
    supply_balanced = supply[:]
    demand_balanced = demand[:]
    
    if total_supply > total_demand:
        # Exceso de oferta: agregar columna dummy (destino ficticio)
        difference = total_supply - total_demand
        
        # Agregar columna de costos 0 a cada fila
        for row in costs_balanced:
            row.append(0.0)
        
        # Agregar demanda dummy
        demand_balanced.append(difference)
        
        balancing_info['dummy_type'] = 'column'
        balancing_info['difference'] = round(difference, 2)
        
    else:
        # Exceso de demanda: agregar fila dummy (origen ficticio)
        difference = total_demand - total_supply
        
        # Agregar fila de costos 0
        costs_balanced.append([0.0] * len(demand))
        
        # Agregar oferta dummy
        supply_balanced.append(difference)
        
        balancing_info['dummy_type'] = 'row'
        balancing_info['difference'] = round(difference, 2)
    
    return costs_balanced, supply_balanced, demand_balanced, balancing_info


class TransportationProblem:
    """Clase base para el problema de transporte"""
    
    def __init__(self, costs: List[List[float]], supply: List[float], demand: List[float]):
        """
        Inicializa el problema de transporte
        
        Args:
            costs: Matriz de costos (m×n) donde m=orígenes, n=destinos
            supply: Vector de ofertas (capacidad de cada origen)
            demand: Vector de demandas (necesidad de cada destino)
        """
        self.costs = np.array(costs, dtype=float)
        self.supply = np.array(supply, dtype=float)
        self.demand = np.array(demand, dtype=float)
        
        self.m = len(supply)  # Número de orígenes
        self.n = len(demand)  # Número de destinos
        
        # Verificar balanceo
        self.total_supply = np.sum(self.supply)
        self.total_demand = np.sum(self.demand)
        self.is_balanced = abs(self.total_supply - self.total_demand) < 1e-6
        
        # Iteraciones
        self.iterations = []
        self.current_iteration = 0
    
    def _save_iteration(self, allocation: np.ndarray, supply_left: np.ndarray, 
                       demand_left: np.ndarray, description: str, 
                       cell_assigned: Optional[Tuple[int, int]] = None,
                       amount: Optional[float] = None):
        """Guarda el estado de una iteración"""
        total_cost = np.sum(allocation * self.costs)
        
        iteration_data = {
            'iteration': self.current_iteration,
            'description': description,
            'allocation': allocation.copy().tolist(),
            'supply_left': supply_left.copy().tolist(),
            'demand_left': demand_left.copy().tolist(),
            'total_cost': round(total_cost, 2),
            'cell_assigned': cell_assigned,
            'amount': round(amount, 2) if amount is not None else None,
            'is_complete': np.all(supply_left < 1e-6) and np.all(demand_left < 1e-6)
        }
        
        self.iterations.append(iteration_data)
        self.current_iteration += 1
    
    def _format_solution(self, allocation: np.ndarray, method_name: str) -> Dict:
        """Formatea la solución final"""
        total_cost = np.sum(allocation * self.costs)
        
        # Crear diccionario de variables de decisión
        variables = {}
        for i in range(self.m):
            for j in range(self.n):
                if allocation[i, j] > 1e-6:
                    var_name = f"X{i+1}{j+1}"
                    variables[var_name] = {
                        'value': round(allocation[i, j], 2),
                        'cost': round(self.costs[i, j], 2),
                        'total': round(allocation[i, j] * self.costs[i, j], 2)
                    }
        
        return {
            'success': True,
            'method': method_name,
            'allocation': allocation.tolist(),
            'total_cost': round(total_cost, 2),
            'variables': variables,
            'iterations': self.iterations,
            'costs': self.costs.tolist(),
            'supply': self.supply.tolist(),
            'demand': self.demand.tolist(),
            'is_balanced': self.is_balanced
        }


class NorthwestCorner(TransportationProblem):
    """Método de la Esquina Noroeste"""
    
    def solve(self) -> Dict:
        """Resuelve usando el método de Esquina Noroeste"""
        # Inicializar
        allocation = np.zeros((self.m, self.n))
        supply_left = self.supply.copy()
        demand_left = self.demand.copy()
        
        self._save_iteration(allocation, supply_left, demand_left, 
                           "Tabla inicial - Método Esquina Noroeste")
        
        i, j = 0, 0  # Empezar en esquina noroeste
        
        while i < self.m and j < self.n:
            # Asignar el mínimo entre oferta y demanda
            amount = min(supply_left[i], demand_left[j])
            allocation[i, j] = amount
            supply_left[i] -= amount
            demand_left[j] -= amount
            
            self._save_iteration(
                allocation, supply_left, demand_left,
                f"Asignar {amount:.0f} unidades a celda ({i+1},{j+1})",
                cell_assigned=(i, j),
                amount=amount
            )
            
            # Moverse a la siguiente celda
            if supply_left[i] < 1e-6 and demand_left[j] < 1e-6:
                # Ambos satisfechos, moverse diagonal (priorizar fila)
                i += 1
                j += 1
            elif supply_left[i] < 1e-6:
                # Oferta agotada, siguiente fila
                i += 1
            else:
                # Demanda satisfecha, siguiente columna
                j += 1
        
        return self._format_solution(allocation, "Esquina Noroeste")


class MinimumCost(TransportationProblem):
    """Método del Costo Mínimo"""
    
    def solve(self) -> Dict:
        """Resuelve usando el método de Costo Mínimo"""
        # Inicializar
        allocation = np.zeros((self.m, self.n))
        supply_left = self.supply.copy()
        demand_left = self.demand.copy()
        
        self._save_iteration(allocation, supply_left, demand_left,
                           "Tabla inicial - Método Costo Mínimo")
        
        # Crear máscara de celdas disponibles
        available = np.ones((self.m, self.n), dtype=bool)
        
        while np.any(supply_left > 1e-6) and np.any(demand_left > 1e-6):
            # Encontrar celda con costo mínimo entre las disponibles
            masked_costs = np.where(available, self.costs, np.inf)
            
            # Buscar el mínimo
            min_cost = np.min(masked_costs)
            if min_cost == np.inf:
                break
            
            # Encontrar todas las celdas con costo mínimo
            min_positions = np.argwhere(masked_costs == min_cost)
            
            # Elegir la primera (criterio de desempate)
            i, j = min_positions[0]
            
            # Asignar el mínimo entre oferta y demanda
            amount = min(supply_left[i], demand_left[j])
            allocation[i, j] = amount
            supply_left[i] -= amount
            demand_left[j] -= amount
            
            self._save_iteration(
                allocation, supply_left, demand_left,
                f"Asignar {amount:.0f} unidades a celda ({i+1},{j+1}) con costo {self.costs[i,j]:.0f}",
                cell_assigned=(i, j),
                amount=amount
            )
            
            # Marcar fila/columna como no disponible si se agotó
            if supply_left[i] < 1e-6:
                available[i, :] = False
            if demand_left[j] < 1e-6:
                available[:, j] = False
        
        return self._format_solution(allocation, "Costo Mínimo")


class VogelMethod(TransportationProblem):
    """Método de Aproximación de Vogel (VAM)"""
    
    def _calculate_penalties(self, available: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula las penalizaciones para filas y columnas
        
        Returns:
            (row_penalties, col_penalties)
        """
        row_penalties = np.zeros(self.m)
        col_penalties = np.zeros(self.n)
        
        # Penalizaciones de filas
        for i in range(self.m):
            available_costs = self.costs[i, available[i, :]]
            if len(available_costs) >= 2:
                sorted_costs = np.sort(available_costs)
                row_penalties[i] = sorted_costs[1] - sorted_costs[0]
            elif len(available_costs) == 1:
                row_penalties[i] = available_costs[0]
            else:
                row_penalties[i] = -np.inf
        
        # Penalizaciones de columnas
        for j in range(self.n):
            available_costs = self.costs[available[:, j], j]
            if len(available_costs) >= 2:
                sorted_costs = np.sort(available_costs)
                col_penalties[j] = sorted_costs[1] - sorted_costs[0]
            elif len(available_costs) == 1:
                col_penalties[j] = available_costs[0]
            else:
                col_penalties[j] = -np.inf
        
        return row_penalties, col_penalties
    
    def solve(self) -> Dict:
        """Resuelve usando el Método de Vogel"""
        # Inicializar
        allocation = np.zeros((self.m, self.n))
        supply_left = self.supply.copy()
        demand_left = self.demand.copy()
        
        self._save_iteration(allocation, supply_left, demand_left,
                           "Tabla inicial - Método de Vogel (VAM)")
        
        # Crear máscara de celdas disponibles
        available = np.ones((self.m, self.n), dtype=bool)
        
        while np.any(supply_left > 1e-6) and np.any(demand_left > 1e-6):
            # Calcular penalizaciones
            row_penalties, col_penalties = self._calculate_penalties(available)
            
            # Encontrar la penalización máxima
            max_row_penalty = np.max(row_penalties)
            max_col_penalty = np.max(col_penalties)
            
            if max_row_penalty == -np.inf and max_col_penalty == -np.inf:
                break
            
            # Decidir si usar fila o columna
            if max_row_penalty >= max_col_penalty:
                # Usar fila con mayor penalización
                i = np.argmax(row_penalties)
                # Encontrar celda con costo mínimo en esa fila
                masked_costs = np.where(available[i, :], self.costs[i, :], np.inf)
                j = np.argmin(masked_costs)
                penalty_info = f"Fila {i+1} (penalización: {max_row_penalty:.0f})"
            else:
                # Usar columna con mayor penalización
                j = np.argmax(col_penalties)
                # Encontrar celda con costo mínimo en esa columna
                masked_costs = np.where(available[:, j], self.costs[:, j], np.inf)
                i = np.argmin(masked_costs)
                penalty_info = f"Columna {j+1} (penalización: {max_col_penalty:.0f})"
            
            # Asignar el mínimo entre oferta y demanda
            amount = min(supply_left[i], demand_left[j])
            allocation[i, j] = amount
            supply_left[i] -= amount
            demand_left[j] -= amount
            
            self._save_iteration(
                allocation, supply_left, demand_left,
                f"Asignar {amount:.0f} unidades a celda ({i+1},{j+1}) - {penalty_info}",
                cell_assigned=(i, j),
                amount=amount
            )
            
            # Marcar fila/columna como no disponible si se agotó
            if supply_left[i] < 1e-6:
                available[i, :] = False
            if demand_left[j] < 1e-6:
                available[:, j] = False
        
        return self._format_solution(allocation, "Vogel (VAM)")


def solve_transportation_problem(costs: List[List[float]], 
                                supply: List[float], 
                                demand: List[float],
                                method: str = 'northwest') -> Dict:
    """
    Resuelve un problema de transporte con el método especificado
    
    Args:
        costs: Matriz de costos
        supply: Vector de ofertas
        demand: Vector de demandas
        method: 'northwest', 'minimum_cost', 'vogel', o 'all'
    
    Returns:
        Dict con la solución
    """
    try:
        # Validaciones
        if not costs or not supply or not demand:
            return {
                'success': False,
                'error': 'Datos incompletos. Verifique costos, ofertas y demandas.'
            }
        
        costs_array = np.array(costs)
        if costs_array.shape[0] != len(supply):
            return {
                'success': False,
                'error': 'El número de filas de costos debe coincidir con el número de orígenes.'
            }
        
        if costs_array.shape[1] != len(demand):
            return {
                'success': False,
                'error': 'El número de columnas de costos debe coincidir con el número de destinos.'
            }
        
        # Balancear el problema automáticamente si es necesario
        costs_balanced, supply_balanced, demand_balanced, balancing_info = balance_problem(costs, supply, demand)
        
        # Resolver según método
        if method == 'all':
            # Resolver con los 3 métodos
            nw = NorthwestCorner(costs_balanced, supply_balanced, demand_balanced)
            result_nw = nw.solve()
            result_nw['balancing_info'] = balancing_info
            
            mc = MinimumCost(costs_balanced, supply_balanced, demand_balanced)
            result_mc = mc.solve()
            result_mc['balancing_info'] = balancing_info
            
            vogel = VogelMethod(costs_balanced, supply_balanced, demand_balanced)
            result_vogel = vogel.solve()
            result_vogel['balancing_info'] = balancing_info
            
            return {
                'success': True,
                'method': 'Comparación de los 3 métodos',
                'results': {
                    'northwest': result_nw,
                    'minimum_cost': result_mc,
                    'vogel': result_vogel
                },
                'comparison': _create_comparison_table(result_nw, result_mc, result_vogel),
                'costs': costs,
                'supply': supply,
                'demand': demand,
                'balancing_info': balancing_info
            }
        
        elif method == 'northwest':
            solver = NorthwestCorner(costs_balanced, supply_balanced, demand_balanced)
        elif method == 'minimum_cost':
            solver = MinimumCost(costs_balanced, supply_balanced, demand_balanced)
        elif method == 'vogel':
            solver = VogelMethod(costs_balanced, supply_balanced, demand_balanced)
        else:
            return {
                'success': False,
                'error': f'Método desconocido: {method}'
            }
        
        result = solver.solve()
        result['balancing_info'] = balancing_info
        return result
    
    except Exception as e:
        return {
            'success': False,
            'error': f'Error al resolver el problema: {str(e)}'
        }


def _create_comparison_table(result_nw: Dict, result_mc: Dict, result_vogel: Dict) -> Dict:
    """Crea tabla comparativa de los 3 métodos"""
    # Recolectar todas las variables posibles
    all_vars = set()
    all_vars.update(result_nw['variables'].keys())
    all_vars.update(result_mc['variables'].keys())
    all_vars.update(result_vogel['variables'].keys())
    all_vars = sorted(all_vars)
    
    comparison = {
        'variables': all_vars,
        'northwest': [],
        'minimum_cost': [],
        'vogel': [],
        'totals': {
            'northwest': result_nw['total_cost'],
            'minimum_cost': result_mc['total_cost'],
            'vogel': result_vogel['total_cost']
        }
    }
    
    for var in all_vars:
        comparison['northwest'].append(
            result_nw['variables'].get(var, {'value': 0})['value']
        )
        comparison['minimum_cost'].append(
            result_mc['variables'].get(var, {'value': 0})['value']
        )
        comparison['vogel'].append(
            result_vogel['variables'].get(var, {'value': 0})['value']
        )
    
    # Determinar el mejor método
    min_cost = min(
        result_nw['total_cost'],
        result_mc['total_cost'],
        result_vogel['total_cost']
    )
    
    if result_nw['total_cost'] == min_cost:
        comparison['best_method'] = 'Esquina Noroeste'
    elif result_mc['total_cost'] == min_cost:
        comparison['best_method'] = 'Costo Mínimo'
    else:
        comparison['best_method'] = 'Vogel'
    
    return comparison
