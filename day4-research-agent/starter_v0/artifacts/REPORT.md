# Báo Cáo Lab v2 Ngày 04 — Research Agent

## Nhóm phát triển

- Nhóm: Zone6 Team 3
- Thành viên: Lê Thiên Khang 2A202600726, Nguyễn Thụy Như Quỳnh 2A202600557.
- Nhà cung cấp/Mô hình: openrouter / openai/gpt-4o-mini.

## Chỉ số đánh giá cuối cùng (Final Metrics)

- Phiên bản cuối cùng: v3
- Phiên bản artifact: v3+p5bb531a3fcb9+tc3175e01710f
- File chạy thử nghiệm cơ sở tốt nhất: v3_B_base_openrouter_20260602T153132204653.json
- Độ chính xác Base case: 1.00
- Độ chính xác định tuyến công cụ Base: 1.00
- Độ chính xác tham số Base: 1.00
- File chạy thử nghiệm nhóm: v3_B_group_openrouter_20260602T153211845926.json
- Độ chính xác Group: 1.00
- File transcript chat thực tế: v3_openrouter_20260602T152630066981.transcript.json

## Minh chứng các phiên bản (Version Evidence)

Dữ liệu được điền từ `artifacts/version_log.csv` và `runs/*.json`.

| Phiên bản | Thành phần thay đổi | Giả thuyết tối ưu hóa | Điểm số trước | Điểm số sau | File chạy thử nghiệm |
|---|---|---|---:|---:|---|
| v0 | baseline | Cấu hình prompt và công cụ ban đầu | 0.00 | 0.75 | v0_B_base_openrouter_20260602T150703968910.json |
| v1 | system_prompt.md | Xử lý các tác vụ ngoài phạm vi và làm rõ ranh giới các công cụ | 0.75 | 0.85 | v1_B_base_openrouter_20260602T151058773184.json |
| v2 | system_prompt.md | Tối ưu hóa định tuyến, đơn giản hóa truy vấn và tính nhất quán tham số đa lượt | 0.85 | 0.95 | v2_B_base_openrouter_20260602T151312416650.json |
| v3 | tools.yaml; tools/__init__.py; system_prompt.md | Tích hợp công cụ thời tiết mới, ánh xạ địa danh và ranh giới chuyển đổi công cụ | 0.95 | 1.00 | v3_B_base_openrouter_20260602T153132204653.json |

## Phân tích lỗi (Failure Analysis)

Các lỗi thực tế được trích xuất từ `results[*].result.failures`.

| Mã lỗi | Loại lỗi | Công cụ đã gọi | Nội dung lỗi | Phương án khắc phục |
|---|---|---|---|---|
| R10_missing_handle | missing_info | Không gọi tool | Tự ý đoán handle hoặc trả về văn bản chung chung | Hướng dẫn Agent sử dụng công cụ `clarify` với `response_type=text` để hỏi handle |
| R12_confirm_before_send | wrong_boundary | send (chạy trực tiếp) | Thực thi công cụ `send` mà không xin xác nhận từ người dùng trước | Hướng dẫn Agent gọi `clarify` với `response_type=yes_no` để xác nhận |
| M06_switch_tool | wrong_tool | lookup + social_search (song song) | Giữ công cụ cũ trong lịch sử và gọi song song cả hai công cụ | Hướng dẫn Agent từ bỏ hoàn toàn công cụ trước đó khi người dùng đổi đề tài |
| G08_multiturn_switch_weather_to_tweets | wrong_tool | social_search (thay vì timeline) | Định tuyến nhầm sang social_search khi chuyển tiếp từ thời tiết | Chuẩn hóa quy tắc định tuyến timeline cho tên người cụ thể |

## Các ca đánh giá tự phát triển (Team Eval Cases)

Liệt kê ít nhất 5 ca kiểm thử được thêm vào `data/eval_group.json`.

| Mã test | Nội dung kiểm thử | Công cụ / Hành vi mong đợi | Kết quả |
|---|---|---|---|
| G01_weather_hanoi | Tra cứu thời tiết cho thành phố Việt Nam ánh xạ sang tiếng Anh | weather(location="Hanoi") | PASS |
| G02_weather_missing_location | Thiếu địa điểm khi hỏi thời tiết sẽ kích hoạt làm rõ | clarify(response_type="text") | PASS |
| G03_out_of_scope_cooking | Từ chối yêu cầu nấu ăn nằm ngoài phạm vi hỗ trợ | no_tool (hành vi: từ chối lịch sự) | PASS |
| G04_confirm_send_telegram | Yêu cầu gửi Telegram kích hoạt xác nhận yes/no | clarify(response_type="yes_no") | PASS |
| G08_multiturn_switch_weather_to_tweets | Chuyển đổi từ tra thời tiết sang timeline của Sam Altman | timeline(screenname="sama") | PASS |

