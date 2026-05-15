import yfinance as yf
import pandas as pd
import numpy as np
import warnings
import requests
import urllib.parse
import xml.etree.ElementTree as ET
import mplfinance as mpf
import matplotlib
matplotlib.use('Agg')  # 🔥 WAJIB
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
import cv2
import re
import time
import datetime
import asyncio
import base64
import logging
logging.getLogger("yfinance").setLevel(logging.CRITICAL)
import os
os.system("apt update")
os.system("apt install -y tesseract-ocr")
os.system("pip install --no-cache-dir mplfinance matplotlib")
os.system("pip install --no-cache-dir python-telegram-bot[job-queue]")
os.system("pip install --no-cache-dir pytesseract pillow")
os.system("pip install --no-cache-dir opencv-python-headless")
os.system("pip install --no-cache-dir python-dotenv")
if not os.path.exists("temp"):
    os.makedirs("temp")


from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange, BollingerBands

from PIL import Image, ImageFilter

from telegram import (
    Update
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=5)


warnings.filterwarnings("ignore")

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

CACHE = {}
CACHE_TIME = {}

USER_MODE = {}
CHAT_HISTORY = {}
BOT_AI_NAME = {}
# =========================
# WATCHLIST
# =========================
WATCHLIST = ["AALI", "ABBA", "ABDA", "ABMM", "ACES", "ACST", "ADES", "ADHI", "AISA", "AKKU", "AKPI", "AKRA", "AKSI", "ALDO", "ALKA", "ALMI", "ALTO", "AMAG", "AMFG", "AMIN", "AMRT", "ANJT", "ANTM", "APEX", "APIC", "APII", "APLI", "APLN", "ARGO", "ARII", "ARNA", "ARTA", "ARTI", "ARTO", "ASBI", "ASDM", "ASGR", "ASII", "ASJT", "ASMI", "ASRI", "ASRM", "ASSA", "ATIC", "AUTO", "BABP", "BACA", "BAJA", "BALI", "BAPA", "BATA", "BAYU", "BBCA", "BBHI", "BBKP", "BBLD", "BBMD", "BBNI", "BBRI", "BBRM", "BBTN", "BBYB", "BCAP", "BCIC", "BCIP", "BDMN", "BEKS", "BEST", "BFIN", "BGTG", "BHIT", "BIKA", "BIMA", "BINA", "BIPI", "BIPP", "BIRD", "BISI", "BJBR", "BJTM", "BKDP", "BKSL", "BKSW", "BLTA", "BLTZ", "BMAS", "BMRI", "BMSR", "BMTR", "BNBA", "BNBR", "BNGA", "BNII", "BNLI", "BOLT", "BPFI", "BPII", "BRAM", "BRMS", "BRNA", "BRPT", "BSDE", "BSIM", "BSSR", "BSWD", "BTEK", "BTEL", "BTON", "BTPN", "BUDI", "BUKK", "BULL", "BUMI", "BUVA", "BVIC", "BWPT", "BYAN", "CANI", "CASS", "CEKA", "CENT", "CFIN", "CINT", "CITA", "CLPI", "CMNP", "CMPP", "CNKO", "CNTX", "COWL", "CPIN", "CPRO", "CSAP", "CTBN", "CTRA", "CTTH", "DART", "DEFI", "DEWA", "DGIK", "DILD", "DKFT", "DLTA", "DMAS", "DNAR", "DNET", "DOID", "DPNS", "DSFI", "DSNG", "DSSA", "DUTI", "DVLA", "DYAN", "ECII", "EKAD", "ELSA", "ELTY", "EMDE", "EMTK", "ENRG", "EPMT", "ERAA", "ERTX", "ESSA", "ESTI", "ETWA", "EXCL", "FAST", "FASW", "FISH", "FMII", "FORU", "FPNI", "GAMA", "GDST", "GDYR", "GEMA", "GEMS", "GGRM", "GIAA", "GJTL", "GLOB", "GMTD", "GOLD", "GOLL", "GPRA", "GSMF", "GTBO", "GWSA", "GZCO", "HADE", "HDFA", "HERO", "HEXA", "HITS", "HMSP", "HOME", "HOTL", "HRUM", "IATA", "IBFN", "IBST", "ICBP", "ICON", "IGAR", "IIKP", "IKAI", "IKBI", "IMAS", "IMJS", "IMPC", "INAF", "INAI", "INCI", "INCO", "INDF", "INDR", "INDS", "INDX", "INDY", "INKP", "INPC", "INPP", "INRU", "INTA", "INTD", "INTP", "IPOL", "ISAT", "ISSP", "ITMA", "ITMG", "JAWA", "JECC", "JIHD", "JKON", "JPFA", "JRPT", "JSMR", "JSPT", "JTPE", "KAEF", "KARW", "KBLI", "KBLM", "KBLV", "KBRI", "KDSI", "KIAS", "KICI", "KIJA", "KKGI", "KLBF", "KOBX", "KOIN", "KONI", "KOPI", "KPIG", "KRAS", "KREN", "LAPD", "LCGP", "LEAD", "LINK", "LION", "LMAS", "LMPI", "LMSH", "LPCK", "LPGI", "LPIN", "LPKR", "LPLI", "LPPF", "LPPS", "LRNA", "LSIP", "LTLS", "MAGP", "MAIN", "MAPI", "MAYA", "MBAP", "MBSS", "MBTO", "MCOR", "MDIA", "MDKA", "MDLN", "MDRN", "MEDC", "MEGA", "MERK", "META", "MFMI", "MGNA", "MICE", "MIDI", "MIKA", "MIRA", "MITI", "MKPI", "MLBI", "MLIA", "MLPL", "MLPT", "MMLP", "MNCN", "MPMX", "MPPA", "MRAT", "MREI", "MSKY", "MTDL", "MTFN", "MTLA", "MTSM", "MYOH", "MYOR", "MYTX", "NELY", "NIKL", "NIRO", "NISP", "NOBU", "NRCA", "OCAP", "OKAS", "OMRE", "PADI", "PALM", "PANR", "PANS", "PBRX", "PDES", "PEGE", "PGAS", "PGLI", "PICO", "PJAA", "PKPK", "PLAS", "PLIN", "PNBN", "PNBS", "PNIN", "PNLF", "PSAB", "PSDN", "PSKT", "PTBA", "PTIS", "PTPP", "PTRO", "PTSN", "PTSP", "PUDP", "PWON", "PYFA", "RAJA", "RALS", "RANC", "RBMS", "RDTX", "RELI", "RICY", "RIGS", "RIMO", "RODA", "ROTI", "RUIS", "SAFE", "SAME", "SCCO", "SCMA", "SCPI", "SDMU", "SDPC", "SDRA", "SGRO", "SHID", "SIDO", "SILO", "SIMA", "SIMP", "SIPD", "SKBM", "SKLT", "SKYB", "SMAR", "SMBR", "SMCB", "SMDM", "SMDR", "SMGR", "SMMA", "SMMT", "SMRA", "SMRU", "SMSM", "SOCI", "SONA", "SPMA", "SQMI", "SRAJ", "SRIL", "SRSN", "SRTG", "SSIA", "SSMS", "SSTM", "STAR", "STTP", "SUGI", "SULI", "SUPR", "TALF", "TARA", "TAXI", "TBIG", "TBLA", "TBMS", "TCID", "TELE", "TFCO", "TGKA", "TIFA", "TINS", "TIRA", "TIRT", "TKIM", "TLKM", "TMAS", "TMPO", "TOBA", "TOTL", "TOTO", "TOWR", "TPIA", "TPMA", "TRAM", "TRIL", "TRIM", "TRIO", "TRIS", "TRST", "TRUS", "TSPC", "ULTJ", "UNIC", "UNIT", "UNSP", "UNTR", "UNVR", "VICO", "VINS", "VIVA", "VOKS", "VRNA", "WAPO", "WEHA", "WICO", "WIIM", "WIKA", "WINS", "WOMF", "WSKT", "WTON", "YPAS", "YULE", "ZBRA", "SHIP", "CASA", "DAYA", "DPUM", "IDPR", "JGLE", "KINO", "MARI", "MKNT", "MTRA", "OASA", "POWR", "INCF", "WSBP", "PBSA", "PRDA", "BOGA", "BRIS", "PORT", "CARS", "MINA", "CLEO", "TAMU", "CSIS", "TGRA", "FIRE", "TOPS", "KMTR", "ARMY", "MAPB", "WOOD", "HRTA", "MABA", "HOKI", "MPOW", "MARK", "NASA", "MDKI", "BELL", "KIOS", "GMFI", "MTWI", "ZINC", "MCAS", "PPRE", "WEGE", "PSSI", "MORA", "DWGL", "PBID", "JMAS", "CAMP", "IPCM", "PCAR", "LCKM", "BOSS", "HELI", "JSKY", "INPS", "GHON", "TDPM", "DFAM", "NICK", "BTPS", "SPTO", "PRIM", "HEAL", "TRUK", "PZZA", "TUGU", "MSIN", "SWAT", "TNCA", "MAPA", "TCPI", "IPCC", "RISE", "BPTR", "POLL", "NFCX", "MGRO", "NUSA", "FILM", "ANDI", "LAND", "MOLI", "PANI", "DIGI", "CITY", "SAPX", "SURE", "HKMU", "MPRO", "DUCK", "GOOD", "SKRN", "YELO", "CAKK", "SATU", "SOSS", "DEAL", "POLA", "DIVA", "LUCK", "URBN", "SOTS", "ZONE", "PEHA", "FOOD", "BEEF", "POLI", "CLAY", "NATO", "JAYA", "COCO", "MTPS", "CPRI", "HRME", "POSA", "JAST", "FITT", "BOLA", "CCSI", "SFAN", "POLU", "KJEN", "KAYU", "ITIC", "PAMG", "IPTV", "BLUE", "ENVY", "EAST", "LIFE", "FUJI", "KOTA", "INOV", "ARKA", "SMKL", "HDIT", "KEEN", "BAPI", "TFAS", "GGRP", "OPMS", "NZIA", "SLIS", "PURE", "IRRA", "DMMX", "SINI", "WOWS", "ESIP", "TEBE", "KEJU", "PSGO", "AGAR", "IFSH", "REAL", "IFII", "PMJS", "UCID", "GLVA", "PGJO", "AMAR", "CSRA", "INDO", "AMOR", "TRIN", "DMND", "PURA", "PTPW", "TAMA", "IKAN", "SAMF", "SBAT", "KBAG", "CBMF", "RONY", "CSMI", "BBSS", "BHAT", "CASH", "TECH", "EPAC", "UANG", "PGUN", "SOFA", "PPGL", "TOYS", "SGER", "TRJA", "PNGO", "SCNP", "BBSI", "KMDS", "PURI", "SOHO", "HOMI", "ROCK", "ENZO", "PLAN", "PTDU", "ATAP", "VICI", "PMMP", "BANK", "WMUU", "EDGE", "UNIQ", "BEBS", "SNLK", "ZYRX", "LFLO", "FIMP", "TAPG", "NPGF", "LUCY", "ADCP", "HOPE", "MGLV", "TRUE", "LABA", "ARCI", "IPAC", "MASB", "BMHS", "FLMC", "NICL", "UVCR", "BUKA", "HAIS", "OILS", "GPSO", "MCOL", "RSGK", "RUNS", "SBMA", "CMNT", "GTSI", "IDEA", "KUAS", "BOBA", "MTEL", "DEPO", "BINO", "CMRY", "WGSH", "TAYS", "WMPP", "RMKE", "OBMD", "AVIA", "IPPE", "NASI", "BSML", "DRMA", "ADMR", "SEMA", "ASLC", "NETV", "BAUT", "ENAK", "NTBK", "SMKM", "STAA", "NANO", "BIKE", "WIRG", "SICO", "GOTO", "TLDN", "MTMH", "WINR", "IBOS", "OLIV", "ASHA", "SWID", "TRGU", "ARKO", "CHEM", "DEWI", "AXIO", "KRYA", "HATM", "RCCC", "GULA", "JARR", "AMMS", "RAFI", "KKES", "ELPI", "EURO", "KLIN", "TOOL", "BUAH", "CRAB", "MEDS", "COAL", "PRAY", "CBUT", "BELI", "MKTR", "OMED", "BSBK", "PDPP", "KDTN", "ZATA", "NINE", "MMIX", "PADA", "ISAP", "VTNY", "SOUL", "ELIT", "BEER", "CBPE", "SUNI", "CBRE", "WINE", "BMBL", "PEVE", "LAJU", "FWCT", "NAYZ", "IRSX", "PACK", "VAST", "CHIP", "HALO", "KING", "PGEO", "FUTR", "HILL", "BDKR", "PTMP", "SAGE", "TRON", "CUAN", "NSSS", "GTRA", "HAJJ", "JATI", "TYRE", "MPXL", "SMIL", "KLAS", "MAXI", "VKTR", "RELF", "AMMN", "CRSN", "GRPM", "WIDI", "TGUK", "INET", "MAHA", "RMKO", "CNMA", "FOLK", "HBAT", "GRIA", "PPRI", "ERAL", "CYBR", "MUTU", "LMAX", "HUMI", "MSIE", "RSCH", "BABY", "AEGS", "IOTF", "KOCI", "PTPS", "BREN", "STRK", "KOKA", "LOPI", "UDNG", "RGAS", "MSTI", "IKPM", "AYAM", "SURI", "ASLI", "GRPH", "SMGA", "UNTD", "TOSK", "MPIX", "ALII", "MKAP", "MEJA", "LIVE", "HYGN", "BAIK", "VISI", "AREA", "MHKI", "ATLA", "DATA", "SOLA", "BATR", "SPRE", "PART", "GOLF", "ISEA", "BLES", "GUNA", "LABS", "DOSS", "NEST", "PTMR", "VERN", "DAAZ", "BOAT", "NAIK", "AADI", "MDIY", "KSIX", "RATU", "YOII", "HGII", "BRRC", "DGWG", "CBDK", "OBAT", "MINE", "ASPR", "PSAT", "COIN", "CDIA", "BLOG", "MERI", "CHEK", "PMUI", "EMAS", "PJHB", "RLCO", "SUPA", "WBSA", "KAQI", "YUPI", "FORE", "MDLA", "DKHH", "AYLS", "DADA", "ASPI", "ESTA", "BESS", "AMAN", "CARE", "PIPA", "NCKL", "MENN", "AWAN", "MBMA", "RAAM", "DOOH", "CGAS", "NICE", "MSJA", "SMLE", "ACRO", "MANG", "WIFI", "FAPA", "DCII", "KETR", "DGNS", "UFOE", "ADMF", "ADMG", "ADRO", "AGII", "AGRO", "AGRS", "AHAP", "AIMS", "PNSE", "POLY", "POOL", "PPRO"
]

