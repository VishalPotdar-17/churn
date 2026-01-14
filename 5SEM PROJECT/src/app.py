import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px
import time
import numpy as np

# Set page config
st.set_page_config(
    page_title="Telecom Churn Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Load data
@st.cache_data
def load_data():
    return pd.read_csv('data/telecom_churn.csv')


@st.cache_resource
def load_model():
    try:
        return joblib.load('models/best_churn_model.pkl')
    except FileNotFoundError:
        st.error("❌ Model file not found.")
        st.stop()


# Generate realistic names
@st.cache_data
def generate_customer_names(df):
    first_names_male = [
        'Rajesh', 'Amit', 'Arjun', 'Vikram', 'Rohit', 'Akshay',
        'Sanjay', 'Pradeep', 'Nikhil', 'Arun', 'Varun', 'Karthik',
        'Mahesh', 'Suresh', 'Bhaskar', 'Deepak', 'Ashok', 'Ravi',
        'Kumar', 'Jitesh', 'Manish', 'Naveen', 'Sachin', 'Rahul'
    ]
    first_names_female = [
        'Priya', 'Anjali', 'Neha', 'Divya', 'Shreya', 'Pooja',
        'Isha', 'Megha', 'Sneha', 'Ananya', 'Riya', 'Kavya',
        'Simran', 'Nikita', 'Geeta', 'Aarti', 'Rani', 'Sunita',
        'Meera', 'Lata', 'Kalpana', 'Swati', 'Vidya', 'Seema'
    ]
    last_names = [
        'Sharma', 'Singh', 'Kumar', 'Patel', 'Gupta', 'Verma',
        'Reddy', 'Rao', 'Pillai', 'Nair', 'Desai', 'Kapoor',
        'Joshi', 'Iyer', 'Menon', 'Bhat', 'Das', 'Roy', 'Khan',
        'Ahmed', 'Chopra', 'Malhotra', 'Bansal', 'Saxena', 'Tiwari',
        'Mishra', 'Pandey'
    ]

    names = []
    np.random.seed(42)
    for idx, row in df.iterrows():
        gender = row['gender']
        if gender == 'Male':
            first = np.random.choice(first_names_male)
        else:
            first = np.random.choice(first_names_female)
        last = np.random.choice(last_names)
        names.append(f"{first} {last}")

    return names


# Load data and model
df = load_data()
df['CustomerName'] = generate_customer_names(df)
model = load_model()

# Theme configuration
THEMES = {
    "� Blue & White": {
        "primary": "#1e40af",
        "dark": "#0f2847",
        "light_bg": "#f0f7ff",
        "accent": "#dc2626",
        "border": "#bfdbfe",
        "secondary": "#ffffff",
        "text_dark": "#0f2847"
    },
    "🟢 Green": {
        "primary": "#27ae60",
        "dark": "#1e8449",
        "light_bg": "#f0f8f4",
        "accent": "#16a34a",
        "border": "#e8f5e9",
        "secondary": "#ffffff",
        "text_dark": "#1e3a1f"
    },
    "🟠 Orange": {
        "primary": "#e67e22",
        "dark": "#d35400",
        "light_bg": "#fdebd0",
        "accent": "#f05545",
        "border": "#fad7a0",
        "secondary": "#ffffff",
        "text_dark": "#6f2d0f"
    },
    "🟣 Purple": {
        "primary": "#9b59b6",
        "dark": "#6c3483",
        "light_bg": "#f4ecf7",
        "accent": "#af7ac5",
        "border": "#ebdef0",
        "secondary": "#ffffff",
        "text_dark": "#3d1b52"
    },
    "🔴 Red": {
        "primary": "#dc2626",
        "dark": "#b91c1c",
        "light_bg": "#fef2f2",
        "accent": "#991b1b",
        "border": "#fecaca",
        "secondary": "#ffffff",
        "text_dark": "#7f1d1d"
    }
}

# Theme selector in sidebar
with st.sidebar:
    st.markdown("### 🎨 Theme Settings")
    selected_theme = st.selectbox(
        "Choose Theme",
        list(THEMES.keys()),
        index=0,
        help="Select your preferred dashboard theme"
    )

theme_colors = THEMES[selected_theme]

# Custom CSS for stunning separated styling
st.markdown(f"""
<style>
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    body {{
        background: linear-gradient(135deg, {theme_colors['light_bg']} 0%, #ffffff 100%);
    }}
    .main {{
        background: linear-gradient(135deg, {theme_colors['light_bg']} 0%, #ffffff 100%);
        padding: 30px;
    }}
    .dashboard-header {{
        background: linear-gradient(135deg, {theme_colors['primary']} 0%, {theme_colors['dark']} 100%);
        color: white;
        padding: 40px 30px;
        border-radius: 20px;
        margin-bottom: 40px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    .header-title {{
        font-size: 38px;
        font-weight: 900;
        letter-spacing: -0.5px;
    }}
    .header-subtitle {{
        font-size: 15px;
        opacity: 0.95;
        margin-top: 8px;
        font-weight: 300;
    }}
    .header-logo {{
        font-size: 52px;
        margin-right: 15px;
        display: inline-block;
    }}
    .card {{
        background: linear-gradient(135deg, #ffffff 0%, {theme_colors['light_bg']} 100%);
        padding: 32px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        margin-bottom: 28px;
        border-left: 5px solid {theme_colors['primary']};
        border-top: 1px solid rgba(255, 255, 255, 0.6);
        transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
        position: relative;
        overflow: hidden;
    }}
    .card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, {theme_colors['primary']}, {theme_colors['accent']});
    }}
    .card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 20px 50px rgba(30, 64, 175, 0.15);
        border-left: 5px solid {theme_colors['accent']};
    }}
    .card-title {{
        font-size: 12px;
        color: {theme_colors['primary']};
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 2.5px;
        font-weight: 800;
    }}
    .card-value {{
        font-size: 48px;
        font-weight: 900;
        color: {theme_colors['text_dark']};
        line-height: 1.1;
        background: linear-gradient(135deg, {theme_colors['primary']} 0%, {theme_colors['dark']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    .card-subtitle {{
        font-size: 13px;
        color: {theme_colors['primary']};
        margin-top: 12px;
        font-weight: 600;
    }}
    .section-title {{
        font-size: 26px;
        font-weight: 900;
        color: #1e3a1f;
        margin: 45px 0 30px 0;
        padding-bottom: 15px;
        border-bottom: 4px solid {theme_colors['primary']};
        letter-spacing: -0.5px;
    }}
    .form-card {{
        background: linear-gradient(135deg, #ffffff 0%, {theme_colors['light_bg']} 100%);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
        border: 2px solid {theme_colors['border']};
        transition: all 0.3s ease;
    }}
    .form-card:hover {{
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        border-color: {theme_colors['primary']};
    }}
    .stButton>button {{
        width: 100%;
        background: linear-gradient(135deg, {theme_colors['primary']} 0%, {theme_colors['dark']} 100%);
        color: white;
        font-weight: 800;
        border-radius: 14px;
        padding: 18px 25px;
        border: none;
        font-size: 16px;
        letter-spacing: 0.5px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .stButton>button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
    }}
    .stButton>button:active {{
        transform: translateY(-1px);
    }}
    .metrics-card {{
        background: linear-gradient(135deg, #ffffff 0%, {theme_colors['light_bg']} 100%);
        padding: 35px;
        border-radius: 20px;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.07);
        border: 2px solid {theme_colors['border']};
        margin-bottom: 30px;
        transition: all 0.3s ease;
    }}
    .metrics-card:hover {{
        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.12);
    }}
    .profile-section {{
        display: flex;
        align-items: center;
        gap: 30px;
        background: linear-gradient(135deg, {theme_colors['primary']} 0%, {theme_colors['dark']} 100%);
        padding: 35px;
        border-radius: 20px;
        color: white;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 30px;
    }}
    .profile-avatar {{
        width: 110px;
        height: 110px;
        border-radius: 50%;
        background-color: rgba(255, 255, 255, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 50px;
        border: 4px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    }}
    .profile-info {{
        flex: 1;
    }}
    .profile-name {{
        font-size: 24px;
        font-weight: 900;
        letter-spacing: -0.5px;
    }}
    .profile-detail {{
        font-size: 14px;
        opacity: 0.95;
        margin: 8px 0;
        font-weight: 500;
    }}
    .alert-high {{
        background: linear-gradient(135deg, #fff5f5 0%, #ffe5e5 100%);
        border-left: 6px solid #dc3545;
        border-top: 2px solid #dc3545;
        padding: 25px;
        border-radius: 15px;
        color: #742c2c;
        font-weight: 600;
        box-shadow: 0 6px 20px rgba(220, 53, 69, 0.1);
    }}
    .alert-low {{
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 6px solid {theme_colors['primary']};
        border-top: 2px solid {theme_colors['primary']};
        padding: 25px;
        border-radius: 15px;
        color: #052e16;
        font-weight: 600;
        box-shadow: 0 6px 20px rgba(30, 64, 175, 0.1);
    }}
    .chart-container {{
        background: linear-gradient(135deg, #ffffff 0%, {theme_colors['light_bg']} 100%);
        padding: 30px;
        border-radius: 18px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07);
        margin-bottom: 30px;
        border: 2px solid {theme_colors['border']};
        transition: all 0.3s ease;
    }}
    .chart-container:hover {{
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class='dashboard-header'>
    <div class='header-title'><span class='header-logo'>📈</span>Telecom Churn Dashboard</div>
    <div class='header-subtitle'>
        Your comprehensive churn prediction &
        customer analytics platform
    </div>
</div>
""", unsafe_allow_html=True)

# Calculate statistics from actual data
total_customers = len(df)
churn_count = len(df[df['Churn'] == 'Yes'])
churn_rate = (churn_count / total_customers) * 100
avg_tenure = df['tenure'].mean()
avg_monthly_charges = df['MonthlyCharges'].mean()
total_revenue = df['MonthlyCharges'].sum()

# Main layout - Left sidebar for input, Right for display
left_col, right_col = st.columns([2.5, 1.2])

with right_col:
    st.markdown("### 📝 Customer Lookup & Analysis")
    
    # Search for existing customer
    st.markdown("**🔍 Search Customer**")
    customer_search = st.selectbox(
        "Find & Auto-fill Customer Data",
        ["Manual Entry"] + sorted(df['CustomerName'].unique().tolist()),
        help="Select a customer to auto-populate their data"
    )
    
    selected_customer_data = None
    if customer_search != "Manual Entry":
        selected_customer_data = (
            df[df['CustomerName'] == customer_search].iloc[0]
        )
        msg = f"✅ Found: {customer_search} (ID: "
        msg += f"{selected_customer_data['customerID']})"
        st.success(msg)

    with st.form("churn_form"):
        # Demographics
        st.markdown("**Personal**")

        # Pre-fill if customer selected
        if selected_customer_data is not None:
            gender_default = selected_customer_data['gender']
            senior_citizen_default = int(
                selected_customer_data['SeniorCitizen']
            )
            partner_default = selected_customer_data['Partner']
        else:
            gender_default = "Male"
            senior_citizen_default = 0
            partner_default = "Yes"

        gender = st.selectbox(
            "Gender",
            ("Male", "Female"),
            index=0 if gender_default == "Male" else 1
        )
        senior_citizen = st.selectbox(
            "Senior?",
            (0, 1),
            index=senior_citizen_default,
            format_func=lambda x: "Yes" if x == 1 else "No"
        )
        partner = st.selectbox(
            "Partner",
            ("Yes", "No"),
            index=0 if partner_default == "Yes" else 1
        )

        # Services
        st.markdown("**Services**")
        if selected_customer_data is not None:
            phone_service_default = (
                selected_customer_data['PhoneService']
            )
            internet_service_default = (
                selected_customer_data['InternetService']
            )
        else:
            phone_service_default = "Yes"
            internet_service_default = "DSL"

        phone_service = st.selectbox(
            "Phone",
            ("Yes", "No"),
            index=0 if phone_service_default == "Yes" else 1
        )

        internet_options = ["DSL", "Fiber optic", "No"]
        internet_idx = (
            internet_options.index(internet_service_default)
            if internet_service_default in internet_options
            else 0
        )
        internet_service = st.selectbox(
            "Internet",
            internet_options,
            index=internet_idx
        )

        # Contract & Billing
        st.markdown("**Contract**")
        if selected_customer_data is not None:
            contract_default = selected_customer_data['Contract']
            tenure_default = int(selected_customer_data['tenure'])
        else:
            contract_default = "Month-to-month"
            tenure_default = 12

        contract_options = [
            "Month-to-month", "One year", "Two year"
        ]
        contract_idx = (
            contract_options.index(contract_default)
            if contract_default in contract_options
            else 0
        )
        contract = st.selectbox(
            "Type",
            contract_options,
            index=contract_idx
        )
        tenure = st.slider("Months", 0, 72, tenure_default)

        st.markdown("**Charges**")
        if selected_customer_data is not None:
            monthly_charges_default = float(
                selected_customer_data['MonthlyCharges']
            )
            total_charges_default = float(
                selected_customer_data['TotalCharges']
            )
        else:
            monthly_charges_default = 70.0
            total_charges_default = monthly_charges_default * tenure

        col_a, col_b = st.columns(2)
        with col_a:
            monthly_charges = st.number_input(
                "Monthly",
                0.0,
                200.0,
                monthly_charges_default
            )
        with col_b:
            total_charges = st.number_input(
                "Total",
                0.0,
                10000.0,
                total_charges_default
            )

        submit_button = st.form_submit_button("🔍 Analyze")


with left_col:
    # Top metrics
    st.markdown("<div class='section-title'>📊 Network Insights</div>",
                unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='card'>
            <div class='card-title'>👥 Total Customers</div>
            <div class='card-value'>{total_customers:,}</div>
            <div class='card-subtitle'>Active users</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='card'>
            <div class='card-title'>📉 Churn Rate</div>
            <div class='card-value'>{churn_rate:.1f}%</div>
            <div class='card-subtitle'>{churn_count} customers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='card'>
            <div class='card-title'>⏱️ Avg Tenure</div>
            <div class='card-value'>{avg_tenure:.1f}M</div>
            <div class='card-subtitle'>Customer lifetime</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='card'>
            <div class='card-title'>💰 Revenue/Month</div>
            <div class='card-value'>₹{total_revenue/1000:.0f}K</div>
            <div class='card-subtitle'>Total charges</div>
        </div>
        """, unsafe_allow_html=True)

    if submit_button:
        # Show selected customer details first
        if selected_customer_data is not None:
            st.markdown("<div class='metrics-card'>",
                        unsafe_allow_html=True)
            st.markdown("### 📊 Customer Profile")

            profile_cols = st.columns(4)
            with profile_cols[0]:
                cust_id = selected_customer_data['customerID']
                st.metric("Customer ID", cust_id)
            with profile_cols[1]:
                if selected_customer_data['Churn'] == 'Yes':
                    status = "Churned"
                    delta_text = "⚠️ Left"
                else:
                    status = "Active"
                    delta_text = "✅ Active"
                st.metric("Status", status, delta=delta_text)
            with profile_cols[2]:
                tenure_months = int(
                    selected_customer_data['tenure']
                )
                st.metric("Tenure", f"{tenure_months} months")
            with profile_cols[3]:
                monthly = selected_customer_data[
                    'MonthlyCharges'
                ]
                st.metric("Monthly Spend", f"₹{monthly:.0f}")
            st.markdown("</div>", unsafe_allow_html=True)
        # Prepare input data
        multiple_lines = "No phone service"
        online_security = "No internet service"
        online_backup = "No internet service"
        device_protection = "No internet service"
        tech_support = "No internet service"
        streaming_tv = "No internet service"
        streaming_movies = "No internet service"
        
        dependents = "No"
        paperless_billing = "Yes"
        payment_method = "Credit card (automatic)"

        data = {
            'gender': gender,
            'SeniorCitizen': senior_citizen,
            'Partner': partner,
            'Dependents': dependents,
            'tenure': tenure,
            'PhoneService': phone_service,
            'MultipleLines': multiple_lines,
            'InternetService': internet_service,
            'OnlineSecurity': online_security,
            'OnlineBackup': online_backup,
            'DeviceProtection': device_protection,
            'TechSupport': tech_support,
            'StreamingTV': streaming_tv,
            'StreamingMovies': streaming_movies,
            'Contract': contract,
            'PaperlessBilling': paperless_billing,
            'PaymentMethod': payment_method,
            'MonthlyCharges': monthly_charges,
            'TotalCharges': total_charges
        }
        input_df = pd.DataFrame(data, index=[0])

        with st.spinner('🔄 Analyzing...'):
            time.sleep(0.5)
            prediction = model.predict(input_df)
            prediction_proba = model.predict_proba(input_df)
            churn_prob = prediction_proba[0][1]

        # Customer Profile Section
        st.markdown("<div class='section-title'>👤 Customer Profile</div>",
                    unsafe_allow_html=True)
        
        customer_id = f"CUST{np.random.randint(10000, 99999)}"
        gender_icon = "👨" if gender == "Male" else "👩"
        
        st.markdown(f"""
        <div class='profile-section'>
            <div class='profile-avatar'>{gender_icon}</div>
            <div class='profile-info'>
                <div class='profile-name'>{customer_id}</div>
                <div class='profile-detail'>
                    📧 {gender} Customer
                </div>
                <div class='profile-detail'>
                    📱 {internet_service} |
                    📞 {phone_service}
                </div>
                <div class='profile-detail'>
                    💳 {contract} Contract |
                    ⏱️ {tenure} months
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Churn Analysis
        st.markdown(
            "<div class='section-title'>"
            "⚡ Churn Risk Analysis</div>",
            unsafe_allow_html=True
        )

        # Create columns for analysis
        analysis_col1, analysis_col2 = st.columns([1.5, 1])

        with analysis_col1:
            # Gauge chart
            st.markdown(
                "<div class='chart-container'>",
                unsafe_allow_html=True
            )
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=churn_prob * 100,
                title={'text': "Churn Risk Score"},
                delta={'reference': 50},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#1e40af"},
                    'steps': [
                        {'range': [0, 33], 'color': "#dbeafe"},
                        {'range': [33, 66], 'color': "#93c5fd"},
                        {'range': [66, 100], 'color': "#dc2626"}
                    ],
                    'threshold': {
                        'line': {'color': "#dc2626", 'width': 4},
                        'thickness': 0.75,
                        'value': 75
                    }
                }
            ))
            fig.update_layout(
                height=350,
                font=dict(size=12),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with analysis_col2:
            # Risk Status
            if churn_prob > 0.65:
                risk_level = "🔴 CRITICAL"
                risk_color = "#ff6b6b"
            elif churn_prob > 0.40:
                risk_level = "🟠 HIGH"
                risk_color = "#ffa500"
            elif churn_prob > 0.25:
                risk_level = "🟡 MEDIUM"
                risk_color = "#ffb800"
            else:
                risk_level = "🟢 LOW"
                risk_color = "#51cf66"

            st.markdown(f"""
            <div class='card'>
                <div style='font-size: 24px; font-weight: bold;
                           color: {risk_color};'>
                    {risk_level}
                </div>
                <div style='font-size: 14px; color: #666;
                           margin-top: 10px;'>
                    Probability: {churn_prob*100:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Comparative Analysis
        st.markdown("<div class='section-title'>📈 Comparative Analysis</div>",
                    unsafe_allow_html=True)

        col_compare1, col_compare2, col_compare3 = st.columns(3)

        similar_tenure = df[
            df['tenure'].between(max(0, tenure-6), tenure+6)
        ]
        similar_contract = df[df['Contract'] == contract]

        with col_compare1:
            avg_similar_monthly = (
                similar_tenure['MonthlyCharges'].mean()
            )
            st.markdown(f"""
            <div class='card'>
                <div class='card-title'>
                    📊 Similar Tenure Avg
                </div>
                <div class='card-value'>
                    ₹{avg_similar_monthly:.0f}
                </div>
                <div class='card-subtitle'>
                    vs ₹{monthly_charges:.0f} (yours)
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_compare2:
            if len(similar_contract) > 0:
                churn_similar = similar_contract[
                    similar_contract['Churn'] == 'Yes'
                ]
                contract_churn_rate = (
                    (len(churn_similar) /
                     len(similar_contract)) * 100
                )
            else:
                contract_churn_rate = 0
            st.markdown(f"""
            <div class='card'>
                <div class='card-title'>📉 Contract Churn Rate</div>
                <div class='card-value'>{contract_churn_rate:.1f}%</div>
                <div class='card-subtitle'>{contract} plan</div>
            </div>
            """, unsafe_allow_html=True)

        with col_compare3:
            phone_count = 1 if phone_service == "Yes" else 0
            internet_count = (
                1 if internet_service != "No" else 0
            )
            service_count = phone_count + internet_count
            st.markdown(f"""
            <div class='card'>
                <div class='card-title'>🎯 Active Services</div>
                <div class='card-value'>{service_count}</div>
                <div class='card-subtitle'>Services in use</div>
            </div>
            """, unsafe_allow_html=True)

        # Recommendations
        if churn_prob > 0.50:
            st.markdown("""
            <div class='alert-high'>
                <strong>🚨 IMMEDIATE ACTION REQUIRED</strong>
                <p style='margin-top: 10px; font-size: 13px;'>
                This customer is at high risk of churning. Recommended actions:
                </p>
                <ul style='margin-top: 8px; margin-left: 20px;'>
                    <li>📞 Personal outreach call within 24 hours</li>
                    <li>💳 Exclusive loyalty discount (12-15%)</li>
                    <li>📦 Premium services upgrade with benefits</li>
                    <li>⏰ Offer long-term contract (annual/2-year)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='alert-low'>
                <strong>✅ CUSTOMER SATISFIED</strong>
                <p style='margin-top: 10px; font-size: 13px;'>
                This customer shows low churn risk. Recommended actions:
                </p>
                <ul style='margin-top: 8px; margin-left: 20px;'>
                    <li>⭐ Reward loyalty program participation</li>
                    <li>🎁 Cross-sell premium services (streaming, cloud)</li>
                    <li>📱 Encourage referral program enrollment</li>
                    <li>👥 Invite to VIP customer events</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # Risk Factors
        st.markdown(
            "<div class='section-title'>🔍 Key Risk Drivers</div>",
            unsafe_allow_html=True
        )

        factors = []
        if contract == "Month-to-month":
            factors.append((
                "⚠️ Month-to-Month Contract",
                "High flexibility = Higher risk",
                30
            ))
        if internet_service == "Fiber optic":
            factors.append((
                "⚠️ Fiber Optic Service",
                "Service quality concerns",
                20
            ))
        if tenure < 12:
            factors.append((
                "⚠️ New Customer",
                "Early tenure = Early churn window",
                25
            ))
        if monthly_charges > 100:
            factors.append((
                "⚠️ Premium Pricing",
                "Above-average charges",
                15
            ))
        if tech_support == "No":
            factors.append((
                "⚠️ No Tech Support",
                "Increased frustration risk",
                10
            ))
        if (streaming_tv == "No" and
                streaming_movies == "No" and
                internet_service != "No"):
            factors.append((
                "ℹ️ Limited Services",
                "Opportunity to upsell",
                -5
            ))

        if factors:
            factor_col1, factor_col2 = st.columns([2, 1])
            with factor_col1:
                for factor_title, factor_desc, _ in factors:
                    factor_style = (
                        "background: #f8f8f8; padding: 12px; "
                        "border-radius: 8px; margin-bottom: 8px; "
                        "border-left: 3px solid #27ae60;"
                    )
                    st.markdown(f"""
                    <div style='{factor_style}'>
                        <strong>{factor_title}</strong><br>
                        <span style='font-size: 12px;
                                     color: #666;'>
                            {factor_desc}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

        # Historical Data Comparison
        st.markdown("<div class='section-title'>📊 Churn Distribution</div>",
                    unsafe_allow_html=True)

        # Create comparison charts
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            churn_by_contract = df['Contract'].value_counts()
            fig1_data = [
                go.Bar(
                    x=churn_by_contract.index,
                    y=churn_by_contract.values,
                    marker_color='#1e40af'
                )
            ]
            fig1 = go.Figure(data=fig1_data)
            fig1.update_layout(
                title="Customers by Contract Type",
                height=300,
                showlegend=False
            )
            st.plotly_chart(fig1, use_container_width=True)

        with chart_col2:
            churn_dist = df['Churn'].value_counts()
            colors = ['#1e40af', '#dc2626']
            fig2_data = [
                go.Pie(
                    labels=churn_dist.index,
                    values=churn_dist.values,
                    marker=dict(colors=colors)
                )
            ]
            fig2 = go.Figure(data=fig2_data)
            fig2.update_layout(
                title="Overall Churn Distribution",
                height=300
            )
            st.plotly_chart(fig2, use_container_width=True)

    else:
        # Default welcome view
        st.markdown(
            "<div class='section-title'>"
            "🎯 Welcome to Telecom Dashboard</div>",
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class='card'>
            <p style='font-size: 16px; line-height: 1.8;'>
            � <strong>Telecom Churn Dashboard</strong> -
            Your AI-powered customer retention platform
            </p>
            <p style='font-size: 14px; color: #666;
                       margin-top: 15px; line-height: 1.6;'>
            ✨ Fill customer details on the right to unlock:
            <br>• Real-time churn risk prediction
            <br>• Personalized retention strategies
            <br>• Comparative customer analytics
            <br>• Data-driven recommendations
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Display data insights
        st.markdown("<div class='section-title'>📈 Network Statistics</div>",
                    unsafe_allow_html=True)
        
        stat_col1, stat_col2, stat_col3 = st.columns(3)

        with stat_col1:
            contract_data = df['Contract'].value_counts()
            contract_data = df['Contract'].value_counts()
            fig = px.pie(
                values=contract_data.values,
                names=contract_data.index,
                title="Contract Distribution"
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

        with stat_col2:
            internet_data = df['InternetService'].value_counts()
            fig = px.bar(
                x=internet_data.index,
                y=internet_data.values,
                title="Internet Service Type"
            )
            fig.update_layout(
                height=300,
                xaxis_title="Service",
                yaxis_title="Count"
            )
            st.plotly_chart(fig, use_container_width=True)

        with stat_col3:
            fig = px.histogram(
                df,
                x='MonthlyCharges',
                nbins=30,
                title="Monthly Charges Distribution"
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<p style='text-align: center; font-size: 12px; color: #999;'>
© 2026 Telecom Churn | Churn Prediction & Analytics |
Powered by Streamlit & ML
</p>
""", unsafe_allow_html=True)
