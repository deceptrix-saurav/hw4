# Campus Customs

Campus Customs is a Vite React TypeScript storefront with a FastAPI/PydanticAI concierge.

## Setup

Place the local data pack at `data/campus_customs.db` and `data/products/`. Copy `.env.example` to `.env` and add `PORTKEY_API_KEY` locally; never commit either file or the data pack.

Backend:

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Frontend:

```bash
npm install
npm run dev
```

The Vite app uses `/api` and `/data` paths; configure a local dev proxy to port 8000 when running the two servers separately.
