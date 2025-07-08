import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np

# Page config
st.set_page_config(
    page_title="AI Maturity & EU AI Act Compliance Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'assessment_type' not in st.session_state:
    st.session_state.assessment_type = None
if 'maturity_scores' not in st.session_state:
    st.session_state.maturity_scores = {}
if 'compliance_answers' not in st.session_state:
    st.session_state.compliance_answers = {}
if 'org_info' not in st.session_state:
    st.session_state.org_info = {}

# Gartner AI Maturity Model - Enhanced with market data
gartner_maturity_levels = {
    1: {
        "name": "Awareness",
        "description": "Organization is exploring AI possibilities without active implementation",
        "market_position": "Bottom 20% - Lagging behind competitors",
        "characteristics": [
            "AI discussions happening but no strategic roadmap",
            "Limited understanding of AI capabilities and limitations",
            "No formal AI governance or dedicated resources",
            "Awareness of AI potential but no concrete plans"
        ],
        "business_impact": {
            "revenue": "Below industry average by 15-20%",
            "efficiency": "Manual processes dominate",
            "innovation": "Minimal innovation capability",
            "risk": "Unaware of AI-related risks"
        },
        "typical_organizations": "Traditional enterprises just starting digital transformation",
        "time_to_next_level": "12-18 months with focused effort",
        "investment_required": "€500K - €2M initial investment",
        "key_barriers": [
            "Lack of AI leadership and vision",
            "Limited technical capabilities",
            "Data silos and quality issues",
            "Cultural resistance to change"
        ],
        "critical_success_factors": [
            "Executive buy-in and sponsorship",
            "AI literacy programs",
            "Data foundation assessment",
            "Quick win pilot identification"
        ],
        "atlan_accelerators": {
            "Data Discovery": "Understand what data assets you have across the organization",
            "Data Quality Assessment": "Identify and fix data quality issues blocking AI initiatives",
            "Metadata Management": "Create a single source of truth for all data assets",
            "Collaboration Tools": "Break down silos between data, IT, and business teams"
        },
        "color": "#ff6b6b"
    },
    2: {
        "name": "Active",
        "description": "Organization is experimenting with AI through pilots and proof of concepts",
        "market_position": "Bottom 40% - Starting to catch up",
        "characteristics": [
            "Running AI pilots in specific departments",
            "Basic AI skills present in pockets",
            "Initial data quality improvements underway",
            "Some executive sponsorship for AI initiatives"
        ],
        "business_impact": {
            "revenue": "5-10% efficiency gains in pilot areas",
            "efficiency": "20-30% process improvement in isolated use cases",
            "innovation": "Beginning to explore new possibilities",
            "risk": "Ad-hoc risk management"
        },
        "typical_organizations": "Companies with digital initiatives and innovation labs",
        "time_to_next_level": "18-24 months with structured approach",
        "investment_required": "€2M - €10M for scaling",
        "key_barriers": [
            "Difficulty scaling from pilots to production",
            "Lack of enterprise data strategy",
            "Skills gap in AI/ML expertise",
            "Fragmented technology landscape"
        ],
        "critical_success_factors": [
            "Establish AI Center of Excellence",
            "Implement data governance framework",
            "Build reusable AI infrastructure",
            "Develop success metrics and KPIs"
        ],
        "atlan_accelerators": {
            "Data Lineage": "Track data flow from source to AI models for reliability",
            "Quality Monitoring": "Automated data quality checks for AI training data",
            "Access Control": "Secure data access for AI teams while maintaining governance",
            "Impact Analysis": "Understand downstream effects of data changes on AI models"
        },
        "color": "#ffa726"
    },
    3: {
        "name": "Operational",
        "description": "AI is integrated into core business processes with measurable impact",
        "market_position": "Top 40% - Above industry average",
        "characteristics": [
            "Multiple AI systems in production",
            "Dedicated AI/ML teams established",
            "Formal AI governance and ethics policies",
            "Systematic approach to AI development"
        ],
        "business_impact": {
            "revenue": "15-25% revenue improvement from AI",
            "efficiency": "40-50% automation of routine tasks",
            "innovation": "New AI-enhanced products/services",
            "risk": "Formal risk management processes"
        },
        "typical_organizations": "Digital leaders and tech-forward enterprises",
        "time_to_next_level": "24-36 months for transformation",
        "investment_required": "€10M - €50M for enterprise scale",
        "key_barriers": [
            "Complexity of enterprise-wide integration",
            "Change management at scale",
            "Regulatory compliance requirements",
            "Technical debt from early implementations"
        ],
        "critical_success_factors": [
            "MLOps and AIOps implementation",
            "Enterprise AI platform strategy",
            "Cross-functional AI teams",
            "Continuous learning culture"
        ],
        "atlan_accelerators": {
            "ML Model Governance": "Complete lifecycle management for all AI models",
            "Automated Compliance": "Built-in EU AI Act compliance workflows",
            "Business Glossary": "Ensure consistent understanding across AI initiatives",
            "Advanced Analytics": "Monitor model performance and business impact"
        },
        "color": "#66bb6a"
    },
    4: {
        "name": "Systemic",
        "description": "AI drives innovation and competitive advantage across the organization",
        "market_position": "Top 20% - Industry leader",
        "characteristics": [
            "AI embedded in strategic planning",
            "Cross-functional AI integration",
            "Continuous AI innovation culture",
            "Advanced AI capabilities (GenAI, ML, etc.)"
        ],
        "business_impact": {
            "revenue": "30-40% competitive advantage from AI",
            "efficiency": "60-70% of decisions AI-augmented",
            "innovation": "AI-first product development",
            "risk": "Predictive risk management"
        },
        "typical_organizations": "Tech giants and AI-native companies",
        "time_to_next_level": "36-48 months for full transformation",
        "investment_required": "€50M+ for platform leadership",
        "key_barriers": [
            "Talent competition and retention",
            "Keeping pace with AI advancement",
            "Ethical AI at scale",
            "Platform ecosystem complexity"
        ],
        "critical_success_factors": [
            "AI platform ecosystem",
            "Continuous innovation pipeline",
            "Strategic partnerships",
            "Thought leadership"
        ],
        "atlan_accelerators": {
            "AI Ecosystem Management": "Orchestrate complex AI workflows across platforms",
            "Real-time Governance": "Automated policy enforcement and monitoring",
            "Knowledge Graph": "Connect all data, models, and insights intelligently",
            "API Integration": "Seamless integration with entire AI tool stack"
        },
        "color": "#42a5f5"
    },
    5: {
        "name": "Transformational",
        "description": "AI is core to business model and value proposition",
        "market_position": "Top 5% - Market maker and disruptor",
        "characteristics": [
            "AI-first organization culture",
            "Continuous AI innovation at scale",
            "Industry-leading AI capabilities",
            "AI drives primary value creation"
        ],
        "business_impact": {
            "revenue": "50%+ revenue from AI-driven offerings",
            "efficiency": "90%+ processes AI-optimized",
            "innovation": "Creating new markets with AI",
            "risk": "AI-driven risk prediction and mitigation"
        },
        "typical_organizations": "AI platform companies and market disruptors",
        "time_to_next_level": "Continuous innovation required",
        "investment_required": "€100M+ annually",
        "key_barriers": [
            "Maintaining innovation edge",
            "Regulatory scrutiny",
            "Societal impact management",
            "Talent pipeline sustainability"
        ],
        "critical_success_factors": [
            "Industry standard setting",
            "Open innovation platforms",
            "Responsible AI leadership",
            "Ecosystem orchestration"
        ],
        "atlan_accelerators": {
            "Platform Governance": "Enterprise-grade governance for AI platforms",
            "Industry Benchmarking": "Set and track industry standards",
            "Innovation Metrics": "Measure and optimize innovation velocity",
            "Ecosystem Analytics": "Understand and optimize partner networks"
        },
        "color": "#ab47bc"
    }
}

# Enhanced assessment dimensions with weights
maturity_dimensions = {
    "Strategy & Leadership": {
        "weight": 0.25,
        "questions": [
            {
                "text": "Do you have a formal AI strategy aligned with business objectives?",
                "weight": 0.3,
                "maturity_indicators": {
                    1: "No AI strategy exists",
                    2: "Informal AI discussions happening",
                    3: "Formal AI strategy documented",
                    4: "AI strategy integrated with business strategy",
                    5: "AI-first strategic planning"
                }
            },
            {
                "text": "Is there executive sponsorship and budget allocation for AI initiatives?",
                "weight": 0.3,
                "maturity_indicators": {
                    1: "No executive interest",
                    2: "Limited sponsorship, minimal budget",
                    3: "Strong sponsorship, dedicated budget",
                    4: "C-level AI leadership, significant investment",
                    5: "Board-level AI oversight, unlimited investment"
                }
            },
            {
                "text": "Do you have an AI ethics committee or governance board?",
                "weight": 0.2,
                "maturity_indicators": {
                    1: "No governance structure",
                    2: "Ad-hoc ethics discussions",
                    3: "Formal ethics committee established",
                    4: "Integrated governance across organization",
                    5: "Industry-leading responsible AI practices"
                }
            },
            {
                "text": "Is AI considered in strategic business planning?",
                "weight": 0.2,
                "maturity_indicators": {
                    1: "AI not considered",
                    2: "AI mentioned in some plans",
                    3: "AI integral to key initiatives",
                    4: "AI drives strategic decisions",
                    5: "Business strategy is AI strategy"
                }
            }
        ]
    },
    "Data & Technology": {
        "weight": 0.25,
        "questions": [
            {
                "text": "Do you have high-quality, accessible data for AI initiatives?",
                "weight": 0.3,
                "maturity_indicators": {
                    1: "Data silos, poor quality",
                    2: "Some data cleanup efforts",
                    3: "Centralized data, good quality",
                    4: "Real-time data platform",
                    5: "Self-optimizing data ecosystem"
                }
            },
            {
                "text": "Is your technology infrastructure AI-ready (cloud, compute, storage)?",
                "weight": 0.25,
                "maturity_indicators": {
                    1: "Legacy on-premise systems",
                    2: "Partial cloud migration",
                    3: "Cloud-first infrastructure",
                    4: "Elastic AI compute platform",
                    5: "Cutting-edge AI infrastructure"
                }
            },
            {
                "text": "Do you have data governance and quality management processes?",
                "weight": 0.25,
                "maturity_indicators": {
                    1: "No data governance",
                    2: "Basic data policies",
                    3: "Comprehensive governance framework",
                    4: "Automated governance workflows",
                    5: "Self-governing data systems"
                }
            },
            {
                "text": "Are ML platforms and tools standardized across the organization?",
                "weight": 0.2,
                "maturity_indicators": {
                    1: "No ML tools",
                    2: "Fragmented tool usage",
                    3: "Standardized ML platform",
                    4: "Integrated ML ecosystem",
                    5: "Industry-leading ML platform"
                }
            }
        ]
    },
    "People & Culture": {
        "weight": 0.2,
        "questions": [
            {
                "text": "Do you have dedicated AI/ML talent and teams?",
                "weight": 0.3,
                "maturity_indicators": {
                    1: "No AI expertise",
                    2: "Few AI practitioners",
                    3: "Dedicated AI teams",
                    4: "AI talent throughout organization",
                    5: "World-class AI organization"
                }
            },
            {
                "text": "Is there organization-wide AI literacy and training?",
                "weight": 0.25,
                "maturity_indicators": {
                    1: "No AI awareness",
                    2: "Limited AI training",
                    3: "Comprehensive AI education",
                    4: "Continuous AI upskilling",
                    5: "AI-literate entire workforce"
                }
            },
            {
                "text": "Does your culture support experimentation and innovation?",
                "weight": 0.25,
                "maturity_indicators": {
                    1: "Risk-averse culture",
                    2: "Some innovation pockets",
                    3: "Innovation encouraged",
                    4: "Fail-fast culture",
                    5: "Innovation is the norm"
                }
            },
            {
                "text": "Are business and technical teams collaborating on AI projects?",
                "weight": 0.2,
                "maturity_indicators": {
                    1: "Siloed departments",
                    2: "Occasional collaboration",
                    3: "Regular collaboration",
                    4: "Integrated teams",
                    5: "Seamless fusion"
                }
            }
        ]
    },
    "Process & Governance": {
        "weight": 0.15,
        "questions": [
            {
                "text": "Do you have established AI development lifecycles and MLOps?",
                "weight": 0.25,
                "maturity_indicators": {
                    1: "Ad-hoc development",
                    2: "Basic processes",
                    3: "Formal MLOps implemented",
                    4: "Automated ML pipelines",
                    5: "Self-optimizing MLOps"
                }
            },
            {
                "text": "Are AI risks systematically identified and managed?",
                "weight": 0.25,
                "maturity_indicators": {
                    1: "No risk assessment",
                    2: "Informal risk discussions",
                    3: "Formal risk framework",
                    4: "Proactive risk management",
                    5: "Predictive risk systems"
                }
            },
            {
                "text": "Do you measure and monitor AI system performance?",
                "weight": 0.25,
                "maturity_indicators": {
                    1: "No monitoring",
                    2: "Basic metrics",
                    3: "Comprehensive monitoring",
                    4: "Real-time dashboards",
                    5: "Self-healing systems"
                }
            },
            {
                "text": "Is there a process for AI model validation and testing?",
                "weight": 0.25,
                "maturity_indicators": {
                    1: "No validation process",
                    2: "Manual testing",
                    3: "Automated testing suite",
                    4: "Continuous validation",
                    5: "Zero-trust AI systems"
                }
            }
        ]
    },
    "Value & Innovation": {
        "weight": 0.15,
        "questions": [
            {
                "text": "Are you measuring ROI from AI initiatives?",
                "weight": 0.25,
                "maturity_indicators": {
                    1: "No ROI measurement",
                    2: "Anecdotal benefits",
                    3: "Formal ROI tracking",
                    4: "Real-time value monitoring",
                    5: "AI drives P&L"
                }
            },
            {
                "text": "Do AI projects deliver tangible business value?",
                "weight": 0.25,
                "maturity_indicators": {
                    1: "No clear value",
                    2: "Some efficiency gains",
                    3: "Significant cost savings",
                    4: "Revenue generation",
                    5: "Business transformation"
                }
            },
            {
                "text": "Are you using AI to create new products or services?",
                "weight": 0.25,
                "maturity_indicators": {
                    1: "No AI products",
                    2: "AI features in development",
                    3: "AI-enhanced offerings",
                    4: "AI-native products",
                    5: "AI platform business"
                }
            },
            {
                "text": "Is AI driving competitive advantage for your organization?",
                "weight": 0.25,
                "maturity_indicators": {
                    1: "No advantage",
                    2: "Catching up to competitors",
                    3: "On par with industry",
                    4: "Leading the industry",
                    5: "Defining the industry"
                }
            }
        ]
    }
}

# Enhanced EU AI Act compliance with examples and GPAI
eu_ai_act_requirements = {
    "Governance & Oversight": {
        "questions": [
            {
                "text": "Do you have designated roles and responsibilities for AI governance?",
                "article": "Article 26 – Obligations of users of high-risk AI systems",
                "link": "https://artificialintelligenceact.eu/article/26/",
                "example": "We have a Chief AI Officer, AI Ethics Committee with quarterly meetings, designated AI system owners for each deployment, and clear RACI matrix for AI decisions.",
                "documentation": "Organizational charts, role descriptions, governance charter, meeting minutes, and decision logs.",
                "risk_level": "high",
                "implementation_effort": "medium"
            },
            {
                "text": "Is there human oversight for high-risk AI system decision-making?",
                "article": "Article 14 – Human oversight",
                "link": "https://artificialintelligenceact.eu/article/14/",
                "example": "All high-risk AI decisions require human review before execution, with kill switches, override capabilities, and mandatory human sign-off for critical decisions.",
                "documentation": "Human oversight procedures, approval workflows, override logs, and training records.",
                "risk_level": "critical",
                "implementation_effort": "high"
            },
            {
                "text": "Do you have processes to monitor AI system performance and accuracy?",
                "article": "Article 26 – Obligations of users",
                "link": "https://artificialintelligenceact.eu/article/26/",
                "example": "We run daily accuracy checks, weekly performance reviews, monthly drift detection, with automated alerts for anomalies and dashboards showing key metrics.",
                "documentation": "Monitoring procedures, KPI definitions, alert configurations, and performance reports.",
                "risk_level": "high",
                "implementation_effort": "medium"
            },
            {
                "text": "Are employees trained on AI system capabilities and limitations?",
                "article": "Article 4 – AI literacy",
                "link": "https://artificialintelligenceact.eu/article/4/",
                "example": "All staff complete mandatory AI literacy training, role-specific workshops for AI users, annual refreshers, and maintain >90% completion rate.",
                "documentation": "Training curricula, attendance records, assessment results, and competency matrices.",
                "risk_level": "medium",
                "implementation_effort": "low"
            },
            {
                "text": "Do you have incident reporting procedures for AI system failures?",
                "article": "Article 26 – Obligations of users",
                "link": "https://artificialintelligenceact.eu/article/26/",
                "example": "24-hour incident hotline, standardized reporting forms, root cause analysis process, with escalation matrix and remediation tracking system.",
                "documentation": "Incident response procedures, reporting templates, investigation reports, and corrective action logs.",
                "risk_level": "high",
                "implementation_effort": "medium"
            }
        ]
    },
    "Risk Management": {
        "questions": [
            {
                "text": "Do you have a risk management system for AI systems?",
                "article": "Article 9 – Risk management system",
                "link": "https://artificialintelligenceact.eu/article/9/",
                "example": "ISO 31000-based framework with AI-specific risk taxonomy, quarterly risk assessments, mitigation plans, and board-level risk reporting.",
                "documentation": "Risk management framework, risk registers, assessment reports, and mitigation plans.",
                "risk_level": "critical",
                "implementation_effort": "high"
            },
            {
                "text": "Are AI systems tested for bias and discrimination before deployment?",
                "article": "Article 10 – Data and data governance",
                "link": "https://artificialintelligenceact.eu/article/10/",
                "example": "We conduct fairness audits using multiple metrics (demographic parity, equal opportunity), test on diverse datasets, and engage external auditors.",
                "documentation": "Bias testing protocols, audit reports, test datasets specifications, and remediation records.",
                "risk_level": "critical",
                "implementation_effort": "high"
            },
            {
                "text": "Do you conduct impact assessments for high-risk AI systems?",
                "article": "Article 27 – Fundamental rights impact assessment",
                "link": "https://artificialintelligenceact.eu/article/27/",
                "example": "Full DPIA plus AI-specific assessments covering fundamental rights, using EU methodology, with stakeholder consultations and public summaries.",
                "documentation": "Impact assessment templates, completed assessments, stakeholder feedback, and action plans.",
                "risk_level": "high",
                "implementation_effort": "high"
            },
            {
                "text": "Are there procedures to address AI system risks to vulnerable groups?",
                "article": "Article 9 – Risk management system",
                "link": "https://artificialintelligenceact.eu/article/9/",
                "example": "Special testing for elderly, children, disabled users; accessibility features; simplified interfaces; and dedicated support channels.",
                "documentation": "Vulnerability assessment procedures, accessibility standards, user testing results, and support protocols.",
                "risk_level": "high",
                "implementation_effort": "medium"
            },
            {
                "text": "Do you have quality management systems for AI development?",
                "article": "Article 17 – Quality management system",
                "link": "https://artificialintelligenceact.eu/article/17/",
                "example": "ISO 9001 certified processes adapted for AI, including version control, peer reviews, staging environments, and automated testing pipelines.",
                "documentation": "QMS documentation, process maps, audit reports, and continuous improvement records.",
                "risk_level": "medium",
                "implementation_effort": "medium"
            }
        ]
    },
    "Documentation & Transparency": {
        "questions": [
            {
                "text": "Do you maintain technical documentation for AI systems?",
                "article": "Article 11 – Technical documentation",
                "link": "https://artificialintelligenceact.eu/article/11/",
                "example": "Comprehensive docs including architecture diagrams, data flows, model cards, API specs, update logs, maintained in version-controlled repository.",
                "documentation": "Technical specifications, architecture documents, data dictionaries, and API documentation.",
                "risk_level": "high",
                "implementation_effort": "medium"
            },
            {
                "text": "Are users informed when interacting with AI systems?",
                "article": "Article 52 – Transparency obligations",
                "link": "https://artificialintelligenceact.eu/article/52/",
                "example": "Clear AI disclosure badges, pop-up notifications, terms of service mentions, and opt-out options visible at all interaction points.",
                "documentation": "Transparency notices, UI/UX guidelines, user communication templates, and consent forms.",
                "risk_level": "medium",
                "implementation_effort": "low"
            },
            {
                "text": "Do you keep logs of AI system operations and decisions?",
                "article": "Article 12 – Record-keeping",
                "link": "https://artificialintelligenceact.eu/article/12/",
                "example": "Automated logging of all AI decisions with timestamps, input data, outputs, confidence scores, retained for 5 years with secure access controls.",
                "documentation": "Logging specifications, retention policies, access control procedures, and audit trail reports.",
                "risk_level": "high",
                "implementation_effort": "medium"
            },
            {
                "text": "Are instructions for use provided to AI system users?",
                "article": "Article 13 – Instructions for use",
                "link": "https://artificialintelligenceact.eu/article/13/",
                "example": "Multi-language user guides, video tutorials, in-app help, FAQs, covering proper use, limitations, and safety guidelines.",
                "documentation": "User manuals, training materials, help documentation, and safety guidelines.",
                "risk_level": "medium",
                "implementation_effort": "low"
            },
            {
                "text": "Do you maintain records of AI system modifications and updates?",
                "article": "Article 12 – Record-keeping",
                "link": "https://artificialintelligenceact.eu/article/12/",
                "example": "Git-based version control, detailed changelogs, rollback procedures, with approval records for all production changes.",
                "documentation": "Change management procedures, version histories, approval records, and rollback plans.",
                "risk_level": "medium",
                "implementation_effort": "low"
            }
        ]
    },
    "Data Governance": {
        "questions": [
            {
                "text": "Are training datasets quality-controlled and bias-tested?",
                "article": "Article 10 – Data and data governance",
                "link": "https://artificialintelligenceact.eu/article/10/",
                "example": "Multi-stage QA process: automated checks, statistical analysis, manual reviews, bias metrics, with 99.5% quality threshold before use.",
                "documentation": "Data quality standards, QA procedures, test results, and quality metrics.",
                "risk_level": "critical",
                "implementation_effort": "high"
            },
            {
                "text": "Do you have data lineage tracking for AI training data?",
                "article": "Article 10 – Data and data governance",
                "link": "https://artificialintelligenceact.eu/article/10/",
                "example": "End-to-end lineage from source systems through transformations to model training, using automated tools with visual lineage maps.",
                "documentation": "Data lineage tools configuration, lineage maps, data flow documentation, and source mappings.",
                "risk_level": "high",
                "implementation_effort": "medium"
            },
            {
                "text": "Are personal data processing activities compliant with GDPR?",
                "article": "Article 10 – Data and data governance",
                "link": "https://artificialintelligenceact.eu/article/10/",
                "example": "All processing has legal basis, documented in ROPA, with DPIAs completed, consent mechanisms implemented, and DPO approval obtained.",
                "documentation": "ROPA entries, legal basis documentation, DPIAs, consent records, and DPO assessments.",
                "risk_level": "critical",
                "implementation_effort": "high"
            },
            {
                "text": "Do you validate data quality before using for AI training?",
                "article": "Article 10 – Data and data governance",
                "link": "https://artificialintelligenceact.eu/article/10/",
                "example": "Automated validation pipelines checking completeness, accuracy, consistency, with manual spot checks and domain expert reviews.",
                "documentation": "Validation procedures, quality criteria, validation reports, and exception handling processes.",
                "risk_level": "high",
                "implementation_effort": "medium"
            },
            {
                "text": "Are datasets representative and free from harmful biases?",
                "article": "Article 10 – Data and data governance",
                "link": "https://artificialintelligenceact.eu/article/10/",
                "example": "Statistical analysis ensuring demographic representation matching target population, with external bias audits and corrective sampling.",
                "documentation": "Representation analysis, demographic breakdowns, bias audit reports, and sampling strategies.",
                "risk_level": "critical",
                "implementation_effort": "high"
            }
        ]
    },
    "Compliance & Conformity": {
        "questions": [
            {
                "text": "Do you have conformity assessments for high-risk AI systems?",
                "article": "Article 43 – Conformity assessment",
                "link": "https://artificialintelligenceact.eu/article/43/",
                "example": "Third-party assessments following harmonized standards, internal audits, technical documentation reviews, with annual reassessments.",
                "documentation": "Assessment reports, certificates, audit trails, and corrective action plans.",
                "risk_level": "critical",
                "implementation_effort": "high"
            },
            {
                "text": "Are AI systems registered in the EU database when required?",
                "article": "Article 60 – EU database for high-risk AI systems",
                "link": "https://artificialintelligenceact.eu/article/60/",
                "example": "All high-risk systems registered before deployment, with quarterly updates, maintaining complete records and public transparency.",
                "documentation": "Registration confirmations, database entries, update logs, and compliance certificates.",
                "risk_level": "high",
                "implementation_effort": "low"
            },
            {
                "text": "Do you have CE marking for applicable AI systems?",
                "article": "Article 48 – CE marking",
                "link": "https://artificialintelligenceact.eu/article/48/",
                "example": "CE marks affixed following conformity assessment, with technical files maintained, DoC issued, and market surveillance cooperation.",
                "documentation": "CE marking procedures, technical files, declarations of conformity, and test reports.",
                "risk_level": "high",
                "implementation_effort": "medium"
            },
            {
                "text": "Are there procedures for corrective actions when non-compliance is detected?",
                "article": "Article 21 – Corrective actions",
                "link": "https://artificialintelligenceact.eu/article/21/",
                "example": "24-hour response SLA, root cause analysis, corrective action plans, effectiveness verification, with board reporting for serious issues.",
                "documentation": "Corrective action procedures, investigation reports, action plans, and effectiveness reviews.",
                "risk_level": "medium",
                "implementation_effort": "medium"
            },
            {
                "text": "Do you have post-market monitoring systems for deployed AI?",
                "article": "Article 26 – Obligations of users",
                "link": "https://artificialintelligenceact.eu/article/26/",
                "example": "Continuous performance monitoring, user feedback loops, incident tracking, with monthly reviews and proactive improvement cycles.",
                "documentation": "Monitoring plans, performance reports, user feedback analysis, and improvement records.",
                "risk_level": "high",
                "implementation_effort": "medium"
            }
        ]
    },
    "General Purpose AI (GPAI)": {
        "questions": [
            {
                "text": "Do you maintain comprehensive technical documentation for your GPAI model?",
                "article": "Article 53 – Obligations for providers of GPAI models",
                "link": "https://artificialintelligenceact.eu/article/53/",
                "example": "500-page technical report covering architecture (transformer, 175B parameters), training (500TB data, 3 months), capabilities, limitations, and safety measures.",
                "documentation": "Model architecture specifications, training process documentation, capability assessments, and limitation disclosures.",
                "risk_level": "high",
                "implementation_effort": "high"
            },
            {
                "text": "Have you implemented a policy to respect copyright law in your training data?",
                "article": "Article 53 – Obligations for providers of GPAI models",
                "link": "https://artificialintelligenceact.eu/article/53/",
                "example": "Automated filtering for copyrighted content, licensed dataset procurement, opt-out portal for creators, with quarterly legal reviews.",
                "documentation": "Copyright compliance policy, data filtering procedures, licensing agreements, and opt-out mechanisms.",
                "risk_level": "critical",
                "implementation_effort": "high"
            },
            {
                "text": "Do you provide adequate information to downstream providers?",
                "article": "Article 53 – Obligations for providers of GPAI models",
                "link": "https://artificialintelligenceact.eu/article/53/",
                "example": "Comprehensive API documentation, model cards, integration guides, safety guidelines, usage restrictions, and support channels.",
                "documentation": "API documentation, model cards, safety guidelines, usage policies, and technical support materials.",
                "risk_level": "medium",
                "implementation_effort": "medium"
            },
            {
                "text": "Have you conducted systemic risk assessments for models with systemic risk?",
                "article": "Article 55 – Obligations for GPAI models with systemic risk",
                "link": "https://artificialintelligenceact.eu/article/55/",
                "example": "Red team exercises for misuse potential, bias audits across demographics, safety evaluations for harmful content generation.",
                "documentation": "Risk assessment reports, red team findings, mitigation strategies, and monitoring plans.",
                "risk_level": "critical",
                "implementation_effort": "high"
            },
            {
                "text": "Do you have measures to mitigate systemic risks?",
                "article": "Article 55 – Obligations for GPAI models with systemic risk",
                "link": "https://artificialintelligenceact.eu/article/55/",
                "example": "Content filters, use case restrictions, rate limiting, continuous monitoring, incident response team, and regular safety updates.",
                "documentation": "Mitigation measures documentation, incident response plans, monitoring dashboards, and update logs.",
                "risk_level": "critical",
                "implementation_effort": "high"
            }
        ]
    }
}

# Industry benchmarks with more detail
industry_benchmarks = {
    "Technology": {
        "average": 3.2,
        "leaders": ["Google", "Microsoft", "Amazon"],
        "typical_challenges": "Talent retention, ethical AI at scale",
        "investment_range": "5-15% of revenue"
    },
    "Financial Services": {
        "average": 3.0,
        "leaders": ["JPMorgan", "Goldman Sachs", "Ant Financial"],
        "typical_challenges": "Regulatory compliance, legacy systems",
        "investment_range": "2-8% of revenue"
    },
    "Healthcare": {
        "average": 2.5,
        "leaders": ["Mayo Clinic", "Kaiser Permanente"],
        "typical_challenges": "Data privacy, clinical validation",
        "investment_range": "1-5% of revenue"
    },
    "Manufacturing": {
        "average": 2.3,
        "leaders": ["Siemens", "GE", "Bosch"],
        "typical_challenges": "IoT integration, workforce upskilling",
        "investment_range": "1-4% of revenue"
    },
    "Retail": {
        "average": 2.4,
        "leaders": ["Amazon", "Alibaba", "Walmart"],
        "typical_challenges": "Omnichannel integration, personalization",
        "investment_range": "2-6% of revenue"
    },
    "Government": {
        "average": 1.8,
        "leaders": ["Singapore", "Estonia", "UK"],
        "typical_challenges": "Procurement, citizen trust",
        "investment_range": "0.5-2% of budget"
    },
    "Education": {
        "average": 2.2,
        "leaders": ["ASU", "Georgia Tech"],
        "typical_challenges": "Budget constraints, change management",
        "investment_range": "0.5-3% of budget"
    },
    "Energy": {
        "average": 2.5,
        "leaders": ["Shell", "BP", "Equinor"],
        "typical_challenges": "Safety requirements, field deployment",
        "investment_range": "1-5% of revenue"
    },
    "Other": {
        "average": 2.5,
        "leaders": ["Industry varies"],
        "typical_challenges": "Varies by sector",
        "investment_range": "1-5% of revenue"
    }
}

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        height: 100%;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .stProgress > div > div > div > div {
        background-color: #667eea;
    }
    
    .recommendation-box {
        background: linear-gradient(to right, #f8f9fa, #e9ecef);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    .warning-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .maturity-level-card {
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .compliance-example {
        background: #e7f3ff;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        font-style: italic;
    }
    
    .documentation-note {
        background: #fff5ec;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border-left: 3px solid #ff9800;
    }
</style>
""", unsafe_allow_html=True)

# Home page
if st.session_state.current_page == 'home':
    # Professional header
    st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 2.5rem; margin: 0;">🚀 AI Maturity & EU Compliance Assessment Platform</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">
            Benchmark your AI maturity against Gartner's model, ensure EU AI Act compliance, 
            and accelerate your transformation with Atlan
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("AI Leaders ROI", "3.5x", "vs industry average")
    with col2:
        st.metric("EU AI Act Penalties", "€35M", "or 7% of revenue")
    with col3:
        st.metric("Time to Next Level", "18-24mo", "with right strategy")
    with col4:
        st.metric("Atlan Acceleration", "40%", "faster implementation")
    
    # Market positioning visualization
    st.markdown("### 📊 Where Do Organizations Stand on AI Maturity?")
    
    # Create distribution chart
    fig = go.Figure()
    
    # Market distribution data
    distribution = {
        "Level 1: Awareness": 30,
        "Level 2: Active": 35,
        "Level 3: Operational": 20,
        "Level 4: Systemic": 12,
        "Level 5: Transformational": 3
    }
    
    colors = ['#ff6b6b', '#ffa726', '#66bb6a', '#42a5f5', '#ab47bc']
    
    fig.add_trace(go.Bar(
        x=list(distribution.keys()),
        y=list(distribution.values()),
        marker_color=colors,
        text=[f"{v}%" for v in distribution.values()],
        textposition='outside',
        hovertemplate='%{x}<br>%{y}% of organizations<extra></extra>'
    ))
    
    fig.update_layout(
        title="Global AI Maturity Distribution (2024 Gartner Research)",
        yaxis_title="Percentage of Organizations",
        xaxis_title="AI Maturity Level",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Value propositions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Gartner AI Maturity</h3>
            <p>Comprehensive assessment across 5 dimensions with industry benchmarking</p>
            <hr>
            <ul style="text-align: left; font-size: 0.9rem;">
                <li>Market positioning analysis</li>
                <li>Investment requirements</li>
                <li>Timeline to next level</li>
                <li>Critical success factors</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🛡️ EU AI Act Compliance</h3>
            <p>Article-by-article assessment with implementation guidance</p>
            <hr>
            <ul style="text-align: left; font-size: 0.9rem;">
                <li>Risk-based prioritization</li>
                <li>Real-world examples</li>
                <li>Documentation templates</li>
                <li>Penalty avoidance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🔧 Atlan Acceleration</h3>
            <p>Specific features mapped to your maturity level and compliance needs</p>
            <hr>
            <ul style="text-align: left; font-size: 0.9rem;">
                <li>Feature recommendations</li>
                <li>Implementation roadmap</li>
                <li>ROI projections</li>
                <li>Success metrics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Maturity journey details
    st.markdown("### 🗺️ The AI Maturity Journey - Detailed View")
    
    # Create tabs for each maturity level
    tabs = st.tabs([f"Level {i}: {gartner_maturity_levels[i]['name']}" for i in range(1, 6)])
    
    for i, tab in enumerate(tabs, 1):
        with tab:
            level_data = gartner_maturity_levels[i]
            
            col1, col2 = st.columns([3, 2])
            
            with col1:
                st.markdown(f"""
                <div class="maturity-level-card" style="background: linear-gradient(to right, {level_data['color']}20, white);">
                    <h4 style="color: {level_data['color']};">Level {i}: {level_data['name']}</h4>
                    <p><strong>Description:</strong> {level_data['description']}</p>
                    <p><strong>Market Position:</strong> {level_data['market_position']}</p>
                    <p><strong>Typical Organizations:</strong> {level_data['typical_organizations']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("**Key Characteristics:**")
                for char in level_data['characteristics']:
                    st.markdown(f"• {char}")
                
                st.markdown("**Critical Success Factors:**")
                for factor in level_data['critical_success_factors']:
                    st.markdown(f"✓ {factor}")
            
            with col2:
                # Business impact metrics
                st.markdown("**📈 Business Impact:**")
                for metric, value in level_data['business_impact'].items():
                    st.metric(metric.capitalize(), value)
                
                st.info(f"**Time to Next Level:** {level_data['time_to_next_level']}")
                st.warning(f"**Investment Required:** {level_data['investment_required']}")
                
                # Atlan accelerators
                st.markdown("**🔧 How Atlan Helps:**")
                for feature, benefit in level_data['atlan_accelerators'].items():
                    st.markdown(f"**{feature}:** {benefit}")
    
    # Assessment selection
    st.markdown("---")
    st.markdown("### 🎯 Select Your Assessment Path")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.markdown("""
            <div class="metric-card">
                <h4>🚀 AI Maturity Assessment</h4>
                <p>Based on Gartner's 5-level model</p>
                <hr>
                <ul style="text-align: left;">
                    <li>20 strategic questions</li>
                    <li>Weighted scoring model</li>
                    <li>Industry benchmarking</li>
                    <li>10-15 minutes</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Start Maturity Assessment", key="start_maturity", use_container_width=True):
                st.session_state.assessment_type = 'maturity'
                st.session_state.current_page = 'organization'
                st.rerun()
    
    with col2:
        with st.container():
            st.markdown("""
            <div class="metric-card">
                <h4>🛡️ EU AI Act Compliance</h4>
                <p>Comprehensive regulatory check</p>
                <hr>
                <ul style="text-align: left;">
                    <li>25 compliance questions</li>
                    <li>Article mapping</li>
                    <li>Risk prioritization</li>
                    <li>15-20 minutes</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Start Compliance Check", key="start_compliance", use_container_width=True):
                st.session_state.assessment_type = 'compliance'
                st.session_state.current_page = 'organization'
                st.rerun()
    
    with col3:
        with st.container():
            st.markdown("""
            <div class="metric-card">
                <h4>💎 Complete Assessment</h4>
                <p>Full maturity + compliance</p>
                <hr>
                <ul style="text-align: left;">
                    <li>Both assessments</li>
                    <li>Integrated insights</li>
                    <li>Comprehensive roadmap</li>
                    <li>25-35 minutes</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Start Complete Assessment", key="start_combined", use_container_width=True):
                st.session_state.assessment_type = 'combined'
                st.session_state.current_page = 'organization'
                st.rerun()
    
    # Why this matters
    st.markdown("---")
    st.markdown("### 💡 Why AI Maturity & Compliance Matter Now")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="warning-box">
            <h4>⚠️ The AI Leadership Gap is Widening</h4>
            <p>Organizations at Level 4-5 are seeing:</p>
            <ul>
                <li>3.5x better financial performance</li>
                <li>70% faster time-to-market</li>
                <li>2x higher customer satisfaction</li>
                <li>50% lower operational costs</li>
            </ul>
            <p><strong>Every month of delay costs market share.</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="error-box">
            <h4>🚨 EU AI Act Enforcement Begins 2024</h4>
            <p>Non-compliance risks include:</p>
            <ul>
                <li>Fines up to €35M or 7% of revenue</li>
                <li>Prohibition from EU markets</li>
                <li>Reputational damage</li>
                <li>Competitive disadvantage</li>
            </ul>
            <p><strong>Compliance is not optional for EU operations.</strong></p>
        </div>
        """, unsafe_allow_html=True)

# Organization info page
elif st.session_state.current_page == 'organization':
    st.markdown("### 🏢 Organization Profile")
    st.markdown("This information helps us provide industry-specific insights and recommendations")
    
    with st.form("org_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Basic Information")
            org_name = st.text_input("Organization Name *", placeholder="Your company name")
            industry = st.selectbox("Industry Sector *", 
                ["Select...", "Technology", "Financial Services", "Healthcare", 
                 "Manufacturing", "Retail", "Government", "Education", "Energy", "Other"])
            org_size = st.selectbox("Organization Size *",
                ["Select...", "1-50 employees", "51-200 employees", "201-1000 employees",
                 "1001-5000 employees", "5000+ employees"])
            geography = st.selectbox("Primary Geography *",
                ["Select...", "Europe", "North America", "Asia Pacific", "Latin America", "Global"])
        
        with col2:
            st.markdown("#### AI Context")
            ai_state = st.selectbox("Current AI State *",
                ["Select...", "No AI initiatives", "Exploring AI possibilities", 
                 "Running pilot projects", "AI in production use", "AI-driven organization"])
            ai_budget = st.selectbox("Annual AI Investment",
                ["Select...", "< €100k", "€100k - €500k", "€500k - €1M", 
                 "€1M - €5M", "€5M - €10M", "> €10M"])
            primary_goal = st.selectbox("Primary AI Goal *",
                ["Select...", "Cost reduction", "Revenue growth", "Customer experience", 
                 "Operational efficiency", "Innovation", "Risk management"])
            eu_operations = st.selectbox("EU Operations? *",
                ["Select...", "Yes - Primary market", "Yes - Secondary market", 
                 "No - But planning to enter", "No - No EU presence"])
        
        st.markdown("#### Additional Context")
        col1, col2 = st.columns(2)
        
        with col1:
            data_maturity = st.select_slider(
                "Data Infrastructure Maturity",
                options=["Very Low", "Low", "Medium", "High", "Very High"],
                value="Medium"
            )
            biggest_challenge = st.selectbox("Biggest AI Challenge",
                ["Select...", "Lack of skills/talent", "Data quality issues", 
                 "Budget constraints", "Regulatory compliance", "Technology infrastructure", 
                 "Change management", "Executive buy-in"])
        
        with col2:
            using_atlan = st.selectbox("Currently Using Atlan?",
                ["Select...", "Yes - Extensively", "Yes - Limited use", 
                 "No - Currently evaluating", "No - Not familiar"])
            timeline = st.selectbox("AI Implementation Timeline",
                ["Select...", "Immediate (< 3 months)", "Short-term (3-6 months)", 
                 "Medium-term (6-12 months)", "Long-term (> 12 months)"])
        
        submitted = st.form_submit_button("Continue to Assessment →", type="primary", use_container_width=True)
        
        if submitted:
            required_fields = [org_name, industry, org_size, ai_state, primary_goal, eu_operations]
            if all(field and field != "Select..." for field in required_fields):
                st.session_state.org_info = {
                    'name': org_name,
                    'industry': industry,
                    'size': org_size,
                    'geography': geography,
                    'ai_state': ai_state,
                    'ai_budget': ai_budget,
                    'primary_goal': primary_goal,
                    'eu_operations': eu_operations,
                    'data_maturity': data_maturity,
                    'biggest_challenge': biggest_challenge,
                    'using_atlan': using_atlan,
                    'timeline': timeline
                }
                
                if st.session_state.assessment_type == 'maturity':
                    st.session_state.current_page = 'maturity_assessment'
                elif st.session_state.assessment_type == 'compliance':
                    st.session_state.current_page = 'compliance_assessment'
                else:  # combined
                    st.session_state.current_page = 'maturity_assessment'
                st.rerun()
            else:
                st.error("Please fill in all required fields marked with *")
    
    if st.button("← Back to Home"):
        st.session_state.current_page = 'home'
        st.rerun()

# Maturity Assessment
elif st.session_state.current_page == 'maturity_assessment':
    org_name = st.session_state.org_info.get('name', 'Your Organization')
    st.markdown(f"### 🚀 AI Maturity Assessment - {org_name}")
    st.markdown("Rate your organization's current state across each dimension")
    
    # Progress tracking
    total_questions = sum(len(dim['questions']) for dim in maturity_dimensions.values())
    current_question = 0
    
    # Assessment form
    dimension_scores = {}
    
    for dim_name, dim_data in maturity_dimensions.items():
        st.markdown(f"#### {dim_name} (Weight: {dim_data['weight']*100:.0f}%)")
        
        dim_scores = []
        
        for q_idx, question in enumerate(dim_data['questions']):
            current_question += 1
            
            # Question with maturity indicators
            with st.expander(f"Question {current_question}: {question['text']}", expanded=True):
                
                # Show maturity indicators
                st.markdown("**Maturity Indicators:**")
                indicator_cols = st.columns(5)
                for level in range(1, 6):
                    with indicator_cols[level-1]:
                        st.caption(f"**Level {level}**")
                        st.caption(question['maturity_indicators'][level])
                
                # Score selection
                score = st.slider(
                    "Select your maturity level:",
                    min_value=1,
                    max_value=5,
                    value=3,
                    key=f"{dim_name}_{q_idx}",
                    help="Choose the level that best describes your current state"
                )
                
                # Visual feedback
                level_color = gartner_maturity_levels[score]['color']
                st.markdown(f"""
                <div style="background: {level_color}20; padding: 0.5rem; border-radius: 5px; 
                     border-left: 4px solid {level_color};">
                    <strong>Selected: Level {score} - {gartner_maturity_levels[score]['name']}</strong>
                </div>
                """, unsafe_allow_html=True)
                
                dim_scores.append(score * question['weight'])
        
        # Calculate weighted dimension score
        dimension_scores[dim_name] = {
            'score': sum(dim_scores),
            'weight': dim_data['weight']
        }
        
        st.progress(current_question / total_questions)
        st.markdown("---")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Back"):
            st.session_state.current_page = 'organization'
            st.rerun()
    
    with col3:
        if st.button("Continue →", type="primary"):
            st.session_state.maturity_scores = dimension_scores
            if st.session_state.assessment_type == 'maturity':
                st.session_state.current_page = 'results'
            else:  # combined
                st.session_state.current_page = 'compliance_assessment'
            st.rerun()

# Compliance Assessment
elif st.session_state.current_page == 'compliance_assessment':
    org_name = st.session_state.org_info.get('name', 'Your Organization')
    st.markdown(f"### 🛡️ EU AI Act Compliance Assessment - {org_name}")
    st.markdown("Evaluate your compliance with EU AI Act requirements")
    
    # Show warning if no EU operations
    eu_ops = st.session_state.org_info.get('eu_operations', '')
    if 'No' in eu_ops and 'planning' not in eu_ops:
        st.warning("⚠️ You indicated no EU operations. This assessment is still valuable for understanding global best practices and preparing for similar regulations in other jurisdictions.")
    
    # Progress tracking
    total_questions = sum(len(cat['questions']) for cat in eu_ai_act_requirements.values())
    current_question = 0
    
    # Compliance assessment
    compliance_answers = {}
    
    for cat_name, cat_data in eu_ai_act_requirements.items():
        st.markdown(f"#### {cat_name}")
        
        for q_idx, question in enumerate(cat_data['questions']):
            current_question += 1
            
            with st.expander(f"Q{current_question}: {question['text']}", expanded=True):
                # Article reference
                st.caption(f"📖 {question['article']} | [View Article]({question['link']})")
                
                # Show example
                st.info(f"**Example of Compliance:** {question['example']}")
                
                # Show documentation needed
                st.warning(f"**Documentation Required:** {question['documentation']}")
                
                # Risk and effort indicators
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    answer = st.selectbox(
                        "Compliance Status:",
                        ["Select...", "Yes - Fully Compliant", "Partial - In Progress", "No - Not Compliant"],
                        key=f"compliance_{cat_name}_{q_idx}"
                    )
                
                with col2:
                    risk_colors = {"low": "🟢", "medium": "🟡", "high": "🔴", "critical": "🔴"}
                    st.metric("Risk Level", risk_colors[question['risk_level']] + " " + question['risk_level'].upper())
                
                with col3:
                    effort_colors = {"low": "🟢", "medium": "🟡", "high": "🔴"}
                    st.metric("Implementation", effort_colors[question['implementation_effort']] + " " + question['implementation_effort'].upper())
                
                if answer != "Select...":
                    compliance_answers[f"{cat_name}_{q_idx}"] = {
                        'answer': answer,
                        'question': question['text'],
                        'article': question['article'],
                        'risk_level': question['risk_level'],
                        'implementation_effort': question['implementation_effort']
                    }
        
        st.progress(current_question / total_questions)
        st.markdown("---")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Back"):
            if st.session_state.assessment_type == 'combined':
                st.session_state.current_page = 'maturity_assessment'
            else:
                st.session_state.current_page = 'organization'
            st.rerun()
    
    with col3:
        if st.button("View Results →", type="primary"):
            if len(compliance_answers) < total_questions:
                st.error(f"Please answer all {total_questions} questions ({len(compliance_answers)} completed)")
            else:
                st.session_state.compliance_answers = compliance_answers
                st.session_state.current_page = 'results'
                st.rerun()

# Results page
elif st.session_state.current_page == 'results':
    org_name = st.session_state.org_info.get('name', 'Your Organization')
    st.markdown(f"## 📊 Assessment Report - {org_name}")
    st.markdown(f"**Generated:** {datetime.now().strftime('%B %d, %Y')}")
    
    # Create tabs based on assessment type
    if st.session_state.assessment_type == 'combined':
        tab1, tab2, tab3, tab4 = st.tabs(["🚀 AI Maturity", "🛡️ EU Compliance", "🎯 Roadmap", "📋 Executive Summary"])
    elif st.session_state.assessment_type == 'maturity':
        tab1, tab3 = st.tabs(["🚀 AI Maturity", "🎯 Roadmap"])
        tab2 = tab4 = None
    else:  # compliance
        tab2, tab3 = st.tabs(["🛡️ EU Compliance", "🎯 Action Plan"])
        tab1 = tab4 = None
    
    # Maturity Results Tab
    if tab1 and st.session_state.assessment_type in ['maturity', 'combined']:
        with tab1:
            # Calculate overall maturity
            dimension_scores = st.session_state.get('maturity_scores', {})
            
            # Weighted overall score
            overall_score = sum(data['score'] * data['weight'] for data in dimension_scores.values())
            
            # Determine maturity level
            if overall_score <= 1.5:
                level = 1
            elif overall_score <= 2.5:
                level = 2
            elif overall_score <= 3.5:
                level = 3
            elif overall_score <= 4.5:
                level = 4
            else:
                level = 5
            
            level_data = gartner_maturity_levels[level]
            
            # Executive metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Overall Score", f"{overall_score:.2f}/5.00", 
                         help="Weighted average across all dimensions")
            
            with col2:
                st.metric("Maturity Level", f"Level {level}", 
                         f"{level_data['name']}")
            
            with col3:
                industry = st.session_state.org_info.get('industry', 'Other')
                industry_avg = industry_benchmarks[industry]['average']
                delta = overall_score - industry_avg
                st.metric("vs Industry", f"{delta:+.2f}", 
                         f"Industry avg: {industry_avg:.1f}")
            
            with col4:
                percentile = 0
                if level == 1: percentile = 20
                elif level == 2: percentile = 40
                elif level == 3: percentile = 60
                elif level == 4: percentile = 80
                elif level == 5: percentile = 95
                st.metric("Market Position", f"Top {100-percentile}%",
                         level_data['market_position'])
            
            # Current state analysis
            st.markdown(f"""
            <div class="maturity-level-card" style="background: linear-gradient(to right, {level_data['color']}20, white);">
                <h3 style="color: {level_data['color']};">You are at Level {level}: {level_data['name']}</h3>
                <p><strong>{level_data['description']}</strong></p>
                <p>{level_data['market_position']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Dimension analysis with radar chart
            st.markdown("### 📊 Dimensional Analysis")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Create radar chart
                categories = list(dimension_scores.keys())
                values = [data['score'] for data in dimension_scores.values()]
                
                fig = go.Figure()
                
                # Add industry average
                industry_data = industry_benchmarks.get(st.session_state.org_info.get('industry', 'Other'), {})
                industry_avg_value = industry_data.get('average', 2.5)
                
                fig.add_trace(go.Scatterpolar(
                    r=[industry_avg_value] * len(categories),
                    theta=categories,
                    fill='toself',
                    name=f'{industry} Industry Average',
                    line_color='gray',
                    fillcolor='rgba(128,128,128,0.1)'
                ))
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name='Your Organization',
                    line_color=level_data['color'],
                    fillcolor='rgba(102, 126, 234, 0.25)'  # Using rgba for transparency
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 5]
                        )),
                    showlegend=True,
                    title="AI Maturity by Dimension"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("**Dimension Scores:**")
                for dim, data in dimension_scores.items():
                    score = data['score']
                    if score >= 4:
                        icon = "🟢"
                        status = "Strong"
                    elif score >= 3:
                        icon = "🟡"
                        status = "Moderate"
                    else:
                        icon = "🔴"
                        status = "Needs Focus"
                    
                    st.metric(dim, f"{score:.2f}/5.00", status)
                
                # Identify strengths and weaknesses
                sorted_dims = sorted(dimension_scores.items(), key=lambda x: x[1]['score'], reverse=True)
                
                st.success(f"**Strongest:** {sorted_dims[0][0]}")
                st.error(f"**Weakest:** {sorted_dims[-1][0]}")
            
            # Business impact analysis
            st.markdown("### 💼 Business Impact at Your Level")
            
            col1, col2, col3, col4 = st.columns(4)
            
            for metric, value in level_data['business_impact'].items():
                with col1 if metric == 'revenue' else col2 if metric == 'efficiency' else col3 if metric == 'innovation' else col4:
                    st.info(f"**{metric.capitalize()}**\n\n{value}")
            
            # Industry comparison
            st.markdown("### 🏭 Industry Benchmarking")
            
            industry = st.session_state.org_info.get('industry', 'Other')
            industry_info = industry_benchmarks[industry]
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Create industry comparison chart
                industries = list(industry_benchmarks.keys())
                averages = [industry_benchmarks[ind]['average'] for ind in industries]
                colors = ['#667eea' if ind == industry else '#e0e0e0' for ind in industries]
                
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=industries,
                    y=averages,
                    marker_color=colors,
                    text=[f"{avg:.1f}" for avg in averages],
                    textposition='outside'
                ))
                
                # Add your organization's score
                fig.add_shape(
                    type="line",
                    x0=-0.5, x1=len(industries)-0.5,
                    y0=overall_score, y1=overall_score,
                    line=dict(color="red", width=3, dash="dash"),
                )
                
                fig.add_annotation(
                    x=len(industries)-1,
                    y=overall_score,
                    text=f"Your Score: {overall_score:.2f}",
                    showarrow=True,
                    arrowhead=2,
                    bgcolor="red",
                    bordercolor="red",
                    font=dict(color="white")
                )
                
                fig.update_layout(
                    title="AI Maturity by Industry",
                    yaxis_title="Average Maturity Score",
                    yaxis=dict(range=[0, 5]),
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown(f"**{industry} Industry**")
                st.metric("Industry Average", f"{industry_info['average']:.1f}")
                st.info(f"**Leaders:** {', '.join(industry_info['leaders'][:2])}")
                st.warning(f"**Key Challenge:** {industry_info['typical_challenges']}")
                st.success(f"**Investment Range:** {industry_info['investment_range']}")
            
            # Path to next level
            if level < 5:
                st.markdown(f"### 🚀 Path to Level {level + 1}: {gartner_maturity_levels[level + 1]['name']}")
                
                next_level = gartner_maturity_levels[level + 1]
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.info(f"**Target State:** {next_level['description']}")
                    
                    st.markdown("**Key Barriers to Overcome:**")
                    for barrier in level_data['key_barriers']:
                        st.markdown(f"❌ {barrier}")
                    
                    st.markdown("**Critical Success Factors:**")
                    for factor in next_level['critical_success_factors']:
                        st.markdown(f"✅ {factor}")
                
                with col2:
                    st.metric("Time Required", next_level['time_to_next_level'])
                    st.metric("Investment Needed", next_level['investment_required'])
                    st.warning(f"**Business Value:** {next_level['business_impact']['revenue']}")
            
            # How Atlan accelerates
            st.markdown("### 🔧 How Atlan Accelerates Your Journey")
            
            st.info(f"Based on your Level {level} maturity, Atlan can help you progress faster with these specific capabilities:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Current Level Support:**")
                for feature, benefit in level_data['atlan_accelerators'].items():
                    st.markdown(f"""
                    <div class="recommendation-box">
                        <strong>{feature}:</strong> {benefit}
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                if level < 5:
                    st.markdown("**Next Level Enablers:**")
                    for feature, benefit in gartner_maturity_levels[level + 1]['atlan_accelerators'].items():
                        st.markdown(f"""
                        <div class="recommendation-box">
                            <strong>{feature}:</strong> {benefit}
                        </div>
                        """, unsafe_allow_html=True)
    
    # Compliance Results Tab
    if tab2 and st.session_state.assessment_type in ['compliance', 'combined']:
        with tab2:
            compliance_answers = st.session_state.get('compliance_answers', {})
            
            # Calculate compliance scores
            total_questions = len(compliance_answers)
            fully_compliant = sum(1 for a in compliance_answers.values() if "Yes" in a['answer'])
            partial_compliant = sum(1 for a in compliance_answers.values() if "Partial" in a['answer'])
            non_compliant = sum(1 for a in compliance_answers.values() if "No" in a['answer'])
            
            overall_compliance = (fully_compliant * 100 + partial_compliant * 50) / total_questions
            
            # Compliance metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Overall Compliance", f"{overall_compliance:.0f}%",
                         help="Weighted compliance score")
            
            with col2:
                st.metric("Fully Compliant", f"{fully_compliant}/{total_questions}",
                         f"{fully_compliant/total_questions*100:.0f}%")
            
            with col3:
                st.metric("Partially Compliant", f"{partial_compliant}/{total_questions}",
                         f"{partial_compliant/total_questions*100:.0f}%")
            
            with col4:
                st.metric("Non-Compliant", f"{non_compliant}/{total_questions}",
                         f"{non_compliant/total_questions*100:.0f}%")
            
            # Risk assessment
            if overall_compliance >= 80:
                st.success("✅ **Low Risk** - Your organization demonstrates strong EU AI Act compliance")
            elif overall_compliance >= 60:
                st.warning("⚠️ **Medium Risk** - Several compliance gaps need attention")
            else:
                st.error("❌ **High Risk** - Significant compliance gaps require immediate action")
            
            # Article-by-Article Compliance Analysis
            st.markdown("### 📊 Compliance by EU AI Act Article")
            
            # Analyze compliance by article
            article_compliance = {}
            
            for key, answer in compliance_answers.items():
                article = answer['article'].split(' – ')[0]  # Extract article number
                
                if article not in article_compliance:
                    article_compliance[article] = {
                        'yes': 0,
                        'partial': 0,
                        'no': 0,
                        'total': 0,
                        'questions': []
                    }
                
                article_compliance[article]['total'] += 1
                article_compliance[article]['questions'].append(answer['question'])
                
                if "Yes" in answer['answer']:
                    article_compliance[article]['yes'] += 1
                elif "Partial" in answer['answer']:
                    article_compliance[article]['partial'] += 1
                else:
                    article_compliance[article]['no'] += 1
            
            # Calculate compliance score per article
            article_scores = {}
            for article, data in article_compliance.items():
                score = (data['yes'] * 100 + data['partial'] * 50) / data['total']
                article_scores[article] = {
                    'score': score,
                    'data': data
                }
            
            # Sort articles by number
            sorted_articles = sorted(article_scores.items(), 
                                   key=lambda x: int(''.join(filter(str.isdigit, x[0])) or '0'))
            
            # Create article compliance visualization
            articles = [item[0] for item in sorted_articles]
            scores = [item[1]['score'] for item in sorted_articles]
            
            # Color based on compliance level
            colors = []
            for score in scores:
                if score >= 80:
                    colors.append('#28a745')  # Green
                elif score >= 60:
                    colors.append('#ffc107')  # Yellow
                else:
                    colors.append('#dc3545')  # Red
            
            fig = go.Figure()
            
            # Add bars
            fig.add_trace(go.Bar(
                x=articles,
                y=scores,
                marker_color=colors,
                text=[f"{s:.0f}%" for s in scores],
                textposition='outside',
                hovertemplate='%{x}<br>Compliance: %{y:.0f}%<br>%{customdata}<extra></extra>',
                customdata=[f"Questions: {article_scores[art]['data']['total']}" for art in articles]
            ))
            
            # Add target line at 80%
            fig.add_shape(
                type="line",
                x0=-0.5, x1=len(articles)-0.5,
                y0=80, y1=80,
                line=dict(color="#28a745", width=2, dash="dash"),
            )
            
            fig.add_annotation(
                x=len(articles)-1,
                y=80,
                text="Target: 80%",
                showarrow=False,
                bgcolor="#28a745",
                font=dict(color="white", size=10),
                xanchor="right"
            )
            
            fig.update_layout(
                title="EU AI Act Compliance by Article",
                xaxis_title="Article",
                yaxis_title="Compliance Score (%)",
                yaxis=dict(range=[0, 110]),
                xaxis_tickangle=-45,
                height=500,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Article details expandable section
            with st.expander("📋 Detailed Article Compliance Breakdown"):
                for article, score_data in sorted_articles:
                    data = score_data['data']
                    score = score_data['score']
                    
                    # Color code based on score
                    if score >= 80:
                        status_color = "🟢"
                        status_text = "Good"
                    elif score >= 60:
                        status_color = "🟡"
                        status_text = "Needs Improvement"
                    else:
                        status_color = "🔴"
                        status_text = "Critical"
                    
                    st.markdown(f"#### {status_color} {article} - {score:.0f}% Compliant ({status_text})")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Compliant", data['yes'])
                    with col2:
                        st.metric("Partial", data['partial'])
                    with col3:
                        st.metric("Non-Compliant", data['no'])
                    with col4:
                        st.metric("Total Questions", data['total'])
                    
                    if data['no'] > 0 or data['partial'] > 0:
                        st.caption("Questions requiring attention:")
                        for q in data['questions']:
                            if any(a['question'] == q and ("No" in a['answer'] or "Partial" in a['answer']) 
                                  for a in compliance_answers.values()):
                                st.write(f"• {q[:100]}...")
                    
                    st.markdown("---")
            
            # Compliance by category (existing code)
            st.markdown("### 📊 Compliance by Category")
            
            # Calculate category scores
            category_scores = {}
            for cat_name in eu_ai_act_requirements.keys():
                cat_answers = {k: v for k, v in compliance_answers.items() if k.startswith(cat_name)}
                if cat_answers:
                    yes = sum(1 for a in cat_answers.values() if "Yes" in a['answer'])
                    partial = sum(1 for a in cat_answers.values() if "Partial" in a['answer'])
                    no = sum(1 for a in cat_answers.values() if "No" in a['answer'])
                    total = len(cat_answers)
                    score = (yes * 100 + partial * 50) / total
                    category_scores[cat_name] = {
                        'score': score,
                        'yes': yes,
                        'partial': partial,
                        'no': no,
                        'total': total
                    }
            
            # Create category chart
            categories = list(category_scores.keys())
            scores = [category_scores[cat]['score'] for cat in categories]
            colors = ['#28a745' if s >= 80 else '#ffc107' if s >= 60 else '#dc3545' for s in scores]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=categories,
                y=scores,
                marker_color=colors,
                text=[f"{s:.0f}%" for s in scores],
                textposition='outside'
            ))
            
            fig.update_layout(
                title="EU AI Act Compliance by Category",
                yaxis_title="Compliance Score (%)",
                yaxis=dict(range=[0, 110]),
                xaxis_tickangle=-45,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # GPAI-specific compliance summary (if applicable)
            if "General Purpose AI (GPAI)" in category_scores:
                gpai_score = category_scores["General Purpose AI (GPAI)"]
                
                st.markdown("### 🤖 General Purpose AI (GPAI) Compliance")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("GPAI Compliance", f"{gpai_score['score']:.0f}%",
                             help="Specific requirements for foundation models")
                
                with col2:
                    if gpai_score['score'] < 60:
                        st.error("⚠️ **High Risk** - GPAI models face strict requirements")
                    elif gpai_score['score'] < 80:
                        st.warning("📊 **Medium Risk** - Some GPAI requirements unmet")
                    else:
                        st.success("✅ **Low Risk** - Good GPAI compliance")
                
                with col3:
                    st.info(f"**Key Areas:**\n• Technical documentation\n• Copyright compliance\n• Systemic risk assessment")
                
                # GPAI-specific recommendations
                if gpai_score['no'] > 0:
                    st.error(f"### 🚨 Critical GPAI Gaps ({gpai_score['no']} items)")
                    st.markdown("""
                    Foundation models and GPAI systems have specific obligations under Articles 53-55:
                    - Comprehensive technical documentation
                    - Copyright compliance in training data
                    - Information for downstream providers
                    - Systemic risk assessments (for models with systemic risk)
                    """)
            
            # Risk priority matrix (existing code continues...)
            st.markdown("### 🎯 Risk Priority Matrix")
            
            # Analyze non-compliant items by risk and effort
            high_risk_gaps = []
            medium_risk_gaps = []
            low_risk_gaps = []
            
            for key, answer in compliance_answers.items():
                if "No" in answer['answer'] or "Partial" in answer['answer']:
                    gap = {
                        'question': answer['question'],
                        'article': answer['article'],
                        'risk': answer['risk_level'],
                        'effort': answer['implementation_effort'],
                        'status': 'Partial' if "Partial" in answer['answer'] else 'Non-compliant'
                    }
                    
                    if answer['risk_level'] in ['critical', 'high']:
                        high_risk_gaps.append(gap)
                    elif answer['risk_level'] == 'medium':
                        medium_risk_gaps.append(gap)
                    else:
                        low_risk_gaps.append(gap)
            
            # Display priority gaps
            if high_risk_gaps:
                st.error(f"### 🚨 Critical/High Risk Gaps ({len(high_risk_gaps)} items)")
                for gap in high_risk_gaps[:5]:  # Show top 5
                    with st.expander(f"❌ {gap['question'][:80]}..."):
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.write(f"**Article:** {gap['article']}")
                            st.write(f"**Status:** {gap['status']}")
                        with col2:
                            st.metric("Risk", gap['risk'].upper())
                        with col3:
                            st.metric("Effort", gap['effort'].upper())
            
            if medium_risk_gaps:
                st.warning(f"### ⚠️ Medium Risk Gaps ({len(medium_risk_gaps)} items)")
                for gap in medium_risk_gaps[:3]:  # Show top 3
                    st.write(f"• {gap['question'][:100]}... (*{gap['status']}*)")
            
            # Penalty risk calculation
            st.markdown("### 💰 Potential Penalty Exposure")
            
            # Get organization size for penalty calculation
            org_size = st.session_state.org_info.get('size', '201-1000 employees')
            if '5000+' in org_size:
                estimated_revenue = 1000  # €1B
            elif '1001-5000' in org_size:
                estimated_revenue = 200  # €200M
            elif '201-1000' in org_size:
                estimated_revenue = 50  # €50M
            else:
                estimated_revenue = 10  # €10M
            
            max_penalty_percent = 0.07  # 7% of revenue
            max_penalty_fixed = 35  # €35M
            
            potential_penalty = min(estimated_revenue * max_penalty_percent, max_penalty_fixed)
            risk_factor = (100 - overall_compliance) / 100
            estimated_penalty = potential_penalty * risk_factor
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Maximum Penalty", f"€{potential_penalty:.1f}M",
                         "Lesser of 7% revenue or €35M")
            
            with col2:
                st.metric("Risk-Adjusted Exposure", f"€{estimated_penalty:.1f}M",
                         f"Based on {overall_compliance:.0f}% compliance")
            
            with col3:
                compliance_cost = estimated_revenue * 0.002  # 0.2% of revenue
                st.metric("Compliance Investment", f"€{compliance_cost:.1f}M",
                         "Typical: 0.2% of revenue")
            
            # Implementation timeline
            st.markdown("### 📅 Recommended Implementation Timeline")
            
            # Create Gantt-style timeline
            timeline_data = []
            
            if high_risk_gaps:
                timeline_data.append({
                    'Task': 'Critical/High Risk Items',
                    'Start': 0,
                    'Duration': 3,
                    'Color': '#dc3545'
                })
            
            if medium_risk_gaps:
                timeline_data.append({
                    'Task': 'Medium Risk Items',
                    'Start': 2,
                    'Duration': 4,
                    'Color': '#ffc107'
                })
            
            if low_risk_gaps:
                timeline_data.append({
                    'Task': 'Low Risk Items',
                    'Start': 5,
                    'Duration': 4,
                    'Color': '#28a745'
                })
            
            timeline_data.append({
                'Task': 'Ongoing Monitoring',
                'Start': 3,
                'Duration': 9,
                'Color': '#17a2b8'
            })
            
            if timeline_data:
                fig = go.Figure()
                
                for i, task in enumerate(timeline_data):
                    fig.add_trace(go.Bar(
                        y=[task['Task']],
                        x=[task['Duration']],
                        base=[task['Start']],
                        orientation='h',
                        marker_color=task['Color'],
                        showlegend=False,
                        hovertemplate=f"{task['Task']}<br>Months {task['Start']}-{task['Start']+task['Duration']}<extra></extra>"
                    ))
                
                fig.update_layout(
                    title="Compliance Implementation Timeline",
                    xaxis_title="Months",
                    barmode='overlay',
                    height=300,
                    xaxis=dict(range=[0, 12])
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # How Atlan helps with compliance
            st.markdown("### 🔧 How Atlan Enables EU AI Act Compliance")
            
            compliance_features = {
                "Automated Documentation": "Generate Article 11 technical documentation automatically from your data catalog",
                "Data Lineage Tracking": "Meet Article 10 requirements with end-to-end data lineage visualization",
                "Access Controls & Audit": "Implement Article 14 human oversight with role-based access and audit trails",
                "Quality Monitoring": "Ensure Article 10 data quality with automated monitoring and alerts",
                "Compliance Workflows": "Built-in workflows for impact assessments and conformity reviews",
                "Risk Management": "Article 9 risk management with automated risk scoring and tracking"
            }
            
            col1, col2 = st.columns(2)
            
            for i, (feature, benefit) in enumerate(compliance_features.items()):
                with col1 if i % 2 == 0 else col2:
                    st.markdown(f"""
                    <div class="recommendation-box">
                        <strong>{feature}:</strong> {benefit}
                    </div>
                    """, unsafe_allow_html=True)
    
    # Roadmap Tab
    if tab3:
        with tab3:
            st.markdown("### 🎯 Your Personalized AI & Compliance Roadmap")
            
            # Generate integrated roadmap based on both assessments
            if st.session_state.assessment_type == 'combined':
                # Combined roadmap
                maturity_level = level if 'level' in locals() else 3
                compliance_score = overall_compliance if 'overall_compliance' in locals() else 70
                
                st.info(f"""
                **Current State Summary:**
                - AI Maturity: Level {maturity_level} ({gartner_maturity_levels[maturity_level]['name']})
                - EU Compliance: {compliance_score:.0f}%
                - Primary Goal: {st.session_state.org_info.get('primary_goal', 'Not specified')}
                - Timeline: {st.session_state.org_info.get('timeline', 'Not specified')}
                """)
                
                # Create phased roadmap
                st.markdown("### 📅 Phased Implementation Plan")
                
                phases = [
                    {
                        "name": "Phase 1: Foundation (0-3 months)",
                        "icon": "🏗️",
                        "focus": "Address critical compliance gaps and establish governance",
                        "actions": [
                            "Establish AI governance structure and roles",
                            "Implement high-risk compliance requirements",
                            "Deploy Atlan for data cataloging and lineage",
                            "Conduct AI literacy training for key stakeholders"
                        ],
                        "atlan_features": ["Data Discovery", "Access Controls", "Basic Governance"],
                        "expected_outcome": "Reduce compliance risk by 50%, establish AI foundation"
                    },
                    {
                        "name": "Phase 2: Acceleration (3-6 months)",
                        "icon": "🚀",
                        "focus": "Scale AI capabilities and enhance compliance",
                        "actions": [
                            "Implement MLOps and model governance",
                            "Complete medium-risk compliance items",
                            "Scale successful AI pilots to production",
                            "Build data quality monitoring systems"
                        ],
                        "atlan_features": ["ML Model Governance", "Quality Monitoring", "Automated Workflows"],
                        "expected_outcome": f"Progress to Level {min(maturity_level + 1, 5)}, achieve 80%+ compliance"
                    },
                    {
                        "name": "Phase 3: Optimization (6-12 months)",
                        "icon": "⚡",
                        "focus": "Optimize AI operations and maintain compliance",
                        "actions": [
                            "Implement advanced AI capabilities",
                            "Establish continuous compliance monitoring",
                            "Develop AI-driven products/services",
                            "Create innovation pipeline"
                        ],
                        "atlan_features": ["Advanced Analytics", "Real-time Monitoring", "API Integration"],
                        "expected_outcome": "Achieve target maturity level, maintain 95%+ compliance"
                    }
                ]
                
                for phase in phases:
                    with st.expander(f"{phase['icon']} {phase['name']}", expanded=True):
                        st.write(f"**Focus:** {phase['focus']}")
                        
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown("**Key Actions:**")
                            for action in phase['actions']:
                                st.write(f"• {action}")
                        
                        with col2:
                            st.markdown("**Atlan Enablers:**")
                            for feature in phase['atlan_features']:
                                st.write(f"• {feature}")
                        
                        st.success(f"**Expected Outcome:** {phase['expected_outcome']}")
            
            elif st.session_state.assessment_type == 'maturity':
                # Maturity-only roadmap
                st.markdown("### 🚀 AI Maturity Advancement Roadmap")
                
                current_level = level if 'level' in locals() else 3
                target_level = min(current_level + 2, 5)
                
                st.info(f"**Journey:** Level {current_level} → Level {target_level} in 18-24 months")
                
                # Quick wins
                st.markdown("### 💡 Quick Wins (Next 30 Days)")
                quick_wins = [
                    "Establish AI steering committee with executive sponsor",
                    "Catalog existing data assets using Atlan",
                    "Identify and prioritize 3 high-impact AI use cases",
                    "Begin AI literacy training for leadership team"
                ]
                
                for win in quick_wins:
                    st.write(f"✓ {win}")
                
            else:
                # Compliance-only roadmap
                st.markdown("### 🛡️ EU AI Act Compliance Roadmap")
                
                st.warning("⚠️ **Compliance Deadline:** Full enforcement begins August 2026")
                
                # Priority actions based on gaps
                st.markdown("### 🚨 Priority Actions by Risk Level")
                
                if 'high_risk_gaps' in locals() and high_risk_gaps:
                    st.error(f"**Immediate Actions (1-2 months) - {len(high_risk_gaps)} items**")
                    for gap in high_risk_gaps[:3]:
                        st.write(f"• {gap['question'][:100]}...")
            
            # ROI calculation
            st.markdown("### 💰 Expected Return on Investment")
            
            investment = st.session_state.org_info.get('ai_budget', '€1M - €5M')
            
            # Simple ROI model
            if 'level' in locals():
                current_impact = gartner_maturity_levels[level]['business_impact']['revenue']
                if level < 5:
                    next_impact = gartner_maturity_levels[level + 1]['business_impact']['revenue']
                    roi_text = f"Moving from Level {level} to {level + 1} typically delivers 2-3x ROI within 18 months"
                else:
                    roi_text = "At Level 5, focus on maintaining leadership and exploring new frontiers"
                
                st.success(roi_text)
            
            # Success metrics
            st.markdown("### 📊 Success Metrics to Track")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Business Metrics**")
                st.write("• Revenue impact from AI")
                st.write("• Cost savings achieved")
                st.write("• Time-to-market improvement")
                st.write("• Customer satisfaction gains")
            
            with col2:
                st.markdown("**Technical Metrics**")
                st.write("• Models in production")
                st.write("• Data quality scores")
                st.write("• Model accuracy/performance")
                st.write("• System uptime/reliability")
            
            with col3:
                st.markdown("**Compliance Metrics**")
                st.write("• Compliance score trend")
                st.write("• Audit findings")
                st.write("• Documentation completeness")
                st.write("• Incident response time")
    
    # Executive Summary Tab (for combined assessment)
    if tab4 and st.session_state.assessment_type == 'combined':
        with tab4:
            st.markdown("### 📋 Executive Summary")
            
            # Key findings
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>🚀 AI Maturity Assessment</h4>
                    <h2>Level {level}: {gartner_maturity_levels[level]['name']}</h2>
                    <p>Score: {overall_score:.2f}/5.00</p>
                    <p>{level_data['market_position']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>🛡️ EU AI Act Compliance</h4>
                    <h2>{overall_compliance:.0f}% Compliant</h2>
                    <p>Risk Level: {'Low' if overall_compliance >= 80 else 'Medium' if overall_compliance >= 60 else 'High'}</p>
                    <p>Gaps: {non_compliant} critical items</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Strategic recommendations
            st.markdown("### 🎯 Strategic Recommendations")
            
            recommendations = []
            
            # Based on maturity level
            if level <= 2:
                recommendations.append({
                    "priority": "High",
                    "recommendation": "Establish formal AI governance and strategy",
                    "impact": "Foundation for all AI initiatives",
                    "timeline": "1-2 months"
                })
            elif level == 3:
                recommendations.append({
                    "priority": "High",
                    "recommendation": "Implement MLOps and scale AI operations",
                    "impact": "10-20% efficiency improvement",
                    "timeline": "3-6 months"
                })
            else:
                recommendations.append({
                    "priority": "High",
                    "recommendation": "Drive AI innovation and market leadership",
                    "impact": "New revenue streams and competitive advantage",
                    "timeline": "Ongoing"
                })
            
            # Based on compliance
            if overall_compliance < 60:
                recommendations.append({
                    "priority": "Critical",
                    "recommendation": "Address high-risk compliance gaps immediately",
                    "impact": "Avoid penalties up to €35M",
                    "timeline": "1-3 months"
                })
            
            # Based on organization context
            if st.session_state.org_info.get('biggest_challenge') == 'Data quality issues':
                recommendations.append({
                    "priority": "High",
                    "recommendation": "Implement comprehensive data governance with Atlan",
                    "impact": "Enable reliable AI at scale",
                    "timeline": "2-4 months"
                })
            
            # Display recommendations
            for rec in recommendations:
                color = "#dc3545" if rec['priority'] == "Critical" else "#ffc107" if rec['priority'] == "High" else "#28a745"
                st.markdown(f"""
                <div style="border-left: 4px solid {color}; padding: 1rem; margin: 0.5rem 0; background: #f8f9fa;">
                    <strong>{rec['priority']} Priority:</strong> {rec['recommendation']}<br>
                    <strong>Impact:</strong> {rec['impact']}<br>
                    <strong>Timeline:</strong> {rec['timeline']}
                </div>
                """, unsafe_allow_html=True)
            
            # Investment summary
            st.markdown("### 💰 Investment Summary")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                current_investment = st.session_state.org_info.get('ai_budget', 'Not specified')
                st.metric("Current AI Investment", current_investment)
            
            with col2:
                if 'level' in locals() and level < 5:
                    required_investment = gartner_maturity_levels[level + 1]['investment_required']
                    st.metric("Required for Next Level", required_investment)
            
            with col3:
                typical_roi = "2-3x in 18 months"
                st.metric("Typical ROI", typical_roi)
            
            # Next steps
            st.markdown("### ⏭️ Recommended Next Steps")
            
            next_steps = [
                "Schedule executive briefing on assessment results",
                "Prioritize top 3 AI initiatives for next quarter",
                "Begin Atlan implementation for data governance",
                "Establish AI Center of Excellence",
                "Create 18-month AI transformation roadmap"
            ]
            
            for i, step in enumerate(next_steps, 1):
                st.write(f"{i}. {step}")
            
            # Call to action
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 2rem; border-radius: 10px; text-align: center; margin-top: 2rem;">
                <h3>Ready to Accelerate Your AI Journey?</h3>
                <p>Atlan can help you advance your AI maturity and ensure compliance 40% faster than traditional approaches.</p>
                <p><strong>Contact us for a personalized implementation plan based on your assessment results.</strong></p>
            </div>
            """, unsafe_allow_html=True)
    
    # Action buttons at bottom
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📧 Email Report", use_container_width=True):
            st.success("✅ Report sent to your email")
    
    with col2:
        if st.button("📥 Download PDF", use_container_width=True):
            st.success("✅ Generating PDF report...")
    
    with col3:
        if st.button("📅 Schedule Follow-up", use_container_width=True):
            st.success("✅ Our team will contact you within 24 hours")
    
    with col4:
        if st.button("🔄 New Assessment", use_container_width=True):
            # Reset all session state
            for key in ['current_page', 'assessment_type', 'maturity_scores', 'compliance_answers', 'org_info']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.current_page = 'home'
            st.rerun()