
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="Conservation Decision Support Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .scenario-card {
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Dashboard Header
st.markdown('<h1 class="main-header">🌿 Conservation Decision Support Dashboard</h1>', unsafe_allow_html=True)

# Load data (in practice, this would load from the JSON files we saved)
@st.cache_data
def load_optimization_data():
    # This would load from actual files
    return {
        "total_budget": 4500000,
        "allocated_budget": 4000000,
        "scenarios_funded": 2,
        "budget_efficiency": 1.158
    }

@st.cache_data  
def load_scenarios():
    return [
        {
            "name": "Rainforest Protection Initiative",
            "budget": 1800000,
            "score": 0.657,
            "timeline": 24,
            "description": "Comprehensive protection of primary rainforest areas"
        },
        {
            "name": "Marine Conservation Program", 
            "budget": 2200000,
            "score": 0.501,
            "timeline": 30,
            "description": "Protection of coastal and marine ecosystems"
        }
    ]

# Sidebar for user role selection
st.sidebar.header("👤 User Profile")
user_role = st.sidebar.selectbox(
    "Select your role:",
    ["Conservation Director", "Environment Minister", "Climate Research Lead", "Community Leader", "Public User"]
)

# Main dashboard content
optimization_data = load_optimization_data()
scenarios = load_scenarios()

# Key Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Budget",
        value=f"${optimization_data['total_budget']:,.0f}",
        delta=f"${optimization_data['allocated_budget']:,.0f} allocated"
    )

with col2:
    st.metric(
        label="🎯 Scenarios Funded",
        value=optimization_data['scenarios_funded'],
        delta="High impact selection"
    )

with col3:
    budget_utilization = (optimization_data['allocated_budget'] / optimization_data['total_budget']) * 100
    st.metric(
        label="📊 Budget Utilization",
        value=f"{budget_utilization:.1f}%",
        delta="Efficient allocation"
    )

with col4:
    st.metric(
        label="⚡ Efficiency Score",
        value=f"{optimization_data['budget_efficiency']:.3f}",
        delta="Optimized portfolio"
    )

# Scenario Details Section
st.header("🎯 Selected Conservation Scenarios")

for i, scenario in enumerate(scenarios, 1):
    with st.expander(f"{i}. {scenario['name']} - Score: {scenario['score']:.3f}"):
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Budget Required:** ${scenario['budget']:,.0f}")
            st.write(f"**Timeline:** {scenario['timeline']} months")
            st.write(f"**Effectiveness Score:** {scenario['score']:.3f}")

        with col2:
            st.write(f"**Description:** {scenario['description']}")

            # Progress bar for budget allocation
            budget_percentage = (scenario['budget'] / optimization_data['total_budget']) * 100
            st.progress(budget_percentage / 100)
            st.write(f"Budget share: {budget_percentage:.1f}%")

# Interactive Charts Section
st.header("📊 Decision Analysis")

tab1, tab2, tab3 = st.tabs(["Budget Allocation", "Timeline View", "Risk Assessment"])

with tab1:
    # Budget allocation pie chart
    budget_data = pd.DataFrame({
        'Scenario': [s['name'] for s in scenarios] + ['Unallocated'],
        'Budget': [s['budget'] for s in scenarios] + [optimization_data['total_budget'] - optimization_data['allocated_budget']]
    })

    fig_pie = px.pie(budget_data, values='Budget', names='Scenario', 
                     title='Budget Allocation by Scenario')
    st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
    # Timeline Gantt chart
    timeline_data = pd.DataFrame({
        'Scenario': [s['name'] for s in scenarios],
        'Start': [datetime(2024, 1, 1) for _ in scenarios],
        'Finish': [datetime(2024, 1 + s['timeline']//30, 1) for s in scenarios],
        'Duration': [s['timeline'] for s in scenarios]
    })

    fig_timeline = px.timeline(timeline_data, x_start='Start', x_end='Finish', y='Scenario',
                              title='Implementation Timeline')
    st.plotly_chart(fig_timeline, use_container_width=True)

with tab3:
    # Risk assessment (mock data for demonstration)
    risk_data = pd.DataFrame({
        'Scenario': [s['name'] for s in scenarios],
        'Risk_Level': [20, 23],  # Mock uncertainty percentages
        'Risk_Category': ['Medium', 'Medium']
    })

    fig_risk = px.bar(risk_data, x='Scenario', y='Risk_Level', color='Risk_Category',
                     title='Risk Assessment by Scenario')
    st.plotly_chart(fig_risk, use_container_width=True)

# Role-specific content
st.header(f"📋 Information for {user_role}")

if user_role == "Conservation Director":
    st.info("🔬 **Technical Details**: Access detailed implementation plans and monitoring protocols.")
    st.write("- Species protection targets and methodologies")
    st.write("- Habitat conservation metrics and monitoring")
    st.write("- Resource allocation and staff deployment plans")

elif user_role == "Environment Minister":
    st.info("🏛️ **Policy Recommendations**: Evidence-based policy development support.")
    st.write("- Regulatory framework requirements")
    st.write("- Economic impact assessments")  
    st.write("- Stakeholder engagement strategies")

elif user_role == "Community Leader":
    st.info("🤝 **Community Benefits**: Local impact and participation opportunities.")
    st.write("- Economic opportunities for local communities")
    st.write("- Community engagement and training programs")
    st.write("- Sustainable livelihood development")

else:
    st.info("ℹ️ **Public Information**: Simplified overview of conservation initiatives.")
    st.write("- Conservation goals and expected benefits")
    st.write("- Community involvement opportunities")
    st.write("- Environmental impact and progress updates")

# Action Items and Next Steps
st.header("🚀 Next Steps")

if user_role in ["Conservation Director", "Environment Minister"]:
    st.write("**Immediate Actions:**")
    st.write("1. ✅ Review and approve selected scenarios")
    st.write("2. 📋 Finalize implementation timelines")
    st.write("3. 👥 Assign project teams and responsibilities")
    st.write("4. 📊 Establish monitoring and evaluation framework")

    if st.button("📄 Generate Detailed Implementation Plan"):
        st.success("Implementation plan generated! Check your email for the detailed document.")

    if st.button("📊 Schedule Stakeholder Review Meeting"):
        st.success("Meeting scheduled! Calendar invitations sent to all stakeholders.")

# Feedback Section
st.header("💬 Feedback")
feedback = st.text_area("Share your thoughts on this decision analysis:", 
                       placeholder="Your feedback helps improve our decision support system...")

if st.button("Submit Feedback"):
    if feedback:
        st.success("Thank you for your feedback! Your input has been recorded.")
    else:
        st.warning("Please enter your feedback before submitting.")

# Footer
st.markdown("---")
st.markdown("🌿 **Conservation Decision Support System** | Generated on " + datetime.now().strftime("%Y-%m-%d %H:%M"))
