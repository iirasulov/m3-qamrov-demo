"""Maktablar qamrovi: Toshkent shahri va viloyati.

Modul 3 (GIS) · 9-dars namoyishi. Bufer radiusini tanlang:
maktabdan shu masofadan uzoqda yashovchi aholi qayta hisoblanadi.
"""
from pathlib import Path

import folium
import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import streamlit as st
from rasterio import features
from streamlit_folium import st_folium

DATA = Path(__file__).parent / "data"
METRIK_CRS = 32642          # UTM 42N — masofa va bufer metrda

st.set_page_config(page_title="Maktablar qamrovi", page_icon="🏫", layout="wide")


# ---------- Ma'lumotlarni bir marta yuklash ----------
@st.cache_resource
def yuklash():
    tumanlar = gpd.read_file(DATA / "qamrov_data.gpkg", layer="tumanlar")
    maktablar = gpd.read_file(DATA / "qamrov_data.gpkg", layer="maktablar")
    with rasterio.open(DATA / "aholi_100m_tuzatilgan.tif") as r:
        aholi = r.read(1).astype("float64")
        transform = r.transform
    aholi[aholi < 0] = 0
    tuman_id = features.rasterize(
        ((g, i + 1) for i, g in enumerate(tumanlar.geometry)),
        out_shape=aholi.shape, transform=transform, fill=0)
    return tumanlar, maktablar, aholi, transform, tuman_id


@st.cache_data
def hisoblash(radius_km: float) -> pd.DataFrame:
    """Har tumanda maktabdan radius_km dan uzoqdagi aholi."""
    tumanlar, maktablar, aholi, transform, tuman_id = yuklash()
    bufer = maktablar.to_crs(METRIK_CRS).buffer(radius_km * 1000).union_all()
    bufer = gpd.GeoSeries([bufer], crs=METRIK_CRS).to_crs(4326).iloc[0]
    ichida = features.rasterize([(bufer, 1)], out_shape=aholi.shape, transform=transform, fill=0)
    tash = np.bincount(tuman_id.ravel(), weights=(aholi * (1 - ichida)).ravel(),
                       minlength=len(tumanlar) + 1)[1:]
    df = tumanlar[["district_soato", "district_name_uz", "hudud", "aholi_2026"]].copy()
    df["uzoqda"] = tash.round()
    df["uzoqda_%"] = (tash / df["aholi_2026"] * 100).round(1)
    return df


tumanlar, maktablar, _, _, _ = yuklash()

# ---------- Chap panel ----------
st.sidebar.header("Sozlamalar")
radius = st.sidebar.slider("Maktabgacha masofa, km", 0.5, 3.0, 1.0, 0.5)
hudud = st.sidebar.radio("Hudud", ["Ikkalasi", "Toshkent shahri", "Toshkent viloyati"])
st.sidebar.caption("Masofa — to'g'ri chiziq bo'yicha. Aholi — WorldPop 2026, "
                   "har tumanda stat.uz'ga moslangan (barcha yoshdagilar).")

natija = hisoblash(radius)
if hudud != "Ikkalasi":
    natija = natija[natija["hudud"] == hudud]

# ---------- Asosiy raqamlar ----------
st.title("Maktabdan uzoqda kim qoladi?")
jami = natija["aholi_2026"].sum()
uzoq = natija["uzoqda"].sum()
k1, k2, k3 = st.columns(3)
k1.metric("Aholi", f"{jami:,.0f}".replace(",", " "))
k2.metric(f"{radius:g} km dan uzoqda", f"{uzoq:,.0f}".replace(",", " "))
k3.metric("Ulushi", f"{uzoq / jami * 100:.1f}%")

# ---------- Xarita ----------
CHEGARALAR = [0, 5, 15, 30, 100]
RANGLAR = ["#FEF0D9", "#FDCC8A", "#FC8D59", "#D7301F"]


def rang(v):
    for i in range(4):
        if v <= CHEGARALAR[i + 1]:
            return RANGLAR[i]
    return RANGLAR[-1]


xarita_df = tumanlar.merge(natija[["district_soato", "uzoqda", "uzoqda_%"]], on="district_soato")
xarita_df["geometry"] = xarita_df.simplify(0.0005)          # xarita tez ochilishi uchun
M = folium.Map(location=[41.2, 69.5], zoom_start=9, tiles="OpenStreetMap")
folium.GeoJson(
    xarita_df.to_json(),
    style_function=lambda f: {"fillColor": rang(f["properties"]["uzoqda_%"]), "color": "#FFFFFF",
                              "weight": 0.8, "fillOpacity": 0.75},
    tooltip=folium.GeoJsonTooltip(["district_name_uz", "aholi_2026", "uzoqda", "uzoqda_%"],
                                  aliases=["Tuman", "Aholi", "Uzoqda", "Uzoqda, %"]),
).add_to(M)
mk = folium.FeatureGroup(name="Maktablar", show=False)
for p, n in zip(maktablar.geometry, maktablar["name"]):
    folium.CircleMarker([p.y, p.x], radius=2, color="#08306B", fill=True, tooltip=n).add_to(mk)
mk.add_to(M)
folium.LayerControl().add_to(M)

chap, ong = st.columns([3, 2])
with chap:
    st_folium(M, height=560, use_container_width=True, returned_objects=[])
    st.caption("Rang: maktabdan uzoqdagi aholi ulushi — 5% gacha · 5–15% · 15–30% · 30% dan ko'p")
with ong:
    st.subheader("Eng og'ir 10 ta tuman")
    top = (natija.sort_values("uzoqda_%", ascending=False).head(10)
           [["district_name_uz", "aholi_2026", "uzoqda", "uzoqda_%"]]
           .rename(columns={"district_name_uz": "Tuman", "aholi_2026": "Aholi",
                            "uzoqda": "Uzoqda", "uzoqda_%": "%"}))
    st.dataframe(top, hide_index=True, width="stretch")
    st.caption("Nazorat (8-dars): ikki hudud, 1 km → ≈ 1,12 mln (17,7%); 2 km → ≈ 163 ming (2,6%).")
