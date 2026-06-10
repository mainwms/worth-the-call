
import streamlit as st
from datetime import date

# ------------------------------------------------------------
# Worth the Call? - Free Senior Benefit Call Checker
# Version: 1.0
# Purpose: Help seniors decide which official benefit calls may be worth making.
# Important: This is not an eligibility decision tool.
# ------------------------------------------------------------

st.set_page_config(
    page_title="Worth the Call? Senior Benefit Checker",
    page_icon="☎️",
    layout="centered"
)

CUSTOM_CSS = """
<style>
    .main .block-container {
        max-width: 920px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        line-height: 1.2;
    }

    .big-note {
        font-size: 1.08rem;
        line-height: 1.55;
        padding: 1rem 1.1rem;
        border-radius: 12px;
        border: 1px solid #ddd;
        background: #f8f8f8;
        margin-bottom: 1rem;
    }

    .safe-box {
        font-size: 1.02rem;
        line-height: 1.55;
        padding: 1rem 1.1rem;
        border-radius: 12px;
        border: 1px solid #c7e0c1;
        background: #f6fff4;
        margin: 1rem 0;
    }

    .warning-box {
        font-size: 1.02rem;
        line-height: 1.55;
        padding: 1rem 1.1rem;
        border-radius: 12px;
        border: 1px solid #f0cf87;
        background: #fff9ec;
        margin: 1rem 0;
    }

    .result-card {
        padding: 1rem 1.1rem;
        border-radius: 14px;
        border: 1px solid #ddd;
        background: #ffffff;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }

    .priority-high {
        border-left: 8px solid #2e7d32;
    }

    .priority-medium {
        border-left: 8px solid #f9a825;
    }

    .priority-low {
        border-left: 8px solid #757575;
    }

    .priority-no {
        border-left: 8px solid #b71c1c;
    }

    .small-muted {
        color: #555;
        font-size: 0.95rem;
        line-height: 1.45;
    }

    div.stButton > button, div.stDownloadButton > button {
        min-height: 3rem;
        font-size: 1.05rem;
        border-radius: 10px;
    }

    label, .stRadio, .stSelectbox, .stCheckbox {
        font-size: 1.05rem !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# -----------------------------
# Helper functions
# -----------------------------

def add_result(results, category, title, contact, why, ask, have_ready=None, caution=None):
    results.append({
        "category": category,
        "title": title,
        "contact": contact,
        "why": why,
        "ask": ask,
        "have_ready": have_ready or [],
        "caution": caution or ""
    })


def category_label(category):
    labels = {
        "high": "Worth a Call",
        "medium": "Maybe Worth a Call",
        "low": "Low Priority / Check Further If Needed",
        "no": "Probably Not Applicable Right Now"
    }
    return labels.get(category, category)


def card_class(category):
    classes = {
        "high": "priority-high",
        "medium": "priority-medium",
        "low": "priority-low",
        "no": "priority-no"
    }
    return classes.get(category, "priority-low")


def render_result_card(item):
    st.markdown(
        f"""
        <div class="result-card {card_class(item['category'])}">
            <h3>{category_label(item['category'])}: {item['title']}</h3>
            <p><strong>Who to contact:</strong> {item['contact']}</p>
            <p><strong>Why:</strong> {item['why']}</p>
            <p><strong>What to ask:</strong><br>{item['ask']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if item["have_ready"]:
        with st.expander("What to have ready"):
            for thing in item["have_ready"]:
                st.write(f"- {thing}")

    if item["caution"]:
        st.markdown(
            f"""
            <div class="warning-box">
            <strong>Important:</strong> {item['caution']}
            </div>
            """,
            unsafe_allow_html=True
        )


def checklist_text(results, answers_summary):
    lines = []
    lines.append("WORTH THE CALL? - SENIOR BENEFIT CALL CHECKLIST")
    lines.append(f"Created: {date.today().strftime('%B %d, %Y')}")
    lines.append("")
    lines.append("Important:")
    lines.append("This checklist is for general education only. It is not an approval, denial, legal advice, tax advice, financial advice, or Medicare plan recommendation.")
    lines.append("Only the official agency, state office, Social Security, Medicare, SHIP, Medicaid office, or your Medicare plan can confirm your situation.")
    lines.append("")
    lines.append("Privacy note:")
    lines.append("This tool should not collect your Social Security number, Medicare number, bank information, full address, or private medical records.")
    lines.append("")
    lines.append("YOUR ANSWERS SUMMARY")
    for k, v in answers_summary.items():
        lines.append(f"- {k}: {v}")
    lines.append("")

    for category in ["high", "medium", "low", "no"]:
        group = [r for r in results if r["category"] == category]
        if not group:
            continue
        lines.append(category_label(category).upper())
        lines.append("-" * len(category_label(category)))
        for idx, item in enumerate(group, start=1):
            lines.append(f"{idx}. {item['title']}")
            lines.append(f"   Contact: {item['contact']}")
            lines.append(f"   Why: {item['why']}")
            lines.append(f"   Ask: {item['ask']}")
            if item["have_ready"]:
                lines.append("   Have ready:")
                for thing in item["have_ready"]:
                    lines.append(f"   - {thing}")
            if item["caution"]:
                lines.append(f"   Caution: {item['caution']}")
            lines.append("")

    lines.append("CALL LOG")
    lines.append("Date called: __________________________")
    lines.append("Office / agency: ______________________")
    lines.append("Phone number used: ____________________")
    lines.append("Person spoken to: _____________________")
    lines.append("What they said: _______________________")
    lines.append("Next step: ____________________________")
    lines.append("Follow-up date: _______________________")
    lines.append("")
    lines.append("SCAM WARNING")
    lines.append("Do not pay a company a fee or percentage to 'unlock' Social Security, Medicare Savings Programs, Extra Help, SHIP counseling, or benefits already included in your Medicare plan.")
    lines.append("Be careful with anyone asking for your Medicare number, Social Security number, bank information, or credit card.")
    return "\n".join(lines)


# -----------------------------
# App header
# -----------------------------

st.title("☎️ Worth the Call?")
st.subheader("Free Senior Benefit Call Checker")

st.markdown(
    """
    <div class="big-note">
    Answer a few quick questions. This tool does <strong>not</strong> decide if you qualify for benefits.
    It helps you figure out which official agency may be worth contacting, what to ask, and what probably does not apply.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="safe-box">
    <strong>Privacy promise:</strong> Do not enter your Social Security number, Medicare number, bank information,
    full address, or private medical records into this tool.
    </div>
    """,
    unsafe_allow_html=True
)

with st.expander("Important disclaimer"):
    st.write(
        "The information in this tool is based on general program rules available at the time it was made. "
        "Rules, income limits, enrollment periods, state programs, and Medicare plan benefits can change. "
        "This tool is for general education only. It does not guarantee that you qualify for any benefit. "
        "Always confirm your own situation with Social Security, Medicare, SHIP, your state Medicaid office, "
        "your local county/state office, or your Medicare plan."
    )


# -----------------------------
# Form
# -----------------------------

st.header("Quick Check Questions")
st.caption("Most people can complete this in a few minutes. Choose “Not sure” whenever needed.")

with st.form("quick_check_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.selectbox(
            "1. What is your age range?",
            ["Under 60", "60–64", "65–69", "70+", "Prefer not to say"]
        )

        receiving_ss = st.radio(
            "2. Are you currently receiving Social Security?",
            ["Yes", "No", "Not sure"]
        )

        ss_main_income = st.radio(
            "3. Is Social Security your main or only income?",
            ["Yes", "No", "Not sure"]
        )

        monthly_ss = st.selectbox(
            "4. About how much Social Security do you receive each month?",
            ["Under $1,500", "$1,500–$2,000", "$2,000–$2,500", "Over $2,500", "Prefer not to say"]
        )

        marital_status = st.selectbox(
            "5. What is your marital status?",
            ["Single", "Married", "Divorced", "Widowed", "Separated", "Prefer not to say"]
        )

        married_10 = st.radio(
            "6. Were you ever married for 10 years or more?",
            ["Yes", "No", "Not sure", "Does not apply"]
        )

    with col2:
        spouse_higher = st.radio(
            "7. Does/did your spouse or former spouse likely have a higher Social Security record?",
            ["Yes", "No", "Not sure", "Does not apply"]
        )

        medicare = st.radio(
            "8. Are you on Medicare?",
            ["Yes", "No", "Not sure"]
        )

        coverage_type = st.selectbox(
            "9. Which Medicare coverage do you have?",
            ["Original Medicare", "Medicare Advantage", "I am not sure", "I am not on Medicare"]
        )

        prescriptions = st.radio(
            "10. Do you take regular prescriptions?",
            ["Yes", "No", "Prefer not to say"]
        )

        part_b = st.radio(
            "11. Do you pay a Medicare Part B premium from your Social Security check?",
            ["Yes", "No", "Not sure"]
        )

        current_help = st.radio(
            "12. Do you already receive Medicaid, SSI, SNAP, or state assistance?",
            ["Yes", "No", "Not sure", "Prefer not to say"]
        )

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        owns_home = st.radio(
            "13. Do you own your home?",
            ["Yes", "No", "Prefer not to say"]
        )

    with col4:
        utility_strain = st.radio(
            "14. Are utility bills a strain?",
            ["Yes", "No", "Prefer not to say"]
        )

    submitted = st.form_submit_button("Show My Call Checklist")


# -----------------------------
# Results logic
# -----------------------------

if submitted:
    results = []

    answers_summary = {
        "Age range": age,
        "Receiving Social Security": receiving_ss,
        "Social Security main/only income": ss_main_income,
        "Monthly Social Security range": monthly_ss,
        "Marital status": marital_status,
        "Married 10+ years": married_10,
        "Spouse/former spouse likely higher record": spouse_higher,
        "On Medicare": medicare,
        "Medicare coverage type": coverage_type,
        "Regular prescriptions": prescriptions,
        "Pays Part B premium": part_b,
        "Already receives Medicaid/SSI/SNAP/state help": current_help,
        "Owns home": owns_home,
        "Utility bills are a strain": utility_strain
    }

    # Social Security benefits
    ss_docs = [
        "Your current Social Security monthly benefit amount",
        "Marriage dates, divorce dates, or spouse death information if applicable",
        "Any letters or notices from Social Security",
        "A pen and paper for call notes"
    ]

    if marital_status == "Married":
        if spouse_higher in ["Yes", "Not sure"]:
            add_result(
                results,
                "high",
                "Spousal Social Security benefit review",
                "Social Security Administration",
                "You said you are married, and your spouse may have a higher Social Security record.",
                "“Can you check whether I am receiving the highest benefit available to me, including any spousal benefit?”",
                ss_docs,
                "Do not assume this is automatic. Ask Social Security to review your record."
            )
        else:
            add_result(
                results,
                "low",
                "Spousal Social Security benefit review",
                "Social Security Administration",
                "You are married, but you said your spouse likely does not have a higher record.",
                "“Can you confirm whether any spousal benefit would increase my monthly amount?”",
                ss_docs
            )

    elif marital_status == "Divorced":
        if married_10 in ["Yes", "Not sure"]:
            add_result(
                results,
                "high",
                "Divorced-spouse Social Security benefit review",
                "Social Security Administration",
                "You said you are divorced and may have been married for 10 years or more.",
                "“Can you check whether divorced-spouse benefits or survivor benefits on a former spouse’s record may apply to me?”",
                ss_docs,
                "This depends on your exact marriage history, current marital status, and Social Security records."
            )
        else:
            add_result(
                results,
                "no",
                "Divorced-spouse Social Security benefit",
                "Social Security Administration only if your history changes or you are unsure",
                "You said you were not married for 10 years or more.",
                "Check further only if you are unsure about the length of a former marriage or if a former spouse has passed away.",
                ss_docs
            )

    elif marital_status == "Widowed":
        add_result(
            results,
            "high",
            "Survivor Social Security benefit review",
            "Social Security Administration",
            "You said you are widowed. Survivor benefits may be worth checking if your spouse’s benefit record was higher.",
            "“Can you check whether I am eligible for a survivor benefit or a higher monthly benefit based on my spouse’s record?”",
            ss_docs,
            "Only Social Security can compare the records and confirm the best option."
        )

    elif marital_status in ["Single", "Separated"]:
        if married_10 in ["Yes", "Not sure"] or spouse_higher == "Yes":
            add_result(
                results,
                "medium",
                "Possible former-spouse or survivor Social Security review",
                "Social Security Administration",
                "You are not currently married, but your prior marriage history may matter.",
                "“Can you check whether divorced-spouse or survivor benefits may apply to me based on a prior marriage?”",
                ss_docs
            )
        else:
            add_result(
                results,
                "no",
                "Spousal/divorced-spouse Social Security benefits",
                "Social Security Administration only if you had a 10+ year marriage, are widowed, or are unsure",
                "You did not indicate a current marriage, a 10+ year former marriage, or widow/widower status.",
                "Check further only if you were married for 10 years or more, had a spouse/former spouse pass away, or are unsure.",
                ss_docs
            )

    # Medicare-related screening
    ship_docs = [
        "Your Medicare card",
        "Your Medicare plan card if you have one",
        "Your approximate monthly income",
        "A list of regular prescriptions, if any",
        "Any notices from Medicare, Medicaid, or Social Security"
    ]

    if medicare == "Yes":
        if ss_main_income == "Yes" or part_b in ["Yes", "Not sure"] or current_help in ["Yes", "Not sure"]:
            add_result(
                results,
                "medium",
                "Medicare Savings Program screening",
                "SHIP or your state Medicaid office",
                "You are on Medicare, and Medicare Savings Programs may help some people pay the Part B premium and other Medicare costs. State rules can vary.",
                "“Can you screen me for a Medicare Savings Program that may help pay my Part B premium or other Medicare costs?”",
                ship_docs,
                "Do not decide on your own that you make too much. Ask SHIP or the state office to screen you."
            )
        else:
            add_result(
                results,
                "low",
                "Medicare Savings Program screening",
                "SHIP or your state Medicaid office",
                "You are on Medicare, but your answers do not strongly point to this program. It can still be worth checking if costs are a strain.",
                "“Can you tell me whether a Medicare Savings Program may apply to me?”",
                ship_docs
            )

        if prescriptions == "Yes":
            add_result(
                results,
                "medium",
                "Extra Help for prescription drug costs",
                "Social Security, Medicare, or SHIP",
                "You take regular prescriptions. Extra Help may reduce Medicare Part D drug costs for people with limited income and resources.",
                "“Can you screen me for Extra Help, also called the Part D Low-Income Subsidy?”",
                ship_docs,
                "If you already receive Medicaid, SSI, or certain state help, ask whether you qualify automatically."
            )
        else:
            add_result(
                results,
                "low",
                "Extra Help for prescription drug costs",
                "Social Security, Medicare, or SHIP",
                "You did not say regular prescriptions are an issue right now.",
                "Check further if prescription costs become a strain or if your medication situation changes.",
                ship_docs
            )

    elif medicare == "Not sure":
        add_result(
            results,
            "medium",
            "Medicare coverage identification",
            "SHIP",
            "You are not sure whether you are on Medicare. SHIP can help identify your coverage and explain your options.",
            "“Can you help me understand what Medicare coverage I have and whether any cost-help programs may apply?”",
            ship_docs
        )
    else:
        add_result(
            results,
            "low",
            "Medicare benefit screening",
            "SHIP when you become Medicare-eligible or if you are unsure",
            "You said you are not on Medicare.",
            "Ask SHIP about Medicare options when you become eligible or if your coverage status changes.",
            ship_docs
        )

    # Medicare Advantage OTC/flex card
    plan_docs = [
        "Your Medicare Advantage plan card, if you have one",
        "Your member portal login, if you use one",
        "A pen and paper for the balance, expiration date, and approved stores/items"
    ]

    if coverage_type == "Medicare Advantage":
        add_result(
            results,
            "high",
            "Medicare Advantage OTC / flex-card benefit",
            "Member Services number on the back of your Medicare Advantage plan card",
            "You said you have Medicare Advantage. Some plans include OTC allowances, flex cards, transportation, dental, vision, or other supplemental benefits.",
            "“Do I have an OTC allowance, flex card, grocery benefit, transportation benefit, or other unused plan benefit? What is my current balance, and when does it expire?”",
            plan_docs,
            "Do not give your Medicare number to random callers. Use the official phone number on your actual plan card."
        )
    elif coverage_type == "Original Medicare":
        add_result(
            results,
            "no",
            "Medicare Advantage OTC / flex-card benefit",
            "SHIP if you want to compare Medicare coverage options",
            "You said you have Original Medicare. OTC/flex-card benefits are usually tied to certain Medicare Advantage plans, not Original Medicare by itself.",
            "“Can you help me compare Original Medicare, Medigap, Part D, and Medicare Advantage options before I make any change?”",
            ["Your Medicare card", "Any Medigap/supplement card", "Your Part D drug plan card", "Your doctor and prescription list"],
            "Do not switch to Medicare Advantage just for an OTC card. Compare doctors, hospitals, prescriptions, prior authorization rules, and yearly out-of-pocket risk first."
        )
    elif coverage_type == "I am not sure":
        add_result(
            results,
            "medium",
            "Check whether you have Original Medicare, Medicare Advantage, Part D, or Medigap",
            "SHIP",
            "Many people are not sure what type of Medicare coverage they have. SHIP can help identify it.",
            "“Can you help me identify my Medicare coverage and whether any plan benefits or cost-help programs may apply?”",
            ship_docs
        )

    # Property tax relief
    if owns_home == "Yes":
        add_result(
            results,
            "medium",
            "Senior property tax relief",
            "Your county property tax office, county trustee, assessor, or state tax office",
            "You said you own your home. Some counties or states offer senior property tax exemptions, freezes, deferrals, or relief programs.",
            "“Do you have any senior property tax relief, homestead exemption, tax freeze, or tax deferral programs, and how do I apply?”",
            ["Property tax bill", "Proof of age if requested by the office", "Proof of residence if requested by the office"],
            "Property tax programs vary by state and county. The Medicare or Social Security office usually does not handle this."
        )
    elif owns_home == "No":
        add_result(
            results,
            "no",
            "Senior property tax relief",
            "County/state tax office only if you own property later",
            "You said you do not own your home.",
            "This probably does not apply unless you own property, co-own property, or are responsible for property taxes.",
            []
        )

    # Utility help
    if utility_strain == "Yes":
        add_result(
            results,
            "medium",
            "Utility bill or energy assistance",
            "Local community action agency, Area Agency on Aging, or state benefits office",
            "You said utility bills are a strain. Some areas have energy assistance, weatherization, or local utility relief programs.",
            "“Can you tell me whether I may qualify for energy assistance, weatherization, or senior utility help?”",
            ["Recent utility bill", "Approximate monthly income", "Any shutoff notice if one exists"],
            "Program names and rules vary by state and local area."
        )

    # Already getting help
    if current_help in ["Yes", "Not sure"]:
        add_result(
            results,
            "medium",
            "Review whether current benefits unlock other help",
            "SHIP or your state benefits office",
            "You said you receive, or may receive, Medicaid, SSI, SNAP, or state assistance. Some programs can connect to other help.",
            "“Because I receive or may receive state assistance, can you check whether I automatically qualify for Medicare cost help or Extra Help?”",
            ship_docs,
            "Before making changes, ask whether a new benefit affects any assistance you already receive."
        )

    # General call-difficulty warning
    st.success("Your checklist is ready.")

    st.header("Your Quick Call Results")

    st.markdown(
        """
        <div class="warning-box">
        <strong>Call reality check:</strong> You may not get through on the first try.
        Busy lines or long hold times do not mean you are not eligible. Keep notes, try again, and ask for written guidance if possible.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Best first call
    high_count = len([r for r in results if r["category"] == "high"])
    if high_count > 0:
        st.subheader("Best first move")
        st.write("Start with the items marked **Worth a Call** below.")
    else:
        st.subheader("Best first move")
        st.write("Start with **SHIP** if your question is Medicare-related, or **Social Security** if your question is about spousal, divorced-spouse, survivor, or retirement benefits.")

    for cat in ["high", "medium", "low", "no"]:
        group = [r for r in results if r["category"] == cat]
        if group:
            st.subheader(category_label(cat))
            for item in group:
                render_result_card(item)

    st.header("Official contact starting points")
    st.markdown(
        """
        - **Social Security:** 1-800-772-1213, Monday–Friday. Ask about retirement, spousal, divorced-spouse, or survivor benefits.
        - **SHIP:** Use shiphelp.org to find your local SHIP. Ask for free Medicare counseling and screening.
        - **Medicare:** Use Medicare.gov for Medicare basics, plan comparison, Extra Help, and Medicare Savings Program information.
        - **Medicare Advantage plan:** Use the Member Services number on the back of your plan card.
        - **County/state offices:** Use for property tax relief, utility help, food assistance, and other local programs.
        """
    )

    st.header("What to write down when you call")
    st.markdown(
        """
        - Date and time of the call
        - Phone number you called
        - Name or ID of the person you spoke with
        - What they said
        - Whether you need to apply, send documents, call another office, or wait for a letter
        - Follow-up date
        """
    )

    st.header("Scam warning")
    st.markdown(
        """
        You should not have to pay a company a fee or percentage to check these benefits.
        Be careful with anyone who calls you, pressures you, asks for your Medicare number,
        asks for your Social Security number, asks for bank information, or promises guaranteed money.
        """
    )

    text = checklist_text(results, answers_summary)

    st.download_button(
        label="Download My Call Checklist",
        data=text,
        file_name="Worth_the_Call_Senior_Benefit_Checklist.txt",
        mime="text/plain"
    )

    with st.expander("Copy/paste version of your checklist"):
        st.text_area("Checklist text", text, height=400)


st.divider()

st.caption(
    "Worth the Call? is a free educational screening guide. It does not collect private numbers and does not make official eligibility decisions."
)
