
```markdown
# Algorithm 1 - Ngram

## Contributors
- **Nguyễn Đan Thục Khanh** - Implement thuật toán Ngram.
- **Nguyễn Lê Tuấn Thành** - Cải thiện thời gian và độ chính xác.

## Overview
**Ngram**, cụ thể là Bigram, chạy qua 1 chuỗi string và tạo các cặp chữ liền kề nhau bỏ vào 1 set sau đó tính độ giống nhau giữa 2 chuỗi.
Công thức tính độ giống nhau: **Sørensen-Dice Coefficient** = (tổng số cặp chữ giống nhau của 2 chuỗi * 2) / (tổng độ dài 2 chuỗi)

## Code Overview
1. **Bước 1**: Đọc dữ liệu từ file database.csv đã chuẩn bị trước chứa mapping giữa phường, quận, thành phố.
2. **Bước 2**: Lọc các dữ liệu N/A và format tên về chữ thường, xóa các kí tự đặt biệt và dấu cách.
3. **Bước 3**: Tạo thêm 4 cột tên phường + quận (combo1), phường + thành phố (combo2), quận + thành phố (combo3), phường + quận + thành phố (combo4).
4. **Bước 4**: Tạo Bigram cho các cột.
5. **Bước 5**: Đọc input của testcase và format input về chữ thường, xóa các kí tự đặt biệt và dấu cách.
6. **Bước 6**: Tạo Bigram cho imput.
7. **Bước 7**: Tính độ giống nhau giữa Bigram input và Bigram combo4 và chọn hàng có điểm cao nhất.
8. **Bước 8**: Tính độ giống nhau giữa Bigram input và Bigram combo1, combo2, combo3 của hàng đã chọn ở Bước 7.
9. **Bước 9**: So sánh điểm độ giống nhau của Bigram input và Bigram combo1, combo2, combo3, combo4 và chọn combo có điểm cao nhất.
10. **Bước 10**: Trả tên phường, quận, thành phố tùy theo combo.

## Future Improve
- Tự động ngắt khi thời gian chạy gần 0.1s
- Trả về rỗng nếu tên bị xóa trong DB của thầy
- Đọc chữ viết tắt
- Cải thiện đọc số
- Cảm thiện thời gian