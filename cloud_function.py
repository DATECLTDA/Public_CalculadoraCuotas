import json
import logging
from CalculadoraCuotas.calculadora_cuotas import obtener_cuota_mensual_total


def calculate_monthly_fee(request):
    logging.basicConfig(level=logging.DEBUG)

    logging.debug("Request data: %s", request.data)
    # Define una lista de dominios permitidos
    allowed_origins = [
        'https://elgeniox.com',
        'https://elgenioxlatam.com/'
    ]

    # Obtén el valor del origen de la solicitud actual
    origin = request.headers.get('Origin')
    print(origin)

    headers = {
        'Access-Control-Allow-Origin': origin if origin in allowed_origins else 'https://elgeniox.com',
        'Access-Control-Allow-Methods': 'PUT, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization', 
        'Access-Control-Max-Age': '3600',
    }

    # Aquí se maneja la solicitud de tipo OPTIONS
    if request.method == 'OPTIONS':
        return ('', 204, headers)
    
    # Leer el JSON del cuerpo de la solicitud
    request_json = request.get_json()["prestamo"]
    if not request_json or (('monto' not in request_json) or
                            ('plazo' not in request_json) or
                            ('aporte_inicial' not in request_json)):
        return 'JSON inválido', 400, headers
    
    try:
        # Calcular cuota mensual 
        cuota = obtener_cuota_mensual_total(request_json['monto'], request_json['plazo'], \
                            aporte_inicial=request_json['aporte_inicial'])
        
        return json.dumps({'cuota_mensual': cuota}), 200, headers
    except ValueError as ve:
         return str(ve), 400, headers
    
    

