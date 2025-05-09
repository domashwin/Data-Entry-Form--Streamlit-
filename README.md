# Data Entry Form for QIP Work

This is an app built using the `streamlit` python module to make a desktop and mobile friendly app which can run in the local browser to simplify/speed up data collection from records by providing a user-friendly data input form.

The app itself contains fields for entering the required data to be collected/stored in a form, which when submitted populate a .csv file (which is also previewed below the form pain)
This .csv file can then be exported using the `pyzipper` library to make a .zip file which is password protected - to protect identifiable/confidential data.
This .csv can then be used as the basis for data analysis work 

The contents of the form are clearable, submission is confirmed with a checkbox, and all session files in the .csv can be deleted by pressing a button before exiting the session.

