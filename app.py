import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Admin credentials
ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD = "AdminPOEconomics"

# Simulated data for daily deposits (example data as per your provided input)
deposits_data = {
    "username": [
        "PoEconomics", "JESUS (Spector)", "eepee", "ElVincenzo", "Jinn", "Lord", "Chris", "Biscuit Roger", "PoEconomics", 
        "suicideduner", "coolrd", "Dissonances", "Rycaxx", "PoEconomics", "JESUS (Spector)", "Reaper4k", "Coord", "n u", 
        "Wylou", "Arashi", "Mav", "shootermcgavin", "Aufketa", "SatantheAngel", "Ermes", "ElVincenzo", "DavaiiLama", 
        "ACAB", "Reaper4k", "Wohta", "bradonf333", "shinyeyes", "Hisesu", "chipseatingmonkey", "RDcabra", "Nomad443", 
        "Alex 13", "Floon", "CHOSEN CHICKAN", "Franzclammer", "Closure", "Dissonances", "Chakkree", "Hanzel", "PoEconomics", 
        "PIX CAIU FOTO SUMIU", "Vividly Exhausted", "kronostec", "ASH_KO", "Coolrd", "Kazaam", "Chris", "dug", 
        "Vividly Exhausted", "n u", "sogxinran", "MIRROR_IDOL_FUBGUN", "dxdiy", "behuia", "Jinn", "conconnait", 
        "Reaper4k", "Rasp", "Chakree", "Dorfman420", "highoncaffe1ne", "Franzclammer", "Bruh Moment", "farchioj", 
        "ElVincenzo", "Alex13", "Mea", "Reaper4k", "conconnait", "TheDirtyDaveyy", "Viking0071", "JESUS (Spector)", 
        "Anonx1987", "MatsumuraSan", "Steven"
    ],
    "deposit_amount": [
        18.5, 9.88, 10, 5.58, 33.45, 41.69, 5, 1, 128.11, 10, 9.51, 50, 30, 19.5, 2.33, 200, 10, 30, 10, 40, 30, 18, 
        50, 150, 100, 14.89, 50, 70, 200, 20, 20, 50, 20, 60, 6, 175.47, 120, 25, 90, 15, 30, 162.96, 46.8, 3, 19, 
        6, 80, 20, 2.68, 80, 19, 6, 5, 13, 18, 25, 18, 40, 8.5, 2, 10, 10, 300, 4, 13.86, 4, 59, 7, 50, 7, 4, 
        100, 100, 50, 17, 26
    ],
    "date": [
        "2025-05-18", "2025-05-18", "2025-05-18", "2025-05-18", "2025-05-18", "2025-05-18", "2025-05-18", "2025-05-18", 
        "2025-05-18", "2025-05-18", "2025-05-18", "2025-05-18", "2025-05-18", "2025-05-18", "2025-05-18", "2025-05-18", 
        "2025-05-19", "2025-05-19", "2025-05-19", "2025-05-19", "2025-05-19", "2025-05-19", "2025-05-19", "2025-05-19", 
        "2025-05-19", "2025-05-19", "2025-05-19", "2025-05-19", "2025-05-20", "2025-05-20", "2025-05-20", "2025-05-20", 
        "2025-05-20", "2025-05-20", "2025-05-20", "2025-05-20", "2025-05-20", "2025-05-21", "2025-05-21", "2025-05-21", 
        "2025-05-21", "2025-05-21", "2025-05-21", "2025-05-21", "2025-05-21", "2025-05-21", "2025-05-21", "2025-05-21", 
        "2025-05-21", "2025-05-21", "2025-05-21", "2025-05-21", "2025-05-21", "2025-05-21", "2025-05-21", "2025-05-21", 
        "2025-05-22", "2025-05-22", "2025-05-22", "2025-05-22", "2025-05-22", "2025-05-22", "2025-05-22", "2025-05-22", 
        "2025-05-22", "2025-05-22", "2025-05-22", "2025-05-22"
    ]
}

# Convert deposit data into DataFrame
df = pd.DataFrame(deposits_data)
df['date'] = pd.to_datetime(df['date'])

# Admin login
st.subheader("Admin Login")
admin_username = st.text_input("Username", type="default")
admin_password = st.text_input("Password", type="password")

# Admin login validation
if admin_username == ADMIN_USERNAME and admin_password == ADMIN_PASSWORD:
    st.success("Logged in as Admin")
    
    # Display deposit history
    st.subheader("Deposit History")
    st.dataframe(df)

    # User search for wallet
    st.subheader("Search for Your Wallet")
    username_input = st.text_input("Enter your username")

    # Growth calculation logic
    def calculate_growth(initial_amount, deposit_date, daily_growth_percentage):
        today = datetime.today()
        days_elapsed = (today - deposit_date).days
        growth_multiplier = (1 + daily_growth_percentage / 100) ** days_elapsed
        return initial_amount * growth_multiplier

    # Admin controls for growth percentage
    daily_growth_percentage = st.number_input("Set Daily Growth Percentage (%)", min_value=0.0, max_value=100.0, value=5.0)
    st.write(f"Daily Growth Percentage: {daily_growth_percentage}%")
    
    # Update daily growth percentage
    if st.button("Update Growth Percentage"):
        st.success(f"Growth percentage updated to {daily_growth_percentage}%")
        
        # Generate a new entry for the day with the updated percentage
        new_day = pd.DataFrame({
            "username": df['username'].unique(),
            "deposit_amount": [0] * len(df['username'].unique()),  # No deposit on the new day
            "date": [datetime.today().strftime('%Y-%m-%d')] * len(df['username'].unique())  # Today's date
        })
        
        df = pd.concat([df, new_day], ignore_index=True)

    if username_input:
        # Filter data for the entered user
        user_data = df[df['username'] == username_input]
        
        if not user_data.empty:
            st.write(f"Showing data for {username_input}")
            
            # Calculate growth for each deposit
            user_data['growth_value'] = user_data.apply(lambda row: calculate_growth(row['deposit_amount'], row['date'], daily_growth_percentage), axis=1)
            user_data['total_value'] = user_data['growth_value']
            
            # Display user-specific data with growth
            st.dataframe(user_data[['date', 'deposit_amount', 'growth_value', 'total_value']])
        else:
            st.write(f"No deposits found for user {username_input}")
else:
    st.warning("Invalid username or password")
