from pathlib import Path
import json, sqlite3, zipfile
try:
    from .models import ProductCard, StockResult
except ImportError:
    from models import ProductCard, StockResult

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "campus_customs.db"
ARCHIVE = ROOT / "data (1).zip"

def connect():
    if DB.exists(): con = sqlite3.connect(DB)
    else:
        con = sqlite3.connect(":memory:")
        with zipfile.ZipFile(ARCHIVE) as archive: con.deserialize(archive.read("data/campus_customs.db"))
    con.row_factory = sqlite3.Row
    return con

def product(row):
    return ProductCard(id=row["product_id"], name=row["name"], price=row["price"], description=row["description"], image="/" + row["image_file_path"].replace("\\", "/"))

def search_products(query: str) -> list[ProductCard]:
    terms = [f"%{word}%" for word in query.lower().split() if len(word) > 2]
    with connect() as con:
        if terms:
            where = " OR ".join("lower(name || ' ' || garment_type || ' ' || description || ' ' || colors || ' ' || search_tags) LIKE ?" for _ in terms)
            rows = con.execute(f"SELECT * FROM catalogue WHERE {where} ORDER BY name LIMIT 12", terms).fetchall()
        else: rows = con.execute("SELECT * FROM catalogue ORDER BY name LIMIT 12").fetchall()
    return [product(row) for row in rows]

def lookup_price(product_id: str):
    with connect() as con: row = con.execute("SELECT * FROM catalogue WHERE product_id=? OR lower(name) LIKE lower(?) LIMIT 1", (product_id, f"%{product_id}%")).fetchone()
    return product(row) if row else None

def lookup_stock(product_id: str, size: str | None = None) -> StockResult:
    with connect() as con: rows = con.execute("SELECT c.name,i.size,i.quantity FROM inventory i JOIN catalogue c ON c.product_id=i.product_id WHERE i.product_id=? OR lower(c.name) LIKE lower(?)", (product_id, f"%{product_id}%")).fetchall()
    if size: rows = [row for row in rows if row["size"].lower() == size.lower()]
    return StockResult(product_name=rows[0]["name"] if rows else product_id, requested_size=size, sizes={row["size"]: row["quantity"] for row in rows})

def save_message(user_id: int, role: str, content: str, products=None):
    with connect() as con:
        con.execute("CREATE TABLE IF NOT EXISTS chat_messages (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,role TEXT NOT NULL,content TEXT NOT NULL,products_json TEXT,created_at TEXT NOT NULL DEFAULT (datetime('now')))")
        con.execute("INSERT INTO chat_messages(user_id,role,content,products_json) VALUES (?,?,?,?)", (user_id, role, content, json.dumps([p.model_dump() for p in products or []])))
        con.commit()

def load_history(user_id: int):
    with connect() as con:
        try: rows = con.execute("SELECT role,content FROM chat_messages WHERE user_id=? ORDER BY id", (user_id,)).fetchall()
        except sqlite3.Error: return []
    return [{"role": row["role"], "content": row["content"]} for row in rows]