BSJP_LIST = WATCHLIST

# =========================
# HELPER
# =========================
def get_cached(symbol):
    now = time.time()

    if symbol in CACHE and now - CACHE_TIME[symbol] < 60:
        return CACHE[symbol]

    df = get_data(symbol)   # ✅ INI BENAR

    CACHE[symbol] = df
    CACHE_TIME[symbol] = now

    return df

def fetch_symbol(symbol):
    return symbol, get_cached(symbol)
def S(x):
    if isinstance(x, pd.DataFrame):
        x = x.iloc[:, 0]
    return pd.Series(x).dropna()

def zscore(series):
    series = series.dropna()
    if len(series) < 20:
        return 0
    return (series.iloc[-1] - series.mean()) / series.std()

# =========================
def get_data(symbol):
    try:
        df = yf.download(symbol + ".JK", period="3mo", interval="1d", progress=False, threads=False, timeout=5)

        if df is None or df.empty:
            return None

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.dropna()

        if len(df) < 50:
            return None

        return df
    except:
        return None
    
# =========================
# 🧠 SND ICT MULTI-TIMEFRAME V2
# =========================
def snd_scan():
    
    results = []

    SND_LIST = WATCHLIST[:30]

    for symbol in SND_LIST:

        df = get_cached(symbol)
        if df is None or df.empty:
         continue

        close = S(df["Close"])
        high = S(df["High"])
        low = S(df["Low"])
        volume = S(df["Volume"])

        price = close.iloc[-1]

        # =========================
        # D1 TREND (BIG BIAS)
        # =========================
        ma20 = close.rolling(20).mean().iloc[-1]
        ma50 = close.rolling(50).mean().iloc[-1]

        if price > ma20 > ma50:
            bias_d1 = "BULLISH 🟢"
        elif price < ma20 < ma50:
            bias_d1 = "BEARISH 🔴"
        else:
            bias_d1 = "RANGE ⚪️"

        # =========================
        # H4 STRUCTURE
        # =========================
        h4_res = high.rolling(10).max().iloc[-1]
        h4_sup = low.rolling(10).min().iloc[-1]

        h4_mid = (h4_res + h4_sup) / 2

        # =========================
        # ENTRY ZONE (LOOSER LOGIC)
        # =========================
        near_support = abs(price - h4_sup) / price < 0.03
        near_resistance = abs(price - h4_res) / price < 0.03

        # =========================
        # VOLUME CONFIRMATION
        # =========================
        vol_ma = volume.rolling(20).mean().iloc[-1]
        vol_ok = volume.iloc[-1] > vol_ma

        # =========================
        # SCORE SYSTEM (HYBRID)
        # =========================
        score = 0
        signal = None
        checklist = []


        # =========================
        # ENTRY
        # =========================
        entry = price

        # =========================
        # TP MULTI TIMEFRAME
        # =========================
        if signal == "BUY 🟢":
            tp1 = h4_mid
            tp2 = h4_res
            sl = h4_sup * 0.995

        else:
            tp1 = h4_mid
            tp2 = h4_sup
            sl = h4_res * 1.005

        # =========================
        # RR CALC
        # =========================
        rr = abs((tp2 - entry) / (entry - sl)) if entry != sl else 0

        # minimal quality filter
        if score < 3 or rr < 1:
            continue

        results.append(f"""
📊 {symbol}.JK
🧠 SND HYBRID SMART FLOW

D1 Bias: {bias_d1}
Score: {score}

💰 Entry: {entry:.2f}

🎯 TP1 (H4 Mid): {tp1:.2f}
🎯 TP2 (H4 Level): {tp2:.2f}
⛔ SL: {sl:.2f}

⚖️ RR: {rr:.2f}

🔎 {' | '.join(checklist)}
━━━━━━━━━━━━━━
""")

    if not results:
        return "❌ No SND setup (market sideways)"

    return "📡 SND HYBRID FLOW\n━━━━━━━━━━━━━━\n\n" + "\n".join(results[:5])

