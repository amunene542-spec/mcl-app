import streamlit as st
import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. Define your API key
api_key = "YOUR_ACTUAL_API_KEY_HERE"

# 2. Configure the SDK
genai.configure(api_key=api_key)

# 3. Create the model instance
model = genai.GenerativeModel("gemini-1.5-flash")
from datetime import datetime

# (Keep your API key input variable here, e.g., api_key = ...)
# Put your actual key inside the quotation marks:
api_key = "AIzaSy..."  

# This goes right below it:
genai.configure(api_key=api_key)

# Then your existing Streamlit code starts below:
st.set_page_config(page_title="MCL Farm & Operations Manager", page_icon="🌾", layout="wide")
# Initialize all session state variables to prevent errors
if "poultry_logs" not in st.session_state:
    st.session_state.poultry_logs = []

if "supplies_needed" not in st.session_state:
    st.session_state.supplies_needed = []

if "security_logs" not in st.session_state:
    st.session_state.security_logs = []
import pandas as pd
from datetime import datetime
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Page setup
st.set_page_config(page_title="MCL Farm & Operations Manager", page_icon="🌾", layout="wide")
# Initialize Session States for Data Persistence
if "crops" not in st.session_state:
    st.session_state.crops = []
if "supplies_needed" not in st.session_state:
    st.session_state.supplies_needed = []
if "watering_logs" not in st.session_state:
    st.session_state.watering_logs = []

if "harvest_logs" not in st.session_state:
    st.session_state.harvest_logs = []

if "labor_logs" not in st.session_state:
    st.session_state.labor_logs = []

if "security_logs" not in st.session_state:
    st.session_state.security_logs=[] 
if "supplies_needed" not in st.session_state:
    st.session_state.supplies_needed = []
page = st.sidebar.selectbox("Navigation", 
["Dashboard", 
    "Planting Tracker", 
    "Watering & Irrigation", 
    "Poultry & Egg Tracker", 
    "Harvest Tracker", 
    "Labor & Caretaker Work",
    "Askari & Security Logs",
    "Garden Supplies & Requirements",
    "AI Farm Assistant & Reports"
])

# ---------------------------------------------------------
# PAGE 1: DASHBOARD
# ---------------------------------------------------------
if page == "Dashboard":
    st.title("📊 Farm & Property Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Active Crops", len(st.session_state.crops))
    with col2:
        total_eggs = sum([log["Eggs Collected"] for log in st.session_state.poultry_logs]) if st.session_state.poultry_logs else 0
        st.metric("Total Eggs Collected", total_eggs)
    with col3:
        st.metric("Harvest Logs", len(st.session_state.harvest_logs))
    with col4:
        st.metric("Security Check Logs", len(st.session_state.security_logs))
    with col5:
        st.metric("Pending Supplies Needed", len([s for s in st.session_state.supplies_needed if s["Status"] == "Needed"]))
    
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Active Crops Summary")
        if st.session_state.crops:
            st.dataframe(pd.DataFrame(st.session_state.crops), use_container_width=True)
        else:
            st.info("No crops registered yet.")
            
    with c2:
        st.subheader("Recent Security & Patrol Reports")
        if st.session_state.security_logs:
            st.dataframe(pd.DataFrame(st.session_state.security_logs), use_container_width=True)
        else:
            st.info("No security logs recorded yet.")

# ---------------------------------------------------------
# PAGE 2: PLANTING TRACKER
# ---------------------------------------------------------
elif page == "Planting Tracker":
    st.title("🌱 Crop & Bed Tracker")
    
    with st.form("add_crop_form"):
        crop_name = st.text_input("Crop Name (e.g., Garlic, Passion Fruit, Peas, Cucumbers, Maize)")
        bed_location = st.text_input("Bed / Plot Location (e.g., Block A, 1/4 Acre Plot)")
        date_planted = st.date_input("Date Planted", datetime.now())
        expected_harvest = st.date_input("Expected Harvest Date", datetime.now())
        notes = st.text_area("Notes (e.g., organic fertilizer applied, debelling done, drip line checked)")
        
        submit = st.form_submit_button("Save Crop")
        
        if submit:
            if crop_name and bed_location:
                st.session_state.crops.append({
                    "ID": len(st.session_state.crops) + 1,
                    "Crop Name": crop_name,
                    "Location": bed_location,
                    "Date Planted": str(date_planted),
                    "Expected Harvest": str(expected_harvest),
                    "Notes": notes
                })
                st.success(f"Added {crop_name} successfully!")
            else:
                st.error("Please fill in Crop Name and Location.")

    st.markdown("---")
    st.subheader("Registered Crops")
    if st.session_state.crops:
        st.dataframe(pd.DataFrame(st.session_state.crops), use_container_width=True)

