# RAG (Retrieval-Augmented Generation) Nedir?

RAG, bir dil modelinin cevaplarını kendi eğitim verisiyle sınırlı kalmadan, harici
bir bilgi kaynağından alınan güncel/özel içerikle zenginleştirmesini sağlayan bir
tasarım desenidir. Üç adımdan oluşur:

1. **Retrieve (Getir):** Kullanıcının sorusuyla en alakalı doküman parçalarını
   (chunk) bir bilgi tabanından bul.
2. **Augment (Zenginleştir):** Bulunan parçaları modelin prompt'una bağlam (context)
   olarak ekle.
3. **Generate (Üret):** Model, bu bağlamı kullanarak sorulan soruya cevap üretir.

## Neden RAG Kullanılır?

Salt bir LLM'e soru sorulduğunda, model yalnızca eğitim verisindeki genel bilgiye
dayanır ve özel/güncel dokümanlar hakkında ya yanlış (halüsinasyon) ya da eksik
cevap verebilir. RAG, cevabı gerçek dokümanlara dayandırarak (source-grounded)
hem doğruluğu artırır hem de kaynak gösterme imkânı sağlar.

## Bu Projedeki Uygulama

Bu projede RAG şu şekilde uygulanır: dokümanlar paragraf bazlı parçalara bölünür,
her parça embedding modeliyle vektöre çevrilip SQLite'a kaydedilir. Bir soru
geldiğinde, soru da embed edilir; kosinüs benzerliğiyle en alakalı parçalar
bulunur ve yerel LLM'e "yalnızca bu bağlamı kullan" talimatıyla birlikte verilir.
