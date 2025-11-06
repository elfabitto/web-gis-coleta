"""
Configuração do Gunicorn para produção
"""

import multiprocessing

# Número de workers
workers = multiprocessing.cpu_count() * 2 + 1

# Tipo de worker
worker_class = "sync"

# Bind
bind = "0.0.0.0:8000"

# Timeout
timeout = 30

# Keepalive
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Processos
max_requests = 1000
max_requests_jitter = 50

# Segurança
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
