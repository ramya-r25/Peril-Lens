from pathlib import Path
import sys
from datetime import datetime, timedelta
import json

import pandas as pd
import plotly.express as px
import streamlit as st

# -------------------------------------------------------------------
# Project paths
# -------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
def _brand_markup(compact=False):
    size = "compact" if compact else "full"
    return f"""
    <div class="tl-brand {size}">
        <div class="tl-brand-mark">
            <svg viewBox="0 0 48 48" aria-hidden="true">
                <path d="M24 4 40 10v11c0 10.5-6.2 18.3-16 23C14.2 39.3 8 31.5 8 21V10l16-6Z" fill="none" stroke="currentColor" stroke-width="2.4"/>
                <path d="m16 24 5 5 11-12" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div>
            <div class="tl-brand-name">Peril<span>Lens</span></div>
            <div class="tl-brand-sub">SAT-SA · Supervisory Analytics</div>
        </div>
    </div>
    """


def security_gate():
    """Local authentication gate with a product-style Peril-Lens login screen."""
    if "tl_authenticated" not in st.session_state:
        st.session_state.tl_authenticated = False
    if "tl_username" not in st.session_state:
        st.session_state.tl_username = ""
    if "tl_key" not in st.session_state:
        st.session_state.tl_key = None

    if not SECURITY.is_configured():
        st.markdown("<div class='tl-login-wrap'>", unsafe_allow_html=True)
        st.markdown(_brand_markup(), unsafe_allow_html=True)
        st.markdown(
            """<div class="tl-login-card">
                <div class="tl-login-kicker">FIRST-RUN SECURITY SETUP</div>
                <div class="tl-login-title">Create administrator access</div>
                <div class="tl-login-copy">Initialize local access for this controlled supervisory environment.</div>
            """ , unsafe_allow_html=True)
        password1 = st.text_input("Administrator password", type="password", key="setup_password")
        password2 = st.text_input("Confirm password", type="password", key="setup_password_confirm")
        if st.button("Initialize secure access", type="primary", use_container_width=True):
            if len(password1) < 10:
                st.error("Use at least 10 characters for the administrator password.")
            elif password1 != password2:
                st.error("The passwords do not match.")
            else:
                SECURITY.create_admin(password1)
                encryption_key = SECURITY.derive_encryption_key(password1)
                st.session_state.tl_authenticated = True
                st.session_state.tl_username = "admin"
                st.session_state.tl_key = encryption_key
                SECURITY.append_audit(encryption_key, "admin", "security_setup")
                st.rerun()
        st.markdown("<div class='tl-login-foot'>Local authentication · Salted password hash · No external identity service</div></div></div>", unsafe_allow_html=True)
        return False

    if not st.session_state.tl_authenticated:
        st.markdown("<div class='tl-login-wrap'>", unsafe_allow_html=True)
        st.markdown(_brand_markup(), unsafe_allow_html=True)
        st.markdown(
            """<div class="tl-login-card">
                <div class="tl-login-kicker">PROTECTED SUPERVISORY ENVIRONMENT</div>
                <div class="tl-login-title">Sign in to Peril-Lens</div>
                <div class="tl-login-copy">Access is restricted to authorised local users.</div>
            """, unsafe_allow_html=True)
        username = st.text_input("Username", value="admin", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Sign in", type="primary", use_container_width=True):
            if username == "admin" and SECURITY.verify_password(password):
                encryption_key = SECURITY.derive_encryption_key(password)
                st.session_state.tl_authenticated = True
                st.session_state.tl_username = username
                st.session_state.tl_key = encryption_key
                SECURITY.append_audit(encryption_key, username, "login_success")
                st.rerun()
            st.error("Invalid username or password.")
        st.markdown(
            "<div class='tl-secure-row'><span class='tl-secure-dot'></span> LOCAL / OFFLINE</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<div class='tl-login-foot'>Authentication is processed locally. No external identity or cloud service is required.</div></div></div>", unsafe_allow_html=True)
        return False

    return True

DATA = ROOT / "data" / "synthetic"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.analytics.prioritization_engine import build_prioritization_queue
from src.analytics.explainability_engine import build_explanation
from src.features.feature_engineering import build_feature_dataset
from src.reports.organisation_report import build_organisation_report
from src.security.security_manager import ThreatLensSecurity
SECURITY = ThreatLensSecurity(ROOT)

# -------------------------------------------------------------------
# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_csv(name):
    return pd.read_csv(DATA / name)


@st.cache_data(show_spinner=False)
def load_queue():
    return build_prioritization_queue()


@st.cache_data(show_spinner=False)
def load_features():
    """Normalize the existing feature-engineering tuple for dashboard use."""
    result = build_feature_dataset()
    if isinstance(result, tuple):
        return {
            "alerts": result[0] if len(result) > 0 else pd.DataFrame(),
            "case_features": result[1] if len(result) > 1 else pd.DataFrame(),
            "monitoring": result[2] if len(result) > 2 else pd.DataFrame(),
        }
    if isinstance(result, dict):
        return result
    return {"alerts": pd.DataFrame(), "case_features": pd.DataFrame(), "monitoring": pd.DataFrame()}


def safe_num(value, default=0):
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def metric_card(label, value, detail=""):
    st.markdown(
        f"""
        <div class="signal-card">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            <div class="detail">{detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def pick_column(df, names, default=None):
    for name in names:
        if name in df.columns:
            return df[name]
    return pd.Series(default, index=df.index)



# -------------------------------------------------------------------
# SAT-SA Data Ingestion & Validation
# -------------------------------------------------------------------
REQUIRED_DATASETS = {
    "entities": {"required": ["entity_id", "entity_name", "sector", "entity_size"], "key": "entity_id"},
    "assessments": {"required": ["assessment_id", "entity_id", "period_start", "period_end", "submission_date"], "key": "assessment_id"},
    "alerts": {"required": ["alert_id", "assessment_id", "asset_id", "severity"], "key": "alert_id"},
    "cases": {"required": ["case_id", "assessment_id", "status", "priority", "disposition"], "key": "case_id"},
    "investigations": {"required": ["investigation_id", "case_id", "evidence_count", "steps_recorded"], "key": "investigation_id"},
    "escalations": {"required": ["escalation_id", "case_id"], "key": "escalation_id"},
    "assets": {"required": ["asset_id", "entity_id", "criticality", "expected_monitoring"], "key": "asset_id"},
    "monitoring": {"required": ["monitoring_id", "assessment_id", "asset_id", "expected_coverage", "observed_coverage", "telemetry_available"], "key": "monitoring_id"},
}

RELATIONSHIPS = [
    ("assessments", "entity_id", "entities", "entity_id"),
    ("assets", "entity_id", "entities", "entity_id"),
    ("alerts", "assessment_id", "assessments", "assessment_id"),
    ("alerts", "asset_id", "assets", "asset_id"),
    ("alerts", "case_id", "cases", "case_id"),
    ("cases", "assessment_id", "assessments", "assessment_id"),
    ("investigations", "case_id", "cases", "case_id"),
    ("escalations", "case_id", "cases", "case_id"),
    ("monitoring", "assessment_id", "assessments", "assessment_id"),
    ("monitoring", "asset_id", "assets", "asset_id"),
]


def infer_dataset_name(filename):
    stem = Path(filename).stem.lower().strip()
    aliases = {
        "entity": "entities", "entities": "entities",
        "assessment": "assessments", "assessments": "assessments",
        "alert": "alerts", "alerts": "alerts",
        "case": "cases", "cases": "cases",
        "investigation": "investigations", "investigations": "investigations",
        "escalation": "escalations", "escalations": "escalations",
        "asset": "assets", "assets": "assets",
        "monitoring": "monitoring",
    }
    return aliases.get(stem)


def read_uploaded_table(uploaded_file):
    suffix = Path(uploaded_file.name).suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(uploaded_file)
    if suffix == ".json":
        raw = json.load(uploaded_file)
        if isinstance(raw, list):
            return pd.DataFrame(raw)
        if isinstance(raw, dict) and isinstance(raw.get("records"), list):
            return pd.DataFrame(raw["records"])
        if isinstance(raw, dict):
            return pd.DataFrame([raw])
        raise ValueError("JSON must contain an array of records or a single object.")
    raise ValueError("Unsupported format. Use CSV or JSON.")


def validate_dataset_bundle(data):
    rows = []
    summary = {
        "datasets_present": 0,
        "datasets_expected": len(REQUIRED_DATASETS),
        "schema_failures": 0,
        "duplicate_failures": 0,
        "null_key_failures": 0,
        "relationship_failures": 0,
    }

    for name, spec in REQUIRED_DATASETS.items():
        df = data.get(name)
        if df is None:
            rows.append({
                "Dataset": name, "Rows": 0, "Schema": "MISSING",
                "Key": "MISSING", "Referential integrity": "NOT CHECKED",
                "Status": "FAIL", "Issue": "Required dataset was not supplied.",
            })
            summary["schema_failures"] += 1
            continue

        summary["datasets_present"] += 1
        missing = [c for c in spec["required"] if c not in df.columns]
        key = spec["key"]
        duplicate_count = int(df[key].duplicated().sum()) if key in df.columns else 0
        null_count = int(df[key].isna().sum()) if key in df.columns else 0
        schema_ok = not missing
        key_ok = key in df.columns and duplicate_count == 0 and null_count == 0

        if not schema_ok:
            summary["schema_failures"] += 1
        summary["duplicate_failures"] += duplicate_count
        summary["null_key_failures"] += null_count

        rows.append({
            "Dataset": name,
            "Rows": len(df),
            "Schema": "PASS" if schema_ok else f"FAIL: missing {', '.join(missing)}",
            "Key": "PASS" if key_ok else f"FAIL: duplicates={duplicate_count}, nulls={null_count}",
            "Referential integrity": "PENDING",
            "Status": "PASS" if schema_ok and key_ok else "FAIL",
            "Issue": "" if schema_ok and key_ok else "Review schema/key quality.",
        })

    for child, child_col, parent, parent_col in RELATIONSHIPS:
        child_df = data.get(child)
        parent_df = data.get(parent)
        if child_df is None or parent_df is None:
            continue
        if child_col not in child_df.columns or parent_col not in parent_df.columns:
            continue

        child_values = child_df[child_col].dropna().astype(str)
        parent_values = set(parent_df[parent_col].dropna().astype(str))
        orphan_count = int((~child_values.isin(parent_values)).sum())
        summary["relationship_failures"] += orphan_count

        rows.append({
            "Dataset": f"{child}.{child_col} → {parent}.{parent_col}",
            "Rows": orphan_count,
            "Schema": "PASS",
            "Key": "PASS",
            "Referential integrity": "PASS" if orphan_count == 0 else f"FAIL: {orphan_count} orphan(s)",
            "Status": "PASS" if orphan_count == 0 else "FAIL",
            "Issue": "" if orphan_count == 0 else "Referenced ID does not exist in parent dataset.",
        })

    overall_ok = (
        summary["datasets_present"] == summary["datasets_expected"]
        and summary["schema_failures"] == 0
        and summary["duplicate_failures"] == 0
        and summary["null_key_failures"] == 0
        and summary["relationship_failures"] == 0
    )
    return overall_ok, pd.DataFrame(rows), summary


def render_data_ingestion_panel(demo_data):
    st.markdown('<div class="section-title">Data Ingestion & Validation</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Validate periodic structured CSE submissions before supervisory analysis. '
        'CSV and JSON are handled locally; database/API adapters remain deployment-specific.</div>',
        unsafe_allow_html=True,
    )

    source_mode = st.radio(
        "Data source",
        ["Built-in demonstration dataset", "Upload CSE submission files"],
        horizontal=True,
        key="tl_data_source_mode",
    )

    if source_mode == "Built-in demonstration dataset":
        st.success("Demo source selected. Current synthetic assessment data remains the active analytical source.")
        st.caption(
            "6 entities · 8 assessments · 800 alerts · 489 cases · 426 investigations · "
            "103 escalations · 12 monitoring records."
        )
        return

    uploaded = st.file_uploader(
        "Upload SAT-SA structured data files",
        type=["csv", "json"],
        accept_multiple_files=True,
        key="tl_submission_files",
        help="Use filenames such as entities.csv, assessments.json, alerts.csv, cases.csv, etc.",
    )

    if not uploaded:
        st.info("Upload the structured submission tables to run schema, key and referential-integrity checks.")
        st.dataframe(
            pd.DataFrame({
                "Expected dataset": list(REQUIRED_DATASETS.keys()),
                "Primary key": [v["key"] for v in REQUIRED_DATASETS.values()],
            }),
            use_container_width=True,
            hide_index=True,
        )
        return

    data = {}
    parse_errors = []
    for file in uploaded:
        dataset_name = infer_dataset_name(file.name)
        if not dataset_name:
            parse_errors.append(f"{file.name}: filename does not map to a SAT-SA dataset.")
            continue
        try:
            data[dataset_name] = read_uploaded_table(file)
        except Exception as exc:
            parse_errors.append(f"{file.name}: {exc}")

    for message in parse_errors:
        st.error(message)

    if data:
        st.write("**Detected submission tables**")
        st.dataframe(
            pd.DataFrame([
                {"Dataset": name, "Rows": len(df), "Columns": len(df.columns)}
                for name, df in data.items()
            ]),
            use_container_width=True,
            hide_index=True,
        )

    overall_ok, validation_df, summary = validate_dataset_bundle(data)

    v1, v2, v3, v4 = st.columns(4)
    with v1:
        metric_card("Tables received", summary["datasets_present"], f"of {summary['datasets_expected']} expected")
    with v2:
        metric_card("Schema failures", summary["schema_failures"], "Required fields")
    with v3:
        metric_card("Key failures", summary["duplicate_failures"] + summary["null_key_failures"], "Duplicates / null IDs")
    with v4:
        metric_card("Relationship failures", summary["relationship_failures"], "Orphan references")

    if overall_ok:
        st.success("Validation PASS — expected tables, required fields, keys and checked relationships are valid.")
        st.session_state["tl_validated_upload"] = data
        if st.button("Use validated submission for supervisory analysis", type="primary", key="tl_activate_upload"):
            st.session_state["tl_active_source"] = "uploaded"
            st.rerun()
    else:
        st.warning("Validation requires attention. Resolve failed checks before treating the submission as analysis-ready.")

    st.dataframe(validation_df, use_container_width=True, hide_index=True)

    if data:
        preview_name = st.selectbox("Preview submitted dataset", list(data.keys()), key="tl_preview_dataset")
        st.dataframe(data[preview_name].head(20), use_container_width=True, hide_index=True)

    st.caption(
        "Offline boundary: uploaded data is parsed in the local Streamlit process. "
        "No cloud, SaaS, external AI model or external API is required."
    )


def build_uploaded_supervisory_queue(data):
    """Build an explainable assessment queue directly from a validated upload bundle.

    This is intentionally deterministic and auditable: every score component maps to
    a visible count of execution-gap, negative-space, peer-deviation or operational
    pattern signals. It does not use an external model or API.
    """
    assessments_df = data.get("assessments", pd.DataFrame()).copy()
    cases_df = data.get("cases", pd.DataFrame()).copy()
    inv_df = data.get("investigations", pd.DataFrame()).copy()
    esc_df = data.get("escalations", pd.DataFrame()).copy()
    mon_df = data.get("monitoring", pd.DataFrame()).copy()
    assets_df = data.get("assets", pd.DataFrame()).copy()

    if assessments_df.empty:
        return pd.DataFrame()

    # Case-level execution signals.
    case_signal = pd.DataFrame(index=cases_df.index)
    if not cases_df.empty:
        case_signal["case_id"] = cases_df.get("case_id", pd.Series(index=cases_df.index, dtype=object)).astype(str)
        case_signal["assessment_id"] = cases_df.get("assessment_id", pd.Series(index=cases_df.index, dtype=object))
        case_signal["priority"] = cases_df.get("priority", "").astype(str).str.lower()
        if "case_created_time" in cases_df.columns and "closure_time" in cases_df.columns:
            created = _to_datetime(cases_df["case_created_time"])
            closed = _to_datetime(cases_df["closure_time"])
            case_signal["closure_hours"] = (closed - created).dt.total_seconds() / 3600
        else:
            case_signal["closure_hours"] = 9999
        case_signal["rapid_closure"] = case_signal["closure_hours"].between(0, 12, inclusive="both") & case_signal["priority"].isin(["high", "critical"])
    else:
        case_signal = pd.DataFrame(columns=["case_id", "assessment_id", "priority", "closure_hours", "rapid_closure"])

    # Investigation quality signals.
    if not inv_df.empty and "case_id" in inv_df.columns:
        inv = inv_df.copy()
        inv["case_id"] = inv["case_id"].astype(str)
        inv_quality = inv.groupby("case_id", as_index=False).agg(
            evidence_count=("evidence_count", "max") if "evidence_count" in inv.columns else ("case_id", "size"),
            steps_recorded=("steps_recorded", "max") if "steps_recorded" in inv.columns else ("case_id", "size"),
        )
        if "root_cause_identified" in inv.columns:
            inv_quality = inv_quality.merge(inv.groupby("case_id")["root_cause_identified"].max().rename("root_cause_identified"), on="case_id", how="left")
        if "remediation_recorded" in inv.columns:
            inv_quality = inv_quality.merge(inv.groupby("case_id")["remediation_recorded"].max().rename("remediation_recorded"), on="case_id", how="left")
        if "start_time" in inv.columns and "end_time" in inv.columns:
            inv["duration_minutes"] = (_to_datetime(inv["end_time"]) - _to_datetime(inv["start_time"])).dt.total_seconds() / 60
            inv_quality = inv_quality.merge(inv.groupby("case_id")["duration_minutes"].mean().rename("duration_minutes"), on="case_id", how="left")
        inv_quality["weak_investigation"] = (
            pd.to_numeric(inv_quality["evidence_count"], errors="coerce").fillna(0).le(2)
            | pd.to_numeric(inv_quality["steps_recorded"], errors="coerce").fillna(0).le(2)
        )
        if "root_cause_identified" in inv_quality.columns:
            inv_quality["weak_investigation"] |= ~_bool_series(inv_quality["root_cause_identified"])
        case_signal = case_signal.merge(inv_quality, on="case_id", how="left")
    if "weak_investigation" not in case_signal.columns:
        case_signal["weak_investigation"] = False
    case_signal["weak_investigation"] = case_signal["weak_investigation"].fillna(False)

    if not esc_df.empty and "case_id" in esc_df.columns:
        escalated_ids = set(esc_df["case_id"].astype(str))
    else:
        escalated_ids = set()
    case_signal["missing_escalation"] = case_signal["priority"].isin(["high", "critical"]) & ~case_signal["case_id"].isin(escalated_ids)
    case_signal["execution_signal"] = case_signal["rapid_closure"] | case_signal["weak_investigation"] | case_signal["missing_escalation"]

    # Negative-space signals by assessment.
    neg_counts = {}
    if not mon_df.empty:
        m = mon_df.copy()
        if not assets_df.empty and "asset_id" in m.columns and "asset_id" in assets_df.columns:
            acols = [c for c in ["asset_id", "criticality"] if c in assets_df.columns]
            m = m.merge(assets_df[acols].drop_duplicates("asset_id"), on="asset_id", how="left")
        m["critical"] = m.get("criticality", "").astype(str).str.lower().isin(["critical", "high"])
        m["telemetry_missing"] = ~_bool_series(m.get("telemetry_available", pd.Series(False, index=m.index)))
        if "expected_coverage_hours" in m.columns and "observed_coverage_hours" in m.columns:
            expected = pd.to_numeric(m["expected_coverage_hours"], errors="coerce").fillna(0)
            observed = pd.to_numeric(m["observed_coverage_hours"], errors="coerce").fillna(0)
            m["low_coverage"] = (observed / expected.replace(0, pd.NA)).fillna(1).lt(0.5)
        else:
            m["low_coverage"] = False
        m["negative_signal"] = m["critical"] & (m["telemetry_missing"] | m["low_coverage"])
        neg_counts = m[m["negative_signal"]].groupby("assessment_id").size().to_dict()

    # Operational pattern counts.
    op_counts = case_signal[case_signal["rapid_closure"]].groupby("assessment_id").size().to_dict()
    if "duration_minutes" in case_signal.columns:
        op_counts2 = case_signal[pd.to_numeric(case_signal["duration_minutes"], errors="coerce").fillna(99999).le(30)].groupby("assessment_id").size().to_dict()
        op_counts = {k: int(op_counts.get(k, 0)) + int(op_counts2.get(k, 0)) for k in set(op_counts) | set(op_counts2)}

    # Peer weak-investigation rate by sector/size, then deviation from comparable peers.
    base = assessments_df[[c for c in ["assessment_id", "entity_id"] if c in assessments_df.columns]].drop_duplicates("assessment_id")
    if "case_signal" in locals() and not case_signal.empty:
        weak_by_assessment = case_signal.groupby("assessment_id").agg(cases=("case_id", "nunique"), weak=("weak_investigation", "sum")).reset_index()
    else:
        weak_by_assessment = pd.DataFrame(columns=["assessment_id", "cases", "weak"])
    weak_by_assessment["weak_rate"] = weak_by_assessment["weak"] / weak_by_assessment["cases"].replace(0, pd.NA) * 100
    weak_by_assessment["weak_rate"] = weak_by_assessment["weak_rate"].fillna(0)
    weak_by_assessment = weak_by_assessment.merge(base, on="assessment_id", how="left")
    entity_meta = data.get("entities", pd.DataFrame()).copy()
    if not entity_meta.empty and "entity_id" in entity_meta.columns:
        weak_by_assessment = weak_by_assessment.merge(entity_meta[[c for c in ["entity_id", "sector", "entity_size"] if c in entity_meta.columns]].drop_duplicates("entity_id"), on="entity_id", how="left")
    peer_dev = {}
    for idx, r in weak_by_assessment.iterrows():
        peers = weak_by_assessment.copy()
        if "sector" in peers.columns and pd.notna(r.get("sector")):
            peers = peers[peers["sector"] == r.get("sector")]
        if "entity_size" in peers.columns and pd.notna(r.get("entity_size")):
            peers = peers[peers["entity_size"] == r.get("entity_size")]
        peer_avg = peers.loc[peers["assessment_id"] != r["assessment_id"], "weak_rate"].mean()
        if pd.isna(peer_avg):
            peer_avg = weak_by_assessment[weak_by_assessment["assessment_id"] != r["assessment_id"]]["weak_rate"].mean()
        deviation = max(0.0, safe_num(r.get("weak_rate")) - safe_num(peer_avg)) if not pd.isna(peer_avg) else 0.0
        peer_dev[r["assessment_id"]] = deviation

    rows = []
    for _, a in assessments_df.iterrows():
        aid = a.get("assessment_id")
        cs = case_signal[case_signal["assessment_id"] == aid] if not case_signal.empty else pd.DataFrame()
        execution = int(cs["execution_signal"].sum()) if not cs.empty else 0
        negative = int(neg_counts.get(aid, 0))
        operational = int(op_counts.get(aid, 0))
        peer = float(peer_dev.get(aid, 0.0))
        score = execution * 1.0 + negative * 2.5 + operational * 0.5 + min(peer / 10.0, 10.0)
        priority = "High" if score >= 15 else ("Medium" if score >= 6 else "Low")
        reasons = []
        if execution: reasons.append(f"{execution} execution-gap candidate(s)")
        if negative: reasons.append(f"{negative} negative-space signal(s)")
        if operational: reasons.append(f"{operational} operational outlier(s)")
        if peer > 0: reasons.append(f"peer deviation +{peer:.1f} pp")
        rows.append({
            "assessment_id": aid,
            "entity_id": a.get("entity_id", ""),
            "execution_gap_findings": execution,
            "negative_space_findings": negative,
            "peer_deviations": 1 if peer > 10 else 0,
            "operational_patterns": operational,
            "score": round(score, 2),
            "priority": priority,
            "rationale": "; ".join(reasons) if reasons else "No major supervisory signal under current transparent rules.",
        })
    q = pd.DataFrame(rows).sort_values(["score", "assessment_id"], ascending=[False, True]).reset_index(drop=True)
    q["rank"] = range(1, len(q) + 1)
    return q

def normalize_queue(queue):
    queue = queue.copy()
    if "priority" not in queue.columns:
        queue["priority"] = pick_column(queue, ["review_priority", "review_priority_level", "priority_level"], "Low")
    if "score" not in queue.columns:
        queue["score"] = pick_column(queue, ["priority_score", "attention_score", "supervisory_score"], 0)
    if "rank" not in queue.columns:
        queue["rank"] = pick_column(queue, ["review_rank", "priority_rank", "supervisory_rank"], None)
    aliases = {
        "execution_gap_findings": ["execution_gap_findings", "execution_gaps", "execution_gap_count"],
        "negative_space_findings": ["negative_space_findings", "negative_space", "negative_space_count"],
        "peer_deviations": ["peer_deviations", "peer_deviation_findings", "peer_deviation_count"],
        "operational_patterns": ["operational_patterns", "operational_pattern_findings", "operational_pattern_count"],
    }
    for standard, names in aliases.items():
        if standard not in queue.columns:
            queue[standard] = pick_column(queue, names, 0)
    if "rationale" not in queue.columns:
        queue["rationale"] = pick_column(queue, ["reason", "priority_rationale", "review_rationale"], "Evidence-based supervisory prioritization.")
    for col in ["rank", "score", "execution_gap_findings", "negative_space_findings", "peer_deviations", "operational_patterns"]:
        queue[col] = pd.to_numeric(queue[col], errors="coerce")
    if queue["rank"].isna().all():
        queue = queue.sort_values(["score", "assessment_id"], ascending=[False, True]).reset_index(drop=True)
        queue["rank"] = range(1, len(queue) + 1)
    else:
        missing = queue["rank"].isna()
        if missing.any():
            next_rank = int(queue["rank"].max()) + 1
            queue.loc[missing, "rank"] = range(next_rank, next_rank + int(missing.sum()))
    queue["rank"] = queue["rank"].astype(int)
    queue["score"] = queue["score"].fillna(0)
    return queue


def make_fig(fig, height=330):
    fig.update_layout(
        height=height,
        margin=dict(l=15, r=15, t=55, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6EDF7"),
        title_font=dict(size=14, color="#E6EDF7"),
        legend=dict(font=dict(color="#8EA2BA")),
    )
    fig.update_xaxes(gridcolor="rgba(100,140,180,.12)", zerolinecolor="rgba(100,140,180,.12)")
    fig.update_yaxes(gridcolor="rgba(100,140,180,.12)", zerolinecolor="rgba(100,140,180,.12)")
    return fig



# -------------------------------------------------------------------
# PS-complete supervisory analytics helpers
# -------------------------------------------------------------------
def _to_datetime(series):
    return pd.to_datetime(series, errors="coerce")


def _bool_series(series):
    if series is None:
        return pd.Series(dtype=bool)
    if series.dtype == bool:
        return series.fillna(False)
    return series.astype(str).str.strip().str.lower().isin(["true", "1", "yes", "y", "t"])


def _first_existing(df, names, default=None):
    if df is None or df.empty:
        return pd.Series(default, index=df.index if df is not None else [])
    for name in names:
        if name in df.columns:
            return df[name]
    return pd.Series(default, index=df.index)


def build_entity_supervisory_overview(queue_df, entities_df, assessments_df):
    """Aggregate assessment-level signals into an entity-level supervisory view."""
    q = normalize_queue(queue_df).copy()
    if q.empty:
        return pd.DataFrame()
    grouped = q.groupby("entity_id", as_index=False).agg(
        assessments=("assessment_id", "nunique"),
        attention_score=("score", "max"),
        avg_attention_score=("score", "mean"),
        execution_gaps=("execution_gap_findings", "sum"),
        negative_space=("negative_space_findings", "sum"),
        peer_deviations=("peer_deviations", "sum"),
        operational_patterns=("operational_patterns", "sum"),
    )
    grouped["attention"] = grouped["attention_score"].apply(
        lambda x: "High" if x >= 15 else ("Medium" if x >= 6 else "Low")
    )
    if not entities_df.empty:
        cols = [c for c in ["entity_id", "entity_name", "sector", "entity_size"] if c in entities_df.columns]
        grouped = grouped.merge(entities_df[cols].drop_duplicates("entity_id"), on="entity_id", how="left")
    if not assessments_df.empty:
        latest = assessments_df.copy()
        latest["period_end_dt"] = _to_datetime(latest.get("period_end", pd.Series(dtype=object)))
        latest = latest.sort_values("period_end_dt").drop_duplicates("entity_id", keep="last")
        if "assessment_id" in latest.columns:
            grouped = grouped.merge(latest[["entity_id", "assessment_id"]].rename(columns={"assessment_id": "latest_assessment"}), on="entity_id", how="left")
    def signal(row):
        vals = {
            "Execution gaps": row.get("execution_gaps", 0),
            "Negative space": row.get("negative_space", 0),
            "Peer deviation": row.get("peer_deviations", 0),
            "Operational pattern": row.get("operational_patterns", 0),
        }
        positive = {k: v for k, v in vals.items() if safe_num(v) > 0}
        return max(positive, key=positive.get) if positive else "No major signal"
    grouped["key_signal"] = grouped.apply(signal, axis=1)
    grouped = grouped.sort_values(["attention_score", "entity_id"], ascending=[False, True]).reset_index(drop=True)
    grouped["review_rank"] = range(1, len(grouped) + 1)
    return grouped


def build_trend_dataset(queue_df, assessments_df, cases_df, investigations_df):
    """Create assessment-period trend metrics without requiring raw SOC logs."""
    q = normalize_queue(queue_df).copy()
    a = assessments_df.copy()
    if a.empty or q.empty:
        return pd.DataFrame()
    a["period_end_dt"] = _to_datetime(a.get("period_end"))
    q = q.merge(a[["assessment_id", "entity_id", "period_start", "period_end", "period_end_dt"]], on=["assessment_id", "entity_id"], how="left")
    if not cases_df.empty:
        c = cases_df.copy()
        c["case_count"] = 1
        case_agg = c.groupby("assessment_id", as_index=False)["case_count"].sum()
        q = q.merge(case_agg, on="assessment_id", how="left")
    else:
        q["case_count"] = 0
    q["case_count"] = q["case_count"].fillna(0)
    q["weak_investigation_rate"] = q["execution_gap_findings"].fillna(0) / q["case_count"].replace(0, pd.NA) * 100
    q["weak_investigation_rate"] = q["weak_investigation_rate"].fillna(0)
    q["period_label"] = q["period_end_dt"].dt.strftime("%Y-%m-%d")
    return q.sort_values(["entity_id", "period_end_dt"])


def build_negative_space_findings(monitoring_df, assets_df, alerts_df, cases_df, assessments_df):
    """Detect expected-but-absent evidence patterns emphasized by SIH26157."""
    findings = []
    if monitoring_df is not None and not monitoring_df.empty:
        m = monitoring_df.copy()
        a = assessments_df[["assessment_id", "entity_id"]].drop_duplicates() if not assessments_df.empty else pd.DataFrame(columns=["assessment_id", "entity_id"])
        m = m.merge(a, on="assessment_id", how="left")
        m["telemetry_available_bool"] = _bool_series(m.get("telemetry_available", pd.Series(False, index=m.index)))
        if "expected_coverage_hours" in m.columns and "observed_coverage_hours" in m.columns:
            expected = pd.to_numeric(m["expected_coverage_hours"], errors="coerce").fillna(0)
            observed = pd.to_numeric(m["observed_coverage_hours"], errors="coerce").fillna(0)
            m["coverage_ratio"] = observed / expected.replace(0, pd.NA)
        elif "expected_coverage" in m.columns and "observed_coverage" in m.columns:
            expected = pd.to_numeric(m["expected_coverage"], errors="coerce").fillna(0)
            observed = pd.to_numeric(m["observed_coverage"], errors="coerce").fillna(0)
            m["coverage_ratio"] = observed / expected.replace(0, pd.NA)
        else:
            m["coverage_ratio"] = 1.0
        if not assets_df.empty:
            ac = assets_df[[c for c in ["asset_id", "entity_id", "asset_name", "criticality", "expected_monitoring"] if c in assets_df.columns]].drop_duplicates("asset_id")
            m = m.merge(ac, on=["asset_id", "entity_id"], how="left", suffixes=("", "_asset"))
        for _, r in m.iterrows():
            critical = str(r.get("criticality", "")).strip().lower() in {"critical", "high"}
            telemetry_missing = not bool(r.get("telemetry_available_bool", False))
            coverage = safe_num(r.get("coverage_ratio"), 1)
            low_coverage = coverage < 0.50
            if critical and (telemetry_missing or low_coverage):
                reasons = []
                if telemetry_missing:
                    reasons.append("telemetry unavailable")
                if low_coverage:
                    reasons.append(f"coverage {coverage*100:.1f}%")
                findings.append({
                    "entity_id": r.get("entity_id", ""),
                    "assessment_id": r.get("assessment_id", ""),
                    "asset_id": r.get("asset_id", ""),
                    "asset": r.get("asset_name", r.get("asset_id", "")),
                    "criticality": r.get("criticality", ""),
                    "signal": "Missing monitoring evidence",
                    "evidence": "; ".join(reasons),
                    "severity": "High" if telemetry_missing else "Medium",
                })
    # Low activity relative to assessment-level peer population.
    if not alerts_df.empty and not assessments_df.empty:
        counts = alerts_df.groupby("assessment_id", as_index=False).size().rename(columns={"size": "alert_count"})
        counts = counts.merge(assessments_df[["assessment_id", "entity_id"]], on="assessment_id", how="left")
        if len(counts) >= 3:
            peer_median = counts.groupby("entity_id")["alert_count"].median().median()
            for _, r in counts.iterrows():
                if safe_num(r["alert_count"]) < max(3, safe_num(peer_median) * 0.35):
                    findings.append({
                        "entity_id": r.get("entity_id", ""),
                        "assessment_id": r.get("assessment_id", ""),
                        "asset_id": "",
                        "asset": "Assessment activity",
                        "criticality": "",
                        "signal": "Unexpectedly low activity",
                        "evidence": f"{int(r['alert_count'])} alerts vs peer median {safe_num(peer_median):.0f}",
                        "severity": "Medium",
                    })
    return pd.DataFrame(findings)


def build_anomaly_findings(cases_df, investigations_df, alerts_df):
    """Identify transparent operational outliers; no black-box ML is required."""
    findings = []
    if investigations_df is not None and not investigations_df.empty:
        inv = investigations_df.copy()
        if "start_time" in inv.columns and "end_time" in inv.columns:
            inv["start_dt"] = _to_datetime(inv["start_time"])
            inv["end_dt"] = _to_datetime(inv["end_time"])
            inv["duration_minutes"] = (inv["end_dt"] - inv["start_dt"]).dt.total_seconds() / 60
        else:
            inv["duration_minutes"] = pd.to_numeric(inv.get("duration_minutes", 0), errors="coerce")
        inv["duration_minutes"] = inv["duration_minutes"].fillna(0)
        median_duration = float(inv["duration_minutes"].median()) if not inv.empty else 0
        low_threshold = max(5, median_duration * 0.20)
        for _, r in inv[inv["duration_minutes"] <= low_threshold].sort_values("duration_minutes").head(100).iterrows():
            findings.append({
                "case_id": r.get("case_id", ""),
                "signal": "Low investigation effort outlier",
                "metric": "Investigation duration",
                "observed": f"{safe_num(r.get('duration_minutes')):.1f} min",
                "benchmark": f"dataset median {median_duration:.1f} min",
                "severity": "High" if safe_num(r.get("duration_minutes")) <= 30 else "Medium",
            })
        if "template_id" in inv.columns:
            template_counts = inv[inv["template_id"].notna()].groupby("template_id").size().sort_values(ascending=False)
            for template, count in template_counts.head(5).items():
                if count >= max(5, len(inv) * 0.15):
                    findings.append({
                        "case_id": "Multiple",
                        "signal": "Repetitive investigation pattern",
                        "metric": "Template reuse",
                        "observed": int(count),
                        "benchmark": f"{count/len(inv)*100:.1f}% of investigations",
                        "severity": "Medium",
                    })
    if cases_df is not None and not cases_df.empty and "case_created_time" in cases_df.columns and "closure_time" in cases_df.columns:
        c = cases_df.copy()
        c["created_dt"] = _to_datetime(c["case_created_time"])
        c["closed_dt"] = _to_datetime(c["closure_time"])
        c["closure_hours"] = (c["closed_dt"] - c["created_dt"]).dt.total_seconds() / 3600
        for _, r in c[(c["closure_hours"] >= 0) & (c["closure_hours"] <= 12) & (c["priority"].astype(str).str.lower().isin(["high", "critical"]))].head(100).iterrows():
            findings.append({
                "case_id": r.get("case_id", ""),
                "signal": "High-severity rapid closure",
                "metric": "Closure time",
                "observed": f"{safe_num(r.get('closure_hours')):.1f} h",
                "benchmark": "High/Critical case reviewed for rapid closure",
                "severity": "High",
            })
    return pd.DataFrame(findings)


def build_manual_review_samples(selected_assessment, cases_df, investigations_df, escalations_df, alerts_df):
    """Create a transparent case/sample queue for human examiner review."""
    c = cases_df[cases_df["assessment_id"] == selected_assessment].copy() if "assessment_id" in cases_df.columns else pd.DataFrame()
    if c.empty:
        return pd.DataFrame()
    if "case_id" not in c.columns:
        return pd.DataFrame()
    c["manual_review_score"] = 0.0
    c["review_reason"] = ""
    inv = investigations_df[investigations_df["case_id"].astype(str).isin(c["case_id"].astype(str))].copy() if not investigations_df.empty else pd.DataFrame()
    esc_ids = set(escalations_df["case_id"].astype(str)) if not escalations_df.empty and "case_id" in escalations_df.columns else set()
    inv_map = {}
    if not inv.empty:
        if "start_time" in inv.columns and "end_time" in inv.columns:
            inv["duration_minutes"] = (_to_datetime(inv["end_time"]) - _to_datetime(inv["start_time"])).dt.total_seconds() / 60
        else:
            inv["duration_minutes"] = pd.to_numeric(inv.get("duration_minutes", 0), errors="coerce")
        for _, r in inv.iterrows():
            inv_map[str(r.get("case_id"))] = r
    reasons = []
    for idx, r in c.iterrows():
        score = 0.0
        rs = []
        priority = str(r.get("priority", "")).lower()
        if priority == "critical": score += 5; rs.append("Critical priority")
        elif priority == "high": score += 3; rs.append("High priority")
        inv_row = inv_map.get(str(r.get("case_id")))
        if inv_row is None:
            score += 3; rs.append("No investigation record")
        else:
            if safe_num(inv_row.get("evidence_count")) <= 2: score += 2; rs.append("Low evidence count")
            if safe_num(inv_row.get("steps_recorded")) <= 2: score += 2; rs.append("Few investigation steps")
            if not bool(_bool_series(pd.Series([inv_row.get("root_cause_identified", False)])).iloc[0]): score += 1; rs.append("No root-cause record")
            if not bool(_bool_series(pd.Series([inv_row.get("remediation_recorded", False)])).iloc[0]): score += 1; rs.append("No remediation record")
            if safe_num(inv_row.get("duration_minutes")) <= 30: score += 2; rs.append("Very short investigation")
        if str(r.get("case_id")) not in esc_ids and priority in {"high", "critical"}:
            score += 2; rs.append("No escalation record for high-severity case")
        c.at[idx, "manual_review_score"] = score
        reasons.append("; ".join(rs) if rs else "Representative sample")
    c["review_reason"] = reasons
    return c.sort_values(["manual_review_score", "priority"], ascending=[False, False]).head(10)


def build_traceability(selected_assessment, selected_entity, queue_df, cases_df, investigations_df, escalations_df, monitoring_df, assets_df):
    """Return an explicit evidence chain for the selected assessment."""
    q = normalize_queue(queue_df)
    row = q[q["assessment_id"] == selected_assessment]
    if row.empty:
        return []
    r = row.iloc[0]
    chains = []
    signal_map = [
        ("Execution gaps", r.get("execution_gap_findings", 0), "Execution-gap engine / assessment-level evidence"),
        ("Negative space", r.get("negative_space_findings", 0), "Negative-space analysis / expected evidence absence"),
        ("Peer deviations", r.get("peer_deviations", 0), "Peer benchmark comparison"),
        ("Operational patterns", r.get("operational_patterns", 0), "Operational anomaly/pattern analysis"),
    ]
    for signal, count, rule in signal_map:
        if safe_num(count) > 0:
            chains.append({
                "Supervisory indicator": f"{selected_entity} — {signal}",
                "Why flagged": f"{safe_num(count):.0f} signal(s) linked to {selected_assessment}",
                "Analytic source": rule,
                "Supporting evidence": "Cases / investigations / escalations / monitoring records",
                "Underlying record": selected_assessment,
            })
    return chains


def render_ps_coverage_panel(queue_df, entities_df, assessments_df, cases_df, monitoring_df):
    coverage = [
        ("Structured multi-CSE ingestion", "PASS", "CSV/JSON upload + validation; database/API adapters are deployment-specific"),
        ("Execution-gap detection", "PASS", "Existing execution-gap analytics + dashboard evidence"),
        ("Negative-space detection", "PASS", "Critical monitoring / telemetry absence and low-activity signals"),
        ("Anomaly / outlier analysis", "PASS", "Transparent duration, closure and repetitive-pattern rules"),
        ("Peer comparison / benchmarking", "PASS", "Existing peer benchmark and deviation analytics"),
        ("Entity-level supervisory indicators", "PASS", "Entity aggregation of assessment signals"),
        ("Manual-review prioritisation", "PASS", "Assessment queue + case-level review samples"),
        ("Rationale and supporting evidence", "PASS", "Explainability and evidence drill-down"),
        ("Traceability / auditability", "PASS", "Indicator → analytic source → evidence → underlying record"),
        ("Trend analysis", "PASS", "Assessment-period trend metrics across time"),
        ("Dashboards / reports", "PASS", "Dashboard + organisation PDF report"),
        ("Offline / air-gapped design", "PASS", "Local processing; no external service dependency in dashboard"),
        ("Human-in-the-loop", "PASS", "All findings framed as supervisory signals, not final compliance judgments"),
        ("AI/ML governance", "DESIGN NOTE", "Current prototype uses deterministic/explainable analytics; no external AI model dependency"),
    ]
    df = pd.DataFrame(coverage, columns=["PS capability", "Status", "Implementation note"])
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption("Coverage labels describe the current prototype implementation; production deployment still requires validated CSE data, threshold calibration and expert validation.")




# -------------------------------------------------------------------
# Shared application context
# -------------------------------------------------------------------
def get_demo_data():
    return {
        "entities": load_csv("entities.csv"),
        "assessments": load_csv("assessments.csv"),
        "alerts": load_csv("alerts.csv"),
        "cases": load_csv("cases.csv"),
        "investigations": load_csv("investigations.csv"),
        "escalations": load_csv("escalations.csv"),
        "assets": load_csv("assets.csv"),
        "monitoring": load_csv("monitoring.csv"),
    }

def get_active_data():
    demo = get_demo_data()
    if st.session_state.get("tl_active_source") == "uploaded" and st.session_state.get("tl_validated_upload"):
        active = st.session_state["tl_validated_upload"]
        data = {k: active.get(k, demo[k]) for k in demo}
        q = normalize_queue(build_uploaded_supervisory_queue(data))
        if not q.empty:
            return data, q
        st.session_state["tl_active_source"] = "demo"
    return demo, normalize_queue(load_queue())

def get_active_features():
    return load_features()

def priority_counts(queue_df):
    return {p: int((queue_df["priority"] == p).sum()) for p in ["High", "Medium", "Low"]}

def render_header():
    st.markdown(
        """<div class="tl-app-header">
            <div class="tl-app-brand">
                <div class="tl-app-mark"><svg viewBox="0 0 48 48"><path d="M24 4 40 10v11c0 10.5-6.2 18.3-16 23C14.2 39.3 8 31.5 8 21V10l16-6Z" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="m16 24 5 5 11-12" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
                <div><div class="tl-app-name">Peril<span>Lens</span></div><div class="tl-app-sub">SAT-SA · Supervisory Analytics</div></div>
            </div>
            <div class="tl-header-status"><span></span> OFFLINE · CONTROLLED</div>
        </div>""",
        unsafe_allow_html=True,
    )


def render_sidebar_status(data):
    source = "Validated CSE submission" if st.session_state.get("tl_active_source") == "uploaded" else "Demonstration dataset"
    selected = st.session_state.get("tl_selected_assessment", "ALL")
    assessment_label = "All assessments" if selected == "ALL" else str(selected)
    st.sidebar.markdown("<div class='tl-side-brand'><div class='tl-side-mark'>✓</div><div><b>Peril-Lens</b><small>Supervisory workspace</small></div></div>", unsafe_allow_html=True)
    st.sidebar.markdown("<div class='tl-side-divider'></div>", unsafe_allow_html=True)
    st.sidebar.markdown("<div class='tl-side-heading'>WORKSPACE</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div class='tl-context'><span>Current assessment</span><b>{assessment_label}</b></div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div class='tl-context'><span>Source</span><b>{source}</b></div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div class='tl-context'><span>Entities</span><b>{len(data['entities']):,}</b></div>", unsafe_allow_html=True)
    st.sidebar.markdown("<div class='tl-side-divider'></div>", unsafe_allow_html=True)
    st.sidebar.caption("Decision support for human examiners · not a SOC, SIEM or real-time monitoring system")

