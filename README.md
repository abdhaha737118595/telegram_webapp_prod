# Telegram WebApp - Production SAM-ready project

This project contains:
- FastAPI backend (AWS Lambda via Mangum)
- SQLAlchemy models for Users/Wallets/Transactions/AdminActions
- Admin-safe endpoints (topup) with root-admin env and role checks
- React minimal admin UI to perform top-ups
- SAM template (template.yaml) to deploy backend

## Quick deploy (Backend)
1. Configure AWS CLI and SAM CLI.
2. Build & deploy:
   ```bash
   sam build
   sam deploy --guided
   ```
   Provide BotToken, DatabaseURL and RootAdmins (comma-separated telegram IDs).

## Frontend
- Set VITE_API_BASE to the API Gateway URL returned by SAM.
- Build and host on S3/CloudFront.

## Security notes
- Store secrets in AWS Secrets Manager and inject via environment variables.
- Use RDS Proxy if connecting many Lambdas to Postgres.
- Ensure Lambda has least privilege IAM role.
- Log and audit admin actions.
