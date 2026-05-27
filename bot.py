import requests
import os
import html
import json
import time
import logging
from datetime import datetime, timezone
from pathlib import Path

# ─── Optional: Google Sheets ──────────────────────────────────────────────────
try:
    import gspread
    from google.oauth2.service_account import Credentials
    SHEETS_AVAILABLE = True
except ImportError:
    SHEETS_AVAILABLE = False

# ─── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# ─── Config ───────────────────────────────────────────────────────────────────
RAPIDAPI_KEY       = os.environ["RAPIDAPI_KEY"]
TELEGRAM_TOKEN     = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID   = os.environ["TELEGRAM_CHAT_ID"]
GSHEET_CREDENTIALS = os.environ.get("GSHEET_CREDENTIALS", "")   # JSON string
GSHEET_ID          = os.environ.get("GSHEET_ID", "")
GSHEET_SHEET_NAME  = "Jobs"

SEEN_JOBS_FILE    = Path("seen_jobs.txt")
MAX_SEEN_JOBS     = 2000   # حداکثر تعداد ID ذخیره شده (جلوگیری از بزرگ شدن فایل)
MAX_JOBS_PER_RUN  = 15     # حداکثر آگهی ارسالی در هر اجرا

# ─── کلمات جستجو ──────────────────────────────────────────────────────────────
SEARCH_QUERIES = [
    "Junior SEO remote",
    "Technical SEO remote",
    "SEO Content Editor remote",
    "SEO Python remote",
    "WordPress SEO Specialist remote",
]

# ─── کلمات ممنوعه (Blacklist) ──────────────────────────────────────────────────
BLACKLIST_KEYWORDS = [
    "us residents only",
    "must reside in us",
    "must be located in the us",
    "must be based in",
    "senior",
    "director",
    "agency",
    "full stack",
    "fullstack",
]

# ══════════════════════════════════════════════════════════════════════════════
# حافظه دائمی — seen_jobs.txt
# ══════════════════════════════════════════════════════════════════════════════

def load_seen_jobs() -> set:
    """بارگذاری ID های قبلاً ارسال‌شده از فایل کش"""
    if SEEN_JOBS_FILE.exists():
        ids = set(line.strip() for line in SEEN_JOBS_FILE.read_text().splitlines() if line.strip())
        log.info(f"Loaded {len(ids)} seen job IDs from cache")
        return ids
    log.info("No cache file found — starting fresh")
    return set()


def save_seen_jobs(seen: set) -> None:
    """ذخیره ID ها — با محدودیت MAX_SEEN_JOBS برای جلوگیری از بزرگ شدن فایل"""
    ids_list = list(seen)
    if len(ids_list) > MAX_SEEN_JOBS:
        ids_list = ids_list[-MAX_SEEN_JOBS:]   # فقط جدیدترین‌ها نگه داشته میشه
    SEEN_JOBS_FILE.write_text("\n".join(ids_list))
    log.info(f"Saved {len(ids_list)} job IDs to cache")


# ══════════════════════════════════════════════════════════════════════════════
# JSearch API
# ══════════════════════════════════════════════════════════════════════════════

def search_jobs(query: str, retries: int = 3) -> list:
    """جستجو با retry خودکار و مدیریت rate limit"""
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key":  RAPIDAPI_KEY,
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
    }
    params = {
        "query":          query,
        "num_pages":      "1",
        "date_posted":    "today",
        "work_from_home": "true",
    }

    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=20)

            if resp.status_code == 429:
                log.warning("Rate limit hit — waiting 60s before retry...")
                time.sleep(60)
                continue

            if resp.status_code == 403:
                log.error("API key invalid or not subscribed (403)")
                return []

            resp.raise_for_status()
            data = resp.json()

            if data.get("status") != "OK":
                log.warning(f"API non-OK for '{query}': {data.get('error')}")
                return []

            return data.get("data", [])

        except requests.exceptions.Timeout:
            log.warning(f"Timeout on attempt {attempt}/{retries} for '{query}'")
        except requests.exceptions.JSONDecodeError:
            log.error(f"Invalid JSON response for '{query}'")
            return []
        except requests.exceptions.RequestException as e:
            log.error(f"Request error (attempt {attempt}/{retries}): {e}")

        if attempt < retries:
            wait = 5 * attempt
            log.info(f"Waiting {wait}s before retry...")
            time.sleep(wait)

    log.error(f"All {retries} attempts failed for '{query}'")
    return []


