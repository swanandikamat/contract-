# Canonical Legal Clause Categories
CLAUSE_CATEGORIES = [
    "Limitation of Liability",
    "Indemnification",
    "Termination & Auto-Renewal",
    "Intellectual Property",
    "Force Majeure",
    "Specifications & Quality Remedies",
    "Governing Law & Dispute Resolution",
    "Payment & Currency Terms",
    "Non-Compete & Exclusivity",
    "Compliance & Data Protection",
    "Confidentiality",
    "General / Miscellaneous"
]

# Syngenta Benchmark 10 Core Defect Categories
BENCHMARK_DEFECTS = {
    "UNCAPPED_LIABILITY": "Uncapped or missing limitation of liability cap",
    "ONE_SIDED_INDEMNITY": "One-sided indemnification obligation without reciprocity",
    "AUTO_RENEWAL_TRAP": "Automatic renewal without reasonable opt-out notice",
    "WEAK_IP_OWNERSHIP": "Ambiguous or weak IP rights / ownership allocation",
    "MISSING_FORCE_MAJEURE": "Total absence of Force Majeure protective clause",
    "VAGUE_SPECS_NO_REMEDY": "Vague quality specifications or lack of warranty remedy",
    "UNFAVORABLE_JURISDICTION": "Inconvenient or foreign court jurisdiction / governing law",
    "ONE_SIDED_CURRENCY_PENALTY": "Unilateral currency risk or aggressive late penalty terms",
    "OVERBROAD_NON_COMPETE": "Overly broad non-compete or restraint of trade obligations",
    "MISSING_COMPLIANCE_DATA": "Missing statutory compliance or data protection clauses"
}

# Risk Level Classification Thresholds (0 to 100)
RISK_THRESHOLD_HIGH = 50.0   # Score >= 50 indicates PROBABLE ISSUES (HIGH RISK)
RISK_THRESHOLD_MEDIUM = 25.0 # Score 25-49 indicates MODERATE RISK
# Score < 25 indicates CLEAN (LOW RISK)
