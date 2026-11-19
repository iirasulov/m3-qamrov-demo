# Maktablar qamrovi — Streamlit ilovasi (9-dars namoyishi)

Bufer radiusini (0,5–3 km) tanlang — maktabdan shu masofadan uzoqda yashovchi aholi har bir tuman uchun qayta hisoblanadi.

## Fayllar

| Fayl | Nima |
|---|---|
| `app.py` | ilova kodi |
| `requirements.txt` | kerakli kutubxonalar |
| `.streamlit/config.toml` | ranglar (Link Data) |
| `data/qamrov_data.gpkg` | tumanlar (stat.uz aholisi) va maktablar |
| `data/aholi_100m_tuzatilgan.tif` | aholi rastri (WorldPop 2026, stat.uz'ga moslangan) |

## Internetga joylash (bir marta, ~20 daqiqa)

1. **GitHub** → New repository → nomi `m3-qamrov-demo`.
   Ma'lumot ochiqligini tekshiring: kerak bo'lsa **Private** tanlang.
2. Repozitoriyga shu papkadagi hamma narsani yuklang
   (Add file → Upload files; `.streamlit` papkasi ham, `data` papkasi ham).
3. **share.streamlit.io** → GitHub bilan kiring → **Create app** →
   Repository: `m3-qamrov-demo`, Branch: `main`, Main file: `app.py`.
   Advanced settings → Python 3.11 → **Deploy**.
4. 3–5 daqiqada `https://….streamlit.app` havolasi chiqadi.
   Private repo bo'lsa: Settings → Sharing → ko'rishi kerak bo'lganlarning email manzillarini qo'shing.

**Darsdan 10 daqiqa oldin havolani oching** — bepul ilova uxlab qolgan bo'lsa, uyg'onishi 30–60 soniya oladi.

## O'z kompyuterda ishga tushirish (zaxira)

```
pip install -r requirements.txt
streamlit run app.py
```
Brauzerda `http://localhost:8501` ochiladi.

## Nazorat qiymatlari (8-dars bilan bir xil)

| Hudud | Radius | Uzoqda |
|---|---|---|
| Ikkalasi | 1 km | 1 119 352 (17,7%) |
| Ikkalasi | 2 km | 162 791 (2,6%) |
| Toshkent shahri | 2 km | 5 877 (0,2%) |

## Darsda ko'rsatish (3–5 daqiqa)

1. Slayderni 1 → 2 → 3 km ga suring: «uzoqda» raqami qanday kamayadi.
2. Hududni «Toshkent shahri» / «viloyati» ga almashtiring: farq qayerda?
3. `app.py` ni 30 soniya ko'rsating: «~100 qator, Claude yozdi; men raqamlarni 8-dars natijasi bilan tekshirdim».
4. Loyihada Streamlit — **ixtiyoriy** (+5 ball).
