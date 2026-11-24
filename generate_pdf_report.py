import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#666666"))
        
        # Header (pages after page 1)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "HCL Tech Data Analyst Training Program — Advanced Statistics Project Report")
            self.setStrokeColor(colors.HexColor("#CCCCCC"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
        
        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 36, footer_text)
        self.drawString(54, 36, "Author: Unzila Ansari | Project: Testing Business Claims with Evidence, Not Opinion")
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.5)
        self.line(54, 46, letter[0] - 54, 46)
        
        self.restoreState()

def build_pdf():
    pdf_filename = "Statistical_Findings_Report_Advanced_Statistics.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_navy = colors.HexColor("#1B365D")
    c_steel = colors.HexColor("#336699")
    c_dark = colors.HexColor("#222222")
    c_muted = colors.HexColor("#555555")
    c_callout_bg = colors.HexColor("#EBF3FA")
    c_header_bg = colors.HexColor("#1B365D")
    c_row_alt = colors.HexColor("#F4F6F9")

    # Typography Styles
    style_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_navy,
        spaceAfter=4
    )
    style_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=11.5,
        leading=15,
        textColor=c_steel,
        spaceAfter=12
    )
    style_h1 = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_navy,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    style_h2 = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_steel,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    style_body = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=c_dark,
        spaceAfter=5
    )
    style_caption = ParagraphStyle(
        'CaptionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=10,
        textColor=c_muted,
        alignment=1, # Center
        spaceBefore=2,
        spaceAfter=6
    )
    style_callout_title = ParagraphStyle(
        'CalloutTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=c_navy
    )
    style_callout_body = ParagraphStyle(
        'CalloutBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_dark
    )
    style_table_header = ParagraphStyle(
        'TblHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        alignment=1
    )
    style_table_cell = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=c_dark
    )
    style_table_cell_bold = ParagraphStyle(
        'TblCellB',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=c_navy
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("STATISTICAL FINDINGS REPORT", style_title))
    story.append(Paragraph("Testing Business Claims with Empirical Evidence, Not Opinion", style_subtitle))

    meta_table_data = [
        [
            Paragraph("<b>Candidate Name:</b> Unzila Ansari", style_table_cell),
            Paragraph("<b>Program:</b> HCL Shaper Career — 2nd Year Engineering", style_table_cell)
        ],
        [
            Paragraph("<b>Role:</b> Data Analyst Intern", style_table_cell),
            Paragraph("<b>Dataset:</b> retail_customer_sales_dataset.csv (7,000 Trans.)", style_table_cell)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[240, 264])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8F9FA")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#D0D7DE")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E1E4E8")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # Helper: Callout Box in PDF
    def make_callout(title, body_text):
        content = [
            Paragraph(f"<b>EXECUTIVE TAKEAWAY: {title}</b>", style_callout_title),
            Spacer(1, 2),
            Paragraph(body_text, style_callout_body)
        ]
        tbl = Table([[content]], colWidths=[504])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_callout_bg),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#D0E2FF")),
            ('LINELEFT', (0,0), (0,0), 3.5, c_navy),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        return tbl

    # Section 1
    story.append(Paragraph("1. Executive Problem Statement & Context", style_h1))
    story.append(Paragraph(
        "In retail management, critical commercial strategies are frequently dictated by gut feelings and executive assumptions: "
        "(1) <i>'The West region sells significantly better than other regions'</i>; "
        "(2) <i>'Aggressive promotional discounts are destroying our profit margins'</i>; "
        "(3) <i>'Corporate clients buy fundamentally different product categories than individual consumers'</i>. "
        "Until now, none of these business claims had been formally tested against statistical criteria. "
        "This empirical report investigates each assertion using the retail dataset of 7,000 transactions, delivering rigorous "
        "test statistics, p-values, regression parameters, and practical recommendations for leadership.",
        style_body
    ))

    # Section 2
    story.append(Paragraph("2. Data Integrity Audit & Preprocessing Methodology", style_h1))
    story.append(Paragraph(
        "The raw dataset ('retail_customer_sales_dataset.csv') comprised 7,084 records across 24 columns. "
        "Following the project brief, realistic data corruption issues were systematically addressed: "
        "<b>(1) Deduplication:</b> Identified and eliminated 84 duplicate transactions (168 duplicate transaction ID rows), leaving 7,000 unique orders. "
        "<b>(2) Categorical Standardization:</b> Standardized region spellings ('Sth' -> 'South', 'Nort'/'north'/'NORTH' -> 'North', 'west'/'WEST' -> 'West') "
        "and gender encodings ('M'/'MALE' -> 'Male', 'F'/'FEMALE' -> 'Female'). "
        "<b>(3) Outlier & Impossible Value Filtering:</b> Replaced impossible customer ages (<18 or >100 years, e.g., -12 and 999) "
        "and invalid discount proportions (<0.0 or >0.50, e.g., -0.2 and 2.0) with NaN to preserve inferential validity. "
        "<b>(4) Date Parsing:</b> Formatted order and delivery dates, identifying 53 fulfillment timestamp inconsistencies.",
        style_body
    ))

    # Section 3
    story.append(Paragraph("3. Descriptive Statistics & Metric Distribution Analysis", style_h1))
    story.append(Paragraph(
        "Summary statistics were calculated for Sales, Profit, Age, and Income to evaluate central tendency, dispersion, and skewness.",
        style_body
    ))

    # Descriptive Table
    desc_headers = ["Variable", "Count", "Mean", "Median", "Mode", "Std Dev", "Variance", "Q1 (25%)", "Q3 (75%)", "IQR"]
    desc_rows = [
        ["Sales (Rs.)", "7,000", "10,961.60", "4,825.56", "258.73", "14,549.03", "2.12e+08", "1,815.46", "14,095.35", "12,279.89"],
        ["Profit (Rs.)", "7,000", "3,589.70", "1,528.70", "19.47", "4,928.02", "2.43e+07", "574.08", "4,533.29", "3,959.20"],
        ["Age (Years)", "6,854", "36.06", "36.00", "18.00", "10.42", "108.54", "29.00", "43.00", "14.00"],
        ["Income (Rs.)", "6,755", "55,101.38", "49,005.17", "15,000.00", "37,338.42", "1.39e+09", "37,125.40", "65,721.73", "28,596.33"]
    ]
    t_data = [[Paragraph(h, style_table_header) for h in desc_headers]]
    for r in desc_rows:
        t_data.append([
            Paragraph(r[0], style_table_cell_bold),
            Paragraph(r[1], style_table_cell),
            Paragraph(r[2], style_table_cell),
            Paragraph(r[3], style_table_cell),
            Paragraph(r[4], style_table_cell),
            Paragraph(r[5], style_table_cell),
            Paragraph(r[6], style_table_cell),
            Paragraph(r[7], style_table_cell),
            Paragraph(r[8], style_table_cell),
            Paragraph(r[9], style_table_cell)
        ])
    t_desc = Table(t_data, colWidths=[65, 38, 48, 48, 42, 50, 48, 52, 55, 58])
    t_desc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D0D7DE")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_row_alt]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_desc)
    story.append(Spacer(1, 6))

    if os.path.exists('images/descriptive_distributions.png'):
        story.append(Image('images/descriptive_distributions.png', width=480, height=260))
        story.append(Paragraph("Figure 1: Probability distributions for Sales, Profit, Age, and Income with Mean (red) and Median (green).", style_caption))

    story.append(make_callout(
        "Heavy Positive Skew in Financial Metrics Mandates Use of Median",
        "Sales and Profit exhibit extreme right-skewness (+2.45 and +2.48). Mean Sales (Rs. 10,961.60) is over twice "
        "the median (Rs. 4,825.56) due to large-ticket electronics orders (up to Rs. 122,951). Store quotas and baseline KPI "
        "tracking must rely on the Median to avoid inflated performance expectations, while the Mean remains suitable for total cash budgeting."
    ))
    story.append(Spacer(1, 8))

    # Section 4
    story.append(Paragraph("4. Inferential Estimation: 95% Confidence Interval Analysis", style_h1))
    story.append(Paragraph(
        "Two-sided 95% Confidence Intervals were constructed using Student's t-distribution: CI = x̄ ± t_(α/2, n-1) * (s / √n).",
        style_body
    ))

    ci_headers = ["Metric", "Sample (n)", "Mean (x̄)", "Std Dev (s)", "Margin of Error (MOE)", "95% Confidence Interval"]
    ci_rows = [
        ["Transaction Sales (Rs.)", "7,000", "Rs. 10,961.60", "Rs. 14,549.03", "± Rs. 340.89", "[Rs. 10,620.71, Rs. 11,302.48]"],
        ["Customer Rating (1-5)", "6,580", "3.0924", "1.0006", "± 0.0244", "[3.0680, 3.1168]"]
    ]
    ci_data = [[Paragraph(h, style_table_header) for h in ci_headers]]
    for r in ci_rows:
        ci_data.append([
            Paragraph(r[0], style_table_cell_bold),
            Paragraph(r[1], style_table_cell),
            Paragraph(r[2], style_table_cell),
            Paragraph(r[3], style_table_cell),
            Paragraph(r[4], style_table_cell),
            Paragraph(r[5], style_table_cell)
        ])
    t_ci = Table(ci_data, colWidths=[120, 60, 80, 80, 80, 84])
    t_ci.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D0D7DE")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_row_alt]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_ci)
    story.append(Spacer(1, 5))
    story.append(Paragraph(
        "<b>Plain-Language Interpretation:</b> We are 95% confident that the true population average transaction revenue across India "
        "lies between Rs. 10,620.71 and Rs. 11,302.48. If sampling were repeated 100 times, 95 intervals would contain the true population mean. "
        "The narrow margin of error (±Rs. 340.89, or 3.1% of the mean) provides strong fiscal predictability for inventory and working capital.",
        style_body
    ))
    story.append(Spacer(1, 8))

    # Section 5: Hypothesis Tests
    story.append(Paragraph("5. Formal Hypothesis Testing (Section 3.3 & 3.6)", style_h1))

    # Test 1
    story.append(Paragraph("Test 1: Regional Sales Comparison — North vs. South (Two-Sample t-Test)", style_h2))
    story.append(Paragraph(
        "• <b>Business Question:</b> Is average transaction sales significantly different between customers in North and South regions?<br/>"
        "• <b>Null Hypothesis (H₀):</b> μ_North = μ_South (Mean sales are equal between North and South).<br/>"
        "• <b>Alternative Hypothesis (H₁):</b> μ_North ≠ μ_South (Mean sales between North and South differ significantly).<br/>"
        "• <b>Test Used & Why:</b> Two-Sample Independent Welch's t-test (unequal variance assumed across continuous independent groups).<br/>"
        "• <b>Test Statistics:</b> t = 0.1052, df ≈ 3,432.8 (North n = 1,676, Mean = Rs. 10,777.98; South n = 1,761, Mean = Rs. 10,726.92).<br/>"
        "• <b>Exact p-Value:</b> p = 0.9162<br/>"
        "• <b>Decision at α = 0.05:</b> Fail to Reject H₀ (p = 0.9162 > 0.05).",
        style_body
    ))
    story.append(make_callout(
        "North and South Regional Sales are Statistically Identical",
        "The difference between North and South mean sales is only Rs. 51.06 (p = 0.916), representing random sampling variation. "
        "Regional leadership should not allocate differential sales quotas or advertising spend under the belief that southern or northern shoppers spend differently."
    ))
    story.append(Spacer(1, 6))

    # Test 2
    story.append(Paragraph("Test 2: Multi-Region Sales Comparison — All 4 Regions (One-Way ANOVA)", style_h2))
    story.append(Paragraph(
        "• <b>Business Question:</b> Is average Sales significantly different across all four regions (North, South, East, West) simultaneously?<br/>"
        "• <b>Null Hypothesis (H₀):</b> μ_North = μ_South = μ_East = μ_West (Mean transaction sales are identical across all four regions).<br/>"
        "• <b>Alternative Hypothesis (H₁):</b> At least one region has a significantly different mean transaction sales value.<br/>"
        "• <b>Test Used & Why:</b> One-Way Analysis of Variance (ANOVA). Omnibus test comparing between-group variance to within-group variance.<br/>"
        "• <b>Test Statistics:</b> F = 0.6455, df_between = 3, df_within = 6,996 (East = Rs. 11,341.75; West = Rs. 10,989.43; North = Rs. 10,777.98; South = Rs. 10,726.92).<br/>"
        "• <b>Exact p-Value:</b> p = 0.5857<br/>"
        "• <b>Decision at α = 0.05:</b> Fail to Reject H₀ (p = 0.5857 > 0.05).<br/>"
        "• <b>Post-Hoc Discussion:</b> Post-hoc tests are not formally required since omnibus ANOVA is non-significant. Tukey's HSD confirms that all pairwise adjusted p-values exceed 0.59 (East-West p = 0.888, North-West p = 0.974, North-South p = 0.9996).",
        style_body
    ))

    if os.path.exists('images/regional_sales_anova.png'):
        story.append(Image('images/regional_sales_anova.png', width=480, height=190))
        story.append(Paragraph("Figure 2: Boxplots and 95% Confidence Interval error bars across the four geographic regions.", style_caption))

    story.append(make_callout(
        "Executive Claim 'West Region Sells Better' is Completely Refuted",
        "The prevailing stakeholder belief that 'the West region sells better' is refuted by empirical evidence. Average transaction values "
        "are uniform across India (East: Rs. 11,342; West: Rs. 10,989; North: Rs. 10,778; South: Rs. 10,727; p = 0.586). Regional reorganization "
        "or preferential sales targets for the West are unjustified."
    ))
    story.append(Spacer(1, 6))

    # Test 3
    story.append(Paragraph("Test 3: Customer Segment vs. Product Category (Chi-Square Independence Test)", style_h2))
    story.append(Paragraph(
        "• <b>Business Question:</b> Is Customer_Segment (Consumer, Corporate, Home Office) associated with Product_Category, or are they independent?<br/>"
        "• <b>Null Hypothesis (H₀):</b> Customer Segment and Product Category are independent.<br/>"
        "• <b>Alternative Hypothesis (H₁):</b> Customer Segment and Product Category are dependent.<br/>"
        "• <b>Test Used & Why:</b> Pearson's Chi-Square Test of Independence (χ²) on cross-tabulated contingency frequencies.<br/>"
        "• <b>Test Statistics:</b> χ² = 3.4534, df = (3 - 1) × (5 - 1) = 8.<br/>"
        "• <b>Exact p-Value:</b> p = 0.9028<br/>"
        "• <b>Decision at α = 0.05:</b> Fail to Reject H₀ (p = 0.9028 > 0.05).",
        style_body
    ))

    if os.path.exists('images/chisquare_segment_category.png'):
        story.append(Image('images/chisquare_segment_category.png', width=460, height=200))
        story.append(Paragraph("Figure 3: Product Category order proportion breakdown by Customer Segment.", style_caption))

    story.append(make_callout(
        "Claim 'Corporate Clients Buy Different Products' is Debunked",
        "Empirical testing refutes the claim that corporate customers buy different product lines than individual consumers. "
        "Across all segments, the product mix is practically identical (~31% Electronics, ~24% Grocery, ~22% Clothing, ~15% Furniture, ~8% Office Supplies). "
        "Marketing should unify product promotions rather than building siloed catalogs for corporate vs. consumer buyers."
    ))
    story.append(Spacer(1, 6))

    # Test 4
    story.append(Paragraph("Test 4: Discount Concessions vs. Profitability (Correlation Analysis)", style_h2))
    story.append(Paragraph(
        "• <b>Business Question:</b> Is Discount correlated with Profit, and does discounting hurt business profit margins?<br/>"
        "• <b>Null Hypothesis (H₀):</b> ρ = 0 (Zero correlation between Discount and Profit).<br/>"
        "• <b>Alternative Hypothesis (H₁):</b> ρ ≠ 0 (Statistically significant correlation between Discount and Profit).<br/>"
        "• <b>Test Used & Why:</b> Pearson Product-Moment Correlation (r) and Spearman Rank Correlation (ρ).<br/>"
        "• <b>Test Statistics:</b> Pearson r = -0.1201, Spearman ρ = -0.1168 (n = 6,930 clean paired observations).<br/>"
        "• <b>Exact p-Value:</b> p = 1.0997 × 10⁻²³ (p < 0.0001)<br/>"
        "• <b>Decision at α = 0.05:</b> Reject H₀ (p < 0.0001).<br/>"
        "• <b>Sign, Strength & Causation Caution:</b> Sign is negative (-); strength is weak (r = -0.1201), explaining r² = 1.44% of profit variance. "
        "<i>Correlation does not prove causation</i>; profit is also driven by unit cost and category margins. However, discounts directly compress margin per unit.",
        style_body
    ))

    if os.path.exists('images/correlation_discount_profit.png'):
        story.append(Image('images/correlation_discount_profit.png', width=450, height=210))
        story.append(Paragraph("Figure 4: Scatter plot and regression trendline of Discount Rate vs. Net Profit.", style_caption))

    story.append(make_callout(
        "Discounts Statistically Erode Profitability — Enforce a 20% Cap",
        "Leadership's concern that 'discounts hurt margins' is statistically confirmed (p < 0.0001). However, because correlation strength is weak (r = -0.12), "
        "discounting is not entirely fatal; rather, discounts above 25% erode profit without driving basket expansion. Management should establish a 20% discount ceiling."
    ))
    story.append(Spacer(1, 8))

    # Section 6: Regression
    story.append(Paragraph("6. Econometric Regression Modeling (Section 3.4)", style_h1))
    story.append(Paragraph(
        "<b>6.1 Simple Linear Regression (Sales ~ Quantity):</b><br/>"
        "• Equation: Saleŝ = -609.30 + 3,844.52 * Quantity<br/>"
        "• Intercept (β₀ = -609.30, p = 0.109): Not significant. Zero quantity transactions do not occur in retail.<br/>"
        "• Slope (β₁ = +3,844.52, t = 33.60, p < 0.0001): Highly significant. Each additional unit purchased increases sales by Rs. 3,844.52.<br/>"
        "• Fit (R² = 0.139): Quantity explains 13.9% of transaction revenue variance; 86.1% depends on item price mix.<br/><br/>"
        "<b>6.2 Multiple Linear Regression (Sales ~ Quantity + Discount + Income):</b><br/>"
        "• Equation: Saleŝ = 2,133.02 + 3,901.22 * Quantity - 15,632.74 * Discount + 0.0047 * Income<br/>"
        "• Fit: R² = 0.159, Adj. R² = 0.158, F(3, 6677) = 419.2, p < 0.0001 (n = 6,681 complete cases).<br/>"
        "• <i>Quantity (β₁ = +3,901.22, p < 0.0001) — Significant:</i> Each unit adds Rs. 3,901.22 holding discount and income constant.<br/>"
        "• <i>Discount (β₂ = -15,632.74, p < 0.0001) — Significant:</i> Higher discounts compress gross sales; a 10% discount increase reduces revenue by Rs. 1,563.27.<br/>"
        "• <i>Income (β₃ = +0.0047, p = 0.280) — Not Significant:</i> Customer income does not meaningfully predict order value (p > 0.05).",
        style_body
    ))

    if os.path.exists('images/regression_analysis.png'):
        story.append(Image('images/regression_analysis.png', width=480, height=190))
        story.append(Paragraph("Figure 5: Simple Linear Regression fit (left) and Multiple Linear Regression Actual vs. Predicted values (right).", style_caption))

    story.append(Spacer(1, 8))

    # Section 7: Bonus Z-Test
    story.append(Paragraph("7. Optional Bonus Analysis: One-Sample Z-Test on Customer Ratings (Section 3.5)", style_h1))
    story.append(Paragraph(
        "• <b>Business Question:</b> Does the sample average rating differ significantly from known historical benchmarks?<br/>"
        "• <b>Assumptions:</b> Known historical baseline μ₀ = 3.0 (neutral), corporate target μ₀ = 3.5; known population std dev σ = 1.0; n = 6,580.<br/>"
        "• <b>Test A (vs. Neutral μ₀ = 3.0):</b> Sample Mean x̄ = 3.0924, Z = +7.4953, p = 6.62 × 10⁻¹⁴ (p < 0.0001). Reject H₀. Rating exceeds neutral.<br/>"
        "• <b>Test B (vs. Target μ₀ = 3.5):</b> Sample Mean x̄ = 3.0924, Z = -33.0633, p < 0.0001. Reject H₀. Rating drastically lags corporate target.",
        style_body
    ))

    if os.path.exists('images/rating_confidence_interval.png'):
        story.append(Image('images/rating_confidence_interval.png', width=450, height=200))
        story.append(Paragraph("Figure 6: Customer rating distribution with 95% CI and historical Z-test benchmark lines.", style_caption))

    story.append(make_callout(
        "Customer Satisfaction is Above Neutrality, But Below Executive Target",
        "While customer sentiment is nominally positive (x̄ = 3.09 vs. neutral 3.0, Z = +7.50, p < 0.001), it is significantly below "
        "the corporate benchmark of 3.5 (Z = -33.06, p < 0.001). Resolving fulfillment delays and delivery tracking must be prioritized."
    ))
    story.append(Spacer(1, 8))

    # Section 8: Master Matrix & Recommendations
    story.append(Paragraph("8. Master Hypothesis Testing Matrix & Strategic Action Plan", style_h1))

    sum_headers = ["Claim / Test", "Statistical Test", "Test Stat", "p-Value", "Decision", "Verdict"]
    sum_rows = [
        ["1. North vs. South Sales", "Two-Sample t-Test", "t = 0.1052", "0.9162", "Fail to Reject H₀", "Refuted: Sales are identical."],
        ["2. West Sells Better", "One-Way ANOVA", "F = 0.6455", "0.5857", "Fail to Reject H₀", "Refuted: Regional sales uniform."],
        ["3. Segment vs. Category", "Chi-Square (χ²)", "χ² = 3.4534", "0.9028", "Fail to Reject H₀", "Refuted: Mix independent of segment."],
        ["4. Discounts Hurt Margins", "Pearson Correlation", "r = -0.1201", "1.10e-23", "Reject H₀", "Supported: Discounts reduce margin."],
        ["5. Rating vs Target 3.5", "One-Sample Z-Test", "Z = -33.06", "< 0.0001", "Reject H₀", "Deficit: Rating lags 3.5 target."],
        ["6. SLR: Sales ~ Quantity", "Simple OLS", "t = 33.60", "< 0.0001", "Significant", "Confirmed: +Rs. 3,844.52 / unit."],
        ["7. MLR: Qty + Disc + Inc", "Multiple OLS", "F = 419.2", "< 0.0001", "Significant", "Confirmed: Qty (+), Disc (-), Inc (NS)."]
    ]
    sum_data = [[Paragraph(h, style_table_header) for h in sum_headers]]
    for r in sum_rows:
        sum_data.append([
            Paragraph(r[0], style_table_cell_bold),
            Paragraph(r[1], style_table_cell),
            Paragraph(r[2], style_table_cell),
            Paragraph(r[3], style_table_cell),
            Paragraph(r[4], style_table_cell),
            Paragraph(r[5], style_table_cell)
        ])
    t_sum = Table(sum_data, colWidths=[110, 85, 65, 55, 85, 104])
    t_sum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D0D7DE")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_row_alt]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sum)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Strategic Action Plan for Executive Leadership", style_h2))
    story.append(Paragraph(
        "1. <b>Eliminate Regional Bias:</b> Discontinue higher revenue expectations for the West region. Empirical evidence proves mean sales are uniform across India (F = 0.646, p = 0.586). Allocate inventory based on logistical fulfillment capacity.<br/>"
        "2. <b>Unify Marketing Across Segments:</b> Stop maintaining distinct product catalogs for Corporate versus Consumer buyers. Category buying proportions are identical (χ² = 3.45, p = 0.903).<br/>"
        "3. <b>Enforce a 20% Discount Ceiling:</b> Given the statistically significant negative correlation with profit (r = -0.12, p < 0.0001) and MLR coefficient (-Rs. 15,632.74), unmonitored discounting directly harms net profitability.<br/>"
        "4. <b>Incentivize Multi-Item Basket Size:</b> Order quantity is the single largest significant revenue driver (+Rs. 3,901.22 per unit). Merchandising should emphasize bundling ('Buy 2, Get 1 at 15% Off') rather than single-item price markdowns.",
        style_body
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"SUCCESS: Report saved as '{pdf_filename}'! Size: {os.path.getsize(pdf_filename):,} bytes.")

if __name__ == '__main__':
    build_pdf()
