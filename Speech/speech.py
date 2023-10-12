import pyttsx3
import io
import sys
 
engine = pyttsx3.init()
 
# 获取语音包
voices = engine.getProperty('voices')
for voice in voices:
    print ('id = {}\tname = {} \n'.format(voice.id, voice.name))
# 设置使用的语音包
engine.setProperty('voice', 'zh') #开启支持中文
# engine.setProperty('voice', voices[0].id)
 
# 改变语速  范围为0-200   默认值为200
rate = engine.getProperty('rate')  #获取当前语速
engine.setProperty('rate', rate-40)
 
# 设置音量  范围为0.0-1.0  默认值为1.0
engine.setProperty('volume', 0.7)
 
# 预设要朗读的文本数据
line = "东部战区新闻发言人施毅陆军大校表示，10月12日，美1架P-8A反潜巡逻机过航台湾海峡并公开炒作。中国人民解放军东部战区组织战机对美机过航行动跟监警戒，依法依规处置。战区部队时刻保持高度戒备，坚决捍卫国家主权安全和地区和平稳定。" #要播报的内容
# engine.say(line)

engine.save_to_file(line, 'Buffer\\Audio\\speech.wav')
 
# 朗读
engine.runAndWait()