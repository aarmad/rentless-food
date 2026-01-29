from collections import defaultdict
import re
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def parse_quantity(q_str):
    # Simple parser for numeric quantities
    match = re.match(r"(\d+(\.\d+)?)", q_str)
    if match:
        return float(match.group(1)), q_str[match.end():].strip()
    return 0, q_str

def generate_shopping_list_data(meal_plans):
    ingredients_map = defaultdict(list)
    
    for plan in meal_plans:
        for ing in plan.recipe.ingredients:
            ingredients_map[ing.name.lower()].append(ing.quantity)
    
    # Simple aggregation logic
    aggregated = []
    for name, quantities in ingredients_map.items():
        unique_quantities = list(set(quantities))
        aggregated.append({
            "name": name.capitalize(),
            "quantities": ", ".join(unique_quantities)
        })
    
    return sorted(aggregated, key=lambda x: x['name'])

def generate_shopping_list_pdf(shopping_list, start_date, end_date):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor("#4f772d"),
        spaceAfter=20
    )
    
    elements = []
    elements.append(Paragraph(f"Liste de Courses", title_style))
    elements.append(Paragraph(f"Semaine du {start_date} au {end_date}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Table data
    data = [["Ingrédient", "Quantité"]]
    for item in shopping_list:
        data.append([item["name"], item["quantities"]])
    
    t = Table(data, colWidths=[300, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4f772d")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(t)
    doc.build(elements)
    
    buffer.seek(0)
    return buffer
