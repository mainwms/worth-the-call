const categoryLabels = {
  high: "Worth a Call",
  medium: "Maybe Worth a Call",
  low: "Low Priority / Check Further If Needed",
  no: "Probably Not Applicable Right Now"
};

function addResult(results, category, title, contact, why, ask, haveReady = [], caution = "") {
  results.push({ category, title, contact, why, ask, have_ready: haveReady, caution });
}

function getValue(name) {
  const element = document.querySelector(`[name="${name}"]:checked`) || document.querySelector(`[name="${name}"]`);
  return element ? element.value : "";
}

function calculateResults(v) {
  const results = [];
  const answersSummary = {
    "Age range": v.age,
    "Receiving Social Security": v.receiving_ss,
    "Social Security main/only income": v.ss_main_income,
    "Monthly Social Security range": v.monthly_ss,
    "Marital status": v.marital_status,
    "Married 10+ years": v.married_10,
    "Spouse/former spouse likely higher record": v.spouse_higher,
    "On Medicare": v.medicare,
    "Medicare coverage type": v.coverage_type,
    "Regular prescriptions": v.prescriptions,
    "Pays Part B premium": v.part_b,
    "Already receives Medicaid/SSI/SNAP/state help": v.current_help,
    "Owns home": v.owns_home,
    "Utility bills are a strain": v.utility_strain,
  };

  const ssDocs = [
    "Your current Social Security monthly benefit amount",
    "Marriage dates, divorce dates, or spouse death information if applicable",
    "Any letters or notices from Social Security",
    "A pen and paper for call notes"
  ];

  if (v.marital_status === "Married") {
    if (["Yes", "Not sure"].includes(v.spouse_higher)) {
      addResult(results, "high", "Spousal Social Security benefit review", "Social Security Administration",
        "You said you are married, and your spouse may have a higher Social Security record.",
        "“Can you check whether I am receiving the highest benefit available to me, including any spousal benefit?”",
        ssDocs, "Do not assume this is automatic. Ask Social Security to review your record.");
    } else {
      addResult(results, "low", "Spousal Social Security benefit review", "Social Security Administration",
        "You are married, but you said your spouse likely does not have a higher record.",
        "“Can you confirm whether any spousal benefit would increase my monthly amount?”", ssDocs);
    }
  } else if (v.marital_status === "Divorced") {
    if (["Yes", "Not sure"].includes(v.married_10)) {
      addResult(results, "high", "Divorced-spouse Social Security benefit review", "Social Security Administration",
        "You said you are divorced and may have been married for 10 years or more.",
        "“Can you check whether divorced-spouse benefits or survivor benefits on a former spouse’s record may apply to me?”",
        ssDocs, "This depends on your exact marriage history, current marital status, and Social Security records.");
    } else {
      addResult(results, "no", "Divorced-spouse Social Security benefit", "Social Security Administration only if your history changes or you are unsure",
        "You said you were not married for 10 years or more.",
        "Check further only if you are unsure about the length of a former marriage or if a former spouse has passed away.", ssDocs);
    }
  } else if (v.marital_status === "Widowed") {
    addResult(results, "high", "Survivor Social Security benefit review", "Social Security Administration",
      "You said you are widowed. Survivor benefits may be worth checking if your spouse’s benefit record was higher.",
      "“Can you check whether I am eligible for a survivor benefit or a higher monthly benefit based on my spouse’s record?”",
      ssDocs, "Only Social Security can compare the records and confirm the best option.");
  } else if (["Single", "Separated"].includes(v.marital_status)) {
    if (["Yes", "Not sure"].includes(v.married_10) || v.spouse_higher === "Yes") {
      addResult(results, "medium", "Possible former-spouse or survivor Social Security review", "Social Security Administration",
        "You are not currently married, but your prior marriage history may matter.",
        "“Can you check whether divorced-spouse or survivor benefits may apply to me based on a prior marriage?”", ssDocs);
    } else {
      addResult(results, "no", "Spousal/divorced-spouse Social Security benefits",
        "Social Security Administration only if you had a 10+ year marriage, are widowed, or are unsure",
        "You did not indicate a current marriage, a 10+ year former marriage, or widow/widower status.",
        "Check further only if you were married for 10 years or more, had a spouse/former spouse pass away, or are unsure.", ssDocs);
    }
  }

  const shipDocs = [
    "Your Medicare card",
    "Your Medicare plan card if you have one",
    "Your approximate monthly income",
    "A list of regular prescriptions, if any",
    "Any notices from Medicare, Medicaid, or Social Security"
  ];

  if (v.medicare === "Yes") {
    if (v.ss_main_income === "Yes" || ["Yes", "Not sure"].includes(v.part_b) || ["Yes", "Not sure"].includes(v.current_help)) {
      addResult(results, "medium", "Medicare Savings Program screening", "SHIP or your state Medicaid office",
        "You are on Medicare, and Medicare Savings Programs may help some people pay the Part B premium and other Medicare costs. State rules can vary.",
        "“Can you screen me for a Medicare Savings Program that may help pay my Part B premium or other Medicare costs?”",
        shipDocs, "Do not decide on your own that you make too much. Ask SHIP or the state office to screen you.");
    } else {
      addResult(results, "low", "Medicare Savings Program screening", "SHIP or your state Medicaid office",
        "You are on Medicare, but your answers do not strongly point to this program. It can still be worth checking if costs are a strain.",
        "“Can you tell me whether a Medicare Savings Program may apply to me?”", shipDocs);
    }

    if (v.prescriptions === "Yes") {
      addResult(results, "medium", "Extra Help for prescription drug costs", "Social Security, Medicare, or SHIP",
        "You take regular prescriptions. Extra Help may reduce Medicare Part D drug costs for people with limited income and resources.",
        "“Can you screen me for Extra Help, also called the Part D Low-Income Subsidy?”", shipDocs,
        "If you already receive Medicaid, SSI, or certain state help, ask whether you qualify automatically.");
    } else {
      addResult(results, "low", "Extra Help for prescription drug costs", "Social Security, Medicare, or SHIP",
        "You did not say regular prescriptions are an issue right now.",
        "Check further if prescription costs become a strain or if your medication situation changes.", shipDocs);
    }
  } else if (v.medicare === "Not sure") {
    addResult(results, "medium", "Medicare coverage identification", "SHIP",
      "You are not sure whether you are on Medicare. SHIP can help identify your coverage and explain your options.",
      "“Can you help me understand what Medicare coverage I have and whether any cost-help programs may apply?”", shipDocs);
  } else {
    addResult(results, "low", "Medicare benefit screening", "SHIP when you become Medicare-eligible or if you are unsure",
      "You said you are not on Medicare.",
      "Ask SHIP about Medicare options when you become eligible or if your coverage status changes.", shipDocs);
  }

  const planDocs = [
    "Your Medicare Advantage plan card, if you have one",
    "Your member portal login, if you use one",
    "A pen and paper for the balance, expiration date, and approved stores/items"
  ];

  if (v.coverage_type === "Medicare Advantage") {
    addResult(results, "high", "Medicare Advantage OTC / flex-card benefit",
      "Member Services number on the back of your Medicare Advantage plan card",
      "You said you have Medicare Advantage. Some plans include OTC allowances, flex cards, transportation, dental, vision, or other supplemental benefits.",
      "“Do I have an OTC allowance, flex card, grocery benefit, transportation benefit, or other unused plan benefit? What is my current balance, and when does it expire?”",
      planDocs, "Do not give your Medicare number to random callers. Use the official phone number on your actual plan card.");
  } else if (v.coverage_type === "Original Medicare") {
    addResult(results, "no", "Medicare Advantage OTC / flex-card benefit", "SHIP if you want to compare Medicare coverage options",
      "You said you have Original Medicare. OTC/flex-card benefits are usually tied to certain Medicare Advantage plans, not Original Medicare by itself.",
      "“Can you help me compare Original Medicare, Medigap, Part D, and Medicare Advantage options before I make any change?”",
      ["Your Medicare card", "Any Medigap/supplement card", "Your Part D drug plan card", "Your doctor and prescription list"],
      "Do not switch to Medicare Advantage just for an OTC card. Compare doctors, hospitals, prescriptions, prior authorization rules, and yearly out-of-pocket risk first.");
  } else if (v.coverage_type === "I am not sure") {
    addResult(results, "medium", "Check whether you have Original Medicare, Medicare Advantage, Part D, or Medigap", "SHIP",
      "Many people are not sure what type of Medicare coverage they have. SHIP can help identify it.",
      "“Can you help me identify my Medicare coverage and whether any plan benefits or cost-help programs may apply?”", shipDocs);
  }

  if (v.owns_home === "Yes") {
    addResult(results, "medium", "Senior property tax relief", "Your county property tax office, county trustee, assessor, or state tax office",
      "You said you own your home. Some counties or states offer senior property tax exemptions, freezes, deferrals, or relief programs.",
      "“Do you have any senior property tax relief, homestead exemption, tax freeze, or tax deferral programs, and how do I apply?”",
      ["Property tax bill", "Proof of age if requested by the office", "Proof of residence if requested by the office"],
      "Property tax programs vary by state and county. The Medicare or Social Security office usually does not handle this.");
  } else if (v.owns_home === "No") {
    addResult(results, "no", "Senior property tax relief", "County/state tax office only if you own property later",
      "You said you do not own your home.",
      "This probably does not apply unless you own property, co-own property, or are responsible for property taxes.", []);
  }

  if (v.utility_strain === "Yes") {
    addResult(results, "medium", "Utility bill or energy assistance", "Local community action agency, Area Agency on Aging, or state benefits office",
      "You said utility bills are a strain. Some areas have energy assistance, weatherization, or local utility relief programs.",
      "“Can you tell me whether I may qualify for energy assistance, weatherization, or senior utility help?”",
      ["Recent utility bill", "Approximate monthly income", "Any shutoff notice if one exists"],
      "Program names and rules vary by state and local area.");
  }

  if (["Yes", "Not sure"].includes(v.current_help)) {
    addResult(results, "medium", "Review whether current benefits unlock other help", "SHIP or your state benefits office",
      "You said you receive, or may receive, Medicaid, SSI, SNAP, or state assistance. Some programs can connect to other help.",
      "“Because I receive or may receive state assistance, can you check whether I automatically qualify for Medicare cost help or Extra Help?”",
      shipDocs, "Before making changes, ask whether a new benefit affects any assistance you already receive.");
  }

  return { results, answersSummary };
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
}

