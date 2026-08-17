import streamlit as st

# Set page configuration for a premium, wide-layout tool
st.set_page_config(
    page_title="Predictive Attrition Risk Simulator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS injection for a beautiful, modern, enterprise-grade UI
st.markdown("""
<style>
    /* Main container styling */
    .reportview-container {
        background: #f8f9fa;
    }
    /* Main Header styling */
    .main-title {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: #1E293B;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #64748B;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    /* Card/Metric containers */
    .metric-card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    .legacy-card {
        background-color: #F8FAFC;
        border-left: 5px solid #94A3B8;
    }
    .cortex-card {
        background-color: #F0FDF4;
        border-left: 5px solid #10B981;
    }
    /* Section headers */
    .section-header {
        color: #334155;
        font-size: 1.3rem;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    /* Risk Gauge Display styling */
    .risk-display {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin: 1rem 0;
        padding: 1rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<h1 class="main-title">Predictive Attrition Risk Simulator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Experience how correlating multiple workplace signals isolates true attrition risk compared to looking at backward-looking, isolated metrics.</p>', unsafe_allow_html=True)

st.markdown("---")

# Layout: Split into Sidebar (Inputs) and Main Panel (Outputs)
with st.sidebar:
    st.markdown('<p class="section-header" style="margin-top:0;">🛠️ Adjust Employee Workplace Signals</p>', unsafe_allow_html=True)
    st.write("Modify the indicators below to see how hidden correlations drive the final Attrition Risk.")
    
    # Simple, high-impact input sliders
    overtime_hours = st.slider("Weekly Overtime Hours", min_value=0, max_value=25, value=12, step=1, 
                              help="Normal baseline is under 5 hours. Over 10 signals potential burnout.")
    
    months_stagnant = st.slider("Months Since Last Promotion/Raise", min_value=0, max_value=36, value=14, step=1,
                               help="Time spent in the same role without financial or career progression.")
    
    leave_spike = st.slider("Unplanned Leaves (Last 60 Days)", min_value=0, max_value=10, value=3, step=1,
                            help="Sudden, non-approved time off (often concentrated around weekends).")

# Mathematical Logic for Correlation and Risk Calculation
# Base risk calculation reflecting a real predictive algorithm matrix
base_risk = 5.0

# Add impact of Overtime Burnout
if overtime_hours > 15:
    overtime_impact = overtime_hours * 2.2
elif overtime_hours > 8:
    overtime_impact = overtime_hours * 1.5
else:
    overtime_impact = overtime_hours * 0.5

# Add impact of Career Stagnation
if months_stagnant > 24:
    stagnation_impact = months_stagnant * 1.5
elif months_stagnant > 12:
    stagnation_impact = months_stagnant * 1.0
else:
    stagnation_impact = months_stagnant * 0.3

# Add impact of Unplanned Leave Spikes
leave_impact = leave_spike * 4.0

# THE CORE CONCEPT: Multiplier effect when variables are simultaneously high (Correlation Factor)
correlation_multiplier = 1.0
if overtime_hours >= 12 and months_stagnant >= 18 and leave_spike >= 4:
    correlation_multiplier = 1.6  # Severe risk overlap
elif overtime_hours >= 10 and (months_stagnant >= 12 or leave_spike >= 3):
    correlation_multiplier = 1.25 # Moderate compounding risk

# Calculate final risk percentage
calculated_risk = min(100.0, (base_risk + overtime_impact + stagnation_impact + leave_impact) * correlation_multiplier)

# Assign risk category and matching UX color schemes
if calculated_risk < 35:
    risk_label = "LOW"
    risk_color = "#10B981"  # Emerald Green
    risk_bg = "#F0FDF4"
    risk_desc = "The signals indicate normal workload and healthy engagement. Attrition risk is minimal."
elif calculated_risk < 70:
    risk_label = "MEDIUM"
    risk_color = "#F59E0B"  # Amber/Yellow
    risk_bg = "#FEF3C7"
    risk_desc = "Early friction detected. Disengagement is developing, but a timely intervention can easily retain this employee."
else:
    risk_label = "HIGH"
    risk_color = "#EF4444"  # Coral Red
    risk_bg = "#FEE2E2"
    risk_desc = "CRITICAL ALERT: Compounding triggers indicate a highly correlated flight pattern. Action should be taken immediately."

# Main Dashboard View: Split comparison into two columns
col1, col2 = st.columns(2)

with col1:
    st.markdown('<p class="section-header">❌ The Old Way: Isolated Legacy Dashboards</p>', unsafe_allow_html=True)
    st.write("Legacy HR software lists metrics in siloed graphs without tracking relationships.")
    
    st.markdown(f"""
    <div class="metric-card legacy-card">
        <h4>📊 Overtime Log</h4>
        <p style="font-size:1.8rem; font-weight:bold; margin:0; color:#475569;">{overtime_hours} Hours/Wk</p>
        <span style="color:#64748B; font-size:0.85rem;">Status: Logged retroactively at month-end.</span>
    </div>
    <div class="metric-card legacy-card">
        <h4>📅 HRIS Tenure Profile</h4>
        <p style="font-size:1.8rem; font-weight:bold; margin:0; color:#475569;">{months_stagnant} Months Stagnant</p>
        <span style="color:#64748B; font-size:0.85rem;">Status: Static entry in the employee system database.</span>
    </div>
    <div class="metric-card legacy-card">
        <h4>🤒 Absence Tracker</h4>
        <p style="font-size:1.8rem; font-weight:bold; margin:0; color:#475569;">{leave_spike} Incidents</p>
        <span style="color:#64748B; font-size:0.85rem;">Status: Captured purely for payroll deductions.</span>
    </div>
    """, unsafe_allow_html=True)
    st.warning("⚠️ **Legacy System Output**: No alerts triggered. These look like three completely unrelated, routine HR data entries.")

with col2:
    st.markdown('<p class="section-header">✨ The Modern Way: Real-Time Signal Correlation</p>', unsafe_allow_html=True)
    st.write("An AI-native graph engine immediately cross-references all data streams simultaneously.")
    
    # Beautiful Risk Container
    st.markdown(f"""
    <div class="metric-card cortex-card" style="border-left: 5px solid {risk_color}; height: 100%;">
        <h3 style="margin-top:0; color:#1E293B; font-weight:600;">System Attrition Risk Assessment</h3>
        <div style="background-color: {risk_bg}; color: {risk_color};" class="risk-display">
            {calculated_risk:.1f}% <span style="font-size:1.5rem; font-weight:600;">({risk_label})</span>
        </div>
        <p style="color:#334155; font-size:1rem; line-height:1.5; margin-bottom:1.5rem;"><b>Insight</b>: {risk_desc}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Informative Footer explaining the math
st.markdown("### 🧠 The Statistical Correlation Concept in Action")
if correlation_multiplier > 1.0:
    st.info(f"⚡ **Correlation Engine Active (Multiplier: {correlation_multiplier}x)**: Notice how your current inputs aren't just being added up—they are compounding. Because Overtime, Stagnation, and Leaves are spiking together, the engine recognizes a matching historical pattern of flight behavior, multiplying the risk scale exponentially.")
else:
    st.info("ℹ️ **Linear Scaling**: The current inputs show independent fluctuations but have not crossed the critical multi-variable correlation threshold yet. Risk remains linearly predictable.")
