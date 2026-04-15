# 07 - Validation et dépannage

Utilisez cette liste de contrôle après le déploiement.

## 1. Vérifications de santé

```bash
curl -fsS "$MATOS_BACKEND_URL/health"
curl -fsS "$BRIDGE_URL/health"
```

## 2. Vérification des produits backend

```bash
curl -fsS "$MATOS_BACKEND_URL/products" | head
```

## 3. Problèmes courants

### A) L'agent ne trouve pas les produits

- Confirmer que l'exécution de l'agent a `BACKEND_URL=$MATOS_BACKEND_URL`.
- Confirmer que le service backend est accessible et sain.

### B) Le pont retourne 500 sur le webhook Twilio

- Confirmer que `ADK_SERVICE_URL` pointe vers l'URL de l'agent.
- Confirmer que `ADK_APP_NAME` correspond au nom d'app déployé.
- Confirmer que les secrets Twilio ont été définis au moment du déploiement.

### C) Échecs de signature webhook Twilio

- Confirmer que l'URL du pont est exactement celle configurée dans Twilio.
- Confirmer que `TWILIO_AUTH_TOKEN` est correct.
- Confirmer la gestion URL proxy/https dans la validation de signature du pont.

### D) Pas de réponse WhatsApp

- Vérifier que la jonction sandbox Twilio est active pour votre numéro de test.
- Vérifier les logs Cloud Run pour les services pont et agent.

## 4. Test de bout en bout

1. Envoyez une question en français : `Avez-vous des laptops disponibles ?`
2. Envoyez un message d'intention d'achat en swahili : `Nataka kununua laptop, naitwa Amina.`
3. Confirmer que la langue de réponse correspond à la langue de la requête.
4. Confirmer que le chemin de capture de prospect fonctionne lorsque les détails de contact sont fournis.

## 5. Logs

```bash
gcloud run services logs read matos-backend --region "$REGION" --limit 50
gcloud run services logs read matos-agent-service --region "$REGION" --limit 50
gcloud run services logs read matos-whatsapp-bridge --region "$REGION" --limit 50
```

## 6. Option finale: tester sans Twilio

Si Twilio n'est pas encore fonctionnel dans votre contexte, terminez le workshop avec:

- `08 - Frontend de test (sans Twilio)`

Cette page vous permet de valider la qualite de l'agent via un chat web connecte directement au service ADK.
