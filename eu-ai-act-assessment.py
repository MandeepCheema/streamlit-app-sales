import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np
import base64

# Detect theme and dynamically set CSS
theme_base = st.get_option("theme.base")
is_dark = theme_base == "dark"

# Define colors based on theme
background_color = "#0e1117" if is_dark else "#ffffff"
text_color = "#f0f2f6" if is_dark else "#000000"
card_color = "#1e1e24" if is_dark else "#f8f9fa"
secondary_background = "#2a2d36" if is_dark else "#e9ecef"

# Inject theme-aware CSS
st.markdown(f"""
<style>
    html, body, [class*="css"] {{
        color: {text_color};
        background-color: {background_color};
    }}

    .main-header {{
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }}

    .metric-card {{
        background: {card_color};
        color: {text_color};
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        text-align: center;
        height: 100%;
        transition: transform 0.3s ease;
    }}

    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }}

    .recommendation-box {{
        background: {secondary_background};
        border-left: 4px solid #42a5f5;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }}

    .warning-box {{
        background: #fff3cd;
        color: #856404;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}

    .success-box {{
        background: #d4edda;
        color: #155724;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}

    .error-box {{
        background: #f8d7da;
        color: #721c24;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}

    .compliance-example {{
        background: rgba(100, 181, 246, 0.15);
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        font-style: italic;
        color: {text_color};
    }}

    .documentation-note {{
        background: rgba(255, 152, 0, 0.15);
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border-left: 3px solid #ff9800;
        color: {text_color};
    }}

    .stProgress > div > div > div > div {{
        background-color: #42a5f5;
    }}
</style>
""", unsafe_allow_html=True)

