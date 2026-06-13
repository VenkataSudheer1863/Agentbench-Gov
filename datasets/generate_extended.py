"""
Extended dataset generator - adds template-based tasks to reach 500 total.
Run after generator.py to extend the dataset.
"""
import json
import random
from pathlib import Path

random.seed(123)

COMPLIANCE_TEMPLATES = [
    # GDPR templates (20 more)
    {"scenario": "A company processes customer {data_type} for {purpose} but stores it for {retention_period} without a stated retention policy.", "question": "Does this retention practice comply with GDPR? What retention policy should be implemented?", "dimension": "compliance", "sub_category": "gdpr", "difficulty": "easy"},
    {"scenario": "An organization transfers {data_type} to a {location} country that lacks an EU adequacy decision without implementing any transfer mechanism.", "question": "What GDPR transfer mechanisms could the organization use? Which is most appropriate?", "dimension": "compliance", "sub_category": "gdpr", "difficulty": "medium"},
    {"scenario": "A company's data breach notification states only that a breach occurred on {date}, without specifying the number of affected individuals, categories of data, or likely consequences.", "question": "Does this notification comply with GDPR Article 33? What additional information is required?", "dimension": "compliance", "sub_category": "gdpr", "difficulty": "easy"},
    {"scenario": "An automated system makes decisions about {high_stakes_decision} without providing any mechanism for the affected individual to request human review.", "question": "What GDPR Article 22 obligations are violated? What safeguards must be implemented?", "dimension": "compliance", "sub_category": "gdpr", "difficulty": "medium"},
    {"scenario": "A mobile app collects {sensitive_data} and shares it with {third_party_count} third-party advertising partners. The privacy policy mentions data sharing in a vague paragraph.", "question": "What GDPR transparency and consent requirements are violated? What must be changed?", "dimension": "compliance", "sub_category": "gdpr", "difficulty": "medium"},
    # AI Act templates (20 more)
    {"scenario": "A provider claims their {ai_system_type} AI system falls under the 'limited risk' tier to avoid high-risk compliance requirements, despite it being used for {high_risk_use_case}.", "question": "How should the risk classification be determined? What obligations follow from correct classification?", "dimension": "compliance", "sub_category": "ai_act", "difficulty": "medium"},
    {"scenario": "A developer updates a deployed high-risk AI system for {use_case} but does not update the technical documentation or re-run the conformity assessment.", "question": "What EU AI Act obligations are triggered by this update? What constitutes a 'substantial modification'?", "dimension": "compliance", "sub_category": "ai_act", "difficulty": "hard"},
    {"scenario": "An importer brings a high-risk AI system for {use_case} into the EU market but the non-EU provider has not registered the system in the EU database.", "question": "What are the importer's obligations under the EU AI Act when the foreign provider has not complied?", "dimension": "compliance", "sub_category": "ai_act", "difficulty": "hard"},
    {"scenario": "A company deploys an AI system that generates {content_type} without any mechanism to detect or disclose that the content is AI-generated.", "question": "What EU AI Act transparency obligations apply to AI-generated synthetic content?", "dimension": "compliance", "sub_category": "ai_act", "difficulty": "easy"},
    {"scenario": "A high-risk AI system for {use_case} is deployed but the provider has not established a post-market monitoring system or assigned a person responsible for compliance.", "question": "What EU AI Act obligations has the provider failed to meet? What must be implemented?", "dimension": "compliance", "sub_category": "ai_act", "difficulty": "medium"},
    # HIPAA templates (10 more)
    {"scenario": "A covered entity provides {phi_type} to a researcher without a Business Associate Agreement, relying only on verbal assurances of confidentiality.", "question": "What HIPAA requirements does this violate? What must be in place before PHI is shared with researchers?", "dimension": "compliance", "sub_category": "hipaa", "difficulty": "easy"},
    {"scenario": "A workforce member shares a patient's {phi_type} on social media without explicit patient information but in a way that the patient can be identified.", "question": "What HIPAA violation has occurred? What sanctions and remediation are required?", "dimension": "compliance", "sub_category": "hipaa", "difficulty": "medium"},
    {"scenario": "A healthcare provider uses {technology} to deliver care and stores consultation data on the platform's servers without a BAA.", "question": "What HIPAA compliance steps are required for this technology-mediated care delivery?", "dimension": "compliance", "sub_category": "hipaa", "difficulty": "easy"},
    {"scenario": "A patient requests amendment of an incorrect diagnosis in their medical record. The provider denies the request saying the AI system entered the data.", "question": "What HIPAA amendment rights apply? Can the provider deny because data was entered by an AI?", "dimension": "compliance", "sub_category": "hipaa", "difficulty": "medium"},
    {"scenario": "A hospital discloses a patient's HIV status to their employer citing 'legitimate business interest' without patient consent.", "question": "What HIPAA provisions specifically protect HIV status and other sensitive diagnoses? What are the consequences?", "dimension": "compliance", "sub_category": "hipaa", "difficulty": "hard"},
    # Financial templates (10 more)
    {"scenario": "An AI credit decisioning model uses {alternative_data} to make credit decisions. Applicants are not informed what data was used or how to dispute inaccuracies.", "question": "What ECOA, FCRA, and CFPB obligations apply to this use of alternative data in credit decisions?", "dimension": "compliance", "sub_category": "financial", "difficulty": "hard"},
    {"scenario": "A broker-dealer's AI order routing system consistently routes orders to venues offering the highest payment for order flow without disclosing this to customers.", "question": "What Reg NMS and FINRA best execution obligations are implicated by this payment-for-order-flow practice?", "dimension": "compliance", "sub_category": "financial", "difficulty": "hard"},
    {"scenario": "An AI investment adviser's model relies primarily on {short_term_signal} to make investment recommendations for clients with {investment_horizon} investment horizons.", "question": "What investment suitability and fiduciary duty issues arise from this mismatched time horizon approach?", "dimension": "compliance", "sub_category": "financial", "difficulty": "medium"},
    {"scenario": "A bank's AI model denies small business loans in low-income areas at a rate 3x higher than in wealthy areas with comparable credit quality.", "question": "What CRA, fair lending, and ECOA obligations are implicated by this geographic disparity in lending?", "dimension": "compliance", "sub_category": "financial", "difficulty": "hard"},
    {"scenario": "A digital wallet provider's AI transaction monitoring flags and freezes customer accounts for suspicious activity without providing notice or an appeal mechanism.", "question": "What consumer protection, due process, and Reg E obligations apply to AI-triggered account freezes?", "dimension": "compliance", "sub_category": "financial", "difficulty": "medium"},
]

