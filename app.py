# archivo: app.py
"""
Aplicación web Flask para resolver problemas de programación lineal 
usando el método gráfico.

Autor: Para curso de Investigación de Operaciones
Fecha: 2025
"""

import os
import sys
import importlib
import json
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from lp_solver import solve_lp_problem
import simplex_tableau
import dual_simplex_tableau
import two_phase_simplex
import transportation_model
import dijkstra_algorithm
import kruskal_algorithm

# Recargar módulos en cada petición (útil en desarrollo)
if 'WERKZEUG_RUN_MAIN' in os.environ or not os.environ.get('FLASK_ENV'):
    importlib.reload(simplex_tableau)
    importlib.reload(dual_simplex_tableau)
    importlib.reload(two_phase_simplex)
    importlib.reload(transportation_model)
    importlib.reload(dijkstra_algorithm)
    importlib.reload(kruskal_algorithm)

# Crear instancia de la aplicación Flask
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'utp-investigacion-operaciones-jose-herrera-2025')

# Filtro personalizado para formatear números de manera inteligente
@app.template_filter('smart_number')
def smart_number_filter(value):
    """
    Formatea números de manera inteligente:
    - Enteros se muestran sin decimales
    - Decimales se muestran con máximo 2-4 decimales significativos
    """
    try:
        num = float(value)
        # Si es muy cercano a cero, mostrar como 0
        if abs(num) < 1e-10:
            return "0"
        # Si es un entero (o muy cercano), mostrar sin decimales
        if abs(num - round(num)) < 1e-10:
            return str(int(round(num)))
        # Si tiene decimales, mostrar con 2 decimales
        if abs(num) >= 0.01:
            formatted = f"{num:.2f}"
            # Eliminar ceros innecesarios al final
            formatted = formatted.rstrip('0').rstrip('.')
            return formatted
        # Para números muy pequeños, usar notación científica
        return f"{num:.2e}"
    except (ValueError, TypeError):
        return str(value)

@app.route('/')
def index():
    """
    Página principal con el formulario para ingresar el problema de LP.
    """
    return render_template('index.html')

@app.route('/graphical')
def graphical():
    """
    Ruta alternativa para el método gráfico (redirige a index).
    """
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    """
    Procesa el formulario y resuelve el problema de programación lineal.
    """
    # Obtener datos del formulario
    objective = request.form.get('objective', '').strip()
    constraints_text = request.form.get('constraints', '').strip()
    
    # Validar que se ingresaron datos
    if not objective:
        flash('Por favor ingresa una función objetivo.', 'error')
        return redirect(url_for('index'))
    
    if not constraints_text:
        flash('Por favor ingresa al menos una restricción.', 'error')
        return redirect(url_for('index'))
    
    # Procesar restricciones (una por línea)
    constraints_list = [line.strip() for line in constraints_text.split('\n') 
                       if line.strip()]
    
    if not constraints_list:
        flash('Por favor ingresa al menos una restricción válida.', 'error')
        return redirect(url_for('index'))
    
    # Resolver el problema
    try:
        result = solve_lp_problem(objective, constraints_list)
        
        if not result['success']:
            flash(result['error'], 'error')
            return redirect(url_for('index'))
        
        # Preparar datos para mostrar en la página de resultados
        context = {
            'objective': objective,
            'constraints': constraints_list,
            'opt_type': result['opt_type'],
            'obj_coeffs': result['obj_coeffs'],
            'vertices': result['vertices'],
            'results': result['results'],
            'best_point': result['best_point'],
            'best_value': result['best_value'],
            'graphic': result['graphic']
        }
        
        return render_template('results.html', **context)
        
    except Exception as e:
        flash(f'Error inesperado: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/simplex')
def simplex():
    """
    Página para resolver problemas usando el método Simplex.
    """
    return render_template('simplex.html')

