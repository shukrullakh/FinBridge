# FinBridge — Project Definition

> **Working product name:** FinBridge  
> **Concept foundation:** SMARTMIND — behavioral finance  
> **Product category:** AI-powered financial wellness web application  
> **Current target:** Hackathon MVP  
> **Primary currency:** Uzbek soʻm (UZS)  
> **Document status:** Initial product and technical baseline — decisions marked “Proposed” require team confirmation.

---

## 1. Executive summary

FinBridge is a web-based financial wellness platform designed to help people improve the way they make everyday financial decisions.

Many people experience financial stress not only because of limited income, but also because of impulsive purchases, inconsistent saving habits, and difficulty managing several debts or installment obligations at once.

FinBridge turns financial awareness into practical behavioral support. Instead of only displaying historical spending, it helps users pause before a questionable purchase, build saving habits through simulated round-ups, compare debt repayment strategies, and understand their financial behavior through a transparent score.

**Core message:** Don’t just track money. Train your financial behavior.

## 2. Vision and mission

### Vision
Make healthier financial decision-making accessible, understandable, and practical for everyday users.

### Mission
Help users build financial discipline through behavioral nudges, clear financial insights, and personalized guidance.

### Product principle
FinBridge should help users make their own informed decisions. It should not shame users, make unsupported promises, or pretend to control bank payments.

## 3. Problem statement

The initial concept identifies three connected behavioral problems:

1. **Impulse spending:** People sometimes make unplanned purchases in response to emotion or convenience.
2. **Difficulty saving:** Large monthly saving targets can feel painful or unrealistic, making consistency difficult.
3. **Debt complexity:** Users may have bank loans, installment purchases, and informal debts with different amounts, rates, and due dates.

These problems are especially relevant to users managing UZS income and local installment obligations in Uzbekistan.

### Core question
How can technology improve the way people make financial decisions?

## 4. Target users

### Primary persona — young adult / student / early-career user
- Receives a limited or variable monthly income.
- Makes frequent everyday purchases.
- Wants to save for a meaningful goal.
- May have installment payments or informal debts.
- Benefits from simple explanations and practical nudges.

### Secondary persona
A working adult who wants one place to understand spending, saving, and debt obligations.

### Initial market focus
Uzbekistan, with UZS-first calculations and Uzbek-language product copy. Russian and English localization may follow if time allows.

## 5. Value proposition

FinBridge connects four things that are often separated:

- **Awareness:** Understand where money goes.
- **Intervention:** Pause and reconsider before an impulsive purchase.
- **Habit formation:** Turn small amounts into visible savings progress.
- **Control:** Make debt obligations and repayment options easier to understand.

The differentiator is not simply an AI chatbot. It is the combination of behavioral workflows and explainable financial calculations.

## 6. Product modules

### 6.1 Dashboard
**Purpose:** Give users a clear snapshot of their current financial situation.

MVP capabilities:
- Income, expenses, and available balance for a selected period.
- Spending by category.
- Recent transactions.
- Savings goal progress.
- Debt summary and upcoming due dates.
- Financial Behavior Score and its breakdown.

### 6.2 Smart Pause — signature feature
**Purpose:** Encourage users to reconsider purchases that may conflict with their budgets or goals.

Proposed flow:
1. User enters a planned purchase amount and category.
2. FinBridge checks the amount against the user's available budget and category “red line”.
3. If a configured rule is triggered, the app explains why the purchase may be risky.
4. The user can start a 15-minute cooling-off period.
5. The app shows the purchase's estimated impact on the budget and savings goal.
6. The user chooses to postpone, proceed, or cancel.
7. The decision may contribute to later behavior insights.

**Hackathon limitation:** Smart Pause is a decision-support and reminder mechanism. It does not intercept, reject, or block a real card or bank payment.

### 6.3 Invisible Savings — simulated round-up
**Purpose:** Make saving feel incremental and achievable.

Proposed flow:
1. User creates a savings goal.
2. Eligible recorded transactions are rounded up to a configured step.
3. The difference is displayed as a potential savings contribution.
4. Contributions accumulate in an in-app simulated savings balance.
5. The user sees goal progress and an estimated completion date.

**Hackathon limitation:** Round-ups are simulated in the app. No real money is transferred or stored.

### 6.4 Debt Coach
**Purpose:** Make multiple obligations easier to understand and plan.

User-entered debt fields:
- Debt name/type.
- Current balance or principal.
- Interest rate, if known.
- Minimum payment, if applicable.
- Due date.
- Optional notes.

Strategies:
- **Snowball:** Prioritize the smallest balance to create visible progress.
- **Avalanche:** Prioritize the highest interest rate to reduce estimated interest cost.

The backend calculates the plan. AI may explain the comparison in plain language, but must not invent rates, balances, or guaranteed payoff dates.

### 6.5 Financial Behavior Score
**Purpose:** Show how the user's financial habits are developing over time.

Proposed dimensions:
- Spending discipline.
- Saving consistency.
- Debt payment discipline.
- Financial goal progress.

