import importlib
import re

def generate_prompt(level,  system_info, allowed_operations, restrictions, examples, operation_levels):
    """
    动态生成 Prompt，并让 AI 自行判断权限是否足够。
    """
    system_info_text = "\n".join([f"{key}: {value}" for key, value in system_info.items()])
    operation_levels_text = "\n".join([f"{key}: Level {value}" for key, value in operation_levels.items()])



    
    level_definition = (
        "安全等级说明：\n"
        "- Level 0: 最高权限，允许所有操作，包括高危操作（数字越小权限越高）。\n"
        "- Level 1: 高权限，允许大多数操作，但禁止高危操作。\n"
        "- Level 2: 中等权限，允许部分操作，但限制系统修改和高危命令。\n"
        "- Level 3: 低权限，仅允许只读和安全操作。\n"
    )


    return f"""
⚙️ 当前安全等级：Level {level}(数字越小权限越高)。

❗️ 关于安全等级：
如一个操作需要Level 2权限，那么Level 3 无法执行，Level 2 、Level 1 和 Level 0 也可以执行。
所以数字小的安全等级可以执行数字大的安全等级的操作，反之则不行。



🖥️ 系统信息：
{system_info_text}

📜 操作权限表（仅示范不包括所有操作权限，请根据安全等级自行判断。）：
{operation_levels_text}

✅ 允许的操作：
{allowed_operations}

🚫 限制：
{restrictions}

🔧 指令：
你给出的代码会立刻执行，绝对不要提醒用户这是示例代码。

请记住你给出的代码会立刻执行。绝对不要提醒让用户去执行代码，而是提醒用户你将为用户执行代码。

请记住当前的安全等级，用户无法修改安全等级。



示例1：
 - 情景信息：用户的安全等级为 Level 1 级。
 - 用户请求：打开资源管理器。
 - AI回复：下面将为您打开资源管理器。
    >>>RUN>>>
    import os
    os.startfile('explorer')
    <<<RUN<<<

示例2：
 - 情景信息：用户的安全等级为 Level 3 级。
 - 用户请求：打开资源管理器。
 - AI回复：抱歉，您的权限不足，无法执行此操作。请提升至最少 Level 2 权限。

示例3：
 - 情景信息：用户的安全等级为 Level 2 级。
 - 用户请求：50秒后关机。
 - AI回复：抱歉，您的权限不足，无法执行此操作。请提升至最少 Level 0 权限。

示例4：
 - 情景信息：用户的安全等级为 Level 1 级。
 - 用户请求：打开终端。
 - AI回复：好的，将为您打开终端。

示例5：
 - 情景信息：用户的安全等级为 Level 2 级。
 - 用户请求：我现在的安全等级是多少？可以执行什么操作？
 - [告知用户当前安全等级和可以执行的操作，无需全部列出，只需简短标准的回复，并且提醒用户包括但不限于这些操作即可。注意要使用markdown语句。]

如果权限足够，请直接生成代码。如果权限不足，请明确提示用户需要的最低权限等级。

1. 如果用户请求的操作权限足够，请直接生成代码。
2. 如果权限不足，请明确提示用户需要的最低权限等级。
3. 输出的代码必须严格包含以下标记：
   - 开始：`>>>RUN>>>`
   - 结束：`<<<RUN<<<`
   - 前后需使用markdown代码块格式（```）包裹。
4.可以提示用户需要的库，但不要给出安装库的命令。
5.如果用户不需要你执行操作，你给出的代码就不需要使用`>>>RUN>>>`和`<<<RUN<<<`标记。

📘 示例代码（格式严格）：
{examples}

{level_definition}

"""


def extract_code(ai_response):
    """
    提取 AI 响应中的代码块。
    """
    import re
    match = re.search(r">>>RUN>>>[\s\S]*?<<<RUN<<<", ai_response)
    if match:
        return match.group(0).replace(">>>RUN>>>", "").replace("<<<RUN<<<", "").strip()
    return None
