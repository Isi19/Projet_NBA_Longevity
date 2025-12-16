import streamlit as st, requests

API_URL = "http://127.0.0.1:8000"

st.title("🏀 NBA Longevity Demo")

# (label, min, max, default, type)
FIELDS = [
    ("gp", 0, 100, 75, int),
    ("min", 0.0, 48.0, 24.3, float),
    ("pts", 0.0, 90.0, 11.2, float),
    ("fgm", 0.0, 40.0, 4.3, float),
    ("fga", 0.0, 60.0, 9.7, float),
    ("fg_pct", 0.0, 100, 44.5, float),
    ("three_p_made", 0.0, 20.0, 1.6, float),
    ("three_p_attempts", 0.0, 30.0, 4.5, float),
    ("three_p_pct", 0.0, 100.0, 35.5, float),
    ("ftm", 0.0, 20.0, 1.1, float),
    ("fta", 0.0, 30.0, 1.3, float),
    ("ft_pct", 0.0, 100, 82, float),
    ("oreb", 0.0, 20.0, 0.8, float),
    ("dreb", 0.0, 30.0, 3.1, float),
    ("reb", 0.0, 40.0, 3.9, float),
    ("ast", 0.0, 30.0, 2.4, float),
    ("stl", 0.0, 15.0, 0.9, float),
    ("blk", 0.0, 15.0, 0.3, float),
    ("tov", 0.0, 20.0, 1.7, float),
]

cols = st.columns(3)
values = {}
for i, (name, vmin, vmax, default, typ) in enumerate(FIELDS):
    with cols[i % 3]:
        if typ is int:
            values[name] = int(st.number_input(name.upper(), min_value=int(vmin), max_value=int(vmax), value=int(default)))
        else:
            values[name] = float(st.number_input(name.upper(), min_value=float(vmin), max_value=float(vmax), value=float(default), step=0.001 if "pct" in name else 0.1))

threshold = st.slider("Seuil (threshold)", 0.0, 1.0, 0.5, 0.01)

if st.button("🔮 Scorer"):
    try:
        r = requests.post(f"{API_URL}/predict", params={"threshold": threshold}, json=values, timeout=15)
        r.raise_for_status()
        st.success("OK ✅")
        st.json(r.json())
    except Exception as e:
        st.error(f"Erreur: {e}")
        try:
            st.json(r.json())
        except:
            pass
