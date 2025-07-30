# pylinreglib

Esta es una biblioteca para realizar regresiones lineales compatible con Python. Permite realizar análisis estadísticos avanzados utilizando modelos de regresión múltiple.

## Instalación

Para instalar esta biblioteca, puedes usar `pip`:

```bash
pip install pylinreglib
```
## Requisitos
- Python >= 3.6

- NumPy

- Pandas

- scipy

- matplotlib

- seaborn

## Uso
### Regresión Lineal Múltiple
Puedes usar la biblioteca para realizar regresiones lineales múltiples con variables tanto numéricas como categóricas. Aquí tienes un ejemplo básico de cómo hacerlo:
```python

import pandas as pd
from pylinreglib import mlrm

# Cargar datos
data = pd.read_csv('tus_datos.csv')

# Crear el modelo
model = mlrm(data, response_col="Horas_estudio", cat_col="Genero", predictor_cols=["Edad"])

# Ver los coeficientes del modelo
print(model.coefficients)
```

## Funcionalidades
Regresión Lineal Múltiple (MLRM): Permite realizar regresiones con variables continuas y categóricas, con soporte para interacción entre variables.

## Licencia
Este proyecto está bajo la licencia MIT - mira el archivo LICENSE para más detalles.

### Autor
Samuel Ortiz Toro, estudiante de ingenieria de sistemas e informática de la Universidad Nacional de Colombia sede Medellín
