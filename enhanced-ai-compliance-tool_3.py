import streamlit as st
import json
import matplotlib.pyplot as plt
import numpy as np
import os
from fpdf import FPDF
import tempfile
import plotly.graph_objects as go
import plotly.express as px

# Load schema (keeping for backward compatibility)
schema_path = "ai_compliance_framework_schema_eu_tagged_full.json"
try:
    with open(schema_path, "r") as f:
        schema = json.load(f)
except FileNotFoundError:
    schema = {}  # Handle missing schema file gracefully

# Updated EU AI Act clauses with accurate articles and requirements
real_eu_ai_clauses = {
    "Governance & Oversight": {
        "Do you have designated roles and responsibilities for AI governance?": ("Article 26 – Obligations of users of high-risk AI systems", "https://artificialintelligenceact.eu/article/26/"),
        "Is there human oversight for high-risk AI system decision-making?": ("Article 14 – Human oversight", "https://artificialintelligenceact.eu/article/14/"),
        "Do you have processes to monitor AI system performance and accuracy?": ("Article 26 – Obligations of users", "https://artificialintelligenceact.eu/article/26/"),
        "Are employees trained on AI system capabilities and limitations?": ("Article 4 – AI literacy", "https://artificialintelligenceact.eu/article/4/"),
        "Do you have incident reporting procedures for AI system failures?": ("Article 26 – Obligations of users", "https://artificialintelligenceact.eu/article/26/")
    },
    "Risk Management": {
        "Do you have a risk management system for AI systems?": ("Article 9 – Risk management system", "https://artificialintelligenceact.eu/article/9/"),
        "Are AI systems tested for bias and discrimination before deployment?": ("Article 10 – Data and data governance", "https://artificialintelligenceact.eu/article/10/"),
        "Do you conduct impact assessments for high-risk AI systems?": ("Article 27 – Fundamental rights impact assessment", "https://artificialintelligenceact.eu/article/27/"),
        "Are there procedures to address AI system risks to vulnerable groups?": ("Article 9 – Risk management system", "https://artificialintelligenceact.eu/article/9/"),
        "Do you have quality management systems for AI development?": ("Article 17 – Quality management system", "https://artificialintelligenceact.eu/article/17/")
    },
    "Documentation & Transparency": {
        "Do you maintain technical documentation for AI systems?": ("Article 11 – Technical documentation", "https://artificialintelligenceact.eu/article/11/"),
        "Are users informed when interacting with AI systems?": ("Article 52 – Transparency obligations", "https://artificialintelligenceact.eu/article/52/"),
        "Do you keep logs of AI system operations and decisions?": ("Article 12 – Record-keeping", "https://artificialintelligenceact.eu/article/12/"),
        "Are instructions for use provided to AI system users?": ("Article 13 – Instructions for use", "https://artificialintelligenceact.eu/article/13/"),
        "Do you maintain records of AI system modifications and updates?": ("Article 12 – Record-keeping", "https://artificialintelligenceact.eu/article/12/")
    },
    "Data Governance": {
        "Are training datasets quality-controlled and bias-tested?": ("Article 10 – Data and data governance", "https://artificialintelligenceact.eu/article/10/"),
        "Do you have data lineage tracking for AI training data?": ("Article 10 – Data and data governance", "https://artificialintelligenceact.eu/article/10/"),
        "Are personal data processing activities compliant with GDPR?": ("Article 10 – Data and data governance", "https://artificialintelligenceact.eu/article/10/"),
        "Do you validate data quality before using for AI training?": ("Article 10 – Data and data governance", "https://artificialintelligenceact.eu/article/10/"),
        "Are datasets representative and free from harmful biases?": ("Article 10 – Data and data governance", "https://artificialintelligenceact.eu/article/10/")
    },
    "Compliance & Conformity": {
        "Do you have conformity assessments for high-risk AI systems?": ("Article 43 – Conformity assessment", "https://artificialintelligenceact.eu/article/43/"),
        "Are AI systems registered in the EU database when required?": ("Article 60 – EU database for high-risk AI systems", "https://artificialintelligenceact.eu/article/60/"),
        "Do you have CE marking for applicable AI systems?": ("Article 48 – CE marking", "https://artificialintelligenceact.eu/article/48/"),
        "Are there procedures for corrective actions when non-compliance is detected?": ("Article 21 – Corrective actions", "https://artificialintelligenceact.eu/article/21/"),
        "Do you have post-market monitoring systems for deployed AI?": ("Article 26 – Obligations of users", "https://artificialintelligenceact.eu/article/26/")
    },
    "General Purpose AI (GPAI) - Technical Documentation": {
        "Do you maintain comprehensive technical documentation for your GPAI model?": ("Article 53 – Obligations for providers of GPAI models", "https://artificialintelligenceact.eu/article/53/"),
        "Is your model architecture and training process documented?": ("Article 53 – Obligations for providers of GPAI models", "https://artificialintelligenceact.eu/article/53/")
    },
    "General Purpose AI (GPAI) - Copyright & IP": {
        "Have you implemented a policy to respect copyright law in your training data?": ("Article 53 – Obligations for providers of GPAI models", "https://artificialintelligenceact.eu/article/53/"),
        "Do you provide summaries of training data content and sources?": ("Article 53 – Obligations for providers of GPAI models", "https://artificialintelligenceact.eu/article/53/")
    },
    "General Purpose AI (GPAI) - Risk Assessment": {
        "Have you conducted systemic risk assessments for your model?": ("Article 55 – Obligations for providers of GPAI models with systemic risk", "https://artificialintelligenceact.eu/article/55/"),
        "Do you have risk mitigation measures in place?": ("Article 55 – Obligations for providers of GPAI models with systemic risk", "https://artificialintelligenceact.eu/article/55/")
    },
    "General Purpose AI (GPAI) - Governance": {
        "Do you have a designated governance structure for AI compliance?": ("Article 53 – Obligations for providers of GPAI models", "https://artificialintelligenceact.eu/article/53/"),
        "Have you registered your model with EU authorities?": ("Article 53 – Obligations for providers of GPAI models", "https://artificialintelligenceact.eu/article/53/")
    },
    "General Purpose AI (GPAI) - Downstream Use": {
        "Do you provide adequate information to downstream providers?": ("Article 53 – Obligations for providers of GPAI models", "https://artificialintelligenceact.eu/article/53/"),
        "Do you monitor and support downstream compliance?": ("Article 53 – Obligations for providers of GPAI models", "https://artificialintelligenceact.eu/article/53/")
    }
}

