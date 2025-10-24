# Telegram WebApp Wallet System v1.0.1 / نظام محفظة Telegram WebApp الإصدار 1.0.1

## 🧾 Overview / نظرة عامة
Telegram WebApp Wallet هو نظام إدارة محفظة رقمية يعمل مع Telegram WebApp لإدارة المستخدمين، الأرصدة، والشحن.

## 🚀 Features / الميزات
- ✅ إدارة المستخدمين
- ✅ شحن الرصيد
- ✅ سجل إجراءات الأدمن
- ✅ تكامل مع Telegram WebApp
- ✅ قابل للتطوير والتحديث

## 🛠️ Requirements / المتطلبات
- Python 3.8+
- Node.js 16+
- Docker & Docker Compose

## 💻 Local Setup / إعداد التشغيل المحلي
```bash
docker-compose -f docker-compose.local.yml up -d
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## 🔗   
- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs
- Adminer: http://localhost:8080

## 🧪 Quick Test / اختبار سريع
```bash
curl -X POST http://localhost:8000/api/auth/ensure-simple \
 -H "Content-Type: application/json" \
 -d '{"telegram_id":123456789,"username":"test","first_name":"Test"}'
```

## 📚 التوثيق الكامل

- [📡 توثيق واجهة البرمجة (API)](./docs/API.md)
- [🏗️ هيكل المشروع](./docs/STRUCTURE.md)
- [🚀 دليل النشر](./docs/DEPLOYMENT.md) 
- [🐛 استكشاف الأخطاء](./docs/TROUBLESHOOTING.md)

## 📄 الترخيص
هذا المشروع مرخص تحت [MIT License](./LICENSE.md)