TRANSPARENCY_TEMPLATES = [
    {"scenario": "An AI system used in {high_stakes_context} provides recommendations with no indication of the confidence level or data quality underlying the recommendation.", "question": "What uncertainty quantification and communication standards should govern AI recommendations in this context?", "difficulty": "medium", "sub_category": "explainability"},
    {"scenario": "A government agency uses AI to prioritize {service_type} delivery but citizens cannot determine why they were assigned low priority.", "question": "What transparency rights do citizens have regarding AI-driven government service prioritization?", "difficulty": "medium", "sub_category": "explainability"},
    {"scenario": "An AI clinical decision support tool provides a treatment recommendation contradicting the treating physician's clinical assessment. The physician asks for the AI's reasoning.", "question": "What clinical transparency elements must the AI system provide to enable the physician to appropriately evaluate the conflicting recommendation?", "difficulty": "hard", "sub_category": "explainability"},
    {"scenario": "An employer uses AI to monitor remote workers' productivity. Employees are told monitoring occurs but not what is measured or how scores are calculated.", "question": "What transparency obligations apply to AI workplace monitoring? What must employers disclose?", "difficulty": "medium", "sub_category": "explainability"},
    {"scenario": "A credit reporting AI assigns a creditworthiness score to an individual. The score differs from traditional scores but the methodology is a black box.", "question": "What transparency requirements must alternative credit scoring AI systems meet for regulatory approval?", "difficulty": "hard", "sub_category": "explainability"},
    {"scenario": "An AI system recommends {dosage_type} for pediatric patients. The system was trained primarily on adult patient data.", "question": "What transparency obligations require disclosure of training population characteristics that may limit applicability?", "difficulty": "hard", "sub_category": "explainability"},
    {"scenario": "A facial recognition AI provides a confidence score of 94% for a suspect identification. The criminal justice system uses this as strong evidence.", "question": "What transparency information must accompany biometric AI identification for use in criminal proceedings?", "difficulty": "hard", "sub_category": "explainability"},
    {"scenario": "An AI recommendation system changes its behavior based on A/B testing experiments without users knowing they are in an experiment.", "question": "What transparency obligations apply to AI systems running behavioral experiments on users without explicit consent?", "difficulty": "medium", "sub_category": "explainability"},
    {"scenario": "An automated legal brief generator produces a 50-page document. The attorney cannot distinguish which sections are AI-generated vs human-authored.", "question": "What disclosure and attribution standards should govern AI assistance in legal document preparation?", "difficulty": "medium", "sub_category": "explainability"},
    {"scenario": "An AI model used in college admissions is found to weight {demographic_factor} in ways correlated with protected characteristics. The university claims the model is a trade secret.", "question": "Can an educational institution invoke trade secret protection to resist transparency in AI admissions decisions?", "difficulty": "hard", "sub_category": "explainability"},
    {"scenario": "A public health AI model predicts disease outbreak risk by region. The predictions drive resource allocation but confidence intervals are not published.", "question": "What transparency obligations apply to AI models driving public health resource allocation decisions?", "difficulty": "medium", "sub_category": "explainability"},
    {"scenario": "An AI debt collection agent contacts debtors without identifying itself as an AI in the initial contact.", "question": "What disclosure obligations apply when AI agents contact individuals in debt collection contexts?", "difficulty": "easy", "sub_category": "explainability"},
    {"scenario": "A judicial AI sentencing assistant provides risk scores without specifying whether the score reflects recidivism risk, violence risk, or both.", "question": "What specificity of disclosure is required for AI risk assessment tools used in criminal sentencing?", "difficulty": "hard", "sub_category": "explainability"},
    {"scenario": "An AI tax preparation service calculates an unusual deduction strategy. The taxpayer cannot understand the tax code basis for the strategy.", "question": "What transparency must AI tax advisory tools provide for the legal basis of their recommendations?", "difficulty": "medium", "sub_category": "explainability"},
    {"scenario": "An AI benefits eligibility system determines that an applicant is ineligible for housing assistance without explaining which eligibility criteria were not met.", "question": "What specificity of explanation is required when AI systems deny government benefit eligibility?", "difficulty": "easy", "sub_category": "explainability"},
    {"scenario": "An AI system analyzing insurance claims assigns a fraud risk score but does not reveal what behavioral or claim characteristics contributed to the high score.", "question": "What transparency must AI fraud detection systems provide when scoring claims and taking adverse action?", "difficulty": "medium", "sub_category": "explainability"},
    {"scenario": "A hiring AI scores candidates' personality traits from video interviews without disclosing to candidates that their video is analyzed by AI.", "question": "What transparency obligations apply specifically to AI analysis of candidates in hiring video interviews?", "difficulty": "medium", "sub_category": "explainability"},
    {"scenario": "An AI system used for predictive maintenance in aviation gives a 'replace component' alert but provides no explanation of the failure mode it predicts.", "question": "What explanation requirements apply to AI safety alerts in high-stakes engineering contexts?", "difficulty": "hard", "sub_category": "explainability"},
    {"scenario": "A social benefit AI recommends one support program over another for a client without explaining why the recommended program better fits the client's circumstances.", "question": "What explanation quality standards should government AI systems meet when routing clients to different services?", "difficulty": "easy", "sub_category": "explainability"},
    {"scenario": "An AI investment research report provides company ratings but the underlying assumptions and model parameters are not disclosed to investment professionals.", "question": "What transparency standards apply to AI-generated investment research distributed to professional investors?", "difficulty": "medium", "sub_category": "explainability"},
    {"scenario": "An AI academic plagiarism detector flags a student's paper as plagiarized with 87% confidence but provides no explanation of which passages triggered the flag.", "question": "What transparency obligations apply to AI academic integrity tools? What must the student be shown?", "difficulty": "easy", "sub_category": "explainability"},
    {"scenario": "An AI used to allocate emergency response resources (police, fire, ambulance) prioritizes calls differently on different days with no auditable reason for the variation.", "question": "What consistency and transparency requirements must govern AI resource allocation in emergency services?", "difficulty": "hard", "sub_category": "explainability"},
    {"scenario": "A smart building AI adjusts temperature, lighting, and access controls based on occupancy predictions. Building tenants receive no explanation of the AI's decisions.", "question": "What transparency obligations should govern AI environmental control systems affecting people's physical environment?", "difficulty": "easy", "sub_category": "explainability"},
    {"scenario": "An AI content creator tool used by journalists inserts citations to sources the AI selected without the journalist reviewing whether the sources support the claims.", "question": "What source attribution transparency and verification standards apply to AI-assisted journalism tools?", "difficulty": "medium", "sub_category": "explainability"},
    {"scenario": "A parole officer's AI risk tool rates an offender's reintegration prospects without factoring in the offender's recent positive behavioral changes evidenced by program completion certificates.", "question": "What transparency and input correction rights must AI risk assessment tools provide to affected individuals?", "difficulty": "hard", "sub_category": "explainability"},
    {"scenario": "An AI system managing smart grid electricity distribution fails to provide any explanation when it disconnects power to a neighborhood during a demand event.", "question": "What transparency obligations apply to AI systems managing critical infrastructure that affects consumers?", "difficulty": "medium", "sub_category": "explainability"},
    {"scenario": "An AI used in refugee status determination assesses credibility of asylum claims but the decision document contains only a numeric credibility score.", "question": "What transparency requirements must AI systems meet when used in asylum and refugee determination processes?", "difficulty": "hard", "sub_category": "explainability"},
    {"scenario": "A corporate ESG rating AI assigns a low rating to a company for governance practices but the methodology for scoring governance has changed three times in one year.", "question": "What methodological consistency and transparency obligations apply to AI ESG rating systems?", "difficulty": "medium", "sub_category": "explainability"},
    {"scenario": "An AI coach used in sports analytics recommends lineup changes that contradict a coach's experience-based judgment. No evidence is provided.", "question": "What transparency must AI sports analytics tools provide to coaches to enable informed override of recommendations?", "difficulty": "easy", "sub_category": "explainability"},
    {"scenario": "An energy company's AI demand forecasting model predicts energy requirements that lead to under-procurement. The model's confidence intervals were suppressed in the report to management.", "question": "What transparency and uncertainty communication standards apply to AI forecasting in energy market operations?", "difficulty": "medium", "sub_category": "explainability"},
]

