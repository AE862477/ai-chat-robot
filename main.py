import streamlit as st
from utils import generate_script

# 通过streamlit构建前端网页

# streamlit启动命令：终端中输入，streamlit run main.py

st.title("视频脚本生成器")

with st.sidebar:
    openai_api_key = st.text_input("请输入openai api秘钥：",type = "password")
    st.markdown("[获取OpenAI API秘钥](https://platform.openai.com/account/api-keys)")

# 主题
subject = st.text_input("请输入视频的主题")
# 视频时长
video_length = st.number_input("请输入视频的大致时长（单位：分钟）",min_value=0.1,step=0.1)

# 创建性
creativity = st.slider("✨ 请输入视频脚本的创造力（数字小说明更严谨，数字大说明更多样）", min_value=0.0,

                   max_value=1.0, value=0.2, step=0.1)
# 提交按钮
submit = st.button("生成脚本")

# 如果用户提交但是没有提供秘钥，则给与提示，且后续什么都不用做了
if submit and not openai_api_key:
    st.info("请输入你的OPenAI API秘钥")
    # 执行到这后面的代码都不会执行
    st.stop()

if submit and not subject:
    st.info("请输入视频的主题")
    st.stop()

if submit and not video_length >= 0.1:
    st.info("视频长度需要大于等于0.1分钟")
    st.stop()

if submit:
    with st.spinner(("AI正在思考中，请稍等...")):
        # 只要下面的代码没有运行完，则网页上会一直有一个加载的效果反馈给用户
        search_result, title, script = generate_script(subject, video_length, creativity,openai_api_key)
    st.success("视频脚本已生成")

    st.subheader("🔥 标题：")
    st.write(title)
    st.subheader("📝 视频脚本：")
    st.write(script)
    with st.expander("维基百科搜索结果 👀"):
        st.info(search_result)
