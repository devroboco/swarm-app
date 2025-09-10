# Swarm App: Frontend + Backend com Réplicas e Balanceamento

## Estrutura

```
swarm-demo-app/
├─ stack.yml
├─ frontend/
│  ├─ Dockerfile
│  ├─ requirements.txt
│  └─ app.py
└─ backend/
   ├─ Dockerfile
   ├─ requirements.txt
   └─ app.py
```

## Passo a Passo (resumo)

1. **Inicialize o Swarm**
   ```bash
   docker swarm init --advertise-addr 127.0.0.1
   ```
2. **Crie a rede overlay**
   ```bash
   docker network create --driver overlay --attachable app-net
   ```
3. **Crie Config e Secret (opcional)**
   ```bash
   echo "Demo Swarm - App Message" | docker config create app-message -
   printf "MY_FAKE_TOKEN_123" | docker secret create app-token -
   ```
4. **Build das imagens (no manager)**
   ```bash
   cd backend && docker build -t backend:1.0 .
   cd ../frontend && docker build -t frontend:1.0 .
   ```
5. **Deploy do stack**
   ```bash
   docker stack deploy -c stack.yml mystack
   docker stack services mystack
   ```
6. **Testes de balanceamento**
   ```bash
   curl -s http://localhost:8080 | jq
   ```
   Observe `frontend_hostname` alternando entre réplicas (balanceamento externo) e
   os `backend_calls` alternando hostnames do backend (balanceamento interno).
7. **Scaling**
   ```bash
   docker service scale mystack_frontend=5
   docker service scale mystack_backend=5
   ```
8. **Update / Rollback**
   ```bash
   docker service update --update-parallelism 1 --update-delay 5s mystack_frontend
   # docker service rollback mystack_frontend
   ```

## Como funciona o balanceamento

- **Externo (frontend):** o Swarm publica a porta (8080) e usa **Ingress + Routing Mesh** para distribuir
  as conexões entre as réplicas do `frontend` (round-robin).
- **Interno (backend):** o `frontend` chama `http://backend:5000/info`: o DNS de serviço do Swarm resolve
  para um **VIP** e distribui as chamadas entre as réplicas do `backend`.
- **Configs/Secrets:** montados em runtime como arquivos em `/run/configs/*` e `/run/secrets/*`.

## Limpeza

```bash
docker stack rm mystack
docker config rm app-message
docker secret rm app-token
docker network rm app-net
```