# ══════════════════════════════════════════════════════════════════════════════
# فیلتر Blacklist
# ══════════════════════════════════════════════════════════════════════════════

def is_blacklisted(job: dict) -> bool:
    description = (job.get("job_description") or "").lower()
    title       = (job.get("job_title") or "").lower()
    combined    = f"{title} {description}"

    for keyword in BLACKLIST_KEYWORDS:
        if keyword.lower() in combined:
            log.info(f"  ⛔ Blacklisted '{job.get('job_title')}' — matched: '{keyword}'")
            return True
    return False


# ══════════════════════════════════════════════════════════════════════════════
# Telegram
# ══════════════════════════════════════════════════════════════════════════════

def send_telegram(text: str) -> bool:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id":                  TELEGRAM_CHAT_ID,
        "text":                     text,
        "parse_mode":               "HTML",
        "disable_web_page_preview": True,
    }
    try:
        resp = requests.post(url, json=payload, timeout=15)
        if not resp.ok:
            log.error(f"Telegram error {resp.status_code}: {resp.text[:300]}")
            return False
        return True
    except Exception as e:
        log.error(f"Telegram send exception: {e}")
        return False


def extract_salary(job: dict) -> str:
    """استخراج حقوق از فیلدهای مختلف API"""
    # اول فیلد آماده رو چک میکنیم
    if job.get("job_salary_string"):
        return job["job_salary_string"]

    # بعد min/max رو بررسی میکنیم
    min_s  = job.get("job_min_salary")
    max_s  = job.get("job_max_salary")
    period = (job.get("job_salary_period") or "").lower()

    period_map = {"year": "/yr", "month": "/mo", "hour": "/hr", "week": "/wk"}
    period_label = period_map.get(period, f"/{period}" if period else "")

    if min_s and max_s:
        return f"${int(min_s):,} – ${int(max_s):,}{period_label}"
    if min_s:
        return f"${int(min_s):,}+{period_label}"
    return ""


def format_job(job: dict) -> str:
    """ساخت متن پیام تلگرام با html.escape روی تمام متن‌ها"""
    title    = html.escape(job.get("job_title")    or "بدون عنوان")
    company  = html.escape(job.get("employer_name") or "نامشخص")
    city     = html.escape(job.get("job_city")     or "")
    country  = html.escape(job.get("job_country")  or "")
    location = f"{city}, {country}".strip(", ") or "Remote"
    source   = html.escape(job.get("job_publisher") or "")
    link     = job.get("job_apply_link") or job.get("job_google_link") or ""
    salary   = extract_salary(job)

    lines = [
        f"💼 <b>{title}</b>",
        f"🏢 {company}",
        f"📍 {location}",
    ]

    if salary:
        lines.append(f"💰 <b>{html.escape(salary)}</b>")   # برجسته و مجزا

    if source:
        lines.append(f"🌐 {source}")

    if link:
        lines.append(f'🔗 <a href="{link}">Apply Now</a>')

    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# Google Sheets (اختیاری)
# ══════════════════════════════════════════════════════════════════════════════

def get_sheets_client():
    if not SHEETS_AVAILABLE:
        log.info("gspread not installed — skipping Google Sheets")
        return None
    if not GSHEET_CREDENTIALS or not GSHEET_ID:
        log.info("GSHEET_CREDENTIALS or GSHEET_ID not set — skipping Google Sheets")
        return None
    try:
        creds_dict = json.loads(GSHEET_CREDENTIALS)
        scopes     = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds  = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(creds)
        log.info("Google Sheets connected ✅")
        return client
    except json.JSONDecodeError:
        log.error("GSHEET_CREDENTIALS is not valid JSON")
    except Exception as e:
        log.error(f"Google Sheets auth error: {e}")
    return None


