from app import create_app
from app.models import db
from app.models.user import User
from app.models.service import Service
from app.models.article import Article

app = create_app()


SERVICES_DATA = [
    {
        "title": "Accounting & Bookkeeping",
        "slug": "accounting-bookkeeping",
        "order": 1,
        "icon": "book-open",
        "short_description": "Comprehensive accounting, balance sheet management, financial statement preparation, and statutory audit readiness for businesses.",
        "description": "MVR Associates provides systematic accounting and bookkeeping advisory tailored for sole proprietorships, partnerships, LLPs, and corporate entities. Backed by formal Master of Commerce (M.Com) and Cost Management Accounting (CMA) credentials, our team ensures your financial records remain accurate, compliant, and insightful for strategic decision-making.",
        "problems_addressed": [
            "Disorganized financial records & unaligned ledgers",
            "Inaccurate profit & loss tracking causing tax overpayment",
            "Delays in statutory audit readiness & financial closing",
            "Lack of clear cash flow visibility for management decisions"
        ],
        "services_included": [
            "Daily & monthly ledger posting & reconciliation",
            "Preparation of Balance Sheet & Profit and Loss Statements",
            "Cash flow analysis & working capital statement drafting",
            "Inventory & asset accounting management",
            "Audit readiness file preparation & liaison with statutory auditors"
        ],
        "benefits": [
            "Complete statutory compliance with Indian accounting standards",
            "Timely financial reports for bank credit lines & investor reviews",
            "Elimination of double entries and ledger discrepancies",
            "Dedicated CMA oversight on cost structure optimization"
        ],
        "process_steps": [
            {"step": "01", "title": "Data Collection", "desc": "Collection of invoices, bank statements, and vouchers."},
            {"step": "02", "title": "Classification", "desc": "Categorization of income, expenses, assets, and liabilities."},
            {"step": "03", "title": "Reconciliation", "desc": "Reconciling bank accounts and vendor ledgers."},
            {"step": "04", "title": "Reporting", "desc": "Generating monthly P&L, balance sheet, and MIS reports."}
        ],
        "faqs": [
            {"question": "How frequently are financial statements updated?", "answer": "We provide monthly, quarterly, and annual financial reporting based on your operational scale and preference."},
            {"question": "Can you assist during statutory audits?", "answer": "Yes, we prepare comprehensive audit schedules and liaise directly with external auditors to ensure smooth audit completion."}
        ]
    },
    {
        "title": "GST & Tax Services",
        "slug": "gst-taxation",
        "order": 2,
        "icon": "shield-check",
        "short_description": "End-to-end GST return filing, income tax planning, statutory tax audits, and representation before tax assessment authorities.",
        "description": "Navigating complex Indian direct and indirect tax compliance requires rigorous expertise. MVR Associates delivers meticulous GST registration, GSTR-1, GSTR-3B, and annual return filings, as well as direct income tax optimization for businesses and individuals while strictly maintaining full statutory compliance.",
        "problems_addressed": [
            "Penalties due to delayed GST or Income Tax filings",
            "Input Tax Credit (ITC) mismatches between GSTR-2B and GSTR-3B",
            "Uncertainty around GST tax rates and HSN/SAC code classification",
            "Notices or audit queries received from Tax Departments"
        ],
        "services_included": [
            "GST Registration & Composition scheme advisory",
            "Monthly/Quarterly GSTR-1, GSTR-3B & GSTR-9 filings",
            "Input Tax Credit (ITC) reconciliation & vendor tracking",
            "Income Tax return (ITR) preparation for corporate & non-corporate entities",
            "Representation & reply drafting for tax assessment notices"
        ],
        "benefits": [
            "100% adherence to statutory filing deadlines avoiding late fees",
            "Maximized legitimate Input Tax Credit reconciliation",
            "Reduced risk of tax department notices and scrutiny",
            "Strategic tax planning to optimize net cash flow"
        ],
        "process_steps": [
            {"step": "01", "title": "Document Fetch", "desc": "Gather sales registers, purchase bills, and ITC records."},
            {"step": "02", "title": "Reconciliation", "desc": "Cross-match GSTR-2A/2B with internal purchase ledgers."},
            {"step": "03", "title": "Computation", "desc": "Calculate net tax liability or eligible refund amount."},
            {"step": "04", "title": "Filing", "desc": "Upload GST/ITR returns on official government portals."}
        ],
        "faqs": [
            {"question": "What happens if there is an ITC mismatch in GSTR-2B?", "answer": "We perform vendor-level reconciliation to identify delinquent suppliers and rectify claims prior to filing."},
            {"question": "Do you handle tax department notice replies?", "answer": "Yes, our team drafts legally sound responses backed by tax provisions and relevant case laws."}
        ]
    },
    {
        "title": "Business Consultancy",
        "slug": "business-consultancy",
        "order": 3,
        "icon": "trending-up",
        "short_description": "Strategic business advisory, entity structuring, cost control frameworks, margin analysis, and corporate growth planning.",
        "description": "MVR Associates advises business leaders on structural planning, operational cost efficiency, and legal framework selection. Whether you are launching a private limited company, partnership, or LLP, our advisory combines financial analysis (CMA) with legal compliance (LL.B) to build sustainable corporate structures.",
        "problems_addressed": [
            "Choosing the wrong business entity structure causing higher liability",
            "Uncontrolled overhead costs eroding profit margins",
            "Lack of long-term business roadmap and strategic governance",
            "Operational bottlenecks during company expansion"
        ],
        "services_included": [
            "Business entity selection advisory (Proprietorship, Partnership, LLP, Pvt Ltd)",
            "Cost center analysis & overhead reduction strategies",
            "Feasibility studies & break-even analysis for new ventures",
            "Standard Operating Procedure (SOP) design for financial workflows",
            "Corporate governance & restructuring support"
        ],
        "benefits": [
            "Optimized corporate structure aligned with growth plans",
            "Actionable insights into cost savings and operational efficiency",
            "Risk mitigation across legal, regulatory, and financial domains",
            "Clear milestone tracking for enterprise scaling"
        ],
        "process_steps": [
            {"step": "01", "title": "Initial Audit", "desc": "Comprehensive assessment of current business structure & financials."},
            {"step": "02", "title": "Gap Analysis", "desc": "Identifying operational inefficiencies and compliance gaps."},
            {"step": "03", "title": "Strategy Design", "desc": "Formulating tailored growth, cost-control, and structural plans."},
            {"step": "04", "title": "Execution Support", "desc": "Guiding management through rollout and performance review."}
        ],
        "faqs": [
            {"question": "Which entity structure is best for my startup?", "answer": "We evaluate your funding plans, liability tolerance, tax implications, and operational scale before recommending Private Limited, LLP, or Partnership structures."},
            {"question": "How does cost accounting benefit growing businesses?", "answer": "CMA advisory pinpoints precise product/service margins, uncovers hidden waste, and improves pricing models."}
        ]
    },
    {
        "title": "Finance & Loan Assistance",
        "slug": "finance-loan-assistance",
        "order": 4,
        "icon": "banknote",
        "short_description": "CMA data preparation, bank loan project reports, working capital credit assistance, and MSME debt syndication.",
        "description": "Securing commercial debt or bank credit lines requires impeccably prepared financial documentation. MVR Associates specializes in drafting CMA data (Credit Monitoring Arrangement), detailed project reports, and financial projections that conform to banking standards for loan appraisal.",
        "problems_addressed": [
            "Loan rejection due to incomplete or improper CMA data",
            "Inadequate working capital limit allocation from financial institutions",
            "Inability to present clear debt service coverage ratios (DSCR)",
            "Delay in bank loan appraisal and sanction turnaround times"
        ],
        "services_included": [
            "CMA Data preparation conforming to RBI & bank appraisal norms",
            "Bankable Detailed Project Reports (DPR) for new/expansion projects",
            "Working capital loan assistance (CC/OD limits, Letters of Credit)",
            "Term loan documentation & Debt Service Coverage Ratio (DSCR) modeling",
            "MSME & CGTMSE scheme documentation support"
        ],
        "benefits": [
            "Bank-compliant financial modeling increasing appraisal transparency",
            "Accurate projection of turnover, margins, and debt repayment capability",
            "Streamlined bank liaison and documentation turnaround",
            "Optimized capital structure balancing equity and debt"
        ],
        "process_steps": [
            {"step": "01", "title": "Requirement Assessment", "desc": "Determining funding requirements & credit line type."},
            {"step": "02", "title": "Data Compilation", "desc": "Gathering audited financials, estimates, and asset details."},
            {"step": "03", "title": "CMA Drafting", "desc": "Constructing multi-year financial statements & ratio models."},
            {"step": "04", "title": "Submission Support", "desc": "Finalizing DPR report for presentation to bank loan sanction officers."}
        ],
        "faqs": [
            {"question": "What is CMA Data in bank loans?", "answer": "CMA Data (Credit Monitoring Arrangement) is a structured multi-year financial presentation required by Indian banks to assess creditworthiness and working capital limits."},
            {"question": "Do you guarantee loan sanction?", "answer": "While loan sanction decisions rest solely with lending institutions, our CMA reports adhere strictly to bank underwriting guidelines to maximize approval eligibility."}
        ]
    },
    {
        "title": "Project Reports",
        "slug": "project-reports",
        "order": 5,
        "icon": "file-text",
        "short_description": "Detailed feasibility reports, financial projections, techno-economic evaluations, and industrial project documentation.",
        "description": "A well-structured Project Report is essential for obtaining government approvals, subsidy sanctions, bank financing, and investor confidence. MVR Associates authors detailed, realistic Techno-Economic Viability (TEV) reports and project profiles customized for industrial, commercial, and service sector ventures.",
        "problems_addressed": [
            "Unrealistic financial projections damaging enterprise credibility",
            "Lack of detailed capital cost breakdown and operational assumptions",
            "Inability to fulfill subsidy or industrial grant documentation requirements",
            "Unclear break-even and payback period calculations"
        ],
        "services_included": [
            "Techno-Economic Viability (TEV) report authoring",
            "Detailed capital expenditure (CAPEX) & operational expenditure (OPEX) estimation",
            "Sensitivity analysis, internal rate of return (IRR), and net present value (NPV) modeling",
            "Project profiles for government incentives & industrial land allocation",
            "Executive summary decks for financial institutions"
        ],
        "benefits": [
            "Methodical financial assumptions validated by CMA professionals",
            "Clear representation of payback period, break-even point, and margins",
            "Compliance with government subsidy & industrial board documentation norms",
            "Professional presentation suitable for bank managers and institutional stakeholders"
        ],
        "process_steps": [
            {"step": "01", "title": "Scope Definition", "desc": "Defining project capacity, location, plant & machinery details."},
            {"step": "02", "title": "Financial Modeling", "desc": "Calculating cost of project, means of finance, and operational costs."},
            {"step": "03", "title": "Ratio & Sensitivity Analysis", "desc": "Testing project resilience against cost overruns or revenue dips."},
            {"step": "04", "title": "Final Dossier", "desc": "Delivering bound comprehensive project report."}
        ],
        "faqs": [
            {"question": "What key metrics are included in your Project Reports?", "answer": "Our reports include DSCR, IRR, NPV, Break-Even Analysis, Sensitivity Analysis, Balance Sheets, and Cash Flow Statements for 5-10 projected years."},
            {"question": "Can project reports be customized for subsidy claims?", "answer": "Yes, we tailor documentation to align with specific central and state government subsidy scheme guidelines."}
        ]
    },
    {
        "title": "Legal Documentation & Support",
        "slug": "legal-documentation",
        "order": 6,
        "icon": "scale",
        "short_description": "Commercial contract drafting, partnership deeds, NDAs, employment agreements, vendor terms, and legal compliance advisory.",
        "description": "Legal documentation forms the legal shield of any enterprise. Spearheaded by LL.B qualified legal consultancy background, MVR Associates drafts, reviews, and negotiates commercial contracts, partnership deeds, non-disclosure agreements, and operational agreements to safeguard your commercial interests and mitigate legal risks.",
        "problems_addressed": [
            "Vague contract clauses leading to commercial disputes & financial loss",
            "Unprotected intellectual property, trade secrets, or client data",
            "Ambiguous partnership terms causing partner deadlock",
            "Non-compliant vendor or employment terms exposing firm to liability"
        ],
        "services_included": [
            "Commercial contract drafting & legal review (SLA, Vendor, Distribution)",
            "Partnership deeds, LLP agreements & Memorandum of Understanding (MoU)",
            "Non-Disclosure Agreements (NDA) & Confidentiality agreements",
            "Employment contracts, non-compete clauses & HR policy documentation",
            "Legal notices drafting & preliminary dispute resolution advisory"
        ],
        "benefits": [
            "Legally sound contract structures drafted with LL.B legal background",
            "Protection against default, liability exposure, and contract breach",
            "Clear dispute resolution and arbitration mechanisms embedded in contracts",
            "Compliance with Indian Contract Act and relevant commercial statutes"
        ],
        "process_steps": [
            {"step": "01", "title": "Requirement Briefing", "desc": "Understanding commercial intent, parties, and deal terms."},
            {"step": "02", "title": "Risk Mapping", "desc": "Identifying potential legal risks, liabilities, and default conditions."},
            {"step": "03", "title": "Drafting", "desc": "Formulating comprehensive legal clauses, covenants, and remedies."},
            {"step": "04", "title": "Review & Finalization", "desc": "Refining terms with client prior to execution."}
        ],
        "faqs": [
            {"question": "Why is customized contract drafting important over online templates?", "answer": "Generic online templates often omit critical jurisdictional, indemnity, and dispute clauses required under Indian law, leaving your business legally vulnerable."},
            {"question": "Do you provide legal litigation representation in courts?", "answer": "Our legal service focuses on corporate documentation, contract advisory, statutory compliance, and preliminary notices support."}
        ]
    },
    {
        "title": "HR & Payroll Consultancy",
        "slug": "hr-payroll-consultancy",
        "order": 7,
        "icon": "users",
        "short_description": "Statutory payroll processing, PF/ESI return compliance, employment agreements, HR policy manuals, and labor law advisory.",
        "description": "Managing human resources requires balancing employee satisfaction with strict labor law compliance. MVR Associates provides streamlined payroll calculations, Provident Fund (PF), Employee State Insurance (ESI), Professional Tax (PT) filings, and labor law advisory to keep your workplace compliant.",
        "problems_addressed": [
            "Errors in salary calculations, TDS deductions, or net pay disbursemal",
            "Penalties for delayed PF/ESI monthly return submissions",
            "Non-compliance with local Shops & Establishments and labor acts",
            "Lack of formal HR employee handbooks & grievance policies"
        ],
        "services_included": [
            "Monthly salary structure design & net pay processing",
            "Employees' Provident Fund (EPF) & ESI registration and monthly filings",
            "Professional Tax (PT) deduction & deposit advisory",
            "Form 16 generation & salary TDS compliance",
            "Drafting HR manuals, code of conduct, and employment letters"
        ],
        "benefits": [
            "Zero salary calculation errors and automated pay-slip generation data",
            "100% labor statutory compliance avoiding inspections and fines",
            "Clear HR policies fostering professional workplace discipline",
            "Confidential payroll data management"
        ],
        "process_steps": [
            {"step": "01", "title": "Attendance Input", "desc": "Receiving monthly attendance, leave, and overtime records."},
            {"step": "02", "title": "Payroll Computation", "desc": "Calculating gross pay, PF, ESI, PT, TDS, and net payable."},
            {"step": "03", "title": "Statutory Filing", "desc": "Generating ECR challans for PF & ESI portals."},
            {"step": "04", "title": "Disbursal Data", "desc": "Providing bank-ready salary transfer sheets & pay slips."}
        ],
        "faqs": [
            {"question": "When is PF & ESI registration mandatory for a business?", "answer": "PF registration is generally mandatory for establishments employing 20 or more persons, while ESI applies to 10 or more employees (subject to wage thresholds under rules)."},
            {"question": "How do you handle confidential payroll data?", "answer": "All payroll files are processed using secure encrypted systems with strict access controls."}
        ]
    }
]

