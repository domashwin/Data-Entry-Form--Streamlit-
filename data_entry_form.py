import streamlit as st
import pandas as pd
import os
import csv
import pyzipper
import io 
import datetime


st.write(
    """
# Streamlit Data Entry testing
This is a test of the Streamlit app to input data, which saves to a *.csv* file and can be downloaded
"""
)

st.header("Let's see how it goes", divider="orange")

col1, col2 = st.columns(2)

with col1:
    Rating = st.slider("How much do you like the app?", 1, 100)

with col2:
    st.write("Your :rainbow[***rating***] is", Rating)

st.header("", divider="blue")

# Initialize session state variables
for key in ["CRP", "Hb", "MRN", "DOB", "Completed"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key != "DOB" else None

if "data" not in st.session_state:
    st.session_state.data = []

st.header("Trial Input Form")

# Initialize session flag
if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = False

# Delete button logic
if st.button("Delete Session Data", type="primary"):
    st.session_state.confirm_delete = True

st.write("Please delete session data prior to closing the app")

# Show confirmation step
if st.session_state.confirm_delete:
    st.warning("⚠️ Are you sure you want to delete the CSV file? This cannot be undone.")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("✅ Yes, delete it"):
            if os.path.exists("database.csv"):
                os.remove("database.csv")
                st.session_state.data = []
                st.success("✅ database.csv has been deleted.")
            else:
                st.warning("No Database.csv file found.")
            st.session_state.confirm_delete = False
            st.rerun()  # Auto-refresh UI
    with col2:
        if st.button("❌Cancel"):
            st.session_state.confirm_delete = False
            st.rerun()  # Cancel and refresh




# Button to clear the form manually
if st.button("Clear Form 🧹 ", type="tertiary"):
    # Reset all session state values to defaults
    st.session_state.CRP = ""
    st.session_state.Hb = ""
    st.session_state.MRN = ""
    st.session_state.DOB = None
    st.session_state.Completed = False
    # Clear data input when clicked
    st.success("Form cleared!")
    st.rerun()  # Force Streamlit to rerun and update UI
   

with st.form("Data Entry", clear_on_submit=False, enter_to_submit=False):
    st.write("Input required data fields")
    
    # getting values and retaining them in the sewssion state
    crp_val = st.text_input("CRP", value=st.session_state.CRP)
    hb_val = st.text_input("Hb", value=st.session_state.Hb)
    mrn_val = st.text_input("MRN", value=st.session_state.MRN)
    dob_val = st.date_input("DOB", value=st.session_state.DOB, min_value= datetime.date(1900, 1, 1))
    complete_checkbox = st.checkbox("Mark form as completed", value=st.session_state.Completed)

    submitted = st.form_submit_button("Submit", type='secondary')

    if submitted:
        # Save current inputs back to session state
        st.session_state.CRP = crp_val
        st.session_state.Hb = hb_val
        st.session_state.MRN = mrn_val
        st.session_state.DOB = dob_val
        st.session_state.Completed = complete_checkbox

        if not complete_checkbox:
            st.warning("You must mark the form as completed before submitting.")
        else:
            new_entry = {
                "CRP": crp_val,
                "Hb": hb_val,
                "MRN": mrn_val,
                "DOB": dob_val,
            }

            st.session_state.data.append(new_entry)

            file_exists = os.path.isfile('Database.csv')
            write_header = not file_exists or os.stat('database.csv').st_size == 0

            with open('database.csv', 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=new_entry.keys())
                if write_header:
                    writer.writeheader()
                writer.writerow(new_entry)
            st.success("Entry submitted successfully!")


            # Manually clear form fields after successful submission
            
            
            st.rerun()
            st.session_state.CRP = ""
            st.session_state.Hb = ""
            st.session_state.MRN = ""
            st.session_state.DOB = None
            st.session_state.Completed = False
            
# Display the collected data
df = pd.DataFrame(st.session_state.data)
st.write("Last 3 entries submitted:")
st.write(df.tail(3))


# Convert the DataFrame to CSV format
csv_data = df.to_csv(index=False)


# Password for the ZIP file (this is an example, use your preferred password)
password = "aau1962"


# Create a BytesIO buffer to hold the ZIP data
zip_buffer = io.BytesIO()

# Create the password-protected ZIP file
with pyzipper.AESZipFile(zip_buffer, mode='w', encryption=pyzipper.WZ_AES, compression=pyzipper.ZIP_DEFLATED) as zf:
    zf.setpassword(password.encode())  # Set the password
    zf.writestr("database.csv", csv_data)  # Write the CSV content to the ZIP file

# Seek to the beginning of the buffer
zip_buffer.seek(0)

# Add download button for the password-protected ZIP file
st.download_button(
    label="Download Encrypted ZIP",
    data=zip_buffer,
    file_name="Encrypted_Database.zip",
    mime="application/zip"
)

# Display the password (for demonstration purposes)
# In practice, the password should be provided securely and privately
st.write("Password for the ZIP file", password)
