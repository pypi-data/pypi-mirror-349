
COMMON_FIELD_MAPPING = {
    "datetime": "time",
    "bid": "bid",
    "bidsize": "bidSize",
    "ask": "ask",
    "asksize": "askSize",
    "last": "last",
    "lastsize": "lastSize",
    "volume": "volume"
}

OPT_FOP_BASE_MAPPING = {
    "iv": ("impliedVolatility", "lastGreeks.implieVol"),
    "underlying": "lastGreeks.undPrice",
    "oi": ("callOpenInterest", "putOpenInterest", "futuresOpenInterest")
}

OPT_FOP_MODELGREEKS_MAPPING = {
    "price": "modelGreeks.optPrice",
    "dividend": "modelGreeks.pvDividend",
    "imp_vol": "modelGreeks.impliedVol",
    "delta": "modelGreeks.delta",
    "gamma": "modelGreeks.gamma",
    "vega": "modelGreeks.vega",
    "theta": "modelGreeks.theta"
}

OPT_FOP_LASTGREEKS_MAPPING = {
    "last_price": "lastGreeks.optPrice",
    "last_dividend": "lastGreeks.pvDividend",
    "last_imp_vol": "lastGreeks.impliedVol",
    "last_delta": ".lastGreeks.delta",
    "last_gamma": "lastGreeks.gamma",
    "last_vega": "lastGreeks.vega",
    "last_theta": "lastGreeks.theta"
}

OPT_FOP_BIDGREEKS_MAPPING = {
    "bid_price": "bidGreeks.optPrice",
    "bid_dividend": "bidGreeks.pvDividend",
    "bid_imp_vol": "bidGreeks.impliedVol",
    "bid_delta": "bidGreeks.delta",
    "bid_gamma": "bidGreeks.gamma",
    "bid_vega": "bidGreeks.vega",
    "bid_theta": "bidGreeks.theta"
}

OPT_FOP_ASKGREEKS_MAPPING = {
    "ask_price": "askGreeks.optPrice",
    "ask_dividend": "askGreeks.pvDividend",
    "ask_imp_vol": "askGreeks.impliedVol",
    "ask_delta": "askGreeks.delta",
    "ask_gamma": "askGreeks.gamma",
    "ask_vega": "askGreeks.vega",
    "ask_theta": "askGreeks.theta"
}