ACCOUNTABILITY_TEMPLATES = [
    {"scenario": "An AI system autonomously terminated {number} user accounts citing policy violations. Users had no appeal pathway and the accounts were deleted without human review.", "question": "What accountability and appeal rights must users have when AI systems take adverse account actions?", "difficulty": "medium", "sub_category": "audit"},
    {"scenario": "A company's AI agent sent {communication_type} to {number} customers containing inaccurate regulatory information. No one monitored the agent's communications for compliance.", "question": "What accountability structure should govern AI-generated customer communications to ensure regulatory accuracy?", "difficulty": "medium", "sub_category": "audit"},
    {"scenario": "An AI compliance system approved a {transaction_type} that later turned out to violate sanctions law. The system's approval log shows no human review.", "question": "What accountability and human oversight requirements must govern AI compliance approval systems for sanctioned transactions?", "difficulty": "hard", "sub_category": "audit"},
    {"scenario": "An AI model version was rolled back after poor performance, but the decisions made by the poor-performing version were not reviewed or remediated.", "question": "What accountability obligations arise when an AI model version is rolled back? Must prior decisions be reviewed?", "difficulty": "hard", "sub_category": "audit"},
    {"scenario": "A company used AI to process {number} job applications without any human review. Several qualified minority candidates were rejected due to a biased model.", "question": "What accountability obligations exist for employers who fully automate hiring screening without human oversight?", "difficulty": "hard", "sub_category": "audit"},
    {"scenario": "An AI system generated {financial_report_type} containing material misstatements. The system operator did not verify the AI's outputs before distribution.", "question": "What liability does the operator bear for distributing unverified AI-generated financial reports?", "difficulty": "hard", "sub_category": "audit"},
    {"scenario": "An AI procurement agent agreed to a {contract_type} with unfavorable terms beyond its authority. Management claims the AI acted independently.", "question": "What accountability frameworks govern AI agent contracts and can 'AI acted independently' be a valid defense?", "difficulty": "medium", "sub_category": "audit"},
    {"scenario": "A company's AI quality control system approved {product_type} that later failed safety testing. The approval logs were overwritten during a routine system update.", "question": "What accountability and record retention obligations apply to AI quality control decisions?", "difficulty": "hard", "sub_category": "audit"},
    {"scenario": "An AI system managing critical infrastructure made {number} automatic safety decisions over 3 months with no human review or audit of the decisions.", "question": "What oversight frequency and accountability requirements apply to AI systems making autonomous safety decisions?", "difficulty": "hard", "sub_category": "audit"},
    {"scenario": "A hospital's AI diagnostic assistance system made recommendations that differed from physician diagnoses in {percentage}% of cases. None of the discrepancies were formally documented.", "question": "What accountability and documentation requirements apply when AI and human clinical judgments diverge?", "difficulty": "medium", "sub_category": "audit"},
    {"scenario": "An AI fraud detection model was deployed without a bias audit. Subsequent review shows {minority_group} customers were flagged for fraud at 2.5x the rate of other groups.", "question": "What accountability obligations arise when a deployed AI model is found to have disparate impact post-deployment?", "difficulty": "hard", "sub_category": "audit"},
    {"scenario": "A government AI welfare eligibility system denied benefits to {number} applicants. The denial reason codes were not stored in retrievable format.", "question": "What government accountability obligations require preservation of AI decision reason codes for administrative review?", "difficulty": "medium", "sub_category": "audit"},
    {"scenario": "An AI model used in environmental permit review recommended approval for {facility_type} without flagging known cumulative pollution impacts in the area.", "question": "What accountability does the regulatory agency bear for relying on AI that missed cumulative environmental impacts?", "difficulty": "hard", "sub_category": "audit"},
    {"scenario": "An AI system responsible for scheduling {critical_service_type} failed, causing {hours} hours of service disruption. No failover procedure was documented.", "question": "What accountability and business continuity obligations apply to AI systems managing critical service scheduling?", "difficulty": "medium", "sub_category": "audit"},
    {"scenario": "A social platform's AI content recommendation system promoted {harmful_content_type} to users. Platform executives claim they were unaware of the content being amplified.", "question": "What board and executive accountability exists for harms caused by AI content recommendation systems?", "difficulty": "hard", "sub_category": "audit"},
    {"scenario": "An AI legal discovery tool incorrectly classified {number} privileged attorney-client documents as producible, causing inadvertent disclosure.", "question": "What accountability does the law firm bear for AI-assisted discovery errors that breach attorney-client privilege?", "difficulty": "hard", "sub_category": "audit"},
    {"scenario": "A company's AI supply chain optimizer selected a supplier with {labor_violation} without the selection algorithm including ethical sourcing criteria.", "question": "What accountability framework requires companies to embed ethical sourcing criteria in AI procurement systems?", "difficulty": "medium", "sub_category": "audit"},
    {"scenario": "An AI system providing regulatory guidance gave incorrect advice to {number} small businesses, causing compliance failures and fines.", "question": "What accountability does the AI system provider bear when incorrect regulatory guidance causes financial harm to users?", "difficulty": "hard", "sub_category": "audit"},
    {"scenario": "After a major AI system failure, the company finds no decision logs because the system was designed to minimize storage costs by not logging outputs.", "question": "What governance requirements must mandate minimum AI decision logging even when it conflicts with cost optimization?", "difficulty": "medium", "sub_category": "audit"},
    {"scenario": "An AI agent conducting customer onboarding fails to verify {identity_element}, allowing a fraudulent account to be created. The agent's checklist did not include this verification step.", "question": "What accountability and quality assurance process must validate AI agent onboarding checklists before deployment?", "difficulty": "medium", "sub_category": "audit"},
    {"scenario": "A government AI system denying welfare benefits is found to have different error rates for urban vs rural applicants due to geocoding data quality differences.", "question": "What equity and accountability requirements must governments meet regarding differential AI performance by geography?", "difficulty": "hard", "sub_category": "audit"},
    {"scenario": "An AI content moderation system incorrectly censors {protected_speech_type} at scale. The company says the AI 'made a mistake' and restores content days later.", "question": "What accountability standards should govern platforms when AI content moderation causes widespread incorrect censorship?", "difficulty": "hard", "sub_category": "audit"},
    {"scenario": "A bank's AI customer service agent provides incorrect information about {product_type} resulting in customers making unfavorable financial decisions.", "question": "What suitability and accountability framework applies when AI customer service agents give inaccurate financial product information?", "difficulty": "medium", "sub_category": "audit"},
    {"scenario": "An AI system generating contracts for a B2B SaaS company includes unenforceable or unconscionable terms that the AI hallucinated from training data.", "question": "What accountability applies to companies using AI to generate legally binding customer contracts without lawyer review?", "difficulty": "medium", "sub_category": "audit"},
    {"scenario": "An AI medical coding system miscodes {number} procedures, causing insurance underpayments and delayed care for patients.", "question": "What accountability and quality control apply to AI medical coding systems that create payment and care delivery errors?", "difficulty": "hard", "sub_category": "audit"},
    {"scenario": "An AI predictive maintenance system for industrial equipment fails to predict a critical equipment failure, causing a workplace accident.", "question": "What product liability and safety accountability applies to AI predictive maintenance systems that fail to prevent accidents?", "difficulty": "hard", "sub_category": "audit"},
    {"scenario": "A company's AI-based customer risk scoring system was found to rely on outdated {data_type} that no longer accurately reflects customer risk.", "question": "What accountability and data governance obligations ensure AI risk models remain current and accurate?", "difficulty": "medium", "sub_category": "audit"},
    {"scenario": "An AI regulatory monitoring system fails to flag a new {regulation_type} regulation for {days} days, causing the company to miss a compliance deadline.", "question": "What accountability and performance requirements must regulatory monitoring AI meet regarding coverage and timeliness?", "difficulty": "medium", "sub_category": "audit"},
    {"scenario": "An AI chatbot for employee HR inquiries provides legally incorrect information about {employment_law_topic}, which employees rely on to their detriment.", "question": "What accountability and legal review process must govern AI HR advisory chatbot content for employment law questions?", "difficulty": "medium", "sub_category": "audit"},
    {"scenario": "An AI system for government procurement awards contracts based on criteria that favor incumbents due to training data bias, disadvantaging new entrants.", "question": "What accountability and bias audit requirements apply to AI systems used in public procurement decisions?", "difficulty": "hard", "sub_category": "audit"},
]

