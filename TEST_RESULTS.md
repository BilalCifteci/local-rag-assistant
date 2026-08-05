# Test Sonuclari (Hafta 5)

## Cevaplanabilir Sorular (dokumanlarda karsiligi var)

### Soru: RAG nedir ve neden kullanilir?
- En yuksek retrieval benzerligi: 0.6739
- Cevap:  RAG, kaynak: prompt_engineering.md, belirt: "kaynağa dayalı, güvenilir cevap" sağlamak için sistem prompt içine yazılı prompt-dayanabilir, güçlü doğruluğu ve güncel/özel bilgi sağlamak için kullanılır.

### Soru: Foundry Local'in en onemli ozelligi nedir?
- En yuksek retrieval benzerligi: 0.6449
- Cevap:  Foundry Local'in en onemli ozelliği, kullanıcı verilerini hiçbir zaman internete çıkarmayı sağlamaktır, bu da uygulamaları sıfır ağ çağrısıyla yerel ve dictatörlü AI sunabilme yeteneği sağlar.

### Soru: Kosinus benzerligi ne ise yarar?
- En yuksek retrieval benzerligi: 0.6178
- Cevap:  Kosinüs benzerliği, birkaç dokumanın (vektörler) arasındaki anlam yakınlığını ölçmek için kullanılan yöntemdir, bu da SQLite'da `embedding` sütununu kullanarak kosinüs benzerliği hesaplamak için kullanılır. Bu yöntem, dilbilgilere ilişkin dokumanların (vektörler) arasındaki benzerlik değerlendirmesini sağlar, bu da RAG sistemi için soru cevaplarını daha doğru bir dil modeline bağlamaktır.

### Soru: Bu projede SQLite hangi amacla kullaniliyor?
- En yuksek retrieval benzerligi: 0.6901
- Cevap:  Projenizin doküman parçalarını (chunk) ve bunlara karşılık gelen embedding vektörlerini saklamak için SQLite kullandığını belirt. Chunk tablosunu oluşturma ve içerici işleme amacıyla kullandı.

## Cevaplanamaz Sorular (dokuman disi konu)

### Soru: Bugun hava durumu nasil?
- En yuksek retrieval benzerligi: 0.3674
- Cevap: Bu bilgi elimdeki dokumanlarda yok.

### Soru: 2026 Dunya Kupasi'ni hangi ulke kazandi?
- En yuksek retrieval benzerligi: 0.3136
- Cevap: Bu bilgi elimdeki dokumanlarda yok.

## Edge Case: Bos Sorgu

- Beklenen davranis: bos sorgu reddedildi (ValueError: Input must be a non-empty string.)