function renderResults(results) {
  const container = document.getElementById("results");
  container.innerHTML = "";
  ["high", "medium", "low", "no"].forEach(category => {
    results.filter(r => r.category === category).forEach(item => {
      const card = document.createElement("article");
      card.className = `result-card priority-${category}`;
      let ready = "";
      if (item.have_ready.length) {
        ready = `<p><strong>What to have ready:</strong></p><ul class="have-ready">${item.have_ready.map(x => `<li>${escapeHtml(x)}</li>`).join("")}</ul>`;
      }
      const caution = item.caution ? `<div class="caution"><strong>Important:</strong> ${escapeHtml(item.caution)}</div>` : "";
      card.innerHTML = `
        <h3>${escapeHtml(categoryLabels[category])}: ${escapeHtml(item.title)}</h3>
        <p><strong>Who to contact:</strong> ${escapeHtml(item.contact)}</p>
        <p><strong>Why:</strong> ${escapeHtml(item.why)}</p>
        <p><strong>What to ask:</strong><br>${escapeHtml(item.ask)}</p>
        ${ready}${caution}`;
      container.appendChild(card);
    });
  });
}

function buildChecklist(results, answersSummary) {
  const lines = [];
  const today = new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
  lines.push("WORTH THE CALL? - SENIOR BENEFIT CALL CHECKLIST", `Created: ${today}`, "", "Important:",
    "This checklist is for general education only. It is not an approval, denial, legal advice, tax advice, financial advice, or Medicare plan recommendation.",
    "Only the official agency, state office, Social Security, Medicare, SHIP, Medicaid office, or your Medicare plan can confirm your situation.", "",
    "Privacy note:", "This tool should not collect your Social Security number, Medicare number, bank information, full address, or private medical records.", "", "YOUR ANSWERS SUMMARY");
  Object.entries(answersSummary).forEach(([k, v]) => lines.push(`- ${k}: ${v}`));
  lines.push("");
  ["high", "medium", "low", "no"].forEach(category => {
    const group = results.filter(r => r.category === category);
    if (!group.length) return;
    lines.push(categoryLabels[category].toUpperCase(), "-".repeat(categoryLabels[category].length));
    group.forEach((item, index) => {
      lines.push(`${index + 1}. ${item.title}`, `   Contact: ${item.contact}`, `   Why: ${item.why}`, `   Ask: ${item.ask}`);
      if (item.have_ready.length) {
        lines.push("   Have ready:");
        item.have_ready.forEach(x => lines.push(`   - ${x}`));
      }
      if (item.caution) lines.push(`   Caution: ${item.caution}`);
      lines.push("");
    });
  });
  lines.push("CALL LOG", "Date called: __________________________", "Office / agency: ______________________", "Phone number used: ____________________",
    "Person spoken to: _____________________", "What they said: _______________________", "Next step: ____________________________",
    "Follow-up date: _______________________", "", "SCAM WARNING",
    "Do not pay a company a fee or percentage to 'unlock' Social Security, Medicare Savings Programs, Extra Help, SHIP counseling, or benefits already included in your Medicare plan.",
    "Be careful with anyone asking for your Medicare number, Social Security number, bank information, or credit card.");
  return lines.join("\n");
}