# Add comprehensive examples and documentation notes for all questions
all_examples = {
    # Governance & Oversight
    "Do you have designated roles and responsibilities for AI governance?": {
        "example": "We have a Chief AI Officer, AI Ethics Committee with quarterly meetings, designated AI system owners for each deployment, and clear RACI matrix for AI decisions.",
        "documentation": "Organizational charts, role descriptions, governance charter, meeting minutes, and decision logs."
    },
    "Is there human oversight for high-risk AI system decision-making?": {
        "example": "All high-risk AI decisions require human review before execution, with kill switches, override capabilities, and mandatory human sign-off for critical decisions.",
        "documentation": "Human oversight procedures, approval workflows, override logs, and training records."
    },
    "Do you have processes to monitor AI system performance and accuracy?": {
        "example": "We run daily accuracy checks, weekly performance reviews, monthly drift detection, with automated alerts for anomalies and dashboards showing key metrics.",
        "documentation": "Monitoring procedures, KPI definitions, alert configurations, and performance reports."
    },
    "Are employees trained on AI system capabilities and limitations?": {
        "example": "All staff complete mandatory AI literacy training, role-specific workshops for AI users, annual refreshers, and maintain >90% completion rate.",
        "documentation": "Training curricula, attendance records, assessment results, and competency matrices."
    },
    "Do you have incident reporting procedures for AI system failures?": {
        "example": "24-hour incident hotline, standardized reporting forms, root cause analysis process, with escalation matrix and remediation tracking system.",
        "documentation": "Incident response procedures, reporting templates, investigation reports, and corrective action logs."
    },
    
    # Risk Management
    "Do you have a risk management system for AI systems?": {
        "example": "ISO 31000-based framework with AI-specific risk taxonomy, quarterly risk assessments, mitigation plans, and board-level risk reporting.",
        "documentation": "Risk management framework, risk registers, assessment reports, and mitigation plans."
    },
    "Are AI systems tested for bias and discrimination before deployment?": {
        "example": "We conduct fairness audits using multiple metrics (demographic parity, equal opportunity), test on diverse datasets, and engage external auditors.",
        "documentation": "Bias testing protocols, audit reports, test datasets specifications, and remediation records."
    },
    "Do you conduct impact assessments for high-risk AI systems?": {
        "example": "Full DPIA plus AI-specific assessments covering fundamental rights, using EU methodology, with stakeholder consultations and public summaries.",
        "documentation": "Impact assessment templates, completed assessments, stakeholder feedback, and action plans."
    },
    "Are there procedures to address AI system risks to vulnerable groups?": {
        "example": "Special testing for elderly, children, disabled users; accessibility features; simplified interfaces; and dedicated support channels.",
        "documentation": "Vulnerability assessment procedures, accessibility standards, user testing results, and support protocols."
    },
    "Do you have quality management systems for AI development?": {
        "example": "ISO 9001 certified processes adapted for AI, including version control, peer reviews, staging environments, and automated testing pipelines.",
        "documentation": "QMS documentation, process maps, audit reports, and continuous improvement records."
    },
    
    # Documentation & Transparency
    "Do you maintain technical documentation for AI systems?": {
        "example": "Comprehensive docs including architecture diagrams, data flows, model cards, API specs, update logs, maintained in version-controlled repository.",
        "documentation": "Technical specifications, architecture documents, data dictionaries, and API documentation."
    },
    "Are users informed when interacting with AI systems?": {
        "example": "Clear AI disclosure badges, pop-up notifications, terms of service mentions, and opt-out options visible at all interaction points.",
        "documentation": "Transparency notices, UI/UX guidelines, user communication templates, and consent forms."
    },
    "Do you keep logs of AI system operations and decisions?": {
        "example": "Automated logging of all AI decisions with timestamps, input data, outputs, confidence scores, retained for 5 years with secure access controls.",
        "documentation": "Logging specifications, retention policies, access control procedures, and audit trail reports."
    },
    "Are instructions for use provided to AI system users?": {
        "example": "Multi-language user guides, video tutorials, in-app help, FAQs, covering proper use, limitations, and safety guidelines.",
        "documentation": "User manuals, training materials, help documentation, and safety guidelines."
    },
    "Do you maintain records of AI system modifications and updates?": {
        "example": "Git-based version control, detailed changelogs, rollback procedures, with approval records for all production changes.",
        "documentation": "Change management procedures, version histories, approval records, and rollback plans."
    },
    
    # Data Governance
    "Are training datasets quality-controlled and bias-tested?": {
        "example": "Multi-stage QA process: automated checks, statistical analysis, manual reviews, bias metrics, with 99.5% quality threshold before use.",
        "documentation": "Data quality standards, QA procedures, test results, and quality metrics."
    },
    "Do you have data lineage tracking for AI training data?": {
        "example": "End-to-end lineage from source systems through transformations to model training, using automated tools with visual lineage maps.",
        "documentation": "Data lineage tools configuration, lineage maps, data flow documentation, and source mappings."
    },
    "Are personal data processing activities compliant with GDPR?": {
        "example": "All processing has legal basis, documented in ROPA, with DPIAs completed, consent mechanisms implemented, and DPO approval obtained.",
        "documentation": "ROPA entries, legal basis documentation, DPIAs, consent records, and DPO assessments."
    },
    "Do you validate data quality before using for AI training?": {
        "example": "Automated validation pipelines checking completeness, accuracy, consistency, with manual spot checks and domain expert reviews.",
        "documentation": "Validation procedures, quality criteria, validation reports, and exception handling processes."
    },
    "Are datasets representative and free from harmful biases?": {
        "example": "Statistical analysis ensuring demographic representation matching target population, with external bias audits and corrective sampling.",
        "documentation": "Representation analysis, demographic breakdowns, bias audit reports, and sampling strategies."
    },
    
    # Compliance & Conformity
    "Do you have conformity assessments for high-risk AI systems?": {
        "example": "Third-party assessments following harmonized standards, internal audits, technical documentation reviews, with annual reassessments.",
        "documentation": "Assessment reports, certificates, audit trails, and corrective action plans."
    },
    "Are AI systems registered in the EU database when required?": {
        "example": "All high-risk systems registered before deployment, with quarterly updates, maintaining complete records and public transparency.",
        "documentation": "Registration confirmations, database entries, update logs, and compliance certificates."
    },
    "Do you have CE marking for applicable AI systems?": {
        "example": "CE marks affixed following conformity assessment, with technical files maintained, DoC issued, and market surveillance cooperation.",
        "documentation": "CE marking procedures, technical files, declarations of conformity, and test reports."
    },
    "Are there procedures for corrective actions when non-compliance is detected?": {
        "example": "24-hour response SLA, root cause analysis, corrective action plans, effectiveness verification, with board reporting for serious issues.",
        "documentation": "Corrective action procedures, investigation reports, action plans, and effectiveness reviews."
    },
    "Do you have post-market monitoring systems for deployed AI?": {
        "example": "Continuous performance monitoring, user feedback loops, incident tracking, with monthly reviews and proactive improvement cycles.",
        "documentation": "Monitoring plans, performance reports, user feedback analysis, and improvement records."
    },
    
    # GPAI-specific
    "Do you maintain comprehensive technical documentation for your GPAI model?": {
        "example": "500-page technical report covering architecture (transformer, 175B parameters), training (500TB data, 3 months), capabilities, limitations, and safety measures.",
        "documentation": "Model architecture, training process, datasets used, performance metrics, limitations, and intended use cases."
    },
    "Is your model architecture and training process documented?": {
        "example": "Detailed specs: transformer architecture, 175B parameters, 96 layers, trained on diverse web data using distributed computing across 1000 GPUs.",
        "documentation": "Architecture diagrams, hyperparameters, training procedures, computational requirements, and optimization details."
    },
    "Have you implemented a policy to respect copyright law in your training data?": {
        "example": "Automated filtering for copyrighted content, licensed dataset procurement, opt-out portal for creators, with quarterly legal reviews.",
        "documentation": "Copyright policy, filtering procedures, licensing agreements, opt-out mechanisms, and legal opinions."
    },
    "Do you provide summaries of training data content and sources?": {
        "example": "Public data card detailing: 40% web crawl, 30% books, 20% academic papers, 10% reference data, with quality and bias statistics.",
        "documentation": "Data cards, source breakdowns, quality metrics, and statistical summaries."
    },
    "Have you conducted systemic risk assessments for your model?": {
        "example": "Red team exercises for misuse, bias audits across demographics, safety evaluations for harmful content, with external expert reviews.",
        "documentation": "Risk assessment reports, red team findings, mitigation strategies, and monitoring plans."
    },
    "Do you have risk mitigation measures in place?": {
        "example": "Content filters, use case restrictions, rate limiting, monitoring systems, with escalation procedures and regular effectiveness reviews.",
        "documentation": "Mitigation strategies, implementation plans, effectiveness metrics, and incident reports."
    },
    "Do you have a designated governance structure for AI compliance?": {
        "example": "AI Board meeting monthly, Chief AI Officer, dedicated compliance team, ethics committee, with clear escalation paths and decision rights.",
        "documentation": "Governance charter, organizational structure, meeting minutes, and decision logs."
    },
    "Have you registered your model with EU authorities?": {
        "example": "Registered in EU AI database with complete technical documentation, regular updates submitted, maintaining public transparency page.",
        "documentation": "Registration certificates, submission records, update logs, and compliance confirmations."
    },
    "Do you provide adequate information to downstream providers?": {
        "example": "Comprehensive package: API docs, model cards, integration guides, safety guidelines, rate limits, with developer portal and support.",
        "documentation": "API documentation, model cards, safety guidelines, and usage restrictions."
    },
    "Do you monitor and support downstream compliance?": {
        "example": "Usage monitoring dashboard, compliance APIs, quarterly reviews of downstream implementations, with violation response procedures.",
        "documentation": "Monitoring procedures, compliance metrics, support processes, and enforcement actions."
    }
}