def ensure_sheet_headers(client) -> None:
    if client is None:
        return
    try:
        sheet = client.open_by_key(GSHEET_ID).worksheet(GSHEET_SHEET_NAME)
        first_row = sheet.row_values(1)
        if not first_row:
            headers = ["Job Title", "Company", "Apply Link", "Posted Date",
                       "City", "Country", "Salary", "Saved At (UTC)"]
            sheet.insert_row(headers, 1)
            log.info("Sheet headers created")
    except Exception as e:
        log.error(f"Sheet header check error: {e}")


def append_to_sheet(client, job: dict) -> None:
    if client is None:
        return
    try:
        sheet = client.open_by_key(GSHEET_ID).worksheet(GSHEET_SHEET_NAME)
        posted = (job.get("job_posted_at_datetime_utc") or "")[:10]
        row = [
            job.get("job_title", ""),
            job.get("employer_name", ""),
            job.get("job_apply_link") or job.get("job_google_link") or "",
            posted,
            job.get("job_city", ""),
            job.get("job_country", ""),
            extract_salary(job),
            datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
        ]
        sheet.append_row(row, value_input_option="USER_ENTERED")
    except Exception as e:
        log.error(f"Sheet append error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    log.info(f"═══ Bot started at {now} ═══")

    seen_jobs     = load_seen_jobs()
    sheets_client = get_sheets_client()
    ensure_sheet_headers(sheets_client)

    new_jobs      = []
    blacklisted   = 0
    already_seen  = 0
    errors        = 0

    for query in SEARCH_QUERIES:
        log.info(f"Searching: '{query}'")
        try:
            jobs = search_jobs(query)
            log.info(f"  → {len(jobs)} raw results")

            for job in jobs:
                try:
                    job_id = job.get("job_id") or job.get("job_apply_link") or ""
                    if not job_id:
                        continue

                    if job_id in seen_jobs:
                        already_seen += 1
                        continue

                    seen_jobs.add(job_id)   # همیشه ثبت میکنیم، حتی blacklisted ها

                    if is_blacklisted(job):
                        blacklisted += 1
                        continue

                    new_jobs.append(job)

                except Exception as e:
                    log.error(f"  Error processing job item: {e}")
                    errors += 1
                    continue

        except Exception as e:
            log.error(f"Error in query '{query}': {e}")
            errors += 1
            continue

        time.sleep(1.5)   # احترام به rate limit

    # حذف تکراری‌ها (یه آگهی ممکنه در چند query باشه)
    dedup_seen = set()
    unique_jobs = []
    for job in new_jobs:
        jid = job.get("job_id", "")
        if jid and jid not in dedup_seen:
            dedup_seen.add(jid)
            unique_jobs.append(job)

    log.info(f"Summary → new: {len(unique_jobs)} | blacklisted: {blacklisted} | already seen: {already_seen} | errors: {errors}")

    # ─── ارسال به تلگرام ───────────────────────────────────────────────────
    if not unique_jobs:
        send_telegram(
            f"🔍 <b>گزارش روزانه</b>\n"
            f"📅 {now}\n\n"
            f"✅ آگهی جدیدی امروز پیدا نشد.\n"
            f"⛔ فیلتر شده: {blacklisted} | 🔁 تکراری: {already_seen}"
        )
        save_seen_jobs(seen_jobs)
        return

    # پیام هدر
    send_telegram(
        f"🔍 <b>آگهی‌های شغلی جدید</b>\n"
        f"📅 {now}\n"
        f"📊 {len(unique_jobs)} آگهی جدید | ⛔ {blacklisted} فیلتر شد\n"
        f"➖➖➖➖➖➖➖➖"
    )
    time.sleep(1)

    sent = 0
    for job in unique_jobs[:MAX_JOBS_PER_RUN]:
        try:
            msg = format_job(job)
            if send_telegram(msg):
                sent += 1
                append_to_sheet(sheets_client, job)
            time.sleep(0.8)   # جلوگیری از flood limit تلگرام
        except Exception as e:
            log.error(f"Error sending job to Telegram: {e}")
            continue

    save_seen_jobs(seen_jobs)
    log.info(f"═══ Done. Sent {sent}/{len(unique_jobs)} jobs ═══")


if __name__ == "__main__":
    main()
