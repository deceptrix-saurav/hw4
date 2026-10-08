# AI Prompt Log — Homework 4: Campus Customs Shop + Chatbot

This file records the prompts I type to my AI coding assistant while completing Homework 4. I will update it as I work.

## Problem 1 — Vibe coder prompts

### Prompt

I need to complete Problem 1 of Homework 4 for MGT 409. The assignment requires an `AI_prompts.md` file that logs my own prompts, with a separate section for Problems 1–13. Each section needs the problem number and title, at least one prompt in my own words, and—when applicable—a follow-up prompt plus one sentence explaining what the first prompt was missing. Please help me set up the required log without inventing prompts that I have not typed.

### Follow-up prompt

No follow-up prompt was needed for this request.

The first prompt was missing the exact final wording of any future prompts because those prompts have not been written yet.

## Problem 2 — Database tables

Prompt(s) to add while completing this problem:

- Please inspect `data/campus_customs.db` and understand the fields in the `catalogue`, `inventory`, and `users` tables. Start `output/harness.md` with each table name, every field, and a short explanation of why each field matters to the Campus Customs shop or chatbot. Keep the notes ready to expand in later problems.

Follow-up prompt, if needed:

- The database file was not present in the workspace, so please do not guess the schema. Start the harness with an explicit note that the inspection is pending and include the SQLite commands that can be used once the database is supplied.

What the first prompt was missing:

The first prompt was missing the fact that the requested database file was unavailable, so the schema could not be documented accurately.

## Problem 3 — Vite React TypeScript site

Prompt(s) to add while completing this problem:

- Scaffold a React + Vite + TypeScript Campus Customs shop in `HW 4`. Add top navigation for Home, Products, About Us, Log in, and Create account. Build a product grid and clickable single-product pages, include a bottom-right chat stub, and add a small FastAPI backend in `backend/main.py` for products and images. Use the supplied catalogue image paths when available and keep the design black and pink.

Follow-up prompt, if needed:

- The SQLite database was packaged inside `data (1).zip` rather than already extracted. Keep the app runnable with fallback product records until the database and images can be extracted into the expected `data/` paths, and do not expose secrets.

What the first prompt was missing:

The first prompt did not account for the provided data archive not being extracted into the expected folder, so a fallback was needed for local development.

## Problem 4 — Login with hashed first name, last name, and email

Prompt(s) to add while completing this problem:

- Add a normal create-account and login flow to the Campus Customs app. Signup needs first name, last name, email, password, and password confirmation; login needs email and password. Store new accounts in SQLite and never store plaintext passwords. Connect the React forms to FastAPI endpoints and document the user fields and password protection in `output/harness.md`.

Follow-up prompt, if needed:

- Use a per-user random salt and PBKDF2-HMAC-SHA256 with a high iteration count for password hashes. Return only safe user profile fields after a successful login, never the password or hash.

What the first prompt was missing:

The first prompt did not specify a concrete password hashing format and verification method, so the follow-up selected a salted PBKDF2 representation that can be checked without revealing the password.

## Problem 5 — FastAPI agent

Prompt(s) to add while completing this problem:

- Build the Campus Customs chatbot as a PydanticAI agent behind FastAPI. Create `backend/prompts/prompt.md`, `agent.py`, `tools.py`, and `models.py`; add a typed `/api/chat` route in `main.py`; and connect the existing front-end chat widget. Use the Portkey key from `.env` and default to `gpt-5.6-luna`.

Follow-up prompt, if needed:

- Make the agent importable when Uvicorn is run from inside `backend/` with `uvicorn main:app --reload --port 8000`, while also allowing package-style imports. Add a no-key fallback so the app can start for UI work without exposing or printing secrets.

What the first prompt was missing:

The first prompt did not specify the Uvicorn working-directory import behavior or how the front end should behave when the API key is unavailable.

## Problem 6 — Lookup tools for stock and price

Prompt(s) to add while completing this problem:

- Use the real SQLite catalogue and inventory tables for product descriptions, prices, and size-level stock. Add typed PydanticAI tools that query the database and clearly report an unavailable size instead of guessing.

Follow-up prompt, if needed:

- The database is packaged in `data (1).zip`, so support the extracted `data/campus_customs.db` path and a safe local archive fallback while setup is incomplete. Add `ProductCard` and `StockResult` return models.

What the first prompt was missing:

The first prompt did not address the workspace’s unextracted database archive or define the structured fields needed by the front end.