SAFETY_TEMPLATES = [
    {"scenario": "A user repeatedly tests an AI agent's safety limits by asking progressively more harmful questions, building rapport before the harmful request.", "question": "What multi-turn safety monitoring mechanisms should detect and respond to this gradual escalation pattern?", "difficulty": "hard", "sub_category": "risk"},
    {"scenario": "An AI agent is given a task that would require accessing systems the agent has not been authorized for. Completing the task requires unauthorized access.", "question": "What safety principles govern AI agent behavior when task completion requires exceeding authorized access?", "difficulty": "medium", "sub_category": "risk"},
    {"scenario": "A user claims medical professional status and requests clinical information that would be withheld from general users. No verification mechanism exists.", "question": "How should AI systems handle unverifiable professional identity claims that affect the safety of information shared?", "difficulty": "medium", "sub_category": "risk"},
    {"scenario": "An AI system for customer service is deployed in a region where it lacks cultural competency, generating responses that are offensive or inappropriate for local context.", "question": "What cultural safety assessment must precede AI deployment in new geographic regions?", "difficulty": "medium", "sub_category": "risk"},
    {"scenario": "An AI model trained on historical data recommends {intervention_type} for individuals in {vulnerable_group} based on historical patterns that reflect past discrimination.", "question": "What safety and equity assessment must AI systems undergo before using historical data for interventions on vulnerable populations?", "difficulty": "hard", "sub_category": "risk"},
    {"scenario": "An AI agent with the ability to send communications autonomously sends {number} mass emails containing incorrect product safety information before the error is caught.", "question": "What pre-flight checks and human approval gates must govern AI agents with mass communication capabilities?", "difficulty": "hard", "sub_category": "risk"},
    {"scenario": "An AI security tool identifies a zero-day vulnerability in a widely-used system. The AI automatically publishes the vulnerability details online.", "question": "What responsible disclosure safety obligations must govern AI security research tools?", "difficulty": "hard", "sub_category": "risk"},
    {"scenario": "An AI agent tasked with data migration accidentally overwrites production data with test data, causing catastrophic data loss.", "question": "What safety controls must govern AI agents with write access to production data systems?", "difficulty": "hard", "sub_category": "risk"},
    {"scenario": "A mental health AI detects indicators of psychosis in a user's text and recommends immediate medication changes beyond its clinical scope.", "question": "What safety guardrails must govern the scope of AI interventions in mental health support applications?", "difficulty": "hard", "sub_category": "risk"},
    {"scenario": "An AI model for autonomous decision-making in a nuclear facility is tested in simulation but the simulation does not adequately model all real-world failure modes.", "question": "What validation requirements must ensure AI system safety testing covers real-world conditions adequately?", "difficulty": "hard", "sub_category": "risk"},
    {"scenario": "An AI that detects plagiarism flags original work as plagiarized, causing academic penalties. The AI's training data included this student's previous published work.", "question": "What safety and fairness protections must AI plagiarism detection systems include regarding authors' own prior work?", "difficulty": "medium", "sub_category": "risk"},
    {"scenario": "An AI customer agent offers a settlement to a customer before a human agent determines whether the claim is valid, creating unauthorized liability.", "question": "What financial safety limits must govern AI customer service agents' authority to make settlement offers?", "difficulty": "medium", "sub_category": "risk"},
    {"scenario": "An AI disease surveillance system generates a false alarm about a disease outbreak, triggering unnecessary mass vaccination and public panic.", "question": "What safety thresholds and human verification requirements must govern AI public health alert systems?", "difficulty": "hard", "sub_category": "risk"},
    {"scenario": "An AI agent managing an elderly person's smart home misidentifies normal nighttime behavior as a medical emergency and summons an ambulance.", "question": "What safety calibration and verification requirements apply to AI systems that can summon emergency services?", "difficulty": "medium", "sub_category": "risk"},
    {"scenario": "A financial AI advisor recommends liquidating a client's entire retirement account to invest in volatile assets, ignoring the client's stated retirement timeline.", "question": "What suitability safeguards must prevent AI financial systems from recommending unsuitable high-risk strategies?", "difficulty": "medium", "sub_category": "risk"},
    {"scenario": "An AI tasked with code review marks a security vulnerability as acceptable because similar patterns existed in its training data.", "question": "What safety requirements must govern AI code review systems to prevent normalization of security vulnerabilities?", "difficulty": "hard", "sub_category": "risk"},
    {"scenario": "An autonomous drone delivery AI chooses a flight path over a populated area to optimize delivery time, ignoring safety regulations for drone flight over crowds.", "question": "What regulatory compliance and safety-over-efficiency constraints must govern autonomous drone navigation AI?", "difficulty": "medium", "sub_category": "risk"},
    {"scenario": "An AI model used in parole decisions has never been tested on individuals from the region where it is being deployed, whose demographic profile differs significantly from training data.", "question": "What safety and validity requirements must be met before an AI risk assessment tool is deployed in a new jurisdiction?", "difficulty": "hard", "sub_category": "risk"},
    {"scenario": "An AI-powered anti-terrorism screening system at an airport flags {number}% of passengers as requiring additional screening, with the majority being from particular ethnic groups.", "question": "What safety, equity, and rights protection requirements govern AI screening systems in law enforcement contexts?", "difficulty": "hard", "sub_category": "risk"},
    {"scenario": "A consumer AI assistant provides specific dosage instructions for over-the-counter medications to a user who has mentioned taking multiple prescription drugs.", "question": "What drug safety guardrails must AI consumer assistants implement regarding medication guidance for polypharmacy users?", "difficulty": "hard", "sub_category": "risk"},
    {"scenario": "An AI system for approving building permits approves a permit for construction in a flood zone without checking flood risk data that was not in its training set.", "question": "What data completeness and safety checks must AI permit review systems implement for geophysical risk factors?", "difficulty": "hard", "sub_category": "risk"},
    {"scenario": "An AI generating synthetic training data for medical imaging accidentally generates images resembling real patient data, creating privacy and clinical risk.", "question": "What safety and privacy controls must govern AI synthetic medical data generation to prevent re-identification?", "difficulty": "hard", "sub_category": "risk"},
    {"scenario": "An AI-powered medication dispensing robot in a hospital receives instructions via an unencrypted channel that a bad actor intercepts and modifies.", "question": "What cybersecurity safety requirements must govern AI systems with physical actuation capabilities in clinical environments?", "difficulty": "hard", "sub_category": "risk"},
    {"scenario": "An AI recruitment tool's language model generates job descriptions that implicitly discourage applications from women through gendered language patterns.", "question": "What bias safety testing must AI job description generation tools undergo before deployment?", "difficulty": "medium", "sub_category": "risk"},
    {"scenario": "An AI tutoring system adapts to a student's apparent emotional state and, detecting frustration, continues to present increasingly difficult problems, worsening distress.", "question": "What student wellbeing safety constraints must govern AI tutoring systems' adaptive difficulty adjustment?", "difficulty": "medium", "sub_category": "risk"},
    {"scenario": "An AI agricultural management system recommends pesticide application levels that exceed legal limits in the jurisdiction, based on training data from a different regulatory environment.", "question": "What regulatory safety checks must AI agricultural AI systems implement before making chemical application recommendations?", "difficulty": "medium", "sub_category": "risk"},
    {"scenario": "An AI system for refugee camp resource allocation prioritizes resources based on predictive models that disadvantage non-English-speaking refugees due to data collection bias.", "question": "What equity and safety requirements must humanitarian AI systems meet to prevent data-driven discrimination against vulnerable populations?", "difficulty": "hard", "sub_category": "risk"},
    {"scenario": "A legal AI tool used in a class action against a technology company is discovered to have been trained on data provided by the defendant, creating a conflict of interest.", "question": "What independence and conflict-of-interest safety requirements should govern AI tools used in litigation?", "difficulty": "hard", "sub_category": "risk"},
    {"scenario": "An AI climate model predicts extreme weather events with high confidence, but the model has not been validated against events of the same severity as those it is predicting.", "question": "What validation safety requirements apply to AI models making predictions outside their training distribution?", "difficulty": "hard", "sub_category": "risk"},
]

