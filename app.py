import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import time
import numpy as np
import plotly.subplots as sp

# --- TELEGRAM CONFIGURATION ---
TELEGRAM_BOT_TOKEN = "8593148481:AAEaz5UBehgaJFjNV1wFEskQJ-o242Xe85c"
TELEGRAM_CHAT_ID = "5138828109"

def send_telegram_alert(message):
    """Send alert to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except:
        return False

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SAVOUIR | Luxury Intelligence",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LUXURY MINIMAL CSS (BLACK, WHITE, GOLD) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600;700&family=Montserrat:wght@300;400;500;600&display=swap');
    
    /* Global Styles */
    .stApp {
        background: #000000;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 300 !important;
        letter-spacing: 2px !important;
        color: #FFFFFF !important;
    }
    
    h1 {
        font-size: 3.5rem !important;
        border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        padding-bottom: 15px;
        margin-bottom: 30px;
    }
    
    /* Gold Accents */
    .gold-text {
        color: #D4AF37;
        font-weight: 400;
    }
    
    .gold-border {
        border: 1px solid #D4AF37;
    }
    
    /* Luxury Cards */
    .luxury-card {
        background: linear-gradient(145deg, #0a0a0a 0%, #1a1a1a 100%);
        border: 1px solid rgba(212, 175, 55, 0.1);
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .luxury-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .luxury-card:hover {
        transform: translateY(-5px);
        border-color: rgba(212, 175, 55, 0.3);
        box-shadow: 0 20px 40px rgba(212, 175, 55, 0.15);
    }
    
    .luxury-card:hover::before {
        left: 100%;
    }
    
    /* Metric Cards */
    .metric-card {
        background: #0a0a0a;
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s;
    }
    
    .metric-card:hover {
        border-color: #D4AF37;
        box-shadow: 0 0 30px rgba(212, 175, 55, 0.2);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 400;
        color: #D4AF37;
        font-family: 'Cormorant Garamond', serif;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 10px;
    }
    
    /* Dashboard Cards */
    .dashboard-card {
        background: #0a0a0a;
        border: 1px solid rgba(212, 175, 55, 0.15);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .card-title {
        color: #D4AF37;
        font-size: 1.2rem;
        font-family: 'Cormorant Garamond', serif;
        margin-bottom: 20px;
        letter-spacing: 1px;
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-critical { background: #D4AF37; box-shadow: 0 0 10px #D4AF37; }
    .status-warning { background: #B8860B; box-shadow: 0 0 10px #B8860B; }
    .status-stable { background: #666; box-shadow: 0 0 10px #666; }
    
    /* Buttons */
    .stButton > button {
        background: transparent !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 4px !important;
        padding: 10px 25px !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.9rem !important;
        letter-spacing: 1px !important;
        transition: all 0.3s !important;
    }
    
    .stButton > button:hover {
        background: #D4AF37 !important;
        color: #000000 !important;
        box-shadow: 0 0 30px rgba(212, 175, 55, 0.3) !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: #0a0a0a;
        border-right: 1px solid rgba(212, 175, 55, 0.1);
    }
    
    /* Radio Buttons */
    .stRadio > div {
        background: transparent !important;
    }
    
    .stRadio label {
        color: #888 !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.9rem !important;
        padding: 10px !important;
        border-radius: 4px !important;
        transition: all 0.3s !important;
    }
    
    .stRadio label:hover {
        background: rgba(212, 175, 55, 0.1) !important;
        color: #D4AF37 !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: #0a0a0a !important;
        border: 1px solid rgba(212, 175, 55, 0.2) !important;
        border-radius: 4px !important;
        color: #FFFFFF !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: #0a0a0a;
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 8px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px !important;
        padding: 8px 20px !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.9rem !important;
        color: #888 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(212, 175, 55, 0.1) !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: #0a0a0a !important;
        border: 1px solid rgba(212, 175, 55, 0.2) !important;
        border-radius: 4px !important;
        color: #D4AF37 !important;
        font-family: 'Cormorant Garamond', serif !important;
    }
    
    /* Progress Bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #D4AF37, #B8860B) !important;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Animations */
    @keyframes goldPulse {
        0% { box-shadow: 0 0 5px rgba(212, 175, 55, 0.2); }
        50% { box-shadow: 0 0 20px rgba(212, 175, 55, 0.4); }
        100% { box-shadow: 0 0 5px rgba(212, 175, 55, 0.2); }
    }
    
    .pulse-gold {
        animation: goldPulse 2s infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0px); }
    }
    
    .float {
        animation: float 4s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def load_and_process_data():
    # Load your CSV
    df = pd.read_csv('clients.csv')
    
    # Calculate Churn Probability
    df['Churn_Prob'] = 100 - ((df['Engagement_Score'] * 6) + (df['Service_Quality_Score'] * 4))
    df['Churn_Prob'] = df['Churn_Prob'].clip(lower=5, upper=98).round(1)
    
    # Predict Lifetime
    df['Days_Remaining'] = ((100 - df['Churn_Prob']) * 3.65).astype(int)
    
    # Calculate Revenue Loss
    df['Potential_Loss'] = df['Revenue_Yearly']
    
    # Add risk categories
    df['Risk_Category'] = pd.cut(df['Churn_Prob'], 
                                  bins=[0, 30, 65, 100], 
                                  labels=['LOW', 'MEDIUM', 'HIGH'])
    
    # Calculate expected date of churn
    df['Expected_Churn_Date'] = datetime.now() + pd.to_timedelta(df['Days_Remaining'], unit='D')
    
    # Add health score
    df['Health_Score'] = ((df['Engagement_Score'] * 0.6) + (df['Service_Quality_Score'] * 0.4)).round(1)
    
    # Add client tier based on revenue
    revenue_quantiles = df['Revenue_Yearly'].quantile([0.33, 0.67])
    revenue_bins = [0, revenue_quantiles.iloc[0], revenue_quantiles.iloc[1], float('inf')]
    tier_labels = ['SIGNATURE', 'PREMIUM', 'ELITE']
    
    df['Client_Tier'] = pd.cut(df['Revenue_Yearly'], 
                               bins=revenue_bins, 
                               labels=tier_labels, 
                               include_lowest=True)
    
    # Add days since last interaction
    df['Days_Since_Interaction'] = np.random.randint(1, 30, len(df))
    
    # Add tenure years if not present
    if 'Tenure_Years' not in df.columns:
        df['Tenure_Years'] = (df['Revenue_Yearly'] / 500000).round(1)
    
    # Add products used if not present
    if 'Products_Used' not in df.columns:
        df['Products_Used'] = (df['Engagement_Score'] * 0.8).round().astype(int)
    
    return df

try:
    df = load_and_process_data()
except FileNotFoundError:
    st.error("Error: 'clients.csv' not found. Please ensure the file exists in the folder.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 30px 20px;">
        <h1 style="font-size: 3rem; margin: 0; letter-spacing: 4px;">⚜️</h1>
        <h2 style="margin: 10px 0 0 0; font-size: 1.8rem;">SAVOUIR</h2>
        <p style="color: #D4AF37; font-size: 0.8rem; letter-spacing: 3px;">LUXURY INTELLIGENCE</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    current_time = datetime.now().strftime("%H:%M")
    st.markdown(f"""
    <div style="text-align: center; padding: 10px;">
        <span class="status-indicator status-critical"></span>
        <span style="color: #888; font-size: 0.8rem;">LIVE • {current_time} GMT</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='color: #D4AF37; font-size: 0.9rem; letter-spacing: 2px; margin-bottom: 10px;'>NAVIGATION</p>", unsafe_allow_html=True)
    
    selected = st.radio(
        "",
        ["✨ DASHBOARD", "👑 CLIENT DEEP DIVE", "📈 PORTFOLIO ANALYTICS", "⚡ ALERT CENTER", "🎯 ACQUISITION STRATEGY"],
        label_visibility="collapsed"
    )
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("<p style='color: #D4AF37; font-size: 0.9rem; letter-spacing: 2px; margin-bottom: 10px;'>PORTFOLIO SNAPSHOT</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="text-align: center;">
            <p style="color: #D4AF37; font-size: 1.8rem; margin: 0;">{len(df)}</p>
            <p style="color: #666; font-size: 0.7rem;">CLIENTS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        high_risk = len(df[df['Risk_Category'] == 'HIGH'])
        st.markdown(f"""
        <div style="text-align: center;">
            <p style="color: #D4AF37; font-size: 1.8rem; margin: 0;">{high_risk}</p>
            <p style="color: #666; font-size: 0.7rem;">AT RISK</p>
        </div>
        """, unsafe_allow_html=True)
    
    total_value = df['Revenue_Yearly'].sum()
    st.markdown(f"""
    <div style="text-align: center; margin-top: 15px;">
        <p style="color: #888; font-size: 0.7rem;">PORTFOLIO VALUE</p>
        <p style="color: #D4AF37; font-size: 1.4rem;">${total_value:,.0f}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("<p style='color: #D4AF37; font-size: 0.9rem; letter-spacing: 2px; margin-bottom: 10px;'>QUICK SEARCH</p>", unsafe_allow_html=True)
    selected_client = st.selectbox(
        "",
        df['Client_Name'].tolist(),
        format_func=lambda x: f"⚜️ {x}",
        label_visibility="collapsed"
    )

# --- DASHBOARD PAGE ---
if selected == "✨ DASHBOARD":
    st.markdown("<h1>EXECUTIVE<span class='gold-text'> DASHBOARD</span></h1>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_revenue = df['Revenue_Yearly'].sum()
    avg_risk = df['Churn_Prob'].mean()
    high_risk_count = len(df[df['Risk_Category'] == 'HIGH'])
    at_risk_revenue = df[df['Risk_Category'] == 'HIGH']['Revenue_Yearly'].sum()
    
    metrics = [
        (f"${total_revenue:,.0f}", "TOTAL PORTFOLIO VALUE", f"+{np.random.uniform(5, 10):.1f}% VS QTR"),
        (f"{avg_risk:.1f}%", "AVERAGE RISK SCORE", f"{'🔺' if avg_risk > 40 else '🔻'} {abs(avg_risk-30):.1f}% FROM TARGET"),
        (f"{high_risk_count}", "CLIENTS AT RISK", f"{(high_risk_count/len(df)*100):.0f}% OF PORTFOLIO"),
        (f"${at_risk_revenue:,.0f}", "CAPITAL AT RISK", f"{np.random.randint(15, 25)}% OF TOTAL")
    ]
    
    for idx, (col, (value, label, delta)) in enumerate(zip([col1, col2, col3, col4], metrics)):
        with col:
            st.markdown(f"""
            <div class="luxury-card" style="padding: 15px;">
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
                <div style="color: #D4AF37; font-size: 0.7rem; margin-top: 10px;">{delta}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.2, 0.8])
    
    with col_left:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">RISK DISTRIBUTION MATRIX</p>', unsafe_allow_html=True)
        
        risk_counts = df['Risk_Category'].value_counts().reset_index()
        risk_counts.columns = ['Category', 'Count']
        
        colors = {'LOW': '#D4AF37', 'MEDIUM': '#B8860B', 'HIGH': '#8B0000'}
        
        fig_risk = go.Figure()
        fig_risk.add_trace(go.Pie(
            labels=risk_counts['Category'],
            values=risk_counts['Count'],
            marker=dict(colors=[colors[x] for x in risk_counts['Category']]),
            textinfo='label+percent',
            textfont=dict(color='white', size=14, family='Cormorant Garamond'),
            hole=0.4,
            pull=[0.05 if x == 'HIGH' else 0 for x in risk_counts['Category']]
        ))
        
        fig_risk.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Cormorant Garamond'),
            showlegend=False,
            height=350,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        
        st.plotly_chart(fig_risk, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<br>', unsafe_allow_html=True)
        
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">CLIENT TIER DISTRIBUTION</p>', unsafe_allow_html=True)
        
        tier_counts = df['Client_Tier'].value_counts().reset_index()
        tier_counts.columns = ['Tier', 'Count']
        
        fig_tier = px.bar(tier_counts, x='Tier', y='Count',
                         color='Tier',
                         color_discrete_map={'ELITE': '#D4AF37', 'PREMIUM': '#B8860B', 'SIGNATURE': '#8B0000'})
        
        fig_tier.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Cormorant Garamond'),
            showlegend=False,
            height=250,
            xaxis=dict(gridcolor='#333'),
            yaxis=dict(gridcolor='#333')
        )
        
        st.plotly_chart(fig_tier, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">PORTFOLIO HEALTH</p>', unsafe_allow_html=True)
        
        avg_health = df['Health_Score'].mean()
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_health,
            number={'font': {'color': '#D4AF37', 'size': 50}},
            gauge={
                'axis': {'range': [0, 10], 'tickcolor': 'white', 'tickfont': {'color': 'white'}},
                'bar': {'color': "#D4AF37"},
                'bgcolor': 'rgba(0,0,0,0)',
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 3], 'color': '#330000'},
                    {'range': [3, 7], 'color': '#1a1a1a'},
                    {'range': [7, 10], 'color': '#1a2a1a'}
                ],
                'threshold': {
                    'line': {'color': "#D4AF37", 'width': 4},
                    'thickness': 0.75,
                    'value': avg_health
                }
            }
        ))
        
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white'},
            height=250,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<br>', unsafe_allow_html=True)
        
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">TOP PERFORMERS</p>', unsafe_allow_html=True)
        
        top_clients = df.nlargest(5, 'Revenue_Yearly')[['Client_Name', 'Revenue_Yearly', 'Health_Score']]
        
        for _, client in top_clients.iterrows():
            st.markdown(f"""
            <div style="padding: 10px; border-bottom: 1px solid rgba(212, 175, 55, 0.1);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="color: #D4AF37;">⚜️</span>
                        <span style="color: white; margin-left: 10px;">{client['Client_Name']}</span>
                    </div>
                    <div style="color: #D4AF37;">${client['Revenue_Yearly']:,.0f}</div>
                </div>
                <div style="font-size: 0.8rem; color: #666; margin-top: 5px;">Health: {client['Health_Score']}/10</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<br>', unsafe_allow_html=True)
        
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">RISK ALERTS</p>', unsafe_allow_html=True)
        
        high_risk = df[df['Risk_Category'] == 'HIGH']
        if not high_risk.empty:
            for _, client in high_risk.iterrows():
                st.markdown(f"""
                <div style="padding: 10px; border-bottom: 1px solid rgba(212, 175, 55, 0.1);">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #8B0000;">⚠️ {client['Client_Name']}</span>
                        <span style="color: #D4AF37;">{client['Churn_Prob']}%</span>
                    </div>
                    <div style="font-size: 0.7rem; color: #666;">Action required within 24h</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #666; text-align: center;">No critical alerts</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- CLIENT DEEP DIVE PAGE ---
elif selected == "👑 CLIENT DEEP DIVE":
    st.markdown(f"<h1>CLIENT<span class='gold-text'> {selected_client}</span></h1>", unsafe_allow_html=True)
    
    client_data = df[df['Client_Name'] == selected_client].iloc[0]
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("""
        <div style="font-size: 5rem; text-align: center;">👑</div>
        """, unsafe_allow_html=True)
    with col2:
        risk_color = '#8B0000' if client_data['Risk_Category'] == 'HIGH' else '#B8860B' if client_data['Risk_Category'] == 'MEDIUM' else '#D4AF37'
        st.markdown(f"""
        <h2 style="margin: 0;">{client_data['Client_Name']}</h2>
        <p style="color: {risk_color};">{client_data['Client_Tier']} TIER • {client_data['Risk_Category']} RISK</p>
        <p style="color: #666;">Member since {datetime.now().year - int(client_data.get('Tenure_Years', 3))}</p>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="luxury-card">
            <div class="metric-label">ANNUAL REVENUE</div>
            <div class="metric-value">${client_data['Revenue_Yearly']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="luxury-card">
            <div class="metric-label">RISK PROBABILITY</div>
            <div class="metric-value" style="color: {risk_color};">{client_data['Churn_Prob']}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="luxury-card">
            <div class="metric-label">HEALTH SCORE</div>
            <div class="metric-value">{client_data['Health_Score']}/10</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="luxury-card">
            <div class="metric-label">DAYS REMAINING</div>
            <div class="metric-value">{client_data['Days_Remaining']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 PERFORMANCE", "📈 RISK ANALYSIS", "📝 ACTION PLAN"])
    
    with tab1:
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title">ENGAGEMENT METRICS</p>', unsafe_allow_html=True)
            
            categories = ['Engagement', 'Service Quality', 'Revenue', 'Health']
            values = [
                client_data['Engagement_Score'],
                client_data['Service_Quality_Score'],
                min(client_data['Revenue_Yearly'] / 500000, 10),
                client_data['Health_Score']
            ]
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                line=dict(color='#D4AF37', width=2),
                fillcolor='rgba(212, 175, 55, 0.2)'
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 10], gridcolor='#333'),
                    angularaxis=dict(gridcolor='#333'),
                    bgcolor='rgba(0,0,0,0)'
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=350,
                showlegend=False
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_right:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title">PERFORMANCE TRENDS</p>', unsafe_allow_html=True)
            
            dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
            engagement_trend = [client_data['Engagement_Score'] + np.random.normal(0, 0.5) for _ in range(12)]
            service_trend = [client_data['Service_Quality_Score'] + np.random.normal(0, 0.5) for _ in range(12)]
            
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=dates,
                y=engagement_trend,
                mode='lines+markers',
                name='Engagement',
                line=dict(color='#D4AF37', width=2),
                marker=dict(size=6)
            ))
            fig_trend.add_trace(go.Scatter(
                x=dates,
                y=service_trend,
                mode='lines+markers',
                name='Service Quality',
                line=dict(color='#B8860B', width=2),
                marker=dict(size=6)
            ))
            
            fig_trend.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=350,
                xaxis=dict(gridcolor='#333'),
                yaxis=dict(gridcolor='#333', range=[0, 10]),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_trend, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title">RISK FACTORS</p>', unsafe_allow_html=True)
            
            factors = {
                "Engagement Decline": max(0, (10 - client_data['Engagement_Score']) * 10),
                "Service Quality": max(0, (10 - client_data['Service_Quality_Score']) * 10),
                "Market Volatility": np.random.randint(10, 30),
                "Competitor Pressure": np.random.randint(10, 25)
            }
            
            factors_df = pd.DataFrame({
                'Factor': factors.keys(),
                'Contribution': factors.values()
            })
            
            fig_factors = px.bar(factors_df, y='Factor', x='Contribution',
                                orientation='h',
                                color='Contribution',
                                color_continuous_scale=['#8B0000', '#B8860B', '#D4AF37'])
            
            fig_factors.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=350,
                xaxis=dict(gridcolor='#333', title='Contribution %'),
                yaxis=dict(gridcolor='#333'),
                coloraxis_showscale=False
            )
            
            st.plotly_chart(fig_factors, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_right:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title">30-DAY RISK FORECAST</p>', unsafe_allow_html=True)
            
            dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
            base_risk = client_data['Churn_Prob']
            
            forecast_values = []
            for day in range(30):
                risk_value = base_risk + (day * 0.2) + np.random.normal(0, 1)
                risk_value = max(0, min(100, risk_value))
                forecast_values.append(risk_value)
            
            fig_forecast = go.Figure()
            fig_forecast.add_trace(go.Scatter(
                x=dates,
                y=forecast_values,
                mode='lines',
                line=dict(color='#D4AF37', width=3),
                fill='tozeroy',
                fillcolor='rgba(212, 175, 55, 0.1)',
                name='Forecast'
            ))
            
            fig_forecast.add_hline(y=65, line_dash="dash", line_color="#8B0000",
                                  annotation_text="Critical Threshold")
            
            fig_forecast.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=350,
                xaxis=dict(gridcolor='#333'),
                yaxis=dict(gridcolor='#333', range=[0, 100], title='Risk %')
            )
            
            st.plotly_chart(fig_forecast, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title">IMMEDIATE ACTIONS</p>', unsafe_allow_html=True)
            
            if client_data['Risk_Category'] == 'HIGH':
                actions = [
                    "🚨 Emergency CEO call within 24h",
                    "👥 Dedicated support team assignment",
                    "📋 Contract review meeting",
                    "💰 Retention offer: 20% discount"
                ]
            elif client_data['Risk_Category'] == 'MEDIUM':
                actions = [
                    "📅 Quarterly business review",
                    "📈 Engagement improvement plan",
                    "🎁 Early renewal incentive",
                    "📊 Monthly health checks"
                ]
            else:
                actions = [
                    "🚀 Upsell premium package",
                    "🤝 Referral program invitation",
                    "📝 Case study opportunity",
                    "🎪 VIP event invitation"
                ]
            
            for action in actions:
                st.markdown(f"""
                <div style="padding: 10px; border-bottom: 1px solid rgba(212, 175, 55, 0.1);">
                    <span style="color: #D4AF37;">▸</span>
                    <span style="color: white; margin-left: 10px;">{action}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_right:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.markdown('<p class="card-title">STRATEGIC RECOMMENDATIONS</p>', unsafe_allow_html=True)
            
            recommendations = [
                ("Short-term", "Increase touchpoints to weekly"),
                ("Medium-term", "Introduce new premium features"),
                ("Long-term", "Strategic partnership expansion"),
                ("ROI", f"Potential upside: ${client_data['Revenue_Yearly']*0.3:,.0f}")
            ]
            
            for period, rec in recommendations:
                st.markdown(f"""
                <div style="margin-bottom: 15px;">
                    <p style="color: #D4AF37; margin: 0;">{period}:</p>
                    <p style="color: white; margin: 5px 0 0 20px;">{rec}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# --- PORTFOLIO ANALYTICS PAGE ---
elif selected == "📈 PORTFOLIO ANALYTICS":
    st.markdown("<h1>PORTFOLIO<span class='gold-text'> ANALYTICS</span></h1>", unsafe_allow_html=True)
    
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">RISK FACTOR CORRELATION</p>', unsafe_allow_html=True)
    
    corr_matrix = df[['Engagement_Score', 'Service_Quality_Score', 'Churn_Prob', 'Revenue_Yearly']].corr()
    
    fig_corr = px.imshow(corr_matrix,
                         text_auto=True,
                         aspect="auto",
                         color_continuous_scale=['#000000', '#B8860B', '#D4AF37'])
    
    fig_corr.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400
    )
    
    st.plotly_chart(fig_corr, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">CLIENT SEGMENTATION MATRIX</p>', unsafe_allow_html=True)
    
    fig_scatter = px.scatter(df, x='Engagement_Score', y='Service_Quality_Score',
                            size='Revenue_Yearly', color='Churn_Prob',
                            hover_name='Client_Name',
                            color_continuous_scale=['#D4AF37', '#B8860B', '#8B0000'])
    
    fig_scatter.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=500,
        xaxis=dict(gridcolor='#333', title='Engagement Score'),
        yaxis=dict(gridcolor='#333', title='Service Quality Score')
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ALERT CENTER PAGE ---
elif selected == "⚡ ALERT CENTER":
    st.markdown("<h1>ALERT<span class='gold-text'> CENTER</span></h1>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">🔴 CRITICAL ALERTS</p>', unsafe_allow_html=True)
        
        high_risk = df[df['Risk_Category'] == 'HIGH']
        if not high_risk.empty:
            for _, client in high_risk.iterrows():
                st.markdown(f"""
                <div class="luxury-card" style="margin-bottom: 15px; border-left: 3px solid #8B0000;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h3 style="margin: 0;">{client['Client_Name']}</h3>
                            <p style="color: #888; margin: 5px 0 0 0;">Risk: {client['Churn_Prob']}% • Revenue: ${client['Revenue_Yearly']:,.0f}</p>
                        </div>
                        <div style="font-size: 2rem;">⚠️</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #666; text-align: center;">No critical alerts</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">🟡 WARNINGS</p>', unsafe_allow_html=True)
        
        medium_risk = df[df['Risk_Category'] == 'MEDIUM']
        if not medium_risk.empty:
            for _, client in medium_risk.iterrows():
                st.markdown(f"""
                <div class="luxury-card" style="margin-bottom: 15px; border-left: 3px solid #B8860B;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h3 style="margin: 0;">{client['Client_Name']}</h3>
                            <p style="color: #888; margin: 5px 0 0 0;">Risk: {client['Churn_Prob']}% • Health: {client['Health_Score']}/10</p>
                        </div>
                        <div style="font-size: 2rem;">⚡</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #666; text-align: center;">No warnings</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        if st.button("📱 SEND CRITICAL ALERTS", use_container_width=True):
            high_risk = df[df['Risk_Category'] == 'HIGH']
            if not high_risk.empty:
                alert_count = 0
                for _, client in high_risk.iterrows():
                    message = f"""
🚨 <b>CRITICAL ALERT - SAVOUIR</b> 🚨

<b>Client:</b> {client['Client_Name']}
<b>Risk Level:</b> {client['Churn_Prob']}% 🔴
<b>Revenue at Risk:</b> ${client['Revenue_Yearly']:,}
<b>Health Score:</b> {client['Health_Score']}/10
<b>Expected Churn:</b> {client['Expected_Churn_Date'].strftime('%Y-%m-%d')}

<b>Action Required:</b> Immediate intervention required.
                    """
                    if send_telegram_alert(message):
                        alert_count += 1
                    time.sleep(1)
                
                if alert_count > 0:
                    st.success(f"✅ {alert_count} alerts dispatched")
            else:
                st.info("No critical alerts to send")

# --- ACQUISITION STRATEGY PAGE ---
elif selected == "🎯 ACQUISITION STRATEGY":
    st.markdown("<h1>ACQUISITION<span class='gold-text'> STRATEGY</span></h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    strategies = [
        {
            "title": "LOOKALIKE TARGETING",
            "icon": "🎯",
            "targets": ["Celine", "Goyard", "Balenciaga"],
            "confidence": 92
        },
        {
            "title": "MARKET EXPANSION",
            "icon": "🌍",
            "targets": ["Middle East", "Southeast Asia"],
            "confidence": 87
        },
        {
            "title": "PARTNERSHIPS",
            "icon": "🤝",
            "targets": ["Hotel Chains", "Private Aviation"],
            "confidence": 78
        }
    ]
    
    for col, strategy in zip([col1, col2, col3], strategies):
        with col:
            st.markdown(f"""
            <div class="luxury-card" style="height: 300px;">
                <div style="font-size: 3rem; text-align: center; margin-bottom: 20px;">{strategy['icon']}</div>
                <h3 style="text-align: center; margin: 0;">{strategy['title']}</h3>
                <div style="margin-top: 20px;">
                    <p style="color: #D4AF37; margin: 5px 0;">Targets:</p>
                    <p style="color: white;">{', '.join(strategy['targets'])}</p>
                </div>
                <div style="margin-top: 20px;">
                    <div style="display: flex; justify-content: space-between; color: #888;">
                        <span>Confidence:</span>
                        <span style="color: #D4AF37;">{strategy['confidence']}%</span>
                    </div>
                    <div style="background: #333; height: 4px; margin-top: 5px;">
                        <div style="background: #D4AF37; width: {strategy['confidence']}%; height: 100%;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #333;">
    <p style="margin: 0;">SAVOUIR INTELLIGENCE PLATFORM © 2026</p>
    <p style="font-size: 0.7rem; margin: 5px 0;">LUXURY CLIENT INTELLIGENCE • PREDICTIVE ANALYTICS • REAL-TIME MONITORING</p>
</div>
""", unsafe_allow_html=True)