@app.route('/solve-simplex', methods=['POST'])
def solve_simplex_route():
    """
    Procesa el formulario y resuelve el problema usando método Simplex con tableau.
    """
    try:
        objective = request.form.get('objective', '').strip()
        constraints_text = request.form.get('constraints', '').strip()
        
        if not objective or not constraints_text:
            flash('Por favor completa todos los campos.', 'error')
            return redirect(url_for('simplex'))
        
        constraints_list = [line.strip() for line in constraints_text.split('\n') 
                           if line.strip()]
        
        # Usar el solver con tableau para mostrar iteraciones paso a paso
        result = simplex_tableau.solve_simplex_tableau(objective, constraints_list)
        
        if not result['success']:
            flash(result['error'], 'error')
            return redirect(url_for('simplex'))
        
        return render_template('simplex_results.html', 
                             objective=objective,
                             constraints=constraints_list,
                             result=result,
                             solution=result.get('solution', {}),
                             optimal_value=result.get('optimal_value', 0),
                             opt_type=result.get('opt_type', 'max'),
                             status=result.get('status', 'unknown'),
                             iterations=result.get('iterations', []))
        
    except Exception as e:
        flash(f'Error inesperado: {str(e)}', 'error')
        return redirect(url_for('simplex'))

@app.route('/dual-simplex')
def dual_simplex():
    """
    Página para resolver problemas usando el método Dual Simplex.
    """
    return render_template('dual_simplex.html')

@app.route('/solve-dual-simplex', methods=['POST'])
def solve_dual_simplex_route():
    """
    Procesa el formulario y resuelve el problema usando método Dual Simplex con tableau.
    """
    try:
        objective = request.form.get('objective', '').strip()
        constraints_text = request.form.get('constraints', '').strip()
        
        if not objective or not constraints_text:
            flash('Por favor completa todos los campos.', 'error')
            return redirect(url_for('dual_simplex'))
        
        constraints_list = [line.strip() for line in constraints_text.split('\n') 
                           if line.strip()]
        
        # Usar el solver con tableau para mostrar iteraciones paso a paso
        result = dual_simplex_tableau.solve_dual_simplex_tableau(objective, constraints_list)
        
        if not result['success']:
            flash(result['error'], 'error')
            return redirect(url_for('dual_simplex'))
        
        return render_template('dual_simplex_results.html', 
                             objective=objective,
                             constraints=constraints_list,
                             result=result,
                             solution=result.get('solution', {}),
                             optimal_value=result.get('optimal_value', 0),
                             opt_type=result.get('opt_type', 'min'),
                             status=result.get('status', 'unknown'),
                             iterations=result.get('iterations', []))
        
    except Exception as e:
        flash(f'Error inesperado: {str(e)}', 'error')
        return redirect(url_for('dual_simplex'))

@app.route('/two-phase-simplex')
def two_phase_simplex_route():
    """
    Página para resolver problemas usando el método Simplex Dos Fases.
    """
    return render_template('two_phase_simplex.html')

@app.route('/solve-two-phase-simplex', methods=['POST'])
def solve_two_phase_simplex_route():
    """
    Procesa el formulario y resuelve el problema usando método Simplex Dos Fases.
    """
    try:
        objective = request.form.get('objective', '').strip()
        constraints_text = request.form.get('constraints', '').strip()
        
        if not objective or not constraints_text:
            flash('Por favor completa todos los campos.', 'error')
            return redirect(url_for('two_phase_simplex_route'))
        
        constraints_list = [line.strip() for line in constraints_text.split('\n') 
                           if line.strip()]
        
        # Usar el solver Dos Fases
        result = two_phase_simplex.solve_two_phase_simplex(objective, constraints_list)
        
        if not result['success']:
            flash(result.get('error', 'Error desconocido'), 'error')
            return redirect(url_for('two_phase_simplex_route'))
        
        return render_template('two_phase_simplex_results.html', 
                             objective=objective,
                             constraints=constraints_list,
                             result=result,
                             solution=result.get('solution', {}),
                             optimal_value=result.get('optimal_value', 0),
                             opt_type=result.get('opt_type', 'max'),
                             status=result.get('status', 'unknown'),
                             iterations_phase1=result.get('iterations_phase1', []),
                             iterations_phase2=result.get('iterations_phase2', []),
                             total_iterations=result.get('total_iterations', 0))
        
    except Exception as e:
        flash(f'Error inesperado: {str(e)}', 'error')
        return redirect(url_for('two_phase_simplex_route'))