# Page config
st.set_page_config(
    page_title="EU AI Act Compliance Assessment",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'compliance_answers' not in st.session_state:
    st.session_state.compliance_answers = {}
if 'org_info' not in st.session_state:
    st.session_state.org_info = {}
if 'ai_role' not in st.session_state:
    st.session_state.ai_role = None

# Enhanced EU AI Act Assessment
eu_ai_act_requirements = {
    "Role Identification": {
        "questions": [
            {
                "text": "What is your organization's primary role in the AI value chain?",
                "type": "role_selection",
                "options": ["Provider (develop/supply AI systems)", "Deployer (use AI systems)", "Both Provider and Deployer"],
                "article": "Article 3 – Definitions",
                "link": "https://artificialintelligenceact.eu/article/3/",
                "example": "Provider: Company developing facial recognition software. Deployer: Bank using third-party AI for credit scoring. Both: Tech company using own AI internally and selling to others.",
                "documentation": "Organization role definition matrix, AI system inventory with provider/deployer designation, contractual agreements defining responsibilities.",
                "risk_level": "critical",
                "implementation_effort": "low",
                "applicable_to": ["both"]
            }
        ]
    },
    
    "AI System Classification & Risk Assessment": {
        "questions": [
            {
                "text": "Do you develop or deploy AI systems in high-risk categories (Annex III)?",
                "article": "Article 6 – Classification rules for high-risk AI systems",
                "link": "https://artificialintelligenceact.eu/article/6/",
                "example": "High-risk: CV screening for hiring, credit scoring, medical diagnosis, autonomous vehicles, biometric identification, critical infrastructure management, law enforcement tools.",
                "documentation": "AI system classification matrix, risk assessment reports, Annex III compliance checklist, legal analysis of system categorization.",
                "risk_level": "critical",
                "implementation_effort": "medium",
                "applicable_to": ["both"]
            },
            {
                "text": "Are your AI systems used for biometric identification or categorization?",
                "article": "Article 3 – Definitions & Annex III",
                "link": "https://artificialintelligenceact.eu/article/3/",
                "example": "Facial recognition for access control, emotion detection in interviews, age verification systems, voice identification for authentication, iris scanning for border control.",
                "documentation": "Biometric processing inventory, technical specifications, lawful basis documentation, accuracy test results, demographic bias assessments.",
                "risk_level": "critical",
                "implementation_effort": "low",
                "applicable_to": ["both"]
            },
            {
                "text": "Do you use AI for employment, education, or social benefit decisions?",
                "article": "Annex III - High-risk AI systems",
                "link": "https://artificialintelligenceact.eu/annex/3/",
                "example": "Automated CV screening, performance evaluation algorithms, student assessment systems, social benefit eligibility determination, promotion recommendation systems.",
                "documentation": "Decision-making process documentation, algorithmic impact assessments, human oversight procedures, appeal mechanisms, fairness audits.",
                "risk_level": "high",
                "implementation_effort": "low",
                "applicable_to": ["both"]
            },
            {
                "text": "Are your AI systems used in critical infrastructure or public safety?",
                "article": "Annex III - High-risk AI systems",
                "link": "https://artificialintelligenceact.eu/annex/3/",
                "example": "Traffic management systems, power grid optimization, water treatment control, emergency response coordination, predictive maintenance for critical systems.",
                "documentation": "Safety certification documents, redundancy procedures, failure mode analysis, emergency response protocols, regulatory compliance certificates.",
                "risk_level": "critical",
                "implementation_effort": "low",
                "applicable_to": ["both"]
            },
            {
                "text": "Have you conducted a comprehensive AI risk assessment for your systems?",
                "article": "Article 9 – Risk management system",
                "link": "https://artificialintelligenceact.eu/article/9/",
                "example": "ISO 31000-based risk framework covering: technical risks, operational risks, ethical risks, legal risks, with quantitative risk scores and mitigation strategies.",
                "documentation": "Risk assessment methodology, risk registers, mitigation plans, monitoring procedures, regular review schedules, escalation matrices.",
                "risk_level": "high",
                "implementation_effort": "high",
                "applicable_to": ["both"]
            }
        ]
    },
    
    "Prohibited AI Practices": {
        "questions": [
            {
                "text": "Do you use AI for social scoring of natural persons?",
                "article": "Article 5 – Prohibited AI practices",
                "link": "https://artificialintelligenceact.eu/article/5/",
                "example": "PROHIBITED: Social credit systems, citizen scoring based on behavior, trustworthiness ratings for individuals, social compliance monitoring systems.",
                "documentation": "System purpose documentation, use case definitions, legal compliance verification, alternative approaches documentation.",
                "risk_level": "critical",
                "implementation_effort": "low",
                "applicable_to": ["both"]
            },
            {
                "text": "Do you use real-time biometric identification in publicly accessible spaces?",
                "article": "Article 5 – Prohibited AI practices",
                "link": "https://artificialintelligenceact.eu/article/5/",
                "example": "PROHIBITED: Real-time facial recognition in shopping malls, airports, public transport (except specific law enforcement exceptions with authorization).",
                "documentation": "System deployment locations, real-time processing capabilities, public space definitions, law enforcement authorization status.",
                "risk_level": "critical",
                "implementation_effort": "low",
                "applicable_to": ["both"]
            },
            {
                "text": "Do you deploy AI systems using subliminal techniques or exploiting vulnerabilities?",
                "article": "Article 5 – Prohibited AI practices",
                "link": "https://artificialintelligenceact.eu/article/5/",
                "example": "PROHIBITED: Subliminal advertising, AI targeting children's vulnerabilities, systems exploiting mental health conditions, manipulation through dark patterns.",
                "documentation": "System design documentation, target audience analysis, ethical review reports, vulnerability exploitation assessments.",
                "risk_level": "critical",
                "implementation_effort": "low",
                "applicable_to": ["both"]
            },
            {
                "text": "Do you use AI to infer emotions in workplace or educational settings?",
                "article": "Article 5 – Prohibited AI practices",
                "link": "https://artificialintelligenceact.eu/article/5/",
                "example": "PROHIBITED: Employee mood monitoring, student attention tracking, workplace stress detection (except safety/medical purposes with explicit consent).",
                "documentation": "Use case documentation, consent mechanisms, purpose limitation measures, data minimization protocols, alternative approaches.",
                "risk_level": "high",
                "implementation_effort": "low",
                "applicable_to": ["both"]
            }
        ]
    },
    
    "High-Risk AI System Requirements": {
        "questions": [
            {
                "text": "Do you have a comprehensive quality management system for high-risk AI?",
                "article": "Article 17 – Quality management system",
                "link": "https://artificialintelligenceact.eu/article/17/",
                "example": "ISO 9001-certified QMS with AI-specific modules: development lifecycle procedures, testing protocols, change management, version control, documentation standards, responsibility matrices.",
                "documentation": "QMS manual, process procedures, audit reports, certification documents, continuous improvement records, management review minutes.",
                "risk_level": "critical",
                "implementation_effort": "high",
                "applicable_to": ["provider"]
            },
            {
                "text": "Are your high-risk AI systems designed with appropriate human oversight?",
                "article": "Article 14 – Human oversight",
                "link": "https://artificialintelligenceact.eu/article/14/",
                "example": "Built-in human-in-the-loop controls: manual override capabilities, confidence threshold alerts, decision explanation features, escalation procedures, audit trail logging.",
                "documentation": "Human oversight design specifications, user interface documentation, training materials, oversight procedures, effectiveness monitoring reports.",
                "risk_level": "critical",
                "implementation_effort": "high",
                "applicable_to": ["both"]
            },
            {
                "text": "Do you conduct pre-deployment fundamental rights impact assessments?",
                "article": "Article 27 – Fundamental rights impact assessment",
                "link": "https://artificialintelligenceact.eu/article/27/",
                "example": "DPIA+ assessment covering: discrimination risks, privacy impacts, freedom of expression, human dignity, children's rights, with stakeholder consultation and mitigation measures.",
                "documentation": "Impact assessment reports, stakeholder consultation records, mitigation strategies, monitoring plans, regular review schedules.",
                "risk_level": "critical",
                "implementation_effort": "high",
                "applicable_to": ["deployer"]
            },
            {
                "text": "Do you register high-risk AI systems in the EU database before deployment?",
                "article": "Article 60 – EU database for high-risk AI systems",
                "link": "https://artificialintelligenceact.eu/article/60/",
                "example": "Complete registration with system details, intended use, risk mitigation measures, contact information, updates for substantial modifications.",
                "documentation": "Database registration confirmations, system descriptions, update logs, notification procedures, compliance tracking records.",
                "risk_level": "high",
                "implementation_effort": "low",
                "applicable_to": ["both"]
            }
        ]
    },
    
    "Provider Obligations - Design & Development": {
        "questions": [
            {
                "text": "Do you implement accuracy, robustness and cybersecurity measures during development?",
                "article": "Article 15 – Accuracy, robustness and cybersecurity",
                "link": "https://artificialintelligenceact.eu/article/15/",
                "example": "Accuracy targets >95%, adversarial robustness testing, secure coding practices OWASP Top 10, penetration testing, encryption at rest/transit, regular security updates.",
                "documentation": "Performance benchmarks, security test reports, vulnerability assessments, penetration test results, update logs, incident response procedures.",
                "risk_level": "critical",
                "implementation_effort": "high",
                "applicable_to": ["provider"]
            },
            {
                "text": "Do you maintain comprehensive technical documentation (Article 11)?",
                "article": "Article 11 – Technical documentation",
                "link": "https://artificialintelligenceact.eu/article/11/",
                "example": "Complete technical file: system architecture, algorithm descriptions, training data specifications, performance metrics, risk assessments, all version-controlled and accessible.",
                "documentation": "Technical documentation package per Annex IV, version control systems, document management procedures, access control logs.",
                "risk_level": "critical",
                "implementation_effort": "high",
                "applicable_to": ["provider"]
            },
            {
                "text": "Do you have procedures for assessing substantial modifications?",
                "article": "Article 43 – Conformity assessment",
                "link": "https://artificialintelligenceact.eu/article/43/",
                "example": "Defined thresholds for substantial modifications, impact assessment procedures, re-conformity assessment triggers, documentation update requirements.",
                "documentation": "Modification assessment procedures, thresholds documentation, impact assessment templates, re-assessment records.",
                "risk_level": "high",
                "implementation_effort": "medium",
                "applicable_to": ["provider"]
            },
            {
                "text": "Do you have an authorized representative in the EU (if non-EU provider)?",
                "article": "Article 25 – Authorized representatives",
                "link": "https://artificialintelligenceact.eu/article/25/",
                "example": "EU-based legal entity with written mandate, technical competence, ability to cooperate with authorities, complete documentation access.",
                "documentation": "Authorization agreements, representative contact details, competence assessments, cooperation procedures, documentation access rights.",
                "risk_level": "high",
                "implementation_effort": "low",
                "applicable_to": ["provider"]
            },
            {
                "text": "Do you provide clear, comprehensive instructions for use?",
                "article": "Article 13 – Instructions for use",
                "link": "https://artificialintelligenceact.eu/article/13/",
                "example": "User manuals in all relevant EU languages, intended purpose clearly stated, contraindications, technical requirements, maintenance procedures, troubleshooting guides.",
                "documentation": "User manuals, training materials, technical specifications, safety warnings, maintenance schedules, multi-language versions.",
                "risk_level": "medium",
                "implementation_effort": "medium",
                "applicable_to": ["provider"]
            }
        ]
    },
    
    "Provider Obligations - Market Placement & Post-Market": {
        "questions": [
            {
                "text": "Do you conduct proper conformity assessment before market placement?",
                "article": "Article 43 – Conformity assessment",
                "link": "https://artificialintelligenceact.eu/article/43/",
                "example": "Internal assessment for most high-risk systems, third-party assessment for biometric/emotion recognition, comprehensive testing against harmonized standards.",
                "documentation": "Conformity assessment procedures, test protocols, assessment reports, third-party certificates where required, non-conformity records.",
                "risk_level": "critical",
                "implementation_effort": "high",
                "applicable_to": ["provider"]
            },
            {
                "text": "Do you properly affix CE marking and issue Declaration of Conformity?",
                "article": "Article 48 – CE marking & Article 47 – Declaration of Conformity",
                "link": "https://artificialintelligenceact.eu/article/48/",
                "example": "CE marking affixed after successful conformity assessment, Declaration of Conformity signed by authorized person, technical file maintained, notified body involvement documented.",
                "documentation": "CE marking procedures, Declaration of Conformity documents, technical files, authorized signatory records, notified body certificates.",
                "risk_level": "critical",
                "implementation_effort": "medium",
                "applicable_to": ["provider"]
            },
            {
                "text": "Do you have effective post-market monitoring systems?",
                "article": "Article 61 – Post-market monitoring by providers",
                "link": "https://artificialintelligenceact.eu/article/61/",
                "example": "Systematic data collection from deployers, performance monitoring dashboards, incident tracking systems, trend analysis, regular review cycles with documented actions.",
                "documentation": "Monitoring plan, data collection procedures, performance reports, incident logs, trend analysis reports, corrective action records.",
                "risk_level": "high",
                "implementation_effort": "high",
                "applicable_to": ["provider"]
            },
            {
                "text": "Do you have established corrective action and recall procedures?",
                "article": "Article 21 – Corrective actions",
                "link": "https://artificialintelligenceact.eu/article/21/",
                "example": "24-hour incident response team, root cause analysis procedures, corrective action implementation, effectiveness verification, market withdrawal protocols if needed.",
                "documentation": "Incident response procedures, corrective action templates, effectiveness verification protocols, withdrawal procedures, communication plans.",
                "risk_level": "high",
                "implementation_effort": "medium",
                "applicable_to": ["provider"]
            },
            {
                "text": "Do you report serious incidents to competent authorities?",
                "article": "Article 62 – Reporting of serious incidents",
                "link": "https://artificialintelligenceact.eu/article/62/",
                "example": "Immediate reporting of deaths, serious injuries, fundamental rights violations, with detailed incident analysis, corrective actions, and prevention measures.",
                "documentation": "Incident reporting procedures, authority contact databases, report templates, acknowledgment records, follow-up correspondence.",
                "risk_level": "critical",
                "implementation_effort": "low",
                "applicable_to": ["provider"]
            }
        ]
    },
    
    "Deployer Obligations - Pre-Deployment Assessment": {
        "questions": [
            {
                "text": "Do you verify provider compliance before deploying high-risk AI systems?",
                "article": "Article 26 – Obligations of deployers",
                "link": "https://artificialintelligenceact.eu/article/26/",
                "example": "Verification checklist: CE marking present, Declaration of Conformity valid, technical documentation reviewed, provider registration confirmed, instructions for use complete.",
                "documentation": "Verification procedures, compliance checklists, provider documentation reviews, registration confirmations, due diligence records.",
                "risk_level": "high",
                "implementation_effort": "medium",
                "applicable_to": ["deployer"]
            },
            {
                "text": "Have you assessed compatibility with your existing systems and processes?",
                "article": "Article 26 – Obligations of deployers",
                "link": "https://artificialintelligenceact.eu/article/26/",
                "example": "Technical compatibility testing, process integration analysis, data flow mapping, security assessment, user training needs analysis, change management planning.",
                "documentation": "Compatibility assessment reports, integration test results, security evaluations, training plans, change management documentation.",
                "risk_level": "medium",
                "implementation_effort": "medium",
                "applicable_to": ["deployer"]
            },
            {
                "text": "Do you conduct fundamental rights impact assessments before deployment?",
                "article": "Article 27 – Fundamental rights impact assessment",
                "link": "https://artificialintelligenceact.eu/article/27/",
                "example": "Comprehensive FRIA covering: affected individuals, potential discriminatory impacts, privacy implications, consultation with affected groups, mitigation measures, monitoring plans.",
                "documentation": "Impact assessment reports, stakeholder consultation records, mitigation strategies, monitoring procedures, regular review schedules.",
                "risk_level": "critical",
                "implementation_effort": "high",
                "applicable_to": ["deployer"]
            },
            {
                "text": "Have you established appropriate human oversight for deployment?",
                "article": "Article 26 – Obligations of deployers",
                "link": "https://artificialintelligenceact.eu/article/26/",
                "example": "Designated trained operators, clear oversight responsibilities, intervention authority, regular supervision schedules, performance monitoring, escalation procedures.",
                "documentation": "Oversight procedures, operator assignments, training records, supervision logs, intervention protocols, performance monitoring reports.",
                "risk_level": "critical",
                "implementation_effort": "medium",
                "applicable_to": ["deployer"]
            }
        ]
    },
    
    "Deployer Obligations - Operational Management": {
        "questions": [
            {
                "text": "Do you use AI systems strictly according to provider instructions?",
                "article": "Article 26 – Obligations of deployers",
                "link": "https://artificialintelligenceact.eu/article/26/",
                "example": "Strict adherence to intended use cases, operating within specified parameters, no unauthorized modifications, compliance with usage restrictions, regular compliance audits.",
                "documentation": "Usage policies, compliance checklists, audit reports, training records, violation reporting procedures, corrective action logs.",
                "risk_level": "high",
                "implementation_effort": "low",
                "applicable_to": ["deployer"]
            },
            {
                "text": "Do you maintain required logs and monitor system operation?",
                "article": "Article 26 – Obligations of deployers",
                "link": "https://artificialintelligenceact.eu/article/26/",
                "example": "Automated logging enabled, logs retained for required periods, secure storage with access controls, regular log analysis, performance monitoring dashboards.",
                "documentation": "Log retention policies, storage procedures, access control systems, analysis reports, monitoring dashboards, security measures.",
                "risk_level": "medium",
                "implementation_effort": "medium",
                "applicable_to": ["deployer"]
            },
            {
                "text": "Do you ensure input data quality and relevance?",
                "article": "Article 26 – Obligations of deployers",
                "link": "https://artificialintelligenceact.eu/article/26/",
                "example": "Data validation procedures, quality metrics monitoring, relevance checks, data refresh protocols, bias monitoring, accuracy verification before processing.",
                "documentation": "Data quality procedures, validation rules, monitoring reports, refresh schedules, bias assessments, accuracy metrics.",
                "risk_level": "high",
                "implementation_effort": "medium",
                "applicable_to": ["deployer"]
            },
            {
                "text": "Do you report serious incidents to providers and authorities?",
                "article": "Article 26 – Obligations of deployers",
                "link": "https://artificialintelligenceact.eu/article/26/",
                "example": "Immediate incident reporting within 24 hours, detailed incident documentation, provider notification, authority reporting where required, corrective action coordination.",
                "documentation": "Incident reporting procedures, notification templates, authority contact information, communication logs, corrective action coordination.",
                "risk_level": "high",
                "implementation_effort": "low",
                "applicable_to": ["deployer"]
            },
            {
                "text": "Do you have procedures for suspending or withdrawing AI systems?",
                "article": "Article 26 – Obligations of deployers",
                "link": "https://artificialintelligenceact.eu/article/26/",
                "example": "Clear suspension criteria, emergency shutdown procedures, alternative process activation, stakeholder notification, incident documentation, restart authorization procedures.",
                "documentation": "Suspension procedures, shutdown protocols, alternative processes, notification procedures, incident documentation, restart authorization.",
                "risk_level": "medium",
                "implementation_effort": "medium",
                "applicable_to": ["deployer"]
            }
        ]
    },
    
    "Shared Obligations - Governance & Risk Management": {
        "questions": [
            {
                "text": "Do you have a comprehensive AI risk management system?",
                "article": "Article 9 – Risk management system",
                "link": "https://artificialintelligenceact.eu/article/9/",
                "example": "ISO 31000-based framework with AI-specific risk categories: technical, operational, ethical, legal risks, with quantitative scoring, continuous monitoring, regular updates.",
                "documentation": "Risk management framework, risk registers, assessment procedures, mitigation strategies, monitoring systems, regular review schedules.",
                "risk_level": "critical",
                "implementation_effort": "high",
                "applicable_to": ["both"]
            },
            {
                "text": "Do you conduct regular testing for safety and performance?",
                "article": "Article 9 – Risk management system",
                "link": "https://artificialintelligenceact.eu/article/9/",
                "example": "Comprehensive test suites covering edge cases, stress testing, safety scenarios, performance benchmarks, regression testing, adversarial testing.",
                "documentation": "Test plans, test results, performance benchmarks, safety assessments, regression test logs, adversarial testing reports.",
                "risk_level": "high",
                "implementation_effort": "high",
                "applicable_to": ["both"]
            },
            {
                "text": "Do you assess risks to health, safety and fundamental rights?",
                "article": "Article 9 – Risk management system",
                "link": "https://artificialintelligenceact.eu/article/9/",
                "example": "Systematic assessment using EU Charter of Fundamental Rights, health and safety standards, expert consultations, public input, vulnerable group considerations.",
                "documentation": "Rights impact assessments, health and safety analyses, expert consultations, public consultation records, vulnerability assessments.",
                "risk_level": "critical",
                "implementation_effort": "high",
                "applicable_to": ["both"]
            },
            {
                "text": "Do you have incident management and business continuity procedures?",
                "article": "Article 9 – Risk management system",
                "link": "https://artificialintelligenceact.eu/article/9/",
                "example": "24/7 incident response team, escalation procedures, business continuity plans, disaster recovery protocols, communication plans, lessons learned processes.",
                "documentation": "Incident response procedures, business continuity plans, disaster recovery protocols, communication plans, training records, exercise reports.",
                "risk_level": "high",
                "implementation_effort": "medium",
                "applicable_to": ["both"]
            },
            {
                "text": "Do you have clear roles and responsibilities for AI governance?",
                "article": "Article 17 – Quality management system",
                "link": "https://artificialintelligenceact.eu/article/17/",
                "example": "RACI matrix for AI activities, designated AI officers, clear reporting lines, decision-making authority, accountability measures, regular governance reviews.",
                "documentation": "Governance framework, role definitions, responsibility matrices, reporting structures, accountability measures, governance review minutes.",
                "risk_level": "medium",
                "implementation_effort": "medium",
                "applicable_to": ["both"]
            }
        ]
    },
    
    "Shared Obligations - Data & Transparency": {
        "questions": [
            {
                "text": "Are training/input datasets quality-controlled and bias-tested?",
                "article": "Article 10 – Data and data governance",
                "link": "https://artificialintelligenceact.eu/article/10/",
                "example": "Multi-stage QA: automated quality checks, statistical bias analysis across protected characteristics, manual reviews, 99.5% quality threshold, regular re-assessment.",
                "documentation": "Data quality standards, QA procedures, bias testing protocols, quality metrics, assessment reports, remediation records.",
                "risk_level": "critical",
                "implementation_effort": "high",
                "applicable_to": ["both"]
            },
            {
                "text": "Do you maintain complete data lineage and provenance tracking?",
                "article": "Article 10 – Data and data governance",
                "link": "https://artificialintelligenceact.eu/article/10/",
                "example": "End-to-end lineage from source systems through all transformations to model training/inference, automated tools, visual lineage maps, impact analysis capabilities.",
                "documentation": "Data lineage documentation, lineage mapping tools, data flow diagrams, impact analysis reports, change tracking systems.",
                "risk_level": "high",
                "implementation_effort": "high",
                "applicable_to": ["both"]
            },
            {
                "text": "Are personal data processing activities compliant with GDPR?",
                "article": "Article 10 – Data and data governance",
                "link": "https://artificialintelligenceact.eu/article/10/",
                "example": "Legal basis documented for all processing, DPIAs completed, consent mechanisms implemented, data minimization applied, DPO consulted, retention limits enforced.",
                "documentation": "GDPR compliance documentation, legal basis analysis, DPIAs, consent records, data minimization procedures, retention schedules.",
                "risk_level": "critical",
                "implementation_effort": "high",
                "applicable_to": ["both"]
            },
            {
                "text": "Do you ensure datasets are representative and free from harmful biases?",
                "article": "Article 10 – Data and data governance",
                "link": "https://artificialintelligenceact.eu/article/10/",
                "example": "Statistical representation analysis across demographics, bias testing for protected characteristics, external bias audits, remediation strategies, ongoing monitoring.",
                "documentation": "Representation analysis, demographic studies, bias audit reports, remediation plans, monitoring procedures, external validation.",
                "risk_level": "critical",
                "implementation_effort": "high",
                "applicable_to": ["both"]
            },
            {
                "text": "Are users clearly informed about AI system interactions?",
                "article": "Article 52 – Transparency obligations",
                "link": "https://artificialintelligenceact.eu/article/52/",
                "example": "Clear AI disclosure badges, transparency notices in user interfaces, plain language explanations, opt-out mechanisms, decision explanation capabilities.",
                "documentation": "Transparency notices, user interface guidelines, communication templates, opt-out procedures, explanation mechanisms.",
                "risk_level": "medium",
                "implementation_effort": "medium",
                "applicable_to": ["both"]
            }
        ]
    },
    
    "General Purpose AI (GPAI) - Enhanced Coverage": {
        "questions": [
            {
                "text": "Do you develop general-purpose AI models (foundation models)?",
                "article": "Article 3 – Definitions",
                "link": "https://artificialintelligenceact.eu/article/3/",
                "example": "Large language models (LLMs), multimodal models, diffusion models, foundation models adaptable for multiple downstream tasks (GPT-style, Claude-style, etc.).",
                "documentation": "Model specifications, capability assessments, intended use documentation, downstream application analysis.",
                "risk_level": "critical",
                "implementation_effort": "low",
                "applicable_to": ["provider"]
            },
            {
                "text": "Do you maintain comprehensive technical documentation for GPAI models?",
                "article": "Article 53 – Obligations for providers of GPAI models",
                "link": "https://artificialintelligenceact.eu/article/53/",
                "example": "Complete technical documentation: model architecture (transformer, parameters), training process (data, compute, duration), capabilities, limitations, safety measures, performance metrics.",
                "documentation": "Technical specifications, training documentation, capability assessments, limitation disclosures, safety documentation, performance benchmarks.",
                "risk_level": "high",
                "implementation_effort": "high",
                "applicable_to": ["provider"]
            },
            {
                "text": "Have you implemented copyright-compliant training data policies?",
                "article": "Article 53 – Obligations for providers of GPAI models",
                "link": "https://artificialintelligenceact.eu/article/53/",
                "example": "Comprehensive copyright policy: automated content filtering, licensing agreements, creator opt-out mechanisms, fair use analysis, legal compliance verification.",
                "documentation": "Copyright compliance policies, data filtering procedures, licensing agreements, opt-out mechanisms, legal compliance audits.",
                "risk_level": "critical",
                "implementation_effort": "high",
                "applicable_to": ["provider"]
            },
            {
                "text": "Do you conduct systemic risk assessments for high-capability models?",
                "article": "Article 55 – Obligations for GPAI models with systemic risk",
                "link": "https://artificialintelligenceact.eu/article/55/",
                "example": "Comprehensive risk assessment: misuse potential analysis, societal impact evaluation, dual-use risk assessment, adversarial testing, expert consultations.",
                "documentation": "Risk assessment reports, expert consultations, adversarial testing results, societal impact studies, mitigation strategies.",
                "risk_level": "critical",
                "implementation_effort": "high",
                "applicable_to": ["provider"]
            },
            {
                "text": "Have you implemented safeguards against systemic risks?",
                "article": "Article 55 – Obligations for GPAI models with systemic risk",
                "link": "https://artificialintelligenceact.eu/article/55/",
                "example": "Multi-layered safeguards: content filtering, usage monitoring, access controls, incident response, model behavior monitoring, emergency shutdown capabilities.",
                "documentation": "Safeguard implementations, monitoring systems, access controls, incident response procedures, emergency protocols.",
                "risk_level": "critical",
                "implementation_effort": "high",
                "applicable_to": ["provider"]
            },
            {
                "text": "Do you provide adequate information to downstream deployers?",
                "article": "Article 53 – Obligations for providers of GPAI models",
                "link": "https://artificialintelligenceact.eu/article/53/",
                "example": "Comprehensive downstream support: API documentation, model cards, safety guidelines, usage restrictions, compliance guidance, technical support.",
                "documentation": "API documentation, model cards, safety guidelines, usage policies, compliance guidance, support procedures.",
                "risk_level": "medium",
                "implementation_effort": "medium",
                "applicable_to": ["provider"]
            },
            {
                "text": "Do you track and monitor downstream high-risk applications?",
                "article": "Article 53 – Obligations for providers of GPAI models",
                "link": "https://artificialintelligenceact.eu/article/53/",
                "example": "Downstream monitoring: customer registration, use case tracking, high-risk application identification, compliance verification, usage restriction enforcement.",
                "documentation": "Customer registration systems, use case tracking, compliance monitoring, restriction enforcement procedures.",
                "risk_level": "high",
                "implementation_effort": "medium",
                "applicable_to": ["provider"]
            }
        ]
    },
    
    "Cross-Border & Regulatory Interaction": {
        "questions": [
            {
                "text": "Do you cooperate with market surveillance authorities?",
                "article": "Article 63 – Market surveillance and control",
                "link": "https://artificialintelligenceact.eu/article/63/",
                "example": "Designated authority contacts, document provision procedures, inspection readiness, compliance demonstration capabilities, corrective action implementation.",
                "documentation": "Authority cooperation procedures, contact databases, inspection protocols, compliance packages, corrective action procedures.",
                "risk_level": "high",
                "implementation_effort": "low",
                "applicable_to": ["both"]
            },
            {
                "text": "Do you have procedures for handling regulatory inquiries and investigations?",
                "article": "Article 63 – Market surveillance and control",
                "link": "https://artificialintelligenceact.eu/article/63/",
                "example": "Legal response team, document preservation procedures, privilege protection, regulatory communication protocols, investigation cooperation procedures.",
                "documentation": "Legal response procedures, document preservation policies, communication protocols, cooperation procedures, privilege protection measures.",
                "risk_level": "medium",
                "implementation_effort": "medium",
                "applicable_to": ["both"]
            },
            {
                "text": "Are you prepared for cross-border regulatory coordination?",
                "article": "Article 63 – Market surveillance and control",
                "link": "https://artificialintelligenceact.eu/article/63/",
                "example": "Multi-jurisdiction compliance tracking, regulatory coordination procedures, information sharing agreements, consistent compliance approaches across borders.",
                "documentation": "Multi-jurisdiction compliance procedures, coordination protocols, information sharing agreements, compliance tracking systems.",
                "risk_level": "medium",
                "implementation_effort": "medium",
                "applicable_to": ["both"]
            }
        ]
    }
}

def generate_html_report(org_info, compliance_answers, ai_role, section_scores, obligation_scores):
    """Generate HTML report for download"""
    
    # Calculate overall compliance
    total_questions = len(compliance_answers)
    not_applicable = sum(1 for a in compliance_answers.values() if a['answer'] == "N/A - Not Applicable")
    applicable_questions = total_questions - not_applicable
    
    if applicable_questions > 0:
        fully_compliant = sum(1 for a in compliance_answers.values() if a['answer'] == "Yes - Fully Compliant")
        partial_compliant = sum(1 for a in compliance_answers.values() if a['answer'] == "Partial - In Progress")
        non_compliant = sum(1 for a in compliance_answers.values() if a['answer'] == "No - Not Compliant")
        overall_compliance = (fully_compliant * 100 + partial_compliant * 50) / applicable_questions
    else:
        overall_compliance = 100
        fully_compliant = partial_compliant = non_compliant = 0
    
    role_display = {
        "provider": "AI Provider",
        "deployer": "AI Deployer",
        "both": "Both Provider and Deployer"
    }
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>EU AI Act Compliance Report - {org_info.get('name', 'Organization')}</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 20px;
                background: #f5f5f5;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
                border-radius: 10px;
            }}
            h1 {{
                color: #1e3c72;
                border-bottom: 3px solid #1e3c72;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #2a5298;
                margin-top: 30px;
            }}
            h3 {{
                color: #333;
                margin-top: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 30px;
            }}
            .metrics {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }}
            .metric {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                border-left: 4px solid #2a5298;
            }}
            .metric-value {{
                font-size: 2em;
                font-weight: bold;
                color: #1e3c72;
            }}
            .metric-label {{
                color: #666;
                margin-top: 5px;
            }}
            .status-badge {{
                display: inline-block;
                padding: 5px 15px;
                border-radius: 20px;
                font-weight: bold;
                margin: 5px;
            }}
            .status-compliant {{
                background: #d4edda;
                color: #155724;
            }}
            .status-partial {{
                background: #fff3cd;
                color: #856404;
            }}
            .status-non-compliant {{
                background: #f8d7da;
                color: #721c24;
            }}
            .status-na {{
                background: #e7e7e7;
                color: #666;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th {{
                background: #f8f9fa;
                color: #333;
                padding: 12px;
                text-align: left;
                border-bottom: 2px solid #dee2e6;
            }}
            td {{
                padding: 12px;
                border-bottom: 1px solid #dee2e6;
            }}
            .risk-critical {{
                color: #dc3545;
                font-weight: bold;
            }}
            .risk-high {{
                color: #fd7e14;
                font-weight: bold;
            }}
            .risk-medium {{
                color: #ffc107;
                font-weight: bold;
            }}
            .risk-low {{
                color: #28a745;
                font-weight: bold;
            }}
            .section {{
                margin: 30px 0;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
            }}
            .footer {{
                margin-top: 50px;
                padding-top: 20px;
                border-top: 1px solid #dee2e6;
                color: #666;
                text-align: center;
            }}
            @media print {{
                body {{
                    background: white;
                }}
                .container {{
                    box-shadow: none;
                    padding: 20px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>EU AI Act Compliance Assessment Report</h1>
                <p style="font-size: 1.2em;">{org_info.get('name', 'Organization')}</p>
                <p>Generated: {datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            
            <div class="section">
                <h2>Executive Summary</h2>
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-value">{overall_compliance:.0f}%</div>
                        <div class="metric-label">Overall Compliance</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{applicable_questions}</div>
                        <div class="metric-label">Applicable Questions</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{fully_compliant}</div>
                        <div class="metric-label">Fully Compliant</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{non_compliant}</div>
                        <div class="metric-label">Non-Compliant</div>
                    </div>
                </div>
                
                <h3>Organization Profile</h3>
                <table>
                    <tr><td><strong>Organization:</strong></td><td>{org_info.get('name', 'N/A')}</td></tr>
                    <tr><td><strong>Industry:</strong></td><td>{org_info.get('industry', 'N/A')}</td></tr>
                    <tr><td><strong>Size:</strong></td><td>{org_info.get('size', 'N/A')}</td></tr>
                    <tr><td><strong>AI Role:</strong></td><td>{role_display[ai_role]}</td></tr>
                    <tr><td><strong>EU Operations:</strong></td><td>{org_info.get('eu_operations', 'N/A')}</td></tr>
                    <tr><td><strong>Current AI State:</strong></td><td>{org_info.get('ai_state', 'N/A')}</td></tr>
                </table>
            </div>
            
            <div class="section">
                <h2>Compliance by Section</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Section</th>
                            <th>Score</th>
                            <th>Applicable</th>
                            <th>Compliant</th>
                            <th>Partial</th>
                            <th>Non-Compliant</th>
                            <th>N/A</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    # Add section scores to HTML
    for section_name, data in section_scores.items():
        if data['total_questions'] > 0:
            html_content += f"""
                        <tr>
                            <td>{section_name}</td>
                            <td><strong>{data['raw_score']:.0f}%</strong></td>
                            <td>{data['applicable_questions']}/{data['total_questions']}</td>
                            <td>{data['yes_count']}</td>
                            <td>{data['partial_count']}</td>
                            <td>{data['no_count']}</td>
                            <td>{data['na_count']}</td>
                        </tr>
            """
    
    html_content += """
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h2>Detailed Assessment Results</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Question</th>
                            <th>Article</th>
                            <th>Status</th>
                            <th>Risk Level</th>
                            <th>Implementation Effort</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    # Add detailed results
    for key, answer in compliance_answers.items():
        status_class = {
            "Yes - Fully Compliant": "status-compliant",
            "Partial - In Progress": "status-partial",
            "No - Not Compliant": "status-non-compliant",
            "N/A - Not Applicable": "status-na"
        }.get(answer['answer'], '')
        
        risk_class = f"risk-{answer['risk_level']}"
        
        html_content += f"""
                        <tr>
                            <td>{answer['question'][:100]}...</td>
                            <td>{answer['article']}</td>
                            <td><span class="status-badge {status_class}">{answer['answer'].split(' - ')[1]}</span></td>
                            <td class="{risk_class}">{answer['risk_level'].upper()}</td>
                            <td>{answer['implementation_effort'].upper()}</td>
                        </tr>
        """
    
    html_content += f"""
                    </tbody>
                </table>
            </div>
            
            <div class="footer">
                <p>This report is generated based on the EU AI Act compliance assessment completed on {datetime.now().strftime('%B %d, %Y')}.</p>
                <p>For the latest requirements and guidance, please refer to the official EU AI Act documentation.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

def calculate_section_wise_compliance(compliance_answers, ai_role):
    """Calculate compliance scores by section with proper N/A handling"""
    
    section_weights = {
        "Role Identification": 0.05,
        "AI System Classification & Risk Assessment": 0.15,
        "Prohibited AI Practices": 0.20,
        "High-Risk AI System Requirements": 0.15,
        "Provider Obligations - Design & Development": 0.10,
        "Provider Obligations - Market Placement & Post-Market": 0.10,
        "Deployer Obligations - Pre-Deployment Assessment": 0.08,
        "Deployer Obligations - Operational Management": 0.07,
        "Shared Obligations - Governance & Risk Management": 0.05,
        "Shared Obligations - Data & Transparency": 0.03,
        "General Purpose AI (GPAI) - Enhanced Coverage": 0.02,
        "Cross-Border & Regulatory Interaction": 0.01
    }
    
    section_scores = {}
    
    for key, answer in compliance_answers.items():
        section_name = answer.get('section', 'Other')
        
        if section_name not in section_scores:
            section_scores[section_name] = {
                'total_questions': 0,
                'yes_count': 0,
                'partial_count': 0,
                'no_count': 0,
                'na_count': 0,
                'applicable_questions': 0,
                'weighted_score': 0,
                'raw_score': 0
            }
        
        section_scores[section_name]['total_questions'] += 1
        
        if answer['answer'] == "Yes - Fully Compliant":
            section_scores[section_name]['yes_count'] += 1
        elif answer['answer'] == "Partial - In Progress":
            section_scores[section_name]['partial_count'] += 1
        elif answer['answer'] == "No - Not Compliant":
            section_scores[section_name]['no_count'] += 1
        elif answer['answer'] == "N/A - Not Applicable":
            section_scores[section_name]['na_count'] += 1
    
    for section_name, data in section_scores.items():
        data['applicable_questions'] = data['total_questions'] - data['na_count']
        
        if data['applicable_questions'] > 0:
            data['raw_score'] = (data['yes_count'] * 100 + data['partial_count'] * 50) / data['applicable_questions']
            section_weight = section_weights.get(section_name, 0.01)
            data['weighted_score'] = data['raw_score'] * section_weight
        else:
            data['raw_score'] = 100
            data['weighted_score'] = 100 * section_weights.get(section_name, 0.01)
    
    return section_scores

def calculate_obligation_type_compliance(compliance_answers, ai_role):
    """Calculate compliance by obligation type with proper N/A handling"""
    
    obligation_scores = {
        'provider': {'total': 0, 'yes': 0, 'partial': 0, 'no': 0, 'na': 0},
        'deployer': {'total': 0, 'yes': 0, 'partial': 0, 'no': 0, 'na': 0},
        'shared': {'total': 0, 'yes': 0, 'partial': 0, 'no': 0, 'na': 0}
    }
    
    for key, answer in compliance_answers.items():
        applicable_to = answer.get('applicable_to', ['both'])
        
        if applicable_to == ['provider']:
            obligation_type = 'provider'
        elif applicable_to == ['deployer']:
            obligation_type = 'deployer'
        else:
            obligation_type = 'shared'
        
        obligation_scores[obligation_type]['total'] += 1
        
        if answer['answer'] == "Yes - Fully Compliant":
            obligation_scores[obligation_type]['yes'] += 1
        elif answer['answer'] == "Partial - In Progress":
            obligation_scores[obligation_type]['partial'] += 1
        elif answer['answer'] == "No - Not Compliant":
            obligation_scores[obligation_type]['no'] += 1
        elif answer['answer'] == "N/A - Not Applicable":
            obligation_scores[obligation_type]['na'] += 1
    
    for obligation_type, data in obligation_scores.items():
        applicable = data['total'] - data['na']
        if applicable > 0:
            data['compliance_score'] = (data['yes'] * 100 + data['partial'] * 50) / applicable
        else:
            data['compliance_score'] = 100
        
        data['applicable_questions'] = applicable
    
    return obligation_scores

def identify_compliance_gaps(compliance_answers):
    """Identify compliance gaps properly excluding N/A answers"""
    
    critical_gaps = []
    high_risk_gaps = []
    medium_risk_gaps = []
    
    for key, answer in compliance_answers.items():
        if answer['answer'] == "N/A - Not Applicable":
            continue
        
        if answer['answer'] == "No - Not Compliant":
            gap = {
                'question': answer['question'],
                'article': answer['article'],
                'risk': answer['risk_level'],
                'effort': answer['implementation_effort'],
                'status': 'Non-compliant',
                'applicable_to': answer.get('applicable_to', ['both']),
                'section': answer.get('section', 'Other')
            }
            
            if answer['risk_level'] == 'critical':
                critical_gaps.append(gap)
            elif answer['risk_level'] == 'high':
                high_risk_gaps.append(gap)
            elif answer['risk_level'] == 'medium':
                medium_risk_gaps.append(gap)
        
        elif answer['answer'] == "Partial - In Progress":
            gap = {
                'question': answer['question'],
                'article': answer['article'],
                'risk': answer['risk_level'],
                'effort': answer['implementation_effort'],
                'status': 'Partial compliance',
                'applicable_to': answer.get('applicable_to', ['both']),
                'section': answer.get('section', 'Other')
            }
            
            if answer['risk_level'] == 'critical':
                critical_gaps.append(gap)
            elif answer['risk_level'] == 'high':
                high_risk_gaps.append(gap)
            elif answer['risk_level'] == 'medium':
                medium_risk_gaps.append(gap)
    
    return critical_gaps, high_risk_gaps, medium_risk_gaps

# Home page with organization form
if st.session_state.current_page == 'home':
    st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 2.5rem; margin: 0;">🛡️ EU AI Act Compliance Assessment</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">
            Evaluate your organization's compliance with the EU AI Act requirements
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key information
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Maximum Penalties", "€35M", "or 7% of revenue")
    with col2:
        st.metric("Enforcement Begins", "August 2026", "Full compliance required")
    with col3:
        st.metric("Assessment Questions", "60+", "Comprehensive coverage")
    
    st.markdown("---")
    st.markdown("### 📋 Organization Information")
    st.markdown("Please provide your organization details to generate a customized assessment")
    
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
            eu_operations = st.selectbox("EU Operations? *",
                ["Select...", "Yes - Primary market", "Yes - Secondary market", 
                 "No - But planning to enter", "No - No EU presence"])
            timeline = st.selectbox("Compliance Timeline",
                ["Select...", "Immediate (< 3 months)", "Short-term (3-6 months)", 
                 "Medium-term (6-12 months)", "Long-term (> 12 months)"])
        
        submitted = st.form_submit_button("Start Assessment →", type="primary", use_container_width=True)
        
        if submitted:
            required_fields = [org_name, industry, org_size, ai_state, eu_operations]
            if all(field and field != "Select..." for field in required_fields):
                st.session_state.org_info = {
                    'name': org_name,
                    'industry': industry,
                    'size': org_size,
                    'geography': geography,
                    'ai_state': ai_state,
                    'ai_budget': ai_budget,
                    'eu_operations': eu_operations,
                    'timeline': timeline
                }
                st.session_state.current_page = 'compliance_assessment'
                st.rerun()
            else:
                st.error("Please fill in all required fields marked with *")
    
    # Information sections
    st.markdown("---")
    st.markdown("### 📚 About the EU AI Act")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="warning-box">
            <h4>⚠️ Why Compliance Matters</h4>
            <ul>
                <li>Avoid penalties up to €35M or 7% of annual revenue</li>
                <li>Maintain access to EU markets</li>
                <li>Build trust with customers and partners</li>
                <li>Demonstrate responsible AI practices</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-box">
            <h4>✅ Assessment Coverage</h4>
            <ul>
                <li>Article-by-article compliance check</li>
                <li>Provider and deployer specific requirements</li>
                <li>Risk-based prioritization</li>
                <li>Implementation guidance and examples</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Compliance Assessment
elif st.session_state.current_page == 'compliance_assessment':
    org_name = st.session_state.org_info.get('name', 'Your Organization')
    st.markdown(f"### 🛡️ EU AI Act Compliance Assessment - {org_name}")
    
    # First, determine the organization's role if not already set
    if st.session_state.ai_role is None:
        st.info("### 🎭 First, let's identify your role in the AI value chain")
        
        role = st.radio(
            "What is your organization's primary role?",
            [
                "AI Provider - We develop and/or supply AI systems to others",
                "AI Deployer - We use AI systems developed by others", 
                "Both - We develop AI systems and also use third-party AI"
            ],
            help="This determines which EU AI Act obligations apply to your organization"
        )
        
        if st.button("Continue with selected role", type="primary"):
            if role.startswith("AI Provider"):
                st.session_state.ai_role = "provider"
            elif role.startswith("AI Deployer"):
                st.session_state.ai_role = "deployer"
            else:
                st.session_state.ai_role = "both"
            st.rerun()
    
    else:
        # Display role-specific assessment
        role_display = {
            "provider": "AI Provider",
            "deployer": "AI Deployer", 
            "both": "Both Provider and Deployer"
        }
        
        st.success(f"**Your Role:** {role_display[st.session_state.ai_role]}")
        
        # Show warning if no EU operations
        eu_ops = st.session_state.org_info.get('eu_operations', '')
        if 'No' in eu_ops and 'planning' not in eu_ops:
            st.warning("⚠️ You indicated no EU operations. This assessment is still valuable for understanding global best practices and preparing for similar regulations in other jurisdictions.")
        
        # Filter questions based on role
        applicable_categories = {}
        total_questions = 0
        
        for cat_name, cat_data in eu_ai_act_requirements.items():
            applicable_questions = []
            for question in cat_data['questions']:
                if st.session_state.ai_role in question['applicable_to'] or 'both' in question['applicable_to']:
                    applicable_questions.append(question)
            
            if applicable_questions:
                applicable_categories[cat_name] = {
                    'questions': applicable_questions
                }
                total_questions += len(applicable_questions)
        
        # Progress tracking
        current_question = 0
        
        # Show role-specific guidance
        if st.session_state.ai_role == "provider":
            st.info("""
            **📋 As an AI Provider, you are responsible for:**
            - Ensuring AI systems meet safety and performance requirements
            - Providing technical documentation and instructions
            - Conducting conformity assessments
            - Post-market monitoring and corrective actions
            """)
        elif st.session_state.ai_role == "deployer":
            st.info("""
            **📋 As an AI Deployer, you are responsible for:**
            - Using AI systems according to provider instructions
            - Ensuring appropriate human oversight
            - Monitoring system operation and maintaining logs
            - Conducting fundamental rights impact assessments
            """)
        else:
            st.info("""
            **📋 As both Provider and Deployer, you have dual responsibilities:**
            - All provider obligations for systems you develop
            - All deployer obligations for systems you use
            - Enhanced coordination between development and deployment teams
            """)
        
        # Compliance assessment with proper question keys
        compliance_answers = {}
        
        for cat_name, cat_data in applicable_categories.items():
            # Add role indicator to category name
            role_indicator = ""
            if "Provider" in cat_name and "Deployer" not in cat_name:
                role_indicator = " 🏭"
            elif "Deployer" in cat_name and "Provider" not in cat_name:
                role_indicator = " 🏢"
            elif "Shared" in cat_name:
                role_indicator = " 🤝"
                
            st.markdown(f"#### {cat_name}{role_indicator}")
            
            for q_idx, question in enumerate(cat_data['questions']):
                current_question += 1
                
                with st.expander(f"Q{current_question}: {question['text']}", expanded=True):
                    # Show which role this applies to
                    if len(question['applicable_to']) == 1 and question['applicable_to'][0] != 'both':
                        role_tag = "🏭 Provider Only" if question['applicable_to'][0] == 'provider' else "🏢 Deployer Only"
                        st.caption(f"**{role_tag}**")
                    elif 'both' in question['applicable_to']:
                        st.caption("**🤝 Applies to Both Providers and Deployers**")
                    
                    # Article reference
                    st.caption(f"📖 {question['article']} | [View Article]({question['link']})")
                    
                    # Show example
                    st.info(f"**Example of Compliance:** {question['example']}")
                    
                    # Show documentation needed
                    st.warning(f"**Documentation Required:** {question['documentation']}")
                    
                    # Risk and effort indicators
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        # Create unique key for each question
                        question_key = f"{cat_name}_{q_idx}"
                        
                        answer = st.selectbox(
                            "Compliance Status:",
                            ["Select...", "Yes - Fully Compliant", "Partial - In Progress", 
                             "No - Not Compliant", "N/A - Not Applicable"],
                            key=f"compliance_{question_key}"
                        )
                    
                    with col2:
                        risk_colors = {"low": "🟢", "medium": "🟡", "high": "🔴", "critical": "🔴"}
                        st.metric("Risk Level", risk_colors[question['risk_level']] + " " + question['risk_level'].upper())
                    
                    with col3:
                        effort_colors = {"low": "🟢", "medium": "🟡", "high": "🔴"}
                        st.metric("Implementation", effort_colors[question['implementation_effort']] + " " + question['implementation_effort'].upper())
                    
                    if answer != "Select...":
                        # Store answer with proper categorization
                        compliance_answers[question_key] = {
                            'answer': answer,
                            'question': question['text'],
                            'article': question['article'],
                            'risk_level': question['risk_level'],
                            'implementation_effort': question['implementation_effort'],
                            'applicable_to': question['applicable_to'],
                            'section': cat_name  # Add section name for easier categorization
                        }
            
            st.progress(current_question / total_questions)
            st.markdown("---")
        
        # Add role change option
        if st.button("🔄 Change Role Selection"):
            st.session_state.ai_role = None
            st.rerun()
        
        # Navigation
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("← Back"):
                st.session_state.current_page = 'home'
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
    st.markdown(f"## 📊 Compliance Report - {org_name}")
    st.markdown(f"**Generated:** {datetime.now().strftime('%B %d, %Y')}")
    
    compliance_answers = st.session_state.get('compliance_answers', {})
    ai_role = st.session_state.get('ai_role', 'both')
    
    if not compliance_answers:
        st.warning("No compliance answers found. Please complete the assessment first.")
    else:
        # Calculate compliance scores
        section_scores = calculate_section_wise_compliance(compliance_answers, ai_role)
        obligation_scores = calculate_obligation_type_compliance(compliance_answers, ai_role)
        
        # Calculate overall compliance
        total_questions = len(compliance_answers)
        fully_compliant = sum(1 for a in compliance_answers.values() if a['answer'] == "Yes - Fully Compliant")
        partial_compliant = sum(1 for a in compliance_answers.values() if a['answer'] == "Partial - In Progress")
        non_compliant = sum(1 for a in compliance_answers.values() if a['answer'] == "No - Not Compliant")
        not_applicable = sum(1 for a in compliance_answers.values() if a['answer'] == "N/A - Not Applicable")
        
        applicable_questions = total_questions - not_applicable
        if applicable_questions > 0:
            overall_compliance = (fully_compliant * 100 + partial_compliant * 50) / applicable_questions
        else:
            overall_compliance = 100
        
        # Display metrics
        st.markdown("### 📊 Compliance Overview")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Overall Compliance", f"{overall_compliance:.0f}%",
                     help="Compliance score excluding N/A questions")
        
        with col2:
            if applicable_questions > 0:
                fully_rate = f"{fully_compliant/applicable_questions*100:.0f}%"
            else:
                fully_rate = "100%"
            st.metric("Fully Compliant", f"{fully_compliant}/{applicable_questions}", fully_rate)
        
        with col3:
            if applicable_questions > 0:
                partial_rate = f"{partial_compliant/applicable_questions*100:.0f}%"
            else:
                partial_rate = "0%"
            st.metric("Partially Compliant", f"{partial_compliant}/{applicable_questions}", partial_rate)
        
        with col4:
            if applicable_questions > 0:
                non_rate = f"{non_compliant/applicable_questions*100:.0f}%"
            else:
                non_rate = "0%"
            st.metric("Non-Compliant", f"{non_compliant}/{applicable_questions}", non_rate)
        
        with col5:
            na_rate = f"{not_applicable/total_questions*100:.0f}%"
            st.metric("Not Applicable", f"{not_applicable}/{total_questions}", na_rate)
        
        # Risk assessment
        if overall_compliance >= 80:
            st.success(f"✅ **Low Risk** - Strong EU AI Act compliance ({applicable_questions} applicable questions)")
        elif overall_compliance >= 60:
            st.warning(f"⚠️ **Medium Risk** - Some compliance gaps need attention ({applicable_questions} applicable questions)")
        else:
            st.error(f"❌ **High Risk** - Significant compliance gaps require immediate action ({applicable_questions} applicable questions)")
        
        # Show N/A summary if applicable
        if not_applicable > 0:
            st.info(f"📝 **Note:** {not_applicable} questions marked as Not Applicable are excluded from compliance scoring. This is normal and indicates proper assessment of your organization's specific context.")
        
        # Section-wise analysis
        st.markdown("### 📊 Compliance by Section")
        
        # Create section compliance table
        section_data = []
        for section_name, data in section_scores.items():
            if data['total_questions'] > 0:
                section_data.append({
                    'Section': section_name,
                    'Score': f"{data['raw_score']:.0f}%",
                    'Applicable': f"{data['applicable_questions']}/{data['total_questions']}",
                    'Fully Compliant': data['yes_count'],
                    'Partial': data['partial_count'],
                    'Non-Compliant': data['no_count'],
                    'N/A': data['na_count']
                })
        
        if section_data:
            # Sort by score descending
            section_data.sort(key=lambda x: float(x['Score'].replace('%', '')), reverse=True)
            
            # Display table
            df = pd.DataFrame(section_data)
            st.dataframe(df, use_container_width=True)
            
            # Visualization
            fig = go.Figure()
            
            sections = [item['Section'] for item in section_data]
            scores = [float(item['Score'].replace('%', '')) for item in section_data]
            
            # Color code by score
            colors = []
            for score in scores:
                if score >= 80:
                    colors.append('#28a745')  # Green
                elif score >= 60:
                    colors.append('#ffc107')  # Yellow
                else:
                    colors.append('#dc3545')  # Red
            
            fig.add_trace(go.Bar(
                x=sections,
                y=scores,
                marker_color=colors,
                text=[f"{s:.0f}%" for s in scores],
                textposition='outside',
                hovertemplate='%{x}<br>Compliance: %{y:.0f}%<extra></extra>'
            ))
            
            # Add target line at 80%
            fig.add_shape(
                type="line",
                x0=-0.5, x1=len(sections)-0.5,
                y0=80, y1=80,
                line=dict(color="#28a745", width=2, dash="dash"),
            )
            
            fig.update_layout(
                title="EU AI Act Compliance by Section",
                xaxis_title="Section",
                yaxis_title="Compliance Score (%)",
                yaxis=dict(range=[0, 110]),
                xaxis_tickangle=-45,
                height=600,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Compliance gaps analysis
        st.markdown("### 🚨 Compliance Gaps Analysis")
        
        critical_gaps, high_risk_gaps, medium_risk_gaps = identify_compliance_gaps(compliance_answers)
        
        if critical_gaps:
            st.error(f"### 🚨 Critical Gaps Requiring Immediate Action ({len(critical_gaps)} items)")
            for gap in critical_gaps[:5]:  # Show top 5
                with st.expander(f"❌ {gap['question'][:80]}...", expanded=True):
                    st.error(f"**Risk Level:** {gap['risk'].upper()}")
                    st.write(f"**Article:** {gap['article']}")
                    st.write(f"**Status:** {gap['status']}")
                    st.write(f"**Section:** {gap['section']}")
                    role_text = "Provider" if gap['applicable_to'] == ['provider'] else "Deployer" if gap['applicable_to'] == ['deployer'] else "Both"
                    st.write(f"**Applies to:** {role_text}")
        else:
            st.success("✅ **No Critical Gaps** - Excellent compliance in high-risk areas!")
        
        if high_risk_gaps:
            st.warning(f"### ⚠️ High Risk Gaps Needing Attention ({len(high_risk_gaps)} items)")
            for gap in high_risk_gaps[:3]:  # Show top 3
                st.write(f"• {gap['question'][:100]}... (*{gap['status']}*)")
        
        # Download Report Button
        st.markdown("---")
        st.markdown("### 💾 Download Report")
        
        # Generate HTML report
        html_report = generate_html_report(
            st.session_state.org_info,
            compliance_answers,
            ai_role,
            section_scores,
            obligation_scores
        )
        
        # Create download button
        b64 = base64.b64encode(html_report.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="EU_AI_Act_Compliance_Report_{org_name}_{datetime.now().strftime("%Y%m%d")}.html">📥 Download Complete HTML Report</a>'
        st.markdown(href, unsafe_allow_html=True)
        
        # Action buttons
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 New Assessment", use_container_width=True):
                # Reset all session state
                for key in ['current_page', 'compliance_answers', 'org_info', 'ai_role']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.session_state.current_page = 'home'
                st.rerun()
        
        with col2:
            if st.button("📝 Edit Responses", use_container_width=True):
                st.session_state.current_page = 'compliance_assessment'
                st.rerun()