Requirements:
- The formula must be documented and understandable.
- Each dimension must show why its value changed.
- The app must show insufficient data when there is not enough history.
- The score must not be represented as a credit score, psychological diagnosis, or judgment of a person's worth.
- Comparisons over time must use comparable periods and available data.

The exact formula is an open product decision and must be finalized before implementation.

### 6.6 AI Financial Assistant
**Purpose:** Explain verified financial data and help users explore decisions.

Example questions:
- “How much did I save this month?”
- “What happens to my budget if I make this purchase?”
- “Which debt should I prioritize?”
- “How can I reach my savings target?”

**AI safety and correctness rules:**
- Backend services perform all arithmetic.
- AI receives structured, minimal context and explains returned results.
- AI must distinguish facts, assumptions, and estimates.
- AI must not fabricate transactions, balances, interest rates, or bank activity.
- AI output is guidance, not regulated financial advice or a guarantee.
- If the AI service fails, core product features remain usable.

## 7. Hackathon MVP scope

### Must have
1. Dashboard with seeded sample data.
2. Transaction list and basic transaction entry or controlled demo data.
3. Smart Pause purchase evaluation and 15-minute prompt.
4. Savings goal with simulated round-up.
5. Debt Coach with Snowball/Avalanche comparison.
6. Financial Behavior Score with a transparent breakdown.
7. Responsive web interface.

### Should have
- AI-generated explanations based on backend-calculated results.
- Category spending limits.
- Demo onboarding and a clear sample-data indicator.
- A small number of polished charts.

### Could have
- Spending personality labels.
- Financial challenges and streaks.
- Student mode.
- Financial education.
- Advanced what-if simulator.

### Explicitly out of scope for hackathon MVP
- Direct bank account access.
- Real payment interception or blocking.
- Real-money round-up transfers.
- Lending, credit scoring, or investment execution.
- Claims of guaranteed savings or debt elimination.
- Complex multi-user family finance workflows unless required by the event.

## 8. Demo narrative

The demo should tell one coherent story rather than presenting disconnected screens.

1. **Start with the problem:** A user has monthly income, daily expenses, a savings goal, and multiple obligations.
2. **Dashboard:** Show the financial picture in UZS.
3. **Smart Pause:** The user enters an unplanned purchase. FinBridge identifies a budget conflict, explains the impact, and offers a 15-minute pause.
4. **Invisible Savings:** The user sees how small round-ups could contribute to a goal.
5. **Debt Coach:** The user compares Snowball and Avalanche plans for their entered debts.
6. **Behavior Score:** The user sees how decisions and habits are reflected in a transparent score.
7. **Close with impact:** FinBridge helps turn awareness into better financial habits.

## 9. Technical architecture

### Proposed stack

| Layer | Proposed technology | Responsibility |
|---|---|---|
| Web frontend | React + TypeScript + Vite | Responsive user interface |
| UI styling | Tailwind CSS or a consistent component system | Design system and layout |
| Backend | Python + FastAPI | API and business logic |
| Database | PostgreSQL | Persistent application data |
| ORM/migrations | SQLAlchemy + Alembic | Data access and schema changes |
| Charts | Recharts or equivalent | Spending and progress visualization |
| AI | OpenAI API via backend | Explanations and contextual guidance |
| Testing | Pytest + frontend test tooling | Business and UI verification |
| Deployment | Docker; hosting selected by team | Reproducible demo deployment |

This is a proposed stack, not a claim that the repository already uses it. For a short hackathon, avoid premature microservices. A modular monolith is sufficient.

### High-level flow

```text
React Web Client
      |
      | HTTPS / JSON
      v
FastAPI Application
      |
      +---- Financial Calculation Services
      |       +---- Budget rules
      |       +---- Round-up calculation
      |       +---- Debt repayment plans
      |       +---- Behavior score
      |
      +---- AI Orchestration
      |       +---- Minimal structured context
      |       +---- Validated model response
      |       +---- Fallback response
      |
      v
PostgreSQL
```

### Architectural rules
- Keep financial calculations in deterministic backend services.
- Keep AI orchestration separate from core calculation logic.
- Validate all inputs at API boundaries.
- Use decimal-safe numeric types for money.
- Keep provider secrets on the server.
- Keep demo data separate from real user data.
- Start as one deployable backend unless real constraints justify splitting it.

## 10. Initial data model

Proposed entities:

| Entity | Key fields / purpose |
|---|---|
| User / DemoProfile | User identity or controlled demo profile |
| Transaction | Amount, type, category, date, note |
| Category | Name, icon/color, category type |
| BudgetLimit | Category, period, limit amount |
| SavingsGoal | Name, target amount, current simulated amount, target date |
| SavingsContribution | Transaction reference, round-up amount, date |
| Debt | Name, balance, rate, minimum payment, due date |
| PurchaseDecision | Proposed amount, category, rule result, user decision |
| ScoreSnapshot | Period, total score, dimension scores, calculation version |

### Money representation
Use `NUMERIC/DECIMAL` in the database and Python `Decimal` in business logic. Do not use binary floating-point for financial amounts.

