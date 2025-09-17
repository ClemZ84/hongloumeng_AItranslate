#!/usr/bin/env python3
import os, json, time, argparse, re
from tqdm import tqdm
from openai import OpenAI

def contains_too_much_chinese(text, threshold=0.2):
    """检测翻译结果里是否有太多中文字符"""
    if not text:
        return True
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    return chinese_chars / max(len(text), 1) > threshold

def translate_text(client, model, system_prompt, text, max_tokens=4000, retries=3):
    """带重试的翻译函数"""
    for attempt in range(retries):
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            max_tokens=max_tokens,
        )
        out = resp.choices[0].message.content.strip()
        if not contains_too_much_chinese(out):
            return out
        time.sleep(2)  # 重试等待
    return out  # 即使失败也返回最后一次

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapters_dir", default="chapters")
    parser.add_argument("--out_dir", default="translations")
    parser.add_argument("--model", default="deepseek-reasoner")
    parser.add_argument("--sleep", type=float, default=1.0)
    args = parser.parse_args()

    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("请先设置 DEEPSEEK_API_KEY 环境变量")

    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    os.makedirs(args.out_dir, exist_ok=True)

    system_prompt = (
        "You are a highly experienced literary translator specialized in Chinese to English. "
        "Completely translate the given texts of 《红楼梦(Dream of the Red Chamber)》 into English. "
        "Always considering the context and cultural background when translating it."
        "Do not copy other translators' existing translations."
        "Only return one best version of your translation."
    )

    files = sorted([f for f in os.listdir(args.chapters_dir) if f.endswith(".json")])
    for fname in tqdm(files, desc="翻译章节中"):
        inpath = os.path.join(args.chapters_dir, fname)
        outpath = os.path.join(args.out_dir, fname)

        # 如果已翻译过，跳过
        if os.path.exists(outpath):
            continue

        with open(inpath, "r", encoding="utf-8") as f:
            ch = json.load(f)

        # 按 1000 字切分正文
        chunks = [ch["text"][i:i+1000] for i in range(0, len(ch["text"]), 1000)]
        translations = []
        for chunk in chunks:
            en = translate_text(client, args.model, system_prompt, chunk)
            translations.append(en)
            time.sleep(args.sleep)

        final_translation = "\n\n".join(translations)
        out_data = {
            "index": ch["index"],
            "title": ch["title"],
            "original": ch["text"],
            "translation": final_translation
        }
        with open(outpath, "w", encoding="utf-8") as f:
            json.dump(out_data, f, ensure_ascii=False, indent=2)

    print("✅ 全部章节翻译完成")

if __name__ == "__main__":
    main()