from foundry_local_sdk import Configuration, FoundryLocalManager

# 1. SDK'yı başlat
FoundryLocalManager.initialize(Configuration(app_name="local-rag-assistant"))
manager = FoundryLocalManager.instance

# 2. Küçük ve hızlı bir modeli seç (ilk test için en hafif model)
model = manager.catalog.get_model("qwen2.5-0.5b")

# 3. Model cihazda yoksa indir
print("Model indiriliyor (ilk çalıştırmada biraz sürebilir)...")
model.download(lambda p: print(f"\rİndiriliyor: %{p:.0f}", end="", flush=True))
print()

# 4. Modeli belleğe yükle
model.load()
print("Model yüklendi, yanıt bekleniyor...\n")

# 5. Basit bir soru sor ve yanıtı akış halinde yazdır
client = model.get_chat_client()
for chunk in client.complete_streaming_chat(
    [{"role": "user", "content": "Merhaba! Sen kimsin, kısaca tanıt."}]
):
    if chunk.choices:  # son chunk boş gelebilir, kontrol şart
        print(chunk.choices[0].delta.content or "", end="", flush=True)

print("\n\nTest tamamlandı ✅")

# 6. Modeli bellekten kaldır
model.unload()
