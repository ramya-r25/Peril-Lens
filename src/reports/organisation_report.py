from __future__ import annotations

from io import BytesIO
from datetime import datetime

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)


NAVY = colors.HexColor("#0B1220")
BLUE = colors.HexColor("#00A8FF")
CYAN = colors.HexColor("#22D3EE")
RED = colors.HexColor("#F04444")
AMBER = colors.HexColor("#F59E0B")
GREEN = colors.HexColor("#22C55E")
SLATE = colors.HexColor("#475569")
LIGHT = colors.HexColor("#F1F5F9")
BORDER = colors.HexColor("#CBD5E1")
WHITE = colors.white


def _safe_num(value, default=0.0):
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def _safe_text(value, fallback="Not available"):
    if value is None:
        return fallback
    try:
        if pd.isna(value):
            return fallback
    except Exception:
        pass
    return str(value)


def _status_style(status: str):
    status = str(status).upper()
    if status == "HIGH" or status == "ATTENTION":
        return RED
    if status in {"MEDIUM", "REVIEW"}:
        return AMBER
    return GREEN


def _section(title, subtitle=None):
    items = [Paragraph(title, ParagraphStyle(
        "Section",
        parent=getSampleStyleSheet()["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=NAVY,
        spaceBefore=7,
        spaceAfter=5,
    ))]
    if subtitle:
        items.append(Paragraph(subtitle, ParagraphStyle(
            "SectionSub",
            fontName="Helvetica",
            fontSize=8.5,
            leading=12,
            textColor=SLATE,
            spaceAfter=7,
        )))
    return items


def _table(data, widths=None, header=True, font_size=8):
    converted = []
    for r, row in enumerate(data):
        converted.append([
            Paragraph(_safe_text(cell), ParagraphStyle(
                f"Cell{r}",
                fontName="Helvetica-Bold" if header and r == 0 else "Helvetica",
                fontSize=font_size,
                leading=10,
                textColor=WHITE if header and r == 0 else NAVY,
            )) for cell in row
        ])
    tbl = Table(converted, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        commands += [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ]
        if len(data) > 1:
            commands.append(("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]))
    tbl.setStyle(TableStyle(commands))
    return tbl


def _paragraph(text, style=None):
    styles = getSampleStyleSheet()
    if style is None:
        style = ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=NAVY,
            spaceAfter=6,
        )
    return Paragraph(str(text), style)


def _bullet(text):
    return Paragraph(
        f"• {text}",
        ParagraphStyle(
            "Bullet",
            fontName="Helvetica",
            fontSize=8.8,
            leading=12,
            leftIndent=10,
            firstLineIndent=-6,
            textColor=NAVY,
            spaceAfter=3,
        ),
    )


def _page_header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 14 * mm, width, 14 * mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(16 * mm, height - 9 * mm, "THREATLENS")
    canvas.setFont("Helvetica", 7.5)
    canvas.drawRightString(width - 16 * mm, height - 9 * mm, "SAT-SA · OFFLINE SUPERVISORY ANALYTICS")

    canvas.setStrokeColor(BORDER)
    canvas.line(16 * mm, 12 * mm, width - 16 * mm, 12 * mm)
    canvas.setFillColor(SLATE)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(16 * mm, 7 * mm, "Evidence-based supervisory support · Human review required")
    canvas.drawRightString(width - 16 * mm, 7 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build_organisation_report(
    assessment_id,
    entity_name,
    entity_id,
    period_text,
    selected_row,
    sel_alerts,
    sel_cases,
    sel_investigations,
    sel_escalations,
    execution_evidence,
    negative_evidence,
    peer_evidence,
    operational_evidence,
    case_features,
    assets=None,
    monitoring=None,
    dataset_label="Synthetic Prototype Dataset",
):
    """Generate a self-contained PDF report in memory for local/offline download."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=22 * mm,
        bottomMargin=17 * mm,
        title=f"Peril-Lens{entity_name}_{assessment_id}_Supervisory_Assessment",
        author="Peril-Lens",
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleX", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=25, leading=29, textColor=NAVY, alignment=TA_LEFT, spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "SubX", fontName="Helvetica", fontSize=10.5, leading=14,
        textColor=SLATE, spaceAfter=10,
    )
    executive_style = ParagraphStyle(
        "Executive", fontName="Helvetica", fontSize=9.5, leading=14,
        textColor=NAVY, backColor=LIGHT, borderPadding=9, borderColor=BORDER,
        borderWidth=0.5, borderRadius=3, spaceAfter=8,
    )
    small_style = ParagraphStyle(
        "Small", fontName="Helvetica", fontSize=7.5, leading=10, textColor=SLATE,
    )

    priority = _safe_text(selected_row.get("priority", "Unknown"), "Unknown")
    score = _safe_num(selected_row.get("score", 0))
    rationale = _safe_text(selected_row.get("rationale", "Evidence-based supervisory prioritization."))

    total_alerts = len(sel_alerts)
    total_cases = len(sel_cases)
    high_critical = int(sel_cases["priority"].isin(["High", "Critical"]).sum()) if "priority" in sel_cases.columns else 0
    investigated = len(sel_investigations)
    escalated = int(sel_escalations["case_id"].nunique()) if not sel_escalations.empty and "case_id" in sel_escalations.columns else 0
    closed = int((sel_cases["status"] == "Closed").sum()) if "status" in sel_cases.columns else 0

    story = []

    # Cover / executive section
    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph("THREATLENS", title_style))
    story.append(Paragraph("Organisation Supervisory Assessment Report", ParagraphStyle(
        "CoverSub", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=BLUE, spaceAfter=3,
    )))
    story.append(Paragraph("SAT-SA · Supervisory Analytics Tool for SOC Assessment", subtitle_style))

    cover_data = [
        ["Organisation", entity_name],
        ["Entity ID", entity_id],
        ["Assessment", assessment_id],
        ["Assessment period", period_text],
        ["Dataset", dataset_label],
        ["Report generated", datetime.now().strftime("%d %b %Y, %H:%M")],
    ]
    story.append(_table(cover_data, widths=[42 * mm, 128 * mm], header=False, font_size=8.5))
    story.append(Spacer(1, 7 * mm))

    attention_color = _status_style(priority)
    priority_box = Table([[Paragraph(
        f"<b>SUPERVISORY ATTENTION: {priority.upper()}</b><br/>Priority score: {score:.0f}<br/><font color='#475569'>{rationale}</font>",
        ParagraphStyle("Priority", fontName="Helvetica", fontSize=10, leading=14, textColor=NAVY),
    )]], colWidths=[170 * mm])
    priority_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.Color(attention_color.red, attention_color.green, attention_color.blue, alpha=0.08)),
        ("BOX", (0, 0), (-1, -1), 1.3, attention_color),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    story.append(priority_box)
    story.append(Spacer(1, 5 * mm))

    story.extend(_section("1. Executive Summary"))
    story.append(_paragraph(
        f"Peril-Lens analyzed the available SOC assessment records for <b>{entity_name}</b> "
        f"and identified evidence-based indicators intended to help an examiner focus manual review. "
        f"The assessment received a <b>{priority.lower()}</b> supervisory attention level with a prototype priority score of <b>{score:.0f}</b>."
    ))

    story.extend(_section("1.1 Assessment Overview"))
    overview = [
        ["Metric", "Value"],
        ["Alerts", total_alerts],
        ["Cases", total_cases],
        ["High / Critical cases", high_critical],
        ["Investigated cases", investigated],
        ["Escalated cases", escalated],
        ["Closed cases", closed],
    ]
    story.append(_table(overview, widths=[105 * mm, 65 * mm]))

    story.extend(_section("1.2 Key Supervisory Signals"))
    if operational_evidence.empty and peer_evidence.empty and negative_evidence.empty and execution_evidence.empty:
        story.append(_paragraph("No major supervisory signals were identified by the current prototype rules."))
    else:
        for _, row in operational_evidence.head(4).iterrows():
            signal = _safe_text(row.get("signal_type", row.get("pattern_type", "Operational pattern")))
            affected = row.get("affected_cases", row.get("affected_case_count", None))
            suffix = f" — {int(_safe_num(affected))} affected case(s)." if pd.notna(affected) else "."
            story.append(_bullet(f"{signal}{suffix}"))
        for _, row in peer_evidence.head(3).iterrows():
            metric = _safe_text(row.get("metric", row.get("metric_name", "Peer metric")))
            value = _safe_num(row.get("metric_value", 0))
            avg = _safe_num(row.get("peer_average", 0))
            story.append(_bullet(f"Peer deviation: {metric} = {value:.2f}% (available peer average: {avg:.2f}%)."))
        for _, row in negative_evidence.head(3).iterrows():
            reason = _safe_text(row.get("reason", row.get("signal_type", "Expected evidence appears limited")))
            story.append(_bullet(f"Potential negative-space condition: {reason}."))
        if not execution_evidence.empty:
            story.append(_bullet(f"Execution-gap evidence: {len(execution_evidence)} finding(s) identified for supervisory review."))

    story.append(PageBreak())

    # Profile / data quality
    story.extend(_section("2. Organisation & Assessment Profile"))
    story.extend(_section("2.1 Organisation Information"))
    story.append(_table([
        ["Field", "Value"],
        ["Organisation", entity_name],
        ["Entity ID", entity_id],
        ["Assessment ID", assessment_id],
        ["Assessment period", period_text],
        ["Deployment context", "Offline / controlled environment"],
    ], widths=[65 * mm, 105 * mm]))

    story.extend(_section("2.2 SOC Activity Summary"))
    story.append(_table(overview, widths=[105 * mm, 65 * mm]))

    story.extend(_section("3. Data Quality & Assessment Readiness"))
    missing_checks = []
    if "acknowledgement_time" in sel_alerts.columns:
        missing_checks.append(("Alert acknowledgement time", int(sel_alerts["acknowledgement_time"].isna().sum())))
    if "case_id" in sel_alerts.columns:
        missing_checks.append(("Alert case linkage", int(sel_alerts["case_id"].isna().sum())))
    if "closure_time" in sel_cases.columns:
        missing_checks.append(("Case closure time", int(sel_cases["closure_time"].isna().sum())))
    if "closure_reason" in sel_cases.columns:
        missing_checks.append(("Case closure reason", int(sel_cases["closure_reason"].isna().sum())))
    if "template_id" in sel_investigations.columns:
        missing_checks.append(("Investigation template", int(sel_investigations["template_id"].isna().sum())))
    total_missing = sum(v for _, v in missing_checks)
    readiness = "Suitable for prototype analysis" if total_missing < max(1, total_alerts * 0.25) else "Review data completeness before interpretation"
    quality_data = [["Quality check", "Observation"]]
    quality_data += [[name, count] for name, count in missing_checks]
    quality_data.append(["Readiness", readiness])
    story.append(_table(quality_data, widths=[105 * mm, 65 * mm]))
    story.append(_paragraph(
        "Data-quality observations describe the supplied assessment records. Missing fields do not automatically indicate an operational weakness; "
        "they may instead reflect source-system export limitations and should be interpreted by the examiner."
    ))

    story.extend(_section("4. Supervisory Signal Profile"))
    profile_rows = [["Signal area", "Status", "Evidence / observation"]]
    def add_profile(name, status, observation):
        profile_rows.append([name, status, observation])

    add_profile("Execution & investigation", "ATTENTION" if not execution_evidence.empty else "NO SIGNAL", f"{len(execution_evidence)} finding(s)")
    rapid = sum(1 for _, r in operational_evidence.iterrows() if "Rapid" in _safe_text(r.get("signal_type", "")))
    add_profile("Closure behaviour", "ATTENTION" if rapid else "NO SIGNAL", "Rapid-closure pattern present" if rapid else "No rapid-closure pattern identified")
    add_profile("Escalation practice", "REVIEW" if not execution_evidence.empty else "NO SIGNAL", "Review relevant High/Critical escalation decisions")
    add_profile("Monitoring coverage", "REVIEW" if not negative_evidence.empty else "NO SIGNAL", f"{len(negative_evidence)} potential negative-space finding(s)")
    add_profile("Peer position", "ATTENTION" if not peer_evidence.empty else "NO SIGNAL", f"{len(peer_evidence)} peer deviation finding(s)")
    story.append(_table(profile_rows, widths=[52 * mm, 32 * mm, 86 * mm]))

    story.append(PageBreak())

    # Evidence sections
    story.extend(_section("5. Execution & Investigation Analysis"))
    story.extend(_section("5.1 Execution-Gap Findings"))
    if execution_evidence.empty:
        story.append(_paragraph("No execution-gap findings were identified for this assessment."))
    else:
        rows = [["Case", "Signal", "Reason"]]
        for _, r in execution_evidence.head(30).iterrows():
            rows.append([
                _safe_text(r.get("case_id", "-")),
                _safe_text(r.get("signal_type", r.get("finding_type", "Execution gap"))),
                _safe_text(r.get("reason", "Evidence pattern identified")),
            ])
        story.append(_table(rows, widths=[30 * mm, 55 * mm, 85 * mm], font_size=7.2))
        if len(execution_evidence) > 30:
            story.append(_paragraph(f"Showing the first 30 of {len(execution_evidence)} findings; the dashboard provides full drill-down."))

    story.extend(_section("5.2 Investigation Quality Signals"))
    if not case_features.empty and "weak_investigation" in case_features.columns:
        weak_count = int(case_features["weak_investigation"].fillna(False).sum())
        story.append(_paragraph(f"The feature pipeline identified <b>{weak_count}</b> case record(s) with the prototype weak-investigation characteristics."))
    else:
        story.append(_paragraph("Weak-investigation feature data is not available in the selected assessment."))

    story.extend(_section("5.3 Escalation Review"))
    story.append(_paragraph(
        f"{escalated} unique case(s) are represented in the escalation records for this assessment. "
        "High/Critical cases associated with execution-gap findings should be examined against the organisation's escalation procedures and recorded rationale."
    ))

    story.extend(_section("6. Negative-Space Analysis"))
    if negative_evidence.empty:
        story.append(_paragraph("No potential negative-space conditions were identified by the current prototype rules."))
    else:
        rows = [["Asset", "Signal", "Observation"]]
        for _, r in negative_evidence.iterrows():
            rows.append([
                _safe_text(r.get("asset_id", "-")),
                _safe_text(r.get("signal_type", "Potential negative space")),
                _safe_text(r.get("reason", "Expected evidence appears limited")),
            ])
        story.append(_table(rows, widths=[35 * mm, 50 * mm, 85 * mm]))
        story.append(_paragraph("These observations indicate potential conditions requiring supervisory review; they are not final compliance findings."))

    story.extend(_section("7. Operational Pattern Analysis"))
    if operational_evidence.empty:
        story.append(_paragraph("No operational-pattern findings were identified."))
    else:
        rows = [["Pattern", "Affected cases", "Metric / observation"]]
        for _, r in operational_evidence.iterrows():
            affected = r.get("affected_cases", r.get("affected_case_count", "-"))
            metric = r.get("metric_value", r.get("metric", "-"))
            rows.append([_safe_text(r.get("signal_type", r.get("pattern_type", "Operational pattern"))), _safe_text(affected), _safe_text(metric)])
        story.append(_table(rows, widths=[75 * mm, 35 * mm, 60 * mm]))

    story.append(PageBreak())

    story.extend(_section("8. Peer Benchmarking"))
    if peer_evidence.empty:
        story.append(_paragraph("No peer deviations were identified for this assessment."))
    else:
        rows = [["Metric", "Observed", "Peer average", "Threshold", "Interpretation"]]
        for _, r in peer_evidence.iterrows():
            rows.append([
                _safe_text(r.get("metric", r.get("metric_name", "Peer metric"))),
                f"{_safe_num(r.get('metric_value', 0)):.2f}%",
                f"{_safe_num(r.get('peer_average', 0)):.2f}%",
                f"{_safe_num(r.get('threshold', 0)):.2f}%",
                _safe_text(r.get("reason", "Deviation from available peers")),
            ])
        story.append(_table(rows, widths=[34 * mm, 27 * mm, 27 * mm, 27 * mm, 55 * mm], font_size=7.2))
        story.append(_paragraph("Peer benchmarking is based on the available assessment population. In this prototype, it should be treated as an analytical comparison rather than a validated industry benchmark."))

    story.extend(_section("9. Supervisory Attention & Prioritization"))
    story.append(_table([
        ["Component", "Contribution / evidence"],
        ["Execution-gap evidence", str(int(_safe_num(selected_row.get("execution_gap_findings", 0))))],
        ["Negative-space evidence", str(int(_safe_num(selected_row.get("negative_space_findings", 0))))],
        ["Peer deviations", str(int(_safe_num(selected_row.get("peer_deviations", 0))))],
        ["Operational patterns", str(int(_safe_num(selected_row.get("operational_patterns", 0))))],
        ["Prototype priority score", f"{score:.0f}"],
        ["Review priority", priority],
    ], widths=[80 * mm, 90 * mm]))
    story.append(_paragraph("The prototype score supports ordering of supervisory review. It is not a final compliance or risk judgment."))

    story.extend(_section("10. Representative Case Investigation"))
    reps = case_features.copy()
    if not reps.empty and "assessment_id" in reps.columns:
        reps = reps[reps["assessment_id"] == assessment_id].copy()
    if not reps.empty and "case_id" in reps.columns:
        if "priority" in reps.columns:
            order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
            reps["_order"] = reps["priority"].map(order).fillna(9)
            reps = reps.sort_values("_order")
        reps = reps.drop_duplicates("case_id").head(10)
    if reps.empty:
        story.append(_paragraph("No representative case records are available."))
    else:
        rows = [["Case", "Priority", "Closure (h)", "Evidence", "Steps", "Escalated"]]
        for _, r in reps.iterrows():
            rows.append([
                _safe_text(r.get("case_id", "-")),
                _safe_text(r.get("priority", "-")),
                f"{_safe_num(r.get('closure_hours', 0)):.1f}" if pd.notna(r.get("closure_hours", None)) else "-",
                _safe_text(r.get("evidence_count", "-")),
                _safe_text(r.get("steps_recorded", "-")),
                "Yes" if bool(r.get("was_escalated", False)) else "No",
            ])
        story.append(_table(rows, widths=[30 * mm, 27 * mm, 30 * mm, 25 * mm, 25 * mm, 33 * mm], font_size=7.5))

    story.extend(_section("11. Recommended Supervisory Review Actions"))
    actions = [
        "Review representative cases associated with the flagged patterns.",
        "Examine investigation evidence, recorded steps, root-cause analysis and remediation.",
        "Review escalation decisions for relevant High/Critical cases.",
        "Examine assets associated with potential negative-space conditions.",
        "Compare relevant operational metrics with available peer assessments.",
        "Use supervisory judgment before reaching any final conclusion.",
    ]
    for action in actions:
        story.append(_bullet(action))

    story.extend(_section("12. Evidence & Traceability"))
    story.append(_paragraph(
        "Peril-Lens follows an evidence-to-signal-to-priority workflow. Source records are transformed into analytical features; "
        "the analytical engines identify patterns; the prioritization layer orders assessments for review; and the explanation layer exposes supporting evidence."
    ))
    story.append(_table([
        ["Source layer", "Used for"],
        ["Alerts", "Severity, timestamps, acknowledgement and case linkage"],
        ["Cases", "Closure, status, priority and case workflow"],
        ["Investigations", "Evidence, recorded steps, root cause and remediation"],
        ["Escalations", "Escalation decisions and workflow evidence"],
        ["Assets / Monitoring", "Expected vs observed monitoring conditions"],
        ["Peer assessments", "Assessment-level comparative analysis"],
    ], widths=[45 * mm, 125 * mm], font_size=7.8))

    story.extend(_section("13. Methodology"))
    for item in [
        "Data ingestion and normalization",
        "Feature engineering for case and investigation behaviour",
        "Execution-gap analysis",
        "Negative-space analysis",
        "Operational-pattern analysis",
        "Peer benchmarking",
        "Evidence-based supervisory prioritization",
        "Explainability and representative-case selection",
    ]:
        story.append(_bullet(item))

    story.extend(_section("14. Limitations & Interpretation"))
    for item in [
        "The current prototype uses synthetic assessment data for validation and demonstration.",
        "Peer comparisons reflect the available prototype assessment population and are not a validated industry benchmark.",
        "Thresholds and prioritization weights require calibration against expert-reviewed organisational data before production use.",
        "Source-data quality can affect the visibility of supervisory signals.",
        "Production deployment requires governance, validated source mappings, security controls and expert validation.",
    ]:
        story.append(_bullet(item))

    story.extend(_section("15. Supervisory Disclaimer"))
    story.append(_paragraph(
        "<b>Peril-Lens identifies evidence and potential supervisory concerns from the available assessment data. "
        "It does not make final compliance, regulatory or risk determinations. All findings are intended to support, not replace, expert supervisory judgment.</b>",
        executive_style,
    ))

    story.extend(_section("16. Report Metadata"))
    story.append(_table([
        ["Field", "Value"],
        ["Product", "Peril-Lens"],
        ["Problem statement context", "SAT-SA · Supervisory Analytics Tool for SOC Assessment"],
        ["Deployment mode", "Offline / air-gapped capable"],
        ["Assessment", assessment_id],
        ["Dataset", dataset_label],
        ["Generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
    ], widths=[65 * mm, 105 * mm], font_size=8))

    doc.build(story, onFirstPage=_page_header_footer, onLaterPages=_page_header_footer)
    buffer.seek(0)
    return buffer.getvalue()
