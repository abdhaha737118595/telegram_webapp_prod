# DEPLOYMENT.md

## 🚀 Deployment Guide (English)

This document provides a structured guide to deploy the backend, database, and bot onto AWS using best practices.

---

## ✅ Requirements
- AWS Account
- IAM User with proper permissions
- AWS CLI installed locally
- Docker installed (optional, if using container-based deployment)
- GitHub account (optional, for CI/CD)

---

## ☁️ AWS Services Used
- **API Gateway** (Public HTTP Endpoint)
- **Lambda** (Backend business logic)
- **DynamoDB** (Database for wallets, cards & users)
- **S3** (Card CSV uploads & storage)
- **CloudWatch** (Logs & Cron jobs)
- **Secrets Manager** (Store Telegram Bot token)
- **IAM** (Permissions & policies)

---

## 🔐 Environment Variables
The following must be provided for deployment:
```
TELEGRAM_BOT_TOKEN
DATABASE_TABLE_USERS
DATABASE_TABLE_WALLETS
DATABASE_TABLE_CARDS
S3_BUCKET_CARDS
```
Stored inside AWS Secrets Manager and loaded by Lambda.

---

## 🧩 Architecture Overview
```
User -> Telegram Bot -> Lambda -> DynamoDB
                      |-> S3 (card CSVs)
CloudWatch -> scheduled jobs
```
---

## 🛠️ Deployment Steps

### 1️⃣ Create DynamoDB Tables
- `UsersTable`
- `WalletsTable`
- `CardsTable`

Use `PrimaryKey: userId` for Users.
Use `PrimaryKey: cardId` for Cards.

---

### 2️⃣ Create S3 Bucket
- Name example: `mt-cards-storage-prod`
- Enable versioning

Upload CSV card files here.

---

### 3️⃣ Store Secrets
Store Telegram token inside AWS Secrets Manager.

Key name example:
```
prod/telegram/token
```

---

### 4️⃣ Deploy Lambda
Options:
- SAM CLI (recommended)
- Serverless Framework
- Terraform

Attach necessary policies for DynamoDB, S3, CloudWatch.

---

### 5️⃣ Create API Gateway
Proxy integration -> Lambda

Route example:
```
POST /telegramWebhook
```

---

### 6️⃣ Set Telegram Webhook
Example:
```
https://api.telegram.org/bot<TOKEN>/setWebhook?url=<API_GATEWAY_URL>/telegramWebhook
```

---

### 7️⃣ Configure Logs
CloudWatch log groups per Lambda.

---

### 8️⃣ Schedule Maintenance Tasks
Example jobs:
- unused card cleanup
- daily wallet summary

Create EventBridge rules.

---

### 9️⃣ Upload CSV Cards
Upload to S3 then trigger Lambda S3 event.
Cards are parsed and saved to DynamoDB.

---

## 🔁 CI/CD (Optional)
Use GitHub Actions to redeploy on push.

---

## 🚨 Error Handling
- Retry via SQS DLQ (optional)
- Log alerts via CloudWatch Alarms

---

## 🔒 Security Checklist
- No public DynamoDB access
- S3 is private
- IAM permissions are least privilege
- Webhook secret token enabled

✅ Approved for production.

---

## 📦 Deployment Output
After deployment you should have:
- Public webhook URL
- Active Lambda backend
- DynamoDB storing data
- S3 card uploads working

---

# 🇸🇦 دليل النشر (عربي)

هذا الدليل يشرح خطوات نشر النظام على AWS بطريقة منظمة وآمنة.

---

## ✅ المتطلبات
- حساب AWS
- مستخدم IAM بصلاحيات مناسبة
- AWS CLI مثبت محليًا
- Docker (اختياري)

---

## ☁️ الخدمات المستخدمة
- API Gateway
- Lambda
- DynamoDB
- S3
- CloudWatch
- Secrets Manager

---

## 🔐 متغيرات البيئة
يجب توفير:
```
TELEGRAM_BOT_TOKEN
DATABASE_TABLE_USERS
DATABASE_TABLE_WALLETS
DATABASE_TABLE_CARDS
S3_BUCKET_CARDS
```

---

## 🛠️ خطوات النشر

### 1️⃣ إنشاء جداول DynamoDB
- UsersTable
- WalletsTable
- CardsTable

---

### 2️⃣ إنشاء Bucket في S3
لتخزين ملفات CSV الخاصة بالكروت.

---

### 3️⃣ تخزين التوكنات في Secrets Manager
لزيادة الأمان.

---

### 4️⃣ نشر Lambda
باستخدام SAM أو Serverless Framework.

---

### 5️⃣ إنشاء API Gateway
يربط الطلبات بالـ Lambda.

---

### 6️⃣ ضبط Webhook في Telegram
باستخدام عنوان API Gateway.

---

### 7️⃣ رفع ملفات CSV للكروت
إلى S3 وسيتم معالجتها تلقائياً.

---

### 8️⃣ جدولة مهام الصيانة
مثل حذف الكروت القديمة.

---

✅ عند إتمام الخطوات يكون النظام جاهز للعمل.

---

## 🎉 مبروك!
تم إعداد النظام بكفاءة وبأعلى مستوى أمان واستقرار.

