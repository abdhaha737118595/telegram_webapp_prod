# 🐛 Troubleshooting Guide v1.0.1 / دليل استكشاف الأخطاء

هذا الدليل يقدّم حلولاً فورية لمشاكل التشغيل الشائعة للخادم والواجهة الأمامية.

---
## ❌ 1. API لا يستجيب بعد التشغيل
**English:**
- Check if FastAPI started without errors
- Ensure correct `.env` values
- DynamoDB table exists and is ACTIVE

**Arabic:**
- تأكد أن الخادم بدأ بدون أخطاء
- تأكد من صحة بيانات الاتصال داخل `.env`
- تحقق من أن جدول DynamoDB موجود وتعمل حالته

✅ الحل:
- أعد تشغيل الخادم
- تحقق من سجلات SAM أو Docker

---
## ❌ 2. DynamoDB Access Denied / رفض الوصول
**English:**
- Ensure IAM Role has DynamoDB permissions
- Verify your AWS region

**Arabic:**
- تأكد أن الصلاحيات التشغيلية صالحة
- تأكد من المنطقة (region)

✅ الحل:
- حدّث الصلاحيات عبر IAM
- تأكد من استخدام نفس region في كل من SAM و DynamoDB

---
## ❌ 3. Telegram WebApp لا يفتح داخل التطبيق
**English:**
- Ensure domain is allowed in bot settings
- Ensure HTTPS is enabled

**Arabic:**
- تأكد من تسجيل الرابط داخل إعدادات BotFather
- تأكد من أن الرابط آمن HTTPS

✅ الحل:
```
BotFather → Edit WebApp → Add URL
```

---
## ❌ 4. مشكلة CORS
**Symptoms:**
- Browser blocks requests

✅ الحل:
- عدّل CORS في `main.py`:
```
allow_origins=["*"]
```

---
## ❌ 5. الرصيد لا يتحرك عند الشحن
**السبب المحتمل:**
- Admin not verified
- Target wallet not found

✅ الحل:
- تأكد من وجود المستخدم
- تأكد من أن الـ role = admin للشاحن
- تحقق من سجل العمليات

---
## ❌ 6. React لا يعمل بعد البناء
✅ الحل:
- احذف ثم أعد التثبيت:
```
npm install
npm run build
```

---
## ❌ 7. HTTP 403 عند استدعاء API
**السبب:**
- Missing Telegram auth header

✅ الحل:
- أرسل `telegram_id` في الـ JSON

---
## ❌ 8. لا يمكن ربط WebApp بالبوت
✅ الحل:
```
BotFather → /setdomain
BotFather → /setmenubutton
```

---
## ❌ 9. AWS SAM يفشل أثناء النشر
✅ الحل:
```
sam validate
sam build
sam deploy --guided
```

---
## ✅ نصائح عامة (General Tips)
- استخدم logging في `admin.py`, `auth.py`
- تحقق من DynamoDB TTL
- نظّف Sessions

🚀 انتهى الدليل بنجاح. جاهز للإضافة والتطوير!