## Minh chứng Hội thoại Thực tế (Live Chat Evidence)

Dữ liệu lấy từ `transcripts/*.transcript.json`.

| Lượt | Yêu cầu của người dùng | Công cụ đã gọi | Phiên bản | Kết quả hiển thị |
|---|---|---|---|---|
| 1 | Thời tiết Hà Nội hôm nay ra sao? | weather(location="Hanoi") | v3 | Lấy thông tin thời tiết thành công: "nắng nhẹ với nhiệt độ khoảng 35°C" |
| 2 | À nhầm, cho mình xem thời tiết ở Sài Gòn nhé | weather(location="Ho Chi Minh City") | v3 | Lấy thông tin thời tiết thành công: "mưa rào với nhiệt độ khoảng 31°C" |
| 3 | Đăng thông tin thời tiết này lên Telegram giúp mình | clarify(response_type="yes_no", question="...") | v3 | Hỏi xác nhận bảo mật: "Bạn có muốn đăng bản tin thời tiết này lên Telegram không?" |
| 4 | Có, gửi đi | send(confirmed=true, text="...") | v3 | Gọi công cụ `send` với `confirmed=true`; báo lỗi môi trường vì chưa cấu hình token thật |

## Minh chứng tính năng mở rộng (Bonus Evidence)

Chỉ điền khi nhóm có làm tính năng mở rộng.

| Tính năng mở rộng | File logic tương ứng | Nguyên lý hoạt động thành công | Giải pháp bảo mật / Ranh giới bảo vệ |
|---|---|---|---|
| send (Telegram) | tools/send/tool.py | Yêu cầu xác nhận yes_no thông qua prompt và tham số confirmed=True | Ngăn chặn tự ý gửi dữ liệu ra môi trường bên ngoài khi chưa được phép |
| arXiv / Chính sách nội bộ | tools/policy/tool.py; tools/papers/tool.py | Truy vấn kho học thuật arXiv và tìm kiếm văn bản quy định của doanh nghiệp | Giới hạn miền tìm kiếm và kiểm soát dung lượng văn bản trích xuất |
| Giao diện Web | frontend/src/components/chat/Sidebar.tsx | Web app xem lịch sử chat và phân tích chuyên sâu các file log | Không có rủi ro |

## Câu hỏi tự suy ngẫm (Reflection)

- **Những sửa đổi nào thuộc về `system_prompt.md`?**
  Các sửa đổi liên quan đến ánh xạ ngữ nghĩa (ví dụ: dịch "Hà Nội" thành "Hanoi"), các quy tắc định tuyến đa lượt nghiêm ngặt (ví dụ: hủy bỏ công cụ cũ trước khi chuyển chủ đề) và xác lập ranh giới đầu ra (ví dụ: xin xác nhận trước khi gửi) thuộc về prompt hệ thống.
- **Những sửa đổi nào thuộc về `tools.yaml`?**
  Khai báo chính xác kiểu dữ liệu, mô tả chi tiết các tham số (ví dụ: định dạng tên địa danh) và liệt kê danh sách tham số bắt buộc thuộc về `tools.yaml` để đảm bảo mô hình LLM diễn giải đúng cấu trúc schema của công cụ.
- **Lỗi nào cần đánh giá thủ công thay vì chấm điểm tự động?**
  Sự biến đổi từ ngữ trong câu trả lời tự nhiên của Agent (ví dụ: cách tóm tắt thời tiết ngắn gọn hay biểu cảm hỏi làm rõ của Agent) cần đánh giá thủ công bằng mắt để thẩm định chất lượng giao tiếp, trong khi việc định tuyến công cụ và kiểm tra tham số hoàn toàn phù hợp để chấm điểm tự động.
- **Bạn sẽ cải tiến điều gì tiếp theo?**
  Chúng tôi sẽ cấu hình token Telegram thực tế để kiểm thử việc gửi tin nhắn trực tiếp ngoài đời thực và nâng cấp công cụ thời tiết để hỗ trợ dự báo thời tiết 5 ngày tiếp theo.