let latestChecklist = "";

document.getElementById("benefitForm").addEventListener("submit", event => {
  event.preventDefault();
  const v = {
    age: getValue("age"), receiving_ss: getValue("receiving_ss"), ss_main_income: getValue("ss_main_income"),
    monthly_ss: getValue("monthly_ss"), marital_status: getValue("marital_status"), married_10: getValue("married_10"),
    spouse_higher: getValue("spouse_higher"), medicare: getValue("medicare"), coverage_type: getValue("coverage_type"),
    prescriptions: getValue("prescriptions"), part_b: getValue("part_b"), current_help: getValue("current_help"),
    owns_home: getValue("owns_home"), utility_strain: getValue("utility_strain")
  };
  const { results, answersSummary } = calculateResults(v);
  renderResults(results);
  latestChecklist = buildChecklist(results, answersSummary);
  document.getElementById("checklistText").value = latestChecklist;
  const resultsSection = document.getElementById("resultsSection");
  resultsSection.classList.remove("hidden");
  resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
});

document.getElementById("downloadBtn").addEventListener("click", () => {
  const blob = new Blob([latestChecklist], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "Worth_the_Call_Senior_Benefit_Checklist.txt";
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
});

document.getElementById("copyBtn").addEventListener("click", async () => {
  const button = document.getElementById("copyBtn");
  try {
    await navigator.clipboard.writeText(latestChecklist);
    const oldText = button.textContent;
    button.textContent = "Copied";
    setTimeout(() => button.textContent = oldText, 1600);
  } catch {
    const textarea = document.getElementById("checklistText");
    textarea.select();
    document.execCommand("copy");
  }
});

document.getElementById("startOverBtn").addEventListener("click", () => {
  document.getElementById("benefitForm").reset();
  document.getElementById("resultsSection").classList.add("hidden");
  document.getElementById("results").innerHTML = "";
  document.getElementById("checklistText").value = "";
  latestChecklist = "";
  window.scrollTo({ top: 0, behavior: "smooth" });
});
