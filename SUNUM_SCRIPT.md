# 3 Dakikalık Video - Seslendirme Metni

Doğal, sohbet eder gibi bir tempoda okunduğunda ~3 dakika sürecek şekilde
yazıldı. Köşeli parantez içindeki notlar ekranda ne gösterileceğini belirtir,
sesli okunmaz.

---

**[0:00-0:15] AÇILIŞ**
*(Ekranda: proje klasörü veya README başlığı)*

> "Merhaba, ben Bilal. Bu proje, Maltepe Üniversitesi Yazılım Mühendisliği
> bölümünün ders kayıt, mezuniyet, staj ve sınav yönetmeliklerine göre soru
> cevaplayan, tamamen çevrimdışı çalışan bir yapay zeka asistanı. Microsoft
> Foundry Local kullanıyor, yani hiçbir veri internete çıkmıyor."

---

**[0:15-0:35] MİMARİ**
*(Ekranda: README'deki mimari diyagramı)*

> "Sistem şöyle çalışıyor: önce yönetmelik metinlerini küçük parçalara
> bölüp, her parçayı bir embedding modeliyle vektöre çeviriyoruz ve
> SQLite'a kaydediyoruz. Bir soru geldiğinde, o soru da vektöre çevrilip en
> alakalı parçalar bulunuyor ve yerel bir dil modeline bağlam olarak
> veriliyor. Yani model, cevabı uydurmuyor; gerçek yönetmelik metnine
> dayandırıyor."

---

**[0:35-2:05] CANLI DEMO**
*(Ekranda: web_app.py arayüzü, önceden ısıtılmış model)*

> "Şimdi canlı deneyelim."

*(Soru 1'i yaz/yapıştır: "Yazılım Mühendisliği bölümünde staj kaç iş günü
sürer?")*

> "Gördüğünüz gibi doğru cevabı -otuz iş günü- verdi, hem de hangi
> dokümandan aldığını kaynak olarak gösterdi."

*(Soru 2'yi yaz/yapıştır: konu dışı bir soru, örn. "Bugün hava durumu
nasıl?")*

> "Şimdi de yönetmelikle alakasız bir soru soralım. Görüyorsunuz, uydurma
> bir cevap vermek yerine dürüstçe 'bu bilgi elimde yok' diyor. Bu, RAG
> sistemlerinde en kritik özelliklerden biri: halüsinasyon yapmamak."

*(Opsiyonel Soru 3: "Derslere devamsızlık sınırını aşan öğrenciye hangi
not verilir?")*

> "İlginç bir bulgu paylaşmak istiyorum: bu soruda model doğru dokümanı
> buldu, ama küçük bir hata yaparak yanlış bir not kodu söyledi."

---

**[2:05-2:45] BULGU / DERS ÇIKARIMI**
*(Ekranda: TEST_RESULTS.md dosyası, ilgili kısım vurgulanmış)*

> "Bu bize önemli bir ders verdi: yüksek bir retrieval benzerliği, cevabın
> doğru olacağının garantisi değil. Doğru kaynağı bulmak yetmiyor, küçük
> modeller o kaynaktaki detayı yanlış aktarabiliyor. Bunu görünce sistemde
> bir eşik değeri ekledik - konuyla alakasız sorularda modele hiç
> sormadan otomatik olarak 'bilmiyorum' cevabı veriyoruz - ve bu riski
> README'de açıkça belgeledik."

---

**[2:45-3:00] KAPANIŞ**

> "Sonuç olarak, bir aylık bu çalışmada hem RAG mimarisini uçtan uca kurmayı,
> hem de küçük yerel modellerin gerçek sınırlarını görmeyi öğrendim.
> Teşekkürler."

---

## Kayıt Notları

- Kayıttan önce modeli bir kez ısıt (örnek bir soru sor, cevabı bekle) -
  ilk soğuk yanıt 30-60 saniye sürebilir, bunu videoya almana gerek yok.
- Soruları önceden bir metin dosyasına yaz, demo sırasında kopyala-yapıştır
  yap; yazım hatası riskini ortadan kaldırır.
- Model cevap üretirken geçen bekleme süresini kurguda kısalt/hızlandır
  veya kes; seslendirmeni bu kesim üzerine sonradan bindirebilirsin.
- Toplam kelime sayısı ~280; ortalama konuşma hızıyla (dakikada ~110-130
  kelime, doğal duraklamalarla) 3 dakikaya oturur. Kendi okuma hızına göre
  ince ayar yapabilirsin.
