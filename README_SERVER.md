# EWVtuber Server

## 1.构建配置文件
### 1.1 新建input/qa文件夹，在qa文件夹内新建txt文件
### 1.2 txt文件内数据规范
例如：
人工构建回答 >> 
举例：# Q:你能做什么?
A:我能回答很多问题

AI回答（无需给出A:）:
举例：# Q:你能做什么？

只给答案让AI自动匹配问题：
举例：# A:我今天早上吃的包子。

注意：
每一组问答之间用"#"分隔
### 1.3 预处理face源视频
将人物说话视频放入input/resource/***.mp4

### 1.4 创建待机配置

新建input/standby/standby.txt
各条待机动画之间用"#"

## 2.将上述配置文件预处理
举例：# 
QID:100010
Q:你能做什么?
A:我能回答很多问题
预处理文件后保存至data/pretrain/***.txt

## 3.文本转语音
### 3.1 读取上述配置文件，文本转语音
### 3.2 得到语音文件后，需要重新编码，将采样率改为44100Hz(flv流媒体要求)
方法：
ffmpeg -i /Users/admin/Desktop/speech.mp3 -vn -ar 44100 -ac 2 -b:a 192k /Users/admin/Desktop/speech_1.mp3
### 3.3 转码后的语音文件
保存至data/audio/qid.mp3

## 4.生成数字人视频
读取预处理文件 data/pretrain/***.txt

遍历取出预处理文件中的问答QID

人物视频源：input/resource/***.mp4

## 5.将处理好的数据上传至本地知识库





    