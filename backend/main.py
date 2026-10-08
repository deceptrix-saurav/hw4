"""Small product API; the SQLite connection can be wired in as the database arrives."""
from pathlib import Path
import sqlite3
import json
from datetime import datetime, timezone
import hashlib
import hmac
import secrets
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
try:
    from .models import ChatRequest, ChatReply
    from .agent import chat, AgentDeps
    from .tools import save_message, load_history
except ImportError:
    from models import ChatRequest, ChatReply
    from agent import chat, AgentDeps
    from tools import save_message, load_history

app = FastAPI(title="Campus Customs API")
ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "campus_customs.db"
if (ROOT / "data").exists():
    app.mount("/data", StaticFiles(directory=ROOT / "data"), name="data")

FALLBACK = [
    {"id": 1, "name": "Big Yale Tri-Blend T-Shirt", "price": 32, "description": "A soft everyday tee with unmistakable Yale spirit.", "image": "/data/products/big-yale-tri-blend-t-shirt.jpg", "sizes": "S · M · L · XL", "stock": 18},
    {"id": 2, "name": "Basic Hoodie — Big Yale", "price": 68, "description": "A cozy heavyweight layer for cool New Haven days.", "image": "/data/products/basic-hoodie-big-yale.jpg", "sizes": "S · M · L · XL · XXL", "stock": 9},
]

def audit(event: str, tool_name: str | None = None, args: dict | None = None, result: str | None = None, stop_reason: str | None = None):
    path = ROOT / "output" / "audit_trail.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    try: entries = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    except json.JSONDecodeError: entries = []
    entries.append({"timestamp": datetime.now(timezone.utc).isoformat(), "event": event, "tool_name": tool_name, "args": args or {}, "short_result": (result or "")[:300], "stop_reason": stop_reason})
    path.write_text(json.dumps(entries, indent=2), encoding="utf-8")

class Signup(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

def password_hash(password: str, salt: bytes | None = None) -> str:
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 310_000)
    return f"pbkdf2_sha256$310000${salt.hex()}${digest.hex()}"

def password_matches(password: str, stored: str) -> bool:
    try:
        algorithm, rounds, salt_hex, digest_hex = stored.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), int(rounds)).hex()
        return hmac.compare_digest(actual, digest_hex)
    except (ValueError, TypeError):
        return False

def ensure_users(con: sqlite3.Connection):
    con.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL,
        last_name TEXT NOT NULL, email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    )""")
    con.commit()

@app.post("/api/auth/signup")
def signup(payload: Signup):
    with sqlite3.connect(DB) as con:
        ensure_users(con)
        try:
            con.execute("INSERT INTO users (first_name,last_name,email,password_hash) VALUES (?,?,?,?)", (payload.first_name.strip(), payload.last_name.strip(), payload.email.lower(), password_hash(payload.password)))
            con.commit()
        except sqlite3.IntegrityError:
            return {"ok": False, "message": "An account with that email already exists."}
    return {"ok": True, "message": "Account created."}

@app.post("/api/auth/login")
def login(payload: Login):
    with sqlite3.connect(DB) as con:
        ensure_users(con)
        row = con.execute("SELECT id, first_name, last_name, email, password_hash FROM users WHERE lower(email)=lower(?)", (payload.email,)).fetchone()
    if not row or not password_matches(payload.password, row[4]):
        return {"ok": False, "message": "Email or password is incorrect."}
    return {"ok": True, "user": {"id": row[0], "first_name": row[1], "last_name": row[2], "email": row[3]}}

@app.get("/api/products")
def products():
    if not DB.exists():
        return FALLBACK
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        try:
            rows = con.execute("SELECT * FROM catalogue LIMIT 100").fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error:
            return FALLBACK

@app.post("/api/chat", response_model=ChatReply)
async def chat_route(payload: ChatRequest):
    audit("chat_start", "chat", {"message_length": len(payload.message), "has_user": bool(payload.user)})
    deps = AgentDeps(payload.user, payload.page_context)
    if payload.user and payload.user.get("id"):
        save_message(payload.user["id"], "user", payload.message)
    result = await chat(payload.message, deps)
    if payload.user and payload.user.get("id"):
        save_message(payload.user["id"], "assistant", result.message, result.products)
    audit("chat_stop", "chat", result=result.message, stop_reason="structured_output")
    return result

@app.get("/api/chat/history/{user_id}")
def history(user_id: int):
    return load_history(user_id)
