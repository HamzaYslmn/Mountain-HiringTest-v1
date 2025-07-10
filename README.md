# Mountain Hiring Test

Bu proje, işe alım sürecinde teknik yetkinliğinizi değerlendirmek için hazırlanmış bir test uygulamasıdır. Backend tarafında FastAPI ile geliştirilen RESTful AI servisleri ve bunlarla entegre çalışan bir frontend arayüzü içerir.

## Testin Amacı

- AI tabanlı servislerin entegrasyonunu ve kullanımını göstermek
- API ile etkileşimli, modern ve kullanıcı dostu bir frontend tasarlamak
- Kod kalitesi, dokümantasyon ve teslimat disiplinini değerlendirmek

## İçerik

- [Kurulum](#kurulum)
- [API Servisleri](#api-servisleri)
- [Frontend Tasarım Görevi](#frontend-tasarım-görevi)
- [Çalıştırma](#çalıştırma)
- [Teslimat ve Katkı](#teslimat-ve-katkı)
- [Lisans](#lisans)

## Kurulum

### Gereksinimler

- Python 3.13 ([İndir](https://www.python.org/downloads/release/python-313/))
- Node.js (Frontend için)

### Adımlar

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/HamzaYslmn/Mountain-HiringTest-v1.git
   ```
2. Python bağımlılıklarını yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

## API Servisleri

Tüm servisler FastAPI ile sunulmaktadır. Otomatik API dokümantasyonu için:
- [Swagger UI](http://localhost:8001/docs)
- [ReDoc](http://localhost:8001/redoc)

### Durum Kontrolü
- **GET** `/status`
- API'nin çalışıp çalışmadığını kontrol eder.

### Chat Servisi (Metin ve Görüntü)
- **POST** `/chat`
- JSON Parametreler:
  - `message` (str): Kullanıcı mesajı
  - `agent_id` (str, opsiyonel): AI ajan kimliği
  - `photo` (str, opsiyonel): Base64 kodlu görsel veya görsel URL'si
  - `response_id` (str, opsiyonel): Önceki yanıt kimliği
- Not: Görüntü tabanlı sorgular için `photo` alanı kullanılabilir. Ayrı bir vision endpoint'i yoktur.

### TTS (Text-to-Speech) Servisi
- **POST** `/tts`
- JSON Parametreler:
  - `text` (str): Konuşmaya dönüştürülecek metin
  - `thread_id` (str): Konu kimliği
  - `assistant_id` (str): Asistan kimliği
- Yanıt: WAV formatında ses dosyası (audio/wav)

### STT (Speech-to-Text) Servisi
- **POST** `/stt`
- JSON Parametreler:
  - `audio` (str): Base64 kodlu ses dosyası (WAV)
  - `thread_id` (str): Konu kimliği
  - `assistant_id` (str): Asistan kimliği
- Yanıt: Çözümlenmiş metin

## Frontend Tasarım Görevi

- Chat arayüzü için örnek ekranı geliştirmeniz beklenmektedir.
- Claude, Gemini, ChatGPT gibi modern AI arayüzlerinden ilham alarak, daha iyi ve kullanıcı dostu bir tasarım sunun.
- Figma veya tercih ettiğiniz bir araçla tasarımınızı oluşturun.
- Teslimatta Figma linki veya tasarım dosyasını ekleyin.

## Çalıştırma

### Backend
```bash
python xMain.py
```
Sunucu: [http://localhost:8001](http://localhost:8001)

### Frontend
Frontend framework'ünüze göre uygun komutları kullanın (örn. `npm start`).

## Teslimat ve Katkı

- Kodunuzu ve tasarımınızı paylaşın.
- Açık ve anlaşılır bir şekilde dokümante edin.
- Sorularınız için: developer@mountain.com.tr

## Lisans

Detaylar için `LICENSE` dosyasına bakın.

---

Başarılar!
