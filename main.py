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
import logging
logging.getLogger("yfinance").setLevel(logging.CRITICAL)
import os
os.system("apt update")
os.system("apt install -y tesseract-ocr")
os.system("pip install --no-cache-dir mplfinance matplotlib")
os.system("pip install --no-cache-dir python-telegram-bot[job-queue]")
os.system("pip install --no-cache-dir pytesseract pillow")
os.system("pip install --no-cache-dir opencv-python-headless")
if not os.path.exists("temp"):
    os.makedirs("temp")


from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange, BollingerBands

from PIL import Image
from telegram.ext import MessageHandler, filters

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=5)


warnings.filterwarnings("ignore")

TOKEN = "8746301929:AAGJmL-MOMNqT1VG5Jmv5GZ_d6cFuOPba4s"


CACHE = {}
CACHE_TIME = {}
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

        # trend bias
        if bias_d1 == "BULLISH 🟢":
            score += 1
        if bias_d1 == "BEARISH 🔴":
            score += 1

        # entry zone logic (LOOSER)
        if bias_d1 == "BULLISH 🟢" and near_support:
            score += 3
            signal = "BUY 🟢"
            checklist.append("Near H4 Support")

        if bias_d1 == "BEARISH 🔴" and near_resistance:
            score += 3
            signal = "SELL 🔴"
            checklist.append("Near H4 Resistance")

        # volume boost
        if vol_ok:
            score += 1
            checklist.append("Volume Confirmed")

        if signal is None:
            continue

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
# 🧠 BROKER SUMMARY ANALYZER
# =========================
# =========================
# 🧠 BROKER SUMMARY ANALYZER
# =========================
def analyze_broker_summary(image_path):

    try:
        img = cv2.imread(image_path)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # sharpen OCR
        gray = cv2.GaussianBlur(gray, (3,3), 0)

        text = pytesseract.image_to_string(gray)

        # =========================
        # PARSE BROKER
        # =========================
        brokers = []

        lines = text.splitlines()

        pattern = r'([A-Z]{2})\s+([\d\.]+[BMK]?)'

        for line in lines:

            match = re.findall(pattern, line)

            if match:

                for m in match:

                    broker = m[0]
                    value = m[1]

                    brokers.append((broker, value))

        # =========================
        # SMART MONEY LOGIC
        # =========================
        big_buy = []
        big_sell = []

        for b in brokers:

            broker = b[0]
            val = b[1]

            if "B" in val:
                numeric = float(val.replace("B",""))
                numeric *= 1000

            elif "M" in val:
                numeric = float(val.replace("M",""))

            else:
                numeric = 0

            # dummy smart money classify
            if numeric > 500:
                big_buy.append((broker, numeric))
            else:
                big_sell.append((broker, numeric))

        # =========================
        # OUTPUT
        # =========================
        text_out = "🧠 BROKER SUMMARY ANALYSIS\n"
        text_out += "━━━━━━━━━━━━━━\n\n"

        text_out += "🔥 BIG ACCUMULATION\n"

        for b in big_buy[:5]:
            text_out += f"• {b[0]} → {b[1]:.0f}M\n"

        text_out += "\n🔻 DISTRIBUTION\n"

        for b in big_sell[:5]:
            text_out += f"• {b[0]} → {b[1]:.0f}M\n"

        # =========================
        # SIGNAL ENGINE
        # =========================
        if len(big_buy) > len(big_sell):
            signal = "🟢 ACCUMULATION"
            insight = "Bandar cenderung collecting"
        else:
            signal = "🔴 DISTRIBUTION"
            insight = "Tekanan jual masih dominan"

        text_out += f"""

━━━━━━━━━━━━━━
🎯 SIGNAL: {signal}

💡 Insight:
{insight}
"""

        return text_out

    except Exception as e:
        return f"❌ Error analyze broker summary:\n{e}"