ARTICLES_DATA = [
    {
        "title": "GST Annual Return Filing (GSTR-9): Step-by-Step Checklist for FY 2025-26",
        "slug": "gst-annual-return-filing-checklist-gstr-9",
        "category": "Tax",
        "excerpt": "A comprehensive guide for finance heads and business owners on reconciling GSTR-1, GSTR-3B, and GSTR-2B before filing annual GST returns.",
        "content": "Annual GST filing under GSTR-9 requires thorough reconciliation between outer turn-over reported in monthly returns and internal audited financial statements. MVR Associates has compiled this essential checklist to avoid notices under Section 73 & 74.\n\n### Key Steps in GSTR-9 Preparation\n\n1. **GSTR-2B vs GSTR-3B Input Tax Credit (ITC) Matching**: Ensure all eligible ITC claimed matches the auto-populated GSTR-2B figures.\n2. **Outward Supply Adjustments**: Verify rate-wise taxable values and tax paid under CGST, SGST, and IGST.\n3. **HSN Summary Accuracy**: Ensure HSN codes for both inward and outward supplies align with statutory turnover thresholds.\n4. **Handling Reversals**: Accurately report ITC reversals under Rules 37, 42, and 43.",
        "featured_image": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=800&q=80"
    },
    {
        "title": "Choosing Between LLP and Private Limited Company: A Legal & Tax Perspective",
        "slug": "choosing-between-llp-and-private-limited-company",
        "category": "Legal",
        "excerpt": "Evaluating equity dilution, statutory compliance costs, dividend distribution tax, and partner liability for growing ventures in India.",
        "content": "Selecting the appropriate legal entity structure sets the foundation for your commercial journey. Both Limited Liability Partnerships (LLP) and Private Limited Companies (Pvt Ltd) offer limited liability protection, but differ significantly in governance and tax implications.\n\n### Comparison Highlights\n\n- **Ownership & Equity**: Private Limited companies allow straightforward equity issuance to investors via share allotment. LLPs require partner capital percentage restructuring.\n- **Compliance Burden**: Pvt Ltd companies must hold AGM, maintain board minutes, and submit MGT-7 filings. LLPs enjoy fewer statutory filings.\n- **Profit Withdrawal**: LLPs allow profit distribution to partners without dividend distribution tax friction.",
        "featured_image": "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=800&q=80"
    },
    {
        "title": "How to Prepare Bankable CMA Data & Project Reports for Working Capital Sanction",
        "slug": "prepare-bankable-cma-data-project-reports",
        "category": "Finance",
        "excerpt": "Essential financial ratios, DSCR targets, and inventory turn assumptions that bank credit appraisal officers scrutinize.",
        "content": "Credit Monitoring Arrangement (CMA) data serves as the principal dossier evaluated by commercial banks for Cash Credit (CC), Overdraft (OD), and Term Loan approvals.\n\n### Vital Financial Ratios to Focus On\n\n1. **Current Ratio**: Maintain a minimum current ratio of 1.33:1 as prescribed by Nayak Committee guidelines.\n2. **Debt Service Coverage Ratio (DSCR)**: A healthy DSCR of 1.5 to 2.0 demonstrates adequate debt repayment capacity.\n3. **Working Capital Cycle**: Present realistic holding periods for raw materials, work-in-progress, and trade receivables.",
        "featured_image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80"
    },
    {
        "title": "Strategic Cost Reduction & Overhead Optimization for Manufacturing SMEs",
        "slug": "strategic-cost-reduction-overhead-optimization",
        "category": "Business",
        "excerpt": "Practical cost accounting techniques to identify hidden operational waste, optimize inventory turns, and protect gross margins.",
        "content": "In competitive markets, profit expansion often depends more on operational cost management than top-line revenue growth. Leveraging Cost & Management Accounting (CMA) principles empowers SMEs to pinpoint margin leakage.\n\n### Actionable Cost Control Strategies\n\n- **Activity-Based Costing (ABC)**: Allocate indirect overheads accurately based on actual driver consumption rather than flat percentages.\n- **Vendor Contract Renegotiation**: Audit recurring raw material and logistics agreements periodically.\n- **Variance Analysis**: Track monthly standard vs actual cost variances to detect waste early.",
        "featured_image": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=800&q=80"
    },
    {
        "title": "Statutory Labor Compliance Checklist for Enterprises: EPF, ESI, and PT",
        "slug": "statutory-labor-compliance-checklist-epf-esi-pt",
        "category": "HR",
        "excerpt": "Stay compliant with Employees Provident Fund, ESI wages ceiling, and Professional Tax monthly returns to prevent penalty notices.",
        "content": "Maintaining seamless statutory payroll compliance is crucial to preventing inspections, fines, and legal notices under Indian labor statutes.\n\n### Monthly HR Compliance Workflow\n\n1. **EPF Deduction & Deposit**: Deduct 12% employee contribution on eligible basic salary and deposit via ECR portal by the 15th of every month.\n2. **ESI Coverage**: Ensure all employees drawing gross monthly wages up to Rs. 21,000 are registered under ESI.\n3. **Professional Tax (PT)**: Remit state-specific PT deductions on time based on slab rates.",
        "featured_image": "https://images.unsplash.com/photo-1521791136064-7986c2920216?auto=format&fit=crop&w=800&q=80"
    }
]