# Updated recommendation helper with more specific Atlan integration suggestions
def get_atlan_recommendations(clause_text):
    recommendations = {
        "governance": "Use Atlan's role-based access control and governance workflows to establish clear AI oversight responsibilities and approval processes. Set up custom roles for AI governance team members and configure multi-stage approval workflows for AI system changes.",
        "oversight": "Implement Atlan's lineage tracking and monitoring capabilities to maintain human oversight over AI decision-making processes. Create dashboards showing AI decision flows and set up alerts for decisions requiring human review.",
        "risk": "Leverage Atlan's metadata management and classification features to identify and track high-risk AI systems and their data dependencies. Use custom tags to classify risk levels and create risk assessment workflows.",
        "documentation": "Use Atlan's comprehensive metadata catalog to maintain technical documentation, lineage, and change tracking for AI systems. Create model cards, attach architecture diagrams, and maintain version-controlled documentation.",
        "transparency": "Implement Atlan's glossary and documentation features to ensure clear communication about AI system capabilities and limitations. Publish AI system information to stakeholders through Atlan's collaboration features.",
        "data": "Use Atlan's data quality monitoring, lineage tracking, and profiling capabilities to ensure training data meets Article 10 requirements. Set up quality rules, monitor data drift, and track bias metrics.",
        "compliance": "Leverage Atlan's audit trails, version control, and governance features to support conformity assessments and regulatory compliance. Generate compliance reports and maintain evidence for audits.",
        "conformity": "Use Atlan's workflow automation and approval processes to implement systematic conformity assessment procedures. Create checklists and automate assessment workflows.",
        "corrective": "Implement Atlan's incident management and change tracking capabilities to support corrective action procedures. Set up incident workflows and track remediation progress.",
        "monitoring": "Use Atlan's monitoring and alerting features to implement post-market surveillance of deployed AI systems. Create performance dashboards and configure drift alerts.",
        "gpai": "Leverage Atlan's comprehensive documentation and lineage features to meet GPAI model transparency and documentation requirements. Build model registries and maintain training data catalogs.",
        "copyright": "Use Atlan's data cataloging and lineage features to track copyright status and licensing of training data sources. Tag datasets with licensing information and maintain opt-out records.",
        "downstream": "Implement Atlan's API documentation and access control features to manage downstream provider relationships. Create API catalogs and track usage patterns.",
        "users": "Configure Atlan's access management to control and monitor who can access AI systems and their outputs. Implement usage tracking and access auditing.",
        "literacy": "Use Atlan's knowledge base and glossary features to support AI literacy training. Create learning resources and track training completion.",
        "quality": "Leverage Atlan's data quality framework to implement comprehensive quality management for AI systems. Define quality metrics and automate quality checks.",
        "impact": "Use Atlan's impact analysis features to assess how AI systems affect different stakeholder groups. Map dependencies and analyze downstream impacts.",
        "registration": "Maintain EU database registration information in Atlan's metadata catalog. Track registration status and compliance certificates.",
        "marking": "Use Atlan's tagging and classification features to track CE marking status and conformity assessments. Maintain technical files and declarations."
    }
    
    # Extract key terms to match recommendations
    key_terms = clause_text.lower().split()
    for term in key_terms:
        if term in recommendations:
            return recommendations[term]
    
    # Default comprehensive recommendation
    return "Use Atlan's comprehensive data governance platform to maintain audit readiness and ensure compliance with EU AI Act requirements through automated lineage, metadata management, and governance workflows. Configure custom attributes for EU AI Act compliance tracking and leverage workflow automation for systematic compliance management."

