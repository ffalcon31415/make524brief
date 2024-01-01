import streamlit as st
from decouple import config

from sendgrid import SendGridAPIClient  # type:ignore
from sendgrid.helpers.mail import (
    Mail,
    To,
    From,
)  # type:ignore
from python_http_client import exceptions  # type:ignore

import os

def send_email_to_me(
    plain_text_content: str,
    subject: str,
):
    try:
        FROM_EMAIL_ADDRESS = config("FROM_EMAIL_ADDRESS")
        TO_EMAIL_ADDRESS = config("TO_EMAIL_ADDRESS")
        SENDGRID_KEY = config("SENDGRID_KEY")

    except Exception as e:
        print("Failed to retrieve configuration: " + str(e))
        raise e
    
    to_emails = [To(email=TO_EMAIL_ADDRESS)]
    email = Mail(
        from_email=From(email=FROM_EMAIL_ADDRESS),
        to_emails=to_emails,
        subject=subject,
        plain_text_content=plain_text_content,
    )



    try:
        sg = SendGridAPIClient(SENDGRID_KEY)
        response = sg.send(email)
        print("Sent email")

    except exceptions.BadRequestsError as e:
        print("Error sending email: " + str(e.body))


def main():
    try:
        PASSWORD = config("PASSWORD")
    except Exception as e:
        print("Failed to retrieve configuration: " + str(e))
        raise e
    with st.form(key="my_form", clear_on_submit=True):
        st.markdown("# Create 524 briefs")
        result = st.text_input(
            label="Enter the *accused*  profile number(s) ... *not* the file number. To process more than one, separate them by commas.",

        )
        password = st.text_input(label="Enter the password",type='password')
        submitted = st.form_submit_button("Submit")
    if password != PASSWORD:
        st.toast("Wrong password!")  
    elif submitted and result:    
        print(result)
        send_email_to_me(plain_text_content="Message", subject=f"jes streamlit-524 {result}")
        st.toast("Request submitted! Wait a few minutes and then check the folder.")

if __name__ == "__main__":
    main()