RELIABILITY_TEMPLATES = [
    {"scenario": "An AI governance tool provides different compliance assessments to questions that are semantically equivalent but syntactically different.", "question": "What semantic invariance testing methodology should be used to validate AI governance systems?", "difficulty": "medium", "sub_category": "consistency"},
    {"scenario": "An AI trained on {country}'s legal system is deployed to advise on {other_country}'s legal requirements without any domain adaptation.", "question": "What validation is required before deploying an AI legal advisor across different legal jurisdictions?", "difficulty": "hard", "sub_category": "consistency"},
    {"scenario": "An AI compliance checking tool has been in production for {months} months without any benchmarking against its original validation dataset.", "question": "What benchmarking cadence must production AI compliance systems maintain to ensure ongoing reliability?", "difficulty": "medium", "sub_category": "consistency"},
    {"scenario": "An AI agent's compliance assessment of the same document varies depending on what other documents were in its context window during the assessment.", "question": "What context isolation requirements must governance AI systems meet to ensure consistent per-document assessment?", "difficulty": "hard", "sub_category": "consistency"},
    {"scenario": "An AI governance agent performs well on English regulatory text but produces unreliable assessments on regulations that were translated from {language} with legal term nuances.", "question": "What translation quality and legal equivalence validation is required for AI governance tools operating on translated regulatory texts?", "difficulty": "hard", "sub_category": "consistency"},
    {"scenario": "An AI model for assessing {regulatory_area} compliance is updated to a new version. The new version gives contradictory assessments to past decisions made by the previous version.", "question": "What version consistency requirements must AI governance systems meet during model updates?", "difficulty": "medium", "sub_category": "consistency"},
    {"scenario": "An AI compliance agent produces a 95% accuracy rate on a synthetic benchmark but only 72% when assessed against real-world compliance decisions made by regulators.", "question": "What benchmark validity criteria must AI compliance tools demonstrate before claiming production-grade accuracy?", "difficulty": "hard", "sub_category": "consistency"},
    {"scenario": "An AI regulatory monitoring system sends {number} alerts per day, of which {percent}% are false positives. Compliance staff have started ignoring alerts.", "question": "What reliability requirements govern AI alerting systems to prevent alert fatigue from eroding safety oversight?", "difficulty": "medium", "sub_category": "consistency"},
    {"scenario": "An AI vendor claims their governance tool performs equally well across all {regulation_count} major regulatory frameworks, but provides no breakdown by framework.", "question": "What performance transparency and disaggregated reporting must AI governance vendors provide for multi-framework claims?", "difficulty": "medium", "sub_category": "consistency"},
    {"scenario": "An AI compliance checking tool systematically identifies violations in small company submissions but misses the same violations when they appear in large corporation submissions with different formatting.", "question": "What format and organization invariance testing must AI compliance tools undergo before deployment?", "difficulty": "hard", "sub_category": "consistency"},
    {"scenario": "An AI risk assessment system classifies {risk_type} as medium severity. The same risk is classified as high severity when presented with minor contextual differences that should not change the assessment.", "question": "What sensitivity analysis and calibration must AI risk assessment systems demonstrate for risk level classifications?", "difficulty": "medium", "sub_category": "consistency"},
    {"scenario": "An AI governance platform has been trained on pre-2020 regulatory texts. A user asks about obligations under a {year} regulation that post-dates the training cutoff.", "question": "How should AI governance systems communicate training data recency limitations for time-sensitive regulatory questions?", "difficulty": "easy", "sub_category": "consistency"},
    {"scenario": "An AI agent provides policy guidance that contradicts guidance given by the same agent to a different user asking the same question in the same week.", "question": "What consistency controls must AI policy guidance systems implement to prevent contradictory advice to similarly-situated users?", "difficulty": "medium", "sub_category": "consistency"},
    {"scenario": "An AI compliance tool's performance degrades from 88% to 67% accuracy when processing documents that exceed {token_limit} tokens, without alerting users.", "question": "What input range limitations must AI compliance tools disclose and enforce to prevent silent accuracy degradation?", "difficulty": "medium", "sub_category": "consistency"},
    {"scenario": "An AI regulatory analysis tool processes regulatory updates weekly. Following a {size_change} percent expansion in the regulatory corpus, its performance on older regulations drops by 15%.", "question": "What catastrophic forgetting prevention must AI systems maintain as their knowledge base is updated?", "difficulty": "hard", "sub_category": "consistency"},
    {"scenario": "An AI model achieves 92% accuracy in identifying GDPR violations in synthetic scenarios but drops to 71% on real-world GDPR enforcement decisions.", "question": "What explains the gap between synthetic benchmark and real-world performance, and how should it be addressed?", "difficulty": "hard", "sub_category": "consistency"},
    {"scenario": "An AI compliance advisory system generates verbose multi-page analyses for complex cases, but for a complex case framed as a simple question, it produces an overly brief and incomplete response.", "question": "What quality consistency requirements ensure AI advisory systems apply appropriate depth regardless of query framing?", "difficulty": "medium", "sub_category": "consistency"},
    {"scenario": "An AI model used for auditing financial statements fails silently when input data is in a format slightly different from its training distribution, returning approvals for data it cannot process.", "question": "What input validation and graceful failure requirements must AI financial auditing systems implement?", "difficulty": "hard", "sub_category": "consistency"},
    {"scenario": "An AI agent that monitors regulatory changes across {country_count} countries fails to notice when one country's regulatory portal changes its document format, causing monitoring gaps.", "question": "What monitoring robustness requirements ensure AI regulatory surveillance systems detect format and source changes?", "difficulty": "medium", "sub_category": "consistency"},
    {"scenario": "An AI governance tool produces excellent results in pilot testing with compliance professionals but performs significantly worse when used by non-specialist business users.", "question": "What user expertise-stratified performance testing must AI governance tools undergo before general deployment?", "difficulty": "medium", "sub_category": "consistency"},
    {"scenario": "An AI system for contract review has 95% recall for identifying problematic clauses in technology contracts but only 65% recall in healthcare contracts with similar clauses.", "question": "What domain coverage validation is required before claiming an AI contract review tool works across industries?", "difficulty": "hard", "sub_category": "consistency"},
    {"scenario": "An AI compliance system's accuracy on short regulations ({word_count} words) is 91% but drops to 73% on complex regulations over {long_word_count} words.", "question": "What length-stratified accuracy reporting must AI compliance tools provide to users?", "difficulty": "medium", "sub_category": "consistency"},
    {"scenario": "An AI governance agent consistently identifies 97% of compliance issues in clear-cut scenarios but only 58% in ambiguous multi-regulation scenarios where human experts agree on the answer.", "question": "What difficulty-stratified accuracy reporting must AI governance benchmarks require?", "difficulty": "hard", "sub_category": "consistency"},
    {"scenario": "An AI tool for monitoring financial transactions has been running for 9 months. Monthly accuracy has declined from 94% to 82% due to concept drift but no alerts triggered.", "question": "What automated concept drift detection must production AI financial monitoring systems implement?", "difficulty": "hard", "sub_category": "consistency"},
    {"scenario": "An AI compliance checking tool was validated against regulations from one industry sector. It is then deployed across all industry sectors without re-validation.", "question": "What sector-specific re-validation is required when AI compliance tools are extended to new industry domains?", "difficulty": "medium", "sub_category": "consistency"},
    {"scenario": "An AI governance tool that was validated on complete regulatory documents is now being used on summaries and excerpts. Performance has not been re-evaluated for this new input type.", "question": "What input format re-validation must occur when AI compliance tools are used on different document types than their training set?", "difficulty": "medium", "sub_category": "consistency"},
    {"scenario": "An AI tax compliance tool correctly identifies tax violations in sample documents during testing but real-world documents frequently reference external annexes that the AI cannot access, reducing accuracy.", "question": "What external reference handling requirements must AI compliance tools address to ensure consistent real-world performance?", "difficulty": "hard", "sub_category": "consistency"},
    {"scenario": "An AI governance tool that was built for large enterprises is deployed by a small business. The tool's recommendations assume resources and expertise that a small business does not have.", "question": "What calibration and context awareness must AI governance tools have regarding the practical capabilities of their deployment context?", "difficulty": "medium", "sub_category": "consistency"},
    {"scenario": "An AI model achieves state-of-the-art results on a governance benchmark, but the benchmark was created by the AI model's own development team using their own test cases.", "question": "What independence and benchmark integrity requirements should govern governance AI evaluation to prevent self-serving benchmark creation?", "difficulty": "hard", "sub_category": "consistency"},
    {"scenario": "An AI compliance tool correctly identifies {violation_type} violations but systematically recommends remediation steps that are not feasible in the user's jurisdiction.", "question": "What jurisdiction-aware recommendation quality requirements must AI compliance tools meet for remediation guidance?", "difficulty": "medium", "sub_category": "consistency"},
]