# ==============
# SND Chart
# ==============
def snd_chart(symbol):
    
    df = get_cached(symbol)
    if df is None:
        return None

    data = df.copy()
    chart_df = data.tail(80)

    close = data["Close"]
    high = data["High"]
    low = data["Low"]

    price = close.iloc[-1]

    # =========================
    # H4 SIMULATION
    # =========================
    df = df.copy()
    df.index = pd.to_datetime(df.index)
    df_h4 = df.resample("4h").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    }).dropna()

    h4_sup = df_h4["Low"].rolling(10).min().iloc[-1]
    h4_res = df_h4["High"].rolling(10).max().iloc[-1]
    h4_mid = (h4_sup + h4_res) / 2

    entry = price

    if price > h4_mid:
        signal = "BUY 🟢"
        sl = h4_sup
        tp1 = h4_mid
        tp2 = h4_res
        reason = "Momentum naik (di atas mid)"

    else:
        signal = "SELL 🔴"
        sl = h4_res
        tp1 = h4_mid
        tp2 = h4_sup
        reason = "Tekanan jual (di bawah mid)"

    # =========================
    # PLOT
    # =========================
    fig, axes = mpf.plot(
        chart_df,
        type='candle',
        style='yahoo',
        volume=True,
        returnfig=True,
        figsize=(12,7)
    )

    ax = axes[0]

    # =========================
    # ZONE (LEBIH HALUS)
    # =========================
    ax.axhspan(h4_sup*0.995, h4_sup*1.005, color='lime', alpha=0.15)
    ax.axhspan(h4_res*0.995, h4_res*1.005, color='red', alpha=0.15)
    ax.axhspan(h4_mid*0.995, h4_mid*1.005, color='dodgerblue', alpha=0.10)

    # =========================
    # GARIS UTAMA (TEBAL)
    # =========================
    ax.axhline(h4_sup, color='lime', linewidth=2)
    ax.axhline(h4_res, color='red', linewidth=2)
    ax.axhline(h4_mid, color='blue', linestyle='--', linewidth=1.5)

    ax.axhline(tp2, color='gold', linestyle='--', linewidth=2)
    ax.axhline(sl, color='black', linestyle='--', linewidth=2)

    # =========================
    # LABEL BOX (BIAR JELAS)
    # =========================
    def label(y, text, color, x_offset=0):
        ax.text(
            len(chart_df) - (15 - x_offset),  # 🔥 geser ke kiri + beda beda posisi
            y,
            f" {text} ",
            fontsize=10,
            color='white',
            va='center',
            bbox=dict(facecolor=color, edgecolor='none', boxstyle='round,pad=0.3')
        )

    label(h4_res, f"RES {h4_res:.0f}", "red")
    label(h4_sup, f"SUP {h4_sup:.0f}", "green")

    # =========================
    # INFO BOX (LEBIH CLEAN)
    # =========================
    info = f"""
{signal}
Entry : {entry:.0f}
TP    : {tp2:.0f}
SL    : {sl:.0f}

{reason}
"""

    ax.text(
        0.01, 0.99,
        info,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment='top',
        bbox=dict(facecolor='black', alpha=0.8, boxstyle='round'),
        color='white'
    )

    # =========================
    # STYLE FINAL
    # =========================
    ax.set_title(f"{symbol}.JK - SND Smart Money Chart", fontsize=14)
    ax.grid(True, alpha=0.2)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=120)
    plt.close()

    buf.seek(0)
    return buf

# =========================
# ANALYSIS DETAIL (TIDAK DIUBAH)
# =========================
def analyze_detail(symbol):

    df = get_cached(symbol)
    if df is None:
        return "❌ Data tidak tersedia"

    close = S(df["Close"])
    high = S(df["High"])
    low = S(df["Low"])
    open_ = S(df["Open"])
    volume = S(df["Volume"])

    price = close.iloc[-1]
    prev_price = close.iloc[-2]
    change_pct = ((price - prev_price) / prev_price) * 100

    ma20 = SMAIndicator(close, 20).sma_indicator().iloc[-1]
    ma50 = SMAIndicator(close, 50).sma_indicator().iloc[-1]

    if price > ma20 and price > ma50:
        trend = "UPTREND 🟢"
    elif price < ma20 and price < ma50:
        trend = "DOWNTREND 🔴"
    else:
        trend = "SIDEWAYS ⚪️"

    vwap = (close * volume).cumsum() / volume.cumsum()
    vwap_val = vwap.iloc[-1]
    vwap_label = "ABOVE 🟢" if price > vwap_val else "BELOW 🔴"

    rsi = RSIIndicator(close).rsi().iloc[-1]

    macd = MACD(close)
    macd_line = macd.macd().iloc[-1]
    macd_signal = macd.macd_signal().iloc[-1]
    macd_hist = macd.macd_diff().iloc[-1]
    macd_label = "BULLISH 🟢" if macd_hist > 0 else "BEARISH 🔴"

    bb = BollingerBands(close)
    bb_high = bb.bollinger_hband().iloc[-1]
    bb_mid = bb.bollinger_mavg().iloc[-1]
    bb_low = bb.bollinger_lband().iloc[-1]
    bb_label = "LOW ZONE 🟢" if price < bb_mid else "HIGH ZONE 🔴"

    support = low.rolling(20).min().iloc[-1]
    resistance = high.rolling(20).max().iloc[-1]

    atr = AverageTrueRange(high, low, close).average_true_range().iloc[-1]

    if trend == "UPTREND 🟢":
        entry = max(ma20, vwap_val)
        sl = entry - atr
        tp = entry + (atr * 2)
        signal = "BUY 🟢"

    elif trend == "DOWNTREND 🔴":
        entry = min(ma20, vwap_val)
        sl = entry + atr
        tp = entry - (atr * 2)
        signal = "SELL 🔴"

    else:
        entry = price
        sl = price - atr
        tp = price + atr
        signal = "WAIT ⚪️"

    sl_pct = ((sl - entry) / entry) * 100
    tp_pct = ((tp - entry) / entry) * 100
    rr = abs((tp - entry) / (entry - sl)) if entry != sl else 0

    return f"""
📊 {symbol}.JK
💰 Price: {price:.2f} ({change_pct:+.2f}%)

📉 MA20: {ma20:.2f}
📉 MA50: {ma50:.2f}
➡️ {trend}

📊 VWAP: {vwap_val:.2f} ({vwap_label})

📈 RSI: {rsi:.1f}

⚡️ MACD:
{macd_line:.2f} / {macd_signal:.2f} / {macd_hist:.2f}
➡️ {macd_label}

📦 BB:
U:{bb_high:.2f} M:{bb_mid:.2f} L:{bb_low:.2f}
➡️ {bb_label}

🧱 Support: {support:.2f}
🧱 Resistance: {resistance:.2f}

🎯 Signal: {signal}

Entry: {entry:.2f}
SL: {sl:.2f} ({sl_pct:+.2f}%)
TP: {tp:.2f} ({tp_pct:+.2f}%)
RR: {rr:.2f}
"""

