# Load Balancing

## Algoritmo: least_conn

O `least_conn` direciona cada nova requisição para a instância com **menos conexões ativas** no momento.
Ideal para APIs com tempos de resposta variáveis, evitando sobrecarga em instâncias lentas.

## Fluxo de uma Requisição

```
Cliente → Nginx (porta 443)
       → upstream backend_pool (least_conn)
       → backend1 | backend2 | backend3
       ← resposta com header X-Upstream-Addr
```

## Health Checks e Failover

O Nginx usa **passive health checks** via `max_fails` e `fail_timeout`:

| Parâmetro     | Valor | Descrição                                      |
|---------------|-------|------------------------------------------------|
| max_fails     | 3     | Falhas consecutivas para marcar como inativo   |
| fail_timeout  | 30s   | Tempo fora do pool após atingir max_fails       |

Após 30s, a instância é testada novamente automaticamente.

## Verificar Distribuição de Carga

```bash
# 6 requisições consecutivas — deve mostrar instâncias diferentes
for i in {1..6}; do
  curl -sk https://localhost/api/info | python3 -c "import sys,json; print(json.load(sys.stdin)['instance_id'])"
done
```

## Simular Failover

```bash
# Parar uma instância
docker stop ecommerce-backend1

# Verificar que as outras assumem
curl -sk https://localhost/api/info

# Restaurar
docker start ecommerce-backend1
```

## Visualizar Logs com Upstream Info

```bash
docker-compose logs nginx | grep upstream=
```

Exemplo de linha de log:
```
172.18.0.1 - - [01/Jan/2026:10:00:00 +0000] "GET /api/info HTTP/1.1" 200 120
upstream=172.18.0.3:5000 upstream_status=200 upstream_time=0.003 request_time=0.004
```
