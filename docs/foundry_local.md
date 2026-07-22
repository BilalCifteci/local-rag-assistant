# Foundry Local Nedir?

Foundry Local, büyük dil modellerini (LLM) tamamen kullanıcının kendi cihazında,
internet bağlantısı olmadan çalıştırmayı sağlayan uçtan uca bir yerel AI çözümüdür.
Microsoft tarafından geliştirilmiştir ve hafif bir çalışma zamanı (runtime) ile bir
SDK sunar.

Bulut hesabı veya GPU zorunluluğu yoktur: Foundry Local, modelleri otomatik olarak
indirir, yönetir ve CPU/NPU hızlandırmasıyla çalıştırır. Böylece uygulamalar sıfır
ağ çağrısıyla yerel ve çevrimdışı AI sunabilir.

## Öne Çıkan Özellikler

- Model kataloğundan istenen modelin seçilip cihaza indirilmesi (`catalog.get_model`)
- Model belleğe yükleme/kaldırma (`load()` / `unload()`)
- OpenAI uyumlu Chat Completion API (`get_chat_client()`)
- OpenAI uyumlu Embedding API (`get_embedding_client()`)
- Windows, macOS ve Linux desteği

## Neden Bu Projede Kullanıyoruz?

Bu projede Foundry Local, hem embedding üretimi (dokümanları vektöre çevirmek için)
hem de soru-cevap için kullanılan sohbet modelini çalıştırmak için kullanılır. Tüm
işlem cihazda gerçekleştiği için kullanıcı verisi hiçbir zaman internete çıkmaz.