# START STREAMLIT APP
st.set_page_config(
    page_title="EU AI Act Compliance Tool",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'assessment_type' not in st.session_state:
    st.session_state.assessment_type = None

# Landing Page
if st.session_state.page == 'landing':
    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 3.5rem; margin-bottom: 0.5rem;">🧠 EU AI Act Compliance Tool</h1>
        <p style="font-size: 1.3rem; color: #666; margin-bottom: 2rem;">
            Navigate EU AI Act compliance with confidence using data governance best practices
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Assessment Type Selection
    st.markdown("## 🎯 Choose Your Assessment Type")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #f0f4f8; padding: 2rem; border-radius: 10px; border: 2px solid #e0e0e0;">
            <h3>🏢 General AI Systems Assessment</h3>
            <p>For organizations using or deploying AI systems in various applications</p>
            <ul>
                <li>High-risk AI systems evaluation</li>
                <li>Governance and oversight requirements</li>
                <li>Data governance compliance</li>
                <li>Risk management frameworks</li>
                <li>Documentation requirements</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📋 Start General AI Assessment", key="general", use_container_width=True):
            st.session_state.assessment_type = 'general'
            st.session_state.page = 'info'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="background: #fff3e0; padding: 2rem; border-radius: 10px; border: 2px solid #ffcc80;">
            <h3>🤖 GPAI Model Assessment</h3>
            <p>Specifically for General-Purpose AI model providers (like LLMs)</p>
            <ul>
                <li>Technical documentation requirements</li>
                <li>Copyright and IP compliance</li>
                <li>Systemic risk assessments</li>
                <li>Model governance structures</li>
                <li>Downstream provider obligations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start GPAI Assessment", key="gpai", use_container_width=True):
            st.session_state.assessment_type = 'gpai'
            st.session_state.page = 'info'
            st.rerun()
    
    # Why This Matters Section
    st.markdown("---")
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        ## 🎯 Why This Assessment Matters
        
        The **EU Artificial Intelligence Act** is the world's first comprehensive AI regulation, with **significant penalties** up to €35 million or 7% of worldwide annual turnover for non-compliance.
        
        ### Key Challenges Organizations Face:
        - **Complex Requirements**: 113 articles covering everything from data governance to human oversight
        - **Phased Implementation**: Different deadlines from 2025-2027 based on AI risk categories
        - **Global Impact**: Affects any organization with AI systems used in the EU market
        - **Governance Gaps**: Most organizations lack proper AI governance frameworks
        
        ### What Makes This Different:
        ✅ **Accurate & Current**: Based on the official EU AI Act text and latest updates  
        ✅ **Practical Focus**: Real questions about your current practices, not theoretical concepts  
        ✅ **Actionable Results**: Specific recommendations using Atlan's data governance platform  
        ✅ **Risk-Based Approach**: Prioritizes gaps based on regulatory impact and deadlines  
        """)
    
    with col2:
        st.markdown("""
        ### 📊 What You'll Get
        
        **Immediate Results:**
        - Overall compliance score (%)
        - Article-by-article gap analysis
        - Priority ranking of improvement areas
        - Timeline-based action plan
        - Visual maturity assessment
        
        **Atlan-Specific Guidance:**
        - Feature mapping to EU AI Act requirements
        - Implementation roadmap
        - Governance workflow recommendations
        - Technical setup instructions
        
        **Compliance Confidence:**
        - Clear understanding of your current state
        - Roadmap to full compliance
        - Risk mitigation strategies
        - Audit-ready documentation approach
        """)
    
    # Timeline Section
    st.markdown("---")
    st.markdown("## ⏰ EU AI Act Implementation Timeline")
    
    timeline_cols = st.columns(4)
    
    with timeline_cols[0]:
        st.markdown("""
        <div style="background: #ffebee; padding: 1rem; border-radius: 8px; text-align: center;">
            <h4 style="color: #c62828;">Feb 2, 2025</h4>
            <p><strong>Prohibited Practices</strong><br>
            AI systems ban in effect<br>
            AI literacy requirements</p>
        </div>
        """, unsafe_allow_html=True)
    
    with timeline_cols[1]:
        st.markdown("""
        <div style="background: #fff3e0; padding: 1rem; border-radius: 8px; text-align: center;">
            <h4 style="color: #ef6c00;">Aug 2, 2025</h4>
            <p><strong>GPAI Models</strong><br>
            General-purpose AI obligations<br>
            Governance structures</p>
        </div>
        """, unsafe_allow_html=True)
    
    with timeline_cols[2]:
        st.markdown("""
        <div style="background: #e8f5e8; padding: 1rem; border-radius: 8px; text-align: center;">
            <h4 style="color: #2e7d32;">Aug 2, 2026</h4>
            <p><strong>High-Risk Systems</strong><br>
            Full compliance required<br>
            Main implementation deadline</p>
        </div>
        """, unsafe_allow_html=True)
    
    with timeline_cols[3]:
        st.markdown("""
        <div style="background: #e3f2fd; padding: 1rem; border-radius: 8px; text-align: center;">
            <h4 style="color: #1565c0;">Aug 2, 2027</h4>
            <p><strong>Embedded Systems</strong><br>
            Extended deadline for<br>
            embedded AI systems</p>
        </div>
        """, unsafe_allow_html=True)

# Organization Info Page
elif st.session_state.page == 'info':
    # Header with navigation
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        assessment_title = "GPAI Model" if st.session_state.assessment_type == 'gpai' else "General AI Systems"
        st.title(f"🏢 Organization Information - {assessment_title} Assessment")
        st.markdown("Please provide your organization details to personalize the compliance report.")
    with col2:
        if st.button("🏠 Home", key="home_info"):
            st.session_state.page = 'landing'
            st.session_state.assessment_type = None
            st.rerun()
    with col3:
        if st.button("← Back"):
            st.session_state.page = 'landing'
            st.session_state.assessment_type = None
            st.rerun()
    
    st.markdown("---")
    
    # Organization form
    with st.form("organization_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            org_name = st.text_input("Organization Name *", placeholder="Enter your organization name")
            industry = st.selectbox("Industry Sector *", 
                ["Select...", "Technology", "Healthcare", "Finance", "Education", "Government", 
                 "Manufacturing", "Retail", "Transportation", "Other"])
            org_size = st.selectbox("Organization Size *",
                ["Select...", "1-50 employees", "51-200 employees", "201-1000 employees", 
                 "1001-5000 employees", "5000+ employees"])
        
        with col2:
            ai_maturity = st.selectbox("AI Maturity Level *",
                ["Select...", "Exploring AI", "Pilot Projects", "Production Deployment", 
                 "Scaled Implementation", "AI-First Organization"])
            if st.session_state.assessment_type == 'gpai':
                model_type = st.selectbox("GPAI Model Type *",
                    ["Select...", "Language Model (LLM)", "Vision Model", "Multimodal Model", 
                     "Code Generation Model", "Other"])
                model_size = st.selectbox("Model Parameters *",
                    ["Select...", "< 1B", "1B - 10B", "10B - 100B", "100B+"])
        
        submitted = st.form_submit_button("Continue to Assessment", type="primary", use_container_width=True)
        
        if submitted:
            if org_name and industry != "Select..." and org_size != "Select..." and ai_maturity != "Select...":
                st.session_state.org_name = org_name
                st.session_state.industry = industry
                st.session_state.org_size = org_size
                st.session_state.ai_maturity = ai_maturity
                if st.session_state.assessment_type == 'gpai':
                    st.session_state.model_type = model_type
                    st.session_state.model_size = model_size
                st.session_state.page = 'assessment'
                st.rerun()
            else:
                st.error("Please fill in all required fields marked with *")

# Assessment Page
elif st.session_state.page == 'assessment':
    # Header with navigation
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        assessment_title = "GPAI Model" if st.session_state.assessment_type == 'gpai' else "General AI Systems"
        st.title(f"🧠 EU AI Act Compliance Assessment - {assessment_title}")
        st.markdown(f"**Organization:** {st.session_state.get('org_name', 'Unknown')}")
    with col2:
        if st.button("🏠 Home", key="home_assessment"):
            st.session_state.page = 'landing'
            st.session_state.assessment_type = None
            st.rerun()
    with col3:
        if st.button("← Back"):
            st.session_state.page = 'info'
            st.rerun()
    
    # Progress indicator
    st.markdown("---")

    # Assessment form
    user_answers = {}
    
    # Filter questions based on assessment type
    if st.session_state.assessment_type == 'gpai':
        # GPAI-specific sections
        relevant_sections = {k: v for k, v in real_eu_ai_clauses.items() if "General Purpose AI" in k}
    else:
        # General AI sections (exclude GPAI-specific)
        relevant_sections = {k: v for k, v in real_eu_ai_clauses.items() if "General Purpose AI" not in k}
    
    # Question sections with progress tracking
    total_sections = len(relevant_sections)
    
    for idx, (section, questions) in enumerate(relevant_sections.items(), 1):
        st.markdown(f"### {idx}. {section}")
        st.progress(idx / total_sections, text=f"Section {idx} of {total_sections}")
        
        # Create columns for better layout
        for question, (clause, link) in questions.items():
            # Check if we have examples for this question
            if question in all_examples:
                col1, col2 = st.columns([3, 1])
                with col1:
                    user_answers[question] = st.selectbox(
                        question, 
                        ["Select...", "Yes", "Partial", "No"], 
                        key=question,
                        help=f"📖 Related to: {clause}\n🔗 Click article link in results for details"
                    )
                with col2:
                    with st.expander("📘 Example & Docs"):
                        st.info(f"**Example:** {all_examples[question]['example']}")
                        st.warning(f"**Documentation Required:** {all_examples[question]['documentation']}")
            else:
                user_answers[question] = st.selectbox(
                    question, 
                    ["Select...", "Yes", "Partial", "No"], 
                    key=question,
                    help=f"📖 Related to: {clause}\n🔗 Click article link in results for details"
                )
        
        # Add section summary
        if idx < total_sections:
            st.markdown("---")
    
    # Submit button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📊 Generate Compliance Report", type="primary", use_container_width=True):
            # Check if all questions are answered
            unanswered = [q for q, a in user_answers.items() if a == "Select..."]
            if unanswered:
                st.error(f"Please answer all questions. {len(unanswered)} questions remaining.")
            else:
                st.session_state.page = 'results'
                st.session_state.user_answers = user_answers
                st.rerun()

# Results Page
elif st.session_state.page == 'results':
    # Header with navigation
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.title(f"📊 EU AI Act Compliance Report - {st.session_state.get('org_name', 'Unknown')}")
        assessment_type = "GPAI Model" if st.session_state.assessment_type == 'gpai' else "General AI Systems"
        st.markdown(f"**Assessment Type:** {assessment_type} | **Industry:** {st.session_state.get('industry', 'Unknown')}")
    with col2:
        if st.button("🏠 Home", key="home_results"):
            st.session_state.page = 'landing'
            st.session_state.assessment_type = None
            if 'user_answers' in st.session_state:
                del st.session_state.user_answers
            st.rerun()
    with col3:
        if st.button("🔄 Retake"):
            st.session_state.page = 'assessment'
            if 'user_answers' in st.session_state:
                del st.session_state.user_answers
            st.rerun()
    
    # Get answers from session state
    user_answers = st.session_state.get('user_answers', {})
    
    # Only show results if we have answers
    if not user_answers:
        st.error("No assessment data found. Please complete the assessment first.")
        if st.button("Start Assessment"):
            st.session_state.page = 'assessment'
            st.rerun()
    else:
        # Filter relevant sections for scoring
        if st.session_state.assessment_type == 'gpai':
            relevant_sections = {k: v for k, v in real_eu_ai_clauses.items() if "General Purpose AI" in k}
        else:
            relevant_sections = {k: v for k, v in real_eu_ai_clauses.items() if "General Purpose AI" not in k}
        
        # Compliance scoring
        clause_summary = {}
        compliant = []
        gaps = []
        section_scores = {s: [0, 0] for s in relevant_sections}  # answered, total

        for section, questions in relevant_sections.items():
            for q, (clause_title, clause_link) in questions.items():
                a = user_answers.get(q, "No")  # Default to "No" if missing
                clause_summary.setdefault(clause_title, {"link": clause_link, "compliant": 0, "total": 0, "questions": []})
                clause_summary[clause_title]["total"] += 1
                section_scores[section][1] += 1
                
                if a == "Yes":
                    clause_summary[clause_title]["compliant"] += 1
                    compliant.append((q, clause_title, clause_link))
                    section_scores[section][0] += 1
                else:
                    gaps.append((q, clause_title, clause_link))
                clause_summary[clause_title]["questions"].append((q, a))

        # Calculate overall compliance score
        total_questions = sum(total for _, total in section_scores.values())
        total_compliant = sum(compliant for compliant, _ in section_scores.values())
        overall_compliance = round((total_compliant / total_questions) * 100, 1)

        # Executive Summary
        st.markdown("## 🎯 Executive Summary")
        
        # Determine compliance level and messaging
        if overall_compliance >= 80:
            compliance_level = "High"
            compliance_color = "success"
            compliance_message = "Excellent! Your organization shows strong EU AI Act readiness."
        elif overall_compliance >= 60:
            compliance_level = "Medium"
            compliance_color = "warning"  
            compliance_message = "Good progress! Focus on addressing priority gaps for full compliance."
        else:
            compliance_level = "Low"
            compliance_color = "error"
            compliance_message = "Immediate action required to meet EU AI Act requirements."
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Overall Compliance", f"{overall_compliance}%", 
                     help="Percentage of requirements currently met")
        with col2:
            st.metric("Compliance Level", compliance_level,
                     help="Risk assessment based on current state")
        with col3:
            st.metric("Areas Addressed", f"{len(compliant)}/{total_questions}",
                     help="Number of requirements currently met")
        with col4:
            st.metric("Priority Gaps", len(gaps),
                     help="Number of areas needing attention")
        
        # Compliance message
        if compliance_color == "success":
            st.success(f"✅ {compliance_message}")
        elif compliance_color == "warning":
            st.warning(f"⚠️ {compliance_message}")
        else:
            st.error(f"🚨 {compliance_message}")

        # GPAI-specific maturity quadrants
        if st.session_state.assessment_type == 'gpai':
            st.markdown("---")
            st.markdown("## 🎨 GPAI Maturity Assessment")
            
            # Calculate scores for GPAI quadrants
            gpai_quadrants = {
                "Technical Documentation": ["General Purpose AI (GPAI) - Technical Documentation"],
                "Copyright Compliance": ["General Purpose AI (GPAI) - Copyright & IP"],
                "Risk Management": ["General Purpose AI (GPAI) - Risk Assessment"],
                "Governance & Downstream": ["General Purpose AI (GPAI) - Governance", "General Purpose AI (GPAI) - Downstream Use"]
            }
            
            quadrant_scores = {}
            for quadrant_name, sections in gpai_quadrants.items():
                total_score = 0
                total_questions = 0
                for section in sections:
                    if section in section_scores:
                        score, total = section_scores[section]
                        total_score += score
                        total_questions += total
                if total_questions > 0:
                    quadrant_scores[quadrant_name] = round((total_score / total_questions) * 100, 1)
                else:
                    quadrant_scores[quadrant_name] = 0
            
            # Display quadrants
            col1, col2 = st.columns(2)
            with col1:
                for idx, (quadrant, score) in enumerate(list(quadrant_scores.items())[:2]):
                    color = "#4caf50" if score >= 80 else "#ff9800" if score >= 50 else "#f44336"
                    st.markdown(f"""
                    <div style="background: {color}; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center;">
                        <h4>{quadrant}</h4>
                        <h1 style="margin: 10px 0;">{score}%</h1>
                        <p style="margin: 0;">{"High Maturity" if score >= 80 else "Medium Maturity" if score >= 50 else "Low Maturity"}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                for idx, (quadrant, score) in enumerate(list(quadrant_scores.items())[2:]):
                    color = "#4caf50" if score >= 80 else "#ff9800" if score >= 50 else "#f44336"
                    st.markdown(f"""
                    <div style="background: {color}; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center;">
                        <h4>{quadrant}</h4>
                        <h1 style="margin: 10px 0;">{score}%</h1>
                        <p style="margin: 0;">{"High Maturity" if score >= 80 else "Medium Maturity" if score >= 50 else "Low Maturity"}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            # General AI maturity quadrants
            st.markdown("---")
            st.markdown("## 🎨 AI Governance Maturity Assessment")
            
            # Calculate scores for general AI quadrants
            general_quadrants = {
                "Governance & Oversight": ["Governance & Oversight"],
                "Risk Management": ["Risk Management"],
                "Documentation & Transparency": ["Documentation & Transparency"],
                "Data & Compliance": ["Data Governance", "Compliance & Conformity"]
            }
            
            quadrant_scores = {}
            for quadrant_name, sections in general_quadrants.items():
                total_score = 0
                total_questions = 0
                for section in sections:
                    if section in section_scores:
                        score, total = section_scores[section]
                        total_score += score
                        total_questions += total
                if total_questions > 0:
                    quadrant_scores[quadrant_name] = round((total_score / total_questions) * 100, 1)
                else:
                    quadrant_scores[quadrant_name] = 0
            
            # Create visual maturity matrix
            st.markdown("### 📊 Maturity Matrix Visualization")
            
            # Create a 2x2 grid visualization
            fig = go.Figure()
            
            # Define quadrant positions
            positions = {
                "Governance & Oversight": (0.25, 0.75),
                "Risk Management": (0.75, 0.75),
                "Documentation & Transparency": (0.25, 0.25),
                "Data & Compliance": (0.75, 0.25)
            }
            
            # Add quadrants as scatter points
            for quadrant, score in quadrant_scores.items():
                x, y = positions[quadrant]
                size = score / 2  # Scale size based on score
                color = '#4caf50' if score >= 80 else '#ff9800' if score >= 50 else '#f44336'
                
                fig.add_trace(go.Scatter(
                    x=[x],
                    y=[y],
                    mode='markers+text',
                    marker=dict(
                        size=size,
                        color=color,
                        line=dict(color='white', width=2)
                    ),
                    text=f"{quadrant}<br>{score}%",
                    textposition="middle center",
                    name=quadrant,
                    showlegend=False
                ))
            
            # Add quadrant lines
            fig.add_shape(type="line", x0=0.5, y0=0, x1=0.5, y1=1,
                          line=dict(color="gray", width=1, dash="dash"))
            fig.add_shape(type="line", x0=0, y0=0.5, x1=1, y1=0.5,
                          line=dict(color="gray", width=1, dash="dash"))
            
            # Add quadrant labels
            fig.add_annotation(x=0.25, y=0.95, text="<b>Strategic</b>", showarrow=False)
            fig.add_annotation(x=0.75, y=0.95, text="<b>Operational</b>", showarrow=False)
            fig.add_annotation(x=0.05, y=0.25, text="<b>Foundational</b>", showarrow=False, textangle=-90)
            fig.add_annotation(x=0.95, y=0.75, text="<b>Advanced</b>", showarrow=False, textangle=-90)
            
            fig.update_layout(
                xaxis=dict(showgrid=False, zeroline=False, visible=False, range=[0, 1]),
                yaxis=dict(showgrid=False, zeroline=False, visible=False, range=[0, 1]),
                plot_bgcolor="white",
                height=500,
                title="AI Governance Maturity Matrix"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display detailed quadrants below
            col1, col2 = st.columns(2)
            with col1:
                for idx, (quadrant, score) in enumerate(list(quadrant_scores.items())[:2]):
                    color = "#4caf50" if score >= 80 else "#ff9800" if score >= 50 else "#f44336"
                    st.markdown(f"""
                    <div style="background: {color}; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center;">
                        <h4>{quadrant}</h4>
                        <h1 style="margin: 10px 0;">{score}%</h1>
                        <p style="margin: 0;">{"High Maturity" if score >= 80 else "Medium Maturity" if score >= 50 else "Low Maturity"}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                for idx, (quadrant, score) in enumerate(list(quadrant_scores.items())[2:]):
                    color = "#4caf50" if score >= 80 else "#ff9800" if score >= 50 else "#f44336"
                    st.markdown(f"""
                    <div style="background: {color}; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center;">
                        <h4>{quadrant}</h4>
                        <h1 style="margin: 10px 0;">{score}%</h1>
                        <p style="margin: 0;">{"High Maturity" if score >= 80 else "Medium Maturity" if score >= 50 else "Low Maturity"}</p>
                    </div>
                    """, unsafe_allow_html=True)

        # Enhanced visualizations
        st.markdown("---")
        st.markdown("## 📊 Compliance Analysis")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["Article Compliance", "Section Analysis", "Priority Matrix"])
        
        with tab1:
            # Bar chart
            chart_labels = []
            chart_values = []
            chart_colors = []

            for clause, details in clause_summary.items():
                pct = round((details['compliant'] / details['total']) * 100, 1)
                chart_labels.append(clause.replace(' – ', '\n'))
                chart_values.append(pct)
                
                if pct >= 80:
                    chart_colors.append('#2E8B57')
                elif pct >= 50:
                    chart_colors.append('#FFB347')
                else:
                    chart_colors.append('#FF6B6B')

            fig, ax = plt.subplots(figsize=(12, 8))
            bars = ax.barh(chart_labels, chart_values, color=chart_colors)
            ax.set_xlabel("Compliance Percentage")
            ax.set_title("EU AI Act Article Compliance Status")
            ax.set_xlim(0, 100)

            for bar, value in zip(bars, chart_values):
                ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
                        f'{value}%', ha='left', va='center', fontweight='bold')

            plt.tight_layout()
            st.pyplot(fig)
        
        with tab2:
            # Section-wise radar chart using plotly
            section_names = list(section_scores.keys())
            section_values = [round((score[0] / score[1]) * 100, 1) for score in section_scores.values()]
            
            fig = go.Figure(data=go.Scatterpolar(
                r=section_values,
                theta=section_names,
                fill='toself',
                name='Compliance Score'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=False,
                title="Section-wise Compliance Radar"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Priority matrix
            st.markdown("### 🎯 Priority Action Matrix")
            
            # Create priority scores based on deadline and impact
            priority_matrix = []
            for q, clause, link in gaps:
                # Determine urgency based on implementation timeline
                if "GPAI" in clause or "Article 53" in clause or "Article 55" in clause:
                    deadline = "Aug 2025"
                    urgency = 3
                elif "high-risk" in clause.lower() or "Article 26" in clause:
                    deadline = "Aug 2026"
                    urgency = 2
                else:
                    deadline = "Aug 2027"
                    urgency = 1
                
                # Determine impact
                if any(keyword in clause.lower() for keyword in ['risk management', 'conformity', 'oversight']):
                    impact = 3
                elif any(keyword in clause.lower() for keyword in ['documentation', 'transparency']):
                    impact = 2
                else:
                    impact = 1
                
                priority_matrix.append({
                    "Question": q[:50] + "...",
                    "Article": clause.split(' – ')[0],
                    "Deadline": deadline,
                    "Urgency": urgency,
                    "Impact": impact,
                    "Priority Score": urgency * impact
                })
            
            # Sort by priority score
            priority_matrix.sort(key=lambda x: x["Priority Score"], reverse=True)
            
            # Display top priorities
            st.dataframe(priority_matrix[:10], use_container_width=True)

        # Recommendations
        st.markdown("---")
        st.markdown("## 🎯 Strategic Recommendations & Atlan Implementation")
        
        # Create tabs for different recommendation categories
        rec_tab1, rec_tab2, rec_tab3 = st.tabs(["📋 Compliance Roadmap", "🔧 Atlan Implementation", "📊 Quick Wins"])
        
        with rec_tab1:
            if st.session_state.assessment_type == 'gpai':
                # GPAI-specific recommendations
                st.markdown("### 🤖 GPAI Model Compliance Roadmap")
                
                if overall_compliance < 50:
                    st.error("**Critical**: Your GPAI model requires immediate attention to meet EU AI Act requirements by August 2025.")
                    
                    with st.expander("🚨 Phase 1: Immediate Actions (Next 30 Days)", expanded=True):
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.markdown("""
                            1. **Technical Documentation Sprint**
                               - Create comprehensive model cards
                               - Document architecture and parameters
                               - Map all training data sources
                               
                            2. **Copyright Compliance Audit**
                               - Review all training data for copyright issues
                               - Implement opt-out mechanisms
                               - Document data licensing
                               
                            3. **Risk Assessment Initiative**
                               - Conduct red team exercises
                               - Perform bias audits
                               - Document safety measures
                            """)
                        with col2:
                            st.info("""
                            **Atlan Features to Use:**
                            - Data Catalog
                            - Lineage Tracking
                            - Metadata Management
                            - Workflow Automation
                            """)
                            
                    with st.expander("📅 Phase 2: Foundation Building (Days 31-60)"):
                        st.markdown("""
                        4. **Governance Structure Setup**
                           - Establish AI compliance team
                           - Define roles and responsibilities
                           - Create decision workflows
                           
                        5. **Downstream Documentation**
                           - Prepare API documentation
                           - Create usage guidelines
                           - Build support infrastructure
                        """)
                        
                    with st.expander("🎯 Phase 3: Compliance Finalization (Days 61-90)"):
                        st.markdown("""
                        6. **EU Registration Preparation**
                           - Compile all documentation
                           - Complete registration forms
                           - Submit to EU database
                           
                        7. **Monitoring Systems**
                           - Implement performance tracking
                           - Set up incident response
                           - Create audit trails
                        """)
                else:
                    st.warning("**Action Required**: Focus on priority gaps to ensure GPAI compliance by August 2025.")
                    st.markdown("""
                    #### ⚠️ Priority Actions (Next 60 Days):
                    1. **Documentation Enhancement**: Complete all technical documentation requirements
                    2. **Risk Mitigation**: Implement identified risk mitigation measures
                    3. **Compliance Registration**: Prepare for EU authority registration
                    4. **Downstream Support**: Establish support channels for model users
                    5. **Monitoring Systems**: Set up continuous monitoring for model behavior
                    """)
            else:
                # General AI recommendations
                st.markdown("### 🏢 General AI Systems Compliance Roadmap")
                
                if overall_compliance < 50:
                    st.error("**Immediate Action Required**: Significant improvements needed for EU AI Act compliance.")
                    
                    with st.expander("🚨 Critical Path (Next 30-90 Days)", expanded=True):
                        st.markdown("""
                        **Month 1: Foundation**
                        - Executive briefing on compliance risks
                        - Form cross-functional AI governance team
                        - Complete AI system inventory
                        - Identify high-risk systems
                        
                        **Month 2: Assessment**
                        - Conduct risk assessments
                        - Document current processes
                        - Identify compliance gaps
                        - Prioritize remediation efforts
                        
                        **Month 3: Implementation**
                        - Deploy governance workflows
                        - Implement monitoring systems
                        - Start documentation updates
                        - Begin training programs
                        """)
                elif overall_compliance < 80:
                    st.warning("**Moderate Compliance**: Strategic improvements needed.")
                    st.markdown("""
                    Focus on closing identified gaps through systematic improvements:
                    - Strengthen documentation practices
                    - Enhance risk management processes
                    - Improve transparency measures
                    - Establish monitoring systems
                    """)
                else:
                    st.success("**Strong Position**: Maintain and optimize current practices.")
                    st.markdown("""
                    Continue excellence through:
                    - Regular compliance audits
                    - Continuous improvement cycles
                    - Industry best practice adoption
                    - Proactive regulatory engagement
                    """)
                    
        with rec_tab2:
            st.markdown("### 🔧 Atlan Implementation Guide")
            
            # Atlan implementation phases
            implementation_phases = {
                "Phase 1: Data Foundation (Weeks 1-4)": {
                    "Setup & Configuration": [
                        "Configure Atlan workspace with AI-specific metadata models",
                        "Set up user roles and permissions aligned with AI governance",
                        "Create custom attributes for EU AI Act compliance tracking"
                    ],
                    "Data Cataloging": [
                        "Import AI system inventory into Atlan catalog",
                        "Document all training datasets with quality metrics",
                        "Map data lineage from source to AI model"
                    ],
                    "Atlan Features": ["Data Catalog", "Custom Metadata", "Lineage Tracking", "Access Control"]
                },
                "Phase 2: Governance Workflows (Weeks 5-8)": {
                    "Process Automation": [
                        "Design approval workflows for AI system changes",
                        "Implement data quality checks for training data",
                        "Create incident management workflows"
                    ],
                    "Compliance Tracking": [
                        "Build compliance dashboards in Atlan",
                        "Set up automated compliance score calculations",
                        "Configure alerting for compliance violations"
                    ],
                    "Atlan Features": ["Workflow Builder", "Custom Dashboards", "Automated Actions", "Alerts"]
                },
                "Phase 3: Monitoring & Optimization (Weeks 9-12)": {
                    "Continuous Monitoring": [
                        "Deploy real-time data quality monitoring",
                        "Implement drift detection for AI models",
                        "Track compliance metrics continuously"
                    ],
                    "Reporting & Audit": [
                        "Generate automated compliance reports",
                        "Maintain audit trails for all changes",
                        "Create stakeholder dashboards"
                    ],
                    "Atlan Features": ["Monitoring APIs", "Report Builder", "Audit Logs", "Stakeholder Views"]
                }
            }
            
            for phase, details in implementation_phases.items():
                with st.expander(f"📌 {phase}", expanded=True):
                    for category, items in details.items():
                        if category == "Atlan Features":
                            st.info(f"**Key Atlan Features:** {', '.join(items)}")
                        else:
                            st.markdown(f"**{category}:**")
                            for item in items:
                                st.markdown(f"- {item}")
                                
            # Atlan-specific benefits
            st.markdown("### 💡 How Atlan Addresses EU AI Act Requirements")
            
            # Define benefits mapping based on assessment type
            if st.session_state.assessment_type == 'gpai':
                benefits_mapping = {
                    "Article 53 - GPAI Model Documentation": {
                        "requirement": "Provide technical documentation for GPAI models",
                        "atlan_solution": "Create comprehensive model registries with architecture details, training parameters, and performance metrics in Atlan's catalog",
                        "features": ["Model Registry", "Custom Metadata", "Version Control"]
                    },
                    "Article 53 - Copyright Compliance": {
                        "requirement": "Respect copyright law and provide training data summaries",
                        "atlan_solution": "Track all training data sources with licensing metadata, maintain opt-out records, and generate automated data summaries",
                        "features": ["Data Lineage", "License Tracking", "Automated Reports"]
                    },
                    "Article 55 - Systemic Risk Assessment": {
                        "requirement": "Evaluate and mitigate systemic risks for high-impact models",
                        "atlan_solution": "Implement risk assessment workflows, track red team findings, and monitor model behavior through Atlan's governance features",
                        "features": ["Risk Workflows", "Assessment Tracking", "Monitoring Dashboards"]
                    },
                    "Article 53 - Downstream Provider Info": {
                        "requirement": "Provide adequate information to downstream providers",
                        "atlan_solution": "Publish model cards, API documentation, and usage guidelines through Atlan's collaboration features",
                        "features": ["API Catalog", "Documentation Hub", "Access Controls"]
                    },
                    "Article 55 - Cybersecurity Measures": {
                        "requirement": "Implement cybersecurity measures for GPAI models",
                        "atlan_solution": "Use Atlan's security features including access controls, audit trails, and anomaly detection for model endpoints",
                        "features": ["Security Controls", "Audit Logs", "Anomaly Detection"]
                    }
                }
            else:
                benefits_mapping = {
                    "Article 11 - Technical Documentation": {
                        "requirement": "Maintain comprehensive technical documentation",
                        "atlan_solution": "Use Atlan's metadata catalog to create detailed documentation for each AI system, including model cards, architecture diagrams, and performance metrics",
                        "features": ["Rich Text Documentation", "File Attachments", "Version Control"]
                    },
                    "Article 10 - Data Governance": {
                        "requirement": "Ensure data quality and bias testing",
                        "atlan_solution": "Leverage Atlan's data profiling and quality monitoring to track data characteristics, identify biases, and maintain quality thresholds",
                        "features": ["Data Profiling", "Quality Rules", "Anomaly Detection"]
                    },
                    "Article 12 - Record Keeping": {
                        "requirement": "Maintain logs of AI operations and decisions",
                        "atlan_solution": "Atlan's comprehensive audit logs and lineage tracking automatically capture all changes, access, and transformations",
                        "features": ["Audit Trails", "Change History", "Access Logs"]
                    },
                    "Article 14 - Human Oversight": {
                        "requirement": "Implement human oversight mechanisms",
                        "atlan_solution": "Configure approval workflows and review gates in Atlan to ensure human validation at critical decision points",
                        "features": ["Approval Workflows", "Review Gates", "Role-Based Access"]
                    },
                    "Article 9 - Risk Management": {
                        "requirement": "Systematic risk assessment and mitigation",
                        "atlan_solution": "Use Atlan's classification and tagging to identify high-risk systems and track mitigation measures",
                        "features": ["Risk Classifications", "Custom Tags", "Impact Analysis"]
                    },
                    "Article 26 - User Obligations": {
                        "requirement": "Monitor system performance and maintain human oversight",
                        "atlan_solution": "Create performance dashboards and configure alerts for anomalies, with clear escalation paths for human review",
                        "features": ["Performance Monitoring", "Alert Configuration", "Escalation Workflows"]
                    },
                    "Article 43 - Conformity Assessment": {
                        "requirement": "Conduct conformity assessments for high-risk systems",
                        "atlan_solution": "Use Atlan's workflow automation to implement systematic conformity assessment procedures with evidence tracking",
                        "features": ["Assessment Workflows", "Evidence Management", "Compliance Tracking"]
                    },
                    "Article 4 - AI Literacy": {
                        "requirement": "Ensure AI literacy among staff",
                        "atlan_solution": "Build knowledge bases and glossaries in Atlan to support AI literacy training and track completion",
                        "features": ["Knowledge Base", "Glossary Management", "Training Tracking"]
                    }
                }
            
            for article, details in benefits_mapping.items():
                with st.expander(f"📜 {article}"):
                    st.markdown(f"**Requirement:** {details['requirement']}")
                    st.success(f"**Atlan Solution:** {details['atlan_solution']}")
                    st.info(f"**Features to Use:** {', '.join(details['features'])}")
                    
        with rec_tab3:
            st.markdown("### 🚀 Quick Wins with Atlan")
            
            quick_wins = {
                "Week 1": {
                    "icon": "📊",
                    "title": "AI System Inventory",
                    "action": "Import all AI systems into Atlan catalog",
                    "benefit": "Immediate visibility into AI landscape",
                    "effort": "Low",
                    "impact": "High"
                },
                "Week 2": {
                    "icon": "🔍",
                    "title": "Data Lineage Mapping",
                    "action": "Connect training data sources to AI models",
                    "benefit": "Understand data dependencies",
                    "effort": "Medium",
                    "impact": "High"
                },
                "Week 3": {
                    "icon": "📝",
                    "title": "Documentation Templates",
                    "action": "Create standardized AI documentation templates",
                    "benefit": "Consistent compliance documentation",
                    "effort": "Low",
                    "impact": "Medium"
                },
                "Week 4": {
                    "icon": "🎯",
                    "title": "Risk Classifications",
                    "action": "Tag and classify AI systems by risk level",
                    "benefit": "Prioritized compliance efforts",
                    "effort": "Low",
                    "impact": "High"
                },
                "Week 5": {
                    "icon": "🔔",
                    "title": "Compliance Alerts",
                    "action": "Set up alerts for documentation gaps",
                    "benefit": "Proactive compliance management",
                    "effort": "Medium",
                    "impact": "High"
                },
                "Week 6": {
                    "icon": "📈",
                    "title": "Executive Dashboard",
                    "action": "Build compliance status dashboard",
                    "benefit": "Real-time compliance visibility",
                    "effort": "Medium",
                    "impact": "High"
                }
            }
            
            cols = st.columns(3)
            for idx, (week, details) in enumerate(quick_wins.items()):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 4px solid #2a5298; margin-bottom: 15px;">
                        <h4>{details['icon']} {week}: {details['title']}</h4>
                        <p><strong>Action:</strong> {details['action']}</p>
                        <p><strong>Benefit:</strong> {details['benefit']}</p>
                        <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                            <span style="color: #666;">Effort: {details['effort']}</span>
                            <span style="color: #2a5298; font-weight: bold;">Impact: {details['impact']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
            # ROI Calculator
            st.markdown("### 💰 Compliance ROI with Atlan")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **Time Savings:**
                - 70% reduction in documentation time
                - 80% faster compliance reporting
                - 60% less time on audit preparation
                
                **Risk Reduction:**
                - Avoid penalties up to €35M or 7% revenue
                - Prevent operational shutdowns
                - Reduce legal costs
                """)
                
            with col2:
                st.markdown("""
                **Operational Benefits:**
                - Single source of truth for AI governance
                - Automated compliance workflows
                - Real-time compliance monitoring
                
                **Strategic Value:**
                - Competitive advantage through compliance
                - Faster AI deployment with confidence
                - Enhanced stakeholder trust
                """)
                
        # EU AI Act Official Reference
        st.markdown("---")
        st.markdown("### 📜 EU AI Act Official Reference")
        
        st.info("""
        **Official EU AI Act (Regulation 2024/1689):**
        
        The Artificial Intelligence Act was adopted by the European Parliament on 13 March 2024 and by the Council on 21 May 2024.
        
        🔗 **Official Full Text**: [EUR-Lex - Regulation (EU) 2024/1689](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202401689)
        
        **Key Implementation Dates:**
        - 2 February 2025: Prohibited AI practices
        - 2 August 2025: GPAI model obligations  
        - 2 August 2026: High-risk AI systems
        - 2 August 2027: AI systems already on market
        """)
        
        # Download report option
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📥 Download Detailed Report", type="secondary", use_container_width=True):
                st.info("Report download functionality would be implemented here in production version.")
            
            if st.button("🔄 Take Assessment Again", use_container_width=True):
                st.session_state.page = 'landing'
                st.session_state.assessment_type = None
                if 'user_answers' in st.session_state:
                    del st.session_state.user_answers
                st.rerun()

# Add custom CSS for better styling
st.markdown("""
<style>
.stSelectbox > div > div {
    background-color: #f8f9fa;
}

.stProgress .st-bp {
    background-color: #667eea;
}

div[data-testid="metric-container"] {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stButton > button {
    font-weight: 600;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    padding-left: 20px;
    padding-right: 20px;
}
</style>
""", unsafe_allow_html=True)
