from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper
import os


def generate_script(subject, video_length, creativity, api_key):
    # 1.获得视频标题
    # 1.1）定义提示模板
    title_template = ChatPromptTemplate.from_messages([("human", f"请为'{subject}'这个主题的视频想一个吸引人的标题")])
    script_template = ChatPromptTemplate.from_messages([("human", """
    你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
             要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             ```{wikipedia_search}```
    """)])

    # 1.2）定义模型
    model = ChatOpenAI(openai_api_key=api_key, temperature=creativity,base_url="https://api.aigc369.com/v1")

    # 1.3）定义title和script和链
    title_chain = title_template | model
    script_chain = script_template | model

    # 获得标题信息
    title = title_chain.invoke({"subject": subject}).content

    # 2.脚本信息需要用从维基百科中搜索到的信息，所以调用维基百科API，获得相关信息
    search = WikipediaAPIWrapper(lang="zh")
    search_result = search.run(subject)

    # 3.获得脚本内容
    script = script_chain.invoke({"title": title, "duration": video_length, "wikipedia_search": search_result}).content

    return search_result, title, script


#print(generate_script("sora模型", 1, 0.7, os.getenv("OPENAI_API_KEY")))
