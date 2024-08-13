# Proje Adı

Bu proje bir RESTful API backend ile entegre edilmiş AI servisleri sunan bir uygulama içerir. Ayrıca, backend ile etkileşimde bulunan bir frontend de içerir ve bu sayede tam bir uygulama deneyimi sunar.

## İçindekiler

- [Kurulum](#kurulum)
- [Backend](#backend)
  - [API Dokümantasyonu](#api-dokümantasyonu)
  - [Chatbot Servisi](#chatbot-servisi)
  - [Vision Servisi](#vision-servisi)
  - [TTS (Metin-Konuşma) Servisi](#tts-metin-konuşma-servisi)
  - [STT (Konuşma-Metin) Servisi](#stt-konusma-metin-servisi)
- [Frontend](#frontend)
- [Kullanım](#kullanım)
  - [Backend'i Çalıştırma](#backendi-çalıştırma)
  - [Frontend'i Çalıştırma](#frontendi-çalıştırma)
- [Katkıda Bulunma](#katkıda-bulunma)
- [Lisans](#lisans)

## Kurulum

### Gereksinimler

- [Python 3.11.9](https://www.python.org/downloads/release/python-3119/) (Kurulum sırasında "Add Python to PATH" seçeneğini işaretlemeyi unutmayın)
- Frontend için gerekli olan ek yazılımlar (örneğin, Node.js)

### Adımlar

1. **Depoyu Klonlayın**

   ```bash
   git clone https://github.com/HamzaYslmn/Mountain-HiringTest-v1.git
   ```

2. **Python Bağımlılıklarını Yükleyin**

   Proje dizininde requirements dosyasını bulun ve terminali açarak şu komutu çalıştırın:

   ```bash
   pip install -r requirements.txt
   ```

## Backend

Backend, FastAPI kullanılarak geliştirilmiştir ve çeşitli hizmetlerini RESTful API'ler aracılığıyla sunar.

### API Dokümantasyonu

Otomatik olarak oluşturulan API dokümantasyonuna şu adreslerden erişebilirsiniz:

- **DOCS**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Chatbot Servisi

Chatbot servisi, metin tabanlı girdileri işler ve AI destekli yanıtlar sağlar.

- **Endpoint**: `/chatbot/`
- **Method**: POST
- **Parametreler**:
  - `userinput` (str): Kullanıcıdan gelen metin girdisi. (Örneğin: "Merhaba!")
  - `thread_id` (str): Mevcut konuşma dizisinin kimliği. (Örneğin:"thread_123")
  - `assistant_id` (str): Asistan kimliği. (Örneğin: "asst_123")
  - `username` (str): Kullanıcı adı. (Örneğin: "John Doe")

### Vision Servisi

Bu servis, görüntüleri işler ve ilgili bir yanıt sunar.

- **Endpoint**: `/vision/`
- **Method**: POST
- **Parametreler**:
  - `userinput` (str): Görüntü için ek bağlam veya sorgu.
  - `thread_id` (str): Mevcut konuşma dizisinin kimliği.
  - `assistant_id` (str): Asistan kimliği.
  - `image_file` (UploadFile): İşlenecek görüntü dosyası. (JPEG, PNG)

### TTS (Metin-Konuşma) Servisi

Metin girdisini konuşma sesine dönüştürür.

- **Endpoint**: `/tts/`
- **Method**: POST
- **Parametreler**:
  - `user_input` (str): Konuşmaya dönüştürülecek metin.

### STT (Konuşma-Metin) Servisi

Konuşma sesini metne dönüştürür.

- **Endpoint**: `/stt/`
- **Method**: POST
- **Parametreler**:
  - `thread_id` (str): Mevcut konuşma dizisinin kimliği.
  - `assistant_id` (str): Asistan kimliği.
  - `audio_file` (UploadFile): Yazıya dökülecek ses dosyası. (bu uygulama için WAV)

## Frontend

### Örnek Ekran Tasarımı

Frontend kısmı için daha iyi bir ekran tasarımı yapman bekleniyor. Claude, Gemini, ChatGPT ekranlarından ilham alarak, [http://localhost:8000/HR](http://localhost:8000/HR) adresindeki örnek ekranı geliştirin.

- **Kullanılacak Araç**: Figma (veya tercih ettiğiniz başka bir tasarım aracı)
- **Hedef**: Sağlanan örneklerden daha iyi gözüken, kullanıcı dostu ve görsel olarak çekici bir arayüz tasarlayın.

## Kullanım

### Backend'i Çalıştırma

Backend sunucusunu başlatmak için şu komutu çalıştırın:

```bash
python xMain.py
```

Backend, `http://localhost:8000` adresinde çalışacaktır.

### Frontend'i Çalıştırma

Frontend framework'ünüze göre gerekli talimatları izleyin. Genellikle bir frontend sunucusunu başlatmak için şu komutları kullanabilirsiniz:

```bash
npm start
```

## Lisans

Bu proje lisanslanmıştır. Ayrıntılar için `LICENSE` dosyasına bakın.

---

Bu şablon, projenize başlamanız ve katkıda bulunacak kişiler için gerekli tüm bilgileri sağlar.