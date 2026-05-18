# Configuración de Gunicorn
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50
preload_app = True
daemon = False
pidfile = "/tmp/gunicorn.pid"
umask = 0o022
user = None
group = None
tmp_upload_dir = None
secure_scheme_header = "HTTP_X_FORWARDED_PROTO"
secure_scheme_header_value = "https"

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "crm"

# Server mechanics
daemon = False
pidfile = None
umask = 0
working_directory = None
initgroups = False

# SSL
keyfile = None
certfile = None
ssl_version = 5
cert_reqs = 0
ca_certs = None
suppress_ragged_eof = True
do_handshake_on_connect = False
server_side_ssl_context = None
