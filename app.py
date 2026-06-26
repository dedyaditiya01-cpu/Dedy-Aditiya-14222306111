import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Survei Kepuasan Mahasiswa",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS minimal — hanya warna & sidebar permanen
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* Background gelap */
.stApp { background-color: #0e1117 !important; }

/* Sidebar permanen & gelap */
section[data-testid="stSidebar"] {
    background-color: #161b27 !important;
    border-right: 1px solid #1e2d4a !important;
}
section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #1e2d4a !important;
    border: 1px solid #2d4a6b !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: #1e2d4a !important;
    border-radius: 10px !important;
    padding: 12px !important;
    border: 1px solid #2d4a6b !important;
}
section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    color: #60a5fa !important; font-size: 1.5rem !important; font-weight: 800 !important;
}

/* Sidebar selalu tampil permanen */
section[data-testid="stSidebar"] {
    min-width: 280px !important;
    max-width: 320px !important;
    transform: none !important;
    left: 0 !important;
    display: block !important;
    visibility: visible !important;
}

/* Sembunyikan hanya tombol panah < > saja */
[data-testid="collapsedControl"]    { display: none !important; }
button[aria-label="Close sidebar"]  { display: none !important; }
button[aria-label="Open sidebar"]   { display: none !important; }
.st-emotion-cache-1dp5vir { display: none !important; }
.st-emotion-cache-pkbazv  { display: none !important; }
.css-1dp5vir { display: none !important; }
.css-pkbazv  { display: none !important; }

