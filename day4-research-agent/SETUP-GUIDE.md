# Hướng dẫn Setup & Chạy Dự án Research Agent

Tài liệu này tóm tắt 3 vấn đề quan trọng về các thông tin cần điền vào file cấu hình, chi phí sử dụng Model/API và giao diện của dự án để bạn tiện theo dõi.

---

## 1. Các thông tin cần điền để chạy dự án

Bạn cần sao chép file [.env.example](file:///c:/Users/Admin/Documents/VinUni/CodeLab/Day4/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/.env.example) thành `.env` nằm trong thư mục `starter_v0` và điền đầy đủ các khóa API sau:

### A. Model Provider (Bắt buộc chọn một)
* **`OPENROUTER_API_KEY`**: (Khuyên dùng) Cho phép truy cập nhiều dòng mô hình khác nhau.
* Hoặc các tùy chọn API trực tiếp:
  * `GEMINI_API_KEY` (Google AI Studio)
  * `OPENAI_API_KEY` (OpenAI)
  * `ANTHROPIC_API_KEY` (Anthropic)

### B. API Keys cho các Công cụ (Core Tools)
* **`TAVILY_API_KEY`**: Dùng cho công cụ tìm kiếm web `lookup`.
  * *Đăng ký lấy key miễn phí tại:* [Tavily](https://app.tavily.com)
* **`FIRECRAWL_API_KEY`**: Dùng cho công cụ cào/đọc nội dung bài viết từ URL `fetch`.
  * *Đăng ký lấy key miễn phí tại:* [Firecrawl](https://www.firecrawl.dev)
* **`RAPIDAPI_KEY`** & **`RAPIDAPI_TWITTER_HOST`**: Dùng cho các công cụ mạng xã hội X/Twitter (`timeline`, `social_search`).
  * *Đăng ký gói Free tại:* [RapidAPI Twitter API45](https://rapidapi.com/alexanderxbx/api/twitter-api45)
* **`ARXIV_USER_AGENT`**: Điền chuỗi định danh bất kỳ (Ví dụ: `AI20k-Day04-Research-Agent/1.0`) để tải và đọc bài báo khoa học từ arXiv.

### C. Telegram Bonus (Không bắt buộc)
* **`TELEGRAM_BOT_TOKEN`** & **`TELEGRAM_CHAT_ID`**: Dùng nếu bạn muốn thử nghiệm tính năng tự động gửi bài viết lên kênh Telegram của bạn.

---

## 2. Chi phí sử dụng (Model & API có miễn phí không?)

* **Đối với Mô hình ngôn ngữ lớn (LLM):**
  * **OpenRouter:** Cung cấp nhiều mô hình miễn phí hoàn toàn (ví dụ: `google/gemini-2.5-flash:free`, `meta-llama/llama-3-8b-instruct:free`). Bạn chỉ cần tạo tài khoản lấy API key và gọi mô hình mà không cần nạp tiền.
  * **Gemini API:** Google AI Studio cung cấp hạn mức miễn phí (Free Tier) với số lượng request giới hạn mỗi phút, rất thích hợp cho môi trường học tập.
* **Đối với các API công cụ bổ trợ (Tavily, Firecrawl, Twitter API45):**
  * Tất cả các dịch vụ này đều cung cấp gói **Free Trial** (thường từ 1,000 requests/tháng), hoàn toàn đủ cho nhu cầu chạy thử nghiệm và tối ưu hóa dự án trong bài lab mà không phát sinh chi phí.

---

## 3. Giao diện người dùng (UI)

* **Hiện tại:** Dự án **chưa tích hợp sẵn giao diện đồ họa (GUI)**. Tương tác chính được thực hiện thông qua giao diện dòng lệnh (CLI):
  * **Chạy đánh giá tự động:** 
    ```bash
    python run_eval.py --provider openrouter --version v0 --suite base --eval-cases data/eval_base.json
    ```
  * **Trò chuyện trực tiếp với Agent:** 
    ```bash
    python chat.py --provider openrouter --version v3
    ```
* **Mở rộng (Bài tập Bonus):** Bạn và nhóm có thể tự phát triển thêm giao diện đồ họa bằng **Streamlit** hoặc tích hợp các framework Web như **Next.js / Vercel** để đạt thêm điểm cộng cho bài tập lớn.
