import streamlit as st
import requests

# Configure the page
st.set_page_config(page_title="Payment Gateway Portal", layout="centered")
st.title("💳 Secure Payment Gateway Dashboard")

# Define the base URL where your FastAPI server is listening
BACKEND_URL = "http://localhost:8000"

# Initialize a browser-like session state to hold the JWT token permanently
if "token" not in st.session_state:
    st.session_state.token = None

# Create navigation tabs
tab1, tab2, tab3 = st.tabs(["🔐 Register", "🔑 Login", "💰 Make Payment"])

# --- TAB 1: REGISTRATION ---
with tab1:
    st.header("Create a New Account")
    reg_name = st.text_input("Full Name", key="reg_name")
    reg_email = st.text_input("Email Address", key="reg_email")
    reg_password = st.text_input("Password", type="password", key="reg_password")
    
    if st.button("Submit Registration"):
        payload = {"name": reg_name, "email": reg_email, "password": reg_password}
        # Call your FastAPI endpoint directly
        response = requests.post(f"{BACKEND_URL}/auth/register", json=payload)
        
        if response.status_code == 201:
            st.success("Account successfully created! Please switch to the Login tab.")
        else:
            st.error(f"Registration Failed: {response.json().get('detail', 'Unknown Error')}")

# --- TAB 2: LOGIN ---
with tab2:
    st.header("Account Authentication")
    login_email = st.text_input("Email Address", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login"):
        # Match the standard OAuth2 Form Data that your backend expects
        form_data = {"username": login_email, "password": login_password}
        response = requests.post(f"{BACKEND_URL}/auth/login", data=form_data)
        
        if response.status_code == 200:
            token_data = response.json()
            # Save the token globally in Streamlit's session memory
            st.session_state.token = token_data["access_token"]
            st.success("Authenticated successfully! Your secure JWT token is now active.")
        else:
            st.error("Authentication failed. Check your email or password.")

# --- TAB 3: INITIATE PAYMENT ---
with tab3:
    st.header("Process a Transaction")
    
    # Check if the user has logged in first
    if st.session_state.token is None:
        st.warning("🔒 This action requires authentication. Please log in first to generate a token.")
    else:
        amount = st.number_input("Transaction Amount (in Paise/Cents)", min_value=50, value=50000)
        currency = st.selectbox("Currency", ["INR", "USD", "EUR"])
        description = st.text_input("Order Description", value="Saree Order Batch #001")
        
        if st.button("Initiate Secure Intent"):
            payment_payload = {"amount": amount, "currency": currency, "description": description}
            # Attach the JWT token securely into the Authorization header exactly like Swagger did
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            
            response = requests.post(f"{BACKEND_URL}/payments/initiate", json=payment_payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                st.success("🎉 Stripe Payment Intent Created Successfully!")
                st.json(result)
            else:
                # Try to read JSON, but fall back to raw text if the server completely crashed
                try:
                    error_msg = response.json().get('detail', 'Unauthorized access')
                except Exception:
                    error_msg = f"Server Error ({response.status_code}): {response.text}"
        
                st.error(f"Transaction Denied: {error_msg}")