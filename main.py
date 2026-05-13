from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import Plain, Image, Node, Nodes
import os


MENU_TEXT = """🪶 羽书功能菜单

━━━ 💬 日常对话 ━━━
直接 @羽书 或说「羽书」即可对话
• 支持上下文记忆、多轮聊天
• 自动记住你说过的话和喜好
• 联网搜索、知识问答

━━━ ✍️ AI 写作 ━━━
羽书 写作 [描述]
  → 一次性短篇生成
  例：羽书 写作 500字修仙短篇 主角被师兄陷害

羽书 开书 书名:xxx 题材:xxx
  → 创建长篇小说项目
  例：羽书 开书 书名:我的修仙日记 题材:修仙 基调:热血

羽书 续写 [书名]
  → 写下一章（返回引导模板）

羽书 引导 [书名]
  冲突:xxx 基调:xxx
  → 填写引导后触发生成

羽书 采纳 / 重写 / 修改 [意见]
  → 审阅草稿

羽书 大纲 [书名] → 生成大纲
羽书 我的书 → 查看书籍列表
羽书 进度 [书名] → 查看进度
羽书 导出 [书名] → 导出全文 txt

━━━ 🎨 图片生成 ━━━
羽书 画 [描述]
  → AI 生图（Gemini）
  例：羽书 画 赛博朋克风格的猫

羽书 改图 [描述]
  → 引用/发送图片 + 描述修改

━━━ 😺 表情包 ━━━
• 自动收集群聊表情包
• 对话时根据情绪自动发送
• 支持 LLM 智能选表情

━━━ 🧠 记忆 & 知识 ━━━
• 自动记住对话内容和用户画像
• 好感度系统（影响写作额度）
• 跨群记忆共享
• 内置《没钱修什么仙》知识图谱
  17000+ 实体 / 95000+ 关系
  角色、势力、功法、剧情随问随答

━━━ 📊 群分析 ━━━
羽书 群分析 [天数]
  → 生成群聊分析报告
  （管理员指令）

━━━━━━━━━━━━━━━━━
💡 所有指令前加「羽书」唤醒
💡 好感度越高，写作额度越多"""


@register("astrbot_plugin_yushu_menu", "vivy1024", "羽书功能菜单", "3.1.0")
class YushuMenuPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("菜单", alias=['帮助', '功能', '你怎么用', '你能干嘛'])
    async def show_menu(self, event: AstrMessageEvent):
        """显示羽书功能菜单"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        menu_dir = os.path.join(base_dir, "menu")

        nodes_list = []

        # 第一条：总览图（如果存在）
        overview_img = os.path.join(menu_dir, "overview.png")
        if not os.path.exists(overview_img):
            overview_img = os.path.join(menu_dir, "overview.jpg")
        if os.path.exists(overview_img):
            image = Image.fromFileSystem(overview_img)
            nodes_list.append(Node(name="羽书", content=[image]))

        # 第二条：文字菜单（按段落分割）
        sections = MENU_TEXT.strip().split("\n\n")
        for section in sections:
            nodes_list.append(Node(name="羽书", content=[Plain(section.strip())]))

        if nodes_list:
            nodes = Nodes(nodes=nodes_list)
            yield event.chain_result([nodes])
        else:
            yield event.plain_result(MENU_TEXT)
