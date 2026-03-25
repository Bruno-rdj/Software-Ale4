# TF04 - E-commerce com Load Balancer Avançado

## Aluno
- **Nome:** Bruno Rocha Rozadas de Jesus
- **RA:** 6324038
- **Curso:** Análise e Desenvolvimento de Sistemas

## Arquitetura
- **Nginx:** Load balancer com SSL e rate limiting
- **Backend:** 3 instâncias da API para alta disponibilidade
- **Frontend:** Loja virtual estática
- **Admin:** Painel administrativo

```
                    ┌─────────────────────────────┐
                    │         NGINX               │
                    │  Load Balancer + SSL + GZip │
                    │  Porta 80 → 443 (redirect)  │
                    └──────────┬──────────────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │ backend1 │    │ backend2 │    │ backend3 │
        │ :5000    │    │ :5000    │    │ :5000    │
        └──────────┘    └──────────┘    └──────────┘
```

## Funcionalidades Implementadas
- ✅ Load balancing com algoritmo `least_conn`
- ✅ Health checks automáticos (passive, max_fails=3, fail_timeout=30s)
- ✅ Failover transparente
- ✅ SSL/TLS com certificado self-signed
- ✅ Rate limiting para proteção (`api_limit` 10r/s, `general_limit` 30r/s)
- ✅ Logs detalhados com upstream info (`upstream_addr`, `upstream_time`)
- ✅ Compressão gzip (nível 6)
- ✅ Virtual hosts (HTTP → HTTPS redirect)
- ✅ Proxy headers corretos (X-Real-IP, X-Forwarded-For, X-Forwarded-Proto)
- ✅ Painel admin com dashboard de monitoramento

## Como Executar

### Pré-requisitos
- Docker e Docker Compose

### Execução
```bash
git clone https://github.com/Bruno-rdj/Software-Ale4.git
cd TF04

# Gerar certificados SSL (Linux/Mac)
cd scripts && bash generate-ssl.sh && cd ..

# Subir todos os serviços
docker-compose up -d --build

# Verificar status
docker-compose ps
```

> **Windows:** Os certificados já estão incluídos em `nginx/ssl/`. Não é necessário rodar o script.

## Endpoints

| Endpoint             | Descrição                          |
|----------------------|------------------------------------|
| `https://localhost/` | Frontend - Loja virtual            |
| `https://localhost/produtos.html` | Catálogo de produtos  |
| `https://localhost/carrinho.html` | Carrinho de compras   |
| `https://localhost/api/`         | API (load balanced)   |
| `https://localhost/api/info`     | Info da instância atual |
| `https://localhost/api/products` | Lista de produtos      |
| `https://localhost/api/status`   | Status da instância    |
| `https://localhost/admin/`       | Painel administrativo  |
| `https://localhost/nginx-status` | Métricas do Nginx      |
| `https://localhost/health`       | Health check global    |

## Testes de Load Balancing

```bash
# Testar distribuição de carga (Linux/Mac)
for i in {1..6}; do
  curl -sk https://localhost/api/info | python3 -c "import sys,json; print(json.load(sys.stdin)['instance_id'])"
done

# Windows PowerShell
1..6 | ForEach-Object { (Invoke-WebRequest -Uri "http://localhost/api/info" -UseBasicParsing).Content }

# Simular falha de instância
docker stop ecommerce-backend1

# Verificar failover automático
curl -sk https://localhost/api/info

# Restaurar instância
docker start ecommerce-backend1
```

## Monitoramento

```bash
# Logs com upstream info
docker-compose logs nginx

# Filtrar apenas linhas com upstream
docker-compose logs nginx | grep "upstream="

# Métricas em tempo real
watch -n 2 'curl -s http://localhost/nginx-status'
```

## Estrutura do Projeto

```
TF04/
├── README.md
├── docker-compose.yml
├── nginx/
│   ├── nginx.conf              # Config principal (gzip, rate limit, log format)
│   ├── ssl/
│   │   ├── cert.pem            # Certificado self-signed
│   │   └── key.pem             # Chave privada
│   └── conf.d/
│       ├── load-balancer.conf  # Upstream, virtual hosts, proxy reverso
│       └── ssl.conf            # Segurança SSL global
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   ├── produtos.html
│   ├── carrinho.html
│   └── css/style.css
├── backend/
│   ├── Dockerfile
│   ├── app.py                  # API Flask com 6 endpoints
│   ├── requirements.txt
│   └── config.py
├── admin/
│   ├── Dockerfile
│   ├── dashboard.html          # Dashboard de monitoramento
│   └── css/admin.css
├── scripts/
│   └── generate-ssl.sh
└── docs/
    ├── nginx-config.md         # Documentação das configs Nginx
    └── load-balancing.md       # Documentação do load balancing
```