@app.route('/about')
def about():
    """
    Página con información sobre el método gráfico.
    """
    return render_template('about.html')

@app.route('/examples')
def examples():
    """
    Página con ejemplos de problemas de programación lineal.
    """
    examples_data = [
        # Ejemplos para Método Gráfico (2 variables)
        {
            'title': 'Método Gráfico - Ejercicio del Taller 1',
            'method': 'grafico',
            'objective': 'maximizar z = x + y',
            'constraints': 'x + 3y <= 26\n4x + 3y <= 44\n2x + 3y <= 28\nx >= 0\ny >= 0',
            'description': 'Problema clásico de maximización con restricciones lineales (2 variables).',
            'icon': 'chart-area',
            'color': 'success'
        },
        {
            'title': 'Método Gráfico - Minimización',
            'method': 'grafico',
            'objective': 'minimizar z = 3x + 2y',
            'constraints': '3x + 4y <= 12\n3x + 2y >= 2\nx >= 0\ny >= 0',
            'description': 'Problema de minimización con restricciones mixtas (ideal para visualización).',
            'icon': 'chart-area',
            'color': 'success'
        },
        
        # Ejemplos para Método Simplex (múltiples variables)
        {
            'title': 'Método Simplex - Problema Multivariable',
            'method': 'simplex',
            'objective': 'maximizar z = 3x1 + 2x2 + x3',
            'constraints': 'x1 + x2 + x3 <= 10\n2x1 + x2 <= 8\nx1 + 2x3 <= 6\nx1 >= 0\nx2 >= 0\nx3 >= 0',
            'description': 'Problema con 3 variables ideal para el método Simplex.',
            'icon': 'table',
            'color': 'warning'
        },
        {
            'title': 'Método Simplex - Producción Óptima',
            'method': 'simplex',
            'objective': 'maximizar z = 5x1 + 4x2 + 3x3 + 2x4',
            'constraints': '2x1 + 3x2 + x3 + x4 <= 20\nx1 + 2x2 + 3x3 + x4 <= 15\n3x1 + x2 + 2x3 + 3x4 <= 25\nx1 >= 0\nx2 >= 0\nx3 >= 0\nx4 >= 0',
            'description': 'Problema de producción con 4 productos y recursos limitados.',
            'icon': 'table',
            'color': 'warning'
        },
        
        # Ejemplos para Método Dual Simplex
        {
            'title': 'Dual Simplex - Análisis de Sensibilidad',
            'method': 'dual',
            'objective': 'minimizar z = 2x1 + 3x2',
            'constraints': 'x1 + 2x2 >= 6\n2x1 + x2 >= 8\nx1 >= 0\nx2 >= 0',
            'description': 'Problema ideal para dual simplex con restricciones >= principalmente.',
            'icon': 'exchange-alt',
            'color': 'info'
        },
        {       'title': 'Dual Simplex - Optimización de Costos',
            'method': 'dual',
            'objective': 'minimizar z = 4x1 + 3x2 + 2x3',
            'constraints': 'x1 + x2 + x3 >= 5\n2x1 + x2 >= 4\nx1 + 2x3 >= 3\nx1 >= 0\nx2 >= 0\nx3 >= 0',
            'description': 'Problema de minimización de costos con múltiples restricciones >=.',
            'icon': 'exchange-alt',
            'color': 'info'
        },
        
        # Ejemplos para Método Simplex Dos Fases
        {
            'title': 'Dos Fases - Restricciones Mayor o Igual',
            'method': 'two-phase',
            'objective': 'maximizar z = 3x1 + 5x2',
            'constraints': '4x1 + x2 >= 4\n-x1 + 2x2 >= 2\nx2 <= 3\nx1 >= 0\nx2 >= 0',
            'description': 'Problema con restricciones >= que requiere variables artificiales.',
            'icon': 'layer-group',
            'color': 'two-phase'
        },
        {
            'title': 'Dos Fases - Restricciones Mixtas',
            'method': 'two-phase',
            'objective': 'minimizar z = 2x1 + 3x2 + x3',
            'constraints': 'x1 + 2x2 + x3 >= 10\nx1 + x2 = 5\n2x1 + x3 <= 8\nx1 >= 0\nx2 >= 0\nx3 >= 0',
            'description': 'Problema con mezcla de restricciones <=, >=, y =.',
            'icon': 'layer-group',
            'color': 'two-phase'
        },
        
        # Ejemplos para Modelo de Transporte
        {
            'title': 'Transporte - Problema Básico (3×3)',
            'method': 'transporte',
            'description': 'Distribución de productos desde 3 fábricas a 3 tiendas. Problema balanceado ideal para aprender.',
            'dimensions': '3 Orígenes × 3 Destinos',
            'total_supply': '300 unidades',
            'total_demand': '300 unidades',
            'icon': 'warehouse',
            'data': {
                'costs': [[8, 6, 10], [9, 12, 13], [14, 9, 16]],
                'supply': [150, 80, 70],
                'demand': [100, 120, 80]
            }
        },
        {
            'title': 'Transporte - Distribución Regional (4×4)',
            'method': 'transporte',
            'description': 'Envío de mercancía desde 4 centros de distribución a 4 ciudades. Problema balanceado.',
            'dimensions': '4 Orígenes × 4 Destinos',
            'total_supply': '215 unidades',
            'total_demand': '215 unidades',
            'icon': 'truck-moving',
            'data': {
                'costs': [[5, 2, 7, 3], [3, 6, 6, 1], [6, 1, 2, 4], [4, 3, 6, 6]],
                'supply': [80, 30, 60, 45],
                'demand': [70, 40, 70, 35]
            }
        },
        {
            'title': 'Transporte - Problema Pequeño (2×3)',
            'method': 'transporte',
            'description': 'Distribución simple desde 2 almacenes a 3 puntos de venta.',
            'dimensions': '2 Orígenes × 3 Destinos',
            'total_supply': '250 unidades',
            'total_demand': '250 unidades',
            'icon': 'boxes',
            'data': {
                'costs': [[4, 8, 8], [16, 24, 16]],
                'supply': [120, 130],
                'demand': [80, 90, 80]
            }
        },
        {
            'title': 'Transporte - Exceso de Oferta (Desbalanceado)',
            'method': 'transporte',
            'description': 'Problema con exceso de capacidad. La oferta supera la demanda en 50 unidades. Se balanceará automáticamente.',
            'dimensions': '3 Orígenes × 3 Destinos',
            'total_supply': '350 unidades',
            'total_demand': '300 unidades',
            'icon': 'warehouse',
            'data': {
                'costs': [[7, 8, 5], [6, 9, 11], [10, 7, 8]],
                'supply': [150, 120, 80],
                'demand': [100, 100, 100]
            }
        },
        {
            'title': 'Transporte - Exceso de Demanda (Desbalanceado)',
            'method': 'transporte',
            'description': 'Problema con demanda insatisfecha. La demanda supera la oferta en 40 unidades. Se balanceará automáticamente.',
            'dimensions': '2 Orígenes × 4 Destinos',
            'total_supply': '200 unidades',
            'total_demand': '240 unidades',
            'icon': 'truck-moving',
            'data': {
                'costs': [[5, 3, 6, 4], [7, 9, 8, 5]],
                'supply': [100, 100],
                'demand': [60, 70, 50, 60]
            }
        },
        
        # Ejemplos para Dijkstra
        {
            'title': 'Dijkstra - Red de Carreteras',
            'method': 'dijkstra',
            'description': 'Encuentra la ruta más corta entre ciudades con distancias en kilómetros.',
            'graph_type': 'No Dirigido',
            'nodes': '6 ciudades',
            'edges': '9 carreteras',
            'icon': 'road',
            'data': {
                'edges': '1 2 7\n1 3 9\n1 6 14\n2 3 10\n2 4 15\n3 4 11\n3 6 2\n4 5 6\n5 6 9',
                'start': 1,
                'end': 5,
                'directed': False
            }
        },
        {
            'title': 'Dijkstra - Red de Telecomunicaciones',
            'method': 'dijkstra',
            'description': 'Optimiza el enrutamiento de paquetes en una red con latencias (ms).',
            'graph_type': 'Dirigido',
            'nodes': '5 servidores',
            'edges': '8 conexiones',
            'icon': 'network-wired',
            'data': {
                'edges': '1 2 4\n1 3 2\n2 3 5\n2 4 10\n3 4 3\n3 5 8\n4 5 7\n5 2 1',
                'start': 1,
                'end': 5,
                'directed': True
            }
        },
        {
            'title': 'Dijkstra - Rutas de Distribución',
            'method': 'dijkstra',
            'description': 'Calcula el tiempo mínimo de entrega entre centro de distribución y clientes (minutos).',
            'graph_type': 'No Dirigido',
            'nodes': '7 ubicaciones',
            'edges': '11 rutas',
            'icon': 'shipping-fast',
            'data': {
                'edges': '1 2 5\n1 3 3\n2 4 8\n2 5 6\n3 4 4\n3 5 7\n4 5 2\n4 6 9\n5 6 5\n5 7 10\n6 7 4',
                'start': 1,
                'end': 7,
                'directed': False
            }
        },
        
        # Ejemplos para Kruskal
        {
            'title': 'Kruskal - Red Eléctrica',
            'method': 'kruskal',
            'description': 'Diseño óptimo de red eléctrica minimizando el costo de cableado (miles $).',
            'graph_type': 'No Dirigido',
            'nodes': '6 subestaciones',
            'edges': '10 conexiones posibles',
            'icon': 'bolt',
            'data': {
                'edges': '1 2 4\n1 3 2\n2 3 5\n2 4 10\n3 4 3\n3 5 8\n4 5 7\n4 6 6\n5 6 9\n2 5 12'
            }
        },
        {
            'title': 'Kruskal - Fibra Óptica',
            'method': 'kruskal',
            'description': 'Instalación de fibra óptica con el menor costo de tendido entre edificios (km).',
            'graph_type': 'No Dirigido',
            'nodes': '5 edificios',
            'edges': '8 rutas posibles',
            'icon': 'ethernet',
            'data': {
                'edges': '1 2 7\n1 3 9\n2 3 10\n2 4 15\n3 4 11\n3 5 2\n4 5 6\n1 5 14'
            }
        },
        {
            'title': 'Kruskal - Red de Tuberías',
            'method': 'kruskal',
            'description': 'Sistema de tuberías de agua optimizando el costo de instalación (metros).',
            'graph_type': 'No Dirigido',
            'nodes': '7 tanques',
            'edges': '12 conexiones posibles',
            'icon': 'water',
            'data': {
                'edges': '1 2 5\n1 3 3\n2 3 4\n2 4 8\n3 4 6\n3 5 7\n4 5 2\n4 6 9\n5 6 5\n5 7 10\n6 7 4\n1 7 15'
            }
        }
    ]
    
    return render_template('examples.html', examples=examples_data)