/* Main content */
.main .block-container {
    padding: 20px 28px 40px !important;
    max-width: 1400px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #161b27 !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid #1e2d4a !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #64748b !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    border-radius: 8px !important;
    padding: 10px 18px !important;
}
.stTabs [aria-selected="true"] {
    background: #1e3a5f !important;
    color: #60a5fa !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 20px !important; }

/* Metric cards warna gelap */
[data-testid="metric-container"] {
    background: #161b27 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 14px !important;
    padding: 18px !important;
}
[data-testid="stMetricValue"]  { color: #f1f5f9 !important; font-weight: 800 !important; }
[data-testid="stMetricLabel"]  { color: #64748b !important; font-size: 0.78rem !important; }
[data-testid="stMetricDelta"]  { font-size: 0.75rem !important; }

/* Dataframe */
.stDataFrame { border: 1px solid #1e2d4a !important; border-radius: 12px !important; }

/* Download button */
.stDownloadButton > button {
    background: #1e2d4a !important; border: 1px solid #2d4a6b !important;
    color: #60a5fa !important; border-radius: 8px !important; font-weight: 600 !important;
}

/* Selectbox global */
.stSelectbox > div > div {
    background: #161b27 !important; border: 1px solid #1e2d4a !important;
    border-radius: 8px !important; color: #e2e8f0 !important;
}
.stSelectbox label { color: #94a3b8 !important; }

/* Divider */
hr { border-color: #1e2d4a !important; }
#MainMenu, footer, header { visibility: hidden !important; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0e1117; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 99px; }
</style>
""", unsafe_allow_html=True)


# ── Load data ──────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("Survei_kepuasan_mahasiswa__Responses_.xlsx")
    df.columns = [
        "Timestamp", "Nama", "Kelas", "NIM",
        "Kursi & Meja", "Suhu Udara", "Proyektor (LCD)",
        "Stop Kontak", "Kedap Suara", "Kebersihan",
        "Kenyamanan Keseluruhan",
    ]
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df

df = load_data()
ASPEK = df.columns[4:].tolist()

ASPEK_INFO = {
    "Kursi & Meja":           {"icon": "🪑", "desc": "Ketersediaan kursi & meja"},
    "Suhu Udara":             {"icon": "❄️", "desc": "Kenyamanan suhu ruangan"},
    "Proyektor (LCD)":        {"icon": "📽️", "desc": "Fungsi proyektor & layar"},
    "Stop Kontak":            {"icon": "🔌", "desc": "Ketersediaan colokan listrik"},
    "Kedap Suara":            {"icon": "🔇", "desc": "Minimnya gangguan suara"},
    "Kebersihan":             {"icon": "🧹", "desc": "Kebersihan lantai & meja"},
    "Kenyamanan Keseluruhan": {"icon": "😊", "desc": "Nyaman belajar 2 jam"},
}

WARNA_KELAS = {"Pagi": "#f59e0b", "Malam A": "#3b82f6", "Malam B": "#a855f7"}
C_HIJAU  = "#22c55e"
C_KUNING = "#eab308"
C_MERAH  = "#ef4444"

def status_warna(pct):
    if pct >= 75:   return C_HIJAU,  "🟢 Baik"
    elif pct >= 55: return C_KUNING, "🟡 Cukup"
    else:           return C_MERAH,  "🔴 Perlu Perhatian"


# ══════════════════════════════════════════════════════
#  SIDEBAR — PERMANEN
# ══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🎓 Survei Kepuasan")
    st.caption("Mahasiswa Teknik Industri · Fasilitas Kelas")
    st.divider()

    st.markdown("**⚙️ Filter Data**")
    kelas_pilihan = st.selectbox(
        "Pilih Kelas",
        ["Semua Kelas"] + sorted(df["Kelas"].unique().tolist()),
    )

    df_f        = df if kelas_pilihan == "Semua Kelas" else df[df["Kelas"] == kelas_pilihan]
    avg_global  = (df_f[ASPEK] == 1).mean().mean() * 100
    aspek_best  = (df_f[ASPEK] == 1).mean().idxmax()
    aspek_worst = (df_f[ASPEK] == 1).mean().idxmin()

    st.divider()
    st.markdown("**📊 Statistik Cepat**")
    st.metric("👥 Total Responden",  len(df_f))
    st.metric("✅ Rata-rata Puas",   f"{avg_global:.1f}%")
    st.metric("🏫 Jumlah Kelas",     df_f["Kelas"].nunique())

    st.divider()
    st.markdown("**🏷️ Kelas & Kepuasan**")
    for k, w in WARNA_KELAS.items():
        sub_k  = df[df["Kelas"] == k]
        avg_k  = (sub_k[ASPEK] == 1).mean().mean() * 100
        c, stxt = status_warna(avg_k)
        st.markdown(
            f"<div style='background:#1e2d4a;border-left:3px solid {w};"
            f"border-radius:8px;padding:8px 12px;margin-bottom:6px;'>"
            f"<span style='color:#e2e8f0;font-weight:700;font-size:.85rem;'>Kelas {k}</span>"
            f"<span style='float:right;color:{c};font-weight:700;font-size:.85rem;'>{avg_k:.0f}%</span>"
            f"<br><span style='color:#475569;font-size:.73rem;'>{len(sub_k)} mahasiswa · {stxt}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    st.divider()
    st.markdown("**📌 Keterangan Skala**")
    st.markdown(
        "<div style='background:#1e2d4a;border-radius:8px;padding:10px 12px;"
        "font-size:.82rem;line-height:1.7;'>"
        "<span style='color:#22c55e;font-weight:700;'>1 = Ya / Puas</span> — sudah memadai<br>"
        "<span style='color:#ef4444;font-weight:700;'>2 = Tidak</span> — perlu perbaikan"
        "</div>",
        unsafe_allow_html=True
    )
    st.divider()
    st.caption("📅 Data: Maret 2026")


# ══════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════
df_f       = df if kelas_pilihan == "Semua Kelas" else df[df["Kelas"] == kelas_pilihan]
avg_global = (df_f[ASPEK] == 1).mean().mean() * 100
aspek_best  = (df_f[ASPEK] == 1).mean().idxmax()
aspek_worst = (df_f[ASPEK] == 1).mean().idxmin()
pct_best    = (df_f[ASPEK] == 1).mean().max() * 100
pct_worst   = (df_f[ASPEK] == 1).mean().min() * 100
kelas_label = kelas_pilihan if kelas_pilihan != "Semua Kelas" else "Pagi · Malam A · Malam B"

st.markdown(
    f"<div style='background:linear-gradient(135deg,#0f172a,#1e1b4b,#0f172a);"
    f"border:1px solid #1e3a5f;border-radius:18px;padding:26px 30px;margin-bottom:20px;'>"
    f"<div style='color:#3b82f6;font-size:.7rem;font-weight:700;letter-spacing:2px;"
    f"text-transform:uppercase;margin-bottom:8px;'>"
    f"📋 Program Studi Teknik Industri · Fasilitas Ruang Kelas</div>"
    f"<div style='color:#f1f5f9;font-size:1.7rem;font-weight:800;'>"
    f"Dashboard Survei Kepuasan Mahasiswa</div>"
    f"<div style='margin-top:12px;font-size:.8rem;color:#94a3b8;'>"
    f"🏫 {kelas_label} &nbsp;·&nbsp; 👥 {len(df_f)} Responden &nbsp;·&nbsp; "
    f"<span style='color:#4ade80;font-weight:700;'>✅ {avg_global:.1f}% Puas</span></div>"
    f"</div>",
    unsafe_allow_html=True
)

# ── KPI Cards ──────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4, gap="medium")
c1.metric("👥 Total Responden",  len(df_f),          f"{df_f['Kelas'].nunique()} kelas")
c2.metric("✅ Rata-rata Puas",   f"{avg_global:.1f}%", "Seluruh aspek")
c3.metric(f"⭐ Terbaik",         f"{pct_best:.0f}%",   f"{ASPEK_INFO[aspek_best]['icon']} {aspek_best}")
c4.metric(f"⚠️ Perhatian",       f"{pct_worst:.0f}%",  f"{ASPEK_INFO[aspek_worst]['icon']} {aspek_worst}")

st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Ringkasan Utama",
    "🔍  Detail Per Aspek",
    "🏫  Perbandingan Kelas",
    "📋  Data Lengkap",
])


# ─── TAB 1 — RINGKASAN ────────────────────────────────
with tab1:
    col_l, col_r = st.columns([3, 2], gap="large")

    with col_l:
        st.markdown("#### 📈 Tingkat Kepuasan Per Aspek")
        st.caption("Diurutkan dari yang tertinggi ke terendah. "
                   "🟢 ≥75%  |  🟡 55–74%  |  🔴 <55%")

        pct_ser = (df_f[ASPEK] == 1).mean() * 100

        # Plotly horizontal bar
        bar_df = pd.DataFrame({
            "Aspek": [f"{ASPEK_INFO[a]['icon']} {a}" for a in ASPEK],
            "Puas":  pct_ser.values,
            "Warna": [status_warna(p)[0] for p in pct_ser.values],
        }).sort_values("Puas")

        fig_hbar = go.Figure()
        fig_hbar.add_trace(go.Bar(
            x=bar_df["Puas"], y=bar_df["Aspek"],
            orientation="h",
            marker=dict(color=bar_df["Warna"], line=dict(width=0)),
            text=[f"  {p:.1f}%" for p in bar_df["Puas"]],
            textposition="outside",
            textfont=dict(color="#e2e8f0", size=13, family="Inter"),
            hovertemplate="<b>%{y}</b><br>%{x:.1f}% Puas<extra></extra>",
        ))
        fig_hbar.update_layout(
            height=340, margin=dict(t=10, b=10, l=10, r=60),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(range=[0, 118], showgrid=True, gridcolor="#1e2d4a",
                       tickfont=dict(color="#64748b"), ticksuffix="%"),
            yaxis=dict(tickfont=dict(color="#e2e8f0", size=12)),
            showlegend=False,
        )
        st.plotly_chart(fig_hbar, use_container_width=True,
                        config={"displayModeBar": False})

    with col_r:
        st.markdown("#### 🥧 Ya vs Tidak (Keseluruhan)")
        st.caption("Total seluruh jawaban dari semua aspek fasilitas")

        total_ya    = int((df_f[ASPEK] == 1).sum().sum())
        total_tidak = int((df_f[ASPEK] == 2).sum().sum())

        fig_pie = go.Figure(go.Pie(
            labels=["✅ Ya / Puas", "❌ Tidak / Kurang"],
            values=[total_ya, total_tidak],
            hole=0.62,
            marker=dict(colors=[C_HIJAU, C_MERAH],
                        line=dict(color="#0e1117", width=3)),
            textinfo="percent",
            textfont=dict(size=13, color="white"),
            hovertemplate="<b>%{label}</b><br>%{value} jawaban (%{percent})<extra></extra>",
        ))
        fig_pie.update_layout(
            showlegend=False, height=250,
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10, b=0, l=0, r=0),
            annotations=[dict(
                text=f"<b>{avg_global:.0f}%</b><br>Puas",
                x=0.5, y=0.5,
                font=dict(size=20, color="#f1f5f9", family="Inter"),
                showarrow=False,
            )],
        )
        st.plotly_chart(fig_pie, use_container_width=True,
                        config={"displayModeBar": False})

        # Angka ringkas
        col_ya, col_tdk = st.columns(2)
        with col_ya:
            st.metric("✅ Ya", total_ya, f"{total_ya/(total_ya+total_tidak)*100:.0f}%")
        with col_tdk:
            st.metric("❌ Tidak", total_tidak,
                      f"-{total_tidak/(total_ya+total_tidak)*100:.0f}%")

    # Heatmap
    st.markdown("---")
    st.markdown("#### 🌡️ Peta Kepuasan — Kelas × Aspek")
    st.caption("Angka = % mahasiswa yang menjawab Ya. "
               "Merah = rendah → Kuning = sedang → Hijau = tinggi")

    heat = df_f.groupby("Kelas")[ASPEK].apply(lambda g: (g == 1).mean() * 100)
    xlbl = [f"{ASPEK_INFO[a]['icon']} {a}" for a in ASPEK]

    fig_h = px.imshow(
        heat.values, x=xlbl, y=heat.index.tolist(),
        color_continuous_scale=[[0, C_MERAH], [0.5, C_KUNING], [1, C_HIJAU]],
        zmin=0, zmax=100, text_auto=".0f", aspect="auto", height=190,
    )
    fig_h.update_traces(
        textfont=dict(size=15, color="white", family="Inter"),
        hovertemplate="<b>%{y}</b> — %{x}<br>%{z:.1f}% Puas<extra></extra>",
    )
    fig_h.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=5, b=5, l=5, r=5), coloraxis_showscale=False,
        xaxis=dict(tickfont=dict(size=11, color="#94a3b8")),
        yaxis=dict(tickfont=dict(size=13, color="#e2e8f0")),
    )
    st.plotly_chart(fig_h, use_container_width=True,
                    config={"displayModeBar": False})


# ─── TAB 2 — DETAIL PER ASPEK ─────────────────────────
with tab2:
    st.markdown("#### 🔍 Pilih Aspek untuk Melihat Detail")

    opts = [f"{ASPEK_INFO[a]['icon']}  {a}" for a in ASPEK]
    sel  = st.selectbox("Aspek Fasilitas", opts, label_visibility="collapsed")
    selected = sel.split("  ", 1)[1]

    pct_ya  = (df_f[selected] == 1).mean() * 100
    n_ya    = int((df_f[selected] == 1).sum())
    n_tidak = int((df_f[selected] == 2).sum())
    clr, stxt = status_warna(pct_ya)

    # Ringkasan aspek pakai metric native
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(f"{ASPEK_INFO[selected]['icon']} Aspek", selected)
    m2.metric("% Puas", f"{pct_ya:.1f}%", stxt)
    m3.metric("✅ Menjawab Ya",    n_ya)
    m4.metric("❌ Menjawab Tidak", n_tidak)

    st.caption(f"📝 {ASPEK_INFO[selected]['desc']}")
    st.markdown("---")

    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        st.markdown("**Perbandingan Ya vs Tidak**")
        fig_b = go.Figure(go.Bar(
            x=["✅ Ya / Puas", "❌ Tidak / Kurang"],
            y=[n_ya, n_tidak],
            marker=dict(color=[C_HIJAU, C_MERAH],
                        line=dict(color="#0e1117", width=2)),
            text=[f"{n_ya} ({pct_ya:.0f}%)", f"{n_tidak} ({100-pct_ya:.0f}%)"],
            textposition="outside",
            textfont=dict(color="#e2e8f0", size=13),
            width=[0.4, 0.4],
        ))
        fig_b.update_layout(
            height=320,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=30, b=20), showlegend=False,
            font=dict(color="#94a3b8"),
            yaxis=dict(showgrid=True, gridcolor="#1e2d4a",
                       range=[0, max(n_ya, n_tidak) * 1.35],
                       tickfont=dict(color="#64748b")),
            xaxis=dict(tickfont=dict(size=13, color="#e2e8f0")),
        )
        st.plotly_chart(fig_b, use_container_width=True,
                        config={"displayModeBar": False})

    with col_b:
        st.markdown("**Breakdown Per Kelas**")
        rows = []
        for k in sorted(df["Kelas"].unique()):
            sub = df_f[df_f["Kelas"] == k]
            if not len(sub): continue
            ny = int((sub[selected] == 1).sum())
            nt = int((sub[selected] == 2).sum())
            rows.append({"Kelas": k, "Ya": ny, "Tidak": nt,
                         "pct": ny / len(sub) * 100})
        bd = pd.DataFrame(rows)
        if len(bd):
            fig_k = go.Figure()
            fig_k.add_trace(go.Bar(
                name="✅ Ya", x=bd["Kelas"], y=bd["Ya"],
                marker=dict(color=C_HIJAU),
                text=bd["Ya"], textposition="auto",
                textfont=dict(color="white", size=12),
            ))
            fig_k.add_trace(go.Bar(
                name="❌ Tidak", x=bd["Kelas"], y=bd["Tidak"],
                marker=dict(color=C_MERAH),
                text=bd["Tidak"], textposition="auto",
                textfont=dict(color="white", size=12),
            ))
            fig_k.update_layout(
                barmode="group", height=320,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10, b=20), font=dict(color="#94a3b8"),
                legend=dict(orientation="h", y=-0.2,
                            font=dict(color="#94a3b8"),
                            bgcolor="rgba(0,0,0,0)"),
                yaxis=dict(showgrid=True, gridcolor="#1e2d4a",
                           tickfont=dict(color="#64748b")),
                xaxis=dict(tickfont=dict(size=13, color="#e2e8f0")),
            )
            st.plotly_chart(fig_k, use_container_width=True,
                            config={"displayModeBar": False})

    if len(bd):
        bd["% Puas"] = bd["pct"].apply(lambda x: f"{x:.1f}%")
        bd["Status"] = bd["pct"].apply(lambda x: status_warna(x)[1])
        st.dataframe(bd[["Kelas","Ya","Tidak","% Puas","Status"]],
                     use_container_width=True, hide_index=True)


# ─── TAB 3 — PERBANDINGAN KELAS ───────────────────────
with tab3:
    st.markdown("#### 🏆 Ringkasan Per Kelas")

    kelas_list = sorted(df["Kelas"].unique())
    cols_k = st.columns(len(kelas_list), gap="medium")
    for col, k in zip(cols_k, kelas_list):
        sub   = df[df["Kelas"] == k]
        avg_k = (sub[ASPEK] == 1).mean().mean() * 100
        best  = (sub[ASPEK] == 1).mean().idxmax()
        worst = (sub[ASPEK] == 1).mean().idxmin()
        c, st_txt = status_warna(avg_k)
        with col:
            st.metric(
                label=f"🏫 Kelas {k} — {len(sub)} mhs",
                value=f"{avg_k:.1f}%",
                delta=st_txt,
            )
            st.caption(
                f"⭐ Terbaik: {ASPEK_INFO[best]['icon']} {best}\n\n"
                f"⚠️ Perhatian: {ASPEK_INFO[worst]['icon']} {worst}"
            )

    st.markdown("---")
    st.markdown("#### 📊 Perbandingan Per Aspek Antar Kelas")
    st.caption("Setiap kelompok bar mewakili satu aspek fasilitas")

    rows = []
    for k in kelas_list:
        sub = df[df["Kelas"] == k]
        for a in ASPEK:
            rows.append({
                "Kelas": k,
                "Aspek": f"{ASPEK_INFO[a]['icon']} {a}",
                "% Puas": (sub[a] == 1).mean() * 100,
            })
    comp_df = pd.DataFrame(rows)

    fig_grp = px.bar(
        comp_df, x="Aspek", y="% Puas", color="Kelas",
        barmode="group", height=420,
        color_discrete_map=WARNA_KELAS,
        text=comp_df["% Puas"].apply(lambda x: f"{x:.0f}%"),
    )
    fig_grp.update_traces(textposition="outside",
                          textfont=dict(size=11, color="white"))
    fig_grp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        xaxis=dict(tickangle=-15, tickfont=dict(size=11, color="#94a3b8"),
                   gridcolor="#1e2d4a"),
        yaxis=dict(range=[0, 130], showgrid=True, gridcolor="#1e2d4a",
                   ticksuffix="%", tickfont=dict(color="#64748b")),
        margin=dict(t=30, b=100, l=10, r=10),
        legend=dict(orientation="h", y=-0.22,
                    font=dict(size=12, color="#94a3b8"),
                    bgcolor="rgba(0,0,0,0)", title_text=""),
    )
    st.plotly_chart(fig_grp, use_container_width=True,
                    config={"displayModeBar": False})

    st.markdown("---")
    st.markdown("#### 🕸️ Radar Chart — Profil Kepuasan Tiap Kelas")
    st.caption("Semakin luas area, semakin tinggi kepuasan di semua aspek")

    rlabels = [f"{ASPEK_INFO[a]['icon']} {a}" for a in ASPEK]
    fig_r = go.Figure()
    for k in kelas_list:
        sub  = df[df["Kelas"] == k]
        vals = [(sub[a] == 1).mean() * 100 for a in ASPEK]
        w    = WARNA_KELAS.get(k, "#64748b")
        fig_r.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=rlabels + [rlabels[0]],
            fill="toself", name=f"Kelas {k}",
            line=dict(color=w, width=2.5),
            fillcolor=w, opacity=0.18,
            hovertemplate="%{theta}<br><b>%{r:.1f}%</b><extra>Kelas " + k + "</extra>",
        ))
    fig_r.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True, range=[0, 105],
                tickvals=[25, 50, 75, 100],
                ticktext=["25%", "50%", "75%", "100%"],
                tickfont=dict(size=10, color="#475569"),
                gridcolor="#1e2d4a", linecolor="#1e2d4a",
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color="#94a3b8"),
                linecolor="#1e2d4a", gridcolor="#1e2d4a",
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)", height=440,
        legend=dict(orientation="h", y=-0.1,
                    font=dict(size=12, color="#94a3b8"),
                    bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=20, b=60, l=50, r=50),
    )
    st.plotly_chart(fig_r, use_container_width=True,
                    config={"displayModeBar": False})


# ─── TAB 4 — DATA LENGKAP ─────────────────────────────
with tab4:
    st.markdown("#### 📋 Data Jawaban Seluruh Responden")
    st.caption(f"Menampilkan {len(df_f)} baris data · "
               f"Kelas: {kelas_pilihan}")

    show = df_f.copy()
    for a in ASPEK:
        show[a] = show[a].map({1: "✅ Ya", 2: "❌ Tidak"})
    show["Timestamp"] = show["Timestamp"].dt.strftime("%d %b %Y, %H:%M")
    show = show.rename(columns={a: f"{ASPEK_INFO[a]['icon']} {a}" for a in ASPEK})
    st.dataframe(show, use_container_width=True, height=380, hide_index=True)

    st.markdown("---")
    dl1, dl2, _ = st.columns([1, 1, 2])
    with dl1:
        st.download_button(
            "⬇️ Download Data (CSV)",
            df_f.to_csv(index=False).encode("utf-8"),
            "data_survei.csv", "text/csv", use_container_width=True,
        )
    with dl2:
        smry = pd.DataFrame({
            "Aspek": [f"{ASPEK_INFO[a]['icon']} {a}" for a in ASPEK],
            "Ya": [(df_f[a] == 1).sum() for a in ASPEK],
            "Tidak": [(df_f[a] == 2).sum() for a in ASPEK],
            "% Puas": [f"{(df_f[a]==1).mean()*100:.1f}%" for a in ASPEK],
            "Status": [status_warna((df_f[a]==1).mean()*100)[1] for a in ASPEK],
        })
        st.download_button(
            "⬇️ Download Ringkasan (CSV)",
            smry.to_csv(index=False).encode("utf-8"),
            "ringkasan.csv", "text/csv", use_container_width=True,
        )

    st.markdown("#### 📊 Ringkasan Statistik Per Aspek")
    st.dataframe(smry, use_container_width=True, hide_index=True)
