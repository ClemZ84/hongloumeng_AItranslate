#!/usr/bin/env python3
import os, re, json

def split_chapters(input_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    chapters = []
    current = None
    buffer = []
    chapter_num = None

    # 匹配 “第X章”，X 必须是阿拉伯数字
    chapter_header_pattern = re.compile(r"^第(\d{1,3})章")

    for line in lines:
        line_stripped = line.strip()

        # 检查是否是章节开头
        m = chapter_header_pattern.match(line_stripped)
        if m:
            num = int(m.group(1))
            # 必须在范围内
            if 1 <= num <= 120:
                # 如果当前章节还没结束就遇到新的章节，直接丢弃新的
                if current and buffer:
                    pass
                # 开始新章节
                chapter_num = num
                current = line_stripped
                buffer = []
            continue

        # 检查是否是章节结束
        if line_stripped == "(本章完)" and current:
            idx = f"{chapter_num:03d}"
            text = "\n".join(buffer).strip()
            data = {"index": idx, "title": current, "text": text}
            chapters.append(data)
            with open(os.path.join(out_dir, f"{idx}.json"), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            current = None
            buffer = []
            chapter_num = None
            continue

        # 普通正文
        if current is not None:
            buffer.append(line.rstrip("\n"))

    print(f"✅ 共切分 {len(chapters)} 章，保存到 {out_dir}/")

if __name__ == "__main__":
    split_chapters("input/hongloumeng.txt", "chapters")