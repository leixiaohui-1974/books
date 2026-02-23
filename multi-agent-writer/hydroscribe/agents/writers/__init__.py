"""
9 大写作智能体 — 对应 academic-writer-skill 的 9 种文体
"""
from hydroscribe.agents.writers.book_writer import BookWriterAgent
from hydroscribe.agents.writers.sci_writer import SCIWriterAgent
from hydroscribe.agents.writers.cn_writer import CNWriterAgent
from hydroscribe.agents.writers.patent_writer import PatentWriterAgent
from hydroscribe.agents.writers.report_writer import ReportWriterAgent
from hydroscribe.agents.writers.std_cn_writer import StdCNWriterAgent
from hydroscribe.agents.writers.std_int_writer import StdIntWriterAgent
from hydroscribe.agents.writers.wechat_writer import WeChatWriterAgent
from hydroscribe.agents.writers.ppt_writer import PPTWriterAgent

WRITER_REGISTRY = {
    "BK": BookWriterAgent,
    "SCI": SCIWriterAgent,
    "CN": CNWriterAgent,
    "PAT": PatentWriterAgent,
    "RPT": ReportWriterAgent,
    "STD-CN": StdCNWriterAgent,
    "STD-INT": StdIntWriterAgent,
    "WX": WeChatWriterAgent,
    "PPT": PPTWriterAgent,
}
