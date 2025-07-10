## 🚀 Proje Özeti

Mountain Hiring Test, FastAPI tabanlı bir REST API ile Chat ↔ Vision ↔ TTS/STT gibi yapay zeka servislerini birleştirir.

* **Backend**: Python 3.11+, yüksek performanslı FastAPI, akışlı (`StreamingResponse`) yanıtlar.([fastapi.tiangolo.com][1])
* **Middleware**: Basit “Authorization” başlığıyla JWT benzeri “uuid” doğrulaması.([GitHub][2])
* **Frontend**: React/Next 14 önerilir; akışlı JSON parçalarını gerçek-zamanlı işleyerek sohbet arayüzü sunar.
* **Test Otomasyonu**: `BackEnd/AI/test/test.py` senaryosu ile tüm uç-noktalar uçtan uca denetlenir.([GitHub][3])

---

## İçindekiler

1. [Kurulum](#kurulum)
2. [Mimari](#mimari)
3. [Ortamdaki Değişkenler](#ortam-değişkenleri)
4. [API Referansı](#api-referansı)
5. [Örnek İstekler](#örnek-istekler)
6. [Frontend Gereksinimleri](#frontend-gereksinimleri)
7. [Test & CI](#test--ci)
8. [Katkı](#katkı) — [Lisans](#lisans)

---

## Kurulum

### 1. Sistem Gereksinimleri

| Katman    | Sürüm    | Not                                                  |
| --------- | -------- | ---------------------------------------------------- |
| Python    | 3.11.x   | “Add to PATH” işaretli kurulum                       |
| Node.js   | ≥ 20 LTS | Vite veya Next 14 SSR için gereklidir ([Node.js][4]) |
| pip / npm | Güncel   |                                                      |

### 2. Depoyu Çek ve Yükle

```bash
git clone https://github.com/HamzaYslmn/Mountain-HiringTest-v1.git
cd Mountain-HiringTest-v1
pip install -r requirements.txt
npm i        # frontend dizininde (isteğe bağlı)
```

### 3. Server’ı Çalıştır

```bash
# kök dizinde
uvicorn BackEnd.AI.xMain:app --host 0.0.0.0 --port 8001 --reload
```

`BASE_URL` testlerde olduğu gibi `http://localhost:8001/AI`’dir. ([GitHub][3])

---

## Mimari

```txt
 ┌────────────┐      HTTP(S)        ┌──────────────────────────────────────┐
 │   Frontend │ ───────────────────►│ FastAPI App (uvicorn)                │
 └────────────┘                     │  • /status      (health-check)       │
                                    │  • /openai/chat (GPT-4o-vis)         │
                                    │  • /openai/stt  (Speech→Text)        │
                                    │  • /openai/tts  (Text→Speech)        │
                                    │  • middleware.cors + auth            │
                                    └──────────────────────────────────────┘
```

FastAPI’nin otomatik Swagger & ReDoc arayüzleri `/docs` ve `/redoc` altındadır.([fastapi.tiangolo.com][5])

---

## Ortam Değişkenleri

| Adı               | Açıklama                       | Varsayılan |
| ----------------- | ------------------------------ | ---------- |
| `OPENAI_API_KEY`  | Harici LLM kullanacaksanız     | boş        |
| `ALLOWED_ORIGINS` | CORS listesi (`,` ile ayrılır) | `*`        |
| `LOG_LEVEL`       | `info`, `debug`, `warning` …   | `info`     |

---

## API Referansı

### Yetkilendirme

Her isteğe

```http
Authorization: <uuid|token>
```

başlığı eklenmelidir; aksi hâlde `uuid = "public"` atanır ve 401 dönülür.([GitHub][2])

### 1. GET `/AI/status`

Basit sağlık kontrolü. Örnek çıktı:

```json
{
  "status": "online",
  "output": "Welcome to the Mountain API Service! ️"
}
```

([GitHub][6])

### 2. POST `/AI/openai/chat`

| Alan          | Tip    | Zorunlu | Açıklama                           |
| ------------- | ------ | ------- | ---------------------------------- |
| `message`     | string | ✅       | Kullanıcı mesajı                   |
| `agent_id`    | string | ❌       | Prompt/agent anahtarı              |
| `photo`       | string | ❌       | `data:image/...;base64,` ya da URL |
| `response_id` | string | ❌       | Önceki cevapla devam               |

Yanıt **chunk**-chunk (`3 byte`) olarak akan `application/json` tipinde bir akıştır.([GitHub][7])

Örnek nihai JSON:

```json
{
  "emotion": "curious",
  "output": "Merhaba! Ben Mountain Yapay Zeka…"
}
```

### 3. POST `/AI/openai/stt` – Speech → Text

| Alan           | Tip | Açıklama       |
| -------------- | --- | -------------- |
| `audio`        | b64 | WAV/PCM verisi |
| `thread_id`    | str | Konuşma dizisi |
| `assistant_id` | str | Asistan ID     |

İşte, Google Speech üzerinden transkripsiyon döner.([GitHub][8])
`SpeechRecognition` PyPI paketi kullanılır.([PyPI][9])

### 4. POST `/AI/openai/tts` – Text → Speech

| Alan           | Tip | Açıklama       |
| -------------- | --- | -------------- |
| `text`         | str | Okunacak metin |
| `thread_id`    | str | …              |
| `assistant_id` | str | …              |

`pyttsx3` ile offline WAV akışı döner.([GitHub][10], [PyPI][11])

---

## Örnek İstekler

```bash
curl -N -X POST http://localhost:8001/AI/openai/chat \
 -H "Authorization: Mountain" -H "Content-Type: application/json" \
 -d '{"message":"Merhaba!", "agent_id":"pmpt_...", "photo":null}'
```

Akışı satır satır izlemek için `--no-buffer` (`-N`) parametresine dikkat edin.

---

## Frontend Gereksinimleri

### Temel Yığın

| Katman         | Öneri                      |
| -------------- | -------------------------- |
| UI Framework   | React 18 + Next.js 14      |
| Durum Yönetimi | Zustand / Redux Toolkit    |
| Tasarım        | Figma dosyası ⇒ Components |
| Akış İşleme    | Fetch + ReadableStream API |
| Ses            | Web Speech API veya Howler |

> **Akış Sökümü**:  `ReadableStreamDefaultReader` ile 3-bayt parçalardan `TextDecoder().decode(chunk)` yapın ve JSON biriktirin.

---

## Test & CI

```bash
python BackEnd/AI/test/test.py
```

Betik; `/status`, `/chat`, `/chat+image`, `/stt`, `/tts` uç-noktalarını sırayla çağırır ve hataları raporlar.([GitHub][3])
`httpx.AsyncClient` ile yazılmıştır; FastAPI’nin resmi test kılavuzuyla uyumludur.([fastapi.tiangolo.com][12])

---

## Katkı

1. Fork & PR açın.
2. Her yeni rota için **docstring**, örnek istek ve pytest ekleyin.
3. `pre-commit` → black + isort.

---

## Lisans

[Lisans](https://github.com/HamzaYslmn/Mountain-HiringTest-v1/blob/main/LICENSE)


---

### Kaynakça

* FastAPI resmi dokümantasyonu([fastapi.tiangolo.com][1])
* FastAPI Tutorial & Testing([fastapi.tiangolo.com][5], [fastapi.tiangolo.com][12])
* Repository kaynak kodu (routelar)([GitHub][7], [GitHub][8], [GitHub][10], [GitHub][6], [GitHub][2], [GitHub][3])
* SpeechRecognition PyPI sayfası([PyPI][9])
* pyttsx3 PyPI sayfası([PyPI][11])
* Node.js resmi sitesi([Node.js][4])

[1]: https://fastapi.tiangolo.com/?utm_source=chatgpt.com "FastAPI"
[2]: https://raw.githubusercontent.com/HamzaYslmn/Mountain-HiringTest-v1/main/BackEnd/AI/middleware/middleware.py "raw.githubusercontent.com"
[3]: https://raw.githubusercontent.com/HamzaYslmn/Mountain-HiringTest-v1/main/BackEnd/AI/test/test.py "raw.githubusercontent.com"
[4]: https://nodejs.org/en?utm_source=chatgpt.com "Node.js — Run JavaScript Everywhere"
[5]: https://fastapi.tiangolo.com/tutorial/?utm_source=chatgpt.com "Tutorial - User Guide - FastAPI"
[6]: https://raw.githubusercontent.com/HamzaYslmn/Mountain-HiringTest-v1/main/BackEnd/AI/routes/root.py "raw.githubusercontent.com"
[7]: https://raw.githubusercontent.com/HamzaYslmn/Mountain-HiringTest-v1/main/BackEnd/AI/routes/AI/chat_route.py "raw.githubusercontent.com"
[8]: https://raw.githubusercontent.com/HamzaYslmn/Mountain-HiringTest-v1/main/BackEnd/AI/routes/AI/stt_service.py "raw.githubusercontent.com"
[9]: https://pypi.org/project/SpeechRecognition/?utm_source=chatgpt.com "SpeechRecognition·PyPI"
[10]: https://raw.githubusercontent.com/HamzaYslmn/Mountain-HiringTest-v1/main/BackEnd/AI/routes/AI/tts_service.py "raw.githubusercontent.com"
[11]: https://pypi.org/project/pyttsx3/?utm_source=chatgpt.com "pyttsx3 - PyPI"
[12]: https://fastapi.tiangolo.com/tutorial/testing/?utm_source=chatgpt.com "Testing - FastAPI"
