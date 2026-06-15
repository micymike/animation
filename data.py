from enum import Enum


class TaxType(str, Enum):
    INCOME_TAX = "Income Tax Act"
    VAT = "VAT Act"
    EXCISE = "Excise Duty Act"
    TAX_PROCEDURES = "Tax Procedures Act"
    MISC = "Miscellaneous Fees & Levies"
    STAMP_DUTY = "Stamp Duty Act"


IMPACT = {
    "high": {"label": "High Impact", "color": "#ef4444"},
    "medium": {"label": "Medium Impact", "color": "#f59e0b"},
    "low": {"label": "Low Impact", "color": "#22c55e"},
}


EFFECTIVE_DATES = {
    "Jul 2026": "1 July 2026",
    "Jan 2027": "1 January 2027",
    "Immediate": "Upon Presidential Assent",
}


PROVISIONS = [
    {
        "id": "rental-income-tax",
        "tax_type": TaxType.INCOME_TAX,
        "title": "Residential Rental Income Tax Rate Increase",
        "summary": "Monthly residential rental income tax increased from 7.5% to 10% of gross rent.",
        "current_law": "Monthly rental income tax at 7.5% of gross rent, treated as final tax.",
        "proposed_law": "Rate increased to 10% of gross rent, still treated as final tax.",
        "impact": "high",
        "effective": "Jul 2026",
        "affected": "Landlords, property owners, real estate investors",
        "revenue_impact": "+KES ~8.5B annually",
        "details": "Landlords earning rental income will face a 2.5 percentage point increase. This will directly affect rental pricing, compliance behaviour, and tenant affordability. The tax remains final, meaning no further income tax is due on this income.",
    },
    {
        "id": "nonresident-rental",
        "tax_type": TaxType.INCOME_TAX,
        "title": "Non-Resident Rental Income Tax",
        "summary": "New 30% withholding tax on gross rental income of non-residents from Kenyan property.",
        "current_law": "No specific framework for non-resident rental income taxation.",
        "proposed_law": "30% final withholding tax on gross rental income accruing to non-resident persons from use/occupation of property in Kenya.",
        "impact": "high",
        "effective": "Jul 2026",
        "affected": "Non-resident landlords, foreign property investors, diaspora investors",
        "revenue_impact": "+KES ~3.2B annually",
        "details": "Non-resident persons must file returns by the 20th of the following month. The tax is final. This closes a significant loophole where non-residents earning rental income from Kenya were not effectively taxed.",
    },
    {
        "id": "filing-deadline",
        "tax_type": TaxType.INCOME_TAX,
        "title": "Income Tax Filing Deadline Reduced",
        "summary": "Filing deadline for income tax returns reduced from 6 months to 4 months after year-end.",
        "current_law": "Individual and company tax returns due within 6 months after year-end (30 June for calendar year).",
        "proposed_law": "Returns due within 4 months after year-end (30 April for calendar year taxpayers). Nil returns due within 1 month.",
        "impact": "medium",
        "effective": "Jan 2027",
        "affected": "All individual and corporate taxpayers",
        "revenue_impact": "Accelerated collection",
        "details": "Taxpayers have 2 fewer months to prepare returns. Nil returns must be filed within 1 month. This compresses compliance timelines significantly and will require better tax record-keeping throughout the year.",
    },
    {
        "id": "management-fee-definition",
        "tax_type": TaxType.INCOME_TAX,
        "title": "Expanded Definition of Management/Professional Fees",
        "summary": "Definition expanded to include interchange fees and merchant service fees from card transactions.",
        "current_law": "Interchange fees and merchant service fees not explicitly captured under management or professional fees.",
        "proposed_law": "Definition expanded to capture interchange fees, merchant service fees, and payment-processing charges.",
        "impact": "high",
        "effective": "Jul 2026",
        "affected": "Banks, payment processors, fintechs, merchants, card networks",
        "revenue_impact": "+KES ~5.1B annually",
        "details": "This is a direct response to Supreme Court rulings where KRA lost bids to tax interchange fees. The expanded definition brings these fees into the withholding tax net regardless of contractual description.",
    },
    {
        "id": "royalty-definition",
        "tax_type": TaxType.INCOME_TAX,
        "title": "Expanded Definition of Royalties",
        "summary": "Definition expanded to include payments for digital platforms, payment networks, and payment processing systems.",
        "current_law": "Royalty definition does not explicitly cover digital platform access and payment network fees.",
        "proposed_law": "Royalties now include payments for use of/access to digital platforms, payment networks, and processing systems, regardless of frequency or contractual description.",
        "impact": "high",
        "effective": "Jul 2026",
        "affected": "Tech companies, digital platforms, payment service providers, SaaS businesses",
        "revenue_impact": "+KES ~6.8B annually",
        "details": "Withholding tax applies to these payments. This targets digital economy taxation and closes the gap where payment platform fees were subject to prolonged tax disputes.",
    },
    {
        "id": "vat-digital-services",
        "tax_type": TaxType.VAT,
        "title": "VAT on Digital Financial Services",
        "summary": "Digital financial platform services brought into VAT net.",
        "current_law": "Digital financial platform services not explicitly subject to VAT.",
        "proposed_law": "Digital financial platform services, payment processing, and related digital services subject to VAT at 16%.",
        "impact": "high",
        "effective": "Jul 2026",
        "affected": "Fintechs, digital lenders, mobile money platforms, payment gateways, banks",
        "revenue_impact": "+KES ~12.3B annually",
        "details": "This significantly expands the VAT base to include the rapidly growing digital financial sector. Payment processors, fintechs, banks, and any business relying on digital collections will be affected. Pricing models and contracts may need restructuring.",
    },
    {
        "id": "vat-unsold-supplies",
        "tax_type": TaxType.VAT,
        "title": "VAT Recovery on Unsold Supplies with Rate Change",
        "summary": "Commissioner empowered to recover input VAT claimed on unsold supplies when VAT rate changes.",
        "current_law": "No specific provision for recovery of input VAT on unsold supplies at rate change.",
        "proposed_law": "Commissioner can assess and recover input VAT previously claimed on unsold supplies when VAT rates change.",
        "impact": "medium",
        "effective": "Jul 2026",
        "affected": "All VAT-registered businesses with inventory, manufacturers, retailers",
        "revenue_impact": "One-time recovery, variable",
        "details": "Businesses holding inventory when VAT rates change may face VAT adjustments. This affects how businesses account for inventory, pricing changes, and VAT claims when rates shift.",
    },
    {
        "id": "vat-passenger-exemption",
        "tax_type": TaxType.VAT,
        "title": "Higher VAT-Free Threshold for Returning Passengers",
        "summary": "Increased VAT exemption threshold for accompanied baggage of returning passengers.",
        "current_law": "Lower threshold for VAT exemption on personal effects and accompanied baggage.",
        "proposed_law": "Higher threshold value for VAT-free importation of accompanied baggage by returning passengers.",
        "impact": "low",
        "effective": "Jul 2026",
        "affected": "Returning residents, travellers, diaspora",
        "revenue_impact": "Minor revenue loss",
        "details": "A consumer-friendly measure allowing returning passengers to bring in more goods without VAT. Shows the Bill balances revenue measures with some relief.",
    },
    {
        "id": "excise-mobile",
        "tax_type": TaxType.EXCISE,
        "title": "Excise Duty on Mobile Phones — Timing Change",
        "summary": "Excise liability and payment timing for mobile phones reformed.",
        "current_law": "Current timing rules for excise duty on mobile phones.",
        "proposed_law": "New timing rules for when excise liability arises and must be paid on mobile phones.",
        "impact": "medium",
        "effective": "Jan 2027",
        "affected": "Mobile phone importers, manufacturers, telecom companies",
        "revenue_impact": "Compliance improvement",
        "details": "Reforms to when excise duty on mobile phones must be declared and paid. Aims to improve compliance and close avoidance loopholes.",
    },
    {
        "id": "tax-amnesty",
        "tax_type": TaxType.TAX_PROCEDURES,
        "title": "Tax Amnesty Extension",
        "summary": "Tax amnesty on interest, penalties, and fines extended to 31 Dec 2025, with principal tax payment by 31 Dec 2026.",
        "current_law": "Previous amnesty deadlines have expired.",
        "proposed_law": "Amnesty on interest, penalties, and fines extended — principal tax must be settled by 31 Dec 2026 for penalties to be waived.",
        "impact": "medium",
        "effective": "Immediate",
        "affected": "Taxpayers with outstanding tax liabilities, non-compliant businesses",
        "revenue_impact": "Encourages voluntary compliance and principal tax collection",
        "details": "Taxpayers can clear outstanding principal tax without the burden of accumulated penalties and interest. This is a significant window for compliance clean-up.",
    },
    {
        "id": "calendar-days",
        "tax_type": TaxType.TAX_PROCEDURES,
        "title": "Objection & Appeal Timelines Changed to Calendar Days",
        "summary": "Tax objection and appeal timelines shift from working days to calendar days.",
        "current_law": "Timelines for tax objections and appeals calculated in working days.",
        "proposed_law": "All timelines now calculated in calendar days.",
        "impact": "high",
        "effective": "Jul 2026",
        "affected": "All taxpayers engaged in tax disputes, tax practitioners, lawyers",
        "revenue_impact": "Reduces time for taxpayer response",
        "details": "Calendar-day deadlines are shorter in practical effect (a 30-working-day period is ~42 calendar days). This compresses the time available to prepare objections, file supporting documents, or seek review. Taxpayers need robust internal tax calendar controls.",
    },
    {
        "id": "self-assessment-regime",
        "tax_type": TaxType.TAX_PROCEDURES,
        "title": "Introduction of Self-Declaration Regime",
        "summary": "New self-declaration regime requiring taxpayers to register and account for certain taxes themselves.",
        "current_law": "No specific self-declaration framework for certain tax types.",
        "proposed_law": "Taxpayers required to self-declare and account for specified taxes without awaiting KRA assessment.",
        "impact": "medium",
        "effective": "Jul 2026",
        "affected": "Businesses, importers, specified tax types",
        "revenue_impact": "Enhanced compliance and earlier revenue recognition",
        "details": "Shifts compliance burden explicitly to taxpayers for certain taxes. Reduces KRA's assessment workload but increases taxpayer responsibility.",
    },
    {
        "id": "anti-avoidance",
        "tax_type": TaxType.TAX_PROCEDURES,
        "title": "Strengthened Anti-Avoidance Rules",
        "summary": "Commissioner empowered to disregard tax avoidance arrangements and issue assessments within 5 years.",
        "current_law": "General anti-avoidance rules exist but with limitations.",
        "proposed_law": "Commissioner can disregard any arrangement that results in tax avoidance, including postponement of tax. Assessments can be issued within 5 years.",
        "impact": "high",
        "effective": "Jul 2026",
        "affected": "All taxpayers, corporate structures, tax planners",
        "revenue_impact": "Expanded assessment window for KRA",
        "details": "Strengthened GAAR gives KRA broader powers to challenge tax avoidance arrangements. The 5-year assessment window for such arrangements significantly expands KRA's reach.",
    },
    {
        "id": "vat-definition-cleanup",
        "tax_type": TaxType.VAT,
        "title": "VAT Act Definition Clean-Up",
        "summary": "Removal of duplicate 'assessment' definition from VAT Act since it's already under TPA.",
        "current_law": "'Assessment' defined separately in both VAT Act and Tax Procedures Act.",
        "proposed_law": "Definition removed from VAT Act, relying solely on TPA definition.",
        "impact": "low",
        "effective": "Jul 2026",
        "affected": "Tax practitioners, lawyers, VAT-registered businesses",
        "revenue_impact": "None (administrative clarification)",
        "details": "A technical clean-up amendment eliminating duplication and ensuring uniform interpretation across tax laws.",
    },
    {
        "id": "antique-vehicle",
        "tax_type": TaxType.EXCISE,
        "title": "Definition of Antique, Vintage or Classic Vehicle",
        "summary": "New definition for customs/excise classification: vehicles 30+ years old, value of at least KES 10M.",
        "current_law": "No clear statutory definition for antique/vintage/classic vehicles.",
        "proposed_law": "Defined as motor vehicle at least 30 years from first registration with value of at least KES 10 million (excl. depreciation).",
        "impact": "low",
        "effective": "Jul 2026",
        "affected": "Car collectors, importers of classic vehicles, luxury goods dealers",
        "revenue_impact": "Clarifies revenue classification",
        "details": "Creates clear classification for high-value collector vehicles, enabling appropriate tax treatment.",
    },
    {
        "id": "property-definition",
        "tax_type": TaxType.INCOME_TAX,
        "title": "Immovable Property Definition Clarified",
        "summary": "Definition of immovable property amended: 'and' replaced with 'or' to cover land OR mining/petroleum rights.",
        "current_law": "Definition of immovable property includes both land AND mining/petroleum rights (conjunctive).",
        "proposed_law": "Immovable property means land OR mining and petroleum rights (disjunctive).",
        "impact": "low",
        "effective": "Jul 2026",
        "affected": "Mining and petroleum companies, property lawyers",
        "revenue_impact": "Clarifies tax treatment of mineral rights",
        "details": "A clean-up amendment removing ambiguity. Mining and petroleum rights are now clearly separate categories of immovable property for tax purposes.",
    },
    {
        "id": "national-infrastructure-fund",
        "tax_type": TaxType.MISC,
        "title": "National Infrastructure Fund & Sovereign Wealth Fund",
        "summary": "Establishment of funds to mobilize domestic resources, monetize public assets, and attract private capital.",
        "current_law": "No specific statutory framework for these funds.",
        "proposed_law": "Government authorized to establish National Infrastructure Fund and Sovereign Wealth Fund.",
        "impact": "high",
        "effective": "Immediate",
        "affected": "Public finance, infrastructure developers, investors, PPPs",
        "revenue_impact": "Enables alternative financing for infrastructure",
        "details": "These funds are designed to mobilize domestic resources, monetize public assets, and attract private capital. Represents a fundamental shift in how Kenya finances infrastructure development.",
    },
]


