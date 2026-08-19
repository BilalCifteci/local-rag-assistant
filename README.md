# Local RAG Assistant — Üniversite Yönetmelik Asistanı

Foundry Local kullanarak tamamen offline calisan, RAG (Retrieval-Augmented
Generation) mimarisine dayali bir dokuman soru-cevap asistani. Tum embedding
uretimi ve dil modeli cikarimi kullanicinin kendi cihazinda gerceklesir;
hicbir asamada internete veri gonderilmez.

Bilgi tabani, Maltepe Universitesi Yazilim Muhendisligi bolumunun gercek
yonetmelik/yonerge metinlerinden olusuyor (ders kayit, mezuniyet sartlari,
staj, sinav/degerlendirme, devamsizlik kurallari). Amac, RAG'in "kaynaga
dayali, halusinasyon yapmadan cevap" avantajini somut ve dogrulanabilir bir
senaryoda gostermek: asistanin verdigi cevap, gercek yonetmelik metniyle
karsilastirilarak dogrulanabilir.

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
| `docs/*.md` | 3 | Bilgi tabani: Maltepe Universitesi ders kayit, mezuniyet, staj, sinav/degerlendirme, devamsizlik yonetmelik/yonerge metinleri |
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

- **Konu disi sorular guvenilir reddediliyor.** Konu ici sorularda en
  yuksek retrieval benzerligi ~0.44-0.69, konu disi sorularda ~0.27-0.31
  cikiyor. `phi-3.5-mini` salt sistem promptundaki "bilmiyorum de"
  talimatina tek basina guvenilir uymadigi icin, `qa.py` icine bir
  retrieval benzerlik esigi eklendi; esigin altindaki sorular LLM'e hic
  gonderilmeden sabit bir "Bu bilgi elimdeki dokumanlarda yok." cevabiyla
  karsilaniyor.
- **Esik degeri veri setine gore kalibre edilmeli.** Ilk denemede esik
  `0.45` idi ve gecerli bir soruyu ("bir donemde en fazla kac dersten
  cekilebilirim?", benzerlik 0.44) yanlislikla reddetti. Esik `0.35`'e
  dusurulduktan sonra bu soru dogru cevaplandi. Bu, esigin bilgi tabani
  degistiginde yeniden ayarlanmasi gerektigini gosteriyor - sabit bir
  sayi degil, veriye gore kalibre edilen bir parametre.
- **Onemli bulgu: model dogru kaynagi bulsa bile yanlis detay
  uretebiliyor.** "Devamsizlik sinirini asan ogrenciye hangi not verilir?"
  sorusunda retrieval dogru parcayi buldu (benzerlik 0.65, `devamsizlik.md`
  icindeki ilgili madde) ama model cevap olarak yanlislikla "(DD) notu"
  dedi; dogrusu yonetmelige gore "(DZ) notu"dur. Yani y�ksek retrieval
  benzerligi, cevabin dogru olacaginin garantisi degildir - kucuk model,
  doğru baglami gormesine ragmen belirli bir kodu/detayi yanlis
  aktarabilir. Bir yonetmelik botu gibi hassas dogruluk gerektiren bir
  kullanimda bu risklidir; oneri: kritik kod/rakam iceren cevaplar icin
  daha buyuk bir model kullanmak veya cevaptaki spesifik degerleri
  baglamdaki metinle otomatik dogrulayan bir ek kontrol eklemek.
- **Kaynak gosterimi bazen yanlis dokumana isaret ediyor.** Staj suresi
  sorusunda doğru cevap (30 is gunu) verildi ama kaynak olarak
  `mezuniyet_sartlari.md` gosterildi; oysa asil detay `staj.md`
  icindedir (mezuniyet_sartlari.md sadece stajin mezuniyet sarti oldugunu
  belirtiyor). Kaynak gosterimi su an modelin serbest metin cikisina
  dayaniyor, bu nedenle %100 guvenilir degil.
- Cevaplar dogru bilgiyi iceriyor olsa da bazen dilbilgisi/akicilik acisindan
  pürüzlü cikiyor (kucuk model sinirlamasi); daha buyuk bir sohbet modeliyle
  (orn. `phi-4-mini`, `qwen3-4b`) kalite artirilabilir ama cikarim suresi
  uzar.

## Sonraki Adimlar

- Kaynak adlarinin cevap metninde daha tutarli/yapisal gosterilmesi
  (orn. serbest metin yerine, en yuksek benzerlikli chunk'in source
  alaninin dogrudan kod ile gosterilmesi - modelin serbest metnine
  guvenmemek).
- Kritik rakam/kod iceren cevaplarda (not harfleri, gun sayilari, yuzdeler)
  dogrulugu artirmak icin daha buyuk bir model (`phi-4-mini`, `qwen3-4b`)
  ile karsilastirmali test yapmak.
- Chunk boyutu ve k (kac parca getirilecegi) degerleriyle deney yapip
  retrieval kalitesini artirmak.
- Diger yonetmelik/yonergeleri (cift anadal/yandal, yatay-dikey gecis,
  disiplin yonetmeligi) `docs/` altina ekleyip bilgi tabanini genisletmek.
