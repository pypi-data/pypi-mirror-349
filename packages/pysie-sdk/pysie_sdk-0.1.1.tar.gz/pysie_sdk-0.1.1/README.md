# PYSIE SDK
SDK for get the principal Mexican financial indicators from SIE


## Setup
- Create venv
` python -m venv venv`
- Activate venv
- Install dependencies:
`pip install -r requirements.txt`


## Usage

```
from pysie_sdk.client import SIE

sie_client = SIE()

sie_client.get_cetes() # Retrieve dictionary data for yield of cetes 28 days
"""
{
    'idSerie': 'SF43936',
    'titulo': 'Valores gubernamentales Resultados de la subasta semanal Tasa de rendimiento Cetes a 28 días',
    'datos': [{
        'fecha': '22/05/2025',
        'dato': '8.15'
    }]
}
"""
```


## Available Indicators

| Indicator            | Method                           | Description                                                                                                                              |
|----------------------|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Cetes 28 days        | `sie_client.get_cetes()`         | Valores gubernamentales Resultados de la subasta semanal Tasa de rendimiento Cetes a 28 días                                             |
| Dollar Exchange Rate | `sie_client.get_exchange_rate()` | Tipo de cambio Pesos por dólar E.U.A. Tipo de cambio para solventar obligaciones denominadas en moneda extranjera Fecha de determinación |
| Inflation            | `sie_client.get_inflation()`     | Inflación No subyacente (nueva definición) Anual                                                                                         |
| TIIE                 | `sie_client.get_tiie()`          | TIIE de Fondeo a Un Día Hábil Bancario, Mediana ponderada por volumen                                                                    |
| UDI                  | `sie_client.get_udi()`           | Valor de UDIS (Unidad de Medida de Inflación)                                                                                            |
| Yield Target         | `sie_client.get_yield_target()`  | Tasa objetivo                                                                                                                            |
