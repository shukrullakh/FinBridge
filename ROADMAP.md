# FinBridge — Hackathon Development Roadmap

> **Product concept:** AI-powered financial wellness platform  
> **Core promise:** Don’t just track money. Train your financial behavior.  
> **Target:** Working web MVP for a hackathon  
> **Planning status:** Proposed roadmap; checkboxes are intentionally unchecked until work is verified.

---

## 0. Product direction and scope

- [ ] Confirm FinBridge as the product name and retain the SMARTMIND concept as the behavioral-finance foundation (or decide whether SMARTMIND remains a feature/working title).
- [ ] Confirm the primary demo audience and one representative user persona.
- [ ] Define the single hackathon problem statement: impulsive spending, weak saving habits, and fragmented debt obligations.
- [ ] Freeze the MVP scope: Dashboard, Smart Pause, Invisible Savings, Debt Coach, Financial Behavior Score.
- [ ] Agree that the MVP uses manual/demo transactions; no live bank connection or real payment blocking is promised.
- [ ] Define the demo story and measurable success criteria.
- [ ] Set a feature freeze date before the presentation.

## 1. Discovery and requirements

### 1.1 Problem and users
- [ ] Write a concise problem statement.
- [ ] Define the target user: a young adult/student or early-career user managing income, expenses, savings, and installments.
- [ ] List the top three user pain points.
- [ ] Map each pain point to one product capability.
- [ ] Define what the product explicitly does not do in the hackathon MVP.

### 1.2 User journeys
- [ ] First-time user opens the app and sees a seeded/demo financial snapshot.
- [ ] User records or reviews a transaction.
- [ ] User enters a planned purchase and receives a Smart Pause intervention.
- [ ] User creates a savings goal and sees round-up savings simulated.
- [ ] User enters debts and compares repayment strategies.
- [ ] User reviews their Financial Behavior Score and understands how it was calculated.

### 1.3 Acceptance criteria
- [ ] Every core screen has a clear empty, loading, success, and error state where relevant.
- [ ] Currency is displayed consistently in UZS.
- [ ] Calculations are deterministic and performed by application logic, not invented by the AI.
- [ ] Demo data is clearly identified as sample data.
- [ ] No feature implies that the app can stop a real bank/card payment.

## 2. Product design and UX

- [ ] Define visual direction, typography, spacing, color tokens, and component rules.
- [ ] Create a responsive information architecture for desktop and mobile web.
- [ ] Design the main navigation.
- [ ] Design Dashboard.
- [ ] Design Smart Pause flow.
- [ ] Design Savings goals and round-up simulation.
- [ ] Design Debt Coach and repayment comparison.
- [ ] Design Financial Behavior Score breakdown.
- [ ] Design AI explanation/recommendation states.
- [ ] Design onboarding or demo-user entry.
- [ ] Review accessibility: contrast, keyboard focus, labels, and readable number formats.
- [ ] Validate the full demo flow with a clickable prototype or implemented screens.

## 3. Technical foundation

### 3.1 Repository and environment
- [ ] Create repository and agree on branching/commit conventions.
- [ ] Add README, `.gitignore`, environment example, and license decision.
- [ ] Create frontend and backend project structure.
- [ ] Add formatter, linter, and type checking.
- [ ] Add local development instructions.
- [ ] Add Docker Compose only if it accelerates reliable local setup.
- [ ] Configure separate development and demo environment variables.

### 3.2 Backend foundation
- [ ] Initialize FastAPI application.
- [ ] Add configuration management and environment validation.
- [ ] Add health-check endpoint.
- [ ] Configure PostgreSQL and migrations (if using a persistent database).
- [ ] Define consistent API response and error formats.
- [ ] Add request validation and structured logging.
- [ ] Add CORS configuration for the web client.
- [ ] Add API documentation and version prefix (for example `/api/v1`).

### 3.3 Frontend foundation
- [ ] Initialize the selected web stack (recommended: React + TypeScript + Vite).
- [ ] Configure routing.
- [ ] Configure API client and error handling.
- [ ] Build reusable layout, navigation, cards, forms, dialogs, and charts.
- [ ] Add responsive breakpoints.
- [ ] Add currency/date formatting utilities.
- [ ] Add mock/demo data mode so the presentation does not depend on fragile external services.

