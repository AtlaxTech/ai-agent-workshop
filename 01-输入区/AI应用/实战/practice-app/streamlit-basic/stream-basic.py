import streamlit as st

# 设置页面配置项
st.set_page_config(
    page_title="Ex-stream-ly Cool App",  # 标签页标题
    page_icon="🧊",  # 标签页图标
    # 控制整个网页布局
    # wide 表示使用整个网页的宽度
    # centered：表示只占用网页中间部分
    # None：The page layout is inherited from the previous call of st.set_page_config.
    # If no previous call exists, the page layout is "centered".
    layout="wide",
    # 控制侧边栏状体啊
    initial_sidebar_state="expanded",
    # 右上角菜单信息
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# 这是一个 streamlit 的入门页面！"
    }
)


st.title("Streamlit 入门演示")
st.header("Streamlit 一级标题")
st.subheader("Streamlit 二级标题")

# 段落文字 st.write
st.write(
    "起司猫是温暖的橘色毛团，脊背上那抹最正的橘色延伸到尾巴尖，像被阳光浸透的琥珀。它最特别的是背部那块完美的白色标记，仿佛穿着合身的小西装。四肢短小结实，走动时像橘色糯米团子在地上滚动，尾巴尖总打着优雅的卷儿。")
st.write(
    "那双杏仁状的大眼睛里盛着警惕与好奇，听见冰箱门响会竖起飞机耳，闻到罐头香气又立刻放松成蜜糖色的圆月。它最爱趴在窗台看麻雀，尾巴尖微微颤动时，后腿肌肉在光滑的皮毛下轻轻起伏——那是被驯化千年的猎手基因在苏醒的痕迹。")
st.write(
    "当它蜷在膝头打呼噜，你能摸到脊背流畅的曲线，像抚摸一匹缩小的丝绸。作为公认的贪吃鬼，它总在开饭前用脑袋蹭你的手背，软乎乎的肉垫按在手腕上，像在按一枚温柔的印章。但若是摸到它圆鼓鼓的肚子超过三秒，这位橘色绅士就会礼貌地递来一记“无影掌”，随即又用湿润的鼻尖碰碰你的手指，仿佛在说：“朕宽恕你的冒犯。”")
st.write(
    "它把整个星空穿在身上——安静时是流淌的蜜，跑动时是跃动的火，而当你深夜回家，总能在玄关看见那团蜷成蜗牛壳形状的橘色身影，用均匀的呼噜声告诉你：“欢迎回家，我的两脚兽。”这就是起司猫，把整个秋天的温暖都收进绒毛里，再一口一口还给爱它的人。")

# 图片 st.image
st.image("./resource/2C31C575-ACA4-4608-B466-833E77D55333_1_105_c.jpeg")

# 音频
st.audio("./resource/voiceover.wav")

# 视频
st.video("./resource/ScreenRecording_03-07-2026 11-09-21_1.mov")

# logo
st.logo("./resource/Blossom_4k_Icon_1.webp")

# 表格
student_data = {
    "name": ["Kevin", "Mary", "Jack", "Alex"],
    "student ID": ["12345", "67890", "23423", "2342534"],
    "English Score": ["23", "43", "78", "76"],
    "Math Score": ["35", "34", "23", "88"],
    "Computer Score": ["99", "98", "87", "76"],
    "total Score": ["324", "234", "345", "324"]
}
st.table(student_data)

# 输入框
name = st.text_input("Please input your name")
st.write(f"your name is: {name}")

password = st.text_input("Please input your password", type="password")
st.write(f"your password is: {password}")

# 单选按钮
sex = st.radio("请输入你的性别", ["Male", "Female", "Unknown"], index=2)
st.write(f"你的性别是：{sex}")