### Data ownership
If user accounts are implemented, every financial record must be scoped to its owner. If the hackathon uses a single demo profile, label it clearly and do not imply production-grade multi-user isolation.

## 11. API surface (initial proposal)

Example API groups under `/api/v1`:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/dashboard/summary` | Dashboard totals and summaries |
| GET | `/transactions` | List transactions |
| POST | `/transactions` | Create transaction |
| GET | `/budgets` | List spending limits |
| POST | `/budgets` | Create/update a spending limit |
| POST | `/smart-pause/evaluate` | Evaluate planned purchase |
| POST | `/smart-pause/decisions` | Save user's decision |
| GET | `/savings/goals` | List savings goals |
| POST | `/savings/goals` | Create savings goal |
| GET | `/debts` | List debts |
| POST | `/debts` | Add debt |
| POST | `/debts/plan` | Calculate repayment strategy |
| GET | `/behavior-score/current` | Get score and breakdown |
| POST | `/assistant/explain` | Explain verified financial results |

Endpoints are illustrative and should be aligned with the implemented frontend and data model.

## 12. Financial calculation principles

- Use exact decimal arithmetic for all money.
- Store currency explicitly; MVP defaults to UZS.
- Define rounding rules and apply them consistently.
- Make date ranges and time zones explicit.
- Handle missing interest rates without silently assuming a rate.
- Show assumptions alongside debt payoff estimates.
- Do not double-count round-up contributions.
- Keep the Financial Behavior Score formula versioned so historical scores remain interpretable.
- Add unit tests for boundaries, zero values, negative inputs, and missing data.

## 13. Privacy, security, and trust

- Collect only data needed for the feature.
- Explain when data is sent to an AI provider.
- Never put AI API keys in browser code.
- Avoid writing sensitive financial details to logs.
- Validate and authorize access to every user-owned resource.
- Use HTTPS in deployed environments.
- Provide clear sample/demo-data labeling.
- Do not claim bank-grade security without an audit.
- Make it clear that the MVP does not access bank accounts or move money.
- Plan data export and deletion before production launch.

## 14. Success criteria

### Product/demo success
- A user can understand their financial snapshot from the Dashboard.
- Smart Pause completes a planned-purchase evaluation and records a decision.
- Savings round-up produces a correct simulated contribution.
- Debt Coach compares two repayment strategies using the same input assumptions.
- Financial Behavior Score displays a transparent breakdown or an insufficient-data state.
- The full demo can be completed without relying on a live bank integration.

### Engineering success
- Core money calculations have automated tests.
- Backend and frontend run from documented setup instructions.
- AI failure does not break core financial workflows.
- No secrets are committed to the repository.
- The demo is reproducible on the presentation machine.

## 15. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Scope becomes too large | Freeze the five-screen MVP and defer extras |
| AI returns inaccurate numbers | Calculate in backend; use AI only for explanation |
| Live integrations are unavailable | Use seeded/manual data and disclose simulation |
| Demo depends on internet/provider | Add deterministic fallback and backup recording |
| Score feels arbitrary | Publish formula, dimensions, and data sufficiency rules |
| Financial estimates are misunderstood | Show assumptions and mark estimates clearly |
| Time is lost on infrastructure | Use a modular monolith and minimal deployment setup |

## 16. Open decisions

These decisions must be confirmed by the team; do not silently assume answers.

- [ ] Is **FinBridge** the final product name, with **SMARTMIND** retained as the concept or feature identity?
- [ ] Which exact hackathon date, deadline, and judging criteria apply?
- [ ] Is authentication required, or is a controlled demo profile enough?
- [ ] Which frontend styling/component approach will be used?
- [ ] Will PostgreSQL be hosted, or will the MVP use a simpler local/demo database?
- [ ] Which AI provider/model and budget limits are available?
- [ ] Which languages must be supported at judging time?
- [ ] What exact formula and weights define Financial Behavior Score?
- [ ] What sample user story and demo dataset will be used?
- [ ] Who owns frontend, backend, AI, design, and presentation?

## 17. Decision log

| Date | Decision | Status | Notes |
|---|---|---|---|
| 2026-11-05 | Hackathon-focused scope | Selected by user | Optimize for a convincing, working MVP |
| 2026-11-05 | Web platform | Selected by user | Responsive web application |
| 2026-11-05 | Behavioral-finance concept | Grounded in project chat export | Smart Pause, Invisible Savings, Debt Coach, Behavior Score |
| 2026-11-05 | Proposed React + FastAPI + PostgreSQL stack | Proposed | Confirm against team skills and time |

## 18. Change log

- **2026-11-05:** Initial project definition created from the FinBridge chat export and the selected hackathon/web direction.

---

## Working agreement

`ROADMAP.md` tracks tasks and verification. `PROJECT.md` records what the product is, how it should behave, and why technical decisions were made.

When a decision changes:
1. Update this document.
2. Add an entry to the decision log.
3. Update affected roadmap tasks.
4. Keep completed work checked only after it has been verified.
