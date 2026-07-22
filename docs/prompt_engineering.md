# Soru-Cevap için Prompt Mühendisliği

Doğru dokümanları bulmak yeterli değildir; bu bilgiyi modele nasıl sunduğumuz da
cevabın kalitesini doğrudan etkiler. Chat Completion API'lerinde iki temel rol
vardır:

- **System prompt:** Modele genel davranış talimatı verir (örn. "sadece verilen
  bağlamı kullan").
- **User prompt:** Kullanıcının asıl sorusudur.

## Bu Projede Kullanılan Kurallar

1. Model yalnızca kendisine verilen bağlamı (retrieved context) kullanarak cevap
   vermelidir; bağlam dışında bilgi uydurmamalıdır.
2. Bağlamda cevap yoksa, model "Bu bilgi elimdeki dokümanlarda yok" gibi net bir
   şekilde belirtmelidir; tahmini/halüsinasyon cevap vermemelidir.
3. Mümkünse cevapta hangi kaynaktan (doküman adı) alındığı belirtilmelidir.
4. Cevaplar kısa, net ve konuya odaklı olmalıdır.

Bu kurallar, RAG sisteminin en önemli faydalarından birini (kaynağa dayalı,
güvenilir cevap) garanti altına almak için system prompt içine yazılır.
