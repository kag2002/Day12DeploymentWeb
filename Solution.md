# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found in basic/app.py
1. **Hardcoded Secrets**: The API key (`OPENAI_API_KEY`) and database connection string (`DATABASE_URL`) are hardcoded in the source code. If pushed to public repositories, they will leak instantly.
2. **No Config Management**: Configurations (`DEBUG = True`, `MAX_TOKENS = 500`) are hardcoded in the code rather than using environment variables or settings files.
3. **Improper Logging**: Using standard `print()` statements instead of structured logs. Print logs are slow, hard to parse, and they leak the sensitive `OPENAI_API_KEY` into the standard output.
4. **No Health Checks**: Missing `/health` and `/ready` endpoints, preventing orchestration platforms from checking the health of the container and restarting it if it crashes.
5. **Fixed Binding & Port**: Hardcoded `host="localhost"` (making the container inaccessible from outside) and `port=8000` (does not respect the `PORT` environment variable injected by Railway/Render), along with running `reload=True` which consumes high resources and should not be used in production.

### Exercise 1.3: Comparison table
| Feature | Basic (Develop) | Advanced (Production) | Tại sao quan trọng? |
| :--- | :--- | :--- | :--- |
| **Config** | Hardcoded in source code | Environment variables (12-Factor App) | Cho phép thay đổi cấu hình giữa các môi trường dễ dàng không cần build lại code, bảo mật secret keys. |
| **Health Check** | Không triển khai | Có `/health` (Liveness) & `/ready` (Readiness) | Giúp platform tự động restart nếu app crash, chỉ chuyển traffic khi container đã hoàn tất tải model/DB. |
| **Logging** | Dùng `print()` | Structured JSON logging | Dễ parse, lọc, và tìm kiếm logs trên các hệ thống thu thập log tập trung (Datadog, Kibana, Loki) khi hệ thống scale. |
| **Shutdown** | Tắt đột ngột (abrupt) | Graceful shutdown (SIGTERM handling) | Đảm bảo các request đang xử lý được hoàn thành và đóng kết nối đến DB/Redis an toàn trước khi tắt container. |

---

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. **Base image**: `python:3.11` (chứa toàn bộ Python runtime và các build tools đầy đủ, dung lượng ~1 GB).
2. **Working directory**: `/app` (đường dẫn làm việc chính cô lập bên trong container).
3. **Tại sao COPY requirements.txt trước?**: Để tận dụng cơ chế Docker layer caching. Docker sẽ không chạy lại bước cài dependencies nặng nề (`RUN pip install`) nếu danh sách requirements không thay đổi, giúp tăng tốc build đáng kể.
4. **CMD vs ENTRYPOINT**: `CMD` định nghĩa command mặc định có thể bị ghi đè hoàn toàn khi chạy container. `ENTRYPOINT` định nghĩa tệp thực thi chính cố định của container, các tham số truyền thêm khi chạy sẽ được nối đuôi vào.

### Exercise 2.3: Image size comparison
- **Develop image size**: ~1.02 GB
- **Production image size**: ~200 MB
- **Difference**: Giảm ~80% dung lượng.
- **Why**: Do sử dụng Multi-stage build và base image `python:3.11-slim`. Mọi build tools, compiler (gcc, v.v.) cài đặt ở stage 1 (builder) bị loại bỏ, chỉ copy phần thư viện đã cài đặt sang stage 2 (runtime) siêu nhẹ.

### Exercise 2.4: Nginx Load Balancer Architecture
```
Client
  │
  ▼ (port 80)
┌────────────────────────┐
│      Nginx LB          │
└─────────┬──────────────┘
          │ (phân phối request)
          ├─────────────────────────┬─────────────────────────┐
          ▼ (port 8000)             ▼ (port 8000)             ▼ (port 8000)
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│ Agent Instance 1 │      │ Agent Instance 2 │      │ Agent Instance 3 │
└─────────┬────────┘      └─────────┬────────┘      └─────────┬────────┘
          │                         │                         │
          └─────────────────────────┼─────────────────────────┘
                                    ▼
                          ┌──────────────────┐
                          │   Redis Cache    │ (port 6379, stateless store)
                          └──────────────────┘
```

---

## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- **URL**: https://chatbotsearchweb-production.up.railway.app
- **Screenshot**: [Link to screenshot trong repo hoặc cập nhật screenshots/dashboard.png]

### Exercise 3.2: Railway vs Render config files
- `railway.toml`: Được dùng để tuỳ biến hành vi build và deploy của Railway CLI (như chỉ định build command, watch patterns, static files).
- `render.yaml`: Cấu hình Infrastructure-as-Code (IaC) của Render (Blueprint spec). Cho phép định nghĩa toàn bộ hạ tầng gồm Web Service, Redis, Postgres, các biến môi trường và ổ đĩa volume trong một file duy nhất để deploy đồng bộ.

---

## Part 4: API Security

### Exercise 4.1-4.3: Test results
```bash
# Test API Key Authentication
$ curl http://localhost:8000/ask -X POST -d '{"question":"Hello"}'
{"detail":"Invalid or missing API key. Include header: X-API-Key: <key>"}

$ curl http://localhost:8000/ask -X POST -H "X-API-Key: dev-key-change-me" -H "Content-Type: application/json" -d '{"question":"Hello"}'
{"question":"Hello","answer":"Tôi là AI agent được deploy lên cloud. Câu hỏi của bạn đã được nhận.","model":"gpt-4o-mini","timestamp":"2026-06-12T09:20:00Z"}
```

### Exercise 4.4: Cost guard implementation
- **Cách tiếp cận**: 
  - Tính toán số lượng tokens ước tính từ câu hỏi đầu vào (1 từ ≈ 2 tokens) và câu trả lời đầu ra.
  - Sử dụng Redis để lưu trữ chi phí tích luỹ của từng user trong ngày/tháng với định dạng key `budget:{user_id}:{date}`.
  - Trước khi gọi LLM, kiểm tra xem tổng chi phí đã dùng cộng với chi phí ước lượng của request này có vượt quá ngân sách hay không (`daily_budget_usd`).
  - Nếu vượt quá ngân sách, trả về lỗi `503 Daily budget exhausted`. Nếu không vượt quá, thực hiện request và cập nhật chi phí thực tế vào Redis bằng lệnh `incrbyfloat` và set TTL tự động reset.

---

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
- **Health / Readiness Checks**:
  - `/health` trả về trạng thái của app (200 OK) để platform xác định container còn chạy hay đã chết (Liveness).
  - `/ready` kiểm tra kết nối tới Redis/Database (200 OK). Nếu kết nối thất bại, trả về 503 để load balancer ngừng route traffic vào container bị lỗi đó.
- **Graceful Shutdown**:
  - Đăng ký bộ xử lý tín hiệu SIGTERM. Khi platform muốn shutdown instance để deploy bản mới hoặc scale down, container sẽ dừng nhận request mới, đợi các request cũ trong hàng đợi hoàn thành (uptime grace period) rồi mới đóng các kết nối Redis/DB và exit an toàn.
- **Stateless Design**:
  - Toàn bộ conversation history và session của user được đồng bộ hóa lên Redis thay vì lưu ở bộ nhớ trong RAM. Nhờ vậy, load balancer có thể điều hướng request tiếp theo của user tới bất kỳ instance nào trong pool scale mà không bị mất ngữ cảnh hội thoại.