# ---------------------------------------------------------
# PAGE 3: WATERING & IRRIGATION
# ---------------------------------------------------------
elif page == "Watering & Irrigation":
    st.title("💧 Watering & Drip Irrigation Log")
    
    if not st.session_state.crops:
        st.warning("Please add crops in the 'Planting Tracker' section first.")
    else:
        crop_names = [crop["Crop Name"] + f" ({crop['Location']})" for crop in st.session_state.crops]
        
        with st.form("irrigation_form"):
            selected_crop = st.selectbox("Select Crop / Plot", crop_names)
            water_amount = st.text_input("Water Duration / Amount (e.g., 45 mins drip, 200L)")
            log_date = st.date_input("Date", datetime.now())
            remarks = st.text_input("Remarks / Soil Condition")
            
            submit_log = st.form_submit_button("Record Irrigation")
            
            if submit_log:
                st.session_state.watering_logs.append({
                    "Crop/Plot": selected_crop,
                    "Amount/Duration": water_amount,
                    "Date": str(log_date),
                    "Remarks": remarks
                })
                st.success("Watering record saved!")

    st.markdown("---")
    st.subheader("Irrigation History")
    if st.session_state.watering_logs:
        st.dataframe(pd.DataFrame(st.session_state.watering_logs), use_container_width=True)

# ---------------------------------------------------------
# PAGE 4: POULTRY & EGG TRACKER
# ---------------------------------------------------------
elif page == "Poultry & Egg Tracker":
    st.title("🐔 Poultry & Egg Management")
    
    with st.form("poultry_form"):
        log_date = st.date_input("Date", datetime.now())
        eggs_collected = st.number_input("Eggs Collected Today", min_value=0, step=1)
        broken_eggs = st.number_input("Damaged / Broken Eggs", min_value=0, step=1)
        feed_given = st.text_input("Feed Given (e.g., Maize, wheat & omena mix, greens)")
        health_notes = st.text_area("Flock Observations / Health Notes (e.g., broody hen management, health check)")
        
        submit_poultry = st.form_submit_button("Record Poultry Data")
        
        if submit_poultry:
            st.session_state.poultry_logs.append({
                "Date": str(log_date),
                "Eggs Collected": eggs_collected,
                "Broken Eggs": broken_eggs,
                "Feed": feed_given,
                "Health & Notes": health_notes
            })
            st.success("Poultry record added!")

    st.markdown("---")
    st.subheader("Egg Collection & Feeding Logs")
    if st.session_state.poultry_logs:
        st.dataframe(pd.DataFrame(st.session_state.poultry_logs), use_container_width=True)

# ---------------------------------------------------------
# PAGE 5: HARVEST TRACKER
# ---------------------------------------------------------
elif page == "Harvest Tracker":
    st.title("🍇 Fruits & Vegetables Harvest Tracker")
    
    with st.form("harvest_form"):
        crop_harvested = st.text_input("Crop/Produce Name (e.g., Garlic, Passion Fruit, Cucumbers, Peas)")
        quantity = st.text_input("Quantity Harvested (e.g., 25 kg, 3 crates, 50 bunches)")
        harvest_date = st.date_input("Harvest Date", datetime.now())
        quality = st.selectbox("Produce Quality", ["Grade A (Excellent)", "Grade B (Good)", "Local / Consumption"])
        destination = st.text_input("Destination / Use (e.g., Market, Home, Storage)")
        
        submit_harvest = st.form_submit_button("Record Harvest")
        
        if submit_harvest:
            if crop_harvested and quantity:
                st.session_state.harvest_logs.append({
                    "Produce": crop_harvested,
                    "Quantity": quantity,
                    "Date": str(harvest_date),
                    "Quality": quality,
                    "Destination": destination
                })
                st.success(f"Recorded harvest for {crop_harvested}!")
            else:
                st.error("Please specify produce name and quantity.")

    st.markdown("---")
    st.subheader("Harvest History")
    if st.session_state.harvest_logs:
        st.dataframe(pd.DataFrame(st.session_state.harvest_logs), use_container_width=True)

# ---------------------------------------------------------
# PAGE 6: LABOR & CARETAKER WORK LOGS
# ---------------------------------------------------------
elif page == "Labor & Caretaker Work":
    st.title("👷 Daily Work & Caretaker Tracker")
    
    with st.form("labor_form"):
        worker_name = st.text_input("Worker / Caretaker Name")
        work_date = st.date_input("Date", datetime.now())
        tasks_completed = st.text_area("Tasks Completed (e.g., bed weeding, drip irrigation check, poultry feeding, property maintenance)")
        hours_worked = st.number_input("Hours Worked", min_value=0.0, max_value=24.0, step=0.5, value=8.0)
        daily_cost = st.text_input("Daily Payment / Cost (if applicable)")
        
        submit_labor = st.form_submit_button("Save Work Log")
        
        if submit_labor:
            if worker_name and tasks_completed:
                st.session_state.labor_logs.append({
                    "Worker": worker_name,
                    "Date": str(work_date),
                    "Tasks Completed": tasks_completed,
                    "Hours": hours_worked,
                    "Cost": daily_cost
                })
                st.success("Work log saved!")
            else:
                st.error("Please enter worker name and tasks completed.")

    st.markdown("---")
    st.subheader("Work Logs History")
    if st.session_state.labor_logs:
        st.dataframe(pd.DataFrame(st.session_state.labor_logs), use_container_width=True)

