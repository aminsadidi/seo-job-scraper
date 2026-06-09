# 🤖 ربات یابنده شغل ریموت (Remote Job Scraper Bot)

این ربات هر روز آگهی‌های شغلی ریموت و دورکاری رو از سایت‌های مختلف پیدا می‌کنه و مستقیم به تلگرامت می‌فرسته.

**کاملاً رایگانه و هیچ نیازی به خرید سرور یا هاست نداری.** ربات روی GitHub Actions به صورت خودکار اجرا میشه.

> 💡 این ربات الان روی **SEO** تنظیم شده، ولی با چند تغییر ساده می‌تونی برای **هر فیلد شغلی** ازش استفاده کنی (توسعه‌دهنده، دیزاینر، مارکتینگ، دیتا، DevOps و...). [بخش سفارشی‌سازی](#-سفارشیسازی-برای-فیلدهای-شغلی-دیگه) رو ببین.

---

## ✨ چیکار می‌کنه؟

- 🔍 هر روز از **۶+ سایت کاریابی** آگهی‌های ریموت رو جمع می‌کنه
- 📊 آگهی‌ها رو **امتیازدهی** می‌کنه و فقط مرتبط‌ترین‌ها رو می‌فرسته
- ⛔ آگهی‌های نامرتبط رو **خودکار فیلتر** می‌کنه
- 🧠 با **هوش مصنوعی** برای هر آگهی Cover Letter اختصاصی می‌نویسه (اختیاری)
- ⏰ هر روز صبح **خودش اجرا میشه** — کاری نباید بکنی

---

## 🚀 آموزش راه‌اندازی قدم به قدم (فقط ۵ دقیقه)

برای راه‌اندازی این ربات **اصلاً نیازی نیست برنامه‌نویس باشی**. فقط این ۵ قدم رو به ترتیب انجام بده:

---

### 📌 قدم اول: پروژه رو برای خودت کپی کن (Fork)

اون بالا سمت راست همین صفحه، یک دکمه هست به اسم **Fork**. روش کلیک کن و بعد دکمه سبز رنگ **Create Fork** رو بزن.

یه کپی از این ربات توی اکانت GitHub خودت ساخته میشه. از الان به بعد روی اون کپی کار می‌کنیم.

---

### 📌 قدم دوم: ربات تلگرامت رو بساز

ما به یه ربات تلگرام نیاز داریم تا پیام‌ها رو برات بفرسته.

1. تو تلگرام به `@BotFather` پیام بده
2. بنویس `/newbot` و یه اسم و username برای رباتت انتخاب کن
3. یه متن طولانی بهت میده که توش **Token** نوشته شده (شبیه `123456:ABC-DEF...`). **کپیش کن و یه جا نگهش دار**
4. حالا به `@userinfobot` تو تلگرام پیام بده
5. بهت یه عدد میده به اسم **Id** (مثل `123456789`). **اینو هم کپی کن**

---

### 📌 قدم سوم: ویزارد تنظیمات (Setup Wizard)

به جای اینکه تنظیمات رو دستی و سخت انجام بدی، از فایلی که برات آماده کردیم استفاده کن:

1. توی همین صفحه، فایل `setup_wizard.html` رو پیدا کن و **دانلودش** کن
2. با مرورگر (Chrome یا Firefox) **بازش** کن
3. **Token ربات** و **Chat ID** (که قدم دوم گرفتی) رو وارد کن
4. بقیه گزینه‌ها اختیاریه — می‌تونی فعلاً خالی بذاری
5. روی دکمه **⚙️ تولید Secrets** کلیک کن
6. دکمه **📋 کپی همه** رو بزن

---

### 📌 قدم چهارم: وارد کردن تنظیمات در GitHub

حالا باید اون چیزی که کپی کردی رو به GitHub بدی تا ربات بتونه کار کنه:

1. برو به صفحه ریپوی خودت (همون Fork)
2. تب **Settings** (بالای صفحه) رو بزن
3. از منوی سمت چپ: **Secrets and variables** → **Actions**
4. دکمه سبز **New repository secret** رو بزن
5. دونه‌دونه اطلاعاتی که ویزارد بهت داد رو اینجا وارد کن:
   - اسم: `TELEGRAM_BOT_TOKEN` → مقدار: Token رباتت
   - اسم: `TELEGRAM_CHAT_ID` → مقدار: عدد Chat ID

> 💡 اگه ویزارد چیزای دیگه هم بهت داد (مثل AI_PROVIDER)، اونا رو هم همینجا اضافه کن.

---

### 📌 قدم پنجم: روشن کردن ربات!

تنظیمات تموم شد! الان ربات رو روشن کن:

1. برو به تب **Actions** (بالای صفحه، کنار Pull requests)
2. یه پیام سبز میبینی — روش کلیک کن تا فعال بشه
3. از منوی سمت چپ، روی **Job Search Bot** کلیک کن
4. سمت راست، دکمه **Run workflow** رو بزن و بعد دکمه سبز رو بزن

✅ **تمام!** بعد ۱-۲ دقیقه اولین آگهی‌های کاریابی توی ربات تلگرامت میاد.

از فردا، ربات **خودش هر روز صبح اتوماتیک** اجرا میشه.

---

## 🎯 سفارشی‌سازی برای فیلدهای شغلی دیگه

این ربات الان روی SEO تنظیمه، ولی **فقط با تغییر ۴ بخش ساده** تو فایل `bot.py` می‌تونی برای هر فیلد شغلی ازش استفاده کنی.

فایل `bot.py` رو باز کن و این بخش‌ها رو تغییر بده:

---

### ۱. عبارات جستجو (`JSEARCH_QUERIES`) — خط ~۱۲۲

اینا عباراتی هستن که ربات باهاشون آگهی جستجو می‌کنه. به زبان انگلیسی بنویس:

```python
# نمونه SEO (پیش‌فرض):
JSEARCH_QUERIES = {
    1: ["Junior SEO remote", "Technical SEO remote", "SEO Python remote"],
    2: ["SEO Content Editor remote", "WordPress SEO Specialist remote"],
    3: ["on-page SEO specialist remote", "SEO copywriter remote"],
}

# نمونه Front-end Developer:
JSEARCH_QUERIES = {
    1: ["Junior Frontend Developer remote", "React Developer remote"],
    2: ["Vue.js Developer remote", "JavaScript Developer remote"],
    3: ["UI Developer remote", "Frontend Engineer remote"],
}

# نمونه Data Analyst:
JSEARCH_QUERIES = {
    1: ["Junior Data Analyst remote", "Data Analyst Python remote"],
    2: ["Business Intelligence Analyst remote", "SQL Analyst remote"],
    3: ["Data Visualization Analyst remote", "Excel Analyst remote"],
}

# نمونه Graphic Designer:
JSEARCH_QUERIES = {
    1: ["Graphic Designer remote", "UI Designer remote"],
    2: ["Visual Designer remote", "Brand Designer remote"],
    3: ["Figma Designer remote", "Creative Designer remote"],
}
```

> 💡 **نکته:** عدد ۱ = اولویت بالا (هر روز اجرا میشه)، عدد ۳ = اولویت پایین (فقط روزهای زوج)

---

### ۲. مهارت‌های شما (`USER_SKILLS`) — آسون‌ترین راه!

**بدون نیاز به تغییر کد!** فقط یه GitHub Secret اضافه کن:

- اسم: `USER_SKILLS`
- مقدار: مهارت‌هات رو comma-separated بنویس

```
# نمونه Front-end:
react, javascript, typescript, css, html, tailwind, next.js, git, figma, responsive design

# نمونه Data Analyst:
python, sql, excel, power bi, tableau, pandas, statistics, data visualization

# نمونه DevOps:
docker, kubernetes, aws, terraform, ci/cd, linux, ansible, jenkins, monitoring

# نمونه Graphic Designer:
figma, photoshop, illustrator, after effects, branding, typography, ui design
```

اگه `USER_SKILLS` رو ست نکنی، ربات از مهارت‌های پیش‌فرض (SEO) استفاده می‌کنه.

---

### ۳. کلمات ممنوعه (`BLACKLIST_KEYWORDS`) — خط ~۱۴۲

آگهی‌هایی که این کلمات رو دارن **حذف** میشن. بر اساس فیلد خودت تغییرش بده:

```python
# نمونه عمومی (برای همه فیلدها مناسبه):
BLACKLIST_KEYWORDS = [
    "us residents only", "must reside in us", "must be located in us",
    "must be based in the us", "must be authorized to work in the us",
    "native english speaker only",
    "10+ years", "8+ years", "7+ years",
    "senior", "lead", "staff", "principal", "director", "head of", "vp of",
]

# نمونه Junior Developer (فیلتر پوزیشن‌های سنیور):
BLACKLIST_KEYWORDS = [
    "us residents only", "must reside in us",
    "must be authorized to work in the us",
    "senior developer", "staff engineer", "principal engineer",
    "lead developer", "architect", "director", "vp of",
    "10+ years", "8+ years", "7+ years", "5+ years",
]
```

---

### ۴. کلمات تقویت‌کننده (`BOOST_KEYWORDS`) — خط ~۱۵۳

آگهی‌هایی که این کلمات رو دارن **امتیاز بیشتر** می‌گیرن (عدد = امتیاز اضافه):

```python
# نمونه SEO (پیش‌فرض):
BOOST_KEYWORDS = {
    "technical seo": 20, "python": 18, "wordpress": 15,
    "junior": 18, "entry level": 15, "associate": 12,
    "seo specialist": 12, "seo editor": 12, "content editor": 10,
    "on-page": 10, "part-time": 8, "contract": 5,
    "remote-first": 8, "async": 5, "flexible": 4,
}

# نمونه Front-end Developer:
BOOST_KEYWORDS = {
    "react": 20, "next.js": 18, "typescript": 15,
    "junior": 18, "entry level": 15, "associate": 12,
    "frontend": 12, "front-end": 12, "ui developer": 10,
    "tailwind": 10, "vue": 8, "part-time": 8, "contract": 5,
    "remote-first": 8, "async": 5, "flexible": 4,
}

# نمونه Data Analyst:
BOOST_KEYWORDS = {
    "python": 20, "sql": 18, "power bi": 15, "tableau": 15,
    "junior": 18, "entry level": 15, "associate": 12,
    "data analyst": 12, "business intelligence": 10,
    "excel": 8, "part-time": 8, "contract": 5,
    "remote-first": 8, "async": 5, "flexible": 4,
}
```

---

### 🔄 خلاصه سریع

| چی رو تغییر بدم؟ | کجا؟ | نیاز به تغییر کد؟ |
|---|---|---|
| مهارت‌ها | GitHub Secret → `USER_SKILLS` | ❌ نه |
| عبارات جستجو | `bot.py` → `JSEARCH_QUERIES` | ✅ بله |
| فیلتر آگهی‌های نامرتبط | `bot.py` → `BLACKLIST_KEYWORDS` | ✅ بله |
| اولویت آگهی‌ها | `bot.py` → `BOOST_KEYWORDS` | ✅ بله |
| رزومه برای AI | GitHub Secret → `USER_RESUME` | ❌ نه |

> 🎁 **نکته:** اگه فقط `USER_SKILLS` رو ست کنی و بقیه رو همین‌جوری بذاری، ربات بازم کار می‌کنه ولی نتایج بهتری می‌ده اگه همه ۴ مورد رو تغییر بدی.

---

## ⚙️ تنظیمات پیشرفته (اختیاری — برای حرفه‌ای‌ها)

اگه ربات رو راه انداختی و حالا می‌خوای خفن‌ترش کنی:

---

### 🧠 ۱. هوش مصنوعی برای نوشتن Cover Letter

ربات می‌تونه با AI برای هر آگهی یه **Cover Letter اختصاصی** بنویسه تا شانس استخدامت بیشتر بشه.

**راه‌اندازی:**
1. یه کلید API **رایگان** از [Google Gemini](https://aistudio.google.com/apikey) بگیر
2. فایل `setup_wizard.html` رو باز کن
3. بخش **هوش مصنوعی** رو فعال کن → ارائه‌دهنده رو **Gemini** بذار → کلیدت رو وارد کن
4. دوباره Secrets رو تولید کن و توی GitHub آپدیت کن

**نکته مهم (ساخت Telegraph Token):**
برای اینکه ربات بتونه متن های طولانی Cover Letter رو به شکل یه لینک تمیز و خوانا برات بفرسته، حتما به این توکن نیاز داری. گرفتنش فقط ۱۰ ثانیه زمان می بره:

1. لینک زیر رو کپی کن و توی مرورگرت (مثل کروم) باز کن:
   `https://api.telegra.ph/createAccount?short_name=SEOJobBot&author_name=SEO`
2. یه صفحه سفید باز میشه که یه سری کد توشه. خروجی شبیه اینه:
   ```json
   {"ok":true,"result":{"short_name":"SEOJobBot","author_name":"SEO","author_url":"","access_token":"8a4b323f36c7cffb5c8332ca7d3dcwa2215cf979acd7403c2f34d6122345","auth_url":"..."}}
از بین این متن ها، فقط عبارتی که جلوی access_token نوشته شده رو لازم داریم (توی مثال بالا میشه 8a4b323f36c7cffb5c8332ca7d3dcwa2215cf979acd7403c2f34d6122345).

این کد رو کپی کن و توی فایل setup_wizard.html (بخش Telegraph Token) وارد کن.

**می‌خوای از مدل‌های قوی‌تر استفاده کنی؟**
با [TokenLB](https://tokenlb.net/sign-up?aff=yNLD) می‌تونی از Claude و GPT استفاده کنی. توی ویزارد ارائه‌دهنده رو بذار روی **TokenLB** و کلیدت رو وارد کن.

---

### 👤 ۲. شخصی‌سازی Cover Letter

توی فایل ویزارد یه بخش هست برای **مهارت‌ها و رزومه** شما.

مهارت‌های خودت رو بنویس (مثلاً: `react, typescript, next.js, tailwind`)

AI اینا رو می‌خونه و تو Cover Letter دقیقاً میگه که تو به درد همون کار می‌خوری!

---

### 📊 ۳. ذخیره آگهی‌ها تو Google Sheets (تاریخچه کامل)

اگه می‌خوای همه آگهی‌ها رو تو یه شیت گوگل ذخیره کنی و دسترسی راحت‌تر داشته باشی:

1. برو به [Google Cloud Console](https://console.cloud.google.com)
2. یه پروژه جدید بساز (اسمی که بخوای)
3. **APIs & Services** → **Enable APIs** → سرچ کن و فعال کن:
   - **Google Sheets API**
   - **Google Drive API**
4. برگرد به **Credentials** → **Create Credentials** → **Service Account**
5. یه اسم بده → **Create and Continue** → نقش رو **Editor** بذار → **Done**
6. روی Service Account ساخته‌شده کلیک کن → تب **Keys** → **Add Key** → **Create new key** → **JSON**
7. فایل JSON دانلود میشه — **محتواش رو کپی کن** (کل متن)
8. یه [Google Sheet جدید](https://sheets.google.com) بساز
9. دکمه **Share** رو بزن → ایمیل Service Account رو (که توی JSON هست) اضافه کن → نقش **Editor** بده
10. از URL شیت، بخش بعد از `/d/` تا قبل از `/edit` رو کپی کن (این ID شیته)
11. توی GitHub Secrets اضافه کن:
    - `GSHEET_CREDENTIALS` = کل محتوای فایل JSON
    - `GSHEET_ID` = ID شیت

از این به بعد، ربات همه آگهی‌ها رو توی شیت هم ذخیره می‌کنه.

---

### ۲. جایگزین بخش منابع بیشتر (Cloudflare Worker)

```markdown
### ☁️ ۴. اضافه کردن منابع بیشتر (Cloudflare Worker)

سایت هایی مثل **We Work Remotely** و **Remote OK** برای اینکه ربات بتونه اگهی هاشون رو بخونه، نیاز به یه واسطه دارن. کلادفلر این واسطه رو کاملا رایگان بهت میده. اگه هیچی از کدنویسی نمی دونی، فقط مو به مو این مراحل رو انجام بده:

1. یه اکانت رایگان تو [Cloudflare](https://dash.cloudflare.com) بساز.
2. از منوی سمت چپ اول روی **Build** و بعد **Workers and Pages** کلیک کن.
3. وسط صفحه دکمه ابی **Create application** رو بزن.
4. دکمه **Create Worker** (یا Start with Hello World) رو بزن.
5. یه اسم برای پروژه انتخاب کن و **Deploy** رو بزن.
6. تو صفحه جدید، بالا سمت چپ روی **Edit code** کلیک کن.
7. کدهای پیش فرض وسط صفحه رو انتخاب کن و **کامل پاک کن**.
8. فایل `cf_worker.js` (توی همین ریپازیتوری) رو باز کن، کل متنش رو کپی کن و همونجا Paste کن.
9. بالا سمت راست دکمه **Deploy** رو بزن تا ذخیره بشه.
10. برگرد به صفحه قبلی پروژه؛ سمت راست یه لینک بهت داده (شبیه `https://dark-shadow-430b.sadidi1434.workers.dev/`). این لینک رو کپی کن.
11. این لینک رو توی فایل ویزارد (بخش ادرس Worker) وارد کن و Secrets رو توی گیت هاب اپدیت کن.
---

## ❓ مشکلات رایج

| مشکل | راه‌حل |
|------|--------|
| پیام نمیاد | Actions → آخرین run → لاگ رو بخون |
| Token not set | Secret رو چک کن — اسمش دقیقاً درست باشه |
| آگهی کم میاد | طبیعیه! ممکنه بعضی روزها آگهی جدید نباشه |
| Cover Letter نداره | `AI_PROVIDER` + `AI_API_KEY` + `TELEGRAPH_TOKEN` ست شدن؟ |
| خطای AI | مشکل از سمت سرور ارائه‌دهنده — چند ساعت بعد خودش درست میشه |
| آگهی‌های نامرتبط میاد | `BOOST_KEYWORDS` و `BLACKLIST_KEYWORDS` رو برای فیلد خودت تنظیم کن |

---

## 📄 لایسنس

MIT — هر کاری می‌خوای باهاش بکن ✌️
