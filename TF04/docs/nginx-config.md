# Configuração do Nginx

## nginx.conf

### Gzip Compression
Habilitado para `text/plain`, `text/css`, `application/json`, `application/javascript` e `text/xml`.
Nível de compressão 6, mínimo de 1000 bytes.

### Rate Limiting
Duas zonas definidas:
- `api_limit`: 10 req/s por IP para `/api/` (burst 20)
- `general_limit`: 30 req/s por IP para rotas gerais (burst 50)

### Log Format
Log customizado `upstream_log` inclui:
- `upstream` — endereço IP:porta da instância que respondeu
- `upstream_status` — código HTTP retornado pelo upstream
- `upstream_time` — tempo de resposta do upstream
- `request_time` — tempo total da requisição

## load-balancer.conf

### Upstream `backend_pool`
- Algoritmo: `least_conn` (menor número de conexões ativas)
- 3 servidores: `backend1:5000`, `backend2:5000`, `backend3:5000`
- `max_fails=3 fail_timeout=30s` — após 3 falhas, instância é removida por 30s (failover automático)
- `keepalive 32` — pool de conexões persistentes

### Virtual Hosts
- Porta 80: redireciona para HTTPS
- Porta 443: servidor principal com SSL

### Proxy Headers
```
X-Real-IP         → IP real do cliente
X-Forwarded-For   → cadeia de proxies
X-Forwarded-Proto → protocolo original (https)
X-Upstream-Addr   → instância que respondeu (visível no response header)
```

### Timeouts
- `proxy_connect_timeout 10s`
- `proxy_send_timeout 30s`
- `proxy_read_timeout 30s`

## ssl.conf
- Session cache compartilhado de 10MB
- HSTS habilitado (max-age 1 ano)
- Headers de segurança: `X-Frame-Options`, `X-Content-Type-Options`
