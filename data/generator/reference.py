"""Reference data for synthetic LogiStream sources."""

from __future__ import annotations

CDS = [
    {"origin_cd": "CD-SAO", "city": "Sao Paulo", "state": "SP", "lat": -23.5505, "lon": -46.6333, "cold": True},
    {"origin_cd": "CD-CAM", "city": "Campinas", "state": "SP", "lat": -22.9056, "lon": -47.0608, "cold": True},
    {"origin_cd": "CD-RIO", "city": "Rio de Janeiro", "state": "RJ", "lat": -22.9068, "lon": -43.1729, "cold": False},
    {"origin_cd": "CD-BHZ", "city": "Belo Horizonte", "state": "MG", "lat": -19.9167, "lon": -43.9345, "cold": False},
    {"origin_cd": "CD-CWB", "city": "Curitiba", "state": "PR", "lat": -25.4284, "lon": -49.2733, "cold": True},
    {"origin_cd": "CD-POA", "city": "Porto Alegre", "state": "RS", "lat": -30.0346, "lon": -51.2177, "cold": False},
    {"origin_cd": "CD-SSA", "city": "Salvador", "state": "BA", "lat": -12.9777, "lon": -38.5016, "cold": True},
    {"origin_cd": "CD-REC", "city": "Recife", "state": "PE", "lat": -8.0476, "lon": -34.8770, "cold": False},
]

CITIES = [
    ("Sao Paulo", "SP", "01001000"),
    ("Guarulhos", "SP", "07010000"),
    ("Campinas", "SP", "13010000"),
    ("Santos", "SP", "11010000"),
    ("Rio de Janeiro", "RJ", "20010000"),
    ("Niteroi", "RJ", "24020000"),
    ("Belo Horizonte", "MG", "30110000"),
    ("Uberlandia", "MG", "38400000"),
    ("Curitiba", "PR", "80010000"),
    ("Londrina", "PR", "86010000"),
    ("Porto Alegre", "RS", "90010000"),
    ("Caxias do Sul", "RS", "95010000"),
    ("Salvador", "BA", "40010000"),
    ("Feira de Santana", "BA", "44001000"),
    ("Recife", "PE", "50010000"),
    ("Olinda", "PE", "53010000"),
    ("Brasilia", "DF", "70040900"),
    ("Goiania", "GO", "74000000"),
]

PRODUCTS = [
    {"sku": "SKU-CF0001", "name": "Cafe torrado 500g", "category": "alimentos", "cold": False, "price": 32.9},
    {"sku": "SKU-LT0002", "name": "Leite longa vida 1L", "category": "alimentos", "cold": True, "price": 6.5},
    {"sku": "SKU-QG0003", "name": "Queijo mussarela 400g", "category": "alimentos", "cold": True, "price": 28.4},
    {"sku": "SKU-EL0004", "name": "Fone bluetooth", "category": "eletronicos", "cold": False, "price": 149.0},
    {"sku": "SKU-EL0005", "name": "Carregador USB-C", "category": "eletronicos", "cold": False, "price": 59.9},
    {"sku": "SKU-CS0006", "name": "Camiseta algodao M", "category": "vestuario", "cold": False, "price": 49.9},
    {"sku": "SKU-CS0007", "name": "Tenis corrida 42", "category": "vestuario", "cold": False, "price": 289.0},
    {"sku": "SKU-HS0008", "name": "Shampoo 400ml", "category": "higiene", "cold": False, "price": 24.5},
    {"sku": "SKU-HS0009", "name": "Sabonete kit 4un", "category": "higiene", "cold": False, "price": 18.9},
    {"sku": "SKU-CF0010", "name": "Chocolate 90g", "category": "alimentos", "cold": False, "price": 9.5},
    {"sku": "SKU-EL0011", "name": "Smartwatch", "category": "eletronicos", "cold": False, "price": 799.0},
    {"sku": "SKU-CF0012", "name": "Azeite 500ml", "category": "alimentos", "cold": False, "price": 42.0},
]

VEHICLE_TYPES = [
    {"prefix": 1, "kind": "van", "refrigerated": False},
    {"prefix": 2, "kind": "bau", "refrigerated": False},
    {"prefix": 3, "kind": "bau_frio", "refrigerated": True},
    {"prefix": 4, "kind": "toco", "refrigerated": False},
]

CHANNELS = ["site", "app", "marketplace"]

COMMENTS = [
    "Entrega no prazo, produto ok.",
    "Embalagem amassada, mas o item funcionou.",
    "Atraso de um dia. Ninguem avisou.",
    "Motorista educado, chegou antes da janela.",
    "Produto com validade curta. Pedi troca.",
    "App mostrou entregue e ainda nao tinha chegado.",
    "Perfeito. Compraria de novo.",
    "A caixa veio aberta. Faltou um item.",
    "Temperatura do leite chegou alta. Ficou azedo no outro dia.",
    "Rapido demais. Surpreendeu.",
]
