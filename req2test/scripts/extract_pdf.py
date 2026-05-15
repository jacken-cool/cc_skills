"""可复用 PDF 文本提取脚本

用法:
    python extract_pdf.py /path/to/file.pdf          # 输出到 stdout
    python extract_pdf.py /path/to/file.pdf -o out.txt # 输出到文件
"""

import sys
import io
import argparse


def extract_pdf_text(pdf_path: str) -> str:
    """返回 PDF 完整文本，按页分隔"""
    import fitz
    doc = fitz.open(pdf_path)
    parts = []
    for i, page in enumerate(doc):
        text = page.get_text()
        parts.append(f"===== 第{i + 1}页 =====\n{text}")
    doc.close()
    return "\n".join(parts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="提取 PDF 文本内容")
    parser.add_argument("pdf_path", help="PDF 文件路径")
    parser.add_argument("-o", "--output", help="输出文件路径（可选，默认 stdout）")
    args = parser.parse_args()

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    text = extract_pdf_text(args.pdf_path)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"已保存至 {args.output}")
    else:
        print(text)