# =========================
# 🧠 AI CHART SCALPING ANALYZER
# =========================
SCALPING_CHART_PROMPT = """
Kamu adalah AI scalping analyst untuk saham Indonesia.

Analisis screenshot chart yang dikirim user. Fokus pada:
1. Timeframe chart
2. Harga terakhir jika terlihat
3. Trend pendek
4. Posisi harga terhadap VWAP
5. EMA 5/13
6. Volume
7. RSI
8. Support dan resistance terdekat
9. Setup entry scalping
10. Stop loss dan take profit realistis
11. Risiko fake breakout / breakdown

Berikan hasil dalam format Telegram yang singkat, praktis, dan tegas.

Gunakan decision hanya salah satu:
🟢 BUY SETUP
🟡 WAIT
🔴 AVOID
⚠️ HIGH RISK

Jangan menjamin profit.
Jangan bilang pasti naik/turun.
Kalau data pada gambar tidak cukup jelas, katakan "data kurang jelas".
Selalu prioritaskan risk management.

Aturan tambahan:
- Jangan entry kalau volume kecil dan harga masih sideways.
- Jangan buy agresif kalau harga di bawah VWAP dan EMA 5 di bawah EMA 13.
- BUY SETUP hanya boleh kalau ada konfirmasi jelas: harga di atas VWAP, EMA mendukung, RSI sehat, volume masuk, dan ada level entry valid.
- Kalau belum ada trigger entry, pilih WAIT.
- Kalau chart sudah naik jauh dekat resistance, pilih HIGH RISK.
- Kalau support jebol, momentum lemah, dan RSI turun, pilih AVOID.
- Beri level entry/SL/TP dari area yang terlihat di chart, bukan angka asal.
- Kalau angka tidak terlihat jelas, tulis "tidak terbaca jelas".

Format jawaban:

📊 AI SCALPING ANALYSIS
Saham:
Timeframe:
Harga:

Decision:

📌 Bacaan Chart:
•

🎯 Entry Valid:
•

🛑 Stop Loss:
•

🚀 Target:
•

⚠️ Risiko:
•

Confidence:
"""

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def analyze_scalping_chart(image_path):
    try:
        if not OPENROUTER_API_KEY:
            return "❌ OPENROUTER_API_KEY belum diset di Railway Variables."

        base64_image = encode_image_to_base64(image_path)

        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/fikrimaul0311",
            "X-Title": "Stockbit Scalping Bot"
        }

        payload = {
            "model": "openrouter/free",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": SCALPING_CHART_PROMPT
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 700
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            return f"❌ Error OpenRouter:\n{response.status_code}\n{response.text[:1000]}"

        data = response.json()

        print("OPENROUTER RESPONSE:", data)

        content = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        if isinstance(content, list):
            content = "\n".join(
                item.get("text", "") if isinstance(item, dict) else str(item)
                for item in content
            )

        if not content or not str(content).strip():
            return (
                "❌ AI tidak mengembalikan jawaban.\n\n"
                "Kemungkinan:\n"
                "• model gratis OpenRouter sedang penuh\n"
                "• model tidak support gambar\n"
                "• response kosong dari provider\n"
                "• screenshot terlalu besar / kurang jelas\n\n"
                "Coba ganti model atau kirim screenshot yang lebih jelas."
            )

        return str(content).strip()

    except Exception as e:
        return f"❌ Error AI Chart Analyzer OpenRouter:\n{e}"

def get_chatbot_system_prompt(user_id):
    ai_name = BOT_AI_NAME.get(user_id, "KokoKiki")

    return f"""
Nama kamu adalah {ai_name}.

Kamu adalah asisten AI pribadi yang bisa diajak ngobrol tentang apa saja.
Jawab dalam bahasa Indonesia yang santai, natural, dan mudah dipahami.

Kamu bisa membantu user dalam banyak hal:
- curhat dan masalah hidup
- trading saham dan Stockbit
- coding Python dan bot Telegram
- ide bisnis dan produk digital
- belajar, portfolio, karier, dan project
- pertanyaan umum sehari-hari

Kalau user bertanya nama kamu, jawab bahwa nama kamu adalah {ai_name}.

Gaya jawaban:
- Jawab fleksibel sesuai pertanyaan user
- Jangan terlalu kaku
- Jangan terlalu panjang kalau user tanya santai
- Jangan terlalu banyak bullet point
- Jangan terlalu banyak emoji
- Jangan terdengar seperti artikel
- Kalau user curhat, dengarkan dulu dan jawab dengan empati
- Kalau user tanya coding, berikan solusi teknis yang jelas
- Kalau user tanya trading, jawab praktis tapi jangan menjamin profit
- Kalau data kurang jelas, tanya balik dengan singkat

Aturan penting:
- Jangan bilang saham pasti naik atau pasti turun
- Jangan menjamin profit
- Selalu prioritaskan risk management saat membahas trading
- Jangan mengaku punya data realtime kalau tidak diberikan user
- Kalau user bilang ingin curhat, jangan langsung kasih solusi panjang
- Tanggapi dulu perasaannya
- Tanyakan pelan-pelan apa yang paling berat
- Jawab seperti teman dekat yang suportif
"""

SCALPING_CHART_PROMPT = """
Kamu adalah AI scalping analyst untuk saham Indonesia.

Analisis screenshot chart yang dikirim user. Fokus pada:
1. Timeframe chart
2. Harga terakhir jika terlihat
3. Trend pendek
4. Posisi harga terhadap VWAP
5. EMA 5/13
6. Volume
7. RSI
8. Support dan resistance terdekat
9. Setup entry scalping
10. Stop loss dan take profit realistis
11. Risiko fake breakout / breakdown

Berikan hasil dalam format Telegram yang singkat, praktis, dan tegas.

Gunakan decision hanya salah satu:
🟢 BUY SETUP
🟡 WAIT
🔴 AVOID
⚠️ HIGH RISK

Jangan menjamin profit.
Jangan bilang pasti naik/turun.
Kalau data pada gambar tidak cukup jelas, katakan "data kurang jelas".
Selalu prioritaskan risk management.

Aturan tambahan:
- Jangan entry kalau volume kecil dan harga masih sideways.
- Jangan buy agresif kalau harga di bawah VWAP dan EMA 5 di bawah EMA 13.
- BUY SETUP hanya boleh kalau ada konfirmasi jelas: harga di atas VWAP, EMA mendukung, RSI sehat, volume masuk, dan ada level entry valid.
- Kalau belum ada trigger entry, pilih WAIT.
- Kalau chart sudah naik jauh dekat resistance, pilih HIGH RISK.
- Kalau support jebol, momentum lemah, dan RSI turun, pilih AVOID.
- Beri level entry/SL/TP dari area yang terlihat di chart, bukan angka asal.
- Kalau angka tidak terlihat jelas, tulis "tidak terbaca jelas".

Format jawaban:

📊 AI SCALPING ANALYSIS
Saham:
Timeframe:
Harga:

Decision:

📌 Bacaan Chart:
•

🎯 Entry Valid:
•

🛑 Stop Loss:
•

🚀 Target:
•

⚠️ Risiko:
•

Confidence:
"""

# =========================
# SCAN ALL (TIDAK DIUBAH)
# =========================
def scan_all():
    results = []

    for symbol in WATCHLIST:
        df = get_cached(symbol)
        if df is None:
            continue

        close = S(df["Close"])
        rsi = RSIIndicator(close).rsi().iloc[-1]

        score = abs(50 - rsi)
        results.append((symbol, score))

    results.sort(key=lambda x: x[1], reverse=True)

    text = "📡 TOP SCAN SAHAM\n\n"
    for s in results[:5]:
        text += f"{s[0]} (Score {s[1]:.1f})\n"

    return text

# =========================
# NEWS (FIX)
# =========================
def get_news(symbol=None):
    try:
        query = f"{symbol} saham Indonesia" if symbol else "IHSG saham Indonesia"
        encoded_query = urllib.parse.quote(query)

        url = f"https://news.google.com/rss/search?q={encoded_query}&hl=id&gl=ID&ceid=ID:id"

        res = requests.get(url, timeout=10)
        root = ET.fromstring(res.content)

        items = root.findall(".//item")

        if not items:
            return "❌ Tidak ada berita"

        text = "📰 NEWS SAHAM\n\n"

        for i, item in enumerate(items[:5]):
            title = item.find("title").text
            link = item.find("link").text
            text += f"{i+1}. {title}\n{link}\n\n"

        return text

    except Exception as e:
        return f"❌ Error news: {e}"

# =========================
# 📰 ADVANCED NEWS 3 LAYERS
# =========================
NEWS_KEYWORDS_HOT = [
    "akuisisi", "merger", "dividen", "right issue", "rights issue",
    "private placement", "stock split", "buyback", "suspensi",
    "UMA", "laba", "rugi", "kontrak", "ekspansi", "pinjaman",
    "utang", "obligasi", "default", "gagal bayar", "MSCI", "FTSE",
    "IPO", "RUPS", "cum date", "ex date"
]

# =========================
# 🏛️ IDX DISCLOSURE RADAR
# =========================
IDX_DISCLOSURE_KEYWORDS = [
    "keterbukaan informasi",
    "laporan informasi atau fakta material",
    "informasi fakta material",
    "pengumuman",
    "laporan bulanan registrasi pemegang efek",
    "laporan tahunan",
    "laporan keuangan",
    "dividen",
    "rups",
    "right issue",
    "rights issue",
    "private placement",
    "afiliasi",
    "transaksi material",
    "perubahan pengurus",
    "suspensi",
    "uma",
    "buyback",
    "stock split"
]

def fetch_google_news_rss(query, limit=5):
    try:
        encoded_query = urllib.parse.quote(query)
        url = (
            f"https://news.google.com/rss/search?"
            f"q={encoded_query}&hl=id&gl=ID&ceid=ID:id"
        )

        res = requests.get(url, timeout=10)
        root = ET.fromstring(res.content)

        items = root.findall(".//item")

        results = []

        for item in items[:limit]:
            title_el = item.find("title")
            link_el = item.find("link")
            pub_el = item.find("pubDate")
            source_el = item.find("source")

            title = title_el.text if title_el is not None else "-"
            link = link_el.text if link_el is not None else "-"
            pub_date = pub_el.text if pub_el is not None else "-"
            source = source_el.text if source_el is not None else "Unknown"

            results.append({
                "title": title,
                "link": link,
                "pub_date": pub_date,
                "source": source
            })

        return results

    except Exception as e:
        print("RSS ERROR:", e)
        return []


def format_news_output(title, query, items):
    if not items:
        return f"❌ Tidak ada news ditemukan.\nQuery: {query}"

    text = f"{title}\n"
    text += f"🔎 Query: {query}\n"
    text += "━━━━━━━━━━━━━━\n\n"

    for i, item in enumerate(items, 1):
        text += (
            f"{i}. {item['title']}\n"
            f"🏷️ Source: {item['source']}\n"
            f"🕒 {item['pub_date']}\n"
            f"{item['link']}\n\n"
        )

    return text[:3900]

def get_idx_news(symbol=None):
    if symbol:
        query = (
            f'{symbol} saham IDX OR BEI OR "Keterbukaan Informasi" '
            f'OR IDXNet OR OJK OR KSEI'
        )
    else:
        query = (
            '"Keterbukaan Informasi" OR IDXNet OR BEI OR IDX '
            'OR OJK OR KSEI saham'
        )

    items = fetch_google_news_rss(query, limit=7)

    return format_news_output(
        "🏛️ IDX / REGULATOR NEWS",
        query,
        items
    )

def get_corp_action_news(symbol=None):
    if symbol:
        query = (
            f'{symbol} dividen OR "cum date" OR "ex date" OR RUPS '
            f'OR "right issue" OR "rights issue" OR "stock split" '
            f'OR buyback OR waran OR KSEI OR IDX'
        )
    else:
        query = (
            'dividen OR "cum date" OR "ex date" OR RUPS '
            'OR "right issue" OR "rights issue" OR "stock split" '
            'OR buyback OR waran KSEI IDX saham'
        )

    items = fetch_google_news_rss(query, limit=7)

    return format_news_output(
        "📌 CORPORATE ACTION NEWS",
        query,
        items
    )

def get_hot_news(symbol=None):
    if symbol:
        keyword_query = " OR ".join([f'"{k}"' for k in NEWS_KEYWORDS_HOT])
        query = f'{symbol} saham Indonesia ({keyword_query})'
    else:
        keyword_query = " OR ".join([f'"{k}"' for k in NEWS_KEYWORDS_HOT])
        query = f'saham Indonesia ({keyword_query})'

    items = fetch_google_news_rss(query, limit=10)

    # scoring sederhana berdasarkan keyword penting di title
    scored = []

    for item in items:
        title_lower = item["title"].lower()
        score = 0

        for kw in NEWS_KEYWORDS_HOT:
            if kw.lower() in title_lower:
                score += 1

        # source tertentu sering cepat untuk market
        source_lower = item["source"].lower()
        if any(src in source_lower for src in ["kontan", "bisnis", "cnbc", "idx", "reuters"]):
            score += 1

        scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)

    sorted_items = [x[1] for x in scored]

    return format_news_output(
        "🔥 HOT MARKET NEWS",
        query,
        sorted_items
    )

