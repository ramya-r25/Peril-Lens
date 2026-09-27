from pathlib import Path
import sys
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Peril_Lens_core import (
    security_gate, get_active_data, get_active_features, load_csv, normalize_queue,
    metric_card, safe_num, build_entity_supervisory_overview, build_trend_dataset,
    build_negative_space_findings, build_anomaly_findings, build_manual_review_samples,
    build_traceability, render_data_ingestion_panel, render_ps_coverage_panel,
    priority_counts, render_header, render_sidebar_status,
)
from src.analytics.explainability_engine import build_explanation
from src.reports.organisation_report import build_organisation_report

st.set_page_config(page_title="Peril-Lens | SAT-SA", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# -----------------------------------------------------------------------------
# Professional visual system
# -----------------------------------------------------------------------------
st.markdown("""
<style>
:root { --navy:#0b100f; --panel:#111917; --panel2:#16201d; --line:#283632; --text:#e7eee9; --muted:#89978f; --teal:#27c49a; --blue:#8d7db2; --amber:#d7b45a; --rose:#c87858; }
#MainMenu, footer {visibility:hidden;} header {background:transparent;}
[data-testid="stSidebar"] {background:#0a111d; border-right:1px solid #1d2a3c;}
[data-testid="stSidebarNav"] {padding-top:0.45rem;}
[data-testid="stSidebarNav"] ul {gap:3px;}
[data-testid="stSidebarNav"] li a {border-radius:9px; color:#aebdd0 !important; font-size:13px; padding:9px 12px;}
[data-testid="stSidebarNav"] li a:hover {background:#121f31; color:#f4f8fc !important;}
[data-testid="stSidebarNav"] li a[aria-current="page"] {background:#14283a; color:#ffffff !important; box-shadow:inset 3px 0 0 #27c49a;}
[data-testid="stSidebarNav"] span {font-weight:600;}
.block-container {max-width:1450px; padding-top:1.9rem; padding-bottom:3rem;}
[data-testid="stHeader"] {background:#0b100f;}
[data-testid="stToolbar"] {visibility:hidden;}
.tl-app-header {min-height:74px !important; height:auto !important; padding:4px 0 16px !important; margin-bottom:22px !important;}
.tl-app-status {display:flex;align-items:center;gap:8px;}
.tl-app-header {height:64px; display:flex; align-items:center; justify-content:space-between; padding:0 0 14px; margin-bottom:18px; border-bottom:1px solid #1d2a3c;}
.tl-app-brand,.tl-brand {display:flex; align-items:center; gap:11px;}
.tl-app-mark,.tl-brand-mark {width:39px;height:39px;display:grid;place-items:center;color:#27c49a;background:#102b2b;border:1px solid #24504b;border-radius:11px;}
.tl-app-mark svg,.tl-brand-mark svg {width:25px;height:25px;}
.tl-app-name,.tl-brand-name {font-size:21px;font-weight:800;letter-spacing:-.6px;color:#f7fafc;line-height:1;}
.tl-app-name span,.tl-brand-name span {color:#27c49a;}
.tl-app-sub,.tl-brand-sub {font-size:9px;color:#71849b;letter-spacing:.55px;margin-top:5px;text-transform:uppercase;}
.tl-header-status {font-size:10px;color:#7fa99e;border:1px solid #24443f;background:#0e201f;padding:7px 10px;border-radius:999px;letter-spacing:.7px;font-weight:700;}
.tl-header-status span {display:inline-block;width:6px;height:6px;border-radius:50%;background:#20c49f;margin-right:5px;}
.tl-side-brand {display:flex;align-items:center;gap:9px;padding:7px 2px 4px;color:#f4f8fc;}
.tl-side-brand b {display:block;font-size:16px;letter-spacing:-.2px;}
.tl-side-brand small {display:block;color:#71849b;font-size:9px;margin-top:3px;}
.tl-side-mark {width:27px;height:27px;border-radius:8px;display:grid;place-items:center;background:#102b2b;color:#20c49f;border:1px solid #24504b;font-weight:800;}
.tl-side-divider {height:1px;background:#1d2a3c;margin:11px 0;}
.tl-side-heading {font-size:9px;color:#5f728a;font-weight:800;letter-spacing:1.2px;margin-bottom:7px;}
.tl-context {display:flex;justify-content:space-between;gap:8px;margin:7px 0;font-size:10px;}
.tl-context span {color:#667a91;}
.tl-context b {color:#c8d4e1;text-align:right;max-width:135px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.tl-page-kicker {font-size:10px;font-weight:800;letter-spacing:1.45px;color:#27c49a;text-transform:uppercase;margin-bottom:5px;}
.tl-page-title {font-size:31px;font-weight:800;color:#f5f8fb;letter-spacing:-.8px;line-height:1.08;}
.tl-page-subtitle {font-size:13px;color:#7f91a7;line-height:1.6;max-width:900px;margin:7px 0 22px;}
.tl-hero {padding:28px 31px 26px;border:1px solid #22334a;border-radius:18px;background:linear-gradient(135deg,#0d1726 0%,#102033 60%,#0d1a28 100%);box-shadow:0 18px 45px rgba(0,0,0,.16);}
.tl-hero-kicker {font-size:10px;color:#6e8ca8;letter-spacing:1.6px;font-weight:800;text-transform:uppercase;}
.tl-hero-title {font-size:40px;font-weight:850;color:#f6f9fc;letter-spacing:-1.4px;margin-top:8px;}
.tl-hero-title span {color:#27c49a;}
.tl-hero-copy {font-size:14px;color:#a2b1c2;max-width:790px;line-height:1.7;margin-top:10px;}
.tl-status-line {margin-top:18px;display:flex;gap:9px;align-items:center;color:#79a79e;font-size:10px;font-weight:750;letter-spacing:.7px;}
.tl-status-line i {width:7px;height:7px;border-radius:50%;background:#20c49f;display:inline-block;box-shadow:0 0 9px rgba(32,196,159,.45);}
.tl-selector {padding:16px 18px 17px;border:1px solid #24364d;border-radius:14px;background:#0e1928;margin:18px 0 20px;}
.tl-selector-label {font-size:10px;font-weight:800;letter-spacing:1.1px;color:#7f91a7;text-transform:uppercase;margin-bottom:4px;}
.tl-selector-help {font-size:11px;color:#60748b;margin-bottom:10px;}
.tl-section-head {display:flex;align-items:end;justify-content:space-between;margin:24px 0 11px;}
.tl-section-title {font-size:16px;font-weight:760;color:#e9f0f7;}
.tl-section-note {font-size:10px;color:#647991;}
.tl-card {min-height:108px;padding:16px 17px;border:1px solid #213149;border-radius:14px;background:#101a2a;}
.tl-card-label {font-size:9px;color:#72859b;font-weight:800;letter-spacing:1.05px;text-transform:uppercase;}
.tl-card-value {font-size:27px;color:#f3f7fb;font-weight:800;margin-top:8px;}
.tl-card-note {font-size:10px;color:#63758b;margin-top:5px;line-height:1.45;}
.tl-panel {border:1px solid #213149;border-radius:15px;background:#0f1928;padding:15px 15px 8px;}
.tl-panel-title {font-size:13px;color:#e5edf5;font-weight:750;}
.tl-panel-note {font-size:10px;color:#63768d;margin:3px 0 5px;}
.tl-context-strip {display:flex;gap:18px;flex-wrap:wrap;padding:11px 14px;border:1px solid #213149;border-radius:11px;background:#0e1928;margin-bottom:18px;}
.tl-context-strip span {font-size:10px;color:#647991;}.tl-context-strip b {color:#d8e2ec;font-size:10px;margin-left:4px;}
.tl-callout {padding:13px 15px;border-left:3px solid #27c49a;background:#0d2020;border-radius:8px;color:#aab8c8;font-size:12px;line-height:1.55;}
.tl-flow {display:grid;grid-template-columns:1fr 28px 1fr 28px 1fr;gap:8px;align-items:center;padding:14px;border:1px solid #213149;border-radius:15px;background:#0f1928;}
.tl-flow-box {padding:14px;border-radius:11px;background:#111f31;border:1px solid #24364c;}
.tl-flow-num {font-size:9px;color:#27c49a;font-weight:800;letter-spacing:1px;}.tl-flow-name{font-size:12px;color:#eef4fa;font-weight:750;margin-top:5px}.tl-flow-text{font-size:10px;color:#6e8197;line-height:1.5;margin-top:4px}.tl-arrow{color:#53677f;text-align:center;font-size:17px;}
.tl-login-wrap {max-width:470px;margin:7vh auto 0;}
.tl-login-wrap .tl-brand {justify-content:center;margin-bottom:25px;}
.tl-login-wrap .tl-brand-mark {width:48px;height:48px;border-radius:13px;}.tl-login-wrap .tl-brand-mark svg{width:30px;height:30px;}.tl-login-wrap .tl-brand-name{font-size:26px;}.tl-login-wrap .tl-brand-sub{font-size:9px;}
.tl-login-card {padding:26px 28px 22px;border:1px solid #23364d;border-radius:18px;background:#0e1928;box-shadow:0 24px 70px rgba(0,0,0,.25);}
.tl-login-kicker {font-size:9px;color:#27c49a;font-weight:800;letter-spacing:1.25px;margin-bottom:7px;}.tl-login-title{font-size:23px;font-weight:800;color:#f2f6fa;}.tl-login-copy{font-size:12px;color:#71849a;line-height:1.55;margin:7px 0 19px;}
.tl-login-foot{font-size:9px;color:#5d7188;text-align:center;margin-top:15px;line-height:1.5;}.tl-secure-row{font-size:9px;color:#6d8e86;letter-spacing:.8px;margin-top:14px;text-align:center;font-weight:750;}.tl-secure-dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:#20c49f;margin-right:5px;}
div[data-testid="stMetric"] {background:#101a2a;border:1px solid #213149;padding:10px 12px;border-radius:12px;}
.stButton>button[kind="primary"] {background:#27c49a;border-color:#27c49a;color:#071514;font-weight:800;}
.stButton>button[kind="primary"]:hover {background:#21cbb2;border-color:#21cbb2;}
.stTextInput>div>div>input,.stSelectbox>div>div,.stMultiSelect>div>div {border-color:#26384e;}
div[data-baseweb="select"]>div {background:#0f1a29;border-color:#26384e;}
.stTabs [data-baseweb="tab-list"] {gap:4px;border-bottom:1px solid #213149;}.stTabs [data-baseweb="tab"]{color:#71849a;font-size:11px;font-weight:700;}.stTabs [aria-selected="true"]{color:#f0f5f9!important;}
.tl-note {font-size:10px;color:#62758c;line-height:1.55;}
@media(max-width:900px){.tl-flow{grid-template-columns:1fr;}.tl-arrow{display:none}.tl-hero-title{font-size:31px;}}

.tl-home-intro{padding:10px 0 8px;}
.tl-explain{border:1px solid #213149;background:#0d1827;border-radius:12px;padding:12px 14px;margin:0 0 13px;}
.tl-explain-title{font-size:11px;font-weight:800;color:#eaf1f7;letter-spacing:.3px;}
.tl-explain-text{font-size:10px;color:#7589a0;line-height:1.55;margin-top:4px;}
.tl-chart-takeaway{font-size:9px;color:#84918b;border-top:1px solid #1d2d42;margin-top:4px;padding:8px 2px 3px;line-height:1.5;}
.tl-route{min-height:130px;border:1px solid #213149;border-radius:14px;background:#0f1928;padding:15px;transition:.15s ease;}
.tl-route:hover{border-color:#31506f;background:#111e30;}
.tl-route-num{font-size:9px;font-weight:800;color:#27c49a;letter-spacing:1px;}
.tl-route-title{font-size:13px;font-weight:800;color:#edf4fa;margin-top:8px;}
.tl-route-text{font-size:10px;color:#71859b;line-height:1.55;margin-top:6px;}
.tl-empty{border:1px dashed #2a3b50;background:#0d1827;border-radius:13px;padding:24px;text-align:center;margin:8px 0;}
.tl-empty-title{font-size:13px;font-weight:800;color:#e7eef5;}.tl-empty-text{font-size:10px;color:#71859b;margin-top:5px;}
.tl-case-card{border:1px solid #213149;border-radius:14px;background:#0f1928;padding:16px;}
.tl-case-id{font-size:17px;font-weight:800;color:#edf4fa;margin-bottom:12px;}.tl-case-row{display:flex;justify-content:space-between;gap:15px;padding:8px 0;border-top:1px solid #1d2c40;font-size:10px;color:#71859b;}.tl-case-row b{color:#dce6ef;font-weight:700;text-align:right;}
/* ===== THREATLENS SIDEBAR VISIBILITY FIX ===== */

    [data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        width: 280px !important;
        min-width: 280px !important;
        background: #111827 !important;
    }

    [data-testid="stSidebar"] > div {
        width: 280px !important;
        background: #111827 !important;
    }

    [data-testid="stSidebarContent"] {
        visibility: visible !important;
        display: block !important;
    }

    [data-testid="stSidebarUserContent"] {
        visibility: visible !important;
        display: block !important;
    }

    [data-testid="stSidebar"] * {
        visibility: visible;
    }

    [data-testid="stSidebar"] button {
        visibility: visible !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Chart color system
# -----------------------------------------------------------------------------
# Refined, cohesive palette tuned to sit inside the dark navy shell used above.
# Cooler undertones throughout (teal / slate-indigo / warm gold / muted copper)
# so every chart reads as one family instead of a grab-bag of hues. Key names
# are kept stable since they're referenced across the plotting helpers below.
PALETTE = {
    "emerald": "#22C7A0",   # primary signal — teal, matches brand mark
    "moss": "#5D8BB0",      # secondary comparative series — slate blue
    "gold": "#DCB25E",      # medium priority / warm accent
    "copper": "#D07E5A",    # high priority / alert accent
    "plum": "#8188C4",      # fourth analytical lens — cool indigo
    "ivory": "#E9EEF4",
    "graphite": "#5E7188",
    "track": "#12203A",     # baseline / empty-state fill, matched to panel bg
    "text": "#DCE6EF",
    "muted": "#8093A8",
}

PRIORITY_COLORS = {
    "High": PALETTE["copper"],
    "Medium": PALETTE["gold"],
    "Low": PALETTE["emerald"],
    "Unclassified": PALETTE["graphite"],
}


# Reusable analytical colors for the four Peril-Lens lenses.
LENS_COLORS = [
    PALETTE["emerald"],
    PALETTE["gold"],
    PALETTE["copper"],
    PALETTE["plum"],
]

# Shared cosmetic constants so every chart uses the same border, corner
# radius and gridline treatment — this is what makes a chart set look
# "designed" rather than assembled from defaults.
BAR_LINE_COLOR = "#0F1928"
BAR_CORNER_RADIUS = 6
GRID_COLOR = "rgba(148,163,184,0.09)"
HOVER_BG = "#0c1524"
HOVER_BORDER = "#2b4160"


def style_fig(fig, height=320, show_legend=False):
    """Single restrained visual language for every Peril-Lens Plotly figure."""
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=22, t=22, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=PALETTE["text"], family="Inter, -apple-system, Segoe UI, sans-serif", size=10.5),
        showlegend=show_legend,
        bargap=0.34,
        hoverlabel=dict(
            bgcolor=HOVER_BG,
            bordercolor=HOVER_BORDER,
            font=dict(color="#f4f8fb", size=11, family="Inter, -apple-system, Segoe UI, sans-serif"),
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            font=dict(color="#9fb0c1", size=9.5),
        ),
        transition=dict(duration=200, easing="cubic-in-out"),
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor=GRID_COLOR,
        gridwidth=1,
        zeroline=False,
        showline=False,
        tickfont=dict(size=9.5, color="#96a8bd"),
        title_font=dict(size=10, color=PALETTE["muted"]),
        automargin=True,
    )
    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        showline=False,
        tickfont=dict(size=9.5, color="#96a8bd"),
        title_font=dict(size=10, color=PALETTE["muted"]),
        automargin=True,
    )
    # Rounded bar corners read as far more polished than square bars, and a
    # slightly thinner separator line keeps segments crisp without
    # overwhelming a small chart.
    fig.update_traces(selector=dict(type="bar"), marker_cornerradius=BAR_CORNER_RADIUS)
    return fig


def chart_hover(fig):
    """Keep hover cards consistent and quiet across all charts."""
    fig.update_traces(hoverlabel=dict(bgcolor=HOVER_BG, bordercolor=HOVER_BORDER, font_color="#f4f8fb"))
    return fig


def chart_config():
    """Disable distracting Plotly controls while preserving hover/interaction."""
    return {"displaylogo": False, "modeBarButtonsToRemove": ["lasso2d", "select2d"], "scrollZoom": False}


def _lens_contribution_bar(row, entity_mode=False):
    """Four-lens signal profile as a compact radial column chart."""
    labels=["Execution gaps","Negative space","Peer deviations","Operational patterns"]
    values=[float(v) for v in _lens_values(row)]
    fig=go.Figure(go.Barpolar(
        r=values,theta=labels,
        marker=dict(color=LENS_COLORS,opacity=0.9,line=dict(color=BAR_LINE_COLOR,width=1.8)),
        text=[f"{int(v)}" for v in values],
        hovertemplate="<b>%{theta}</b><br>Findings: %{r:.0f}<extra></extra>",
    ))
    fig.update_layout(
        margin=dict(l=35,r=35,t=30,b=35),showlegend=False,
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(range=[0,max(max(values)*1.2,1)],showticklabels=True,tickfont=dict(size=8,color=PALETTE["muted"]),gridcolor=GRID_COLOR,linecolor=GRID_COLOR),
            angularaxis=dict(direction="clockwise",rotation=90,gridcolor=GRID_COLOR,linecolor=GRID_COLOR,tickfont=dict(size=10,color=PALETTE["muted"])),
        ),
    )
    return fig


def _entity_signal_stack(p):
    """Annotated heatmap for comparing every entity and analytical lens."""
    if p.empty:
        return go.Figure()
    cols=[("execution_gaps","Execution gaps"),("negative_space","Negative space"),("peer_deviations","Peer deviations"),("operational_patterns","Operational patterns")]
    available=[c for c in cols if c[0] in p.columns]
    if not available:
        return go.Figure()
    d=p[["entity_name"]+[c[0] for c in available]].copy()
    for c,_ in available: d[c]=pd.to_numeric(d[c],errors="coerce").fillna(0.0)
    d["total"]=d[[c for c,_ in available]].sum(axis=1); d=d.sort_values("total",ascending=False)
    z=d[[c for c,_ in available]].astype(float).to_numpy()
    fig=go.Figure(go.Heatmap(
        z=z,x=[label for _,label in available],y=d["entity_name"].astype(str),
        colorscale=[[0,"#142237"],[0.45,PALETTE["moss"]],[1,PALETTE["gold"]]],
        text=z.astype(int),texttemplate="%{text}",textfont=dict(size=10,color=PALETTE["ivory"]),
        colorbar=dict(title="Findings",thickness=10,tickfont=dict(color=PALETTE["muted"])),
        hovertemplate="<b>%{y}</b><br>%{x}: %{z:.0f} findings<extra></extra>",
        xgap=3,ygap=3,
    ))
    fig.update_layout(margin=dict(l=10,r=22,t=42,b=22),xaxis=dict(title="Analytical lens",side="top",showgrid=False),yaxis=dict(title="",autorange="reversed",showgrid=False))
    return fig


def _lens_values(row):
    return [safe_num(row.get("execution_gap_findings", row.get("execution_gaps", 0))), safe_num(row.get("negative_space_findings", row.get("negative_space", 0))), safe_num(row.get("peer_deviation_findings", row.get("peer_deviations", 0))), safe_num(row.get("operational_pattern_findings", row.get("operational_patterns", 0)))]


def _radar_figure(labels, values, title_text=None, colors=None, max_value=None):
    """Polished radar/spider chart used for multi-signal fingerprints."""
    labels=list(labels); values=[float(v) for v in values]
    if not labels: return go.Figure()
    max_value=max(1.0,max(values)*1.25) if max_value is None else max_value
    closed_labels=labels+[labels[0]]; closed_values=values+[values[0]]
    line_color=(colors or [PALETTE["emerald"]])[0]
    marker_color=(colors or [PALETTE["gold"], PALETTE["emerald"]])[-1]
    fig=go.Figure(go.Scatterpolar(
        r=closed_values,theta=closed_labels,mode="lines+markers",fill="toself",
        fillcolor=_hex_rgba(line_color,0.16),
        line=dict(color=line_color,width=2.5,shape="spline",smoothing=0.35),
        marker=dict(size=7,color=marker_color,line=dict(color="#0b1220",width=2)),
        hovertemplate="<b>%{theta}</b><br>Signal count: %{r:.0f}<extra></extra>",showlegend=False,
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True,range=[0,max_value],showticklabels=False,gridcolor="rgba(148,163,184,.14)",linecolor="rgba(148,163,184,.14)"),
            angularaxis=dict(gridcolor="rgba(148,163,184,.14)",linecolor="rgba(148,163,184,.14)",tickfont=dict(size=10,color="#B7C6D6")),
        ),
        title=dict(text=title_text or "",font=dict(size=11,color=PALETTE["muted"]),x=0.02,xanchor="left"),
        margin=dict(l=25,r=25,t=35,b=20),
    )
    return fig


def _hex_rgba(hex_color, alpha=0.32):
    h=str(hex_color).lstrip("#")
    if len(h)!=6:
        return f"rgba(93,139,176,{alpha})"
    r,g,b=int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"



def _priority_donut(q, title_text="Queue composition"):
    """Compact priority mix; refined donut with a clean center metric and
    a slight pull on the leading slice for visual hierarchy."""
    if q.empty:
        return go.Figure()
    counts=q["priority"].value_counts()
    order=[x for x in ["High","Medium","Low","Unclassified"] if x in counts.index]
    order += [x for x in counts.index.tolist() if x not in order]
    values=[int(counts.get(x,0)) for x in order]
    colors=[PRIORITY_COLORS.get(x,PALETTE["graphite"]) for x in order]
    top_idx=values.index(max(values)) if values else 0
    pulls=[0.03 if i==top_idx else 0 for i in range(len(values))]
    fig=go.Figure(go.Pie(
        labels=order,
        values=values,
        hole=0.72,
        sort=False,
        direction="clockwise",
        rotation=90,
        pull=pulls,
        marker=dict(colors=colors,line=dict(color="#0c1526",width=3)),
        textinfo="label+percent",
        textfont=dict(size=10,color=PALETTE["ivory"]),
        hovertemplate="<b>%{label}</b><br>Assessments: %{value}<br>Share: %{percent}<extra></extra>",
    ))
    fig.add_annotation(
        x=0.5,y=0.53,text=f"<b style='font-size:22px'>{len(q)}</b>",
        showarrow=False,font=dict(color=PALETTE["ivory"]),
    )
    fig.add_annotation(
        x=0.5,y=0.42,text="<span style='font-size:9px;letter-spacing:.5px'>ASSESSMENTS</span>",
        showarrow=False,font=dict(color=PALETTE["muted"]),
    )
    fig.update_layout(
        margin=dict(l=10,r=10,t=15,b=10),
        showlegend=False,
    )
    return fig


def _portfolio_attention_area(q, top_n=12):
    """Area profile for the command centre, showing how attention builds across the portfolio."""
    if q.empty:
        return go.Figure()
    d=q.sort_values(["score","assessment_id"],ascending=[True,True]).tail(top_n).copy()
    d["label"]=d.apply(lambda r:f"{r['assessment_id']} · {r['entity_name']}",axis=1)
    x=list(range(1,len(d)+1))
    custom=d[["label","priority"]].astype(str).to_numpy()
    fig=go.Figure()
    fig.add_trace(go.Scatter(
        x=x,y=d["score"].astype(float),mode="lines",
        line=dict(color=PALETTE["emerald"],width=2.5,shape="spline",smoothing=0.55),
        fill="tozeroy",fillcolor=_hex_rgba(PALETTE["emerald"],0.18),
        customdata=custom,
        hovertemplate="<b>%{customdata[0]}</b><br>Priority: %{customdata[1]}<br>Attention score: %{y:.1f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=x,y=d["score"].astype(float),mode="markers",showlegend=False,
        marker=dict(size=8,color=[PRIORITY_COLORS.get(str(v),PALETTE["graphite"]) for v in d["priority"]],line=dict(color=BAR_LINE_COLOR,width=1.5)),
        customdata=custom,
        hovertemplate="<b>%{customdata[0]}</b><br>Priority: %{customdata[1]}<br>Attention score: %{y:.1f}<extra></extra>",
    ))
    fig.update_layout(
        margin=dict(l=12,r=24,t=12,b=42),showlegend=False,
        xaxis=dict(title="Portfolio rank · lower to higher attention",tickmode="array",tickvals=x,ticktext=[str(i) for i in x],showgrid=False),
        yaxis=dict(title="Attention score",rangemode="tozero",showgrid=True,gridcolor=GRID_COLOR),
        hovermode="x unified",
    )
    return fig


def _queue_composition_strip(q):
    """Priority distribution as labelled columns for immediate count comparison."""
    if q.empty:
        return go.Figure()
    counts=q["priority"].value_counts()
    order=[x for x in ["High","Medium","Low","Unclassified"] if x in counts.index]
    order += [x for x in counts.index.tolist() if x not in order]
    total=max(int(counts.sum()),1)
    values=[int(counts.get(priority,0)) for priority in order]
    shares=[100.0*value/total for value in values]
    fig=go.Figure(go.Bar(
        x=order,y=values,
        marker=dict(color=[PRIORITY_COLORS.get(priority,PALETTE["graphite"]) for priority in order],line=dict(color=BAR_LINE_COLOR,width=1.6)),
        text=[f"{value}<br>{share:.0f}%" for value,share in zip(values,shares)],textposition="outside",cliponaxis=False,
        textfont=dict(size=11,color=PALETTE["ivory"]),customdata=shares,
        hovertemplate="<b>%{x}</b><br>Assessments: %{y}<br>Queue share: %{customdata:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        margin=dict(l=10,r=20,t=35,b=35),showlegend=False,
        xaxis=dict(title="Routing priority",showgrid=False),
        yaxis=dict(title="Assessments",dtick=1,rangemode="tozero",showgrid=True,gridcolor=GRID_COLOR),bargap=0.42,
    )
    return fig


def _attention_rank_bar(q, top_n=8):
    """Ranked horizontal bar: direct comparison of review attention scores."""
    if q.empty:
        return go.Figure()
    d=q.sort_values(["score","assessment_id"],ascending=[True,True]).tail(top_n).copy()
    d["label"]=d.apply(lambda r:f"{r['assessment_id']} · {r['entity_name']}",axis=1)
    colors=[PRIORITY_COLORS.get(str(v),PALETTE["graphite"]) for v in d["priority"]]
    fig=go.Figure(go.Bar(
        x=d["score"].astype(float),
        y=d["label"],
        orientation="h",
        marker=dict(color=colors,line=dict(color=BAR_LINE_COLOR,width=1.4)),
        text=d["score"].map(lambda x:f"{x:.1f}"),
        textposition="outside",
        textfont=dict(size=10.5,color=PALETTE["ivory"]),
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Attention score: %{x:.1f}<extra></extra>",
    ))
    fig.update_layout(
        margin=dict(l=10,r=48,t=10,b=25),
        showlegend=False,
        xaxis=dict(title="Attention score",zeroline=False),
        yaxis=dict(tickfont=dict(size=10,color=PALETTE["muted"])),
        bargap=0.32,
    )
    return fig


def _entity_attention_lollipop(p):
    """Entity ranking as a restrained lollipop chart with an average reference line."""
    if p.empty:
        return go.Figure()
    d=p.sort_values(["attention_score","entity_name"],ascending=[True,True]).copy()
    scores=d["attention_score"].astype(float)
    colors=[PALETTE["copper"] if x>=15 else PALETTE["gold"] if x>=7 else PALETTE["emerald"] for x in scores]
    fig=go.Figure()
    for _,row in d.iterrows():
        fig.add_shape(type="line",x0=0,x1=float(row["attention_score"]),y0=str(row["entity_name"]),y1=str(row["entity_name"]),line=dict(color=_hex_rgba(PALETTE["graphite"],0.55),width=2))
    fig.add_trace(go.Scatter(
        x=scores,y=d["entity_name"].astype(str),mode="markers+text",
        marker=dict(size=13,color=colors,line=dict(color=BAR_LINE_COLOR,width=2)),
        text=[f"{x:.1f}" for x in scores],textposition="middle right",textfont=dict(size=10,color=PALETTE["ivory"]),
        customdata=d[["entity_id","sector"]].astype(str).to_numpy(),
        hovertemplate="<b>%{y}</b><br>Attention score: %{x:.1f}<br>Entity: %{customdata[0]}<br>Sector: %{customdata[1]}<extra></extra>",
    ))
    average=float(scores.mean()) if len(scores) else 0.0
    fig.add_vline(x=average,line_width=1,line_dash="dot",line_color=PALETTE["moss"],annotation_text=f"Average {average:.1f}",annotation_position="top")
    fig.update_layout(
        margin=dict(l=10,r=62,t=28,b=28),showlegend=False,
        xaxis=dict(title="Attention score",rangemode="tozero",zeroline=False),
        yaxis=dict(tickfont=dict(size=10,color=PALETTE["muted"])),
    )
    return fig


def _sector_signal_bar(p):
    """Compare sector-level average attention without distribution gimmicks."""
    if p.empty or "sector" not in p.columns:
        return go.Figure()
    d=p.groupby("sector",as_index=False)["attention_score"].mean().sort_values("attention_score",ascending=True)
    fig=go.Figure(go.Bar(
        x=d["attention_score"],
        y=d["sector"],
        orientation="h",
        marker=dict(color=PALETTE["moss"],line=dict(color=BAR_LINE_COLOR,width=1.4)),
        text=d["attention_score"].map(lambda x:f"{x:.1f}"),
        textposition="outside",
        textfont=dict(size=10.5,color=PALETTE["ivory"]),
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Average attention: %{x:.1f}<extra></extra>",
    ))
    fig.update_layout(
        margin=dict(l=10,r=48,t=10,b=25),
        showlegend=False,
        xaxis=dict(title="Average attention score",zeroline=False),
        yaxis=dict(tickfont=dict(size=10,color=PALETTE["muted"])),
        bargap=0.34,
    )
    return fig


def _negative_space_bubbles(negative):
    """Grouped severity columns for direct missing-evidence comparisons."""
    if negative.empty:
        return go.Figure()
    tmp=negative.loc[:,~negative.columns.duplicated(keep="first")].copy()
    if "entity_id" not in tmp.columns: tmp["entity_id"]="Unknown"
    if "severity" not in tmp.columns: tmp["severity"]="Unknown"
    tmp["entity_id"]=tmp["entity_id"].fillna("Unknown").astype(str)
    tmp["severity"]=tmp["severity"].fillna("Unknown").astype(str)
    counts=tmp.groupby(["entity_id","severity"],dropna=False).size().reset_index(name="count")
    severity_order=[x for x in ["Critical","High","Medium","Low","Unknown"] if x in counts["severity"].unique()]
    severity_colors={"Critical":PALETTE["copper"],"High":"#D9945F","Medium":PALETTE["gold"],"Low":PALETTE["emerald"],"Unknown":PALETTE["graphite"]}
    fig=go.Figure()
    for severity in severity_order:
        d=counts[counts["severity"].eq(severity)]
        fig.add_trace(go.Bar(
            x=d["entity_id"],y=d["count"],name=severity,
            marker=dict(color=severity_colors.get(severity,PALETTE["graphite"]),line=dict(color=BAR_LINE_COLOR,width=1.2)),
            text=d["count"].astype(int).astype(str),textposition="outside",cliponaxis=False,
            hovertemplate=f"<b>%{{x}}</b><br>Severity: {severity}<br>Missing-evidence findings: %{{y}}<extra></extra>",
        ))
    fig.update_layout(
        barmode="group",margin=dict(l=15,r=20,t=45,b=38),showlegend=True,
        legend=dict(orientation="h",y=1.14,x=0,font=dict(size=9,color=PALETTE["muted"])),
        xaxis=dict(title="Entity",showgrid=False),yaxis=dict(title="Missing-evidence findings",dtick=1,rangemode="tozero",showgrid=True,gridcolor=GRID_COLOR),
    )
    return fig


def _operational_pattern_bubbles(anomalies):
    """Annotated matrix for locating repeated operational patterns quickly."""
    if anomalies.empty:
        return go.Figure()
    tmp=anomalies.loc[:,~anomalies.columns.duplicated(keep="first")].copy()
    if "entity_id" not in tmp.columns: tmp["entity_id"]="Unknown"
    if "signal" not in tmp.columns: tmp["signal"]="Unclassified"
    tmp["entity_id"]=tmp["entity_id"].fillna("Unknown").astype(str)
    tmp["signal"]=tmp["signal"].fillna("Unclassified").astype(str)
    d=tmp.groupby(["entity_id","signal"]).size().reset_index(name="count")
    matrix=d.pivot(index="entity_id",columns="signal",values="count").fillna(0)
    matrix=matrix.loc[matrix.sum(axis=1).sort_values(ascending=False).index,matrix.sum(axis=0).sort_values(ascending=False).index]
    z=matrix.astype(float).to_numpy()
    fig=go.Figure(go.Heatmap(
        z=z,x=matrix.columns.astype(str),y=matrix.index.astype(str),
        colorscale=[[0,"#142237"],[0.5,PALETTE["plum"]],[1,PALETTE["copper"]]],
        text=z.astype(int),texttemplate="%{text}",textfont=dict(size=10,color=PALETTE["ivory"]),
        colorbar=dict(title="Records",thickness=10,tickfont=dict(color=PALETTE["muted"])),
        hovertemplate="<b>%{y}</b><br>Pattern: %{x}<br>Affected records: %{z:.0f}<extra></extra>",xgap=3,ygap=3,
    ))
    fig.update_layout(
        margin=dict(l=15,r=20,t=42,b=65),showlegend=False,
        xaxis=dict(title="Operational pattern",side="top",tickangle=-18,showgrid=False),
        yaxis=dict(title="Entity",autorange="reversed",showgrid=False),
    )
    return fig


def _operational_bar(anomalies):
    """Simple ranked comparison for repeated operational patterns."""
    if anomalies.empty:
        return go.Figure()
    pat=anomalies.groupby("signal",as_index=False).size().rename(columns={"size":"count"})
    pat=pat.sort_values(["count","signal"],ascending=[True,True])
    fig=go.Figure(go.Bar(
        x=pat["count"],
        y=pat["signal"],
        orientation="h",
        marker=dict(color=PALETTE["plum"],line=dict(color=BAR_LINE_COLOR,width=1.4)),
        text=pat["count"].astype(int).astype(str),
        textposition="outside",
        textfont=dict(size=10.5,color=PALETTE["ivory"]),
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Affected records: %{x}<extra></extra>",
    ))
    fig.update_layout(
        margin=dict(l=10,r=48,t=10,b=25),
        showlegend=False,
        xaxis=dict(title="Affected records",dtick=1,zeroline=False),
        yaxis=dict(tickfont=dict(size=10,color=PALETTE["muted"])),
        bargap=0.34,
    )
    return fig


def _execution_gap_lollipop(ex):
    """Simple columns with exact labels for deterministic execution-gap signals."""
    if ex.empty:
        return go.Figure()
    d=ex.sort_values(["count","signal"],ascending=[False,True]).copy()
    colors=[PALETTE["copper"],PALETTE["gold"],PALETTE["emerald"]][:len(d)]
    fig=go.Figure(go.Bar(
        x=d["signal"].astype(str),y=d["count"].astype(float),
        marker=dict(color=colors,line=dict(color=BAR_LINE_COLOR,width=1.6)),
        text=d["count"].astype(int).astype(str),textposition="outside",cliponaxis=False,textfont=dict(size=11,color=PALETTE["ivory"]),
        customdata=d[["definition"]].astype(str).to_numpy(),
        hovertemplate="<b>%{x}</b><br>Records: %{y:.0f}<br>%{customdata[0]}<extra></extra>",
    ))
    fig.update_layout(
        margin=dict(l=10,r=25,t=32,b=38),showlegend=False,
        xaxis=dict(title="Execution-gap rule",showgrid=False),
        yaxis=dict(title="Affected records",dtick=1,rangemode="tozero",showgrid=True,gridcolor=GRID_COLOR),
    )
    return fig


def page_title(kicker,title,subtitle):
    st.markdown(f"<div class='tl-page-kicker'>{kicker}</div><div class='tl-page-title'>{title}</div><div class='tl-page-subtitle'>{subtitle}</div>", unsafe_allow_html=True)


def simple_card(label,value,note):
    st.markdown(f"<div class='tl-card'><div class='tl-card-label'>{label}</div><div class='tl-card-value'>{value}</div><div class='tl-card-note'>{note}</div></div>", unsafe_allow_html=True)


def queue_view(queue, entities=None):
    q = normalize_queue(queue).copy()
    if "entity_id" in q.columns:
        if entities is None:
            entities = load_csv("entities.csv")
        if not entities.empty and "entity_id" in entities.columns:
            # Only add entity attributes that are missing from the queue. This
            # avoids entity_name_x/entity_name_y columns and keeps the chart
            # labels deterministic.
            missing_cols = [
                c for c in ["entity_name", "sector", "entity_size"]
                if c not in q.columns and c in entities.columns
            ]
            if missing_cols:
                cols = ["entity_id"] + missing_cols
                q = q.merge(
                    entities[cols].drop_duplicates("entity_id"),
                    on="entity_id",
                    how="left",
                )
    return q


def selected_assessment():
    return st.session_state.get("tl_selected_assessment", "ALL")


def assessment_options(data):
    a=data.get("assessments",pd.DataFrame())
    if a.empty or "assessment_id" not in a.columns: return ["ALL"]
    rows=[]
    for _,r in a.iterrows():
        aid=str(r.get("assessment_id","")); ent=str(r.get("entity_id",""));
        start=str(r.get("period_start","")); end=str(r.get("period_end",""))
        label=f"{aid} · {ent} · {start} to {end}".strip(" ·")
        rows.append((aid,label))
    return ["ALL"] + rows


def set_assessment_from_home(data):
    options=assessment_options(data)
    ids=[x if isinstance(x,str) else x[0] for x in options]
    labels={"ALL":"All assessments"}
    labels.update({x[0]:x[1] for x in options if not isinstance(x,str)})
    current=selected_assessment()
    if current not in ids: current="ALL"
    idx=ids.index(current)
    chosen=st.selectbox("Assessment focus", ids, index=idx, format_func=lambda x:labels.get(x,x), key="home_assessment_selector")
    st.session_state.tl_selected_assessment=chosen
    return chosen


def scope_data(data, queue):
    aid=selected_assessment()
    if aid=="ALL": return data,queue
    q=queue[queue["assessment_id"].astype(str)==str(aid)].copy() if "assessment_id" in queue.columns else queue
    scoped={k:(v.copy() if isinstance(v,pd.DataFrame) else v) for k,v in data.items()}
    if "assessments" in scoped and "assessment_id" in scoped["assessments"].columns: scoped["assessments"]=scoped["assessments"][scoped["assessments"]["assessment_id"].astype(str)==str(aid)]
    if "cases" in scoped and "assessment_id" in scoped["cases"].columns:
        scoped["cases"]=scoped["cases"][scoped["cases"]["assessment_id"].astype(str)==str(aid)]
    if "alerts" in scoped and "assessment_id" in scoped["alerts"].columns:
        scoped["alerts"]=scoped["alerts"][scoped["alerts"]["assessment_id"].astype(str)==str(aid)]
    if "monitoring" in scoped and "assessment_id" in scoped["monitoring"].columns:
        scoped["monitoring"]=scoped["monitoring"][scoped["monitoring"]["assessment_id"].astype(str)==str(aid)]
    case_ids=set(scoped.get("cases",pd.DataFrame()).get("case_id",pd.Series(dtype=str)).astype(str))
    if "investigations" in scoped and "case_id" in scoped["investigations"].columns: scoped["investigations"]=scoped["investigations"][scoped["investigations"]["case_id"].astype(str).isin(case_ids)]
    if "escalations" in scoped and "case_id" in scoped["escalations"].columns: scoped["escalations"]=scoped["escalations"][scoped["escalations"]["case_id"].astype(str).isin(case_ids)]
    return scoped,q


def context_strip(data):
    aid=selected_assessment()
    if aid=="ALL":
        st.markdown("<div class='tl-context-strip'><span>Assessment focus <b>All assessments</b></span><span>Source <b>"+ ("Validated submission" if st.session_state.get("tl_active_source")=="uploaded" else "Demonstration dataset") +"</b></span></div>",unsafe_allow_html=True)
    else:
        a=data.get("assessments",pd.DataFrame()); r=a[a["assessment_id"].astype(str)==str(aid)] if "assessment_id" in a.columns else pd.DataFrame()
        entity=str(r.iloc[0].get("entity_id","")) if not r.empty else ""
        period=f"{r.iloc[0].get('period_start','')} → {r.iloc[0].get('period_end','')}" if not r.empty else ""
        st.markdown(f"<div class='tl-context-strip'><span>Assessment <b>{aid}</b></span><span>Entity <b>{entity}</b></span><span>Period <b>{period}</b></span></div>",unsafe_allow_html=True)


def section_note(title, text):
    st.markdown(
        f"<div class='tl-explain'><div class='tl-explain-title'>{title}</div><div class='tl-explain-text'>{text}</div></div>",
        unsafe_allow_html=True,
    )


def plot_panel(title, subtitle, fig, height=320, takeaway=None, show_legend=False):
    st.markdown(
        f"<div class='tl-panel'><div class='tl-panel-title'>{title}</div><div class='tl-panel-note'>{subtitle}</div>",
        unsafe_allow_html=True,
    )
    st.plotly_chart(style_fig(fig, height, show_legend), width="stretch", theme=None, config=chart_config())
    if takeaway:
        st.markdown(f"<div class='tl-chart-takeaway'><b>How to read:</b> {takeaway}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def empty_state(title, message):
    st.markdown(
        f"<div class='tl-empty'><div class='tl-empty-title'>{title}</div><div class='tl-empty-text'>{message}</div></div>",
        unsafe_allow_html=True,
    )


def page_home():
    data, queue = get_active_data()
    st.markdown(
        "<div class='tl-home-intro'><div class='tl-page-kicker'>Peril-Lens · SAT-SA</div>"
        "<div class='tl-page-title'>Supervisory Command Center</div>"
        "<div class='tl-page-subtitle'>Start with an assessment, understand its evidence scope, then move into the analytical workspace only when deeper review is required.</div></div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='tl-selector-label'>ASSESSMENT FOCUS</div>", unsafe_allow_html=True)
    st.markdown("<div class='tl-selector-help'>Choose the assessment that will remain the working context across the supervisory workspace.</div>", unsafe_allow_html=True)
    chosen = set_assessment_from_home(data)
    scoped, q = scope_data(data, queue)
    context_strip(scoped)

    entities = scoped.get("entities", pd.DataFrame())
    assessments = scoped.get("assessments", pd.DataFrame())
    alerts = scoped.get("alerts", pd.DataFrame())
    cases = scoped.get("cases", pd.DataFrame())

    st.markdown("<div class='tl-section-head'><div class='tl-section-title'>Assessment snapshot</div><div class='tl-section-note'>Context only — supervisory findings are kept in the dedicated workspaces.</div></div>", unsafe_allow_html=True)
    if chosen == "ALL":
        facts = [
            ("CSEs represented", len(entities), "Entities in the available dataset"),
            ("Assessments", len(assessments), "Assessment periods available"),
            ("Security alerts", len(alerts), "Alert records submitted"),
            ("Case records", len(cases), "Case-management records"),
        ]
    else:
        facts = [
            ("Entity", str(assessments.iloc[0].get("entity_id", "—")) if not assessments.empty else "—", "Selected assessment owner"),
            ("Assessment period", f"{assessments.iloc[0].get('period_start','—')} → {assessments.iloc[0].get('period_end','—')}" if not assessments.empty else "—", "Submission window"),
            ("Security alerts", len(alerts), "Operational evidence available"),
            ("Case records", len(cases), "Cases available for examination"),
        ]
    cols = st.columns(4)
    for c, (label, value, note) in zip(cols, facts):
        with c:
            simple_card(label, f"{value:,}" if isinstance(value, int) else str(value), note)

    st.markdown("<div class='tl-section-head'><div class='tl-section-title'>Supervisory portfolio</div><div class='tl-section-note'>Two conventional views: queue composition and ranked attention.</div></div>", unsafe_allow_html=True)
    q_home = normalize_queue(queue_view(q, scoped.get("entities", pd.DataFrame()))).copy()
    if not q_home.empty:
        q_home["score"] = pd.to_numeric(q_home.get("score", 0), errors="coerce").fillna(0.0)
        q_home["priority"] = q_home.get("priority", "Unclassified").fillna("Unclassified").astype(str)
        q_home["assessment_id"] = q_home.get("assessment_id", "").astype(str)
        q_home["entity_name"] = q_home.get("entity_name", q_home.get("entity_id", "Entity")).fillna("Entity").astype(str)
        c1,c2=st.columns([0.9,1.6],gap="large")
        with c1:
            plot_panel(
                "Priority composition",
                "How the current review portfolio is distributed by routing priority.",
                _priority_donut(q_home), 380,
                "Use the composition to understand the portfolio mix, then use the ranked view for exact candidates.",
                False,
            )
        with c2:
            plot_panel(
                "Attention profile",
                "Area profile of attention scores from lower to higher across the current portfolio.",
                _portfolio_attention_area(q_home), 380,
                "The rising profile shows where attention concentrates; hover over a point to inspect the assessment and priority.",
                False,
            )
    else:
        empty_state("No portfolio visualization", "The active dataset does not contain a prioritised assessment queue.")

    st.markdown("<div class='tl-section-head'><div class='tl-section-title'>Where to go next</div><div class='tl-section-note'>Each workspace has one clear purpose.</div></div>", unsafe_allow_html=True)
    cards = [
        ("01", "Review Queue", "See which assessments or entities deserve attention first."),
        ("02", "Entity Intelligence", "Compare CSEs and inspect the signal fingerprint of one entity."),
        ("03", "Evidence Analytics", "Understand the operational signal behind a finding."),
        ("04", "Case Review", "Inspect representative evidence before forming a supervisory view."),
    ]
    cols = st.columns(4)
    for c, (num, title, text_) in zip(cols, cards):
        with c:
            st.markdown(f"<div class='tl-route'><div class='tl-route-num'>{num}</div><div class='tl-route-title'>{title}</div><div class='tl-route-text'>{text_}</div></div>", unsafe_allow_html=True)


def page_queue():
    data, queue = get_active_data()
    q = normalize_queue(queue_view(queue, data.get("entities", pd.DataFrame()))).copy()
    page_title("SUPERVISION / 01", "Review Queue", "A decision-ready worklist for manual supervisory review.")
    if q.empty:
        empty_state("No review candidates", "The current dataset does not contain a prioritised supervisory review queue.")
        return

    q["assessment_id"] = q.get("assessment_id", pd.Series(dtype=str)).astype(str)
    q["entity_id"] = q.get("entity_id", pd.Series(dtype=str)).astype(str)
    q["entity_name"] = q.get("entity_name", q["entity_id"]).fillna(q["entity_id"]).astype(str)
    q["priority"] = q.get("priority", "Unclassified").fillna("Unclassified").astype(str)
    q["score"] = pd.to_numeric(q.get("score", 0), errors="coerce").fillna(0.0)

    lens_columns = [
        ("execution_gap_findings", "execution_gaps", "Execution gaps"),
        ("negative_space_findings", "negative_space", "Negative space"),
        ("peer_deviation_findings", "peer_deviations", "Peer deviations"),
        ("operational_pattern_findings", "operational_patterns", "Operational patterns"),
    ]
    for primary, fallback, label in lens_columns:
        source = primary if primary in q.columns else fallback
        q[label] = pd.to_numeric(q[source], errors="coerce").fillna(0.0) if source in q.columns else 0.0
    lens_labels = [item[2] for item in lens_columns]
    q["dominant_signal"] = q[lens_labels].idxmax(axis=1)
    q.loc[q[lens_labels].sum(axis=1).eq(0), "dominant_signal"] = "No lens findings"
    q = q.sort_values(["score", "assessment_id"], ascending=[False, True]).reset_index(drop=True)

    st.markdown("<div class='tl-section-head'><div class='tl-section-title'>Triage controls</div><div class='tl-section-note'>Narrow the worklist without changing its supervisory order.</div></div>", unsafe_allow_html=True)
    control_left, control_right = st.columns([1, 1.4], gap="large")
    priority_order = [p for p in ["High", "Medium", "Low", "Unclassified"] if p in set(q["priority"])]
    with control_left:
        priorities = st.multiselect("Priority", priority_order, default=priority_order, key="queue_priority_filter")
    with control_right:
        search = st.text_input("Find assessment or entity", placeholder="Type an ID or entity name", key="queue_text_filter").strip()

    filtered = q[q["priority"].isin(priorities)].copy() if priorities else q.iloc[0:0].copy()
    if search:
        match_text = filtered["assessment_id"].str.cat(filtered["entity_name"], sep=" ")
        filtered = filtered[match_text.str.contains(search, case=False, regex=False)]

    summary_cols = st.columns(4)
    facts = [
        ("Candidates shown", len(filtered), "After the active filters"),
        ("High priority", int(filtered["priority"].eq("High").sum()), "Review first"),
        ("Entities represented", int(filtered["entity_id"].nunique()), "Across this worklist"),
        ("Highest attention", f"{filtered['score'].max():.1f}" if not filtered.empty else "—", "Top remaining candidate"),
    ]
    for col, (label, value, note) in zip(summary_cols, facts):
        with col:
            simple_card(label, value, note)

    st.markdown("<div class='tl-section-head'><div class='tl-section-title'>Supervisory worklist</div><div class='tl-section-note'>Exact candidates, reasons and next review order.</div></div>", unsafe_allow_html=True)
    if filtered.empty:
        empty_state("No matching candidates", "Adjust the priority or search filters to restore review candidates.")
        return

    worklist = filtered[["priority", "score", "assessment_id", "entity_name", "dominant_signal"]].copy()
    worklist.insert(0, "review_order", range(1, len(worklist) + 1))
    worklist["score"] = worklist["score"].round(1)
    st.dataframe(
        worklist.rename(columns={
            "review_order": "Order", "priority": "Priority", "score": "Attention",
            "assessment_id": "Assessment", "entity_name": "Entity", "dominant_signal": "Primary reason",
        }),
        width="stretch", hide_index=True,
    )

    st.markdown("<div class='tl-section-head'><div class='tl-section-title'>Candidate review brief</div><div class='tl-section-note'>The evidence mix behind one queue position.</div></div>", unsafe_allow_html=True)
    assessment_ids = filtered["assessment_id"].tolist()
    current = selected_assessment()
    default_index = assessment_ids.index(current) if current in assessment_ids else 0
    selected = st.selectbox(
        "Assessment to inspect", assessment_ids, index=default_index,
        format_func=lambda aid: f"{aid} · {filtered.loc[filtered['assessment_id'].eq(aid), 'entity_name'].iloc[0]}",
        key="queue_assessment_detail",
    )
    row = filtered[filtered["assessment_id"].eq(selected)].iloc[0]
    signal_cols = st.columns(4)
    for col, label in zip(signal_cols, lens_labels):
        with col:
            simple_card(label, int(row[label]), "Deterministic findings")

    rationale = str(row.get("rationale", "")).strip()
    reason = rationale or (
        f"This assessment is routed as {row['priority']} priority with an attention score of "
        f"{row['score']:.1f}. Its strongest current signal is {row['dominant_signal'].lower()}."
    )
    st.markdown(f"<div class='tl-callout'><b>Why this is queued</b><br>{reason}</div>", unsafe_allow_html=True)


def page_entities():
    data, queue = get_active_data()
    q = normalize_queue(queue_view(queue, data.get("entities", pd.DataFrame()))).copy()
    page_title("SUPERVISION / 02", "Entity Intelligence", "Entity dossiers for direct comparison and focused supervisory review.")
    overview = build_entity_supervisory_overview(q, data["entities"], data["assessments"])
    if overview.empty:
        empty_state("No entity comparison available", "There are not enough assessment-level indicators to build the entity view.")
        return

    p = overview.copy()
    for c in ["entity_id", "entity_name"]:
        p[c] = p[c].fillna("").astype(str)
    numeric_cols = ["attention_score", "avg_attention_score", "execution_gaps", "negative_space", "peer_deviations", "operational_patterns"]
    for c in numeric_cols:
        if c not in p.columns:
            p[c] = 0.0
        p[c] = pd.to_numeric(p[c], errors="coerce").fillna(0.0)

    lens_labels = ["execution_gaps", "negative_space", "peer_deviations", "operational_patterns"]
    display_labels = {
        "execution_gaps": "Execution gaps", "negative_space": "Negative space",
        "peer_deviations": "Peer deviations", "operational_patterns": "Operational patterns",
    }
    p["total_findings"] = p[lens_labels].sum(axis=1)
    p["dominant_signal"] = p[lens_labels].idxmax(axis=1).map(display_labels)
    p.loc[p["total_findings"].eq(0), "dominant_signal"] = "No lens findings"

    assessments = data.get("assessments", pd.DataFrame())
    if not assessments.empty and "entity_id" in assessments.columns:
        volumes = assessments.assign(entity_id=assessments["entity_id"].astype(str)).groupby("entity_id").size()
        p["assessment_count"] = p["entity_id"].map(volumes).fillna(0).astype(int)
    else:
        p["assessment_count"] = 0

    attention_col = "attention_score" if p["attention_score"].abs().sum() else "avg_attention_score"
    portfolio_average = float(p[attention_col].mean()) if not p.empty else 0.0
    p["attention_status"] = p[attention_col].apply(lambda value: "Above portfolio average" if value > portfolio_average else "At or below average")
    p = p.sort_values([attention_col, "entity_name"], ascending=[False, True]).reset_index(drop=True)

    st.markdown("<div class='tl-section-head'><div class='tl-section-title'>Entity register</div><div class='tl-section-note'>One row per CSE, with exact evidence totals rather than visual proxies.</div></div>", unsafe_allow_html=True)
    register = p[["entity_name", attention_col, "attention_status", "assessment_count", "total_findings", "dominant_signal"]].copy()
    register[attention_col] = register[attention_col].round(1)
    register["total_findings"] = register["total_findings"].astype(int)
    st.dataframe(
        register.rename(columns={
            "entity_name": "Entity", attention_col: "Attention", "attention_status": "Portfolio position",
            "assessment_count": "Assessments", "total_findings": "Findings", "dominant_signal": "Primary signal",
        }),
        width="stretch", hide_index=True,
    )

    st.markdown("<div class='tl-section-head'><div class='tl-section-title'>Entity dossier</div><div class='tl-section-note'>Select one CSE for a structured supervisory brief.</div></div>", unsafe_allow_html=True)
    entity_options = p["entity_id"].tolist()
    current_aid = selected_assessment()
    current_entity = None
    if current_aid != "ALL" and "entity_id" in q.columns:
        match = q[q["assessment_id"].astype(str).eq(str(current_aid))]
        if not match.empty:
            current_entity = str(match.iloc[0]["entity_id"])
    default_entity = entity_options.index(current_entity) if current_entity in entity_options else 0
    entity = st.selectbox(
        "Entity to examine", entity_options, index=default_entity,
        format_func=lambda value: str(p.loc[p["entity_id"].eq(value), "entity_name"].iloc[0]),
        key="entity_trend_detail",
    )
    entity_row = p[p["entity_id"].eq(entity)].iloc[0]

    header_cols = st.columns(4)
    header_facts = [
        ("Attention", f"{entity_row[attention_col]:.1f}", entity_row["attention_status"]),
        ("Assessments", int(entity_row["assessment_count"]), "Available review periods"),
        ("Total findings", int(entity_row["total_findings"]), "Across all four lenses"),
        ("Primary signal", entity_row["dominant_signal"], "Largest current concentration"),
    ]
    for col, (label, value, note) in zip(header_cols, header_facts):
        with col:
            simple_card(label, value, note)

    st.markdown("<div class='tl-section-head'><div class='tl-section-title'>Signal inventory</div><div class='tl-section-note'>Exact deterministic finding counts for the selected entity.</div></div>", unsafe_allow_html=True)
    signal_cols = st.columns(4)
    for col, key in zip(signal_cols, lens_labels):
        with col:
            simple_card(display_labels[key], int(entity_row[key]), "Recorded findings")

    if entity_row["total_findings"] > 0:
        brief = (
            f"{entity_row['entity_name']} has {int(entity_row['total_findings'])} findings across "
            f"{int(entity_row['assessment_count'])} assessment(s). Review {str(entity_row['dominant_signal']).lower()} first, "
            "then inspect the underlying records in Evidence Analytics before forming a supervisory view."
        )
    else:
        brief = f"{entity_row['entity_name']} has no current findings across the four deterministic lenses."
    st.markdown(f"<div class='tl-callout'><b>Supervisory brief</b><br>{brief}</div>", unsafe_allow_html=True)


def page_evidence():
    data, queue = get_active_data()
    data, q = scope_data(data, queue)
    page_title("SUPERVISION / 03", "Evidence Analytics", "A record-led evidence ledger connecting every signal to its operational source.")
    context_strip(data)
    features = get_active_features()
    cf = features.get("case_features", pd.DataFrame()) if isinstance(features, dict) else pd.DataFrame()
    if selected_assessment() != "ALL" and not cf.empty and "assessment_id" in cf.columns:
        cf = cf[cf["assessment_id"].astype(str) == selected_assessment()]
    negative = build_negative_space_findings(data["monitoring"], data["assets"], data["alerts"], data["cases"], data["assessments"])
    anomalies = build_anomaly_findings(data["cases"], data["investigations"], data["alerts"])
    if selected_assessment() != "ALL":
        if not negative.empty and "assessment_id" in negative.columns:
            negative = negative[negative["assessment_id"].astype(str) == selected_assessment()]
        if not anomalies.empty and "assessment_id" in anomalies.columns:
            anomalies = anomalies[anomalies["assessment_id"].astype(str) == selected_assessment()]

    tabs = st.tabs(["Execution gaps", "Negative space", "Operational patterns"])
    with tabs[0]:
        section_note("Execution gap", "Operational evidence suggests a documented process, control or metric may not be functioning as expected.")
        rules = [
            ("weak_investigation", "Weak investigation", "Cases with limited investigative evidence."),
            ("rapid_closure", "Rapid closure", "Cases closed unusually quickly under the prototype rules."),
            ("missing_escalation", "Missing escalation", "Critical/high-priority cases without expected escalation evidence."),
        ]
        available_rules = [(col, label, definition) for col, label, definition in rules if col in cf.columns]
        if not available_rules:
            empty_state("No execution-gap indicators", "The current feature set does not contain execution-gap indicators for this scope.")
        else:
            rule_cols = st.columns(len(available_rules))
            for card, (col, label, definition) in zip(rule_cols, available_rules):
                count = int(cf[col].fillna(False).astype(bool).sum())
                with card:
                    simple_card(label, count, definition)
            st.markdown("<div class='tl-section-head'><div class='tl-section-title'>Rule evidence</div><div class='tl-section-note'>Open a rule to inspect only the records that triggered it.</div></div>", unsafe_allow_html=True)
            for col, label, definition in available_rules:
                affected = cf[cf[col].fillna(False).astype(bool)].copy()
                with st.expander(f"{label} · {len(affected)} record(s)"):
                    st.caption(definition)
                    if affected.empty:
                        st.write("No records triggered this rule in the active scope.")
                    else:
                        preferred = [c for c in ["assessment_id", "entity_id", "case_id", "alert_id", "priority", "status"] if c in affected.columns]
                        st.dataframe(affected[preferred] if preferred else affected, width="stretch", hide_index=True)

    with tabs[1]:
        section_note("Negative space", "The tool looks for evidence that would normally be expected but appears absent, unusually low or incomplete.")
        if negative.empty:
            empty_state("No negative-space indicators", "No negative-space condition was detected by the current deterministic rules.")
        else:
            severity = negative.get("severity", pd.Series("Unclassified", index=negative.index)).fillna("Unclassified").astype(str)
            severity_counts = severity.value_counts()
            order = [item for item in ["Critical", "High", "Medium", "Low", "Unclassified"] if item in severity_counts.index]
            remaining = [item for item in severity_counts.index if item not in order]
            summary_cols = st.columns(min(max(len(order + remaining), 1), 5))
            for card, level in zip(summary_cols, order + remaining):
                with card:
                    simple_card(level, int(severity_counts[level]), "Missing-evidence records")
            st.markdown("<div class='tl-section-head'><div class='tl-section-title'>Missing-evidence ledger</div><div class='tl-section-note'>Grouped by finding, with source records available directly below.</div></div>", unsafe_allow_html=True)
            group_key = "finding" if "finding" in negative.columns else "severity"
            for finding, records in negative.groupby(group_key, dropna=False, sort=True):
                with st.expander(f"{finding} · {len(records)} record(s)"):
                    show = [c for c in ["assessment_id", "entity_id", "asset_id", "finding", "severity", "reason"] if c in records.columns]
                    st.dataframe(records[show] if show else records, width="stretch", hide_index=True)

    with tabs[2]:
        section_note("Operational patterns", "Repeated or unusual investigation behaviour can reveal process weaknesses that ordinary KPI summaries may miss.")
        if anomalies.empty:
            empty_state("No operational patterns", "No operational anomaly or repeated-pattern signal was detected by the current rules.")
        else:
            signal_series = anomalies.get("signal", pd.Series("Unclassified", index=anomalies.index)).fillna("Unclassified").astype(str)
            signal_counts = signal_series.value_counts().rename_axis("Pattern").reset_index(name="Affected records")
            st.dataframe(signal_counts, width="stretch", hide_index=True)
            st.markdown("<div class='tl-section-head'><div class='tl-section-title'>Pattern evidence</div><div class='tl-section-note'>Open a pattern to inspect every affected case.</div></div>", unsafe_allow_html=True)
            working = anomalies.copy()
            working["_signal_group"] = signal_series
            for signal, records in working.groupby("_signal_group", sort=True):
                with st.expander(f"{signal} · {len(records)} record(s)"):
                    show = [c for c in ["assessment_id", "entity_id", "case_id", "signal", "description"] if c in records.columns]
                    st.dataframe(records[show] if show else records.drop(columns=["_signal_group"]), width="stretch", hide_index=True)


def page_case_review():
    data, queue = get_active_data()
    data, q = scope_data(data, queue)
    page_title("SUPERVISION / 04", "Case Review", "Inspect the underlying record after a supervisory signal identifies a reason to look closer.")
    context_strip(data)
    if q.empty:
        empty_state("No assessment available", "Select an assessment with review candidates before opening representative case evidence.")
        return
    selected = st.selectbox("Assessment", q.sort_values("rank")["assessment_id"].astype(str).tolist(), key="case_review_assessment")
    samples = build_manual_review_samples(selected, data["cases"], data["investigations"], data["escalations"], data["alerts"])
    if samples.empty:
        empty_state("No representative samples", "No case has been selected for manual-review sampling in this assessment.")
        return
    case_id = st.selectbox("Representative case", samples["case_id"].astype(str).tolist(), key="representative_case")
    case = samples[samples["case_id"].astype(str) == case_id].iloc[0]

    left, right = st.columns([1, 1.25], gap="large")
    with left:
        st.markdown("<div class='tl-section-head'><div class='tl-section-title'>Case summary</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='tl-case-card'><div class='tl-case-id'>{case_id}</div><div class='tl-case-row'><span>Priority</span><b>{case.get('priority','—')}</b></div><div class='tl-case-row'><span>Status</span><b>{case.get('status','—')}</b></div><div class='tl-case-row'><span>Disposition</span><b>{case.get('disposition','—')}</b></div><div class='tl-case-row'><span>Closure time</span><b>{case.get('closure_time','—')}</b></div><div class='tl-case-row'><span>Review reason</span><b>{case.get('review_reason','—')}</b></div></div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='tl-section-head'><div class='tl-section-title'>Why was this case sampled?</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='tl-callout'><b>Manual-review reason</b><br>{case.get('review_reason','The case was selected by the supervisory sampling logic.')}</div>", unsafe_allow_html=True)

    inv = data["investigations"][data["investigations"]["case_id"].astype(str) == case_id] if "case_id" in data["investigations"].columns else pd.DataFrame()
    esc = data["escalations"][data["escalations"]["case_id"].astype(str) == case_id] if "case_id" in data["escalations"].columns else pd.DataFrame()
    alert = data["alerts"][data["alerts"].get("case_id", pd.Series(dtype=str)).astype(str) == case_id] if "case_id" in data["alerts"].columns else pd.DataFrame()

    # Evidence-stage track restored from the first professional chart version.
    stages = [
        ("Alert context", not alert.empty),
        ("Investigation", not inv.empty),
        ("Escalation", not esc.empty),
        ("Closure", bool(str(case.get("closure_time", "")).strip()) and str(case.get("closure_time", "")).lower() not in {"nan", "nat", "none"}),
    ]
    stage_names = [x[0] for x in stages]
    stage_colors = [PALETTE["emerald"] if ok else PALETTE["graphite"] for _, ok in stages]
    stage_status = ["Documented" if ok else "Missing" for _, ok in stages]
    fig = go.Figure(go.Scatter(
        x=stage_names,y=[1] * len(stages),mode="markers+text",
        marker=dict(size=42,color=stage_colors,symbol=["circle" if ok else "circle-open" for _,ok in stages],line=dict(color=stage_colors,width=3)),
        text=["✓" if ok else "×" for _,ok in stages],textposition="middle center",
        textfont=dict(size=17,color=PALETTE["ivory"]),customdata=stage_status,
        hovertemplate="<b>%{x}</b><br>Status: %{customdata}<extra></extra>",showlegend=False,
    ))
    for idx in range(len(stages)-1):
        fig.add_shape(type="line",x0=stage_names[idx],x1=stage_names[idx+1],y0=1,y1=1,line=dict(color=PALETTE["track"],width=5),layer="below")
    fig.update_xaxes(title="Evidence stage",showgrid=False,tickfont=dict(size=10,color=PALETTE["muted"]))
    fig.update_yaxes(visible=False,range=[0.72,1.28])
    fig.update_layout(
        margin=dict(l=20,r=20,t=42,b=48),showlegend=False,
    )
    documented = sum(1 for _,ok in stages if ok)
    plot_panel(
        "Case evidence coverage",
        "The expected evidence stages are checked directly for the selected case.",
        fig, 330,
        f"{documented} of {len(stages)} expected stages are represented in the current records. Missing stages deserve direct examiner attention.",
        False,
    )

    tabs = st.tabs(["Investigation", "Escalation", "Alert context"])
    with tabs[0]:
        st.dataframe(inv, width="stretch", hide_index=True)
    with tabs[1]:
        st.dataframe(esc, width="stretch", hide_index=True)
    with tabs[2]:
        st.dataframe(alert, width="stretch", hide_index=True)
    st.warning("Peril-Lens surfaces evidence for the examiner. The final supervisory conclusion remains human-led.")


def page_data():
    data, _ = get_active_data()
    page_title(
        "PLATFORM / 01",
        "Data & Validation",
        "Validate structured submissions before activating them as the analytical source.",
    )
    render_data_ingestion_panel(data)
    if st.session_state.get("tl_active_source") == "uploaded":
        st.success("Validated submission is active.")
    else:
        st.info("Demonstration dataset is active.")


def page_reports():
    data,queue=get_active_data(); data,q=scope_data(data,queue); page_title("PLATFORM / 02","Reports & Governance","Create an auditable supervisory output and inspect the implementation boundary."); context_strip(data)
    if not q.empty:
        selected=st.selectbox("Assessment for report",q.sort_values("rank")["assessment_id"].astype(str).tolist(),key="report_assessment"); row=q[q["assessment_id"].astype(str)==selected].iloc[0]; entity_id=str(row.get("entity_id","")); entity_name=str(row.get("entity_name",entity_id)); assessments=data["assessments"]; ar=assessments[assessments["assessment_id"].astype(str)==selected] if "assessment_id" in assessments.columns else pd.DataFrame(); period_text=f"{ar.iloc[0].get('period_start','')} to {ar.iloc[0].get('period_end','')}" if not ar.empty else ""; features=get_active_features(); cf=features.get("case_features",pd.DataFrame()) if isinstance(features,dict) else pd.DataFrame(); selected_cases=data["cases"][data["cases"]["assessment_id"].astype(str)==selected] if "assessment_id" in data["cases"].columns else pd.DataFrame(); selected_alerts=data["alerts"][data["alerts"]["assessment_id"].astype(str)==selected] if "assessment_id" in data["alerts"].columns else pd.DataFrame(); selected_invs=data["investigations"][data["investigations"]["case_id"].astype(str).isin(selected_cases["case_id"].astype(str))] if not selected_cases.empty else pd.DataFrame(); selected_esc=data["escalations"][data["escalations"]["case_id"].astype(str).isin(selected_cases["case_id"].astype(str))] if not selected_cases.empty else pd.DataFrame(); negative=build_negative_space_findings(data["monitoring"],data["assets"],data["alerts"],data["cases"],data["assessments"]); negative=negative[negative["assessment_id"].astype(str)==selected] if not negative.empty and "assessment_id" in negative.columns else pd.DataFrame(); anomalies=build_anomaly_findings(selected_cases,selected_invs,selected_alerts); execution=cf[cf["assessment_id"].astype(str)==selected] if not cf.empty and "assessment_id" in cf.columns else pd.DataFrame()
        try:
            report_bytes=build_organisation_report(assessment_id=selected,entity_name=entity_name,entity_id=entity_id,period_text=period_text,selected_row=row,sel_alerts=selected_alerts,sel_cases=selected_cases,sel_investigations=selected_invs,sel_escalations=selected_esc,execution_evidence=execution,negative_evidence=negative,peer_evidence=pd.DataFrame(),operational_evidence=anomalies,case_features=cf,assets=data["assets"],monitoring=data["monitoring"],dataset_label="Validated CSE Submission" if st.session_state.get("tl_active_source")=="uploaded" else "Synthetic Prototype Dataset")
            safe_entity="".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in entity_name); st.download_button("Download supervisory report",data=report_bytes,file_name=f"Peril-Lens{safe_entity}_{selected}_Supervisory_Assessment.pdf",mime="application/pdf",type="primary")
        except Exception as exc: st.error("Could not generate the organisation report."); st.exception(exc)
    st.markdown("<div class='tl-section-head'><div class='tl-section-title'>Implementation coverage</div></div>",unsafe_allow_html=True); render_ps_coverage_panel(queue,data["entities"],data["assessments"],data["cases"],data["monitoring"])
    st.markdown("<div class='tl-section-head'><div class='tl-section-title'>Governance boundary</div></div>",unsafe_allow_html=True); st.markdown("<div class='tl-callout'><b>Human-in-the-loop:</b> analytics produce supervisory signals and review priorities, not final compliance judgements.<br><br><b>Offline boundary:</b> local deterministic analytics with no external AI/API dependency in the prototype.</div>",unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# App shell
# -----------------------------------------------------------------------------
if not security_gate():
    st.stop()

render_header()
data,_queue=get_active_data()
if "tl_selected_assessment" not in st.session_state:
    st.session_state.tl_selected_assessment="ALL"
render_sidebar_status(data)

home=st.Page(page_home,title="Command Center",icon="🏠",default=True)
queue_page=st.Page(page_queue,title="Review Queue",icon=":material/flag:")
entity_page=st.Page(page_entities,title="Entity Intelligence",icon=":material/business:")
evidence_page=st.Page(page_evidence,title="Evidence Analytics",icon=":material/analytics:")
case_page=st.Page(page_case_review,title="Case Review",icon=":material/fact_check:")
data_page=st.Page(page_data,title="Data & Validation",icon=":material/storage:")
report_page=st.Page(page_reports,title="Reports & Governance",icon=":material/description:")

pg=st.navigation({"SUPERVISION":[home,queue_page,entity_page,evidence_page,case_page],"PLATFORM":[data_page,report_page]},position="sidebar",expanded=True)
pg.run()
