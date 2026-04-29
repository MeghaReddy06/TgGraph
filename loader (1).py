import json
import pyTigerGraph as tg

# ─────────────────────────────────────────────
# 1. CONNECT TO TIGERGRAPH
# ─────────────────────────────────────────────
conn = tg.TigerGraphConnection(
    host="https://tg-ea6b3c7b-08d9-41ce-817a-5fce8686281e.tg-2635877100.i.tgcloud.io",
    graphname="CareerGraph",
    username="tigergraph",
    password="your_password"                   # ← replace with your password
)
conn.apiToken = conn.getToken(conn.createSecret())
print("✅ Connected to TigerGraph")

# ─────────────────────────────────────────────
# 2. LOAD DATA FROM JSON FILE
# ─────────────────────────────────────────────
with open("careers.json", "r") as f:           # ← fixed path (was "data/careers.json")
    data = json.load(f)

roles         = data["roles"]
skills        = data["skills"]
companies     = data["companies"]
edges         = data["edges"]

# ─────────────────────────────────────────────
# 3. LOAD VERTICES
# ─────────────────────────────────────────────

# --- Roles ---
print("\n📌 Loading Roles...")
for role in roles:
    conn.upsertVertex("Role", role["id"], {
        "title": role["title"],
        "level": role["level"]
    })
print(f"   ✅ Loaded {len(roles)} roles")

# --- Skills ---
print("\n📌 Loading Skills...")
for skill in skills:
    conn.upsertVertex("Skill", skill["id"], {
        "name":     skill["name"],
        "category": skill["category"]
    })
print(f"   ✅ Loaded {len(skills)} skills")

# --- Companies ---
print("\n📌 Loading Companies...")
for company in companies:
    conn.upsertVertex("Company", company["id"], {
        "name":     company["name"],
        "industry": company["industry"]
    })
print(f"   ✅ Loaded {len(companies)} companies")

# ─────────────────────────────────────────────
# 4. LOAD EDGES
# ─────────────────────────────────────────────
print("\n📌 Loading Edges...")

requires_count = 0
offered_count  = 0
leads_count    = 0

for edge in edges:
    edge_type = edge["type"]
    from_id   = edge["from"]
    to_id     = edge["to"]

    if edge_type == "REQUIRES_SKILL":
        conn.upsertEdge("Role", from_id, "REQUIRES_SKILL", "Skill", to_id)
        requires_count += 1

    elif edge_type == "OFFERED_BY":
        conn.upsertEdge("Role", from_id, "OFFERED_BY", "Company", to_id)
        offered_count += 1

    elif edge_type == "LEADS_TO":
        conn.upsertEdge("Role", from_id, "LEADS_TO", "Role", to_id)
        leads_count += 1

print(f"   ✅ REQUIRES_SKILL edges : {requires_count}")
print(f"   ✅ OFFERED_BY edges     : {offered_count}")
print(f"   ✅ LEADS_TO edges       : {leads_count}")

# ─────────────────────────────────────────────
# 5. VERIFY — quick counts
# ─────────────────────────────────────────────
print("\n📊 Verification — vertex counts in TigerGraph:")
print("   Roles    :", conn.getVertexCount("Role"))
print("   Skills   :", conn.getVertexCount("Skill"))
print("   Companies:", conn.getVertexCount("Company"))

print("\n🎉 All data loaded into CareerGraph successfully!")