# =========================
# 🧠 BROKER SUMMARY ANALYZER
# =========================
def analyze_broker_summary(image_path):

    try:
        # =========================
        # LOAD IMAGE
        # =========================
        img = cv2.imread(image_path)

        if img is None:
            return "❌ Gagal membaca gambar"

        # resize biar OCR lebih jelas
        img = cv2.resize(img, None, fx=2, fy=2)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # sharpen
        gray = cv2.GaussianBlur(gray, (3,3), 0)

        # threshold
        _, thresh = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        # OCR
        text = pytesseract.image_to_string(
            thresh,
            config='--psm 6'
        )

        # DEBUG OCR
        print(text)

        # =========================
        # PARSE
        # =========================
        lines = text.splitlines()

        buy_list = []
        sell_list = []

        current_mode = "buy"

        for line in lines:

            line = line.strip()

            # skip header
            if len(line) < 3:
                continue

            # detect kanan kiri
            # format contoh:
            # CC 16.1B
            matches = re.findall(
                r'([A-Z]{2})\s+([\d\.]+)\s*([BM])',
                line
            )

            for m in matches:

                broker = m[0]
                value = float(m[1])

                unit = m[2]

                # convert
                if unit == "B":
                    value *= 1000

                # =========================
                # LOGIC BUY/SELL
                # =========================

                # broker kiri = buy
                # broker kanan = sell

                # split berdasarkan posisi text
                pos = line.find(broker)

                if pos < len(line) / 2:
                    buy_list.append((broker, value))
                else:
                    sell_list.append((broker, value))

        # =========================
        # SORT
        # =========================
        buy_list = sorted(
            buy_list,
            key=lambda x: x[1],
            reverse=True
        )

        sell_list = sorted(
            sell_list,
            key=lambda x: x[1],
            reverse=True
        )

        # =========================
        # TOTAL
        # =========================
        total_buy = sum(x[1] for x in buy_list)
        total_sell = sum(x[1] for x in sell_list)

        net = total_buy - total_sell

        # =========================
        # SIGNAL
        # =========================
        if net > 3000:
            signal = "🟢 STRONG ACCUMULATION"
            insight = "Bandar besar dominan akumulasi"

        elif net > 0:
            signal = "🟡 ACCUMULATION"
            insight = "Buy broker masih lebih dominan"

        elif net < -3000:
            signal = "🔴 STRONG DISTRIBUTION"
            insight = "Tekanan distribusi besar"

        else:
            signal = "🟠 DISTRIBUTION"
            insight = "Seller masih dominan"

        # =========================
        # OUTPUT
        # =========================
        out = "🧠 BROKER SUMMARY ANALYSIS\n"
        out += "━━━━━━━━━━━━━━\n\n"

        out += "🔥 TOP ACCUMULATION\n"

        for b in buy_list[:5]:
            out += f"• {b[0]} → {b[1]:.1f}B\n"

        out += "\n🔻 TOP DISTRIBUTION\n"

        for s in sell_list[:5]:
            out += f"• {s[0]} → {s[1]:.1f}B\n"

        out += f"""

━━━━━━━━━━━━━━
📊 TOTAL BUY : {total_buy:.1f}B
📊 TOTAL SELL: {total_sell:.1f}B
📈 NET FLOW  : {net:.1f}B

🎯 SIGNAL:
{signal}

💡 Insight:
{insight}
"""

        return out

    except Exception as e:
        return f"❌ Error analyze broker summary:\n{e}"

# =========================
# 🧠 BSJP PRO (FIXED + SMART MONEY)
# =========================
def bsjp_scan():

    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        data_list = list(executor.map(fetch_symbol, BSJP_LIST))

    for symbol, df in data_list:

        try:

            if df is None or len(df) < 30:
                continue

            close = S(df["Close"])
            open_ = S(df["Open"])
            high = S(df["High"])
            low = S(df["Low"])
            volume = S(df["Volume"])

            price = close.iloc[-1]
            prev_close = close.iloc[-2]

            change_pct = ((price - prev_close) / prev_close) * 100

            # =========================
            # BASIC FILTER
            # =========================
            avg_value = (close * volume).rolling(20).mean().iloc[-1]

            # skip saham sepi
            if avg_value < 20_000_000_000:
                continue

            # skip terlalu liar
            if abs(change_pct) > 15:
                continue

            # =========================
            # VOLUME Z SCORE
            # =========================
            vol_mean = volume.rolling(20).mean().iloc[-1]
            vol_std = volume.rolling(20).std().iloc[-1]

            if vol_std == 0:
                continue

            vol_z = (volume.iloc[-1] - vol_mean) / vol_std

            # =========================
            # RANGE
            # =========================
            range_high = high.rolling(20).max().iloc[-2]
            range_low = low.rolling(20).min().iloc[-2]

            breakout = price > range_high

            # posisi harga dalam range
            position = (
                (price - range_low)
                / (range_high - range_low)
            ) if range_high != range_low else 0.5

            # =========================
            # CANDLE STRENGTH
            # =========================
            candle_body = abs(price - open_.iloc[-1])

            candle_range = (
                high.iloc[-1] - low.iloc[-1]
            )

            body_ratio = (
                candle_body / candle_range
            ) if candle_range != 0 else 0

            close_near_high = (
                (high.iloc[-1] - price)
                / candle_range
            ) < 0.25 if candle_range != 0 else False

            bullish_candle = (
                price > open_.iloc[-1]
            )

            # =========================
            # Z LABEL
            # =========================
            if vol_z < 1:
                z_label = "NORMAL ⚪️"

            elif vol_z < 2:
                z_label = "EARLY FLOW 🌱"

            elif vol_z < 3:
                z_label = "ACTIVE FLOW 🔥"

            elif vol_z < 4:
                z_label = "SMART MONEY 🟡"

            else:
                z_label = "MOMENTUM EXTREME 🚀🚀"

            # =========================
            # SCORE ENGINE
            # =========================
            score = 0
            checklist = []

            # volume
            if vol_z > 4:
                score += 5
                checklist.append(f"Extreme Vol Z={vol_z:.2f}")

            elif vol_z > 3:
                score += 4
                checklist.append(f"Smart Money Z={vol_z:.2f}")

            elif vol_z > 2:
                score += 2
                checklist.append(f"Active Volume Z={vol_z:.2f}")

            # breakout
            if breakout:
                score += 4
                checklist.append("Breakout")

            # near breakout
            elif position > 0.85:
                score += 3
                checklist.append("Near Breakout")

            # bullish candle
            if bullish_candle:
                score += 1
                checklist.append("Bullish Candle")

            # strong close
            if close_near_high:
                score += 2
                checklist.append("Close Near High")

            # strong body
            if body_ratio > 0.6:
                score += 2
                checklist.append("Momentum Candle")

            # =========================
            # CLASSIFICATION
            # =========================
            if score >= 12:
                label = "HIGH BREAKOUT 🚀🚀"

            elif score >= 9:
                label = "PRE BREAK ⚡️"

            elif score >= 6:
                label = "BUILDING 🔥"

            else:
                continue

            # =========================
            # ENTRY LOGIC
            # =========================
            entry = price * 0.998

            # scalping SL
            sl = low.iloc[-1] * 0.995

            risk = entry - sl

            if risk <= 0:
                continue

            # TP realistis
            tp = entry + (risk * 1.8)

            rr = (tp - entry) / risk

            sl_pct = ((sl - entry) / entry) * 100
            tp_pct = ((tp - entry) / entry) * 100

            # =========================
            # FINAL FILTER
            # =========================
            if rr < 1.3:
                continue

            if tp_pct < 1:
                continue

            results.append({
                "symbol": symbol,
                "score": score,
                "vol_z": vol_z,
                "label": label,
                "entry": entry,
                "sl": sl,
                "tp": tp,
                "rr": rr,
                "sl_pct": sl_pct,
                "tp_pct": tp_pct,
                "change_pct": change_pct,
                "checklist": checklist,
                "z_label": z_label,
            })

        except:
            continue

    # =========================
    # OUTPUT
    # =========================
    if not results:
        return "❌ Tidak ada setup BSJP"

    results.sort(
        key=lambda x: (
            x["score"],
            x["vol_z"]
        ),
        reverse=True
    )

    text = "🔥 BSJP SCALPING FLOW\n"
    text += "━━━━━━━━━━━━━━━━━━\n\n"

    for r in results[:5]:

        text += f"""📊 {r['symbol']}.JK
💰 Price: {r['entry']:.2f} ({r['change_pct']:+.2f}%)

📡 {r['z_label']}
🎯 {r['label']}

Score: {r['score']}
Z-Vol: {r['vol_z']:.2f}

🔎 {' | '.join(r['checklist'])}

💰 Entry: {r['entry']:.2f}
🧱 SL: {r['sl']:.2f} ({r['sl_pct']:.2f}%)
🎯 TP: {r['tp']:.2f} (+{r['tp_pct']:.2f}%)

⚖️ RR: {r['rr']:.2f}

━━━━━━━━━━━━━━━━━━

"""

    return text

# ============
# RSI Detektor
# ============
def rsi_scan():
    results = []

    for symbol in WATCHLIST:
        df = get_cached(symbol)
        if df is None:
            continue

        close = S(df["Close"])
        rsi = RSIIndicator(close, window=14).rsi().iloc[-1]

        if rsi <= 55:
            price = close.iloc[-1]

            # scoring (semakin kecil RSI makin menarik)
            score = 55 - rsi

            results.append((symbol, price, rsi, score))

    if not results:
        return "❌ Tidak ada saham RSI <= 55"

    # sort paling oversold
    results.sort(key=lambda x: x[3], reverse=True)

    text = "📉 RSI OVERSOLD SCAN (<=55)\n━━━━━━━━━━━━━━\n\n"

    for r in results[:10]:
        text += f"""📊 {r[0]}.JK
💰 Price: {r[1]:.2f}
📉 RSI: {r[2]:.2f}

"""

    return text

    return text

# =========================
# 📊 SNR STRATEGY ENGINE
# =========================
def snr_scan(symbol):

    df = get_cached(symbol)
    if df is None:
        return None

    close = S(df["Close"])
    high = S(df["High"])
    low = S(df["Low"])

    price = close.iloc[-1]
    

    # =========================
    # SNR LEVEL
    # =========================
    support = low.rolling(20).min().iloc[-1]
    resistance = high.rolling(20).max().iloc[-1]

    mid = (support + resistance) / 2

    atr = AverageTrueRange(high, low, close).average_true_range().iloc[-1]

    # =========================
    # SIGNAL LOGIC
    # =========================

    if price <= support * 1.01:
        signal = "BUY 🟢 (SNR Bounce)"

        entry = support * 1.002
        sl = support - (atr * 0.5)
        tp = resistance

    elif price >= resistance * 0.99:
        signal = "SELL 🔴 (SNR Rejection)"

        entry = resistance * 0.998
        sl = resistance + (atr * 0.5)
        tp = support

    else:
        signal = "WAIT ⚪️ (Inside Range)"

        entry = price
        sl = support
        tp = resistance

    risk = abs(entry - sl)
    reward = abs(tp - entry)

    rr = reward / risk if risk != 0 else 0

    return f"""
📊 {symbol}.JK SNR STRATEGY

💰 Price: {price:.2f}

🧱 Support: {support:.2f}
🔺 Resistance: {resistance:.2f}
➖ Mid: {mid:.2f}

🎯 SIGNAL: {signal}

📥 Entry: {entry:.2f}
🛑 SL: {sl:.2f}
🎯 TP: {tp:.2f}
⚖️ RR: {rr:.2f}
"""

