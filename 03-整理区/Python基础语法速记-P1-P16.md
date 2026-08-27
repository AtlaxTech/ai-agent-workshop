# Python 基础语法速记（P1–P16）

## 一句话结论

字面量描述代码中直接出现的值，变量把对象绑定到名称；Python 在运行时处理类型，基础输入必须通过实际运行和类型观察验证。

## 已确认内容

- 常见字面量：`int`、`float`、`str`、`bool` 和 `None`。
- 变量名绑定到对象；同一个名称之后可以绑定不同类型的对象，但工程代码仍应保持清晰稳定的类型预期。
- 字符串可使用单引号、双引号或三引号；三引号常用于多行文本和文档字符串。
- 字符串插值优先考虑 f-string；大量片段拼接通常使用 `str.join()`。字符串不可变，反复 `+` 可能产生额外对象，但不是“破坏字符串完整性”。
- 标识符区分大小写，不能以数字开头或使用关键字；普通变量与函数通常使用 `snake_case`。
- `bool` 在 Python 类型体系中是 `int` 的子类，但业务含义仍应作为真假值处理，不能因为可参与算术就混淆语义。

## 最小验证

实际脚本：[pre-course_prac.py](../02-每日笔记/Python基础/2026-08-27_14-51-49/pre-course_prac.py)

```python
age = 25
height = 1.75
message = "This is a String!"
is_student = True

print(type(age), type(height), type(message), type(is_student))
```

实际输出包含：

```text
<class 'int'> <class 'float'> <class 'str'> <class 'bool'>
```

## 与 AI Agent 工程的关联

- LLM API 请求和工具参数最终都要落到 Python 对象、JSON 数据与明确类型上。
- “模型返回了字符串”不代表字段类型、业务含义或协议已经正确，后续需要 Pydantic/JSON Schema 校验。
- 变量命名和稳定类型预期会直接影响 Agent 状态、工具输入和故障定位。

## 边界

- 本页只对应 2026-08-20 的 P1–P16 运行证据；课程后续已推进至 P88，见[课程跟踪](../00-路线与状态/Python+AI课程跟踪.md)。
- 原始笔记已经写到 list、tuple 和循环，但这些不自动代表对应课程章节已完成。
- 今天未验证函数、异常、模块、类型提示或 Python AI 调用。

## 来源

- [Day 0.5 学习记录（历史证据）](../02-每日笔记/Python基础/2026-08-27_15-55-36/Day-0.5-学习记录.md)
- [原始课程笔记](../02-每日笔记/Python基础/2026-08-27_14-51-49/pre-course_python-intro.md)
- [基础语法练习脚本](../02-每日笔记/Python基础/2026-08-27_14-51-49/pre-course_prac.py)
