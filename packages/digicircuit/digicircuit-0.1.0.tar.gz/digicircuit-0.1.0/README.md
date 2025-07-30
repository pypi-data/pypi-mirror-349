# DigiCircuit

DigiCircuit là một thư viện Python để chuyển đổi biểu thức Boolean thành sơ đồ mạch điện.

## Cài đặt

```bash
pip install digicircuit
```

## Cách sử dụng

1. Tạo file input với các biểu thức Boolean (ví dụ: `data.txt`):
```
1 A + B
2 A.B + C
```

2. Chạy lệnh để tạo sơ đồ mạch:
```bash
digicircuit data.txt
```

Các sơ đồ mạch sẽ được tạo trong thư mục `circuits` dưới dạng file LaTeX.

### Tùy chọn

- `--output_dir` hoặc `-o`: Chỉ định thư mục output (mặc định: `circuits`)
- `--scale` hoặc `-s`: Tỷ lệ của sơ đồ (mặc định: 1.0)

Ví dụ:
```bash
digicircuit data.txt --output_dir my_circuits --scale 1.5
```

## Yêu cầu

- Python >= 3.6
- numpy
- pandas
- openpyxl

## Giấy phép

MIT License 