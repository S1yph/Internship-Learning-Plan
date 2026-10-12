# ai-intern-training

Mini Text Processing Pipeline: 读取 -> 清洗 -> 切分 -> 统计 -> 生成 metadata -> 保存 JSON。

## 运行
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
python src/text_processor.py
```
结果在 `output/documents.json`。