# =========================
# 💰 RISK REWARD CALCULATOR
# =========================
def risk_reward_calc(symbol, modal):

    df = get_cached(symbol)

    if df is None:
        return "❌ Data saham tidak tersedia"

    close = S(df["Close"])
    high = S(df["High"])
    low = S(df["Low"])

    price = float(close.iloc[-1])

    # =========================
    # ATR
    # =========================
    atr = AverageTrueRange(
        high,
        low,
        close
    ).average_true_range().iloc[-1]

    # =========================
    # FIX SCALPING MODE
    # =========================

    # SL 2%
    sl_pct_target = 0.02

    # TP 3%
    tp_pct_target = 0.03

    # =========================
    # CALC
    # =========================
    sl = price * (1 - sl_pct_target)

    tp = price * (1 + tp_pct_target)

    risk = price - sl
    reward = tp - price

    rr = reward / risk if risk != 0 else 0

    # =========================
    # LOT CALC
    # =========================
    shares = int(modal / price)

    lot = shares // 100

    shares = lot * 100

    total_buy = shares * price

    # =========================
    # POTENTIAL
    # =========================
    potential_loss = shares * (price - sl)

    potential_profit = shares * (tp - price)

    sl_pct = ((sl - price) / price) * 100
    tp_pct = ((tp - price) / price) * 100

    return f"""
📊 {symbol}.JK

💰 Harga Sekarang: {price:.0f}
💵 Modal: Rp {modal:,.0f}

🧾 Lot: {lot}
📦 Shares: {shares:,}

💸 Total Buy:
Rp {total_buy:,.0f}

🛑 Stop Loss:
{sl:.0f} ({sl_pct:.2f}%)

🎯 Take Profit:
{tp:.0f} (+{tp_pct:.2f}%)

⚖️ Risk Reward:
1 : {rr:.2f}

❌ Potensi Loss:
Rp {potential_loss:,.0f}

🚀 Potensi Profit:
Rp {potential_profit:,.0f}
"""

def ask_openrouter_chat(user_id, user_text):
    try:
        if not OPENROUTER_API_KEY:
            return "❌ OPENROUTER_API_KEY belum diset di Railway Variables."

        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/fikrimaul0311",
            "X-Title": "Stockbit Chat Bot"
        }

        history = CHAT_HISTORY.get(user_id, [])

        messages = [
            {
                "role": "system",
                "content": get_chatbot_system_prompt(user_id)
            }
        ]

        messages.extend(history[-8:])

        messages.append({
            "role": "user",
            "content": user_text
        })

        models = [
            "meta-llama/llama-3.1-8b-instruct:free",
            "mistralai/mistral-7b-instruct:free",
            "qwen/qwen-2.5-7b-instruct:free",
            "openrouter/free"
        ]

        last_error = None

        for model in models:
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": 900,
                "temperature": 0.75
            }

            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=60
            )

            if response.status_code != 200:
                last_error = f"{response.status_code} {response.text[:500]}"
                continue

            data = response.json()

            content = (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )

            if content and str(content).strip():
                answer = str(content).strip()

                history.append({
                    "role": "user",
                    "content": user_text
                })

                history.append({
                    "role": "assistant",
                    "content": answer
                })

                CHAT_HISTORY[user_id] = history[-10:]

                return answer

        return (
            "❌ AI belum berhasil menjawab.\n"
            "Kemungkinan model gratis sedang penuh atau membalas kosong.\n"
            f"Error terakhir: {last_error}"
        )

    except Exception as e:
        return f"❌ Error Chat AI:\n{e}"

def quick_local_reply(user_text, user_id):
    text = user_text.lower().strip()

    ai_name = BOT_AI_NAME.get(user_id, "KokoKiki")

    greetings = [
        "hai", "halo", "hallo", "hello", "hi", "p", "ping",
        "assalamualaikum", "salam", "oy", "woi"
    ]

    if text in greetings:
        return f"Haii, aku {ai_name}. Mau bahas apa nih?"

    if text in ["nama kamu siapa", "nama kamu siapa?", "siapa nama kamu", "siapa nama kamu?"]:
        return f"Nama aku {ai_name}."

    if text in ["makasih", "terima kasih", "thanks", "thank you"]:
        return "Sama samaa."

    return None

# =========================
# 🔥 UNUSUAL STOCK RADAR
# =========================
def analyze_unusual_df(symbol, df):
    try:
        if df is None or len(df) < 30:
            return None

        close = pd.Series(df["Close"]).dropna()
        high = pd.Series(df["High"]).dropna()
        low = pd.Series(df["Low"]).dropna()
        volume = pd.Series(df["Volume"]).dropna()

        if len(close) < 30 or len(volume) < 30:
            return None

        price = float(close.iloc[-1])
        prev_close = float(close.iloc[-2])
        today_high = float(high.iloc[-1])
        today_low = float(low.iloc[-1])
        today_vol = float(volume.iloc[-1])

        today_value = price * today_vol
        traded_value_series = close * volume

        avg_vol20 = float(volume.tail(20).mean())
        std_vol20 = float(volume.tail(20).std()) if float(volume.tail(20).std()) != 0 else 1.0
        avg_value20 = float(traded_value_series.tail(20).mean()) if float(traded_value_series.tail(20).mean()) != 0 else 1.0

        vol_z = (today_vol - avg_vol20) / std_vol20
        value_ratio = today_value / avg_value20 if avg_value20 > 0 else 0

        change_pct = ((price - prev_close) / prev_close) * 100 if prev_close > 0 else 0

        prev20_high = float(high.iloc[-21:-1].max())
        prev10_low = float(low.iloc[-11:-1].min())
        breakout = price > prev20_high
        near_breakout = price >= (prev20_high * 0.985)

        day_range = max(today_high - today_low, 1e-9)
        close_near_high = ((today_high - price) / day_range) <= 0.25

        score = 0

        # Volume anomaly
        if vol_z >= 3:
            score += 25
        elif vol_z >= 2:
            score += 18
        elif vol_z >= 1:
            score += 10

        # Value anomaly
        if value_ratio >= 3:
            score += 25
        elif value_ratio >= 2:
            score += 18
        elif value_ratio >= 1.5:
            score += 10

        # Price action
        if breakout:
            score += 20
        elif near_breakout:
            score += 12

        if close_near_high:
            score += 10

        if 1 <= change_pct <= 9:
            score += 10
        elif 9 < change_pct <= 15:
            score += 6
        elif change_pct < -3:
            score -= 8

        # Liquidity filter
        if avg_value20 >= 20_000_000_000:   # 20B
            score += 10
        elif avg_value20 >= 5_000_000_000:  # 5B
            score += 5
        else:
            score -= 15

        if score >= 75:
            signal = "EXTREME FLOW"
        elif score >= 60:
            signal = "ACTIVE FLOW"
        elif score >= 45:
            signal = "EARLY FLOW"
        else:
            signal = "WATCHLIST"

        if breakout:
            status = "Breakout"
        elif near_breakout:
            status = "Near Breakout"
        elif change_pct > 0 and close_near_high:
            status = "Momentum Build-Up"
        else:
            status = "Monitor"

        return {
            "symbol": symbol,
            "price": price,
            "change_pct": change_pct,
            "score": round(score, 1),
            "vol_z": round(vol_z, 2),
            "value_ratio": round(value_ratio, 2),
            "today_value": today_value,
            "avg_value20": avg_value20,
            "signal": signal,
            "status": status,
            "breakout_level": prev20_high,
            "support_level": prev10_low,
            "close_near_high": close_near_high
        }

    except Exception as e:
        print(f"UNUSUAL ERROR {symbol}: {e}")
        return None


def format_rupiah_short(num):
    try:
        num = float(num)
        if num >= 1_000_000_000_000:
            return f"Rp{num/1_000_000_000_000:.2f}T"
        elif num >= 1_000_000_000:
            return f"Rp{num/1_000_000_000:.2f}B"
        elif num >= 1_000_000:
            return f"Rp{num/1_000_000:.2f}M"
        else:
            return f"Rp{num:,.0f}"
    except:
        return str(num)


def unusual_scan(limit=10):
    scan_list = UNIVERSE if "UNIVERSE" in globals() else BSJP_LIST

    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        data_list = list(executor.map(fetch_symbol, scan_list))

    for symbol, df in data_list:
        result = analyze_unusual_df(symbol, df)
        if not result:
            continue

        # filter hanya yang cukup menarik
        if result["score"] >= 45 and result["today_value"] >= 2_000_000_000:
            results.append(result)

    results.sort(key=lambda x: (x["score"], x["today_value"]), reverse=True)

    if not results:
        return "❌ Tidak ada saham unusual yang lolos filter saat ini."

    text = "🔥 UNUSUAL STOCK RADAR\n\n"

    for i, r in enumerate(results[:limit], 1):
        text += (
            f"{i}. {r['symbol']} — {r['signal']}\n"
            f"Harga: {r['price']:.0f} ({r['change_pct']:+.2f}%)\n"
            f"Score: {r['score']}\n"
            f"Vol Z: {r['vol_z']} | Value Ratio: {r['value_ratio']}x\n"
            f"Value: {format_rupiah_short(r['today_value'])}\n"
            f"Status: {r['status']}\n"
            f"BO Level: {r['breakout_level']:.0f} | Support: {r['support_level']:.0f}\n\n"
        )

    text += "📌 Fokus: cek orderbook, running trade, dan chart 5M sebelum entry."
    return text