SUMMARY_METRICS = {
    "total_provisions": len(PROVISIONS),
    "high_impact": sum(1 for p in PROVISIONS if p["impact"] == "high"),
    "medium_impact": sum(1 for p in PROVISIONS if p["impact"] == "medium"),
    "low_impact": sum(1 for p in PROVISIONS if p["impact"] == "low"),
    "tax_types_affected": len(set(p["tax_type"].value for p in PROVISIONS)),
    "effective_jul2026": sum(1 for p in PROVISIONS if p["effective"] == "Jul 2026"),
    "effective_jan2027": sum(1 for p in PROVISIONS if p["effective"] == "Jan 2027"),
    "est_revenue_impact": "+KES ~42B+",
}


def search_provisions(query: str):
    q = query.lower()
    return [
        p for p in PROVISIONS
        if q in p["title"].lower()
        or q in p["summary"].lower()
        or q in p["tax_type"].value.lower()
        or q in p["affected"].lower()
        or q in p["details"].lower()
    ]


def get_by_tax_type(tax_type: TaxType):
    return [p for p in PROVISIONS if p["tax_type"] == tax_type]


def get_by_impact(level: str):
    return [p for p in PROVISIONS if p["impact"] == level]


def get_timeline():
    return sorted(set(p["effective"] for p in PROVISIONS),
                  key=lambda x: {"Immediate": 0, "Jul 2026": 1, "Jan 2027": 2}[x])


def get_revenue_highlights():
    high_rev = [p for p in PROVISIONS if p["impact"] == "high"]
    return high_rev
