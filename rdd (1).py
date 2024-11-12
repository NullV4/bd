# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wpKW55crLutDeQ2i26crNopmAgJjyg3Q
"""

from pyspark import SparkContext

sc = SparkContext("local", "FinanceAnalysis")

ventas_data = [
    ("Producto_A", 10000, "2024-01"), ("Producto_B", 15000, "2024-01"), ("Servicio_X", 7000, "2024-01"),
    ("Producto_A", 12000, "2024-02"), ("Producto_B", 16000, "2024-02"), ("Servicio_X", 8000, "2024-02"),
    ("Producto_A", 14000, "2024-03"), ("Producto_B", 17000, "2024-03"), ("Servicio_X", 9000, "2024-03"),
    ("Producto_C", 20000, "2024-01"), ("Producto_C", 21000, "2024-02"), ("Producto_C", 22000, "2024-03"),
]

ventas_rdd = sc.parallelize(ventas_data)

costos_data = [
    ("Producto_A", 4000), ("Producto_B", 6000), ("Servicio_X", 3000), ("Producto_C", 10000),
    ("Producto_A", 4500), ("Producto_B", 6500), ("Servicio_X", 3500), ("Producto_C", 10500),
    ("Producto_A", 5000), ("Producto_B", 7000), ("Servicio_X", 4000), ("Producto_C", 11000),
]
costos_rdd = sc.parallelize(costos_data)

gastos_data = [
    ("Infraestructura", 2000), ("Tecnología", 3000), ("Marketing", 1500), ("Otros", 1000),
    ("Infraestructura", 2100), ("Tecnología", 3200), ("Marketing", 1600), ("Otros", 1100),
    ("Infraestructura", 2200), ("Tecnología", 3300), ("Marketing", 1700), ("Otros", 1200),
]
gastos_rdd = sc.parallelize(gastos_data)

flujo_data = [
    ("Ingresos", 25000), ("Egresos", 18000), ("Ingresos", 27000), ("Egresos", 19000),
    ("Ingresos", 28000), ("Egresos", 20000), ("Ingresos", 30000), ("Egresos", 21000),
]
flujo_rdd = sc.parallelize(flujo_data)

inversion_data = [
    ("Proyecto_NuevaTecnologia", 10000), ("Proyecto_DesarrolloProducto", 15000),
    ("Proyecto_MejoraPlataforma", 8000), ("Proyecto_InvestigacionIA", 12000),
    ("Proyecto_MejoraUIUX", 6000), ("Proyecto_ExpansionInfraestructura", 14000),
]

inversion_rdd = sc.parallelize(inversion_data)

ventas_totales = ventas_rdd.map(lambda x: (x[0], x[1])).reduceByKey(lambda x, y: x + y)
print("Ventas Totales por Producto/Servicio:", ventas_totales.collect())

margen_rdd = ventas_rdd.map(lambda x: (x[0], x[1])).join(costos_rdd).mapValues(lambda x: x[0] - x[1])
margen_total_por_producto = margen_rdd.reduceByKey(lambda x, y: x + y)
print("Margen Total de Ganancia por Producto/Servicio:", margen_total_por_producto.collect())

flujo_total = flujo_rdd.reduceByKey(lambda x, y: x + y)
print("Flujo de Caja:", flujo_total.collect())

inversion_total = inversion_rdd.map(lambda x: x[1]).sum()
print("Inversión Total en Innovación:", inversion_total)

gastos_totales = gastos_rdd.map(lambda x: x[1]).sum()
print("Gastos Generales y Administrativos Totales:", gastos_totales)

ventas_total_mensual = ventas_rdd.map(lambda x: x[1]).sum()
ratio_inversion = inversion_total / ventas_total_mensual
print("Ratio de Inversión en Innovación:", ratio_inversion)

margen_promedio_por_producto = margen_total_por_producto.mapValues(lambda x: x / 3)  # Asumiendo 3 meses
print("Margen Bruto Promedio por Producto:", margen_promedio_por_producto.collect())

flujo_mensual = flujo_rdd.map(lambda x: ("Ingresos" if x[0] == "Ingresos" else "Egresos", x[1])).reduceByKey(lambda x, y: x + y)
print("Total de Ingresos y Egresos:", flujo_mensual.collect())

costos_promedio = costos_rdd.mapValues(lambda x: x / 3).reduceByKey(lambda x, y: x + y)  # Asumiendo 3 meses
print("Costos Promedio por Producto:", costos_promedio.collect())

ingresos_netos = flujo_total.filter(lambda x: x[0] == "Ingresos").map(lambda x: x[1]).sum() - flujo_total.filter(lambda x: x[0] == "Egresos").map(lambda x: x[1]).sum()
print("Ingresos Netos Totales:", ingresos_netos)

producto_max_margen = margen_total_por_producto.takeOrdered(1, key=lambda x: -x[1])
print("Producto/Servicio con Mayor Margen de Ganancia:", producto_max_margen)

inversion_ordenada = inversion_rdd.sortBy(lambda x: x[1], ascending=False)
print("Inversiones Ordenadas por Proyecto:", inversion_ordenada.collect())

total_gastos = gastos_rdd.map(lambda x: x[1]).sum()
porcentaje_gastos = gastos_rdd.map(lambda x: (x[0], (x[1] / total_gastos) * 100))
print("Porcentaje de Gastos por Categoría:", porcentaje_gastos.collect())