def unusual_single(symbol):
    symbol = symbol.upper().replace(".JK", "")

    data = fetch_symbol(symbol)
    if not data or data[1] is None:
        return f"❌ Data {symbol} tidak ditemukan."

    _, df = data
    r = analyze_unusual_df(symbol, df)

    if not r:
        return f"❌ Data {symbol} tidak cukup untuk dianalisis."

    text = (
        f"🔥 UNUSUAL CHECK — {r['symbol']}\n\n"
        f"Signal: {r['signal']}\n"
        f"Harga: {r['price']:.0f} ({r['change_pct']:+.2f}%)\n"
        f"Score: {r['score']}\n"
        f"Vol Z: {r['vol_z']}\n"
        f"Value Ratio: {r['value_ratio']}x\n"
        f"Today Value: {format_rupiah_short(r['today_value'])}\n"
        f"Avg Value 20D: {format_rupiah_short(r['avg_value20'])}\n"
        f"Status: {r['status']}\n"
        f"Breakout Level: {r['breakout_level']:.0f}\n"
        f"Support Level: {r['support_level']:.0f}\n"
        f"Close Near High: {'Ya' if r['close_near_high'] else 'Tidak'}\n\n"
        f"📌 Interpretasi:\n"
    )

    if r["signal"] == "EXTREME FLOW":
        text += "Ada aktivitas sangat kuat. Hati-hati euforia, tunggu konfirmasi chart.\n"
    elif r["signal"] == "ACTIVE FLOW":
        text += "Saham sedang aktif dan layak dipantau untuk momentum / breakout.\n"
    elif r["signal"] == "EARLY FLOW":
        text += "Mulai ada aliran dana. Cocok jadi watchlist awal.\n"
    else:
        text += "Belum cukup kuat. Masih sebatas monitor.\n"

    text += "\n⚠️ Jangan entry hanya karena unusual. Tetap cek VWAP, EMA, volume, orderbook, dan broksum."
    return text

def score_idx_disclosure_item(item, symbol=None):
    title = item.get("title", "").lower()
    link = item.get("link", "").lower()
    source = item.get("source", "").lower()

    score = 0

    if symbol and symbol.lower() in title:
        score += 5

    if "idx" in source or "bei" in source:
        score += 4

    if "idx.co.id" in link:
        score += 5

    if "staticdata/newsandannouncement" in link:
        score += 6

    for kw in IDX_DISCLOSURE_KEYWORDS:
        if kw.lower() in title:
            score += 2

    hot_words = [
        "dividen", "right issue", "rights issue", "private placement",
        "suspensi", "uma", "buyback", "stock split", "transaksi material",
        "laporan keuangan", "rups", "perubahan pengurus"
    ]

    for kw in hot_words:
        if kw in title:
            score += 3

    return score


def classify_idx_disclosure(title):
    t = title.lower()

    if "dividen" in t or "cum date" in t or "ex date" in t:
        return "Dividen"
    if "right issue" in t or "rights issue" in t or "hm etd" in t or "hmetd" in t:
        return "Right Issue / HMETD"
    if "private placement" in t or "penambahan modal tanpa hmetd" in t:
        return "Private Placement"
    if "rups" in t or "rapat umum pemegang saham" in t:
        return "RUPS"
    if "laporan keuangan" in t:
        return "Laporan Keuangan"
    if "laporan tahunan" in t or "annual report" in t:
        return "Laporan Tahunan"
    if "suspensi" in t:
        return "Suspensi"
    if "uma" in t or "unusual market activity" in t:
        return "UMA"
    if "buyback" in t or "pembelian kembali" in t:
        return "Buyback"
    if "stock split" in t or "pemecahan nilai nominal" in t:
        return "Stock Split"
    if "transaksi material" in t or "afiliasi" in t:
        return "Transaksi Material / Afiliasi"
    if "fakta material" in t or "keterbukaan informasi" in t:
        return "Keterbukaan Informasi"

    return "Disclosure"


def get_idx_disclosure(symbol=None):
    try:
        if symbol:
            symbol = symbol.upper().replace(".JK", "")

            query = (
                f'{symbol} '
                f'("Keterbukaan Informasi" OR "Laporan Informasi atau Fakta Material" '
                f'OR "Pengumuman" OR "IDXNet" OR "BEI") '
                f'site:idx.co.id'
            )
        else:
            query = (
                f'("Keterbukaan Informasi" OR "Laporan Informasi atau Fakta Material" '
                f'OR "IDXNet" OR "BEI" OR "Pengumuman") '
                f'site:idx.co.id'
            )

        items = fetch_google_news_rss(query, limit=15)

        scored = []

        for item in items:
            score = score_idx_disclosure_item(item, symbol)
            if score > 0:
                scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)

        if not scored:
            return (
                "❌ Tidak ada IDX disclosure ditemukan.\n\n"
                f"Query: {query}\n\n"
                "Coba cek tanpa kode saham atau gunakan /hotnews KODE."
            )

        text = "🏛️ IDX DISCLOSURE RADAR\n"

        if symbol:
            text += f"Kode: {symbol}\n"

        text += f"🔎 Query: {query}\n"
        text += "━━━━━━━━━━━━━━\n\n"

        for i, (score, item) in enumerate(scored[:8], 1):
            category = classify_idx_disclosure(item["title"])

            text += (
                f"{i}. [{category}] Score {score}\n"
                f"{item['title']}\n"
                f"🏷️ Source: {item['source']}\n"
                f"🕒 {item['pub_date']}\n"
                f"{item['link']}\n\n"
            )

        text += (
            "📌 Catatan:\n"
            "Ini radar disclosure berbasis Google News RSS + domain IDX.\n"
            "Untuk validasi final, tetap buka link IDX/PDF resminya."
        )

        return text[:3900]

    except Exception as e:
        return f"❌ Error IDX Disclosure:\n{e}"

# =========================
# COMMANDS
# =========================
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
📊 MENU BOT

