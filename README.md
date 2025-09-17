# 红楼梦AI翻译-中英对照



## 简介
使用DeepSeek-V3.1模型的reasoner模式，将《红楼梦》从中文翻译为英文，并以中英对照的形式呈现   
翻译耗时较长，但无需担心，translate.py脚本能够自动跳过已翻译内容，继续翻译未翻译的章节


**本项目仅作为学术研究使用**，学术合作可联系ziyang.zeng@upf.edu或zengziyang@foxmail.com



## 致谢
本项目《红楼梦》全文文件来自项目：[red-chamber-llm] https://github.com/turbo-duck/red-chamber-llm/blob/main/01-txt/red-chamber.txt



## 目录结构
```
hongloumeng_AItranslate/
├─ input/                         # 存放《红楼梦》全文txt文件
├─ chapters/                      # 存放《红楼梦》各章节
├─ translations/                  # 存放《红楼梦》AI译文
├─ output/                        # 存放中英对照《红楼梦》AI译文

├─ requirements.txt               #环境要求
├─ split.py                       #分章脚本：将《红楼梦》全文按章节分段
├─ translate.py                   #翻译脚本：调用deepseekV3.1 reasoner进行翻译
├─ generate.py                    #生成脚本：生成中英对照html文件
├─ README.md
```



## 快速开始（Google Colab）

1. 安装依赖
```bash
!pip install -r requirements.txt
```

2. 切分章节
```bash
!python3 split.py    #切分结果位于chapters/
```

3. 翻译章节
```python
import os
os.environ["DEEPSEEK_API_KEY"] = "你的API_KEY"    #这里设置你的API
!python3 translate.py --model deepseek-reasoner    #这里也可以使用deepseek-chat模式；翻译结果位于translations/
```

4. 生成中英文对照对照
```bash
!python3 generate.py   #输出结果位于output/hongloumeng_ZHvsEN.html
```
