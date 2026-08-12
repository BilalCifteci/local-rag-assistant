# Local RAG Assistant

Foundry Local kullanarak tamamen offline calisan, RAG (Retrieval-Augmented
Generation) mimarisine dayali bir dokuman soru-cevap asistani. Tum embedding
uretimi ve dil modeli cikarimi kullanicinin kendi cihazinda gerceklesir;
hicbir asamada internete veri gonderilmez.

## Mimari

```
Kullanici sorusu
      |
      v
[main.py] CLI  veya  [web_app.py] Streamlit
      |
      v
[qa.answer_query]
      |     \
      v      \-- retrieval benzerligi dusukse -> sabit "bilmiyorum" cevabi
[retrieval.get_top_chunks]
      |  sorguyu embed et (Foundry Local: qwen3-embedding-0.6b)
      |  SQLite'daki tum chunk embedding'leriyle kosinus benzerligi hesapla
      |  en alakali k parcayi don
      v
[documents.db] (SQLite: source, chunk_index, content, embedding)
      ^
      |  onceden doldurulur
[ingest.py]  docs/*.md -> paragraf chunk'lari -> embedding -> SQLite

En alakali parcalar bulunduktan sonra qa.py bunlari sistem promptuna
"baglam" olarak ekler ve Foundry Local sohbet modelinden (phi-3.5-mini)
cevap alir.
```

## Kurulum

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Dosyalar

| Dosya | Hafta | Aciklama |
|---|---|---|
| `app.py` | 1 | Foundry Local kurulum testi (Hello Model) |
| `embed_test.py` | 2 | Embedding uretimi ve cosine similarity testi |
| `docs/*.md` | 3 | Bilgi tabani: RAG, Foundry Local, embedding, SQLite, prompt muhendisligi |
| `ingest.py` | 3 | Dokumanlari chunk'lara bolup embedding'leriyle SQLite'a kaydeder |
| `retrieval.py` | 3 | `get_top_chunks(query, k)` - en alakali dokuman parcalarini bulur |
| `qa.py` | 4-5 | `answer_query(question)` - retrieval + yerel LLM ile cevap uretir, benzerlik esigiyle "bilmiyorum" guardrail'i icerir |
| `main.py` | 4 | Komut satiri (CLI) arayuzu |
| `test_qa.py` | 5 | Cevaplanabilir/cevaplanamaz sorularla fonksiyonel test kosucusu |
| `TEST_RESULTS.md` | 5 | Gercek test calistirma ciktilari |
| `web_app.py` | 6 (stretch) | Streamlit tabanli web sohbet arayuzu |
| `requirements.txt` | 6 | Bagimliliklarin tekrarlanabilir kurulumu icin |

## Calistirma

```
# 1) Bilgi tabanini SQLite'a yukle (bir kere, veya docs/ degistiginde tekrar)
python ingest.py

# 2) Asistanla konus
python main.py

# 3) Testleri calistir
python test_qa.py

# 4) Web arayuzunu baslat (alternatif, daha etkileyici demo)
streamlit run web_app.py
```

Erken kurulum/embedding testleri icin (Hafta 1-2):

```
python app.py
python embed_test.py
```

## Kullanilan Modeller

- **Embedding:** `qwen3-embedding-0.6b`
- **Sohbet (cevap uretimi):** `phi-3.5-mini`

Kucuk modeller tercih edildi cunku proje hedefi hizli, tamamen yerel
cevaplar almak; buyuk modeller daha iyi cevap kalitesi verebilir ama
indirme boyutu ve cikarim suresi artar.

## Bilinen Sinirlamalar (Hafta 5 test bulgulari)

`TEST_RESULTS.md` dosyasindaki gercek test ciktilarina gore:

- Konu ici sorularda en yuksek retrieval benzerligi ~0.62-0.69, konu disi
  sorularda ~0.31-0.37 araliginda cikiyor - aralarinda net bir bosluk var.
- Ancak `phi-3.5-mini`, salt sistem promptundaki "bilmiyorum de" talimatina
  guvenilir sekilde uymuyordu; konu disi sorularda bile baglamdaki
  dokumanlardan alakasiz bilgi uretip cevap vermeye calisiyordu.
- Cozum olarak `qa.py` icine bir retrieval benzerlik esigi (`0.45`) eklendi:
  esigin altinda kalan sorular LLM'e hic gonderilmeden sabit bir "Bu bilgi
  elimdeki dokumanlarda yok." cevabiyla karsilaniyor. Bu, kucuk modellerde
  prompt talimatlarina guvenmek yerine basit bir sayisal kontrolun daha
  guvenilir oldugunu gosteren somut bir ders.
- Cevaplar dogru bilgiyi iceriyor olsa da bazen dilbilgisi/akicilik acisindan
  pürüzlü cikiyor (kucuk model sinirlamasi); daha buyuk bir sohbet modeliyle
  (orn. `phi-4-mini`, `qwen3-4b`) kalite artirilabilir ama cikarim suresi
  uzar.

## Sonraki Adimlar

- Kaynak adlarinin cevap metninde daha tutarli/yapisal gosterilmesi
  (orn. serbest metin yerine ayri bir "Kaynaklar:" alani).
- Chunk boyutu ve k (kac parca getirilecegi) degerleriyle deney yapip
  retrieval kalitesini artirmak.
- Kendi gercek dokumanlarini (`docs/` altina) ekleyip `python ingest.py`
  ile yeniden indexlemek.