@app.route('/transportation', methods=['GET', 'POST'])
def transportation_method():
    """Ruta para el modelo de transporte"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario como texto
            costs_text = request.form.get('costs_text', '').strip()
            supply_text = request.form.get('supply_text', '').strip()
            demand_text = request.form.get('demand_text', '').strip()
            method = request.form.get('method', 'northwest')
            
            # Validar que se ingresaron datos
            if not costs_text or not supply_text or not demand_text:
                flash('Error: Datos incompletos. Por favor complete todos los campos.', 'error')
                return redirect(url_for('transportation_method'))
            
            # Parsear matriz de costos
            costs = []
            for line in costs_text.split('\n'):
                line = line.strip()
                if not line:
                    continue
                try:
                    row = [float(x) for x in line.split()]
                    if row:
                        costs.append(row)
                except ValueError:
                    flash('Error: La matriz de costos contiene valores no numéricos.', 'error')
                    return redirect(url_for('transportation_method'))
            
            # Parsear ofertas
            try:
                supply = [float(x) for x in supply_text.split()]
            except ValueError:
                flash('Error: Las ofertas contienen valores no numéricos.', 'error')
                return redirect(url_for('transportation_method'))
            
            # Parsear demandas
            try:
                demand = [float(x) for x in demand_text.split()]
            except ValueError:
                flash('Error: Las demandas contienen valores no numéricos.', 'error')
                return redirect(url_for('transportation_method'))
            
            # Validar dimensiones
            if not costs:
                flash('Error: La matriz de costos está vacía.', 'error')
                return redirect(url_for('transportation_method'))
            
            if len(costs) != len(supply):
                flash(f'Error: La matriz tiene {len(costs)} filas pero se proporcionaron {len(supply)} ofertas.', 'error')
                return redirect(url_for('transportation_method'))
            
            if len(costs[0]) != len(demand):
                flash(f'Error: La matriz tiene {len(costs[0])} columnas pero se proporcionaron {len(demand)} demandas.', 'error')
                return redirect(url_for('transportation_method'))
            
            # Resolver problema
            result = transportation_model.solve_transportation_problem(
                costs=costs,
                supply=supply,
                demand=demand,
                method=method
            )
            
            return render_template('transportation_results.html', result=result)
            
        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'error')
            return redirect(url_for('transportation_method'))
    
    # GET request - mostrar formulario
    return render_template('transportation.html')


@app.route('/dijkstra', methods=['GET', 'POST'])
def dijkstra_method():
    """Método de Dijkstra - Camino más corto"""
    if request.method == 'POST':
        try:
            input_format = request.form.get('input_format', 'edges')
            start_node = int(request.form.get('start_node'))
            end_node_str = request.form.get('end_node', '').strip()
            end_node = int(end_node_str) if end_node_str else None
            directed = request.form.get('directed') == 'true'
            
            edges = []
            
            if input_format == 'edges':
                # Parsear lista de aristas
                edges_text = request.form.get('edges_text', '').strip()
                if not edges_text:
                    flash('Por favor ingresa las aristas del grafo.', 'danger')
                    return redirect(url_for('dijkstra_method'))
                
                for line in edges_text.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split()
                        if len(parts) >= 3:
                            u, v, w = int(parts[0]), int(parts[1]), float(parts[2])
                            edges.append((u, v, w))
            
            elif input_format == 'matrix':
                # Parsear matriz de adyacencia
                matrix_text = request.form.get('matrix_text', '').strip()
                if not matrix_text:
                    flash('Por favor ingresa la matriz de adyacencia.', 'danger')
                    return redirect(url_for('dijkstra_method'))
                
                matrix = []
                for line in matrix_text.split('\n'):
                    line = line.strip()
                    if line:
                        row = [float(x) for x in line.split()]
                        matrix.append(row)
                
                # Convertir matriz a lista de aristas
                n = len(matrix)
                for i in range(n):
                    for j in range(n):
                        if matrix[i][j] > 0:
                            # Nodos numerados desde 1
                            edges.append((i + 1, j + 1, matrix[i][j]))
            
            if not edges:
                flash('No se encontraron aristas válidas en la entrada.', 'danger')
                return redirect(url_for('dijkstra_method'))
            
            # Ejecutar Dijkstra
            result = dijkstra_algorithm.solve_dijkstra(edges, start_node, end_node, directed)
            
            return render_template('dijkstra_results.html', result=result)
            
        except ValueError as e:
            flash(f'Error en el formato de entrada: {str(e)}', 'danger')
            return redirect(url_for('dijkstra_method'))
        except Exception as e:
            flash(f'Error al procesar el grafo: {str(e)}', 'danger')
            return redirect(url_for('dijkstra_method'))
    
    return render_template('dijkstra.html')


@app.route('/kruskal', methods=['GET', 'POST'])
def kruskal_method():
    """Método de Kruskal - Árbol de Expansión Mínima"""
    if request.method == 'POST':
        try:
            input_format = request.form.get('input_format', 'edges')
            edges = []
            
            if input_format == 'edges':
                # Parsear lista de aristas
                edges_text = request.form.get('edges_text', '').strip()
                if not edges_text:
                    flash('Por favor ingresa las aristas del grafo.', 'danger')
                    return redirect(url_for('kruskal_method'))
                
                for line in edges_text.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split()
                        if len(parts) >= 3:
                            u, v, w = int(parts[0]), int(parts[1]), float(parts[2])
                            edges.append((u, v, w))
            
            elif input_format == 'matrix':
                # Parsear matriz de adyacencia
                matrix_text = request.form.get('matrix_text', '').strip()
                if not matrix_text:
                    flash('Por favor ingresa la matriz de adyacencia.', 'danger')
                    return redirect(url_for('kruskal_method'))
                
                matrix = []
                for line in matrix_text.split('\n'):
                    line = line.strip()
                    if line:
                        row = [float(x) for x in line.split()]
                        matrix.append(row)
                
                # Convertir matriz a lista de aristas (evitar duplicados en grafo no dirigido)
                n = len(matrix)
                seen = set()
                for i in range(n):
                    for j in range(i + 1, n):  # Solo mitad superior para evitar duplicados
                        if matrix[i][j] > 0:
                            edges.append((i + 1, j + 1, matrix[i][j]))
            
            if not edges:
                flash('No se encontraron aristas válidas en la entrada.', 'danger')
                return redirect(url_for('kruskal_method'))
            
            # Ejecutar Kruskal
            result = kruskal_algorithm.solve_kruskal(edges)
            
            return render_template('kruskal_results.html', result=result)
            
        except ValueError as e:
            flash(f'Error en el formato de entrada: {str(e)}', 'danger')
            return redirect(url_for('kruskal_method'))
        except Exception as e:
            flash(f'Error al procesar el grafo: {str(e)}', 'danger')
            return redirect(url_for('kruskal_method'))
    
    return render_template('kruskal.html')


# Manejo de errores
@app.errorhandler(404)
def page_not_found(e):
    """Página de error 404."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Página de error 500."""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Configuración para desarrollo y producción
    import os
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print("🚀 Iniciando aplicación de Programación Lineal...")
    print("📊 Métodos: Gráfico, Simplex, Dual Simplex, Dos Fases y Transporte")
    print("🎓 Investigación de Operaciones - Segundo Parcial")
    print("👨‍💻 Desarrollado por José Miguel Herrera Gutiérrez para UTP")
    print("👩‍🏫 Profesora: Bibiana Patricia Arias Villada")
    print(f"🌐 Abre tu navegador en: http://localhost:{port}")
    print("-" * 50)
    
    app.run(debug=debug, host='0.0.0.0', port=port)