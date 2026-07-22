# Embedding ve Vektör Arama

Embedding, bir metnin anlamını sayısal bir vektör (sayı dizisi) olarak temsil etme
yöntemidir. Anlamca birbirine yakın iki metin, vektör uzayında da birbirine yakın
konumlanır. Bu özellik sayesinde "semantik arama" (semantic search) yapılabilir:
tam kelime eşleşmesi aramak yerine, anlam benzerliğine göre arama yapılır.

## Kosinüs Benzerliği (Cosine Similarity)

İki vektör arasındaki anlam yakınlığını ölçmek için en yaygın yöntem kosinüs
benzerliğidir. -1 ile 1 arasında bir değer döndürür; 1'e yaklaştıkça iki metin
anlamca daha benzerdir.

```
cosine_similarity(a, b) = (a · b) / (|a| * |b|)
```

## RAG'de Kullanımı

RAG sisteminde önce bilgi tabanındaki her doküman parçası embedding modeliyle
vektöre çevrilip saklanır. Kullanıcı soru sorduğunda, soru da aynı embedding
modeliyle vektöre çevrilir ve saklanan tüm vektörlerle kosinüs benzerliği
hesaplanarak en yüksek skora sahip parçalar (top-K) seçilir. Bu parçalar daha
sonra dil modeline bağlam olarak verilir.

Küçük ölçekli projelerde (birkaç yüz parça) tüm vektörleri belleğe alıp
karşılaştırmak yeterlidir; çok büyük veri setlerinde özel vektör veritabanları
gerekir.