# =========================
# 🧠 BSJP PRO (FIXED + SMART MONEY)
# =========================
def bsjp_scan():
    
    results = []

    # 🔥 PARALLEL FETCH
    with ThreadPoolExecutor(max_workers=10) as executor:
        data_list = list(executor.map(fetch_symbol, BSJP_LIST))

    # 🔁 LOOP HASIL
    for symbol, df in data_list:

        if df is None:
            continue

        close = S(df["Close"])
        open_ = S(df["Open"])
        high = S(df["High"])
        low = S(df["Low"])
        volume = S(df["Volume"])

        price = close.iloc[-1]
        prev_close = close.iloc[-2] if len(close) > 1 else price
        change_pct = ((price - prev_close) / prev_close) * 100 if prev_close != 0 else 0

        # =========================
        # SMART MONEY ENGINE
        # =========================
        vol_mean = volume.rolling(20).mean()
        vol_std = volume.rolling(20).std()
        vol_z = (volume.iloc[-1] - vol_mean.iloc[-1]) / vol_std.iloc[-1] if vol_std.iloc[-1] != 0 else 0

        range_high = high.rolling(20).max().iloc[-2]
        range_low = low.rolling(20).min().iloc[-2]

        base_low = low.rolling(10).min().iloc[-1]
        base_high = high.rolling(10).max().iloc[-1]

        breakout = price > range_high
        breakdown = price < range_low

        position = (price - range_low) / (range_high - range_low) if range_high != range_low else 0.5

        is_base = position < 0.4
        is_prebreak = 0.7 < position < 0.95

        # =========================
        # SCORING
        # =========================
        score = 0
        checklist = []

        if vol_z > 3:
            score += 4
            checklist.append(f"VOLUME Z={vol_z:.2f} 🚀🚀")
        elif vol_z > 2:
            score += 3
            checklist.append(f"Volume Spike Z={vol_z:.2f} 🚀")
        elif vol_z > 1:
            score += 1
            checklist.append(f"Volume Active Z={vol_z:.2f}")

        if breakout:
            score += 2
            checklist.append("BREAKOUT 🚀🔥")

        if breakdown:
            score += 2
            checklist.append("BREAKDOWN 🔻")

        if 0.90 < position < 0.98 and vol_z > 1:
            score += 3
            checklist.append("PRE-BREAK ⚡️")

        if position < 0.3 and vol_z > 1:
            score += 2
            checklist.append("ACCUMULATION 🟡")

        if price > open_.iloc[-1]:
            score += 1
            checklist.append("BUY PRESSURE 🟢")

        # =========================
        # CLASSIFICATION
        # =========================
        if score >= 9:
            label = "BREAK 🚀🚀"
            strength = "STRONG FLOW"
        elif score >= 7:
            label = "BREAK 🚀"
            strength = "HIGH FLOW"
        elif score >= 5:
            label = "PRE-BREAK ⚡️"
            strength = "BUILDING FLOW"
        elif score >= 3:
            label = "ACCUMULATION 🟡"
            strength = "EARLY FLOW"
        else:
            continue

        # =========================
        # ENTRY LOGIC (FIXED)
        # =========================
        if is_base:
            entry = base_low * 1.01
            sl = base_low * 0.97
            tp = range_high
            entry_type = "BASE ENTRY 🟡"

        elif is_prebreak:
            entry = base_high * 1.01
            sl = base_low * 0.98
            tp = range_high * 1.05
            entry_type = "PRE-BREAK ENTRY ⚡️"

        elif breakout:
            entry = range_high * 1.01
            sl = base_low * 0.98
            tp = range_high * 1.08
            entry_type = "BREAKOUT ENTRY 🚀"

        else:
            continue

        # ❌ Hindari entry terlalu atas
        if position > 0.95:
            continue

        # =========================
        # RISK CALC
        # =========================
        sl_pct = ((sl - entry) / entry) * 100
        tp_pct = ((tp - entry) / entry) * 100
        rr = abs((tp - entry) / (entry - sl)) if entry != sl else 0

        if rr < 1:
            continue

        # =========================
        # SAVE RESULT
        # =========================
        results.append({
            "symbol": symbol,
            "score": score,
            "vol_z": vol_z,
            "label": label,
            "strength": strength,
            "entry": entry,
            "entry_type": entry_type,
            "sl": sl,
            "tp": tp,
            "sl_pct": sl_pct,
            "tp_pct": tp_pct,
            "rr": rr,
            "checklist": checklist,
            "change_pct": change_pct,
        })

    # =========================
    # OUTPUT
    # =========================
    if not results:
        return "❌ Tidak ada setup BSJP MAX V2"

    results.sort(key=lambda x: x["score"], reverse=True)

    text = "🔥 BSJP MAX V2 (SMART MONEY FLOW)\n"
    text += "━━━━━━━━━━━━━━━━━━\n\n"

    for r in results[:5]:
        text += f"""📊 {r['symbol']}.JK
💰 Price: {r['entry']:.2f} ({r['change_pct']:+.2f}%)
Score: {r['score']} | Z-Vol: {r['vol_z']:.2f}
{r['strength']}

{r['label']}
{' | '.join(r['checklist'])}

💰 Entry: {r['entry']:.2f} ({r['entry_type']})
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
# COMMANDS
# =========================
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
📊 MENU BOT

/scanall Tunggu 7 menit
/scan Kode Emiten
/news
/news Kode Emiten
/bsjp Tunggu 7 menit
/daily Tunggu 7 menit
/snr Kode Emiten
/snd Kode Emiten
/sndc Kode Emiten
/rsi 🔥 (RSI Oversold)
/bs Analyze Broker Summary Image
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
# 📸 BROKER SUMMARY IMAGE
# =========================
async def broker_summary_image(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.photo:
        return

    await update.message.reply_text("📸 Membaca Broker Summary...")

    photo = update.message.photo[-1]

    file = await context.bot.get_file(photo.file_id)

    path = f"temp/broker_{update.message.message_id}.jpg"

    await file.download_to_drive(path)

    result = await asyncio.to_thread(analyze_broker_image, path)

    await update.message.reply_text(result)


    

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

# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()


    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("scan", scan))
    app.add_handler(CommandHandler("scanall", scanall))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("bsjp", bsjp))
    app.add_handler(CommandHandler("daily", lambda u, c: u.message.reply_text(daily_report_ihsg())))
    app.add_handler(CommandHandler("snd", snd))
    app.add_handler(CommandHandler("sndc", sndc))
    app.add_handler(CommandHandler("snr", snr))
    app.add_handler(CommandHandler("rsi", rsi))
    app.add_handler(MessageHandler(filters.PHOTO, broker_summary_image))
    

    print("🚀 Bot KokoKiki Ready")
    app.run_polling()

if __name__ == "__main__":
    main()
