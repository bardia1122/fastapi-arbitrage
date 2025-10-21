from prometheus_client import Counter, Histogram, Gauge, CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response

EXCHANGE_LATENCY = Histogram(
    "exchange_response_time_seconds",
    "زمان پاسخ‌دهی درخواست‌ها به هر صرافی (ثانیه)",
    ["exchange"],
)

EXCHANGE_REQUESTS = Counter(
    "exchange_requests_total",
    "تعداد کل درخواست‌ها به هر صرافی، تفکیک‌شده بر اساس وضعیت (ok/error)",
    ["exchange", "status"],
)

ARBITRAGE_EVENTS = Counter(
    "arbitrage_events_total",
    "تعداد فرصت‌های آربیتراژ کشف‌شده در هر جفت ارز",
    ["symbol"],
)

LAST_DIFF = Gauge(
    "arbitrage_last_diff_percent",
    "آخرین درصد اختلاف مشاهده‌شده بین صرافی‌ها برای هر جفت ارز",
    ["symbol"],
)

ARBITRAGE_VALUE = Gauge(
    "arbitrage_last_diff_value",
    "مقدار اختلاف قیمتی آخرین آربیتراژ کشف‌شده برای هر جفت ارز",
    ["symbol"],
)

def metrics_endpoint():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
