# 📡 API Documentation v1.0.1 / توثيق واجهة البرمجة

## 🔐 Authentication & Users / المصادقة والمستخدمون

### ✅ Ensure or Create User / إنشاء أو تأكيد مستخدم
```http
POST /api/auth/ensure-simple
Content-Type: application/json

{
  "telegram_id": 123456789,
  "username": "johndoe",
  "first_name": "John"
}
```
**Response / الاستجابة:**
```json
{
  "user_id": 1,
  "telegram_id": 123456789,
  "role": "user",
  "username": "johndoe",
  "message": "User ensured successfully"
}
```

---
## 👨‍💼 Admin Actions / إجراءات الأدمن

### 💰 Top-up Balance / شحن رصيد
```http
POST /api/admin/topup-simple
Content-Type: application/json

{
  "admin_telegram_id": 123456789,
  "target_telegram_id": 987654321,
  "amount": 1000.0,
  "note": "Test top-up"
}
```
**Response / الاستجابة:**
```json
{
  "status": "success",
  "new_balance": 1000.0,
  "message": "Top-up completed successfully with action log"
}
```

---
## 📊 Developer Endpoints / واجهات التطوير

### List All Users / عرض جميع المستخدمين
```http
GET /api/dev/users
```

### List All Wallets / عرض جميع المحافظ
```http
GET /api/dev/wallets
```

---
## 🧪 Testing / اختبار النظام

### Server Test / اختبار الخادم
```http
GET /api/test/test
```

### Echo Test / اختبار Echo
```http
POST /api/test/echo
Content-Type: application/json

{"test": "data"}
```

---
## 🔍 System Health / حالة النظام
```http
GET /healthz
```

---
## 🧰 Examples / أمثلة جاهزة

### PowerShell
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/auth/ensure-simple" `
  -Method POST `
  -Headers @{"Content-Type" = "application/json"} `
  -Body '{"telegram_id":123456789,"username":"testuser","first_name":"Test"}'
```

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/api/auth/ensure-simple",
    json={
        "telegram_id": 123456789,
        "username": "testuser",
        "first_name": "Test"
    }
)
print(response.json())
```

