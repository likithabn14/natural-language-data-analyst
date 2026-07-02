import io
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle


# -----------------------------
# CSV Export
# -----------------------------
def export_csv(df):
    return df.to_csv(index=False).encode("utf-8")


# -----------------------------
# Excel Export
# -----------------------------
def export_excel(df):
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Results")

    return output.getvalue()


# -----------------------------
# PDF Export
# -----------------------------
def export_pdf(df, title="Query Report"):

    output = io.BytesIO()

    doc = SimpleDocTemplate(output)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph(title, styles["Heading1"]))
    elements.append(Paragraph("<br/>", styles["Normal"]))

    data = [df.columns.tolist()] + df.values.tolist()

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f77b4")),

        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 1, colors.grey),

        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

    ]))

    elements.append(table)

    doc.build(elements)

    return output.getvalue()