import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Atlan Rollout & Implementation Simulator", 
    layout="wide",
    page_icon="📊"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f2937;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f3f4f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }
    .risk-high {
        color: #dc2626;
        font-weight: bold;
    }
    .risk-medium {
        color: #f59e0b;
        font-weight: bold;
    }
    .risk-low {
        color: #10b981;
        font-weight: bold;
    }
    .recommendation-box {
        background-color: #fef3c7;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f59e0b;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# DAMA-DMBOK Aligned Maturity Framework with Atlan Implementation Focus
MATURITY_LEVELS = {
    "Level 0: Non-existent": {
        "description": "No awareness of data management needs",
        "characteristics": [
            "No data management practices",
            "Data managed in silos",
            "No data governance awareness",
            "High risk of data incidents"
        ],
        "dama_dimensions": {
            "Data Governance": "Non-existent",
            "Data Architecture": "Ad-hoc",
            "Data Quality": "Unmanaged",
            "Metadata": "None"
        },
        "atlan_readiness": {
            "implementation_focus": "Basic catalog setup - Start with asset inventory",
            "day_1_requirements": ["Executive sponsorship", "3-5 pilot data sources", "Basic team structure"],
            "ps_hours_estimate": "200-250 hours",
            "ps_focus": "Foundation setup & migration",
            "data_marketplace_readiness": "Not ready - Build foundation first"
        },
        "factor": 2.0
    },
    "Level 1: Initial/Ad-hoc": {
        "description": "Limited awareness, reactive approach",
        "characteristics": [
            "Inconsistent data practices",
            "Individual heroics",
            "Reactive problem solving",
            "Limited documentation"
        ],
        "dama_dimensions": {
            "Data Governance": "Informal",
            "Data Architecture": "Basic documentation",
            "Data Quality": "Issue-based",
            "Metadata": "Spreadsheet-based"
        },
        "atlan_readiness": {
            "implementation_focus": "Data Domains setup - Establish organizational structure",
            "day_1_requirements": ["Domain boundaries defined", "Data stewards identified", "Basic glossary"],
            "ps_hours_estimate": "150-200 hours",
            "ps_focus": "Domain setup & basic governance",
            "data_marketplace_readiness": "Basic discovery only"
        },
        "factor": 1.5
    },
    "Level 2: Repeatable": {
        "description": "Developing awareness, some processes",
        "characteristics": [
            "Some documented procedures",
            "Basic roles defined",
            "Emerging standards",
            "Project-based governance"
        ],
        "dama_dimensions": {
            "Data Governance": "Steering committee formed",
            "Data Architecture": "Logical models exist",
            "Data Quality": "Basic profiling",
            "Metadata": "Repository implemented (Atlan)"
        },
        "atlan_readiness": {
            "implementation_focus": "Data Products creation - Package domains into consumable products",
            "day_1_requirements": ["Business glossary", "Access policies", "Quality metrics", "Workflows"],
            "ps_hours_estimate": "120-150 hours",
            "ps_focus": "Product thinking & workflows",
            "data_marketplace_readiness": "Ready for basic self-service"
        },
        "factor": 1.3
    },
    "Level 3: Defined Process": {
        "description": "Formal standards and procedures",
        "characteristics": [
            "Enterprise standards defined",
            "Clear accountability",
            "Proactive management",
            "Integrated processes"
        ],
        "dama_dimensions": {
            "Data Governance": "Charter & policies active",
            "Data Architecture": "Enterprise models",
            "Data Quality": "Automated monitoring",
            "Metadata": "Active management"
        },
        "atlan_readiness": {
            "implementation_focus": "Full Data Marketplace - Self-service with governance",
            "day_1_requirements": ["Product catalog", "Automated workflows", "Quality SLAs", "Request management"],
            "ps_hours_estimate": "80-120 hours",
            "ps_focus": "Marketplace & automation",
            "data_marketplace_readiness": "Full self-service marketplace"
        },
        "factor": 1.1
    },
    "Level 4: Managed and Measurable": {
        "description": "Quantitative management and control",
        "characteristics": [
            "Metrics-driven decisions",
            "Predictable outcomes",
            "Risk-based approach",
            "Continuous monitoring"
        ],
        "dama_dimensions": {
            "Data Governance": "Metrics & KPIs tracked",
            "Data Architecture": "Impact analysis capable",
            "Data Quality": "SLA-driven",
            "Metadata": "Automated lineage"
        },
        "atlan_readiness": {
            "implementation_focus": "Advanced marketplace with analytics - Insights-driven governance",
            "day_1_requirements": ["Usage analytics", "API integrations", "Custom workflows", "Compliance automation"],
            "ps_hours_estimate": "60-80 hours",
            "ps_focus": "Advanced use cases",
            "data_marketplace_readiness": "Analytics-driven marketplace"
        },
        "factor": 1.0
    },
    "Level 5: Optimized": {
        "description": "Continuous improvement culture",
        "characteristics": [
            "Innovation in practices",
            "Self-organizing teams",
            "Predictive capabilities",
            "Business value focus"
        ],
        "dama_dimensions": {
            "Data Governance": "Value-driven optimization",
            "Data Architecture": "Adaptive architecture",
            "Data Quality": "Predictive quality",
            "Metadata": "AI-enhanced discovery"
        },
        "atlan_readiness": {
            "implementation_focus": "AI-powered marketplace - Predictive and proactive",
            "day_1_requirements": ["AI recommendations", "Predictive governance", "Data mesh", "Value optimization"],
            "ps_hours_estimate": "40-60 hours",
            "ps_focus": "Innovation & optimization",
            "data_marketplace_readiness": "AI-powered predictive marketplace"
        },
        "factor": 0.9
    }
}

# Atlan Feature Implementation Journey
ATLAN_FEATURE_JOURNEY = {
    "foundation": {
        "name": "Foundation Layer",
        "features": [
            "Asset discovery & cataloging",
            "Basic search functionality",
            "Connector setup",
            "User authentication (SSO)"
        ],
        "maturity_level": "Level 0-1",
        "timeline": "Weeks 1-4"
    },
    "data_domains": {
        "name": "Data Domains",
        "description": "Organizational structure for data ownership",
        "features": [
            "Domain boundaries definition",
            "Domain ownership assignment",
            "Domain-specific glossaries",
            "Domain-based access control"
        ],
        "prerequisites": ["Foundation layer complete", "Stewards identified"],
        "maturity_level": "Level 1-2",
        "timeline": "Weeks 4-8"
    },
    "data_products": {
        "name": "Data Products",
        "description": "Curated, packaged data assets for consumption",
        "features": [
            "Product templates & schemas",
            "Product ownership & SLAs",
            "Quality scorecards",
            "Consumer feedback loops"
        ],
        "prerequisites": ["Domains established", "Quality metrics defined"],
        "maturity_level": "Level 2-3",
        "timeline": "Weeks 8-12"
    },
    "governance_workflows": {
        "name": "Governance Workflows",
        "description": "Automated processes for data governance",
        "features": [
            "Access request workflows",
            "Data quality issue workflows",
            "Change approval processes",
            "Compliance workflows"
        ],
        "prerequisites": ["Policies defined", "Roles established"],
        "maturity_level": "Level 2-3",
        "timeline": "Weeks 6-10"
    },
    "data_marketplace": {
        "name": "Data Marketplace",
        "description": "Self-service data discovery and consumption",
        "features": [
            "Searchable product catalog",
            "Self-service access requests",
            "Usage analytics",
            "Consumer ratings & reviews"
        ],
        "prerequisites": ["Products created", "Workflows automated"],
        "maturity_level": "Level 3+",
        "timeline": "Weeks 12-16"
    }
}

# Professional Services Components
PS_COMPONENTS = {
    "TAM (Technical Account Manager)": {
        "responsibilities": [
            "Strategic planning & roadmap",
            "Stakeholder alignment",
            "Change management",
            "Adoption strategy",
            "Success metrics tracking"
        ],
        "hours_by_phase": {
            "Planning": 20,
            "Implementation": 40,
            "Rollout": 30,
            "Optimization": 10
        }
    },
    "CSA (Customer Solution Architect)": {
        "responsibilities": [
            "Technical architecture",
            "Integration design",
            "Migration strategy",
            "Best practices advisory",
            "Technical enablement"
        ],
        "hours_by_phase": {
            "Planning": 30,
            "Implementation": 50,
            "Rollout": 20,
            "Optimization": 20
        }
    },
    "Implementation Engineer": {
        "responsibilities": [
            "Connector setup",
            "Lineage configuration",
            "Custom integrations",
            "Technical troubleshooting",
            "Performance optimization"
        ],
        "hours_by_phase": {
            "Planning": 10,
            "Implementation": 60,
            "Rollout": 20,
            "Optimization": 10
        }
    }
}

# Day 1 Requirements for Data Marketplace
DAY_1_MARKETPLACE = {
    "technical_prerequisites": [
        "Atlan instance provisioned",
        "SSO/Azure AD integrated",
        "3-5 core data sources connected",
        "Basic lineage established",
        "Search functionality configured"
    ],
    "governance_prerequisites": [
        "Data stewards identified",
        "Basic access policies defined",
        "Business glossary started (50+ terms)",
        "Certification process defined",
        "Request workflows configured"
    ],
    "organizational_prerequisites": [
        "Executive sponsorship secured",
        "Communication plan launched",
        "Training schedule defined",
        "Success metrics identified",
        "Change champions appointed"
    ],
    "self_service_capabilities": [
        "Data discovery via search",
        "Business context understanding",
        "Access request workflows",
        "Basic quality indicators",
        "Collaboration features"
    ]
}

# DAMA-DMBOK Knowledge Area Progression
MATURITY_PROGRESSION = {
    "Level 0 → Level 1": [
        "Recognize data as an asset requiring management",
        "Identify key data stakeholders and pain points",
        "Document critical data elements and sources",
        "Establish basic data inventory",
        "Create awareness of data governance need"
    ],
    "Level 1 → Level 2": [
        "Form Data Governance Steering Committee",
        "Define data governance charter and scope",
        "Implement Atlan as metadata repository",
        "Create initial business glossary (50+ terms)",
        "Establish data steward roles",
        "Document data quality issues and impacts",
        "Create high-level data architecture diagrams"
    ],
    "Level 2 → Level 3": [
        "Develop comprehensive data policies and standards",
        "Implement data quality dimensions (Completeness, Accuracy, Timeliness, etc.)",
        "Build enterprise data models in Atlan",
        "Establish data lineage for critical data flows",
        "Create data security classification scheme",
        "Implement master data management for key domains",
        "Define data lifecycle management procedures"
    ],
    "Level 3 → Level 4": [
        "Implement automated data quality scorecards",
        "Establish data governance metrics and KPIs",
        "Deploy data observability and monitoring",
        "Create self-service data catalog with Atlan",
        "Implement reference data management",
        "Establish data privacy compliance framework",
        "Integrate metadata management with DevOps"
    ],
    "Level 4 → Level 5": [
        "Deploy ML-driven data quality predictions",
        "Implement real-time data governance",
        "Create data mesh/fabric architecture",
        "Establish data marketplace and monetization",
        "Implement automated compliance monitoring",
        "Enable citizen data steward programs",
        "Create innovation lab for data practices"
    ]
}

# DAMA-DMBOK Knowledge Areas for Assessment
DAMA_KNOWLEDGE_AREAS = {
    "Data Governance": {
        "description": "Overall management of data assets",
        "key_activities": ["Strategy", "Policy", "Standards", "Oversight", "Compliance"]
    },
    "Data Architecture": {
        "description": "Overall structure of data and data-related resources",
        "key_activities": ["Enterprise models", "Standards", "Integration", "Alignment"]
    },
    "Data Modeling & Design": {
        "description": "Analysis, design, building, testing, and maintenance",
        "key_activities": ["Conceptual models", "Logical models", "Physical models"]
    },
    "Data Storage & Operations": {
        "description": "Design, implementation, and support of stored data",
        "key_activities": ["Database operations", "Performance", "Retention", "Backup"]
    },
    "Data Security": {
        "description": "Ensuring privacy, confidentiality and appropriate access",
        "key_activities": ["Access control", "Encryption", "Monitoring", "Classification"]
    },
    "Data Integration & Interoperability": {
        "description": "Acquisition, extraction, transformation, movement",
        "key_activities": ["ETL/ELT", "Virtualization", "Replication", "CDC"]
    },
    "Document & Content Management": {
        "description": "Managing data found in unstructured sources",
        "key_activities": ["Capture", "Storage", "Access", "Retention"]
    },
    "Reference & Master Data": {
        "description": "Managing shared data to meet organizational goals",
        "key_activities": ["Golden records", "Hierarchies", "Cross-reference", "Distribution"]
    },
    "Data Warehousing & Business Intelligence": {
        "description": "Managing analytical data and enabling access",
        "key_activities": ["Design", "Development", "Analytics", "Reporting"]
    },
    "Metadata Management": {
        "description": "Managing data about data and data processes",
        "key_activities": ["Business metadata", "Technical metadata", "Lineage", "Impact analysis"]
    },
    "Data Quality": {
        "description": "Planning and implementation of quality management techniques",
        "key_activities": ["Profiling", "Monitoring", "Cleansing", "Reporting"]
    }
}

# Landing Page
def landing_page():
    st.markdown('<h1 class="main-header">🚀 Atlan Rollout & Implementation Simulator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform your data governance journey with DAMA-DMBOK aligned planning and Atlan Professional Services</p>', unsafe_allow_html=True)
    
    # Key Questions Banner
    st.warning("🤔 **Key Questions Answered:** What's the right implementation sequence? How many PS hours do you need? When can you launch a self-service data marketplace?")
    
    # DAMA Badge
    st.info("📘 **Aligned with DAMA-DMBOK Framework** - Industry standard for data management best practices")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
        <h3>📈 Rollout Simulator</h3>
        <p>Predict timeline, estimate PS hours, and identify risks for your Atlan implementation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
        <h3>📊 DAMA Maturity Assessment</h3>
        <p>Feature sequence guidance, PS requirements, and marketplace readiness assessment</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
        <h3>🏗️ Implementation Planner</h3>
        <p>Create parallel workstreams with PS allocation across TAM, CSA, and Engineers</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # New Section: Implementation Journey
    st.header("🛤️ Typical Atlan Implementation Journey")
    
    journey_col1, journey_col2, journey_col3, journey_col4, journey_col5 = st.columns(5)
    
    with journey_col1:
        st.markdown("""
        **📦 Foundation**
        (Weeks 1-4)
        - Asset catalog
        - Connectors
        - Basic search
        - SSO setup
        """)
    
    with journey_col2:
        st.markdown("""
        **🏢 Data Domains**
        (Weeks 4-8)
        - Org structure
        - Ownership
        - Stewardship
        - Boundaries
        """)
    
    with journey_col3:
        st.markdown("""
        **⚡ Workflows**
        (Weeks 6-10)
        - Access requests
        - Approvals
        - Quality issues
        - Automation
        """)
    
    with journey_col4:
        st.markdown("""
        **🎯 Data Products**
        (Weeks 8-12)
        - Package assets
        - Define SLAs
        - Quality scores
        - Templates
        """)
    
    with journey_col5:
        st.markdown("""
        **🏪 Marketplace**
        (Weeks 12-16)
        - Self-service
        - Discovery
        - Analytics
        - Reviews
        """)
    
    st.markdown("---")
    
    # Quick Insights
    st.header("💡 Quick Insights")
    
    insight_col1, insight_col2, insight_col3 = st.columns(3)
    
    with insight_col1:
        st.markdown("""
        **🚀 Implementation Sequence**
        1. Foundation setup (mandatory)
        2. Data Domains (organization)
        3. Governance Workflows
        4. Data Products (packaging)
        5. Data Marketplace (self-service)
        """)
    
    with insight_col2:
        st.markdown("""
        **👥 Typical PS Hours**
        - **Foundation**: 70 hours
        - **Domain Implementation**: 120 hours
        - **Training & Adoption**: 10 hours
        - **Total**: ~200 hours
        """)
    
    with insight_col3:
        st.markdown("""
        **🏪 Marketplace Prerequisites**
        - ✓ Domains established
        - ✓ Products defined
        - ✓ Workflows automated
        - ✓ 50+ glossary terms
        - ✓ Training complete
        """)
    
    st.markdown("---")
    
    # Professional Services Overview
    st.header("👥 Atlan Professional Services Team")
    
    ps_col1, ps_col2, ps_col3 = st.columns(3)
    
    with ps_col1:
        st.markdown("""
        **Technical Account Manager (TAM)**
        - Strategic planning
        - Stakeholder alignment
        - Change management
        - Adoption strategy
        - ~100 hours typical
        """)
    
    with ps_col2:
        st.markdown("""
        **Customer Solution Architect (CSA)**
        - Architecture design
        - Migration strategy
        - Best practices
        - Technical enablement
        - ~120 hours typical
        """)
    
    with ps_col3:
        st.markdown("""
        **Implementation Engineer**
        - Connector setup
        - Lineage configuration
        - Custom integrations
        - Performance tuning
        - ~80 hours typical
        """)
    
    st.markdown("---")
    
    # Success Metrics
    st.header("📊 Success Metrics from Real Implementations")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Time to Foundation", "4 weeks", "Basic catalog ready")
    with col2:
        st.metric("Time to Marketplace", "12-16 weeks", "Full self-service")
    with col3:
        st.metric("PS Investment", "$75-200K", "Based on scope")
    with col4:
        st.metric("User Adoption", "78%", "Within 6 months")
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Start Rollout Simulation", use_container_width=True):
            st.session_state.page = 'rollout'
            st.rerun()
    
    with col2:
        if st.button("📊 Assess DAMA Maturity", use_container_width=True):
            st.session_state.page = 'maturity'
            st.rerun()
    
    with col3:
        if st.button("🏗️ Plan Implementation", use_container_width=True):
            st.session_state.page = 'implementation'
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.caption("📘 Based on DAMA-DMBOK v2 Framework | 💰 PS pricing at $375/hour (typical Atlan rate)")

# Maturity Assessment Page
def maturity_assessment():
    st.title("📊 DAMA-DMBOK Maturity Assessment")
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.page = 'landing'
        st.rerun()
    
    st.markdown("""
    This assessment aligns with DAMA-DMBOK (Data Management Body of Knowledge) framework, 
    evaluating your organization across 11 knowledge areas of data management.
    """)
    
    st.markdown("---")
    
    # Assessment Mode Selection
    assessment_mode = st.radio(
        "Choose Assessment Mode",
        ["Quick Assessment", "Detailed DAMA Knowledge Area Assessment"],
        horizontal=True
    )
    
    if assessment_mode == "Detailed DAMA Knowledge Area Assessment":
        st.header("📋 DAMA Knowledge Area Assessment")
        
        # Create assessment for each knowledge area
        knowledge_scores = {}
        
        with st.expander("📊 Rate your maturity in each DAMA Knowledge Area", expanded=True):
            for area, details in DAMA_KNOWLEDGE_AREAS.items():
                st.markdown(f"**{area}**")
                st.caption(details["description"])
                score = st.select_slider(
                    f"Current maturity",
                    options=["Non-existent", "Initial", "Repeatable", "Defined", "Managed", "Optimized"],
                    value="Initial",
                    key=f"ka_{area}"
                )
                knowledge_scores[area] = ["Non-existent", "Initial", "Repeatable", "Defined", "Managed", "Optimized"].index(score)
                st.markdown("---")
        
        # Calculate overall maturity
        avg_score = sum(knowledge_scores.values()) / len(knowledge_scores)
        current_maturity = list(MATURITY_LEVELS.keys())[int(avg_score)]
        
        # Visualization of knowledge areas
        st.header("🎯 Knowledge Area Maturity Radar")
        
        # Create radar chart
        categories = list(DAMA_KNOWLEDGE_AREAS.keys())
        values = list(knowledge_scores.values())
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Current State',
            line_color='blue'
        ))
        
        # Add target state (example: all at level 3)
        target_values = [3] * len(categories)
        fig_radar.add_trace(go.Scatterpolar(
            r=target_values,
            theta=categories,
            fill='toself',
            name='Target State',
            line_color='green',
            opacity=0.3
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5],
                    ticktext=["Non-existent", "Initial", "Repeatable", "Defined", "Managed", "Optimized"],
                    tickvals=[0, 1, 2, 3, 4, 5]
                )),
            showlegend=True,
            title="DAMA Knowledge Areas Maturity Assessment"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Gap Analysis
        st.header("📊 Gap Analysis")
        
        gap_data = []
        for area, score in knowledge_scores.items():
            gap = 3 - score  # Assuming target is level 3 (Defined)
            gap_data.append({
                "Knowledge Area": area,
                "Current": score,
                "Target": 3,
                "Gap": gap
            })
        
        gap_df = pd.DataFrame(gap_data)
        gap_df = gap_df.sort_values("Gap", ascending=False)
        
        fig_gap = px.bar(gap_df, x="Knowledge Area", y="Gap", 
                         title="Maturity Gap by Knowledge Area",
                         color="Gap",
                         color_continuous_scale="Reds")
        fig_gap.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_gap, use_container_width=True)
        
    else:
        # Quick Assessment Mode
        col1, col2 = st.columns(2)
        
        with col1:
            current_maturity = st.selectbox(
                "Current Maturity Level",
                list(MATURITY_LEVELS.keys()),
                help="Select your organization's current data governance maturity based on DAMA-DMBOK"
            )
        
        with col2:
            target_maturity = st.selectbox(
                "Target Maturity Level",
                list(MATURITY_LEVELS.keys()),
                index=3,
                help="Select your desired maturity level"
            )
    
    # Maturity Visualization
    st.header("🎯 Maturity Journey Visualization")
    
    # Create progression chart
    levels = list(MATURITY_LEVELS.keys())
    current_idx = levels.index(current_maturity)
    target_idx = levels.index(target_maturity)
    
    if current_idx < target_idx:
        # Create Sankey diagram for progression
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=[level.split(":")[0] for level in levels],
                color=["#ef4444" if i == current_idx else "#10b981" if i == target_idx else "#6b7280" for i in range(len(levels))]
            ),
            link=dict(
                source=[i for i in range(current_idx, target_idx)],
                target=[i+1 for i in range(current_idx, target_idx)],
                value=[1] * (target_idx - current_idx)
            )
        )])
        
        fig.update_layout(
            title_text="Your Data Governance Maturity Journey (DAMA-DMBOK Framework)",
            font_size=12,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show current and target maturity details with Atlan-specific guidance
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📍 Current State")
            current_level = MATURITY_LEVELS[current_maturity]
            st.markdown(f"**{current_maturity}**")
            st.markdown(f"*{current_level['description']}*")
            
            with st.expander("Characteristics"):
                for char in current_level['characteristics']:
                    st.markdown(f"• {char}")
            
            if 'dama_dimensions' in current_level:
                with st.expander("DAMA Dimensions"):
                    for dim, status in current_level['dama_dimensions'].items():
                        st.markdown(f"**{dim}:** {status}")
            
            if 'atlan_readiness' in current_level:
                with st.expander("🚀 Atlan Implementation Focus", expanded=True):
                    ar = current_level['atlan_readiness']
                    st.markdown(f"**Focus Area:** {ar['implementation_focus']}")
                    st.markdown("**Day 1 Requirements:**")
                    for req in ar['day_1_requirements']:
                        st.markdown(f"• {req}")
                    st.metric("PS Hours Needed", ar['ps_hours_estimate'])
                    st.info(f"**PS Focus:** {ar['ps_focus']}")
                    st.warning(f"**Marketplace Readiness:** {ar['data_marketplace_readiness']}")
        
        with col2:
            st.markdown("### 🎯 Target State")
            target_level = MATURITY_LEVELS[target_maturity]
            st.markdown(f"**{target_maturity}**")
            st.markdown(f"*{target_level['description']}*")
            
            with st.expander("Characteristics"):
                for char in target_level['characteristics']:
                    st.markdown(f"• {char}")
            
            if 'dama_dimensions' in target_level:
                with st.expander("DAMA Dimensions"):
                    for dim, status in target_level['dama_dimensions'].items():
                        st.markdown(f"**{dim}:** {status}")
            
            if 'atlan_readiness' in target_level:
                with st.expander("🎯 Target Capabilities"):
                    ar = target_level['atlan_readiness']
                    st.markdown(f"**Implementation:** {ar['implementation_focus']}")
                    st.markdown("**Key Capabilities:**")
                    for req in ar['day_1_requirements']:
                        st.markdown(f"• {req}")
                    st.success(f"**Marketplace Status:** {ar['data_marketplace_readiness']}")
        
        # Atlan Feature Implementation Journey
        st.header("🚀 Atlan Feature Implementation Journey")
        
        st.info("**Key Insight:** Data Domains and Data Products are complementary features in Atlan, not alternatives. Here's the typical implementation sequence:")
        
        # Create visual journey
        journey_tabs = st.tabs(["📦 Foundation", "🏢 Data Domains", "🎯 Data Products", "⚡ Workflows", "🏪 Marketplace"])
        
        with journey_tabs[0]:
            foundation = ATLAN_FEATURE_JOURNEY["foundation"]
            st.markdown(f"### {foundation['name']}")
            st.markdown(f"**Maturity Required:** {foundation['maturity_level']}")
            st.markdown(f"**Timeline:** {foundation['timeline']}")
            st.markdown("**Features to Implement:**")
            for feature in foundation['features']:
                st.checkbox(feature, key=f"found_{feature}")
            
            progress = sum([st.session_state.get(f"found_{feature}", False) for feature in foundation['features']])
            st.progress(progress / len(foundation['features']))
            
        with journey_tabs[1]:
            domains = ATLAN_FEATURE_JOURNEY["data_domains"]
            st.markdown(f"### {domains['name']}")
            st.markdown(f"*{domains['description']}*")
            st.markdown(f"**Maturity Required:** {domains['maturity_level']}")
            st.markdown(f"**Timeline:** {domains['timeline']}")
            
            st.warning("**Prerequisites:**")
            for prereq in domains['prerequisites']:
                st.markdown(f"• {prereq}")
            
            st.success("**What You'll Implement:**")
            for feature in domains['features']:
                st.markdown(f"✓ {feature}")
            
            st.metric("PS Hours for Domains", "40-60 hours", "TAM + CSA focus")
            
        with journey_tabs[2]:
            products = ATLAN_FEATURE_JOURNEY["data_products"]
            st.markdown(f"### {products['name']}")
            st.markdown(f"*{products['description']}*")
            st.markdown(f"**Maturity Required:** {products['maturity_level']}")
            st.markdown(f"**Timeline:** {products['timeline']}")
            
            st.warning("**Prerequisites:**")
            for prereq in products['prerequisites']:
                st.markdown(f"• {prereq}")
            
            st.success("**What You'll Implement:**")
            for feature in products['features']:
                st.markdown(f"✓ {feature}")
            
            st.metric("PS Hours for Products", "60-80 hours", "CSA + Engineer focus")
            
        with journey_tabs[3]:
            workflows = ATLAN_FEATURE_JOURNEY["governance_workflows"]
            st.markdown(f"### {workflows['name']}")
            st.markdown(f"*{workflows['description']}*")
            st.markdown(f"**Maturity Required:** {workflows['maturity_level']}")
            st.markdown(f"**Timeline:** {workflows['timeline']}")
            
            st.warning("**Prerequisites:**")
            for prereq in workflows['prerequisites']:
                st.markdown(f"• {prereq}")
            
            st.success("**What You'll Implement:**")
            for feature in workflows['features']:
                st.markdown(f"✓ {feature}")
            
            st.metric("PS Hours for Workflows", "30-40 hours", "TAM + Engineer focus")
            
        with journey_tabs[4]:
            marketplace = ATLAN_FEATURE_JOURNEY["data_marketplace"]
            st.markdown(f"### {marketplace['name']}")
            st.markdown(f"*{marketplace['description']}*")
            st.markdown(f"**Maturity Required:** {marketplace['maturity_level']}")
            st.markdown(f"**Timeline:** {marketplace['timeline']}")
            
            st.warning("**Prerequisites:**")
            for prereq in marketplace['prerequisites']:
                st.markdown(f"• {prereq}")
            
            st.success("**What You'll Get:**")
            for feature in marketplace['features']:
                st.markdown(f"✓ {feature}")
            
            st.metric("PS Hours for Marketplace", "20-30 hours", "Full team collaboration")
        
        # Implementation Sequence Visualization
        st.header("📊 Typical Implementation Sequence")
        
        sequence_df = pd.DataFrame({
            'Phase': ['Foundation', 'Data Domains', 'Governance Workflows', 'Data Products', 'Data Marketplace'],
            'Start_Week': [0, 4, 6, 8, 12],
            'Duration': [4, 4, 4, 4, 4],
            'Maturity_Required': [0, 1, 2, 2, 3]
        })
        
        fig_sequence = go.Figure()
        
        colors = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#EF4444']
        
        for idx, row in sequence_df.iterrows():
            fig_sequence.add_trace(go.Bar(
                name=row['Phase'],
                y=[row['Phase']],
                x=[row['Duration']],
                base=[row['Start_Week']],
                orientation='h',
                marker_color=colors[idx],
                text=f"Weeks {row['Start_Week']}-{row['Start_Week']+row['Duration']}",
                textposition='inside',
                hovertemplate=f"<b>{row['Phase']}</b><br>" +
                              f"Start: Week {row['Start_Week']}<br>" +
                              f"Duration: {row['Duration']} weeks<br>" +
                              f"Maturity Level: {row['Maturity_Required']}+<extra></extra>"
            ))
        
        fig_sequence.update_layout(
            title="Atlan Feature Implementation Timeline",
            xaxis_title="Weeks",
            yaxis_title="Features",
            barmode='stack',
            showlegend=False,
            height=300,
            xaxis=dict(range=[0, 20])
        )
        
        # Add phase markers
        fig_sequence.add_vline(x=4, line_dash="dot", line_color="gray", opacity=0.5)
        fig_sequence.add_vline(x=8, line_dash="dot", line_color="gray", opacity=0.5)
        fig_sequence.add_vline(x=12, line_dash="dot", line_color="gray", opacity=0.5)
        fig_sequence.add_vline(x=16, line_dash="dot", line_color="gray", opacity=0.5)
        
        st.plotly_chart(fig_sequence, use_container_width=True)
        
        # Key Insights
        st.markdown("""
        ### 💡 Key Implementation Insights:
        
        1. **Foundation First** (Weeks 1-4): Basic catalog setup is non-negotiable
        2. **Domains Before Products** (Weeks 4-8): Establish organizational structure before packaging
        3. **Workflows Enable Self-Service** (Weeks 6-10): Automation is key to marketplace success
        4. **Products Package Value** (Weeks 8-12): Transform domains into consumable assets
        5. **Marketplace Crowns It All** (Weeks 12-16): Full self-service requires all prior elements
        
        > **Note:** While phases overlap, each builds on the previous. Attempting to jump directly to marketplace without foundation will fail.
        """)
        
        # Professional Services Estimation
        st.header("👥 Professional Services Requirements")
        
        # Get more context for accurate PS estimation
        col1_context, col2_context = st.columns(2)
        
        with col1_context:
            target_timeline = st.select_slider(
                "Target Go-Live Timeline",
                options=["3 months", "6 months", "9 months", "12 months"],
                value="6 months",
                help="Faster timelines require more concentrated PS support"
            )
            
            num_data_sources = st.number_input(
                "Number of Data Sources",
                min_value=1,
                max_value=50,
                value=5,
                help="More sources = more integration complexity"
            )
        
        with col2_context:
            implementation_scope = st.multiselect(
                "Implementation Scope",
                ["Basic Catalog", "Data Domains", "Data Products", "Governance Workflows", 
                 "Data Quality", "Data Marketplace", "API Integrations", "Custom Solutions"],
                default=["Basic Catalog", "Data Domains", "Governance Workflows"],
                help="Select all features you plan to implement"
            )
            
            existing_tool_migration = st.radio(
                "Migrating from existing tool?",
                ["No", "Yes - Simple tool", "Yes - Complex tool (e.g., Collibra)"],
                help="Migration adds complexity"
            )
        
        # Calculate PS hours based on real factors
        base_hours = 200  # Standard SOW baseline
        
        # Timeline multiplier
        timeline_multipliers = {
            "3 months": 1.4,   # Rushed = more parallel PS support needed
            "6 months": 1.0,   # Standard pace
            "9 months": 0.9,   # Relaxed pace
            "12 months": 0.85  # Very relaxed, can optimize PS usage
        }
        timeline_mult = timeline_multipliers[target_timeline]
        
        # Scope multiplier
        scope_hours = {
            "Basic Catalog": 0,  # Included in base
            "Data Domains": 0,   # Included in base
            "Data Products": 40,
            "Governance Workflows": 0,  # Included in base
            "Data Quality": 30,
            "Data Marketplace": 50,
            "API Integrations": 40,
            "Custom Solutions": 60
        }
        additional_scope_hours = sum(scope_hours.get(item, 0) for item in implementation_scope)
        
        # Data source complexity
        source_multiplier = 1.0
        if num_data_sources > 5:
            source_multiplier += (num_data_sources - 5) * 0.02  # 2% per additional source
        
        # Migration complexity
        migration_hours = {
            "No": 0,
            "Yes - Simple tool": 30,
            "Yes - Complex tool (e.g., Collibra)": 70  # Matches SOW
        }
        migration_add = migration_hours[existing_tool_migration]
        
        # Maturity gap multiplier
        maturity_gap = target_idx - current_idx
        maturity_multiplier = 1.0 + (maturity_gap - 1) * 0.15 if maturity_gap > 1 else 1.0
        
        # Calculate total
        calculated_hours = int((base_hours + additional_scope_hours + migration_add) * 
                              timeline_mult * source_multiplier * maturity_multiplier)
        
        # Display calculation breakdown
        st.markdown("### 📊 PS Hours Calculation")
        
        with st.expander("See detailed calculation", expanded=True):
            calc_df = pd.DataFrame({
                "Component": [
                    "Base Package (Catalog + Domains + Workflows)",
                    "Additional Scope",
                    "Migration Effort",
                    "Timeline Factor",
                    "Source Complexity Factor",
                    "Maturity Gap Factor"
                ],
                "Hours/Factor": [
                    f"{base_hours} hours",
                    f"+{additional_scope_hours} hours",
                    f"+{migration_add} hours",
                    f"×{timeline_mult}",
                    f"×{source_multiplier:.2f}",
                    f"×{maturity_multiplier:.2f}"
                ],
                "Running Total": [
                    base_hours,
                    base_hours + additional_scope_hours,
                    base_hours + additional_scope_hours + migration_add,
                    int((base_hours + additional_scope_hours + migration_add) * timeline_mult),
                    int((base_hours + additional_scope_hours + migration_add) * timeline_mult * source_multiplier),
                    calculated_hours
                ]
            })
            st.dataframe(calc_df, use_container_width=True)
        
        # Investment summary
        hourly_rate = 375
        total_investment = calculated_hours * hourly_rate
        
        col1_inv, col2_inv, col3_inv = st.columns(3)
        with col1_inv:
            st.metric("Total PS Hours", f"{calculated_hours}", 
                     f"{'+' if calculated_hours > 200 else ''}{calculated_hours - 200} vs standard")
        with col2_inv:
            st.metric("Investment", f"${total_investment:,}", "at $375/hour")
        with col3_inv:
            package_type = "Standard" if calculated_hours <= 220 else "Extended" if calculated_hours <= 350 else "Enterprise"
            st.metric("Package Type", package_type)
        
        # Team allocation based on actual needs
        st.markdown("### 👥 Recommended Team Allocation")
        
        # Dynamic allocation based on scope
        tam_pct = 0.35 if "Data Marketplace" in implementation_scope else 0.30
        csa_pct = 0.45 if migration_add > 0 else 0.40
        eng_pct = 1 - tam_pct - csa_pct
        
        team_hours = {
            "TAM": int(calculated_hours * tam_pct),
            "CSA": int(calculated_hours * csa_pct),
            "Engineer": int(calculated_hours * eng_pct)
        }
        
        fig_team = go.Figure(data=[
            go.Pie(labels=list(team_hours.keys()), 
                   values=list(team_hours.values()),
                   hole=.3)
        ])
        fig_team.update_layout(title="PS Hours by Role")
        
        col1_team, col2_team = st.columns([1, 1])
        with col1_team:
            st.plotly_chart(fig_team, use_container_width=True)
        
        with col2_team:
            st.markdown("### Hours by Role")
            for role, hours in team_hours.items():
                st.metric(role, f"{hours} hours", f"${hours * hourly_rate:,}")
        
        # Day 1 Data Marketplace Requirements
        st.header("🏪 Day 1: Data Marketplace & Self-Service")
        
        st.info("**Goal:** Enable self-service data discovery and access from Day 1")
        
        day1_tabs = st.tabs(["Technical Setup", "Governance Setup", "Organization Setup", "Self-Service Features"])
        
        with day1_tabs[0]:
            st.markdown("#### Technical Prerequisites")
            for item in DAY_1_MARKETPLACE["technical_prerequisites"]:
                st.checkbox(item, key=f"tech_{item}")
            
            progress = sum([st.session_state.get(f"tech_{item}", False) for item in DAY_1_MARKETPLACE["technical_prerequisites"]])
            st.progress(progress / len(DAY_1_MARKETPLACE["technical_prerequisites"]))
        
        with day1_tabs[1]:
            st.markdown("#### Governance Prerequisites")
            for item in DAY_1_MARKETPLACE["governance_prerequisites"]:
                st.checkbox(item, key=f"gov_{item}")
            
            progress = sum([st.session_state.get(f"gov_{item}", False) for item in DAY_1_MARKETPLACE["governance_prerequisites"]])
            st.progress(progress / len(DAY_1_MARKETPLACE["governance_prerequisites"]))
        
        with day1_tabs[2]:
            st.markdown("#### Organizational Prerequisites")
            for item in DAY_1_MARKETPLACE["organizational_prerequisites"]:
                st.checkbox(item, key=f"org_{item}")
            
            progress = sum([st.session_state.get(f"org_{item}", False) for item in DAY_1_MARKETPLACE["organizational_prerequisites"]])
            st.progress(progress / len(DAY_1_MARKETPLACE["organizational_prerequisites"]))
        
        with day1_tabs[3]:
            st.markdown("#### Self-Service Capabilities Available Day 1")
            for item in DAY_1_MARKETPLACE["self_service_capabilities"]:
                st.markdown(f"✅ {item}")
            
            st.success("These capabilities enable immediate value realization and user adoption")
        
        # Show progression requirements
        st.header("📋 Requirements for Each Transition")
        
        for i in range(current_idx, target_idx):
            transition = f"{levels[i].split(':')[0]} → {levels[i+1].split(':')[0]}"
            with st.expander(f"**{transition}**", expanded=(i == current_idx)):
                requirements = MATURITY_PROGRESSION.get(transition, [])
                
                # Group requirements by DAMA knowledge area
                st.markdown("#### Key Actions:")
                for j, req in enumerate(requirements, 1):
                    if "Atlan" in req:
                        st.markdown(f"{j}. **{req}** 🚀")
                    else:
                        st.markdown(f"{j}. {req}")
                
                # Add Atlan-specific capabilities for this level
                st.markdown("#### Atlan Capabilities to Leverage:")
                if i == 0:  # Level 0 to 1
                    st.markdown("""
                    - Basic metadata cataloging
                    - Asset discovery and inventory
                    - Simple search capabilities
                    """)
                elif i == 1:  # Level 1 to 2
                    st.markdown("""
                    - Business glossary management
                    - Data lineage visualization
                    - Collaboration features
                    - Basic data quality tracking
                    """)
                elif i == 2:  # Level 2 to 3
                    st.markdown("""
                    - Automated metadata harvesting
                    - Policy enforcement
                    - Data quality scorecards
                    - Integration with data platforms
                    """)
                elif i == 3:  # Level 3 to 4
                    st.markdown("""
                    - Advanced analytics on metadata
                    - Automated compliance monitoring
                    - Self-service data discovery
                    - API-driven governance
                    """)
                elif i == 4:  # Level 4 to 5
                    st.markdown("""
                    - AI-powered recommendations
                    - Predictive data quality
                    - Real-time governance metrics
                    - Data mesh enablement
                    """)
        
        # Timeline estimation
        st.header("⏱️ Estimated Timeline")
        
        # More sophisticated timeline based on DAMA experience
        transition_times = {
            "Level 0 → Level 1": 2,
            "Level 1 → Level 2": 3,
            "Level 2 → Level 3": 4,
            "Level 3 → Level 4": 6,
            "Level 4 → Level 5": 6
        }
        
        total_time = 0
        timeline_details = []
        
        for i in range(current_idx, target_idx):
            transition = f"{levels[i].split(':')[0]} → {levels[i+1].split(':')[0]}"
            time = transition_times.get(transition, 3)
            total_time += time
            timeline_details.append((transition, time))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Duration", f"{total_time} months")
        with col2:
            st.metric("Levels to Progress", target_idx - current_idx)
        with col3:
            st.metric("Key Milestones", (target_idx - current_idx) * 5)
        
        # Create timeline visualization
        if timeline_details:
            timeline_df = pd.DataFrame(timeline_details, columns=["Transition", "Duration"])
            timeline_df["Start"] = timeline_df["Duration"].cumsum() - timeline_df["Duration"]
            timeline_df["End"] = timeline_df["Duration"].cumsum()
            
            fig_timeline = px.timeline(
                timeline_df,
                x_start=[pd.Timestamp('2024-01-01') + pd.Timedelta(days=int(d*30)) for d in timeline_df['Start']],
                x_end=[pd.Timestamp('2024-01-01') + pd.Timedelta(days=int(d*30)) for d in timeline_df['End']],
                y="Transition",
                title="Maturity Progression Timeline"
            )
            
            fig_timeline.update_yaxes(categoryorder="total ascending")
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Action Plan with DAMA focus
        st.header("🎯 DAMA-Aligned Action Plan")
        
        st.markdown("""
        <div class="recommendation-box">
        <h4>Phase 1: Foundation (Months 1-3)</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if current_idx == 0:  # Level 0
            st.markdown("""
            1. **Data Governance**
               - Establish executive sponsorship
               - Form initial governance team
               - Create data governance charter
            
            2. **Metadata Management with Atlan**
               - Deploy Atlan platform
               - Connect 3-5 critical data sources
               - Begin asset documentation
            
            3. **Data Architecture**
               - Document high-level data landscape
               - Identify critical data flows
               - Map key systems and interfaces
            """)
        elif current_idx == 1:  # Level 1
            st.markdown("""
            1. **Data Governance**
               - Formalize governance operating model
               - Define RACI for data decisions
               - Establish data council meetings
            
            2. **Data Quality**
               - Define quality dimensions
               - Implement basic profiling in Atlan
               - Create issue tracking process
            
            3. **Master Data Management**
               - Identify master data domains
               - Define golden record sources
               - Build initial business glossary
            """)
        elif current_idx == 2:  # Level 2
            st.markdown("""
            1. **Data Architecture**
               - Create enterprise data models
               - Implement data integration standards
               - Design target state architecture
            
            2. **Data Security**
               - Implement classification scheme
               - Define access control policies
               - Enable monitoring in Atlan
            
            3. **Business Intelligence**
               - Establish self-service analytics
               - Create certified datasets
               - Build KPI dashboards
            """)
        
        # ROI Projection aligned with DAMA metrics
        st.header("💰 Expected Benefits (DAMA-Aligned)")
        
        benefits_data = {
            'Benefit Category': ['Reduced Data Incidents', 'Faster Decision Making', 'Compliance Readiness', 
                               'Productivity Gains', 'Data Quality Improvement'],
            'Year 1': [20, 15, 25, 30, 10],
            'Year 2': [35, 30, 40, 45, 25],
            'Year 3': [50, 45, 60, 60, 40]
        }
        
        benefits_df = pd.DataFrame(benefits_data)
        
        fig_benefits = px.bar(benefits_df, x='Benefit Category', y=['Year 1', 'Year 2', 'Year 3'],
                             title="Expected Improvement by Category (%)",
                             barmode='group')
        st.plotly_chart(fig_benefits, use_container_width=True)
        
        # Knowledge Area Priority
        st.header("📊 Recommended Knowledge Area Priority")
        
        priority_areas = {
            0: ["Data Governance", "Metadata Management", "Data Architecture"],
            1: ["Data Quality", "Data Security", "Master Data Management"],
            2: ["Data Integration", "Business Intelligence", "Data Modeling"],
            3: ["Reference Data", "Document Management", "Data Warehousing"],
            4: ["Advanced Analytics", "Data Science", "Real-time Processing"]
        }
        
        current_priorities = priority_areas.get(current_idx, [])
        
        st.info(f"**Focus Areas for {current_maturity.split(':')[0]}:**")
        for i, area in enumerate(current_priorities, 1):
            st.markdown(f"{i}. **{area}** - Critical for progression")
        
        # Success Factors
        st.header("✅ Critical Success Factors")
        
        col1_sf, col2_sf = st.columns(2)
        
        with col1_sf:
            st.markdown("**Organizational Factors**")
            st.markdown("""
            - Executive sponsorship and visibility
            - Dedicated data governance team
            - Clear communication strategy
            - Change management program
            - Regular training and education
            """)
        
        with col2_sf:
            st.markdown("**Technical Factors**")
            st.markdown("""
            - Atlan platform optimization
            - Integration with key systems
            - Automated metadata collection
            - Data quality monitoring
            - Self-service enablement
            """)
        
    else:
        st.warning("Please select a target maturity level higher than your current level to see the progression path.")

# Rollout Simulator Page
def rollout_simulator():
    st.title("📈 Atlan Rollout Plan Simulator")
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.page = 'landing'
        st.rerun()
    
    st.markdown("""
    This simulator helps estimate your Atlan rollout timeline based on organizational factors and surfaces risks with targeted interventions.
    """)
    
    # Create two columns for inputs
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("📊 Organization Profile")
        
        org_type = st.selectbox("Organization Type", ["Growth", "Enterprise", "Major Enterprise"])
        num_domains = st.slider("Number of Data Domains", 1, 20, 5)
        num_users = st.number_input("Expected Active Users", 10, 5000, 100, step=50)
        
        maturity = st.selectbox("Current DAMA Maturity Level", list(MATURITY_LEVELS.keys()))
        
        adoption_support = st.selectbox("Adoption Support Available", [
            "Low - Limited CDO/DA support, no training org", 
            "Medium - Some training & comms in place", 
            "High - Strong enablement, change management"
        ])
        
        exec_sponsorship = st.radio("Executive Sponsorship Confirmed?", ["Yes", "No"])
        timeline = st.slider("Target Rollout Timeline (months)", 3, 12, 6)
        
        st.header("🛠️ Adoption Accelerators")
        
        exec_connects = st.selectbox("Executive Connects Cadence", ["None", "Monthly", "Bi-weekly", "Weekly"])
        workshops_type = st.multiselect("Workshops Planned", 
            ["Architecture Review", "Admin Training", "End User Training", "Use Case Discovery", "Data Quality Workshop"])
        champion_strength = st.selectbox("Champion Network", ["Weak", "Moderate", "Strong", "Very Strong"])
        user_interviews = st.slider("User Interviews Planned", 0, 50, 15)
        change_mgmt = st.checkbox("Formal Change Management Program")
        dedicated_team = st.checkbox("Dedicated Implementation Team")
    
    with col2:
        # Calculate metrics
        base_duration = {"Growth": 3, "Enterprise": 6, "Major Enterprise": 9}
        support_factor = {"Low": 1.5, "Medium": 1.2, "High": 1.0}
        champion_boost = {"Weak": 1.3, "Moderate": 1.1, "Strong": 0.9, "Very Strong": 0.8}
        exec_boost = {"None": 1.3, "Monthly": 1.1, "Bi-weekly": 0.95, "Weekly": 0.9}
        
        maturity_adjustment = MATURITY_LEVELS[maturity]["factor"]
        domain_factor = 1 + (num_domains - 5) * 0.03
        user_factor = 1 + (num_users - 100) * 0.0001
        exec_penalty = 1.3 if exec_sponsorship == "No" else 1.0
        interview_impact = 1 - min(user_interviews * 0.005, 0.2)
        workshop_impact = 1 - (len(workshops_type) * 0.03)
        change_mgmt_factor = 0.85 if change_mgmt else 1.0
        dedicated_team_factor = 0.9 if dedicated_team else 1.0
        
        expected_duration = (
            base_duration[org_type] *
            support_factor[adoption_support.split()[0]] *
            maturity_adjustment *
            domain_factor *
            user_factor *
            exec_penalty *
            exec_boost[exec_connects] *
            champion_boost[champion_strength] *
            interview_impact *
            workshop_impact *
            change_mgmt_factor *
            dedicated_team_factor
        )
        
        # Risk calculation
        risk_factors = [
            ("Executive Sponsorship", exec_penalty, exec_sponsorship == "No"),
            ("Adoption Support", support_factor[adoption_support.split()[0]], adoption_support.startswith("Low")),
            ("Champion Network", champion_boost[champion_strength], champion_strength == "Weak"),
            ("User Research", interview_impact, user_interviews < 15),
            ("Training Program", workshop_impact, len(workshops_type) < 3),
            ("Change Management", change_mgmt_factor, not change_mgmt),
            ("Team Resources", dedicated_team_factor, not dedicated_team)
        ]
        
        high_risks = sum(1 for _, _, is_risk in risk_factors if is_risk)
        risk_score = min(100, int(high_risks * 15))
        
        # Display metrics with PS hours
        st.header("📊 Rollout Analysis")
        
        col1_metrics, col2_metrics, col3_metrics, col4_metrics = st.columns(4)
        
        with col1_metrics:
            st.metric("Expected Duration", f"{expected_duration:.1f} months", 
                     f"{expected_duration - timeline:.1f} vs target",
                     delta_color="inverse")
        
        with col2_metrics:
            risk_label = "High" if risk_score > 60 else "Medium" if risk_score > 30 else "Low"
            st.metric("Risk Score", f"{risk_score}/100", risk_label)
        
        with col3_metrics:
            success_prob = max(20, min(95, 100 - risk_score + len(workshops_type) * 5))
            st.metric("Success Probability", f"{success_prob}%")
        
        with col4_metrics:
            # PS hours based on actual factors
            base_ps_hours = 200  # Standard SOW
            
            # Timeline factor - rushed timelines need more PS support
            timeline_factor = 1.0
            if timeline <= 3:
                timeline_factor = 1.3  # 30% more hours for aggressive timeline
            elif timeline >= 9:
                timeline_factor = 0.9  # 10% less for relaxed timeline
            
            # Scope factor - more domains/users need more hours
            scope_factor = 1.0
            if num_domains > 5:
                scope_factor += (num_domains - 5) * 0.05  # 5% more per additional domain
            if num_users > 200:
                scope_factor += 0.2  # 20% more for large user base
            
            # Maturity factor - lower maturity needs more guidance
            maturity_factors = {
                "Level 0": 1.3,
                "Level 1": 1.15,
                "Level 2": 1.0,
                "Level 3": 0.9,
                "Level 4": 0.8,
                "Level 5": 0.7
            }
            maturity_key = maturity.split(":")[0].strip()
            maturity_factor = maturity_factors.get(maturity_key, 1.0)
            
            ps_hours = int(base_ps_hours * timeline_factor * scope_factor * maturity_factor)
            st.metric("PS Hours Needed", f"{ps_hours} hrs", f"${ps_hours * 375:,}")
        
        # PS Hours Breakdown Section
        st.header("👥 Professional Services Allocation")
        
        # Show how PS hours were calculated
        with st.expander("📊 How PS Hours Were Calculated", expanded=True):
            st.markdown(f"""
            **Base Package:** 200 hours (standard SOW)
            
            **Adjustments Applied:**
            - **Timeline Factor:** {timeline_factor:.1f}x ({timeline} month target)
            - **Scope Factor:** {scope_factor:.1f}x ({num_domains} domains, {num_users} users)
            - **Maturity Factor:** {maturity_factor:.1f}x ({maturity_key})
            
            **Total Hours:** {base_ps_hours} × {timeline_factor:.1f} × {scope_factor:.1f} × {maturity_factor:.1f} = **{ps_hours} hours**
            
            **Investment:** {ps_hours} hours × $375/hour = **${ps_hours * 375:,}**
            """)
        
        ps_col1, ps_col2 = st.columns([2, 1])
        
        with ps_col1:
            # Dynamic PS allocation based on calculated hours
            st.markdown("### PS Hours Distribution")
            
            # Allocate hours proportionally
            foundation_pct = 0.35
            domain_pct = 0.50
            training_pct = 0.15
            
            ps_allocation = {
                "Phase": ["Foundation & Setup", "Domain Implementation", "Training & Adoption"],
                "% of Total": [f"{foundation_pct*100:.0f}%", f"{domain_pct*100:.0f}%", f"{training_pct*100:.0f}%"],
                "Hours": [
                    int(ps_hours * foundation_pct),
                    int(ps_hours * domain_pct),
                    int(ps_hours * training_pct)
                ],
                "Focus": ["Technical setup, migration", "Use cases, workflows, governance", "Enablement, adoption"]
            }
            
            # Role distribution
            tam_split = 0.35  # 35% TAM
            csa_split = 0.40  # 40% CSA
            eng_split = 0.25  # 25% Engineer
            
            ps_allocation["TAM"] = [
                int(ps_hours * foundation_pct * 0.2),
                int(ps_hours * domain_pct * 0.5),
                int(ps_hours * training_pct * 0.9)
            ]
            ps_allocation["CSA"] = [
                int(ps_hours * foundation_pct * 0.4),
                int(ps_hours * domain_pct * 0.3),
                int(ps_hours * training_pct * 0.1)
            ]
            ps_allocation["Engineer"] = [
                int(ps_hours * foundation_pct * 0.4),
                int(ps_hours * domain_pct * 0.2),
                int(ps_hours * training_pct * 0.0)
            ]
            
            ps_df = pd.DataFrame(ps_allocation)
            st.dataframe(ps_df.set_index("Phase"), use_container_width=True)
        
        with ps_col2:
            # PS package recommendations
            st.markdown("### Package Recommendation")
            
            if ps_hours <= 220:
                st.success("""
                **Standard Package**
                - 200 hours base
                - Single domain focus
                - 3-month timeline
                """)
            elif ps_hours <= 350:
                st.warning("""
                **Extended Package**
                - 300+ hours
                - Multi-domain rollout
                - Complex integrations
                """)
            else:
                st.error("""
                **Enterprise Package**
                - 400+ hours
                - Full transformation
                - Phased approach recommended
                """)
            
            # Key factors affecting hours
            st.markdown("### Key Factors")
            if timeline <= 3:
                st.warning("⚡ Aggressive timeline increases PS needs")
            if num_domains > 5:
                st.info(f"📊 {num_domains} domains require phased approach")
            if maturity_key in ["Level 0", "Level 1"]:
                st.warning("🎯 Low maturity requires more guidance")
        
        # Timeline Distribution
        st.header("📈 Timeline Distribution Analysis")
        
        # Monte Carlo simulation
        np.random.seed(42)
        simulations = 5000
        results = []
        
        for _ in range(simulations):
            # Add variability to each factor
            var_duration = expected_duration * np.random.normal(1.0, 0.15)
            results.append(var_duration)
        
        results = np.array(results)
        
        # Create histogram with plotly
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=results,
            nbinsx=30,
            name='Simulated Outcomes',
            marker_color='lightblue',
            opacity=0.7
        ))
        
        fig.add_vline(x=timeline, line_dash="dash", line_color="red", 
                     annotation_text=f"Target: {timeline} months")
        fig.add_vline(x=expected_duration, line_dash="dash", line_color="green", 
                     annotation_text=f"Expected: {expected_duration:.1f} months")
        
        fig.update_layout(
            title="Monte Carlo Simulation of Rollout Timeline (5000 runs)",
            xaxis_title="Duration (months)",
            yaxis_title="Frequency",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Success metrics
        on_time_probability = (results <= timeline).mean() * 100
        p50 = np.percentile(results, 50)
        p90 = np.percentile(results, 90)
        
        col1_prob, col2_prob, col3_prob = st.columns(3)
        with col1_prob:
            st.metric("On-Time Probability", f"{on_time_probability:.1f}%")
        with col2_prob:
            st.metric("50% Confidence", f"{p50:.1f} months")
        with col3_prob:
            st.metric("90% Confidence", f"{p90:.1f} months")
        
        # Risk Analysis
        st.header("⚠️ Risk Analysis & Mitigation")
        
        risk_df = pd.DataFrame([
            {"Factor": name, "Impact": f"{(factor-1)*100:.0f}%", "Status": "🔴 High Risk" if is_risk else "🟢 Managed"}
            for name, factor, is_risk in risk_factors
        ])
        
        st.dataframe(risk_df, use_container_width=True, hide_index=True)
        
        # Recommendations
        st.header("✅ Prioritized Recommendations")
        
        recommendations = []
        
        if exec_sponsorship == "No":
            recommendations.append(("🚨 Critical", "Secure executive sponsorship immediately - this is the #1 success factor"))
        
        if exec_connects == "None":
            recommendations.append(("⚠️ High", "Establish bi-weekly executive connects to maintain momentum"))
        
        if len(workshops_type) < 3:
            recommendations.append(("⚠️ High", f"Plan {3-len(workshops_type)} additional workshops: Architecture Review and End User Training are essential"))
        
        if user_interviews < 15:
            recommendations.append(("📋 Medium", f"Conduct {15-user_interviews} more user interviews to understand requirements"))
        
        if champion_strength in ["Weak", "Moderate"]:
            recommendations.append(("📋 Medium", "Identify and empower 5-7 strong champions across different domains"))
        
        if not change_mgmt:
            recommendations.append(("📋 Medium", "Implement formal change management program with communication plan"))
        
        if not dedicated_team:
            recommendations.append(("💡 Low", "Consider dedicated team for faster implementation"))
        
        for priority, rec in recommendations:
            st.markdown(f"{priority}: {rec}")
        
        # Implementation Roadmap
        st.header("🗓️ Suggested Implementation Roadmap")
        
        phases = [
            ("Discovery & Planning", 0.15),
            ("Technical Setup", 0.20),
            ("Pilot Implementation", 0.25),
            ("Rollout & Training", 0.25),
            ("Optimization", 0.15)
        ]
        
        roadmap_data = []
        current_end = 0
        
        for phase, percentage in phases:
            duration = expected_duration * percentage
            roadmap_data.append({
                "Phase": phase,
                "Start": current_end,
                "Duration": duration,
                "End": current_end + duration
            })
            current_end += duration
        
        roadmap_df = pd.DataFrame(roadmap_data)
        
        fig_gantt = px.timeline(
            roadmap_df,
            x_start=[pd.Timestamp('2024-01-01') + pd.Timedelta(days=int(d*30)) for d in roadmap_df['Start']],
            x_end=[pd.Timestamp('2024-01-01') + pd.Timedelta(days=int(d*30)) for d in roadmap_df['End']],
            y="Phase",
            title="Implementation Timeline"
        )
        
        fig_gantt.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig_gantt, use_container_width=True)

# Implementation Planner Page
def implementation_planner():
    st.title("🏗️ Atlan Implementation Planner")
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.page = 'landing'
        st.rerun()
    
    st.markdown("""
    Create a detailed implementation plan with phase-wise breakdown, parallel workstreams, dependencies, and risk management strategies.
    """)
    
    with st.form("implementation_form"):
        st.header("📋 Project Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Project Name", placeholder="e.g., Enterprise Data Governance Initiative")
            start_date = st.date_input("Start Date", datetime.now())
            duration_months = st.number_input("Duration (months)", 3, 24, 6)
        
        with col2:
            team_size = st.number_input("Implementation Team Size", 1, 20, 5)
            budget = st.number_input("Budget ($K)", 50, 1000, 200, step=50)
            priority_domains = st.multiselect("Priority Domains", 
                ["Finance", "Sales", "Marketing", "Operations", "HR", "Product", "Engineering"])
        
        st.header("🎯 Implementation Approach")
        
        implementation_type = st.radio(
            "Select Implementation Strategy",
            ["Sequential (Waterfall)", "Parallel Workstreams", "Hybrid (Parallel with Dependencies)"],
            index=2,
            help="Most organizations benefit from a hybrid approach with parallel workstreams"
        )
        
        st.header("📊 Workstreams & Phases")
        
        if implementation_type in ["Parallel Workstreams", "Hybrid (Parallel with Dependencies)"]:
            st.info("💡 Define parallel workstreams that can run concurrently")
            
            # Workstream 1: Technical Foundation
            with st.expander("**Workstream 1: Technical Foundation**", expanded=True):
                tech_tasks = st.text_area(
                    "Key Activities",
                    value="• Atlan instance provisioning\n• Infrastructure setup\n• Security configuration\n• SSO integration\n• Performance optimization",
                    height=100,
                    key="tech_tasks"
                )
                tech_start = st.slider("Start Week", 0, 12, 0, key="tech_start")
                tech_duration = st.slider("Duration (weeks)", 1, 20, 4, key="tech_dur")
                tech_deps = st.multiselect("Dependencies", ["None", "Executive Approval", "Budget Approval"], default=["None"], key="tech_deps")
            
            # Workstream 2: Data Source Integration
            with st.expander("**Workstream 2: Data Source Integration**", expanded=True):
                integration_tasks = st.text_area(
                    "Key Activities",
                    value="• Connector configuration\n• Metadata harvesting\n• Lineage setup\n• Data quality rules\n• Integration testing",
                    height=100,
                    key="int_tasks"
                )
                int_start = st.slider("Start Week", 0, 12, 2, key="int_start")
                int_duration = st.slider("Duration (weeks)", 2, 24, 8, key="int_dur")
                int_deps = st.multiselect("Dependencies", ["Technical Foundation", "Data Owner Approval", "Architecture Review"], 
                                         default=["Technical Foundation"], key="int_deps")
            
            # Workstream 3: Governance Framework
            with st.expander("**Workstream 3: Governance Framework**", expanded=True):
                gov_tasks = st.text_area(
                    "Key Activities",
                    value="• Policy development\n• Business glossary\n• Stewardship model\n• Process documentation\n• Compliance mapping",
                    height=100,
                    key="gov_tasks"
                )
                gov_start = st.slider("Start Week", 0, 12, 0, key="gov_start")
                gov_duration = st.slider("Duration (weeks)", 2, 20, 6, key="gov_dur")
                gov_deps = st.multiselect("Dependencies", ["Stakeholder Alignment", "Legal Review"], 
                                         default=["Stakeholder Alignment"], key="gov_deps")
            
            # Workstream 4: User Enablement
            with st.expander("**Workstream 4: User Enablement**", expanded=True):
                user_tasks = st.text_area(
                    "Key Activities",
                    value="• Training program design\n• User onboarding\n• Documentation creation\n• Champion network\n• Adoption tracking",
                    height=100,
                    key="user_tasks"
                )
                user_start = st.slider("Start Week", 0, 12, 3, key="user_start")
                user_duration = st.slider("Duration (weeks)", 4, 24, 10, key="user_dur")
                user_deps = st.multiselect("Dependencies", ["Technical Foundation", "Governance Framework", "Pilot Success"], 
                                          default=["Technical Foundation"], key="user_deps")
            
            # Workstream 5: Value Realization
            with st.expander("**Workstream 5: Value Realization**", expanded=True):
                value_tasks = st.text_area(
                    "Key Activities",
                    value="• Use case implementation\n• ROI measurement\n• Success metrics\n• Optimization\n• Expansion planning",
                    height=100,
                    key="value_tasks"
                )
                value_start = st.slider("Start Week", 0, 12, 4, key="value_start")
                value_duration = st.slider("Duration (weeks)", 4, 20, 12, key="value_dur")
                value_deps = st.multiselect("Dependencies", ["Initial Adoption", "Metrics Baseline"], 
                                           default=["Initial Adoption"], key="value_deps")
            
        else:
            # Sequential Implementation
            st.subheader("1️⃣ Discovery Phase")
            discovery_tasks = st.text_area(
                "Key Tasks",
                value="• Stakeholder mapping and interviews\n• Current state assessment\n• Data landscape documentation\n• Success criteria definition\n• Technical architecture review"
            )
            discovery_duration = st.slider("Duration (weeks)", 1, 8, 2, key="disc_dur_seq")
            
            st.subheader("2️⃣ Setup Phase")
            setup_tasks = st.text_area(
                "Key Tasks",
                value="• Atlan instance provisioning\n• Connector configuration\n• SSO and security setup\n• Initial user provisioning\n• Integration testing"
            )
            setup_duration = st.slider("Duration (weeks)", 1, 8, 3, key="setup_dur_seq")
            
            st.subheader("3️⃣ Pilot Phase")
            pilot_tasks = st.text_area(
                "Key Tasks",
                value="• Metadata harvesting for pilot domains\n• Business glossary creation\n• Data quality rules setup\n• Lineage validation\n• Pilot user training"
            )
            pilot_duration = st.slider("Duration (weeks)", 2, 12, 4, key="pilot_dur_seq")
            
            st.subheader("4️⃣ Rollout Phase")
            rollout_tasks = st.text_area(
                "Key Tasks",
                value="• Phased domain onboarding\n• End-user training programs\n• Process integration\n• Adoption tracking\n• Success metrics monitoring"
            )
            rollout_duration = st.slider("Duration (weeks)", 4, 20, 8, key="rollout_dur_seq")
            
            st.subheader("5️⃣ Optimization Phase")
            optimization_tasks = st.text_area(
                "Key Tasks",
                value="• Advanced automation setup\n• Custom integration development\n• Performance optimization\n• Governance process refinement\n• ROI measurement"
            )
            optimization_duration = st.slider("Duration (weeks)", 2, 12, 4, key="opt_dur_seq")
        
        st.header("🎯 Critical Milestones")
        
        milestones = st.text_area(
            "Define Key Milestones",
            value="Week 2: Atlan instance live\nWeek 4: First data source connected\nWeek 6: Pilot domain live\nWeek 8: Business glossary launched\nWeek 12: 50% user adoption\nWeek 16: All domains onboarded\nWeek 20: ROI demonstrated",
            height=100
        )
        
        st.header("⚠️ Risk Management")
        
        col1_risk, col2_risk = st.columns(2)
        
        with col1_risk:
            st.subheader("Atlan-Side Risks")
            atlan_risks = st.text_area(
                "Identify risks",
                value="• Connector availability delays\n• Custom feature requests\n• Performance at scale\n• Integration complexity"
            )
        
        with col2_risk:
            st.subheader("Customer-Side Risks")
            customer_risks = st.text_area(
                "Identify risks",
                value="• Stakeholder availability\n• Data quality issues\n• Change resistance\n• Resource constraints"
            )
        
        st.header("📊 Success Metrics")
        
        success_metrics = st.multiselect(
            "Select KPIs to track",
            [
                "Time to discover data (reduction %)",
                "Data incident resolution time",
                "Business glossary coverage",
                "Active user adoption rate",
                "Data quality score improvement",
                "Compliance audit readiness",
                "Self-service analytics usage",
                "Cross-team collaboration index"
            ],
            default=["Active user adoption rate", "Time to discover data (reduction %)", "Business glossary coverage"]
        )
        
        submitted = st.form_submit_button("Generate Implementation Plan", type="primary")
    
    if submitted:
        st.success("✅ Implementation Plan Generated Successfully!")
        
        # Executive Summary
        st.header("📄 Executive Summary")
        
        col1_summary, col2_summary, col3_summary, col4_summary = st.columns(4)
        
        with col1_summary:
            st.metric("Implementation Type", implementation_type.split()[0])
        with col2_summary:
            st.metric("Team Size", f"{team_size} members")
        with col3_summary:
            st.metric("Budget", f"${budget}K")
        with col4_summary:
            st.metric("Priority Domains", len(priority_domains))
        
        # Timeline visualization based on implementation type
        st.header("📅 Implementation Timeline")
        
        if implementation_type in ["Parallel Workstreams", "Hybrid (Parallel with Dependencies)"]:
            # Create Gantt chart for parallel workstreams
            workstreams = [
                {
                    "Workstream": "Technical Foundation",
                    "Start": tech_start,
                    "Duration": tech_duration,
                    "Dependencies": tech_deps,
                    "Color": "#3B82F6"
                },
                {
                    "Workstream": "Data Integration",
                    "Start": int_start,
                    "Duration": int_duration,
                    "Dependencies": int_deps,
                    "Color": "#10B981"
                },
                {
                    "Workstream": "Governance Framework",
                    "Start": gov_start,
                    "Duration": gov_duration,
                    "Dependencies": gov_deps,
                    "Color": "#F59E0B"
                },
                {
                    "Workstream": "User Enablement",
                    "Start": user_start,
                    "Duration": user_duration,
                    "Dependencies": user_deps,
                    "Color": "#8B5CF6"
                },
                {
                    "Workstream": "Value Realization",
                    "Start": value_start,
                    "Duration": value_duration,
                    "Dependencies": value_deps,
                    "Color": "#EF4444"
                }
            ]
            
            # Create timeline visualization
            fig_timeline = go.Figure()
            
            # Add bars for each workstream
            for ws in workstreams:
                fig_timeline.add_trace(go.Bar(
                    name=ws["Workstream"],
                    y=[ws["Workstream"]],
                    x=[ws["Duration"]],
                    base=[ws["Start"]],
                    orientation='h',
                    marker_color=ws["Color"],
                    text=f"{ws['Duration']} weeks",
                    textposition='inside',
                    hovertemplate=f"<b>{ws['Workstream']}</b><br>" +
                                  f"Start: Week {ws['Start']}<br>" +
                                  f"Duration: {ws['Duration']} weeks<br>" +
                                  f"End: Week {ws['Start'] + ws['Duration']}<br>" +
                                  f"Dependencies: {', '.join(ws['Dependencies'])}<extra></extra>"
                ))
            
            # Add milestone markers
            milestone_weeks = [2, 4, 6, 8, 12, 16, 20]
            milestone_labels = ["Instance Live", "First Source", "Pilot Live", "Glossary Launch", 
                               "50% Adoption", "Full Coverage", "ROI Demo"]
            
            for week, label in zip(milestone_weeks, milestone_labels):
                fig_timeline.add_vline(x=week, line_dash="dot", line_color="red", opacity=0.5)
                fig_timeline.add_annotation(x=week, y=4.5, text=label, showarrow=False, 
                                          textangle=-45, font_size=10)
            
            fig_timeline.update_layout(
                title="Parallel Workstream Timeline with Dependencies",
                xaxis_title="Weeks",
                yaxis_title="Workstreams",
                barmode='stack',
                showlegend=False,
                height=400,
                xaxis=dict(range=[0, 25])
            )
            
            st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Dependency visualization
            st.subheader("🔗 Workstream Dependencies")
            
            dependency_matrix = pd.DataFrame({
                "Workstream": ["Technical", "Integration", "Governance", "Enablement", "Value"],
                "Technical": ["—", "Required", "Independent", "Required", "Indirect"],
                "Integration": ["—", "—", "Independent", "Provides Data", "Required"],
                "Governance": ["—", "—", "—", "Provides Framework", "Required"],
                "Enablement": ["—", "—", "—", "—", "Required"],
                "Value": ["—", "—", "—", "—", "—"]
            })
            
            st.dataframe(dependency_matrix.set_index("Workstream"), use_container_width=True)
            
            # Resource allocation across workstreams
            st.subheader("👥 Resource Allocation")
            
            resource_data = pd.DataFrame({
                "Workstream": ["Technical", "Integration", "Governance", "Enablement", "Value"],
                "FTEs Required": [2, 3, 2, 2, 1],
                "Peak Week": [2, 6, 4, 8, 12]
            })
            
            fig_resource = px.bar(resource_data, x="Workstream", y="FTEs Required", 
                                 title="Resource Requirements by Workstream",
                                 color="FTEs Required", color_continuous_scale="Blues")
            st.plotly_chart(fig_resource, use_container_width=True)
            
        else:
            # Sequential timeline
            phases_timeline = [
                {"Phase": "Discovery", "Start": 0, "Duration": discovery_duration},
                {"Phase": "Setup", "Start": discovery_duration, "Duration": setup_duration},
                {"Phase": "Pilot", "Start": discovery_duration + setup_duration, "Duration": pilot_duration},
                {"Phase": "Rollout", "Start": discovery_duration + setup_duration + pilot_duration, "Duration": rollout_duration},
                {"Phase": "Optimization", "Start": discovery_duration + setup_duration + pilot_duration + rollout_duration, "Duration": optimization_duration}
            ]
            
            timeline_df = pd.DataFrame(phases_timeline)
            
            fig_timeline = go.Figure()
            
            for idx, row in timeline_df.iterrows():
                fig_timeline.add_trace(go.Bar(
                    x=[row['Duration']],
                    y=[row['Phase']],
                    base=[row['Start']],
                    orientation='h',
                    name=row['Phase'],
                    text=f"{row['Duration']} weeks",
                    textposition='inside'
                ))
            
            fig_timeline.update_layout(
                title="Sequential Phase Timeline",
                xaxis_title="Weeks",
                barmode='stack',
                showlegend=False,
                height=300
            )
            
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Critical Path Analysis
        st.header("🎯 Critical Path Analysis")
        
        if implementation_type in ["Parallel Workstreams", "Hybrid (Parallel with Dependencies)"]:
            st.info("""
            **Critical Path**: Technical Foundation → Data Integration → User Enablement → Value Realization
            
            **Key Insights:**
            - Technical foundation is on the critical path - any delay impacts overall timeline
            - Governance framework can run in parallel without impacting critical path
            - User enablement depends on both technical and governance workstreams
            - Early wins possible through pilot implementations in week 6
            """)
            
            # Show float/slack for non-critical activities
            st.subheader("⏱️ Schedule Flexibility")
            
            float_data = pd.DataFrame({
                "Workstream": ["Technical Foundation", "Data Integration", "Governance Framework", 
                              "User Enablement", "Value Realization"],
                "Float (weeks)": [0, 0, 3, 1, 0],
                "Criticality": ["Critical", "Critical", "Flexible", "Near-Critical", "Critical"]
            })
            
            st.dataframe(float_data, use_container_width=True)
        
        # Professional Services Hours Planning
        st.header("👥 Professional Services Hours Planning")
        
        if implementation_type in ["Parallel Workstreams", "Hybrid (Parallel with Dependencies)"]:
            # PS allocation for parallel workstreams
            ps_workstream_hours = {
                "Technical Foundation": {"TAM": 10, "CSA": 30, "Engineer": 30, "Total": 70},
                "Data Integration": {"TAM": 15, "CSA": 25, "Engineer": 40, "Total": 80},
                "Governance Framework": {"TAM": 40, "CSA": 20, "Engineer": 10, "Total": 70},
                "User Enablement": {"TAM": 25, "CSA": 15, "Engineer": 10, "Total": 50},
                "Value Realization": {"TAM": 10, "CSA": 10, "Engineer": 10, "Total": 30}
            }
            
            ps_ws_df = pd.DataFrame(ps_workstream_hours).T
            st.dataframe(ps_ws_df, use_container_width=True)
            
            # Visualize PS hours by workstream
            fig_ps_ws = go.Figure()
            
            workstreams = list(ps_workstream_hours.keys())
            tam_hrs = [ps_workstream_hours[ws]["TAM"] for ws in workstreams]
            csa_hrs = [ps_workstream_hours[ws]["CSA"] for ws in workstreams]
            eng_hrs = [ps_workstream_hours[ws]["Engineer"] for ws in workstreams]
            
            fig_ps_ws.add_trace(go.Bar(name='TAM', x=workstreams, y=tam_hrs))
            fig_ps_ws.add_trace(go.Bar(name='CSA', x=workstreams, y=csa_hrs))
            fig_ps_ws.add_trace(go.Bar(name='Engineer', x=workstreams, y=eng_hrs))
            
            fig_ps_ws.update_layout(
                title="PS Hours by Workstream and Role",
                xaxis_title="Workstreams",
                yaxis_title="Hours",
                barmode='stack'
            )
            
            st.plotly_chart(fig_ps_ws, use_container_width=True)
            
            # PS timeline and peak loading
            st.subheader("🗓️ PS Resource Loading Over Time")
            
            ps_timeline_data = []
            for week in range(1, 17):
                if week <= 4:
                    ps_load = {"Week": week, "TAM": 5, "CSA": 10, "Engineer": 10}
                elif week <= 8:
                    ps_load = {"Week": week, "TAM": 10, "CSA": 8, "Engineer": 8}
                elif week <= 12:
                    ps_load = {"Week": week, "TAM": 8, "CSA": 5, "Engineer": 5}
                else:
                    ps_load = {"Week": week, "TAM": 3, "CSA": 2, "Engineer": 2}
                ps_timeline_data.append(ps_load)
            
            ps_timeline_df = pd.DataFrame(ps_timeline_data)
            
            fig_ps_timeline = px.area(ps_timeline_df, x='Week', y=['TAM', 'CSA', 'Engineer'],
                                     title="PS Hours per Week (Stacked)")
            st.plotly_chart(fig_ps_timeline, use_container_width=True)
        
        # Total PS Investment Calculator
        st.header("💰 PS Investment Calculator")
        
        col1_calc, col2_calc = st.columns(2)
        
        with col1_calc:
            st.markdown("### Standard SOW Package")
            st.markdown("""
            - **Foundation & Setup:** 70 hours
            - **Domain Implementation:** 120 hours  
            - **Training & Adoption:** 10 hours
            - **Total:** 200 hours
            - **Investment:** $75,000
            """)
            
            st.success("✅ Covers one domain implementation")
        
        with col2_calc:
            st.markdown("### Your Estimated Needs")
            
            # Calculate based on inputs
            base_hours = 200
            domain_multiplier = max(1, len(priority_domains) / 3)  # Every 3 domains adds complexity
            team_efficiency = 1 - (min(team_size, 10) - 5) * 0.02  # Larger teams = some efficiency
            
            estimated_hours = int(base_hours * domain_multiplier * team_efficiency)
            estimated_cost = estimated_hours * 375
            
            st.markdown(f"""
            - **Domains to implement:** {len(priority_domains)}
            - **Team size factor:** {team_efficiency:.2f}x
            - **Estimated hours:** {estimated_hours}
            - **Estimated investment:** ${estimated_cost:,}
            """)
            
            if estimated_hours > 200:
                st.warning(f"⚠️ You may need {estimated_hours - 200} additional hours beyond standard package")
        
        # Milestone Tracking
        st.header("📍 Milestone Tracking Dashboard")
        
        milestone_data = pd.DataFrame({
            "Milestone": ["Instance Live", "First Integration", "Pilot Launch", "Glossary Ready", 
                         "Training Complete", "Full Rollout", "ROI Achieved"],
            "Target Week": [2, 4, 6, 8, 12, 16, 20],
            "Status": ["Not Started", "Not Started", "Not Started", "Not Started", 
                      "Not Started", "Not Started", "Not Started"],
            "Owner": ["Technical Lead", "Integration Lead", "Program Manager", "Governance Lead",
                     "Enablement Lead", "Program Manager", "Value Lead"]
        })
        
        st.dataframe(milestone_data, use_container_width=True)
        
        # Success Metrics Tracking
        st.header("📈 Success Metrics Tracking Plan")
        
        st.info("Selected KPIs will be tracked throughout the implementation:")
        
        metrics_timeline = pd.DataFrame({
            "Metric": success_metrics,
            "Baseline (Week 0)": ["0%", "0%", "0%"],
            "Target (Week 8)": ["30%", "50%", "40%"],
            "Target (Week 16)": ["60%", "75%", "70%"],
            "Target (Week 24)": ["85%", "90%", "95%"]
        })
        
        st.dataframe(metrics_timeline, use_container_width=True)
        
        # Communication Plan
        st.header("📢 Communication Plan")
        
        comm_plan = pd.DataFrame({
            "Audience": ["Executive Sponsors", "Data Stewards", "End Users", "IT Teams"],
            "Frequency": ["Bi-weekly", "Weekly", "Monthly", "Weekly"],
            "Channel": ["Steering Committee", "Working Groups", "Town Halls", "Tech Syncs"],
            "Key Messages": ["Progress & Risks", "Implementation Details", "Benefits & Training", "Technical Updates"]
        })
        
        st.dataframe(comm_plan, use_container_width=True)
        
        # Next Steps
        st.header("👉 Immediate Next Steps")
        
        col1_next, col2_next = st.columns(2)
        
        with col1_next:
            st.markdown("""
            **Week 1 Actions:**
            1. Finalize workstream leads
            2. Schedule kickoff meetings
            3. Set up project tools
            4. Create communication channels
            5. Baseline current metrics
            """)
        
        with col2_next:
            st.markdown("""
            **Week 2 Actions:**
            1. Complete technical setup
            2. Begin governance framework
            3. Identify pilot candidates
            4. Start user interviews
            5. Define success criteria
            """)
        
        # Export options
        st.markdown("---")
        col1_export, col2_export = st.columns(2)
        
        with col1_export:
            st.download_button(
                label="📥 Download Implementation Plan",
                data="Implementation plan with parallel workstreams would be exported here",
                file_name=f"{project_name}_implementation_plan.pdf",
                mime="application/pdf"
            )
        
        with col2_export:
            st.download_button(
                label="📊 Download Project Schedule",
                data="Detailed schedule with dependencies would be exported here",
                file_name=f"{project_name}_schedule.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# Main app logic
def main():
    # Sidebar navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50/4F46E5/FFFFFF?text=ATLAN", width=150)
        st.markdown("---")
        
        st.markdown("### 🧭 Navigation")
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'landing'
            st.rerun()
        if st.button("📈 Rollout Simulator", use_container_width=True):
            st.session_state.page = 'rollout'
            st.rerun()
        if st.button("📊 Maturity Assessment", use_container_width=True):
            st.session_state.page = 'maturity'
            st.rerun()
        if st.button("🏗️ Implementation Planner", use_container_width=True):
            st.session_state.page = 'implementation'
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📞 Need Help?")
        st.markdown("Contact your Atlan Customer Success Manager or visit [docs.atlan.com](https://docs.atlan.com)")
    
    # Page routing
    if st.session_state.page == 'landing':
        landing_page()
    elif st.session_state.page == 'rollout':
        rollout_simulator()
    elif st.session_state.page == 'maturity':
        maturity_assessment()
    elif st.session_state.page == 'implementation':
        implementation_planner()

if __name__ == "__main__":
    main()
