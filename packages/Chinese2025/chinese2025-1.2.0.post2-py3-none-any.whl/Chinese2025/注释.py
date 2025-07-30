from .Unicode import valid_text, extract_chinese_characters, is_chinese
from .Error import 输入不合法
from .繁體廣韻搜索 import 繁體廣韻搜索
from .繁體平水韻搜索 import 繁體平水韻搜索
from .现代韵书搜索 import 现代韵书搜索

韵字典 = {
    "廣韻":"廣韻",
    "广韵":"廣韻",
    "平水韻":"平水韻",
    "平水韵":"平水韻",
    "现代韵书":"現代韻書",
    "現代韻書":"現代韻書",
    "0":"廣韻",
    "1":"平水韻",
    "2":"現代韻書"
}

import re, pprint

class 注释:
    def __init__(self, text: str, 韵: str | int = "平水韻", 多音字:bool=True, 自动分词:bool=True, 连音变调:bool=False,
                 轻声:bool=False, 特殊声母="特殊声母", 转换符: str = "-i", 转换前符: str = "i", 间隔: str = "，"):
        if not valid_text(text):
            raise 输入不合法(text, "字符串不合法.仅允许中文与标点符号。")

        self.text = text
        self.韵 = self.__获取韵名(str(韵))
        self.多音字 = 多音字
        self.自动分词 = 自动分词
        self.连音变调 = 连音变调
        self.轻声 = 轻声
        self.特殊声母 = 特殊声母
        self.转换符 = 转换符
        self.转换前符 = 转换前符
        self.间隔 = 间隔
        self.pattern = re.compile(
            r'[\u3400-\u4DBF\u4E00-\u9FFF\U00020000-\U0002A6DF'
            r'\U0002A700-\U0002B734\U0002B740-\U0002B81F\U0002B820-\U0002CEAF'
            r'\U0002CEB0-\U0002EBEF\U0002EBF0-\U0002EE5D\U00030000-\U0003134A'
            r'\U00031350-\U000323AF]'
        )

    @staticmethod
    def __获取韵名(name: str):
        if name not in 韵字典:
            raise 输入不合法(name, pprint.pformat(sorted(韵字典), compact=True))
        return 韵字典[name]

    def __判断韵书字典(self, d):
        if self.韵 == "現代韻書":
            if isinstance(d, dict):
                if len(d) != 36:
                    raise 输入不合法(d, "输入字典长度必须为36。")
                return d
            elif d in ["中华通韵", "中華通韻", "0", 0]:
                return "中华通韵"
            elif d in ["中华新韵", "中華新韻", "1", 1]:
                return "中华新韵"
            else:
                raise 输入不合法(d, pprint.pformat(["中华通韵", "中华新韵", "0", "1"], compact=True))
        return d

    def __获取注释(self, 类别, 韵书字典=None):
        self.yun_list = []
        last_chars = extract_chinese_characters(self.text)

        if self.韵 in ["廣韻", "平水韻"]:
            搜索类 = 繁體廣韻搜索 if self.韵 == "廣韻" else 繁體平水韻搜索
            for word in last_chars:
                result = 搜索类().返回(类别, word)
                self.yun_list.append(result if result else None)
        else:
            注音 = 现代韵书搜索(
                韵书字典=韵书字典,
                多音字=self.多音字, 自动分词=self.自动分词,
                连音变调=self.连音变调, 轻声=self.轻声,
                特殊声母=self.特殊声母,
                转换符=self.转换符, 转换前符=self.转换前符
            ).返回(类别, self.text)
            self.yun_list = [y if isinstance(y, list) and y else None for y in 注音]

    def __逐字标注(self) -> str:
        result = ""
        index = 0
        for line in self.text.splitlines():
            if not line.strip(): continue
            new_line = ""
            for ch in line:
                if is_chinese(ch):
                    y = self.yun_list[index]
                    phonetic = "None" if y is None else ",".join(map(str, y))
                    new_line += f"{ch}({phonetic})"
                    index += 1
                else:
                    new_line += ch
            result += new_line + "\n"
        return result.strip()

    def __末字标注(self, 类别, 韵书字典=None):
        self.__获取注释(类别, self.__判断韵书字典(韵书字典))
        result, idx = "", 0
        for line in self.text.splitlines():
            if not line.strip(): continue
            hanzi = [ch for ch in line if is_chinese(ch)]
            if not hanzi:
                result += line + "\n"
                continue
            idx += len(hanzi)
            y = self.yun_list[idx - 1]
            注音 = "None" if not y else self.间隔.join(map(str, y))
            last_char = hanzi[-1]
            pos = line.rfind(last_char)
            result += line[:pos] + f"{last_char}({注音})" + line[pos+1:] + "\n"
        return result.strip()

    def 古体(self, 韵书字典: dict | str = "中华通韵"):
        return self.__末字标注("韻部", 韵书字典)

    def 韵部(self, 韵书字典: dict | str = "中华通韵"):
        self.__获取注释("韻部", self.__判断韵书字典(韵书字典))
        return self.__逐字标注()

    def 韵目(self, 韵书字典: dict | str = "中华通韵"):
        self.__获取注释("韻目", self.__判断韵书字典(韵书字典))
        return self.__逐字标注()

    def 声调(self):
        self.__获取注释("聲調")
        return self.__逐字标注()

    def 平仄(self):
        self.__获取注释("平仄")
        return self.__逐字标注()