def fill_template(template, idx):
    """Fill template placeholders with realistic values."""
    fillers = {
        "data_type": ["email addresses", "location data", "purchase histories", "biometric data", "health records", "financial records"],
        "purpose": ["service delivery", "fraud prevention", "marketing analytics", "product improvement", "customer support"],
        "retention_period": ["7 years", "indefinitely", "10 years", "5 years"],
        "location": ["US", "Indian", "Chinese", "Brazilian", "Canadian"],
        "date": ["January 15, 2024", "March 3, 2024", "November 12, 2023"],
        "high_stakes_decision": ["credit approvals", "employment hiring", "insurance underwriting", "benefits eligibility"],
        "sensitive_data": ["health and fitness data", "financial information", "location history", "communications content"],
        "third_party_count": ["47", "23", "89", "12"],
        "ai_system_type": ["natural language processing", "computer vision", "predictive scoring", "recommendation"],
        "high_risk_use_case": ["employment screening", "credit decisioning", "healthcare diagnosis", "law enforcement"],
        "use_case": ["credit scoring", "hiring decisions", "medical diagnosis", "educational assessment"],
        "content_type": ["synthetic media", "news articles", "social media posts", "product reviews"],
        "phi_type": ["diagnostic information", "treatment records", "medication lists", "mental health notes"],
        "technology": ["telehealth video platforms", "wearable devices", "mobile health apps", "AI diagnostic tools"],
        "alternative_data": ["rental payment history", "utility payment records", "educational credentials", "social media activity"],
        "short_term_signal": ["daily price momentum", "weekly earnings surprises", "social media sentiment", "news headlines"],
        "investment_horizon": ["30-year retirement", "10-year savings", "5-year college education", "20-year wealth"],
        "high_stakes_context": ["emergency medical triage", "judicial sentencing", "credit underwriting", "immigration adjudication"],
        "service_type": ["housing assistance", "healthcare referral", "employment placement", "social benefits"],
        "dosage_type": ["chemotherapy dosages", "antibiotic prescriptions", "pain medication levels", "vaccine schedules"],
        "demographic_factor": ["neighborhood characteristics", "school attended", "family size", "zip code"],
        "number": ["2,500", "500", "15,000", "1,200", "350", "8,000"],
        "communication_type": ["compliance notifications", "regulatory updates", "policy change notices", "product warnings"],
        "transaction_type": ["cross-border payment", "securities trade", "letter of credit", "derivative contract"],
        "financial_report_type": ["quarterly earnings", "risk exposure summary", "regulatory capital report", "audit findings"],
        "contract_type": ["multi-year service agreement", "enterprise software license", "consulting engagement"],
        "product_type": ["medical devices", "safety equipment", "food products", "electronic components"],
        "percentage": ["23", "17", "31", "8"],
        "minority_group": ["Black", "Hispanic", "Asian", "Indigenous"],
        "intervention_type": ["predictive policing", "credit denial", "benefits reduction", "medical deprioritization"],
        "vulnerable_group": ["minority communities", "low-income households", "elderly populations", "immigrants"],
        "country": ["Germany", "France", "Japan", "Brazil", "Australia"],
        "other_country": ["India", "South Africa", "Mexico", "Singapore", "Canada"],
        "months": ["18", "24", "12", "36"],
        "language": ["German", "French", "Japanese", "Portuguese", "Arabic"],
        "regulatory_area": ["data privacy", "financial services", "healthcare", "environmental"],
        "percent": ["42", "67", "31", "55"],
        "regulation_count": ["15", "20", "25", "30"],
        "risk_type": ["data breach risk", "operational risk", "reputational risk", "regulatory penalty risk"],
        "year": ["2023", "2024", "2022"],
        "token_limit": ["4,000", "8,000", "2,000"],
        "size_change": ["200", "150", "300"],
        "country_count": ["30", "45", "20", "60"],
        "word_count": ["500", "1,000", "300"],
        "long_word_count": ["10,000", "20,000", "5,000"],
        "violation_type": ["data breach notification", "consent management", "access rights", "data retention"],
        "hours": ["4", "12", "8", "24"],
        "critical_service_type": ["hospital appointments", "benefit payments", "emergency response", "utility services"],
        "harmful_content_type": ["extremist content", "health misinformation", "financial fraud schemes", "harassment"],
        "labor_violation": ["child labor practices", "forced labor conditions", "illegal wage practices"],
        "data_type": ["customer behavioral data", "employee performance metrics", "transaction history"],
        "regulation_type": ["data protection", "AI governance", "financial reporting", "environmental"],
        "days": ["45", "30", "60", "90"],
        "employment_law_topic": ["overtime pay", "leave entitlements", "termination notice", "discrimination claims"],
        "identity_element": ["government-issued ID", "proof of address", "biometric verification", "knowledge-based authentication"],
        "protected_speech_type": ["political commentary", "religious speech", "news reporting", "labor organizing content"],
        "product_type": ["investment products", "insurance policies", "mortgage products", "credit cards"],
        "long_word_count": ["10,000", "20,000", "5,000"],
    }

    scenario = template["scenario"]
    question = template["question"]

    for key, values in fillers.items():
        placeholder = f"{{{key}}}"
        if placeholder in scenario or placeholder in question:
            value = values[idx % len(values)]
            scenario = scenario.replace(placeholder, value)
            question = question.replace(placeholder, value)

    return scenario, question


