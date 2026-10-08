# Campus Customs Harness

## Problem 2 — Database tables

The requested database file, `data/campus_customs.db`, is not currently present in the assignment workspace. I searched the workspace for `campus_customs.db`, other SQLite database files, and schema definitions, but none were available. Therefore, the field lists below must be completed after the database is supplied; no columns are being guessed.

### `catalogue`

Fields: **pending database inspection**

Field notes: Each field will be documented here with its role in product search, product cards, product details, or chatbot responses.

### `inventory`

Fields: **pending database inspection**

Field notes: Each field will be documented here with its role in stock availability, quantity checks, or purchase guidance from the chatbot.

### `users`

Fields: **pending database inspection**

Field notes: Each field will be documented here with its role in login, customer identification, account safety, or chat-history ownership.

### Inspection command to run when the database is available

```sql
SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name;
PRAGMA table_info(catalogue);
PRAGMA table_info(inventory);
PRAGMA table_info(users);
```

## Problem 4 — Authentication

### User data

The account flow stores `first_name`, `last_name`, `email`, and `password_hash` in `users`. The database row also has an `id` primary key. The application returns only the id, names, and email to the client after login; it never returns the password or password hash.

### Password protection

Passwords are protected with PBKDF2-HMAC-SHA256 using a random 16-byte salt and 310,000 iterations. The stored value contains the algorithm, iteration count, salt, and derived digest separated by `$`. Login recomputes the digest with the stored salt and uses constant-time comparison. Plaintext passwords are not stored.

### API behavior

- `POST /api/auth/signup` validates the required fields, rejects duplicate email addresses, hashes the password, and inserts the new user.
- `POST /api/auth/login` looks up the email and verifies the password hash, returning a safe user profile only when the credentials match.

## Problem 5 — Chat agent

The React floating chat widget sends the shopper's message as JSON to `POST /api/chat` and renders the returned `message`. FastAPI validates the request with `ChatRequest` and returns a structured `ChatReply`, including optional `ProductCard` records for future product-card rendering. If the API is unavailable, the widget shows a short connection message and links the shopper to Products.

The agent is loaded in `backend/agent.py` from `prompts/prompt.md`. It uses the repository `.env` `PORTKEY_API_KEY` through Portkey, the `gpt-5.6-luna` model by default, and returns the typed `ChatReply` model. `backend/tools.py` currently provides `find_products`, a small catalogue search stub that will be replaced or extended with database tools later. Run it from `backend/` with `uvicorn main:app --reload --port 8000`.

## Problems 6–8 — Database tools, dynamic search, and history

The database-backed tools are:

- `search_products(query)`: searches `catalogue.name`, `garment_type`, `description`, `colors`, and `search_tags`; it returns `ProductCard` fields (`id`, `name`, `price`, `description`, `image`) so the website can render trustworthy matches.
- `lookup_price(product_id)`: reads the catalogue `price` field for an exact product or name match; the agent must use this instead of estimating prices.
- `lookup_stock(product_id, size)`: joins `inventory` to `catalogue` and returns `StockResult(product_name, requested_size, sizes)`. A requested size with quantity zero or no matching row is reported as unavailable; quantities are never invented.

The tools read `data/campus_customs.db` and can read the supplied archive during local setup if the database has not yet been extracted. Search results are returned as structured `ProductCard` values in `ChatReply.products`. The front end renders each match with its name, price, and short description; product IDs and image paths preserve the existing single-item route contract.

For logged-in shoppers, the request includes the safe user object (`id`, name, email) and the current `location.pathname` as `page_context`. `AgentDeps` carries both into the agent run, so a question such as “do you have this in pink?” has the current product page context. User and assistant messages are stored in `chat_messages` with `user_id`, `role`, `content`, optional `products_json`, and `created_at`; guests are not persisted. The history endpoint is `GET /api/chat/history/{user_id}`.

## Problems 9–12 — Finish harness

### Models and why they exist

- `ProductCard` carries the stable product id, name, price, description, image path, and optional stock for rendering and detail-page navigation.
- `StockResult` separates the product name, requested size, and per-size quantities so out-of-stock responses are explicit.
- `ChatRequest` carries the message, optional safe user context, page context, and bounded history input.
- `ChatReply` has a short message plus structured product matches, preventing the UI from scraping product data out of prose.
- `AgentDeps` carries customer identity and current page context into tools and the model run.

### Tools and abilities

The agent can search the catalogue, look up an exact price, and query size-level inventory. The FastAPI app also supports product reads, authentication, chat, and chat-history reads. Search is capped at 12 cards and chat input at 1,000 characters.

### Safety and audit

The system prompt forbids invented prices, quantities, policies, and secret handling. It prevents exposure of passwords, API keys, payment details, and other users’ records. `output/audit_trail.json` is append-only: each chat start and structured stop stores UTC time, event, short arguments/result, and stop reason without private chain-of-thought.

### Specs and run instructions

The default model is `gpt-5.6-luna` through Portkey using `PORTKEY_API_KEY`. The backend runs from `backend/` with `uvicorn main:app --reload --port 8000`; the Vite frontend runs with `npm install` then `npm run dev`. Local `.env`, the SQLite database, and product images are ignored by Git.

