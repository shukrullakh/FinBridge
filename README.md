# 🌉 FinBridge — AI-Powered Financial Wellness Platform

> **"Don’t just track money. Train your financial behavior."**  
> (Faqat pulingizni hisoblab bormang. Moliyaviy xulq-atvoringizni shakllantiring).

FinBridge — Oʻzbekiston bozori (UZS valyutasi) uchun maxsus moslashtirilgan, xatti-harakatlarga asoslangan (*Behavioral Finance*) sunʼiy intellektli moliyaviy farovonlik veb-platformasi (Hackathon MVP).

---

## 🌟 Asosiy Modullar (Core Modules)

1. **Dashboard (Boshqaruv paneli):**
   * Balans, daromad va xarajatlar ko'rsatkichlari.
   * Xarajat toifalari va belgilangan "qizil chiziqlar" (limitlar) tahlili.
   * Yaqinlashib kelayotgan qarz to'lovlari va jamg'arma maqsadlari.

2. **Smart Pause (Flagman xususiyat):**
   * Rejalashtirilgan xaridni kiritish va uning byudjet hamda jamg'armaga xavfini baholash.
   * Emotsional xaridlarning oldini olish uchun **15 daqiqalik sovutish taymeri (*cooling-off period*)**.
   * Xaridni bekor qilish, keyinga qoldirish yoki tasdiqlash qarorlari.

3. **Invisible Savings (Sezilmas Jamg'arma):**
   * Har bir xarajatni eng yaqin 1 000 yoki 5 000 UZS gacha yaxlitlash (*round-up* simulyatsiyasi).
   * Mayda qoldiqlarni avtomatik jamg'arma maqsadlariga yo'naltirish.

4. **Debt Coach (Qarzlarni Oqilona To'lash):**
   * Qarz va muddatli to'lovlarni (nasiya, kredit) boshqarish.
   * Ikkita asosiy strategiya taqqoslovi:
     * **Snowball (Qor to'pi):** Eng kichik qarzdan boshlash (psixologik intizom va tez natija).
     * **Avalanche (Qor ko'chkisi):** Eng yuqori foizli qarzdan boshlash (foizdan maksimal tejash).

5. **Financial Behavior Score (Moliyaviy Xulq-atvor Bali):**
   * Shaffof 100 ballik shaxsiy moliya intizomi ko'rsatkichi.
   * 4 ta o'lcham: Xarajatlar nazorati (30%), Jamg'arma barqarorligi (25%), Qarz yuki (25%), Maqsadlar sur'ati (20%).

---

## 🛠 Texnologik Stek

* **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons
* **Backend:** Python 3.9+, FastAPI, Pydantic v2, Pytest (16/16 testlar muvaffaqiyatli o'tgan)
* **Hisob-kitoblar:** Deterministik `Decimal` aniqligida, binary float xatolarisiz

---

## 🚀 Loyihani Ishga Tushirish

### Bitta buyruq bilan (Ham Backend, ham Frontend):
```bash
./start.sh
```

Yoki alohida-alohida:

#### 1. Backend:
```bash
backend/.venv/bin/python3 backend/run.py
```
* **API:** `http://127.0.0.1:8000`
* **Swagger Docs:** `http://127.0.0.1:8000/docs`

#### 2. Frontend:
```bash
cd frontend
npm run dev
```
* **Veb-ilova:** `http://localhost:5173`

---

## 🧪 Testlarni Ishga Tushirish
```bash
PYTHONPATH=backend backend/.venv/bin/pytest backend/tests -v
```