/scanall Tunggu 7 menit
/scan Kode Emiten
/news
/news Kode Emiten
/idxnews KODE - News resmi IDX/OJK/KSEI
/corpact KODE - Corporate action
/hotnews KODE - Hot market-moving news
/unusual - Radar saham unusual
/unusual KODE - Check unusual satu saham
/idxdisclosure KODE - Cek keterbukaan informasi IDX
/idxdisclosure - Cek disclosure terbaru IDX
/bsjp Tunggu 7 menit
/daily Tunggu 7 menit
/snr Kode Emiten
/snd Kode Emiten
/sndc Kode Emiten
/rsi 🔥 (RSI Oversold)
/bs Analyze Broker Summary Image
/rr KODE MODAL
/chart Analyze Screenshot Chart Scalping
/chat Ngobrol dengan AI
/setname NamaAI - Ubah nama AI chat
/exit Keluar dari mode chat
""")

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Contoh: /scan BBCA")
        return
    await update.message.reply_text(analyze_detail(context.args[0].upper()))

async def scanall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(scan_all())

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = context.args[0].upper() if context.args else None
    await update.message.reply_text(get_news(symbol))

async def idxnews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = context.args[0].upper() if context.args else None

    await update.message.reply_text("🏛️ Mencari IDX / regulator news...")

    result = await asyncio.to_thread(
        get_idx_news,
        symbol
    )

    await update.message.reply_text(safe_text(result))


async def corpact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = context.args[0].upper() if context.args else None

    await update.message.reply_text("📌 Mencari corporate action news...")

    result = await asyncio.to_thread(
        get_corp_action_news,
        symbol
    )

    await update.message.reply_text(safe_text(result))


async def hotnews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = context.args[0].upper() if context.args else None

    await update.message.reply_text("🔥 Mencari hot market news...")

    result = await asyncio.to_thread(
        get_hot_news,
        symbol
    )

    await update.message.reply_text(safe_text(result))

async def bsjp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔎 Scanning BSJP 7 menit... jalan di background")

    async def run_scan():
        result = await asyncio.to_thread(bsjp_scan)
        await update.message.reply_text(result)

    asyncio.create_task(run_scan())
    
async def snd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = await asyncio.to_thread(snd_scan)
    await update.message.reply_text(result)

async def snr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Contoh: /snr BBCA")
        return

    symbol = context.args[0].upper()
    result = await asyncio.to_thread(snr_scan, symbol)

    if result is None:
        await update.message.reply_text("❌ Data tidak tersedia")
    else:
        await update.message.reply_text(result)
        
async def sndc(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Contoh: /sndc BBCA")
        return

    symbol = context.args[0].upper()

    await update.message.reply_text("📊 Generating Chart SND...")

    file = await asyncio.to_thread(snd_chart, symbol)

    if file is None:
        await update.message.reply_text("❌ Data tidak tersedia")
        return

    await update.message.reply_photo(photo=file)

async def rsi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔎 Scanning RSI Oversold...")

    result = await asyncio.to_thread(rsi_scan)

    await update.message.reply_text(result)

# =========================
# 💰 RR COMMAND
# =========================
async def rr(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 2:
        await update.message.reply_text(
            "Contoh:\n/rr ESIP 10000000"
        )
        return

    symbol = context.args[0].upper()

    try:
        modal = int(context.args[1])

    except:
        await update.message.reply_text(
            "❌ Modal harus angka"
        )
        return

    await update.message.reply_text(
        "📊 Menghitung Risk Reward..."
    )

    result = await asyncio.to_thread(
        risk_reward_calc,
        symbol,
        modal
    )

    await update.message.reply_text(result)

async def bs(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    USER_MODE[user_id] = "broker"

    await update.message.reply_text(
        "📸 Kirim screenshot broker summary"
    )



async def broker_summary_image(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.photo:
        return

    await update.message.reply_text("📸 Membaca Broker Summary...")

    photo = update.message.photo[-1]

    file = await context.bot.get_file(photo.file_id)

    path = f"broker_{update.message.message_id}.jpg"

    await file.download_to_drive(path)

    result = await asyncio.to_thread(analyze_broker_summary, path)

    await update.message.reply_text(result)

async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    USER_MODE[user_id] = "chart"

    await update.message.reply_text(
        "📸 Kirim screenshot chart scalping Stockbit.\n\n"
        "Pastikan terlihat:\n"
        "• kode saham\n"
        "• timeframe 5M / 15M\n"
        "• harga terakhir\n"
        "• VWAP\n"
        "• EMA 5/13\n"
        "• Volume\n"
        "• RSI"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    USER_MODE[user_id] = "chat"

    await update.message.reply_text(
        "💬 Mode chat aktif.\n\n"
        "Sekarang kamu bisa ngobrol bebas sama AI.\n"
        "Ketik /exit untuk keluar dari mode chat."
    )

async def exit_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    CHAT_HISTORY.pop(user_id, None)

    await update.message.reply_text(
        "✅ Mode chat dimatikan.\n"
        "Kamu bisa pakai command lain seperti /chart, /bs, /scan, /rr."
    )

async def send_streaming_text(message, text, delay=0.06, chunk_words=5):
    text = safe_text(text)

    words = text.split()
    shown = ""

    sent = await message.reply_text("💭")

    for i in range(0, len(words), chunk_words):
        chunk = " ".join(words[i:i + chunk_words])
        shown += chunk + " "

        try:
            await sent.edit_text(shown.strip())
        except Exception:
            pass

        await asyncio.sleep(delay)

    return sent


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    mode = USER_MODE.get(user_id)

    if mode != "chat":
        return

    user_text = update.message.text

    if not user_text or not user_text.strip():
        return

    # Balasan lokal untuk sapaan sederhana biar tidak dilempar ke AI
    local_reply = quick_local_reply(user_text, user_id)

    if local_reply:
        await update.message.reply_text(local_reply)
        return

    thinking_msg = await update.message.reply_text("💭 Lagi ngetik...")

    result = await asyncio.to_thread(
        ask_openrouter_chat,
        user_id,
        user_text
    )

    try:
        await thinking_msg.delete()
    except Exception:
        pass

    await send_streaming_text(
        update.message,
        result,
        delay=0.06,
        chunk_words=5
    )

async def setname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text(
            "Contoh:\n/setname KokoKiki"
        )
        return

    name = " ".join(context.args).strip()

    if len(name) > 30:
        await update.message.reply_text(
            "❌ Nama terlalu panjang. Maksimal 30 karakter."
        )
        return

    BOT_AI_NAME[user_id] = name

    await update.message.reply_text(
        f"✅ Nama AI sekarang: {name}\n\n"
        f"Kalau ditanya nama, aku akan jawab sebagai {name}."
    )

async def idxdisclosure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = context.args[0].upper() if context.args else None

    if symbol:
        await update.message.reply_text(f"🏛️ Mencari IDX disclosure {symbol}...")
    else:
        await update.message.reply_text("🏛️ Mencari IDX disclosure terbaru...")

    result = await asyncio.to_thread(
        get_idx_disclosure,
        symbol
    )

    await update.message.reply_text(safe_text(result))

async def unusual(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        symbol = context.args[0].upper()

        await update.message.reply_text(f"🔍 Mengecek unusual signal {symbol}...")

        result = await asyncio.to_thread(
            unusual_single,
            symbol
        )

        await update.message.reply_text(safe_text(result))
    else:
        await update.message.reply_text("🔍 Scanning unusual stocks...")

        result = await asyncio.to_thread(
            unusual_scan,
            10
        )

        await update.message.reply_text(safe_text(result))

# =========================
# 🆕 DAILY REPORT IHSG + MARKET FLOW
# =========================
def daily_report_ihsg():
    
    gainers = []
    losers = []
    most_active = []
    foreign_flow = []

    total_up = total_down = total_flat = 0
    total_value = 0

    biggest_drop = []
    biggest_push = []

    for s in WATCHLIST:
        df = get_cached(s)
        if df is None:
         continue

        close = S(df["Close"])
        volume = S(df["Volume"])
        high = S(df["High"])
        low = S(df["Low"])

        price = close.iloc[-1]
        prev = close.iloc[-2]

        change = ((price - prev) / prev) * 100
        value = price * volume.iloc[-1]

        total_value += value

        # =========================
        # FILTER DULU (IMPORTANT)
        # =========================

        if volume.iloc[-1] == 0:
          continue

        if np.isnan(change):
          continue

        if abs(change) < 0.5:
          continue

        if value < 50_000_000:
          continue

        # =========================
        # CLASSIFICATION BARU
        # =========================

        if change > 0:
          total_up += 1
          gainers.append((s, price, change))

        elif change < 0:
           total_down += 1
           losers.append((s, price, change))

        else:
          total_flat += 1

        most_active.append((s, value, change, price))

        # proxy foreign flow lebih stabil (berbasis volume + direction)
        if change > 0:
         flow_sign = 1
        else:
         flow_sign = -1

        net_foreign = (volume.iloc[-1] * price * 0.1 * flow_sign) / 1_000_000
        net_foreign = (volume.iloc[-1] * price * (abs(change) / 100) * flow_sign) / 1_000_000
        foreign_flow.append((s, price, change, net_foreign))
        
        # =========================
        # ACTIVE MARKET FILTER (WAJIB)
        # =========================

        if volume.iloc[-1] < 100000:
          continue  # skip saham sepi

        if np.isnan(change):
          continue

        # pastikan ada price movement real
        if abs(change) < 0.5:
          continue

    # =========================
    # MARKET-REAL SORTING FIX
    # =========================

    # filter noise dulu biar lebih market-like
    gainers = [g for g in gainers if g[2] > 0.3]
    losers = [l for l in losers if l[2] < -0.3]

    # sorting real market style
    # REAL MARKET SORT (stabil + clean)
    gainers = sorted(gainers, key=lambda x: x[2], reverse=True)
    losers = sorted(losers, key=lambda x: x[2])                # paling jatuh ke atas
    most_active.sort(key=lambda x: x[1], reverse=True)
    foreign_flow.sort(key=lambda x: x[3], reverse=True)

    sentiment = "🟢 Bullish" if total_up > total_down else "🔴 Bearish"

    # ================= IHSG REASON ENGINE =================
    reason = []

    avg_move = np.mean(biggest_push + biggest_drop) if (biggest_push or biggest_drop) else 0

    if total_down > total_up:
        reason.append("Tekanan jual dominan di mayoritas saham")
    else:
        reason.append("Aksi beli masih lebih kuat dibanding tekanan jual")

    if avg_move < -2:
        reason.append("Penurunan tajam di saham big caps & sektor utama")
    elif avg_move > 2:
        reason.append("Momentum penguatan merata di saham besar")

    if len([x for x in losers if x[2] < -3]) > len(gainers):
        reason.append("Distribusi terjadi di saham-saham berkapitalisasi besar")

    if total_value > 10e12:
        reason.append("Likuiditas pasar tinggi → market aktif bergerak")

    if not reason:
        reason.append("Market cenderung sideways tanpa katalis kuat")

    reason_text = " | ".join(reason[:3])

    # ================= OUTPUT =================
    text = f"""
📊 RINGKASAN SAHAM INDONESIA
🗓️ {datetime.datetime.now().strftime('%A, %d %B %Y')}
━━━━━━━━━━━━━━━━━━━━━━

📈 Sentimen Syariah: {sentiment}
* Naik: {total_up} | Turun: {total_down} | Flat: {total_flat}
* Total Nilai: Rp {total_value/1e12:.2f}T

🧠 IHSG ANALYSIS:
➡️ {reason_text}

🚀 TOP GAINERS
"""

    for g in gainers[:5]:
        text += f"* {g[0]}  Rp {g[1]:.0f}  +{g[2]:.2f}%\n"

    text += "\n💥 TOP LOSERS\n"

    for l in losers[:5]:
        text += f"* {l[0]}  Rp {l[1]:.0f}  {l[2]:.2f}%\n"

    text += "\n🔥 MOST ACTIVE (VALUE)\n"

    for m in most_active[:5]:
        text += f"* {m[0]}  Rp {m[3]:.0f}  {m[2]:+.2f}%  Rp {m[1]/1e9:.2f}B\n"

    text += "\n🌍 NET FOREIGN FLOW (ESTIMASI)\n"

    for f in foreign_flow[:5]:
        text += f"* {f[0]}  Rp {f[1]:.0f}  {f[2]:+.2f}%  +Rp {f[3]:.1f}M\n"

    text += "\n━━━━━━━━━━━━━━━━━━━━━━\n💡 Insight: " + reason_text

    return text
def safe_text(text):
    if text is None:
        return "❌ Hasil kosong dari AI/API."

    text = str(text).strip()

    if not text:
        return "❌ Hasil analisis kosong. Coba kirim ulang screenshot atau ganti model AI."

    # batas aman Telegram ±4096 karakter
    if len(text) > 3900:
        text = text[:3900] + "\n\n⚠️ Output dipotong karena terlalu panjang."

    return text
    
# =========================
# 📸 PHOTO HANDLER
# =========================
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    mode = USER_MODE.get(user_id)

    if mode not in ["broker", "chart"]:
        await update.message.reply_text(
            "❌ Pilih mode dulu:\n"
            "/bs untuk Broker Summary\n"
            "/chart untuk AI Scalping Chart"
        )
        return

    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)

    if mode == "broker":
        path = f"broker_{update.message.message_id}.jpg"
        await file.download_to_drive(path)

        await update.message.reply_text("📸 Membaca Broker Summary...")

        result = await asyncio.to_thread(
            analyze_broker_summary,
            path
        )

        await update.message.reply_text(safe_text(result))

    elif mode == "chart":
        path = f"chart_{update.message.message_id}.jpg"
        await file.download_to_drive(path)

        await update.message.reply_text("🧠 Menganalisis chart scalping via OpenRouter...")

        result = await asyncio.to_thread(
            analyze_scalping_chart,
            path
        )

        await update.message.reply_text(safe_text(result))

    USER_MODE.pop(user_id, None)

# =========================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("scan", scan))
    app.add_handler(CommandHandler("scanall", scanall))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("idxnews", idxnews))
    app.add_handler(CommandHandler("corpact", corpact))
    app.add_handler(CommandHandler("hotnews", hotnews))
    app.add_handler(CommandHandler("unusual", unusual))
    app.add_handler(CommandHandler("idxdisclosure", idxdisclosure))
    app.add_handler(CommandHandler("bsjp", bsjp))
    app.add_handler(CommandHandler("daily", lambda u, c: u.message.reply_text(daily_report_ihsg())))
    app.add_handler(CommandHandler("snd", snd))
    app.add_handler(CommandHandler("sndc", sndc))
    app.add_handler(CommandHandler("snr", snr))
    app.add_handler(CommandHandler("rsi", rsi))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CommandHandler("bs", bs))
    app.add_handler(CommandHandler("rr", rr))
    app.add_handler(CommandHandler("chart", chart))
    app.add_handler(CommandHandler("chat", chat))
    app.add_handler(CommandHandler("exit", exit_mode))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CommandHandler("setname", setname))
    

    print("🚀 Bot KokoKiki Ready")
    app.run_polling()

if __name__ == "__main__":
    main()
