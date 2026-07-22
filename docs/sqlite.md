# Yerel Veri Depolama için SQLite

SQLite, sunucu gerektirmeyen, tek bir dosyada saklanan, kendi kendine yeten bir
SQL veritabanı motorudur. Dünyada en yaygın kullanılan veritabanı motorudur ve
Python'da yerleşik `sqlite3` modülüyle ek kurulum yapmadan kullanılabilir.

## Neden SQLite?

- Ayrı bir sunucu süreci veya kurulum gerektirmez.
- Tüm veritabanı tek bir dosyadır; taşınabilir ve yedeklemesi kolaydır.
- Platformdan bağımsızdır (Windows/macOS/Linux).
- Küçük/orta ölçekli yerel uygulamalar için performansı yeterlidir.

## Bu Projedeki Kullanımı

Bu projede SQLite, doküman parçalarını (chunk) ve bunlara karşılık gelen
embedding vektörlerini saklamak için kullanılır. Basit bir şema yeterlidir:

```sql
CREATE TABLE chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding TEXT NOT NULL
);
```

`embedding` sütunu, vektörün JSON olarak serileştirilmiş halidir (SQLite'ın
yerleşik bir vektör tipi olmadığı için). Sorgu zamanında bu JSON tekrar bir
sayı listesine çevrilip kosinüs benzerliği hesaplanır.
