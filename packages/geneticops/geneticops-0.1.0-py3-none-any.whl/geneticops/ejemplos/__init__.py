"""
Ejemplos de uso de la librería geneticops
======================================

Este paquete contiene varios ejemplos de aplicación de algoritmos genéticos
utilizando la librería geneticops.

Ejemplos disponibles:
- maximizar_funcion.py: Encuentra el máximo de una función de dos variables.
- problema_mochila.py: Resuelve el problema de la mochila (Knapsack Problem).
- viajero_comercio.py: Resuelve el problema del viajante de comercio (TSP).

Para ejecutar un ejemplo, simplemente ejecute el archivo correspondiente:

```
python -m ejemplos.maximizar_funcion
python -m ejemplos.problema_mochila
python -m ejemplos.viajero_comercio
```
"""

# Información sobre los ejemplos disponibles
ejemplos = {
    "maximizar_funcion": "Ejemplo de maximización de una función de dos variables",
    "problema_mochila": "Ejemplo de resolución del problema de la mochila",
    "viajero_comercio": "Ejemplo de resolución del problema del viajante de comercio (TSP)"
}

def listar_ejemplos():
    """
    Muestra una lista de todos los ejemplos disponibles y su descripción.
    """
    print("Ejemplos disponibles en geneticops:")
    print("-" * 40)
    for nombre, descripcion in ejemplos.items():
        print(f"{nombre:20} - {descripcion}")
    print("\nPara ejecutar un ejemplo: python -m ejemplos.<nombre_ejemplo>")

def obtener_info_ejemplo(nombre):
    """
    Devuelve la descripción de un ejemplo específico.
    
    Parameters
    ----------
    nombre : str
        Nombre del ejemplo.
        
    Returns
    -------
    str
        Descripción del ejemplo o un mensaje de error si no existe.
    """
    if nombre in ejemplos:
        return ejemplos[nombre]
    else:
        return f"No se encontró el ejemplo '{nombre}'. Use listar_ejemplos() para ver los disponibles."

# Permitir importar los ejemplos directamente
__all__ = ["listar_ejemplos", "obtener_info_ejemplo"]