## Problem 7 — Chat search that updates the page

Prompt(s) to add while completing this problem:

- Return structured product matches from the chat endpoint and render them as product cards in the chat widget, with each card linking to the existing `/products/:id` detail route.

Follow-up prompt, if needed:

- Keep the same `ProductCard` contract for catalogue and chat results so dynamically loaded cards retain image, name, price, description, and detail-page behavior.

What the first prompt was missing:

The first prompt did not explicitly preserve the single-item route for cards added by chat.

## Problem 8 — Chat history and page context

Prompt(s) to add while completing this problem:

- Persist logged-in users’ chat messages in `chat_messages`, reload history by user ID, and pass the safe customer identity plus current page path into `AgentDeps`. Keep guest conversations ephemeral.

Follow-up prompt, if needed:

- Store only role, message content, timestamp, user ID, and optional structured product results; do not store passwords or secrets, and let the agent use page context for product-specific questions.

What the first prompt was missing:

The first prompt did not spell out which history fields were safe to persist or how product-page context should reach the agent.

## Problem 7 — Chat with product cards and a detail page

Prompt(s) to add while completing this problem:

- 

Follow-up prompt, if needed:

- 

What the first prompt was missing:

## Problem 8 — Chat history

Prompt(s) to add while completing this problem:

- 

Follow-up prompt, if needed:

- 

What the first prompt was missing:

## Problem 9 — Usability notes

Prompt(s) to add while completing this problem:

- Choose and implement two front-end usability improvements and two agent/backend improvements for the Campus Customs app. Write `output/usability.md` as I build and make the improvements visible or active in the running system.

Follow-up prompt, if needed:

- Use responsive product layout and persistent product-card-to-detail navigation for the front end; use database-first bounded search results and request limits for the backend. Document the shopper or business benefit of each.

What the first prompt was missing:

The first prompt did not name concrete improvements or explain how each one would be evidenced.

## Problem 10 — Style the website

Prompt(s) to add while completing this problem:

- Give the Campus Customs storefront a memorable visual system with fonts, color hierarchy, motion, product presentation, and a polished chat feel, then summarize concrete choices in `output/design.md`.

Follow-up prompt, if needed:

- Keep the design accessible and responsive so the creative treatment supports browsing and purchase decisions rather than obscuring content.

What the first prompt was missing:

The first prompt did not explicitly include responsive and readable design constraints.

## Problem 11 — Site testing

Prompt(s) to add while completing this problem:

- Create `output/app_check.html` with three headed checks and relative screenshot links for database inventory, dynamic search cards, and one usability feature.

Follow-up prompt, if needed:

- Keep the HTML double-clickable and portable; place screenshots in `output/app_check_images/` and use short captions explaining what each proves.

What the first prompt was missing:

The first prompt did not specify the portable relative-path structure for the evidence page.

## Problem 12 — Audit trail, safety, finish harness

Prompt(s) to add while completing this problem:

- Add append-only JSON audit events for agent-loop activity, expand prompt safety rules, and finish `output/harness.md` with models, tools, limits, models, and run commands.

Follow-up prompt, if needed:

- Record only timestamps, event/tool names, short sanitized arguments and results, and stop reasons; never store secrets or private chain-of-thought.

What the first prompt was missing:

The first prompt did not define the privacy boundary for audit records.

## Problem 13 — Push to GitHub and submit a public URL

Prompt(s) to add while completing this problem:

- Prepare the project for a public GitHub repository with a safe `.gitignore`, `.env.example`, README run instructions, and no real environment file, database, or product images.

Follow-up prompt, if needed:

- Keep the local data pack documented as a setup prerequisite and do not create or push a repository until the owner supplies the public GitHub destination and confirms they want that external publication.

What the first prompt was missing:

The first prompt did not include the need to avoid publishing to an unspecified external repository.

## Problem 10 — Design document

Prompt(s) to add while completing this problem:

- 

Follow-up prompt, if needed:

- 

What the first prompt was missing:

## Problem 11 — App check page with screenshots

Prompt(s) to add while completing this problem:

- 

Follow-up prompt, if needed:

- 

What the first prompt was missing:

## Problem 12 — Audit

Prompt(s) to add while completing this problem:

- 

Follow-up prompt, if needed:

- 

What the first prompt was missing:

## Problem 13 — Submit a public GitHub URL on Canvas

Prompt(s) to add while completing this problem:

- 

Follow-up prompt, if needed:

- 

What the first prompt was missing:

