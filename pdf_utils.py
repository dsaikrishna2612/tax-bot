from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import requests
from datetime import datetime
import os 

# Register a TrueType Unicode font that supports Telugu + ₹
# pdfmetrics.registerFont(TTFont('NotoSansTelugu', r'D:\income tax\tax\font\NotoSansTelugu-VariableFont_wdth,wght.ttf'))

# Construct relative path to font file
font_path = os.path.join("font", "NotoSansTelugu-VariableFont_wdth,wght.ttf")
# Register the font
pdfmetrics.registerFont(TTFont("NotoSansTelugu", font_path))


def round_nearest_10(amount):
    remainder = amount % 10
    if remainder == 0:
        return amount
    elif remainder <= 5:
        return amount - remainder
    else:
        return amount + (10 - remainder)

def generate_pdf(data, filename="tax_details.pdf"):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin_x = 50

    # --- Watermark image ---
    url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTI8HB7YVrDkVrkdC61hdS9K2nHcm0uasdxog&s"
    response = requests.get(url)
    img_data = BytesIO(response.content)
    img = ImageReader(img_data)
    img_width = 300
    img_height = 300

    # --- Utility: decorations (watermark, borders, footer) ---
    def add_page_decorations():
        # Watermark
        c.saveState()
        c.translate((width - img_width) / 2, (height - img_height) / 2)
        c.drawImage(img, 0, 0, width=img_width, height=img_height,
                    mask='auto', preserveAspectRatio=True, anchor='c')
        c.restoreState()

        # Borders (3 thin lines)
        for offset in range(3):
            margin = 10 + (offset * 2)
            c.setStrokeColor(colors.darkblue)
            c.setLineWidth(0.5)
            c.rect(margin, margin, width - 2 * margin, height - 2 * margin)

        # Footer (on every page)
        c.setFont("NotoSansTelugu", 9)
        c.setFillColor(colors.black)
        c.drawString(margin_x, 60, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        c.drawCentredString(width / 2, 50, "Developed by: CA Student Donakonda Sai Krishna")

    # --- Utility: draw text safely ---
    def draw_line(text, x, y, font="NotoSansTelugu", size=11, color=colors.black):
        c.setFont(font, size)
        c.setFillColor(color)
        c.drawString(x, y, text)

    def check_page(y):
        if y < 100:
            c.showPage()
            add_page_decorations()
            return height - 100
        return y

    # --- Title ---
    usable_width = width - 2 * margin_x
    c.setFont("NotoSansTelugu", 16)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(margin_x + usable_width / 2, 770, "Income Tax Calculation for Assessment Year 2026-2027")
    c.drawCentredString(margin_x + usable_width / 2, 750, "Previous Year 2025-2026")
    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(1)
    c.line(margin_x, 740, width - margin_x, 740)

    add_page_decorations()

    y = 720

    # --- Personal Details ---
    draw_line("Personal Details:", margin_x, y, size=12, color=colors.darkblue)
    y -= 20
    details = [
        f"Name: {data['name']}",
        f"Age: {data['age']} ({data['age_class']})",
        f"Gender: {data['gender']}",
        f"Place: {data['place']}",
        f"Email: {data['email']}",
        f"Taxpayer Type: {data['taxpayer_type']}"
    ]
    if data['taxpayer_type'] == "Individual":
        details.append(f"Employee Type: {data['employee_type']}")

    for d in details:
        y = check_page(y)
        draw_line(d, margin_x + 10, y)
        y -= 20

    # --- Income Details ---
    y -= 10
    draw_line("Income Details:", margin_x, y, size=12, color=colors.darkblue)
    y -= 20

    incomes = [
        f"Salary(as per form-16): ₹{data['salary']}",
        f"House Property: ₹{data['house_property']}",
        f"Other Sources: ₹{data['other_sources']}",
        f"Gross Total Income: ₹{data['gross_income']}"
    ]

    for inc in incomes:
        y = check_page(y)
        draw_line(inc, margin_x + 10, y)

        # Insert House Property Computation Table
        if "House Property" in inc:
            y -= 30
            draw_line("Income from House Property (Computation):", margin_x, y, size=12, color=colors.darkblue)
            y -= 20

            table_data = [
                ["Computation", "Self Occupied (Exempt max 2houses)", "Let Out Property"],
                ["Rent Received [Actual + Receivable - Unrealised]", "0", f"₹{data.get('rent_received_letout',0)}"],
                ["Gross Annual Value (GAV)", "0", f"₹{data.get('rent_received_letout',0)}"],
                ["Municipal Taxes", "0", f"₹{data.get('municipal_tax_letout',0)}"],
                ["Net Annual Value (NAV)", "0", f"₹{data.get('nav_letout',0)}"],
                ["(a) Standard Deduction 30% of NAV", "0", f"₹{data.get('std_deduction_letout',0)}"],
                ["(b) Interest on Loan (max 200000/30000 for SoP)", f"₹{data.get('sop_interest',0)}", f"₹{data.get('interest_deduction_letout',0)}"],
                ["Income from House Property", f"₹{-data.get('sop_interest',0)}", f"₹{data.get('income_letout',0)}"],
            ]

            table = Table(table_data, colWidths=[200, 150, 150])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
                ('TEXTCOLOR',(0,0),(-1,0),colors.black),
                ('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('FONTNAME', (0,0), (-1,-1), 'NotoSansTelugu'),  # ✅ apply Telugu font
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('FONTNAME', (0,-1), (-1,-1), 'NotoSansTelugu'), # bold totals row
                ('TEXTCOLOR', (0,-1), (-1,-1), colors.darkblue),
                ('BACKGROUND', (0,-1), (-1,-1), colors.whitesmoke),
            ]))
            table.wrapOn(c, width, height)
            y = check_page(y - 120)
            table.drawOn(c, margin_x, y)
            y -= 140

        y -= 20

    # --- Deductions ---
    y -= 10
    draw_line("Deductions:", margin_x, y, size=12, color=colors.darkblue)
    y -= 20
    for key, val in data['deductions'].items():
        y = check_page(y)
        draw_line(f"{key}: ₹{val}", margin_x + 10, y)
        y -= 18
    y = check_page(y)
    draw_line(f"Total Deductions (Max 150000): ₹{data['total_deductions']}", margin_x + 10, y)
    y -= 30

    # --- Tax Calculation ---
    draw_line("Tax Calculation:", margin_x, y, size=12, color=colors.darkblue)
    y -= 20
    tax_lines = [
        f"Taxable Income (as per Old Regime): ₹{data['net_income']}",
        f"Tax Payable (as per Old Regime): ₹{data['tax_old']}",
        f"Taxable Income (as per New Regime): ₹{data['gross_income']}",
        f"Tax Payable (as per New Regime): ₹{data['tax_new']}"
    ]
    for t in tax_lines:
        y = check_page(y)
        draw_line(t, margin_x + 10, y)
        y -= 20

    # --- Rounded tax + message ---
    tax_old_rounded = round_nearest_10(data['tax_old'])
    tax_new_rounded = round_nearest_10(data['tax_new'])

    if tax_old_rounded <= tax_new_rounded:
        lower_tax = tax_old_rounded
        regime = "Old Regime"
        savings = tax_new_rounded - tax_old_rounded
    else:
        lower_tax = tax_new_rounded
        regime = "New Regime"
        savings = tax_old_rounded - tax_new_rounded

    salutation = "Sir" if data.get("gender", "Male") == "Male" else "Madam"
    message = f"Dear {salutation} {data.get('name', '')} గారు, this is your Tax Payable amount ₹{lower_tax}. " \
              f"By paying tax under {regime}, you will save ₹{savings}."

    styles = getSampleStyleSheet()
    message_style = ParagraphStyle(
        "message",
        parent=styles["Normal"],
        fontName="NotoSansTelugu",
        fontSize=11,
        alignment=1,
        textColor=colors.darkred
    )
    para = Paragraph(message, message_style)
    para_width, para_height = para.wrap(usable_width, 100)
    y = check_page(y - para_height - 20)
    para.drawOn(c, margin_x, y)

    # Save PDF
    c.save()
    buffer.seek(0)
    return buffer
