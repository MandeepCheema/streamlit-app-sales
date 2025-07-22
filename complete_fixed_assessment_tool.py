import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np
import streamlit as st

# Detect current theme
import streamlit as st

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
        background: linear-gradient(135deg, #3f51b5 0%, #9c27b0 100%);
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

    .maturity-level-card {{
        background: {card_color};
        color: {text_color};
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
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
if 'ai_role' not in st.session_state:
    st.session_state.ai_role = None

# Enhanced EU AI Act Assessment - Best-in-Class
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

# Enhanced compliance scoring with proper N/A handling
def calculate_section_wise_compliance(compliance_answers, ai_role):
    """
    Calculate compliance scores by section with proper N/A handling
    """
    
    # Define section weights based on criticality
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
    
    # Initialize section scores
    section_scores = {}
    
    # Group answers by section using the section stored in the answer
    for key, answer in compliance_answers.items():
        section_name = answer.get('section', 'Other')
        
        # Initialize section if not exists
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
        
        # Count answers properly - check exact answer text
        if answer['answer'] == "Yes - Fully Compliant":
            section_scores[section_name]['yes_count'] += 1
        elif answer['answer'] == "Partial - In Progress":
            section_scores[section_name]['partial_count'] += 1
        elif answer['answer'] == "No - Not Compliant":
            section_scores[section_name]['no_count'] += 1
        elif answer['answer'] == "N/A - Not Applicable":
            section_scores[section_name]['na_count'] += 1
    
    # Calculate scores for each section
    for section_name, data in section_scores.items():
        # Calculate applicable questions (excluding N/A)
        data['applicable_questions'] = data['total_questions'] - data['na_count']
        
        if data['applicable_questions'] > 0:
            # Calculate raw score (0-100) - only for applicable questions
            data['raw_score'] = (data['yes_count'] * 100 + data['partial_count'] * 50) / data['applicable_questions']
            
            # Apply section weight
            section_weight = section_weights.get(section_name, 0.01)
            data['weighted_score'] = data['raw_score'] * section_weight
        else:
            # If all questions are N/A, section gets 100% (fully compliant)
            data['raw_score'] = 100
            data['weighted_score'] = 100 * section_weights.get(section_name, 0.01)
    
    return section_scores

def calculate_obligation_type_compliance(compliance_answers, ai_role):
    """
    Calculate compliance by obligation type with proper N/A handling
    """
    
    obligation_scores = {
        'provider': {'total': 0, 'yes': 0, 'partial': 0, 'no': 0, 'na': 0},
        'deployer': {'total': 0, 'yes': 0, 'partial': 0, 'no': 0, 'na': 0},
        'shared': {'total': 0, 'yes': 0, 'partial': 0, 'no': 0, 'na': 0}
    }
    
    for key, answer in compliance_answers.items():
        # Determine obligation type based on applicable_to
        applicable_to = answer.get('applicable_to', ['both'])
        
        if applicable_to == ['provider']:
            obligation_type = 'provider'
        elif applicable_to == ['deployer']:
            obligation_type = 'deployer'
        else:
            obligation_type = 'shared'
        
        # Count answers by type - check exact answer text
        obligation_scores[obligation_type]['total'] += 1
        
        if answer['answer'] == "Yes - Fully Compliant":
            obligation_scores[obligation_type]['yes'] += 1
        elif answer['answer'] == "Partial - In Progress":
            obligation_scores[obligation_type]['partial'] += 1
        elif answer['answer'] == "No - Not Compliant":
            obligation_scores[obligation_type]['no'] += 1
        elif answer['answer'] == "N/A - Not Applicable":
            obligation_scores[obligation_type]['na'] += 1
    
    # Calculate compliance percentages
    for obligation_type, data in obligation_scores.items():
        applicable = data['total'] - data['na']
        if applicable > 0:
            data['compliance_score'] = (data['yes'] * 100 + data['partial'] * 50) / applicable
        else:
            # If all questions are N/A, obligation type gets 100% (fully compliant)
            data['compliance_score'] = 100
        
        data['applicable_questions'] = applicable
    
    return obligation_scores

def identify_compliance_gaps(compliance_answers):
    """
    Identify compliance gaps properly excluding N/A answers
    """
    
    critical_gaps = []
    high_risk_gaps = []
    medium_risk_gaps = []
    
    for key, answer in compliance_answers.items():
        # Skip N/A answers - they are not gaps!
        if answer['answer'] == "N/A - Not Applicable":
            continue
        
        # Only consider actual non-compliance as gaps
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
        
        # Partial compliance is a gap but lower priority
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

def render_compliance_results_tab(compliance_answers, ai_role):
    """
    Render compliance results with proper N/A handling
    """
    
    # Calculate enhanced compliance scores
    section_scores = calculate_section_wise_compliance(compliance_answers, ai_role)
    obligation_scores = calculate_obligation_type_compliance(compliance_answers, ai_role)
    
    # Calculate overall compliance with proper N/A handling
    total_questions = len(compliance_answers)
    fully_compliant = sum(1 for a in compliance_answers.values() if a['answer'] == "Yes - Fully Compliant")
    partial_compliant = sum(1 for a in compliance_answers.values() if a['answer'] == "Partial - In Progress")
    non_compliant = sum(1 for a in compliance_answers.values() if a['answer'] == "No - Not Compliant")
    not_applicable = sum(1 for a in compliance_answers.values() if a['answer'] == "N/A - Not Applicable")
    
    # Adjusted calculation excluding N/A
    applicable_questions = total_questions - not_applicable
    if applicable_questions > 0:
        overall_compliance = (fully_compliant * 100 + partial_compliant * 50) / applicable_questions
    else:
        # If all questions are N/A, organization is 100% compliant
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
    
    # Compliance gaps analysis - FIXED
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
    else:
        st.success("✅ **No High-Risk Gaps** - Strong compliance across major requirements!")
    
    if medium_risk_gaps:
        st.info(f"### 📝 Medium Risk Items to Address ({len(medium_risk_gaps)} items)")
        for gap in medium_risk_gaps[:3]:  # Show top 3
            st.write(f"• {gap['question'][:100]}... (*{gap['status']}*)")
    
    # Overall assessment
    total_gaps = len(critical_gaps) + len(high_risk_gaps) + len(medium_risk_gaps)
    if total_gaps == 0:
        st.balloons()
        st.success("🎉 **Excellent!** No compliance gaps identified. Your organization demonstrates strong EU AI Act compliance.")
    else:
        st.info(f"📊 **Summary:** {total_gaps} total gaps identified across {len(section_scores)} sections. Focus on critical and high-risk items first.")
    
    return section_scores, obligation_scores

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
                    <li>60+ compliance questions</li>
                    <li>Provider/Deployer specific</li>
                    <li>Article mapping</li>
                    <li>20-30 minutes</li>
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
                    <li>35-45 minutes</li>
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
            <h4>🚨 EU AI Act Enforcement Begins 2026</h4>
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

# Compliance Assessment with Provider/Deployer segregation
elif st.session_state.current_page == 'compliance_assessment':
    org_name = st.session_state.org_info.get('name', 'Your Organization')
    st.markdown(f"### 🛡️ EU AI Act Compliance Assessment - {org_name}")
    st.markdown("Evaluate your compliance with EU AI Act requirements")
    
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
    
    # Compliance Results Tab with Provider/Deployer analysis
    if tab2 and st.session_state.assessment_type in ['compliance', 'combined']:
        with tab2:
            compliance_answers = st.session_state.get('compliance_answers', {})
            ai_role = st.session_state.get('ai_role', 'both')
            
            # Role-specific header
            role_display = {
                "provider": "AI Provider",
                "deployer": "AI Deployer",
                "both": "Both Provider and Deployer"
            }
            
            st.markdown(f"### Your Role: {role_display[ai_role]}")
            
            if not compliance_answers:
                st.warning("No compliance answers found. Please complete the assessment first.")
            else:
                # Use the fixed compliance results renderer
                section_scores, obligation_scores = render_compliance_results_tab(compliance_answers, ai_role)
                
                # Role-specific compliance breakdown
                st.markdown("### 📊 Compliance by Obligation Type")
                
                if ai_role == "both":
                    # Show breakdown for both roles
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        provider_score = obligation_scores['provider']['compliance_score']
                        provider_applicable = obligation_scores['provider']['applicable_questions']
                        provider_total = obligation_scores['provider']['total']
                        
                        st.metric("Provider Obligations", f"{provider_score:.0f}%",
                                 f"{provider_applicable}/{provider_total} applicable")
                    
                    with col2:
                        deployer_score = obligation_scores['deployer']['compliance_score']
                        deployer_applicable = obligation_scores['deployer']['applicable_questions']
                        deployer_total = obligation_scores['deployer']['total']
                        
                        st.metric("Deployer Obligations", f"{deployer_score:.0f}%",
                                 f"{deployer_applicable}/{deployer_total} applicable")
                    
                    with col3:
                        shared_score = obligation_scores['shared']['compliance_score']
                        shared_applicable = obligation_scores['shared']['applicable_questions']
                        shared_total = obligation_scores['shared']['total']
                        
                        st.metric("Shared Obligations", f"{shared_score:.0f}%",
                                 f"{shared_applicable}/{shared_total} applicable")
                    
                    # Visualization
                    fig = go.Figure()
                    
                    categories = ['Provider Obligations', 'Deployer Obligations', 'Shared Obligations']
                    scores = [provider_score, deployer_score, shared_score]
                    colors = ['#667eea', '#42a5f5', '#66bb6a']
                    
                    fig.add_trace(go.Bar(
                        x=categories,
                        y=scores,
                        marker_color=colors,
                        text=[f"{s:.0f}%" for s in scores],
                        textposition='outside',
                        hovertemplate='%{x}<br>Compliance: %{y:.0f}%<extra></extra>'
                    ))
                    
                    fig.update_layout(
                        title="Compliance by Obligation Type",
                        yaxis_title="Compliance Score (%)",
                        yaxis=dict(range=[0, 110]),
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                elif ai_role == "provider":
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        provider_score = obligation_scores['provider']['compliance_score']
                        provider_applicable = obligation_scores['provider']['applicable_questions']
                        provider_total = obligation_scores['provider']['total']
                        st.metric("Provider Obligations", f"{provider_score:.0f}%",
                                 f"{provider_applicable}/{provider_total} applicable")
                    
                    with col2:
                        shared_score = obligation_scores['shared']['compliance_score']
                        shared_applicable = obligation_scores['shared']['applicable_questions']
                        shared_total = obligation_scores['shared']['total']
                        st.metric("Shared Obligations", f"{shared_score:.0f}%",
                                 f"{shared_applicable}/{shared_total} applicable")
                
                else:  # deployer
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        deployer_score = obligation_scores['deployer']['compliance_score']
                        deployer_applicable = obligation_scores['deployer']['applicable_questions']
                        deployer_total = obligation_scores['deployer']['total']
                        st.metric("Deployer Obligations", f"{deployer_score:.0f}%",
                                 f"{deployer_applicable}/{deployer_total} applicable")
                    
                    with col2:
                        shared_score = obligation_scores['shared']['compliance_score']
                        shared_applicable = obligation_scores['shared']['applicable_questions']
                        shared_total = obligation_scores['shared']['total']
                        st.metric("Shared Obligations", f"{shared_score:.0f}%",
                                 f"{shared_applicable}/{shared_total} applicable")
                
                # Penalty calculation - adjusted for N/A
                st.markdown("### 💰 Potential Penalty Exposure")
                
                # Calculate applicable questions for penalty assessment
                total_questions = len(compliance_answers)
                not_applicable = sum(1 for a in compliance_answers.values() if a['answer'] == "N/A - Not Applicable")
                applicable_questions = total_questions - not_applicable
                
                if applicable_questions > 0:
                    non_compliant = sum(1 for a in compliance_answers.values() if a['answer'] == "No - Not Compliant")
                    overall_compliance = (sum(1 for a in compliance_answers.values() if a['answer'] == "Yes - Fully Compliant") * 100 + 
                                        sum(1 for a in compliance_answers.values() if a['answer'] == "Partial - In Progress") * 50) / applicable_questions
                else:
                    non_compliant = 0
                    overall_compliance = 100
                
                # Different penalty structures for providers vs deployers
                org_size = st.session_state.org_info.get('size', '201-1000 employees')
                if '5000+' in org_size:
                    estimated_revenue = 1000  # €1B
                elif '1001-5000' in org_size:
                    estimated_revenue = 200  # €200M
                elif '201-1000' in org_size:
                    estimated_revenue = 50  # €50M
                else:
                    estimated_revenue = 10  # €10M
                
                if ai_role == "provider":
                    st.info("**Providers face higher penalties** for non-compliance as they bear primary responsibility for AI system safety and compliance")
                    max_penalty_percent = 0.07  # 7% of revenue
                    max_penalty_fixed = 35  # €35M
                elif ai_role == "deployer":
                    st.info("**Deployers face penalties** primarily for misuse or failure to implement required oversight")
                    max_penalty_percent = 0.03  # 3% of revenue (lower than providers)
                    max_penalty_fixed = 20  # €20M
                else:
                    st.warning("**Dual exposure** - As both provider and deployer, you face penalties on both fronts")
                    max_penalty_percent = 0.07  # Maximum exposure
                    max_penalty_fixed = 35  # €35M
                
                potential_penalty = min(estimated_revenue * max_penalty_percent, max_penalty_fixed)
                risk_factor = (100 - overall_compliance) / 100
                estimated_penalty = potential_penalty * risk_factor
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Maximum Penalty", f"€{potential_penalty:.1f}M",
                             f"As {role_display[ai_role]}")
                
                with col2:
                    st.metric("Risk-Adjusted Exposure", f"€{estimated_penalty:.1f}M",
                             f"Based on {overall_compliance:.0f}% compliance")
                
                with col3:
                    compliance_cost = estimated_revenue * 0.002  # 0.2% of revenue
                    st.metric("Compliance Investment", f"€{compliance_cost:.1f}M",
                             "Typical: 0.2% of revenue")
                
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
                
                if 'critical_gaps' in locals() and len(identify_compliance_gaps(compliance_answers)[0]) > 0:
                    critical_gaps = identify_compliance_gaps(compliance_answers)[0]
                    st.error(f"**Immediate Actions (1-2 months) - {len(critical_gaps)} items**")
                    for gap in critical_gaps[:3]:
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
                # Calculate overall compliance for executive summary
                if 'compliance_answers' in st.session_state and st.session_state.compliance_answers:
                    compliance_answers = st.session_state.compliance_answers
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
                        non_compliant = 0
                else:
                    overall_compliance = 0
                    non_compliant = 0
                
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
            for key in ['current_page', 'assessment_type', 'maturity_scores', 'compliance_answers', 'org_info', 'ai_role']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.current_page = 'home'
            st.rerun()