# 📊 Solucionador de Programación Lineal - Aplicación Web Educativa

<div align="center">

**Investigación de Operaciones - Segundo Parcial**  
**Universidad Tecnológica de Pereira (UTP)**

![Python](https://img.shields.io/badge/Python-3.13.7-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green?logo=flask&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-2.3.3-orange?logo=numpy&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Desarrollado por:** José Miguel Herrera Gutiérrez  
**Profesora:** Bibiana Patricia Arias Villada  
**Versión:** 6.0 (Final)  
**Fecha:** Noviembre 2025

</div>

---

## 📋 Descripción

Aplicación web educativa completa para resolver problemas de **Programación Lineal** con **7 métodos diferentes**, incluyendo algoritmos de redes con visualización interactiva. Cada método incluye visualización paso a paso de iteraciones y tableaux completos. Proyecto final del segundo parcial de Investigación de Operaciones.

## ✨ Características Principales

### 🔢 Métodos Implementados

| Método | Variables | Restricciones | Características |
|--------|-----------|---------------|---------------|
| 🟢 **Método Gráfico** | 2 | ≤, ≥ | Visualización con Matplotlib, región factible |
| 🟡 **Simplex Estándar** | 2+ | ≤ | Tableau manual, variables de holgura |
| 🟣 **Dual Simplex** | 2+ | ≥ | Ratios duales, minimización/maximización |
| 🟠 **Simplex Dos Fases** | 2+ | ≤, ≥, = | Variables artificiales, Fase I y II |
| 🔴 **Modelo de Transporte** | n×m | Balance | Esquina Noroeste, Costo Mínimo, Vogel (VAM) |
| 🔵 **Dijkstra** | Grafos | Pesos ≥ 0 | Camino más corto, visualización Vis.js |
| 🟢 **Kruskal** | Grafos | No dirigido | Árbol de expansión mínima (MST), Union-Find |

### 🎨 Interfaz Moderna

- ✅ **Diseño responsivo** con Bootstrap 5 y CSS personalizado
- ✅ **Colores distintivos** por método (Verde, Amarillo, Morado, Naranja, Rojo, Teal, Emerald)
- ✅ **Animaciones suaves** y transiciones fluidas
- ✅ **Iconos Font Awesome** para mejor UX
- ✅ **Visualización interactiva de grafos** con Vis.js 9.1.9
- ✅ **Modo oscuro** disponible en toda la aplicación

### 📊 Visualización Educativa

- ✅ **Tableaux completos** con todas las variables
- ✅ **Pivotes resaltados** en color amarillo
- ✅ **Variables básicas** identificadas en cada iteración
- ✅ **Valores de Z/W** actualizados paso a paso
- ✅ **Acordeones expandibles** para navegación fácil
- ✅ **Grafos interactivos** con nodos arrastrables y caminos resaltados

### 🎯 Funcionalidades

- ✅ **Siete métodos de solución** con algoritmos optimizados
- ✅ **Visualización paso a paso** de iteraciones
- ✅ **Tablas interactivas** con resaltado de pivotes
- ✅ **Soporte para restricciones** `<=`, `>=`, `=`
- ✅ **Detección automática** de infactibilidad y no acotamiento
- ✅ **Ejemplos precargados** para cada método
- ✅ **Interfaz responsiva** compatible con móviles y tablets

### 🛠️ Implementación Manual

- **Sin librerías externas** de optimización (no PuLP, no SciPy)
- **NumPy puro** para operaciones matriciales
- **Algoritmos escritos desde cero** para fines educativos
- **Código bien documentado** y legible
- **Tolerancia numérica** (EPS = 1e-9)

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.13.7**
- **Flask 3.1.2** - Framework web
- **NumPy 2.3.3** - Operaciones matriciales
- **Matplotlib 3.10.1** - Gráficos del método gráfico

### Frontend
- **HTML5** con plantillas Jinja2
- **CSS3** con variables personalizadas
- **JavaScript ES6+**
- **Bootstrap 5.3** - Framework CSS
- **Font Awesome 6.6** - Iconos
- **Vis.js 9.1.9** - Visualización interactiva de grafos

---

## 📁 Estructura del Proyecto

```
Investigacion-de-operaciones/
├── app.py                          # 🌐 Aplicación Flask con 5 métodos
├── lp_solver.py                    # 📈 Método Gráfico (2 variables)
├── simplex_tableau.py              # 🔢 Método Simplex (NumPy)
├── dual_simplex_tableau.py         # 🔄 Método Dual Simplex (NumPy)
├── two_phase_simplex.py            # 🔶 Método Simplex Dos Fases
├── transportation_model.py         # 🟣 Modelo de Transporte (3 métodos)
├── dijkstra_algorithm.py           # 🔵 Algoritmo Dijkstra (camino más corto)
├── kruskal_algorithm.py            # 🟢 Algoritmo Kruskal (MST)
├── requirements.txt                # 📦 Dependencias
├── README.md                       # 📖 Este archivo
│
├── static/
│   ├── css/
│   │   └── styles.css              # 🎨 ~1200 líneas de CSS personalizado
│   ├── images/                     # 🖼️ Imágenes generadas (gráficos)
│   └── js/
│       └── app.js                  # ⚡ JavaScript del cliente
│
└── templates/
    ├── base.html                   # 📄 Layout base con navbar
    ├── index.html                  # 🏠 Homepage con 5 métodos
    ├── about.html                  # 📚 Teoría de todos los métodos
    ├── examples.html               # 💡 Ejemplos de problemas
    ├── 404.html                    # ❌ Página de error
    │
    ├── simplex.html                # 📝 Formulario Simplex
    ├── simplex_results.html        # 📊 Resultados Simplex
    ├── dual_simplex.html           # 📝 Formulario Dual Simplex
    ├── dual_simplex_results.html   # 📊 Resultados Dual Simplex
    ├── two_phase_simplex.html      # 📝 Formulario Dos Fases
    ├── two_phase_simplex_results.html  # 📊 Resultados Dos Fases
    ├── transportation.html         # 📝 Formulario Transporte
    ├── transportation_results.html # 📊 Resultados Transporte
    ├── transportation_method_details.html  # 📋 Detalles de método
    ├── dijkstra.html               # 📝 Formulario Dijkstra
    ├── dijkstra_results.html       # 📊 Resultados Dijkstra (Vis.js)
    ├── kruskal.html                # 📝 Formulario Kruskal
    └── kruskal_results.html        # 📊 Resultados Kruskal (Vis.js)
```

---

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Git

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/Eljosek/Investigacion-de-operaciones.git
cd Investigacion-de-operaciones
```

### Paso 2: Crear entorno virtual

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

---

## 📚 Uso de la Aplicación

### Método Gráfico

**Ideal para:** Problemas con 2 variables

**Ejemplo:**
```
Función Objetivo: maximizar z = 3x + 5y
Restricciones:
  x + y <= 4
  2x + y <= 6
  x >= 0
  y >= 0
```

### Método Simplex

**Ideal para:** Problemas con múltiples variables y restricciones <=

**Ejemplo:**
```
Función Objetivo: maximizar z = 3x1 + 2x2 + x3
Restricciones:
  x1 + x2 + x3 <= 10
  2x1 + x2 <= 8
  x1 + 2x3 <= 6
  x1 >= 0
  x2 >= 0
  x3 >= 0
```

**Características:**
- Tableau inicial con variables de holgura
- Iteraciones paso a paso mostradas
- Columna pivote (variable entrante) marcada en verde
- Fila pivote (variable saliente) marcada en naranja
- Ratios θ = b/a calculados
- Solución óptima con variables básicas

### Método Dual-Simplex

**Ideal para:** Problemas de minimización con restricciones >=

**Ejemplo:**
```
Función Objetivo: minimizar z = 3x1 + 2x2
Restricciones:
  3x1 + x2 >= 3
  4x1 + 3x2 >= 6
  x1 + x2 <= 3
  x1 >= 0
  x2 >= 0
```

### Método Simplex Dos Fases

**Ideal para:** Problemas con restricciones >=, = o mixtas

**Ejemplo:**
```
Función Objetivo: maximizar z = 3x1 + 5x2
Restricciones:
  4x1 + x2 >= 4
  -x1 + 2x2 >= 2
  x2 <= 3
  x1, x2 >= 0
```

**Características:**
- Fase I: Minimización de W (suma de artificiales)
- Fase II: Optimización de Z (función original)
- Tableaux completos de ambas fases

### Modelo de Transporte

**Ideal para:** Problemas de distribución m×n (orígenes × destinos)

**Ejemplo:**
```
4 Orígenes (plantas): 80, 30, 60, 45 unidades
4 Destinos (ciudades): 70, 40, 70, 35 unidades

Matriz de costos 4×4:
  [8, 6, 10, 9]
  [9, 12, 13, 7]
  [14, 9, 16, 5]
  [10, 8, 11, 12]
```

**Tres Métodos Disponibles:**
1. **Esquina Noroeste** - Empieza en (1,1), asigna máximo posible, avanza derecha/abajo
2. **Costo Mínimo** - Selecciona celda de menor costo, asigna máximo, elimina fila/columna
3. **Vogel (VAM)** - Calcula penalidades, selecciona máxima, asigna en mínimo de esa fila/col

**Modo Comparación:**
- Ejecuta los 3 métodos simultáneamente
- Tabla comparativa de variables de decisión
- Destaca el método con menor costo total
- Muestra iteraciones detalladas de cada método

---

## 🎓 Algoritmos Implementados

### 1. Método Gráfico
1. Graficar todas las restricciones
2. Identificar la región factible
3. Encontrar vértices (puntos de intersección)
4. Evaluar función objetivo en cada vértice
5. Seleccionar el vértice con mejor valor

### 2. Método Simplex
1. **Construcción del tableau inicial** con variables de holgura
2. **Criterio de optimalidad**: zⱼ - cⱼ ≤ 0 para maximización
3. **Selección de variable entrante**: zⱼ - cⱼ más positivo
4. **Selección de variable saliente**: mínimo ratio θ = bᵢ/aᵢⱼ
5. **Operaciones de pivote** (Gauss-Jordan)
6. **Iteración** hasta optimalidad o unboundedness

### 3. Método Dual Simplex
1. **Verificación de factibilidad dual**: zⱼ - cⱼ ≤ 0
2. **Selección de fila pivote**: RHS más negativo
3. **Selección de columna pivote**: mínimo ratio zⱼ/aᵢⱼ (negativo)
4. **Operaciones de pivote** para restaurar factibilidad primal
5. **Iteración** hasta factibilidad y optimalidad

### 4. Método Simplex Dos Fases
1. **Fase I**: Construir problema auxiliar con variables artificiales
2. Minimizar W = suma de artificiales
3. Si W > 0, problema infactible
4. **Fase II**: Eliminar artificiales, optimizar función original Z
5. Aplicar Simplex estándar hasta optimalidad

### 5. Modelo de Transporte

#### Método Esquina Noroeste
1. Iniciar en celda (1,1)
2. Asignar min(oferta[i], demanda[j])
3. Si oferta[i] se agota, bajar una fila
4. Si demanda[j] se satisface, avanzar una columna
5. Repetir hasta llenar todas las celdas necesarias

#### Método Costo Mínimo
1. Seleccionar celda con menor costo no asignada
2. Asignar min(oferta[i], demanda[j])
3. Marcar fila o columna como agotada
4. Repetir con siguiente mínimo costo disponible
5. Continuar hasta satisfacer toda oferta/demanda

#### Método Vogel (VAM)
1. Calcular penalidad de cada fila: diferencia entre 2 menores costos
2. Calcular penalidad de cada columna: diferencia entre 2 menores costos
3. Seleccionar fila/columna con mayor penalidad
4. En esa fila/columna, asignar en celda de menor costo
5. Actualizar oferta/demanda y recalcular penalidades
6. Repetir hasta completar asignación

**Complejidad Algorítmica:**
| Método | Complejidad | Calidad |
|--------|-------------|---------|
| Esquina Noroeste | O(m+n) | Básica |
| Costo Mínimo | O(mn log(mn)) | Buena |
| Vogel (VAM) | O(mn²) | Muy buena |

---

## 💡 Ejemplos de Problemas

### Ejemplo 1: Maximización Simple (Gráfico)
```
Maximizar Z = 40x₁ + 30x₂
Restricciones:
  2x₁ + 1x₂ ≤ 8   (Recurso A)
  1x₁ + 2x₂ ≤ 10  (Recurso B)
  x₁, x₂ ≥ 0
```
**Solución:** x₁=2, x₂=4, Z=200

### Ejemplo 2: Problema Multivariable (Simplex)
```
Maximizar Z = 5x₁ + 4x₂ + 3x₃
Restricciones:
  2x₁ + 3x₂ + 1x₃ ≤ 5
  4x₁ + 1x₂ + 2x₃ ≤ 11
  3x₁ + 4x₂ + 2x₃ ≤ 8
  x₁, x₂, x₃ ≥ 0
```
**Solución:** x₁=2, x₂=0, x₃=1, Z=13

### Ejemplo 3: Minimización con ≥ (Dual Simplex)
```
Minimizar Z = 8x₁ + 12x₂
Restricciones:
  1x₁ + 2x₂ ≥ 10  (Demanda mínima)
  2x₁ + 1x₂ ≥ 12  (Producción mínima)
  x₁, x₂ ≥ 0
```
**Solución:** x₁=4.67, x₂=2.67, Z=69.33

### Ejemplo 4: Distribución de Energía (Transporte)
```
4 Plantas con capacidad: 80, 30, 60, 45 KW
4 Ciudades con demanda: 70, 40, 70, 35 KW

Costos de transporte ($/KW):
        C1   C2   C3   C4
P1      8    6    10   9
P2      9    12   13   7
P3      14   9    16   5
P4      10   8    11   12
```
**Solución (Vogel):** Costo total = 1,785 $

---

## 🧪 Ejemplos Precargados

La aplicación incluye **12 ejemplos** distribuidos así:

- **Método Gráfico:** 2 ejemplos
- **Método Simplex:** 2 ejemplos
- **Método Dual Simplex:** 2 ejemplos
- **Método Dos Fases:** 2 ejemplos
- **Modelo de Transporte:** 2 ejemplos

Accede a ellos desde la página **"Ejemplos"** en el menú de navegación.

---

## 🐛 Solución de Problemas

### El servidor no inicia
```bash
# Verificar puerto ocupado
netstat -ano | findstr :5000

# Matar proceso si es necesario (Windows)
taskkill /F /PID <número_de_pid>

# O cambiar puerto en app.py
app.run(debug=True, port=5001)
```

### Error de importación de módulos
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Errores con NumPy
```bash
# Actualizar NumPy
pip install --upgrade numpy
```

### Gráfica no se muestra (Método Gráfico)
**Causa:** Problema con matplotlib backend  
**Solución:** Asegúrate de tener matplotlib instalado correctamente

### Servidor no arranca en puerto 5000
**Solución:** Cambia el puerto en `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

---

## 🔧 Mejoras Técnicas Implementadas

### Corrección de Valores Numéricos
**Problema:** Aparecían valores como `4.441e-16` (notación científica para números muy pequeños)

**Solución implementada:**
```python
def _clean_small_values(self, value: float, tolerance: float = 1e-10) -> float:
    """Redondea valores muy pequeños a 0"""
    if abs(value) < tolerance:
        return 0.0
    return value
```

Todos los valores menores a `1e-10` (0.0000000001) se redondean a 0, eliminando la notación científica innecesaria.

### Manejo de Tipos de Datos
- Uso correcto de `float()` para elementos individuales de arrays NumPy
- Uso de `np.all()` y `np.any()` para comparaciones de arrays completos
- Evita el error: "The truth value of an array with more than one element is ambiguous"

### Variables de Template
- Backend envía `solution` (no `variables`)
- Backend envía `objective_value` (no `z_value`)
- Campo `opt_type` agregado para distinguir MAX/MIN
- Estructura consistente entre todos los métodos

---

## 🎓 Contexto Académico

Este proyecto fue desarrollado para el curso de **Investigación de Operaciones** en la Universidad Tecnológica de Pereira (UTP).

### Objetivos del Proyecto
1. ✅ Implementar algoritmos de PL **sin librerías externas de optimización**
2. ✅ Visualizar **paso a paso** el funcionamiento de cada método
3. ✅ Crear interfaz **educativa y moderna** para estudiantes
4. ✅ Comparar **cinco enfoques diferentes** de resolución
5. ✅ Documentar **exhaustivamente** el desarrollo

### Profesora
**Bibiana Patricia Arias Villada**  
Facultad de Ingeniería Industrial  
Universidad Tecnológica de Pereira

### Estudiante
**José Miguel Herrera Gutiérrez**  
Ingeniería de Sistemas y Computación  
Fecha de Entrega: Noviembre 2025

---

## 📝 Licencia

Este proyecto es de uso educativo para la Universidad Tecnológica de Pereira (UTP).

**Autor:** José Miguel Herrera Gutiérrez  
**Materia:** Investigación de Operaciones  
**Profesora:** Bibiana Patricia Arias Villada  
**Año:** 2025

---

## 🙏 Agradecimientos

- **Universidad Tecnológica de Pereira** por la formación académica
- **Profesora Bibiana Patricia Arias Villada** por la guía en Investigación de Operaciones
- **Bootstrap Team** por el framework CSS
- **Flask Community** por el excelente framework web
- **NumPy Developers** por las herramientas matemáticas

---

## 📧 Contacto

**José Miguel Herrera Gutiérrez**  
Universidad Tecnológica de Pereira  
Ingeniería de Sistemas y Computación

- Instagram: @eljosek
- Teléfono: +57 3122843719
- Repositorio: [github.com/Eljosek/Investigacion-de-operaciones](https://github.com/Eljosek/Investigacion-de-operaciones)

---

<div align="center">

**Hecho con ❤️ para Investigación de Operaciones - UTP 2025**

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub

</div>

---

## 📚 Referencias

- Winston, W. L. (2004). *Operations Research: Applications and Algorithms*. Thomson Brooks/Cole.
- Hillier, F. S., & Lieberman, G. J. (2015). *Introduction to Operations Research*. McGraw-Hill Education.
- Taha, H. A. (2017). *Operations Research: An Introduction*. Pearson Education.
- Documentación de NumPy: https://numpy.org/doc/
- Documentación de Flask: https://flask.palletsprojects.com/

---

## 🔄 Historial de Versiones

### Versión 4.0 (Noviembre 2025) - ACTUAL
- ✅ **Modelo de Transporte** con 3 métodos (Esquina Noroeste, Costo Mínimo, Vogel)
- ✅ Modo comparación para ejecutar los 3 métodos simultáneamente
- ✅ Interfaz simplificada con entrada de texto para matriz, ofertas y demandas
- ✅ Visualización detallada de iteraciones por método
- ✅ Color rojo (#dc2626) para identificación visual del Modelo de Transporte
- ✅ Color morado (#9333ea) para Dual Simplex consistente en toda la aplicación
- ✅ 3 ejemplos de transporte agregados (2×3, 3×3, 4×4)
- ✅ Corrección completa de UX y colores
- ✅ Menú de navegación actualizado con todos los métodos
- ✅ README completo y actualizado

### Versión 3.0 (Octubre 2025)
- ✅ Corrección de notación científica (e-16 → 0)
- ✅ Limpieza de documentación (Markdown unificado)
- ✅ README completo y profesional
- ✅ Estructura de proyecto limpia

### Versión 2.0 (Octubre 2025)
- ✅ Dual-Simplex optimizado para MAX/MIN
- ✅ Corrección de errores de arrays NumPy
- ✅ Templates Jinja2 corregidos

### Versión 1.0 (Octubre 2025)
- ✅ Implementación inicial de cuatro métodos
- ✅ Interfaz web con Flask
- ✅ Visualización básica de resultados

---

**¡Listo para usar!** 🚀

Para iniciar: `python app.py` y navega a `http://localhost:5000`