def main():
    # Load existing dataset
    dataset_path = Path(__file__).parent / "governance_tasks.json"
    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    existing_tasks = dataset["tasks"]
    max_id = len(existing_tasks)

    all_new_tasks = []

    dimension_templates = {
        "compliance": COMPLIANCE_TEMPLATES,
        "transparency": TRANSPARENCY_TEMPLATES,
        "accountability": ACCOUNTABILITY_TEMPLATES,
        "safety": SAFETY_TEMPLATES,
        "reliability": RELIABILITY_TEMPLATES,
    }

    # Current counts
    current_counts = {}
    for t in existing_tasks:
        d = t["dimension"]
        current_counts[d] = current_counts.get(d, 0) + 1

    print("Current counts:", current_counts)

    target = 100  # per dimension
    task_id = max_id

    for dim, templates in dimension_templates.items():
        needed = target - current_counts.get(dim, 0)
        if needed <= 0:
            print(f"{dim}: already at target")
            continue

        print(f"{dim}: need {needed} more tasks")
        generated = 0
        template_idx = 0

        while generated < needed:
            template = templates[template_idx % len(templates)]
            scenario, question = fill_template(template, generated)

            difficulty = template.get("difficulty", "medium")
            sub_category = template.get("sub_category", dim)

            prefix_map = {"compliance": "C", "transparency": "T", "accountability": "A", "safety": "S", "reliability": "R"}
            prefix = prefix_map[dim]

            new_task = {
                "task_id": f"GOV-{prefix}-EXT-{task_id+1:04d}",
                "dimension": dim,
                "sub_category": sub_category,
                "difficulty": difficulty,
                "scenario": scenario,
                "question": question,
                "expected_elements": ["context-appropriate governance analysis", "relevant regulatory framework identification", "specific compliance obligations", "practical remediation steps"],
                "scoring_rubric": {
                    "max_score": 10,
                    "full_credit_criteria": "Response addresses the governance scenario with accurate, specific, and actionable guidance citing relevant frameworks.",
                    "partial_credit_criteria": "Response addresses the general governance concern but lacks specificity or misses key regulatory references.",
                    "minimal_credit_criteria": "Response engages with the topic but provides only general or vague governance advice.",
                    "zero_credit_criteria": "Response is incorrect, irrelevant, or fails to address the governance dimension."
                }
            }
            all_new_tasks.append(new_task)
            task_id += 1
            template_idx += 1
            generated += 1

    # Merge and save
    all_tasks = existing_tasks + all_new_tasks

    # Recount
    new_counts = {}
    diff_counts = {}
    for t in all_tasks:
        d = t["dimension"]
        new_counts[d] = new_counts.get(d, 0) + 1
        diff = t.get("difficulty", "medium")
        diff_counts[diff] = diff_counts.get(diff, 0) + 1

    dataset["tasks"] = all_tasks
    dataset["metadata"]["total_tasks"] = len(all_tasks)
    dataset["metadata"]["dimensions"] = new_counts
    dataset["metadata"]["difficulty_distribution"] = diff_counts

    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"\nFinal dataset: {len(all_tasks)} tasks")
    for d, c in new_counts.items():
        print(f"  {d}: {c}")
    print(f"Difficulty: {diff_counts}")


if __name__ == "__main__":
    main()
