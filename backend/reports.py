from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from database import SessionLocal, AttackLog

import csv
import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


reports_router = APIRouter()


# ============================================================
# REPORT SUMMARY
# ============================================================

@reports_router.get("/reports/summary")
def report_summary():

    db = SessionLocal()

    try:

        logs = (
            db.query(AttackLog)
            .order_by(AttackLog.created_at.desc())
            .all()
        )

        total = len(logs)

        blocked = sum(
            1 for log in logs
            if log.defense_triggered
        )

        allowed = total - blocked

        average_score = (
            sum(
                float(log.detection_score or 0)
                for log in logs
            ) / total
            if total > 0
            else 0
        )

        return {
            "success": True,
            "generated_at": datetime.now().isoformat(),
            "total_attacks": total,
            "blocked_attacks": blocked,
            "allowed_attacks": allowed,
            "average_risk_score": round(
                average_score,
                2
            )
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

    finally:

        db.close()


# ============================================================
# CSV REPORT
# ============================================================

@reports_router.get("/reports/csv")
def generate_csv_report():

    db = SessionLocal()

    try:

        logs = (
            db.query(AttackLog)
            .order_by(AttackLog.created_at.desc())
            .all()
        )

        output = io.StringIO()

        writer = csv.writer(output)

        # Header
        writer.writerow([
            "ID",
            "Attack Type",
            "Payload",
            "Risk Score",
            "Blocked",
            "Latency",
            "Username",
            "Role",
            "Created At"
        ])

        # Data
        for log in logs:

            writer.writerow([
                log.id,
                log.attack_type,
                log.payload,
                log.detection_score,
                "Yes" if log.defense_triggered else "No",
                log.latency,
                log.username,
                log.role,
                log.created_at
            ])

        output.seek(0)

        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition":
                    "attachment; filename=llm_security_report.csv"
            }
        )

    finally:

        db.close()


# ============================================================
# PDF REPORT
# ============================================================

@reports_router.get("/reports/pdf")
def generate_pdf_report():

    db = SessionLocal()

    try:

        logs = (
            db.query(AttackLog)
            .order_by(AttackLog.created_at.desc())
            .all()
        )

        total = len(logs)

        blocked = sum(
            1 for log in logs
            if log.defense_triggered
        )

        allowed = total - blocked

        average_score = (
            sum(
                float(log.detection_score or 0)
                for log in logs
            ) / total
            if total > 0
            else 0
        )

        # ----------------------------------------------------
        # CREATE PDF IN MEMORY
        # ----------------------------------------------------

        buffer = io.BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=30
        )

        styles = getSampleStyleSheet()

        elements = []

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        elements.append(
            Paragraph(
                "LLM Security Attack Report",
                styles["Title"]
            )
        )

        elements.append(
            Spacer(1, 15)
        )

        elements.append(
            Paragraph(
                f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
                styles["Normal"]
            )
        )

        elements.append(
            Spacer(1, 20)
        )

        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        elements.append(
            Paragraph(
                "Security Summary",
                styles["Heading2"]
            )
        )

        summary_data = [
            ["Metric", "Value"],
            ["Total Attacks", str(total)],
            ["Blocked Attacks", str(blocked)],
            ["Allowed Attacks", str(allowed)],
            [
                "Average Risk Score",
                f"{average_score:.2f}"
            ]
        ]

        summary_table = Table(
            summary_data,
            colWidths=[250, 150]
        )

        summary_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#2563eb")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )
            ])
        )

        elements.append(summary_table)

        elements.append(
            Spacer(1, 25)
        )

        # ----------------------------------------------------
        # ATTACK LOGS
        # ----------------------------------------------------

        elements.append(
            Paragraph(
                "Attack Logs",
                styles["Heading2"]
            )
        )

        table_data = [
            [
                "ID",
                "Attack",
                "Risk",
                "Blocked",
                "Latency"
            ]
        ]

        for log in logs:

            table_data.append([
                str(log.id),
                str(log.attack_type),
                str(log.detection_score),
                "Yes" if log.defense_triggered else "No",
                str(log.latency)
            ])

        attack_table = Table(
            table_data,
            colWidths=[
                40,
                150,
                60,
                70,
                70
            ]
        )

        attack_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#2563eb")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ])
        )

        elements.append(attack_table)

        # ----------------------------------------------------
        # BUILD PDF
        # ----------------------------------------------------

        document.build(elements)

        buffer.seek(0)

        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                    "attachment; filename=llm_security_report.pdf"
            }
        )

    finally:

        db.close()