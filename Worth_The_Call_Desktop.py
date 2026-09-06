import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date


APP_TITLE = "Worth the Call? Senior Benefit Checker"


def category_label(category):
    labels = {
        "high": "Worth a Call",
        "medium": "Maybe Worth a Call",
        "low": "Low Priority / Check Further If Needed",
        "no": "Probably Not Applicable Right Now",
    }
    return labels.get(category, category)


def add_result(results, category, title, contact, why, ask, have_ready=None, caution=None):
    results.append(
        {
            "category": category,
            "title": title,
            "contact": contact,
            "why": why,
            "ask": ask,
            "have_ready": have_ready or [],
            "caution": caution or "",
        }
    )


def checklist_text(results, answers_summary):
    lines = []
    lines.append("WORTH THE CALL? - SENIOR BENEFIT CALL CHECKLIST")
    lines.append(f"Created: {date.today().strftime('%B %d, %Y')}")
    lines.append("")
    lines.append("Important:")
    lines.append(
        "This checklist is for general education only. It is not an approval, denial, legal advice, "
        "tax advice, financial advice, or Medicare plan recommendation."
    )
    lines.append(
        "Only the official agency, state office, Social Security, Medicare, SHIP, Medicaid office, "
        "or your Medicare plan can confirm your situation."
    )
    lines.append("")
    lines.append("Privacy note:")
    lines.append(
        "This tool should not collect your Social Security number, Medicare number, bank information, "
        "full address, or private medical records."
    )
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
    lines.append(
        "Do not pay a company a fee or percentage to 'unlock' Social Security, Medicare Savings Programs, "
        "Extra Help, SHIP counseling, or benefits already included in your Medicare plan."
    )
    lines.append(
        "Be careful with anyone asking for your Medicare number, Social Security number, bank information, "
        "or credit card."
    )
    return "\n".join(lines)


class ScrollableFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas)

        self.inner.bind(
            "<Configure>",
            lambda _e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.window_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Configure>", self._resize_inner)
        self.canvas.bind_all("<MouseWheel>", self._mousewheel)

    def _resize_inner(self, event):
        self.canvas.itemconfigure(self.window_id, width=event.width)

    def _mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def go_top(self):
        self.canvas.yview_moveto(0)


class WorthTheCallApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("980x760")
        self.minsize(840, 620)

        self.style = ttk.Style(self)
        try:
            self.style.theme_use("vista")
        except tk.TclError:
            pass

        self.style.configure("Title.TLabel", font=("Segoe UI", 28, "bold"))
        self.style.configure("Subtitle.TLabel", font=("Segoe UI", 18, "bold"))
        self.style.configure("Heading.TLabel", font=("Segoe UI", 16, "bold"))
        self.style.configure("Question.TLabel", font=("Segoe UI", 11))
        self.style.configure("Body.TLabel", font=("Segoe UI", 10))
        self.style.configure("Big.TButton", font=("Segoe UI", 11, "bold"), padding=8)

        self.scroll = ScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True)
        self.content = self.scroll.inner
        self.content.columnconfigure(0, weight=1)

        self.vars = {}
        self.results = []
        self.last_answers_summary = {}
        self.last_checklist = ""

        self.build_ui()

    def section_box(self, parent, title=None):
        frame = ttk.Frame(parent, padding=14, relief="solid", borderwidth=1)
        if title:
            ttk.Label(frame, text=title, style="Heading.TLabel").pack(anchor="w", pady=(0, 8))
        return frame

    def build_ui(self):
        for child in self.content.winfo_children():
            child.destroy()

        outer = ttk.Frame(self.content, padding=(22, 18, 22, 30))
        outer.grid(row=0, column=0, sticky="nsew")
        outer.columnconfigure(0, weight=1)

        ttk.Label(outer, text="☎ Worth the Call?", style="Title.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(outer, text="Free Senior Benefit Call Checker", style="Subtitle.TLabel").grid(
            row=1, column=0, sticky="w", pady=(8, 16)
        )

        intro = self.section_box(outer)
        intro.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        ttk.Label(
            intro,
            text=(
                "Answer a few quick questions. This tool does not decide if you qualify for benefits. "
                "It helps you figure out which official agency may be worth contacting, what to ask, "
                "and what probably does not apply."
            ),
            style="Body.TLabel",
            wraplength=850,
            justify="left",
        ).pack(anchor="w")

        privacy = self.section_box(outer)
        privacy.grid(row=3, column=0, sticky="ew", pady=(0, 12))
        ttk.Label(
            privacy,
            text=(
                "Privacy promise: Do not enter your Social Security number, Medicare number, bank information, "
                "full address, or private medical records into this tool."
            ),
            style="Body.TLabel",
            wraplength=850,
            justify="left",
        ).pack(anchor="w")

        disclaimer = self.section_box(outer, "Important disclaimer")
        disclaimer.grid(row=4, column=0, sticky="ew", pady=(0, 18))
        ttk.Label(
            disclaimer,
            text=(
                "The information in this tool is based on general program rules available at the time it was made. "
                "Rules, income limits, enrollment periods, state programs, and Medicare plan benefits can change. "
                "This tool is for general education only. It does not guarantee that you qualify for any benefit. "
                "Always confirm your own situation with Social Security, Medicare, SHIP, your state Medicaid office, "
                "your local county/state office, or your Medicare plan."
            ),
            style="Body.TLabel",
            wraplength=850,
            justify="left",
        ).pack(anchor="w")

        ttk.Label(outer, text="Quick Check Questions", style="Heading.TLabel").grid(
            row=5, column=0, sticky="w"
        )
        ttk.Label(
            outer,
            text="Most people can complete this in a few minutes. Choose “Not sure” whenever needed.",
            style="Body.TLabel",
        ).grid(row=6, column=0, sticky="w", pady=(4, 12))

        form = ttk.Frame(outer)
        form.grid(row=7, column=0, sticky="ew")
        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        left = ttk.Frame(form, padding=(0, 0, 12, 0))
        right = ttk.Frame(form, padding=(12, 0, 0, 0))
        left.grid(row=0, column=0, sticky="nsew")
        right.grid(row=0, column=1, sticky="nsew")

        self.add_combo(left, "age", "1. What is your age range?",
                       ["Under 60", "60–64", "65–69", "70+", "Prefer not to say"])
        self.add_radio(left, "receiving_ss", "2. Are you currently receiving Social Security?",
                       ["Yes", "No", "Not sure"])
        self.add_radio(left, "ss_main_income", "3. Is Social Security your main or only income?",
                       ["Yes", "No", "Not sure"])
        self.add_combo(left, "monthly_ss", "4. About how much Social Security do you receive each month?",
                       ["Under $1,500", "$1,500–$2,000", "$2,000–$2,500", "Over $2,500", "Prefer not to say"])
        self.add_combo(left, "marital_status", "5. What is your marital status?",
                       ["Single", "Married", "Divorced", "Widowed", "Separated", "Prefer not to say"])
        self.add_radio(left, "married_10", "6. Were you ever married for 10 years or more?",
                       ["Yes", "No", "Not sure", "Does not apply"])

        self.add_radio(right, "spouse_higher",
                       "7. Does/did your spouse or former spouse likely have a higher Social Security record?",
                       ["Yes", "No", "Not sure", "Does not apply"])
        self.add_radio(right, "medicare", "8. Are you on Medicare?",
                       ["Yes", "No", "Not sure"])
        self.add_combo(right, "coverage_type", "9. Which Medicare coverage do you have?",
                       ["Original Medicare", "Medicare Advantage", "I am not sure", "I am not on Medicare"])
        self.add_radio(right, "prescriptions", "10. Do you take regular prescriptions?",
                       ["Yes", "No", "Prefer not to say"])
        self.add_radio(right, "part_b",
                       "11. Do you pay a Medicare Part B premium from your Social Security check?",
                       ["Yes", "No", "Not sure"])
        self.add_radio(right, "current_help",
                       "12. Do you already receive Medicaid, SSI, SNAP, or state assistance?",
                       ["Yes", "No", "Not sure", "Prefer not to say"])

        bottom = ttk.Frame(outer)
        bottom.grid(row=8, column=0, sticky="ew", pady=(12, 0))
        bottom.columnconfigure(0, weight=1)
        bottom.columnconfigure(1, weight=1)

        self.add_radio(bottom, "owns_home", "13. Do you own your home?",
                       ["Yes", "No", "Prefer not to say"], grid_col=0)
        self.add_radio(bottom, "utility_strain", "14. Are utility bills a strain?",
                       ["Yes", "No", "Prefer not to say"], grid_col=1)

        ttk.Button(
            outer,
            text="Show My Call Checklist",
            command=self.show_results,
            style="Big.TButton",
        ).grid(row=9, column=0, sticky="ew", pady=(20, 8))

        self.results_holder = ttk.Frame(outer)
        self.results_holder.grid(row=10, column=0, sticky="ew")

        self.scroll.go_top()

    def add_combo(self, parent, key, label, options, grid_col=None):
        box = ttk.Frame(parent, padding=(0, 6))
        if grid_col is None:
            box.pack(fill="x", anchor="w")
        else:
            box.grid(row=0, column=grid_col, sticky="nsew", padx=(0 if grid_col == 0 else 12, 12 if grid_col == 0 else 0))
        ttk.Label(box, text=label, style="Question.TLabel", wraplength=390, justify="left").pack(anchor="w")
        var = tk.StringVar(value=options[0])
        self.vars[key] = var
        cb = ttk.Combobox(box, textvariable=var, values=options, state="readonly")
        cb.pack(fill="x", pady=(4, 0))

    def add_radio(self, parent, key, label, options, grid_col=None):
        box = ttk.Frame(parent, padding=(0, 6))
        if grid_col is None:
            box.pack(fill="x", anchor="w")
        else:
            box.grid(row=0, column=grid_col, sticky="nsew", padx=(0 if grid_col == 0 else 12, 12 if grid_col == 0 else 0))
        ttk.Label(box, text=label, style="Question.TLabel", wraplength=390, justify="left").pack(anchor="w")
        var = tk.StringVar(value=options[0])
        self.vars[key] = var
        row = ttk.Frame(box)
        row.pack(fill="x", pady=(3, 0))
        for option in options:
            ttk.Radiobutton(row, text=option, variable=var, value=option).pack(anchor="w")

    def calculate_results(self):
        v = {k: var.get() for k, var in self.vars.items()}
        results = []

        answers_summary = {
            "Age range": v["age"],
            "Receiving Social Security": v["receiving_ss"],
            "Social Security main/only income": v["ss_main_income"],
            "Monthly Social Security range": v["monthly_ss"],
            "Marital status": v["marital_status"],
            "Married 10+ years": v["married_10"],
            "Spouse/former spouse likely higher record": v["spouse_higher"],
            "On Medicare": v["medicare"],
            "Medicare coverage type": v["coverage_type"],
            "Regular prescriptions": v["prescriptions"],
            "Pays Part B premium": v["part_b"],
            "Already receives Medicaid/SSI/SNAP/state help": v["current_help"],
            "Owns home": v["owns_home"],
            "Utility bills are a strain": v["utility_strain"],
        }

        ss_docs = [
            "Your current Social Security monthly benefit amount",
            "Marriage dates, divorce dates, or spouse death information if applicable",
            "Any letters or notices from Social Security",
            "A pen and paper for call notes",
        ]

        marital_status = v["marital_status"]
        spouse_higher = v["spouse_higher"]
        married_10 = v["married_10"]

        if marital_status == "Married":
            if spouse_higher in ["Yes", "Not sure"]:
                add_result(
                    results, "high", "Spousal Social Security benefit review",
                    "Social Security Administration",
                    "You said you are married, and your spouse may have a higher Social Security record.",
                    "“Can you check whether I am receiving the highest benefit available to me, including any spousal benefit?”",
                    ss_docs,
                    "Do not assume this is automatic. Ask Social Security to review your record.",
                )
            else:
                add_result(
                    results, "low", "Spousal Social Security benefit review",
                    "Social Security Administration",
                    "You are married, but you said your spouse likely does not have a higher record.",
                    "“Can you confirm whether any spousal benefit would increase my monthly amount?”",
                    ss_docs,
                )

        elif marital_status == "Divorced":
            if married_10 in ["Yes", "Not sure"]:
                add_result(
                    results, "high", "Divorced-spouse Social Security benefit review",
                    "Social Security Administration",
                    "You said you are divorced and may have been married for 10 years or more.",
                    "“Can you check whether divorced-spouse benefits or survivor benefits on a former spouse’s record may apply to me?”",
                    ss_docs,
                    "This depends on your exact marriage history, current marital status, and Social Security records.",
                )
            else:
                add_result(
                    results, "no", "Divorced-spouse Social Security benefit",
                    "Social Security Administration only if your history changes or you are unsure",
                    "You said you were not married for 10 years or more.",
                    "Check further only if you are unsure about the length of a former marriage or if a former spouse has passed away.",
                    ss_docs,
                )

        elif marital_status == "Widowed":
            add_result(
                results, "high", "Survivor Social Security benefit review",
                "Social Security Administration",
                "You said you are widowed. Survivor benefits may be worth checking if your spouse’s benefit record was higher.",
                "“Can you check whether I am eligible for a survivor benefit or a higher monthly benefit based on my spouse’s record?”",
                ss_docs,
                "Only Social Security can compare the records and confirm the best option.",
            )

        elif marital_status in ["Single", "Separated"]:
            if married_10 in ["Yes", "Not sure"] or spouse_higher == "Yes":
                add_result(
                    results, "medium", "Possible former-spouse or survivor Social Security review",
                    "Social Security Administration",
                    "You are not currently married, but your prior marriage history may matter.",
                    "“Can you check whether divorced-spouse or survivor benefits may apply to me based on a prior marriage?”",
                    ss_docs,
                )
            else:
                add_result(
                    results, "no", "Spousal/divorced-spouse Social Security benefits",
                    "Social Security Administration only if you had a 10+ year marriage, are widowed, or are unsure",
                    "You did not indicate a current marriage, a 10+ year former marriage, or widow/widower status.",
                    "Check further only if you were married for 10 years or more, had a spouse/former spouse pass away, or are unsure.",
                    ss_docs,
                )

        ship_docs = [
            "Your Medicare card",
            "Your Medicare plan card if you have one",
            "Your approximate monthly income",
            "A list of regular prescriptions, if any",
            "Any notices from Medicare, Medicaid, or Social Security",
        ]

        medicare = v["medicare"]
        if medicare == "Yes":
            if v["ss_main_income"] == "Yes" or v["part_b"] in ["Yes", "Not sure"] or v["current_help"] in ["Yes", "Not sure"]:
                add_result(
                    results, "medium", "Medicare Savings Program screening",
                    "SHIP or your state Medicaid office",
                    "You are on Medicare, and Medicare Savings Programs may help some people pay the Part B premium and other Medicare costs. State rules can vary.",
                    "“Can you screen me for a Medicare Savings Program that may help pay my Part B premium or other Medicare costs?”",
                    ship_docs,
                    "Do not decide on your own that you make too much. Ask SHIP or the state office to screen you.",
                )
            else:
                add_result(
                    results, "low", "Medicare Savings Program screening",
                    "SHIP or your state Medicaid office",
                    "You are on Medicare, but your answers do not strongly point to this program. It can still be worth checking if costs are a strain.",
                    "“Can you tell me whether a Medicare Savings Program may apply to me?”",
                    ship_docs,
                )

            if v["prescriptions"] == "Yes":
                add_result(
                    results, "medium", "Extra Help for prescription drug costs",
                    "Social Security, Medicare, or SHIP",
                    "You take regular prescriptions. Extra Help may reduce Medicare Part D drug costs for people with limited income and resources.",
                    "“Can you screen me for Extra Help, also called the Part D Low-Income Subsidy?”",
                    ship_docs,
                    "If you already receive Medicaid, SSI, or certain state help, ask whether you qualify automatically.",
                )
            else:
                add_result(
                    results, "low", "Extra Help for prescription drug costs",
                    "Social Security, Medicare, or SHIP",
                    "You did not say regular prescriptions are an issue right now.",
                    "Check further if prescription costs become a strain or if your medication situation changes.",
                    ship_docs,
                )

        elif medicare == "Not sure":
            add_result(
                results, "medium", "Medicare coverage identification",
                "SHIP",
                "You are not sure whether you are on Medicare. SHIP can help identify your coverage and explain your options.",
                "“Can you help me understand what Medicare coverage I have and whether any cost-help programs may apply?”",
                ship_docs,
            )
        else:
            add_result(
                results, "low", "Medicare benefit screening",
                "SHIP when you become Medicare-eligible or if you are unsure",
                "You said you are not on Medicare.",
                "Ask SHIP about Medicare options when you become eligible or if your coverage status changes.",
                ship_docs,
            )

        plan_docs = [
            "Your Medicare Advantage plan card, if you have one",
            "Your member portal login, if you use one",
            "A pen and paper for the balance, expiration date, and approved stores/items",
        ]

        coverage_type = v["coverage_type"]
        if coverage_type == "Medicare Advantage":
            add_result(
                results, "high", "Medicare Advantage OTC / flex-card benefit",
                "Member Services number on the back of your Medicare Advantage plan card",
                "You said you have Medicare Advantage. Some plans include OTC allowances, flex cards, transportation, dental, vision, or other supplemental benefits.",
                "“Do I have an OTC allowance, flex card, grocery benefit, transportation benefit, or other unused plan benefit? What is my current balance, and when does it expire?”",
                plan_docs,
                "Do not give your Medicare number to random callers. Use the official phone number on your actual plan card.",
            )
        elif coverage_type == "Original Medicare":
            add_result(
                results, "no", "Medicare Advantage OTC / flex-card benefit",
                "SHIP if you want to compare Medicare coverage options",
                "You said you have Original Medicare. OTC/flex-card benefits are usually tied to certain Medicare Advantage plans, not Original Medicare by itself.",
                "“Can you help me compare Original Medicare, Medigap, Part D, and Medicare Advantage options before I make any change?”",
                ["Your Medicare card", "Any Medigap/supplement card", "Your Part D drug plan card", "Your doctor and prescription list"],
                "Do not switch to Medicare Advantage just for an OTC card. Compare doctors, hospitals, prescriptions, prior authorization rules, and yearly out-of-pocket risk first.",
            )
        elif coverage_type == "I am not sure":
            add_result(
                results, "medium", "Check whether you have Original Medicare, Medicare Advantage, Part D, or Medigap",
                "SHIP",
                "Many people are not sure what type of Medicare coverage they have. SHIP can help identify it.",
                "“Can you help me identify my Medicare coverage and whether any plan benefits or cost-help programs may apply?”",
                ship_docs,
            )

        if v["owns_home"] == "Yes":
            add_result(
                results, "medium", "Senior property tax relief",
                "Your county property tax office, county trustee, assessor, or state tax office",
                "You said you own your home. Some counties or states offer senior property tax exemptions, freezes, deferrals, or relief programs.",
                "“Do you have any senior property tax relief, homestead exemption, tax freeze, or tax deferral programs, and how do I apply?”",
                ["Property tax bill", "Proof of age if requested by the office", "Proof of residence if requested by the office"],
                "Property tax programs vary by state and county. The Medicare or Social Security office usually does not handle this.",
            )
        elif v["owns_home"] == "No":
            add_result(
                results, "no", "Senior property tax relief",
                "County/state tax office only if you own property later",
                "You said you do not own your home.",
                "This probably does not apply unless you own property, co-own property, or are responsible for property taxes.",
                [],
            )

        if v["utility_strain"] == "Yes":
            add_result(
                results, "medium", "Utility bill or energy assistance",
                "Local community action agency, Area Agency on Aging, or state benefits office",
                "You said utility bills are a strain. Some areas have energy assistance, weatherization, or local utility relief programs.",
                "“Can you tell me whether I may qualify for energy assistance, weatherization, or senior utility help?”",
                ["Recent utility bill", "Approximate monthly income", "Any shutoff notice if one exists"],
                "Program names and rules vary by state and local area.",
            )

        if v["current_help"] in ["Yes", "Not sure"]:
            add_result(
                results, "medium", "Review whether current benefits unlock other help",
                "SHIP or your state benefits office",
                "You said you receive, or may receive, Medicaid, SSI, SNAP, or state assistance. Some programs can connect to other help.",
                "“Because I receive or may receive state assistance, can you check whether I automatically qualify for Medicare cost help or Extra Help?”",
                ship_docs,
                "Before making changes, ask whether a new benefit affects any assistance you already receive.",
            )

        return results, answers_summary

    def show_results(self):
        self.results, self.last_answers_summary = self.calculate_results()
        self.last_checklist = checklist_text(self.results, self.last_answers_summary)

        for child in self.results_holder.winfo_children():
            child.destroy()

        holder = self.results_holder

        ttk.Separator(holder).pack(fill="x", pady=(18, 14))
        ttk.Label(holder, text="Your checklist is ready.", style="Heading.TLabel").pack(anchor="w")
        ttk.Label(holder, text="Your Quick Call Results", style="Heading.TLabel").pack(anchor="w", pady=(12, 6))

        reality = self.section_box(holder)
        reality.pack(fill="x", pady=(0, 12))
        ttk.Label(
            reality,
            text=(
                "Call reality check: You may not get through on the first try. Busy lines or long hold times "
                "do not mean you are not eligible. Keep notes, try again, and ask for written guidance if possible."
            ),
            style="Body.TLabel",
            wraplength=850,
            justify="left",
        ).pack(anchor="w")

        ttk.Label(holder, text="Best first move", style="Heading.TLabel").pack(anchor="w", pady=(4, 4))
        high_count = len([r for r in self.results if r["category"] == "high"])
        first_move = (
            "Start with the items marked Worth a Call below."
            if high_count > 0
            else "Start with SHIP if your question is Medicare-related, or Social Security if your question is about spousal, divorced-spouse, survivor, or retirement benefits."
        )
        ttk.Label(holder, text=first_move, style="Body.TLabel", wraplength=850, justify="left").pack(anchor="w", pady=(0, 12))

        for cat in ["high", "medium", "low", "no"]:
            group = [r for r in self.results if r["category"] == cat]
            if not group:
                continue
            ttk.Label(holder, text=category_label(cat), style="Heading.TLabel").pack(anchor="w", pady=(10, 6))
            for item in group:
                self.render_result(holder, item)

        contacts = self.section_box(holder, "Official contact starting points")
        contacts.pack(fill="x", pady=(14, 8))
        contact_text = (
            "• Social Security: 1-800-772-1213, Monday–Friday. Ask about retirement, spousal, divorced-spouse, or survivor benefits.\n"
            "• SHIP: Use shiphelp.org to find your local SHIP. Ask for free Medicare counseling and screening.\n"
            "• Medicare: Use Medicare.gov for Medicare basics, plan comparison, Extra Help, and Medicare Savings Program information.\n"
            "• Medicare Advantage plan: Use the Member Services number on the back of your plan card.\n"
            "• County/state offices: Use for property tax relief, utility help, food assistance, and other local programs."
        )
        ttk.Label(contacts, text=contact_text, style="Body.TLabel", wraplength=850, justify="left").pack(anchor="w")

        notes = self.section_box(holder, "What to write down when you call")
        notes.pack(fill="x", pady=(8, 8))
        ttk.Label(
            notes,
            text=(
                "• Date and time of the call\n"
                "• Phone number you called\n"
                "• Name or ID of the person you spoke with\n"
                "• What they said\n"
                "• Whether you need to apply, send documents, call another office, or wait for a letter\n"
                "• Follow-up date"
            ),
            style="Body.TLabel",
            justify="left",
        ).pack(anchor="w")

        scam = self.section_box(holder, "Scam warning")
        scam.pack(fill="x", pady=(8, 12))
        ttk.Label(
            scam,
            text=(
                "You should not have to pay a company a fee or percentage to check these benefits. "
                "Be careful with anyone who calls you, pressures you, asks for your Medicare number, "
                "asks for your Social Security number, asks for bank information, or promises guaranteed money."
            ),
            style="Body.TLabel",
            wraplength=850,
            justify="left",
        ).pack(anchor="w")

        buttons = ttk.Frame(holder)
        buttons.pack(fill="x", pady=(8, 12))
        buttons.columnconfigure(0, weight=1)
        buttons.columnconfigure(1, weight=1)
        buttons.columnconfigure(2, weight=1)

        ttk.Button(
            buttons, text="Download My Call Checklist", command=self.download_checklist, style="Big.TButton"
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ttk.Button(
            buttons, text="Copy Checklist", command=self.copy_checklist, style="Big.TButton"
        ).grid(row=0, column=1, sticky="ew", padx=6)
        ttk.Button(
            buttons, text="Start Over", command=self.start_over, style="Big.TButton"
        ).grid(row=0, column=2, sticky="ew", padx=(6, 0))

        ttk.Label(
            holder,
            text="Worth the Call? is a free educational screening guide. It does not collect private numbers and does not make official eligibility decisions.",
            style="Body.TLabel",
            wraplength=850,
            justify="left",
        ).pack(anchor="w", pady=(8, 18))

        self.after(50, lambda: self.scroll.canvas.yview_moveto(0.60))

    def render_result(self, parent, item):
        frame = self.section_box(parent)
        frame.pack(fill="x", pady=(0, 8))

        ttk.Label(
            frame,
            text=f"{category_label(item['category'])}: {item['title']}",
            style="Heading.TLabel",
            wraplength=820,
            justify="left",
        ).pack(anchor="w", pady=(0, 6))

        ttk.Label(
            frame,
            text=f"Who to contact: {item['contact']}",
            style="Body.TLabel",
            wraplength=820,
            justify="left",
        ).pack(anchor="w")
        ttk.Label(
            frame,
            text=f"Why: {item['why']}",
            style="Body.TLabel",
            wraplength=820,
            justify="left",
        ).pack(anchor="w", pady=(4, 0))
        ttk.Label(
            frame,
            text=f"What to ask:\n{item['ask']}",
            style="Body.TLabel",
            wraplength=820,
            justify="left",
        ).pack(anchor="w", pady=(4, 0))

        if item["have_ready"]:
            ttk.Label(frame, text="What to have ready:", style="Body.TLabel").pack(anchor="w", pady=(6, 0))
            ttk.Label(
                frame,
                text="\n".join(f"• {x}" for x in item["have_ready"]),
                style="Body.TLabel",
                wraplength=820,
                justify="left",
            ).pack(anchor="w")

        if item["caution"]:
            ttk.Label(
                frame,
                text=f"Important: {item['caution']}",
                style="Body.TLabel",
                wraplength=820,
                justify="left",
            ).pack(anchor="w", pady=(6, 0))

    def download_checklist(self):
        if not self.last_checklist:
            return
        path = filedialog.asksaveasfilename(
            title="Save My Call Checklist",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="Worth_the_Call_Senior_Benefit_Checklist.txt",
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.last_checklist)
        messagebox.showinfo("Saved", "Your call checklist was saved successfully.")

    def copy_checklist(self):
        if not self.last_checklist:
            return
        self.clipboard_clear()
        self.clipboard_append(self.last_checklist)
        self.update()
        messagebox.showinfo("Copied", "The checklist was copied to your clipboard.")

    def start_over(self):
        self.build_ui()
        self.scroll.go_top()


if __name__ == "__main__":
    app = WorthTheCallApp()
    app.mainloop()