# ---------------------------------------------------------
# PAGE 7: ASKARI & SECURITY LOGS
# ---------------------------------------------------------
elif page == "Askari & Security Logs":
    st.title("🛡️ Askari & Night Security Reports")
    
    with st.form("security_form"):
        guard_name = st.text_input("Askari / Guard Name")
        shift_type = st.selectbox("Shift Type", ["Night Shift", "Day Shift", "24-Hour Check"])
        log_date = st.date_input("Date", datetime.now())
        fence_check = st.selectbox("Fence & Gate Status", ["All Clear / Secure", "Fence Maintenance Required", "Breach / Damage Noticed"])
        patrol_observations = st.text_area("Patrol Observations / Night Events (e.g., perimeter checks, lighting status, site safety)")
        incidents = st.text_area("Incidents or Concerns (if any, or type 'None')")
        
        submit_security = st.form_submit_button("Submit Security Report")
        
        if submit_security:
            if guard_name:
                st.session_state.security_logs.append({
                    "Guard Name": guard_name,
                    "Shift": shift_type,
                    "Date": str(log_date),
                    "Fence Status": fence_check,
                    "Observations": patrol_observations,
                    "Incidents": incidents
                })
                st.success("Security log recorded successfully!")
            else:
                st.error("Please enter guard name.")

    st.markdown("---")
    st.subheader("Security & Patrol History")
    if st.session_state.security_logs:
        st.dataframe(pd.DataFrame(st.session_state.security_logs), use_container_width=True)

# ---------------------------------------------------------
# PAGE 8: GARDEN SUPPLIES & REQUIREMENTS
# ---------------------------------------------------------
elif page == "Garden Supplies & Requirements":
    st.title("🛒 Garden & Farm Supplies Requirement List")
    st.write("Track equipment, materials, seeds, tools, and chemicals needed for the garden and farm.")
    
    with st.form("supplies_form"):
        item_name = st.text_input("Item / Material Required (e.g., Drip lines, HDPE pipes, Fencing posts, Omena, Organic fertilizer)")
        category = st.selectbox("Category", ["Irrigation & Water", "Fencing & Infrastructure", "Seeds & Fertilizer", "Poultry Feed & Care", "Tools & Equipment", "General Maintenance"])
        quantity_needed = st.text_input("Quantity / Specification (e.g., 50 meters, 10 posts, 2 bags)")
        priority = st.selectbox("Priority Level", ["High (Urgent)", "Medium", "Low"])
        estimated_cost = st.text_input("Estimated Cost (KSh)")
        
        submit_supply = st.form_submit_button("Add to Requirement List")
        
        if submit_supply:
            if item_name:
                st.session_state.supplies_needed.append({
                    "Item": item_name,
                    "Category": category,
                    "Quantity": quantity_needed,
                    "Priority": priority,
                    "Est Cost": estimated_cost,
                    "Status": "Needed"
                })
                st.success(f"Added '{item_name}' to requirements list!")
            else:
                st.error("Please enter the item name.")

    st.markdown("---")
    st.subheader("Pending Supplies List")
    if st.session_state.supplies_needed:
        df_supplies = pd.DataFrame(st.session_state.supplies_needed)
        st.dataframe(df_supplies, use_container_width=True)
        
        if st.button("Clear Purchased Items List"):
            st.session_state.supplies_needed = [s for s in st.session_state.supplies_needed if s["Status"] == "Needed"]
            st.rerun()

# ---------------------------------------------------------
# PAGE 9: AI FARM ASSISTANT & AUTOMATED REPORT GENERATOR
# ---------------------------------------------------------
elif page == "AI Farm Assistant & Reports":
    st.title("🤖 AI Farm Assistant & Operations Report")
    st.write("Generate a smart breakdown based on your logs: harvests, watering status, fertilizers, and health issues.")

    api_key = st.text_input("Enter Gemini API Key:", type="password")
if st.button("Analyze Logs & Generate Report"):
    if not api_key:
        st.error("Please enter your Gemini API Key first.")
    else:
        try:
            prompt = "You are an expert farm operations manager. Analyze all the farm data below and generate a structured, professional report."
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error generating report: {e}")
    
