import streamlit as st
import pandas as pd
import plotly.express as px
from prediction import predict_student_performance

st.set_page_config(
    page_title="ACADEXA",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.stApp {
    background-color: #101225;
    color: #F5F5FF;
}
[data-testid="stSidebar"] {
    background-color: #1B1E38;
}
h1, h2, h3 {
    color: #FFFFFF;
}
.stButton button {
    background-color: #A78BFA;
    color: #101225;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Load dataset
df = pd.read_csv("dataset/cleaned_student_lifestyle_dataset.csv")



# Premium vertical sidebar navigation

pages = {
    "Dashboard": "⌂",
    "Student Profile": "♙",
    "Lifestyle Assessment": "✧",
    "Lifestyle Analytics": "▥",
    "Academic Performance": "▤",
    "Personalized Recommendations": "✦",
    "Study Planner": "▣",
    "GPA Calculator": "∑",
    "Progress Tracker": "◷",
    "Reports & History": "▤"
}

if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"

st.sidebar.markdown("""
<style>
section[data-testid="stSidebar"] div.stButton > button {
    width: 100%;
    text-align: left;
    background: transparent;
    color: #C7C9DD;
    border: none;
    border-radius: 9px;
    padding: 12px 14px;
    margin: 2px 0;
    font-size: 15px;
    transition: 0.2s;
}

section[data-testid="stSidebar"] div.stButton > button:hover {
    background: #292747;
    color: white;
    border: none;
}

section[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    background: #A78BFA;
    color: #17132B;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🎓 ACADEXA")
st.sidebar.caption("STUDENT INTELLIGENCE PLATFORM")
st.sidebar.divider()
st.sidebar.markdown("**MAIN MENU**")

for menu, icon in pages.items():
    if st.sidebar.button(
        f"{icon}   {menu}",
        key=f"nav_{menu}",
        use_container_width=True,
        type="primary" if st.session_state.active_page == menu else "secondary"
    ):
        st.session_state.active_page = menu
        st.rerun()

page = st.session_state.active_page


# Dashboard
if page == "Dashboard":
    st.title("Welcome to ACADEXA 👋")
    st.write("Your Personal Student Lifestyle & Academic Advisor")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Students", len(df))
    col2.metric("Average GPA", round(df["GPA"].mean(), 2))
    col3.metric(
        "Average Attendance",
        f'{df["Attendance_Percentage"].mean():.1f}%'
    )

    st.subheader("Academic Performance Overview")

    chart = px.pie(
        df,
        names="Academic_Performance_Level",
        title="Performance Distribution"
    )
    st.plotly_chart(chart, use_container_width=True)

# Student Profile
elif page == "Student Profile":
    st.title("Student Profile")
    name = st.text_input("Student Name")
    department = st.text_input("Department")
    year = st.selectbox("Year of Study", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
    college = st.text_input("College Name")

    if st.button("Save Profile"):
        st.session_state["student_profile"] = {
            "name": name,
            "department": department,
            "year": year,
            "college": college
        }
        st.success("Profile saved for this session!")

# Lifestyle Assessment
elif page == "Lifestyle Assessment":
    st.title("Lifestyle Assessment")
    st.write("Enter your daily lifestyle details.")

    with st.form("lifestyle_form"):
        study = st.slider("Study Hours per Day", 0.0, 12.0, 5.0)
        extra = st.slider("Extracurricular Hours", 0.0, 8.0, 2.0)
        sleep = st.slider("Sleep Hours", 0.0, 12.0, 8.0)
        social = st.slider("Social Hours", 0.0, 8.0, 3.0)
        activity = st.slider("Physical Activity Hours", 0.0, 6.0, 2.0)
        stress = st.slider("Stress Score", 1, 10, 4)
        attendance = st.slider("Attendance Percentage", 0, 100, 90)

        submitted = st.form_submit_button("Analyze My Lifestyle")

    if submitted:
        result = predict_student_performance(
            study, extra, sleep, social,
            activity, stress, attendance
        )

        st.session_state["latest_prediction"] = result

        st.success("Your assessment is complete!")
        st.metric("Estimated GPA", result["predicted_gpa"])
        st.metric("Predicted Performance", result["performance_level"])

# Lifestyle Analytics
elif page == "Lifestyle Analytics":
    st.title("Lifestyle Analytics")

    column = st.selectbox(
        "Choose a lifestyle factor",
        [
            "Study_Hours_Per_Day",
            "Sleep_Hours_Per_Day",
            "Social_Hours_Per_Day",
            "Stress_Score",
            "Physical_Activity_Hours_Per_Day"
        ]
    )

    fig = px.histogram(df, x=column, title="Lifestyle Distribution")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.scatter(
        df,
        x=column,
        y="GPA",
        title=f"{column} vs GPA"
    )
    st.plotly_chart(fig2, use_container_width=True)

# Academic Performance
elif page == "Academic Performance":
    st.title("Academic Performance")
    st.metric("Dataset Average GPA", round(df["GPA"].mean(), 2))
    st.metric(
        "Average Attendance",
        f'{df["Attendance_Percentage"].mean():.1f}%'
    )

    st.subheader("Performance Level Distribution")
    st.bar_chart(df["Academic_Performance_Level"].value_counts())

# Personalized Recommendations
elif page == "Personalized Recommendations":
    st.title("Personalized Recommendations")

    result = st.session_state.get("latest_prediction")

    if result:
        st.subheader("Your Recommendations")

        if result["performance_level"] == "Low":
            st.write("- Create a regular study schedule.")
            st.write("- Improve attendance and revision habits.")
            st.write("- Maintain a healthy sleep routine.")

        elif result["performance_level"] == "Medium":
            st.write("- Increase focused study time gradually.")
            st.write("- Practice regular revision.")
            st.write("- Balance study and physical activity.")

        else:
            st.write("- Maintain your consistent study routine.")
            st.write("- Continue regular revision.")
            st.write("- Participate in skill development activities.")
    else:
        st.info("Complete Lifestyle Assessment to receive recommendations.")

# Study Planner
elif page == "Study Planner":
    st.title("Study Planner")

    subject = st.text_input("Subject")
    task = st.text_input("Study Task")
    hours = st.number_input("Planned Hours", 0.5, 12.0, 1.0)

    if st.button("Add Study Task"):
        tasks = st.session_state.get("tasks", [])
        tasks.append({
            "Subject": subject,
            "Task": task,
            "Hours": hours
        })
        st.session_state["tasks"] = tasks
        st.success("Task added!")

    st.write(st.session_state.get("tasks", []))

# GPA Calculator
elif page == "GPA Calculator":
    st.title("GPA Calculator")

    subjects = st.number_input("Number of Subjects", 1, 15, 5)
    total = 0
    credits = 0

    for i in range(int(subjects)):
        col1, col2 = st.columns(2)
        with col1:
            mark = st.number_input(
                f"Grade Point - Subject {i+1}",
                0.0, 10.0, 8.0,
                key=f"mark_{i}"
            )
        with col2:
            credit = st.number_input(
                f"Credits - Subject {i+1}",
                1, 10, 3,
                key=f"credit_{i}"
            )

        total += mark * credit
        credits += credit

    if st.button("Calculate GPA"):
        st.success(f"Your GPA is: {total / credits:.2f}")

# Progress Tracker
elif page == "Progress Tracker":
    st.title("Progress Tracker")

    result = st.session_state.get("latest_prediction")

    if result:
        st.metric("Latest Estimated GPA", result["predicted_gpa"])
        st.metric("Latest Performance Level", result["performance_level"])
    else:
        st.info("Complete your first Lifestyle Assessment to view progress.")

# Reports & History
elif page == "Reports & History":
    st.title("Reports & History")

    result = st.session_state.get("latest_prediction")

    if result:
        st.write("Latest Assessment")
        st.json(result)
        st.download_button(
            "Download Assessment Report",
            data=pd.DataFrame([result]).to_csv(index=False),
            file_name="ACADEXA_report.csv",
            mime="text/csv"
        )
    else:
        st.info("No assessment history available yet.")

st.sidebar.divider()
st.sidebar.caption("ACADEXA | AI-Powered Student Advisor")