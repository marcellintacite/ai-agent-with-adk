# 07 - Validation et dépannage

Utilisez cette checklist après le déploiement.

## 1. Vérifications de santé

```bash
curl -fsS "$MATOS_BACKEND_URL/health"
curl -fsS "$BRIDGE_URL/health"
curl -I "$MATOS_AGENT_URL/dev-ui/"
```

## 2. Vérification des données du backend

```bash
curl -fsS "$MATOS_BACKEND_URL/products" | head
```

## 3. Problèmes courants

### A) L'agent ne trouve pas de produits

- Vérifiez que le runtime de l'agent a `BACKEND_URL=$MATOS_BACKEND_URL`.
- Vérifiez que le service backend est sain.

### B) Le bridge renvoie 500 sur `/chat`

- Vérifiez que `ADK_SERVICE_URL` pointe vers `MATOS_AGENT_URL`.
- Vérifiez que `ADK_APP_NAME=matos`.
- Vérifiez que le service bridge est bien déployé et accessible.

### C) L'endpoint graph du bridge renvoie 404

- Vérifiez que le nom de l'agent déployé est `matos`.
- Retestez :

```bash
curl -I "$MATOS_AGENT_URL/dev/build_graph_image/matos?dark_mode=true"
```

### D) Pas de réponse dans le frontend

- Vérifiez que le frontend appelle `${BRIDGE_URL}/chat`.
- Vérifiez les logs du bridge et de l'agent.

## 4. Vérification du comportement de bout en bout

1. Envoyez une requête produit : `Do you have laptops available?`
2. Envoyez une requête d'intention d'achat : `I want to buy a laptop, my name is Amina.`
3. Vérifiez que la réponse est pertinente et tient compte du contexte.
4. Vérifiez que la capture de lead fonctionne lorsque des infos de contact sont fournies.

## 5. Logs

```bash
gcloud run services logs read matos-backend-service --region "$REGION" --limit 50
gcloud run services logs read matos-agent-service --region "$REGION" --limit 50
gcloud run services logs read matos-bridge --region "$REGION" --limit 50
```

## 6. Parcours principal recommandé

Utilisez `08 - Frontend Playground (webhook/chat)` pour valider le comportement complet de l'agent via le chat web.