## 4. Core MVP features

### 4.1 Dashboard
- [ ] Show total income, expenses, and available balance for the selected period.
- [ ] Show spending by category.
- [ ] Show recent transactions.
- [ ] Show savings goal progress.
- [ ] Show debt summary and upcoming due dates.
- [ ] Show Financial Behavior Score with a clear explanation.
- [ ] Add date-range or monthly filtering.
- [ ] Verify totals against backend calculation tests.

### 4.2 Transactions and spending limits
- [ ] Define transaction fields: amount, type, category, date, note, and source.
- [ ] Add transaction create, read, update, and delete flows if time permits.
- [ ] Add category management or a fixed MVP category list.
- [ ] Add user-defined spending limits / “red lines” by category.
- [ ] Show remaining category budget.
- [ ] Seed realistic Uzbek-market demo transactions.

### 4.3 Smart Pause — signature feature
- [ ] Let a user enter a planned purchase amount and category.
- [ ] Let a user configure a category spending limit (“red line”).
- [ ] Evaluate purchase against available budget and category limit using deterministic rules.
- [ ] Display a clear reason when the purchase triggers a warning.
- [ ] Offer a 15-minute cooling-off timer as a behavioral prompt (the app does not block payment).
- [ ] Show purchase impact on the current budget and savings goal.
- [ ] Offer reflection prompts such as “Is this necessary now?” and “Would you still want it tomorrow?”
- [ ] Let user choose: postpone, proceed, or cancel.
- [ ] Record the decision for later behavior analysis.
- [ ] Add tests for threshold boundaries and unusual amounts.
- [ ] Prepare one compelling, reproducible live-demo scenario.

### 4.4 Invisible Savings — simulated round-up
- [ ] Let user create a savings goal with target amount and target date.
- [ ] Implement round-up calculation for eligible recorded transactions.
- [ ] Show the amount that would be moved to savings for each transaction.
- [ ] Aggregate simulated round-ups into the savings balance.
- [ ] Show progress, remaining amount, and estimated completion date.
- [ ] Allow user to configure the round-up step (for example, nearest 1,000 or 5,000 UZS).
- [ ] Clearly label this as an in-app simulation; no real money transfer occurs.
- [ ] Test rounding, zero values, refunds, and transaction exclusions.

### 4.5 Debt Coach
- [ ] Let user add a debt: name, principal/balance, interest rate (optional), minimum payment, due date, and type.
- [ ] Support informal debt with no interest rate.
- [ ] Calculate a Snowball repayment order.
- [ ] Calculate an Avalanche repayment order when interest rates are available.
- [ ] Compare estimated payoff time and total interest under stated assumptions.
- [ ] Generate a month-by-month suggested repayment plan.
- [ ] Show upcoming due dates.
- [ ] Explain assumptions and warn that estimates depend on accurate user-entered data.
- [ ] Test zero-interest, missing-interest, and minimum-payment edge cases.

### 4.6 Financial Behavior Score
- [ ] Define a transparent score model before displaying a score.
- [ ] Use understandable dimensions: spending discipline, saving consistency, debt payment discipline, and goal progress.
- [ ] Define data sufficiency rules; show “not enough data” instead of a misleading score.
- [ ] Show dimension-level breakdown and plain-language explanations.
- [ ] Show change over time only when comparable historical data exists.
- [ ] Avoid presenting the score as a credit score, diagnosis, or measure of personal worth.
- [ ] Add unit tests for each score component and boundary.
- [ ] Document the formula and its limitations in the product.

## 5. AI layer

- [ ] Decide which interactions genuinely benefit from AI; keep core calculations outside the model.
- [ ] Define a strict structured input containing only the minimum necessary financial context.
- [ ] Build an AI prompt for explaining spending patterns and suggesting practical actions.
- [ ] Build an AI prompt for explaining Smart Pause warnings without shaming the user.
- [ ] Build an AI prompt for explaining Debt Coach strategies based on backend-calculated results.
- [ ] Require the model to distinguish known data from assumptions and never invent balances.
- [ ] Validate model output and handle timeout, rate limit, and provider errors.
- [ ] Add a deterministic fallback if the AI provider is unavailable.
- [ ] Protect API keys on the server; never expose them in frontend code.
- [ ] Add consent and privacy messaging before sending personal financial context.
- [ ] Prepare a scripted fallback response for the hackathon demo.

