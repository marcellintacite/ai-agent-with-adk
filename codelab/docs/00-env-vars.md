# Environment Variables Reference

These variables are set during setup and used throughout the workshop.

| Variable | Value | Purpose |
|----------|-------|---------|
| `PROJECT_ID` | Your GCP project ID | Identifies your Google Cloud project |
| `REGION` | `europe-west1` | Region for all deployed services |
| `MATOS_BACKEND_URL` | Set after deploying backend | URL of the Matos backend service |
| `AGENT_URL` | Set after deploying agent | URL of the deployed AI agent |

## How they're set

All variables are defined in your terminal session during [Setup](01-setup.md).

If you restart your terminal or open a new session, re-run Step 6 from [Setup](01-setup.md):

```bash
export PROJECT_ID="your-gcp-project-id"
export REGION="europe-west1"
```

That's it. Everything else builds from there.
