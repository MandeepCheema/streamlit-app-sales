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

# Configure Plotly default theme for dark mode compatibility
import plotly.io as pio

# Set default plotly theme
plotly_template = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "#ffffff"},
        "xaxis": {"gridcolor": "rgba(128,128,128,0.2)"},
        "yaxis": {"gridcolor": "rgba(128,128,128,0.2)"},
        "polar": {
            "bgcolor": "rgba(0,0,0,0)",
            "angularaxis": {"gridcolor": "rgba(128,128,128,0.3)"},
            "radialaxis": {"gridcolor": "rgba(128,128,128,0.3)"}
        }
    }
}

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
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff'
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

# Custom CSS for professional styling - DARK THEME COMPATIBLE
st.markdown("""
<style>
    /* Main header with gradient */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    /* Metric cards for both themes */
    .metric-card {
        background: var(--background-color, #f8f9fa);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        text-align: center;
        height: 100%;
        transition: transform 0.3s ease;
    }
    
    /* Dark theme specific */
    @media (prefers-color-scheme: dark) {
        .metric-card {
            background: #262730;
            box-shadow: 0 2px 4px rgba(255,255,255,0.1);
        }
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background-color: #667eea;
    }
    
    /* Recommendation box */
    .recommendation-box {
        background: var(--secondary-background-color, #e9ecef);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    @media (prefers-color-scheme: dark) {
        .recommendation-box {
            background: #262730;
        }
    }
    
    /* Warning box */
    .warning-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #856404;
    }
    
    @media (prefers-color-scheme: dark) {
        .warning-box {
            background: #332701;
            color: #ffc107;
        }
    }
    
    /* Success box */
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #155724;
    }
    
    @media (prefers-color-scheme: dark) {
        .success-box {
            background: #0f3013;
            color: #28a745;
        }
    }
    
    /* Error box */
    .error-box {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #721c24;
    }
    
    @media (prefers-color-scheme: dark) {
        .error-box {
            background: #301418;
            color: #dc3545;
        }
    }
    
    /* Maturity level card */
    .maturity-level-card {
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    @media (prefers-color-scheme: dark) {
        .maturity-level-card {
            box-shadow: 0 2px 4px rgba(255,255,255,0.1);
        }
    }
    
    /* Compliance example */
    .compliance-example {
        background: #e7f3ff;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        font-style: italic;
        color: #004085;
    }
    
    @media (prefers-color-scheme: dark) {
        .compliance-example {
            background: #001f3f;
            color: #66b3ff;
        }
    }
    
    /* Documentation note */
    .documentation-note {
        background: #fff5ec;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border-left: 3px solid #ff9800;
        color: #663c00;
    }
    
    @media (prefers-color-scheme: dark) {
        .documentation-note {
            background: #331a00;
            color: #ff9800;
        }
    }
    
    /* Make expanders more visible in dark mode */
    @media (prefers-color-scheme: dark) {
        .streamlit-expanderHeader {
            background-color: #262730;
        }
        
        .streamlit-expanderContent {
            background-color: #0e1117;
        }
    }
    
    /* Improve readability of metrics in dark mode */
    @media (prefers-color-scheme: dark) {
        [data-testid="metric-container"] {
            background-color: #262730;
            border: 1px solid #464646;
            border-radius: 5px;
            padding: 0.5rem;
        }
    }
    
    /* Better button styling for dark mode */
    @media (prefers-color-scheme: dark) {
        .stButton > button {
            background-color: #262730;
            border: 1px solid #464646;
        }
        
        .stButton > button:hover {
            background-color: #333742;
            border-color: #667eea;
        }
    }
    
    /* Tab styling for dark mode */
    @media (prefers-color-scheme: dark) {
        .stTabs [data-baseweb="tab"] {
            background-color: #262730;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #333742;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #667eea !important;
        }
    }
</style>
""", unsafe_allow_html=True)