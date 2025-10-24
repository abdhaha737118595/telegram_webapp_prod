# 🏗️ Project Structure v1.0.1 / هيكل المشروع

## 📁 Root Structure / البنية العامة للجذر
```
telegram_webapp_prod/
├── README.md               # دليل المشروع الرئيسي
├── docker-compose.local.yml # تكوين Docker للتطوير
├── template.yaml           # تكوين AWS SAM للنشر
├── backend/                # الخادم الخلفي (FastAPI)
└── frontend/               # الواجهة الأمامية (React)
```

---
## 🔧 Backend Structure (FastAPI) / هيكلة الخادم الخلفي
```
backend/
├── requirements.txt       # تبعيات Python
├── .env.local             # متغيرات البيئة المحلية
└── app/
    ├── main.py            # التطبيق الرئيسي ونقاط التشغيل
    ├── api/               # مسارات API
    │   ├── auth.py
    │   ├── admin.py
    │   ├── telegram.py
    │   ├── auth_simple.py
    │   ├── admin_simple.py
    │   ├── simple_test.py
    │   └── dev.py
    ├── db/                # إدارة قواعد البيانات
    │   ├── database.py
    │   └── crud.py
    ├── models/            # نماذج ORM
    │   ├── base.py
    │   ├── user.py
    │   ├── wallet.py
    │   ├── transaction.py
    │   └── admin_action.py
    └── utils/             # أدوات مساعدة
        └── security.py
```

---
## 🎨 Frontend Structure (React WebApp) / هيكلة الواجهة الأمامية
```
frontend/
├── package.json
├── index.html
└── src/
    ├── main.jsx           # نقطة الدخول
    ├── App.jsx            # التطبيق الرئيسي
    ├── styles.css         # التنسيقات
    └── pages/
        └── Admin.jsx      # صفحة الإدارة
```

---
## 🗃️ Data Models / نماذج البيانات

### 👤 User / المستخدم
- `id` — User unique identifier / معرف المستخدم
- `telegram_id` — Telegram account ID
- `username`
- `first_name`
- `role` — user/admin
- `created_at`

### 💰 Wallet / المحفظة
- `id`
- `user_id`
- `balance`
- `created_at`
- `updated_at`

### 📋 AdminAction / إجراءات الأدمن
- `id`
- `admin_id`
- `action`
- `target_user_id`
- `details`
- `created_at`

---
## 🔗 Table Relationships / العلاقات بين الجداول
- User (1) ⇄ (1) Wallet
- User (1) ⇄ (N) AdminAction (as admin)
- User (1) ⇄ (N) AdminAction (as target)

