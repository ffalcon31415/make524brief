import streamlit as st
import resend
import os

def send_email_to_me(
    plain_text_content: str,
    subject: str,
):
    try:
        FROM_EMAIL_ADDRESS = st.secrets["FROM_EMAIL_ADDRESS"]
        TO_EMAIL_ADDRESS = st.secrets["TO_EMAIL_ADDRESS"]
        RESEND_API_KEY = st.secrets["RESEND_API_KEY"]

    except Exception as e:
        print("Failed to retrieve configuration: " + str(e))
        raise e
    
    # Set the Resend API key
    resend.api_key = RESEND_API_KEY

    try:
        print("Sending email " + str(subject))
        
        params = {
            "from": FROM_EMAIL_ADDRESS,
            "to": [TO_EMAIL_ADDRESS],
            "subject": subject,
            "text": plain_text_content,
        }
        
        email = resend.Emails.send(params)
        print("Sent email")
        
    except Exception as e:
        print("Error sending email: " + str(e))

def check_password():
    """Returns `True` if the user had the correct password."""
    
    import hmac

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["PASSWORD"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the passward is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


def main():

    
    if not check_password():    
        st.stop()  # Do not continue if check_password is not True.

    with st.form(key="my_form", clear_on_submit=True):
        st.markdown("## Create 524 briefs")
        results = st.text_input(
            label="Enter the *accused*  profile number(s) ... *not* the file number. To process more than one, separate them by commas.",

        )
        submitted = st.form_submit_button("Submit")

    if submitted and results:  
        try:
            candidates = [result.strip() for result in results.split(',')]
            list(map(int, candidates))
            results = ",".join(candidates)
        except ValueError:
            st.error("Invalid input. Please enter a number, or a sequence of numbers separated by commas. Try again.")
            results = None

        if results:  
            send_email_to_me(plain_text_content="Message", subject=f"jes streamlit-524 {results}")
            st.balloons()
            st.success(f"Request submitted for scope profile(s): {results.replace(',',', ')}")
            st.markdown(f"Wait a few minutes and then check the [folder]({st.secrets.FOLDER_URL}) for results.")
            st.markdown("#### Reminder it's up to you to both (a) *vet* the briefs and (b) upload and distribute them.")
            


if __name__ == "__main__":
    main()