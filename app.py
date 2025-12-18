import streamlit as st
import time
import os

# ------------------- AUTO CREATE requirements.txt -------------------
# This ensures Streamlit Cloud can install the correct version automatically.
req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
if not os.path.exists(req_path):
    with open(req_path, "w") as f:
        f.write("streamlit==1.40.0\n")

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="WalkQuote", page_icon="🚶", layout="centered")

# ------------------- STYLING -------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #d0f0c0, #a2d9ce, #d6eaf8);
    background-attachment: fixed;
    color: #1B2631;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #16a085, #1abc9c);
    color: white;
}

h1, h2, h3 {
    color: #0e6251;
    text-align: center;
    font-weight: bold;
}

.stButton>button {
    background-color: #1abc9c;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6rem 1.2rem;
    font-size: 1rem;
}

.stButton>button:hover {
    background-color: #117a65;
    color: #fff;
}

.chat-bubble {
    border-radius: 12px;
    padding: 10px 15px;
    margin: 5px 0;
    max-width: 70%;
}
.sender { background-color: #a3e4d7; margin-left: auto; }
.receiver { background-color: #d6eaf8; margin-right: auto; }

.quote {
    font-style: italic;
    color: #0e6655;
    text-align: center;
    font-size: 1.6rem;
    font-weight: 600;
    padding: 1rem;
    border-left: 5px solid #1abc9c;
    border-right: 5px solid #1abc9c;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.6);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ------------------- SESSION STATE -------------------
for key, default in {
    "logged_in": False,
    "username": "",
    "role": None,
    "matched": False,
    "messages": [],
    "walk_status": "NOT_STARTED",
    "payment_done": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ------------------- FUNCTIONS -------------------
def send_message(sender, text):
    st.session_state.messages.append({"sender": sender, "text": text})

def reset_app():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

# ------------------- QUOTE HEADER -------------------
st.markdown('<p class="quote">"Every step you take brings peace to your mind and strength to your soul."</p>', unsafe_allow_html=True)
st.divider()

# ------------------- LOGIN PAGE -------------------
if not st.session_state.logged_in:
    st.subheader("Login or Sign Up to Continue")

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if username and password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome back, {username}! 🌟")
                st.rerun()
            else:
                st.error("Please enter both username and password.")

    with tab2:
        new_user = st.text_input("Create Username", key="signup_user")
        new_pass = st.text_input("Create Password", type="password", key="signup_pass")
        if st.button("Sign Up"):
            if new_user and new_pass:
                st.session_state.logged_in = True
                st.session_state.username = new_user
                st.success(f"Account created for {new_user}! 🎉")
                st.rerun()
            else:
                st.error("Please fill all fields.")
    st.stop()

# ------------------- ROLE SELECTION -------------------
if st.session_state.role is None:
    st.subheader(f"Hello {st.session_state.username}! Choose Your Role")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🧍‍♀️ I'm a Wanderer"):
            st.session_state.role = "Wanderer"
            st.rerun()
    with c2:
        if st.button("🚶 I'm a Walker"):
            st.session_state.role = "Walker"
            st.rerun()

# ------------------- WANDERER VIEW -------------------
elif st.session_state.role == "Wanderer":
    st.subheader(f"Welcome, {st.session_state.username} 🌸")
    if not st.session_state.matched:
        st.info("Searching for nearby walkers...")
        if st.button("🔍 Find a Walker"):
            with st.spinner("Finding your walking partner..."):
                time.sleep(2)
                st.session_state.matched = True
                st.success("🎉 Walker found: Sarah D. is nearby!")
                st.rerun()
    else:
        if st.session_state.walk_status == "NOT_STARTED":
            st.success("Matched with Sarah D. (Verified Walker ✅)")
            st.image("walkquote.png", use_column_width=True)
            msg = st.text_input("💬 Type your message:")
            if st.button("Send Message"):
                if msg.strip():
                    send_message("You", msg.strip())
                    time.sleep(0.2)
                    st.rerun()

            for chat in st.session_state.messages:
                css_class = "sender" if chat["sender"] == "You" else "receiver"
                st.markdown(f'<div class="chat-bubble {css_class}"><b>{chat["sender"]}:</b> {chat["text"]}</div>', unsafe_allow_html=True)

            if st.button("🚶 Start Walk"):
                st.session_state.walk_status = "IN_PROGRESS"
                st.success("Walk started! Enjoy your journey 🌿")
                st.rerun()

        elif st.session_state.walk_status == "IN_PROGRESS":
            st.subheader("🚶 Walk in Progress")
            st.info("You’re walking with Sarah D.")
            st.write("You can chat while walking:")
            msg = st.text_input("💬 Say something during walk:")
            if st.button("Send During Walk"):
                if msg.strip():
                    send_message("You", msg.strip())
                    st.rerun()

            for chat in st.session_state.messages[-5:]:
                css_class = "sender" if chat["sender"] == "You" else "receiver"
                st.markdown(f'<div class="chat-bubble {css_class}"><b>{chat["sender"]}:</b> {chat["text"]}</div>', unsafe_allow_html=True)

            if st.button("🏁 End Walk"):
                st.session_state.walk_status = "COMPLETED"
                st.success("Walk completed successfully! 💚")
                st.rerun()

        elif st.session_state.walk_status == "COMPLETED" and not st.session_state.payment_done:
            st.balloons()
            st.subheader("Walk Completed 🎉")
            st.write("Distance: 1.2 miles | Duration: 30 mins")
            st.info("Please complete your payment.")
            if st.button("💳 Pay Now"):
                st.session_state.payment_done = True
                st.success("Payment Successful ✅")
                st.rerun()

        elif st.session_state.payment_done:
            st.success("Thank you for walking with WalkQuote! 🌼")
            st.button("🔁 New Walk", on_click=reset_app)

# ------------------- WALKER VIEW -------------------
elif st.session_state.role == "Walker":
    st.subheader(f"Welcome, {st.session_state.username} 👣")
    if not st.session_state.matched:
        st.info("Waiting for a Wanderer to request a walk...")
        if st.button("👀 Accept Request"):
            st.session_state.matched = True
            st.success("You are now connected with a Wanderer!")
            st.rerun()
    else:
        if st.session_state.walk_status == "NOT_STARTED":
            st.success("You’re matched with a Wanderer! Start chatting below:")
            msg = st.text_input("💬 Type your message:")
            if st.button("Send Message"):
                if msg.strip():
                    send_message("You", msg.strip())
                    time.sleep(0.2)
                    st.rerun()

            for chat in st.session_state.messages:
                css_class = "sender" if chat["sender"] == "You" else "receiver"
                st.markdown(f'<div class="chat-bubble {css_class}"><b>{chat["sender"]}:</b> {chat["text"]}</div>', unsafe_allow_html=True)

            if st.button("🚶 Start Walk"):
                st.session_state.walk_status = "IN_PROGRESS"
                st.success("Walk started successfully 🚶‍♀️")
                st.rerun()

        elif st.session_state.walk_status == "IN_PROGRESS":
            st.subheader("Walk in Progress 🌿")
            st.info("You’re walking with your Wanderer partner.")
            msg = st.text_input("💬 Say something during walk:")
            if st.button("Send During Walk"):
                if msg.strip():
                    send_message("You", msg.strip())
                    st.rerun()

            for chat in st.session_state.messages[-5:]:
                css_class = "sender" if chat["sender"] == "You" else "receiver"
                st.markdown(f'<div class="chat-bubble {css_class}"><b>{chat["sender"]}:</b> {chat["text"]}</div>', unsafe_allow_html=True)

            if st.button("🏁 End Walk"):
                st.session_state.walk_status = "COMPLETED"
                st.success("Walk completed successfully ✅")
                st.rerun()

        elif st.session_state.walk_status == "COMPLETED":
            st.subheader("Walk Finished 💚")
            st.success("Your partner will complete payment soon.")
            if st.button("🔁 Ready for Next Walk"):
                reset_app()
