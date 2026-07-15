import math
from foundry_local_sdk import Configuration, FoundryLocalManager

# 1. SDK'yi baslat
FoundryLocalManager.initialize(Configuration(app_name="local-rag-assistant"))
manager = FoundryLocalManager.instance

# 2. Embedding modelini sec ve indir
model = manager.catalog.get_model("qwen3-embedding-0.6b")
print("Embedding modeli indiriliyor...")
model.download(lambda p: print(f"\rIndiriliyor: %{p:.0f}", end="", flush=True))
print()
model.load()
print("Model yuklendi.\n")

embedding_client = model.get_embedding_client()


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)


# 3. Test cumleleri: 2 tanesi benzer konuda, 1 tanesi alakasiz
sentences = [
    "Kedi çok tatlı ve uyuyor.",
    "Köpek bahçede havladı.",
    "Borsa bugün sert düştü.",
]

print("Embedding'ler üretiliyor...")
response = embedding_client.generate_embeddings(sentences)
vectors = [item.embedding for item in response.data]
print(f"Her vektörün boyutu: {len(vectors[0])}\n")

# 4. Benzerlikleri karsilastir
pairs = [(0, 1, "kedi <-> köpek"), (0, 2, "kedi <-> borsa"), (1, 2, "köpek <-> borsa")]
for i, j, label in pairs:
    sim = cosine_similarity(vectors[i], vectors[j])
    print(f"{label}: benzerlik = {sim:.4f}")

model.unload()