## 6. Data model and API

- [ ] Define entities: User/DemoProfile, Transaction, Category, BudgetLimit, SavingsGoal, SavingsContribution, Debt, PurchaseDecision, ScoreSnapshot.
- [ ] Define relationships, indexes, and data ownership rules.
- [ ] Decide whether authentication is required for the hackathon or a controlled demo profile is sufficient.
- [ ] Implement transaction endpoints.
- [ ] Implement dashboard summary endpoint.
- [ ] Implement budget-limit endpoints.
- [ ] Implement Smart Pause evaluation endpoint.
- [ ] Implement savings goal and round-up endpoints.
- [ ] Implement debt and repayment-plan endpoints.
- [ ] Implement score calculation endpoint.
- [ ] Implement AI explanation endpoint.
- [ ] Add API contract examples and error cases.
- [ ] Add database seed script for demo data.

## 7. Quality, privacy, and security

- [ ] Add unit tests for money calculations and business rules.
- [ ] Add API integration tests for critical flows.
- [ ] Add frontend form validation and error states.
- [ ] Ensure monetary values use decimal-safe arithmetic (never binary floating-point for financial calculations).
- [ ] Validate and normalize all user input.
- [ ] Enforce user-level data access if accounts are enabled.
- [ ] Keep secrets in environment variables.
- [ ] Avoid logging sensitive financial details or AI prompts.
- [ ] Add basic rate limiting to AI endpoints if feasible.
- [ ] Add a clear demo-data notice and privacy explanation.
- [ ] Test keyboard navigation and responsive layouts.
- [ ] Run a final smoke test on the presentation device/browser.

## 8. Demo readiness and presentation

- [ ] Prepare a clean demo account with realistic sample data.
- [ ] Prepare a 3–5 minute end-to-end demo script.
- [ ] Start with the user's financial problem, not the technology stack.
- [ ] Demonstrate Smart Pause as the signature moment.
- [ ] Show how a purchase decision affects savings and the score.
- [ ] Demonstrate Debt Coach with two debts and compare strategies.
- [ ] Show the score breakdown and explain why it changes.
- [ ] Prepare architecture diagram and concise technology slide.
- [ ] Prepare a clear explanation of what is simulated vs. real.
- [ ] Prepare screenshots or a short backup recording.
- [ ] Test internet/API failure fallback.
- [ ] Assign presentation roles and rehearse transitions.
- [ ] Prepare answers to questions about AI accuracy, data privacy, bank integrations, and monetization.

## 9. Post-hackathon backlog (not MVP commitments)

- [ ] Real bank/payment-provider integrations, subject to access, legal, and security requirements.
- [ ] Automated transaction import.
- [ ] Real round-up transfers through an authorized provider.
- [ ] Notifications and reminders.
- [ ] Family/shared budgets.
- [ ] Student-focused financial mode.
- [ ] Uzbek, Russian, and English localization.
- [ ] Advanced forecasting and scenario simulator.
- [ ] Financial education and challenges.
- [ ] Export and account deletion workflows.
- [ ] Production observability, backups, and disaster recovery.

---

## Suggested execution order

1. **Scope lock and demo story** — decide exactly what will be shown.
2. **Design and foundation** — build the shell and seeded demo data.
3. **Core calculations** — transactions, budgets, round-ups, debts, and score.
4. **Signature experience** — Smart Pause end-to-end.
5. **AI explanation layer** — add AI only after deterministic results work.
6. **Polish and test** — responsive UI, edge cases, and fallbacks.
7. **Presentation rehearsal** — freeze features and verify the demo.

## Definition of Done

A task is complete only when:
- [ ] The implementation exists in the repository.
- [ ] Its acceptance criteria are met.
- [ ] Relevant tests or a documented manual verification have passed.
- [ ] UI states and errors are handled.
- [ ] `PROJECT.md` is updated if architecture, scope, data, or product behavior changed.
- [ ] The task is reviewed by the team.

> **Rule:** Do not check a box because work has started. Check it only after verification.
