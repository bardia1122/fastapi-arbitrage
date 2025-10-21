def normalize_for_wallex(symbol: str) -> str:
    base, quote = symbol.replace("_", "-").split("-")
    quote = "TMN" if quote.upper() in {"IRT", "TMN"} else quote.upper()
    return f"{base.upper()}{quote}"

def normalize_for_nobitex(symbol: str) -> str:
    base, quote = symbol.replace("_", "-").split("-")
    return f"{base.upper()}{quote.upper()}"