def seed_database():
    with app.app_context():
        print("Creating database tables if not existing...")
        db.create_all()

        # Seed Admin User if not exists
        admin = User.query.filter_by(email="admin@mvrassociates.com").first()
        if not admin:
            admin = User(
                name="MVR Admin",
                email="admin@mvrassociates.com",
                role="admin"
            )
            admin.set_password("AdminMVR2026Secure!")
            db.session.add(admin)
            print("Seeded default admin user: admin@mvrassociates.com")

        # Seed 7 Core Services
        for data in SERVICES_DATA:
            service = Service.query.filter_by(slug=data["slug"]).first()
            if not service:
                service = Service(
                    title=data["title"],
                    slug=data["slug"],
                    order=data["order"],
                    icon=data["icon"],
                    short_description=data["short_description"],
                    description=data["description"],
                    is_active=True
                )
            else:
                service.title = data["title"]
                service.order = data["order"]
                service.icon = data["icon"]
                service.short_description = data["short_description"]
                service.description = data["description"]

            # Assign JSON properties
            service.problems_addressed = data["problems_addressed"]
            service.services_included = data["services_included"]
            service.benefits = data["benefits"]
            service.process_steps = data["process_steps"]
            service.faqs = data["faqs"]

            db.session.add(service)
            print(f"Seeded service: {service.title} ({service.slug})")

        # Seed Articles
        for art_data in ARTICLES_DATA:
            article = Article.query.filter_by(slug=art_data["slug"]).first()
            if not article:
                article = Article(
                    title=art_data["title"],
                    slug=art_data["slug"],
                    category=art_data["category"],
                    excerpt=art_data["excerpt"],
                    content=art_data["content"],
                    featured_image=art_data["featured_image"],
                    is_published=True
                )
                db.session.add(article)
                print(f"Seeded article: {article.title}")

        db.session.commit()
        print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed_database()

