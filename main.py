from pycorrector.macbert.macbert_corrector import MacBertCorrector
import whisper
import opencc
import os
import random

mac_bert_correct = MacBertCorrector("shibing624/macbert4csc-base-chinese").macbert_correct


def random_file(base_dir: str) -> str:
    """
    随机一个音频（基于create_audio*.py）
    参数：
        base_dir：包含音频文件和对应文本的目录
    返回值：音频文件路径
    """
    mp3_files = [file for file in os.listdir(base_dir) if file.endswith("mp3")]
    txt_files = [file for file in os.listdir(base_dir) if file.endswith("txt")]

    # 随机一个mp3文件及其对应的文本
    random_mp3 = random.choice(mp3_files)
    random_txt = txt_files[txt_files.index("".join(random_mp3.split(".")[:-1]) + ".txt")]
    with open(os.path.join(base_dir, random_txt), "r", encoding="u8") as f:
        random_message = f.read()
    print("原始数据：", random_message, "\n")
    return os.path.join(base_dir, random_mp3)


def random_file_by_dataset(base_dir: str) -> str:
    """
    随机读取语音及其文本（基于数据集）
    参数：
        base_dir：包含语音和文本的目录
    返回值：语音文件路径
    """
    label_txt = [os.path.join(base_dir, audios_dir) for audios_dir in os.listdir(base_dir) if audios_dir.endswith("txt")][0]    
    with open(label_txt, "r", encoding="u8") as f:
        audio_info_list = f.readlines()[1:]
    audio_info = random.choice(audio_info_list).split("\t")    
    audio_dir = audio_info[1]
    audio_name = audio_info[0]
    audio_text = audio_info[2]
    audio_path = os.path.join(base_dir, audio_dir, audio_name)
    print(f"音频文件：{audio_name}，原始数据：", audio_text)
    return audio_path


def asr(audio_file_path: str) -> str:
    """
    语音识别
    参数：
        audio_file_path：语音文件路径
    返回值：识别结果
    """
    # 加载模型
    model = whisper.load_model("./models/large-v2.pt")
    # 加载音频
    result = model.transcribe(audio_file_path, language="zh")
    # 结果文本
    result_text = result.get("text")
    # 转换繁体字为简体字
    converter = opencc.OpenCC("t2s")   
    simple_result_text = converter.convert(result_text)  
    return simple_result_text


def text_correction(text: str) -> str:
    """
    文本纠错
    参数：
        text：原始文本
    返回值：纠错后的文本
    """
    corrected_sent = mac_bert_correct(text)
    return corrected_sent[0]


if __name__ == "__main__":
    # 随机读取一条语音及其原始文本方式一
    # audios_dir = "./audios"
    # random_audio_path = random_file(audios_dir)    

    # 随机读取一条语音及其原始文本方式二
    base_dir = "./wav_dataset"
    random_audio_path = random_file_by_dataset("./wav_dataset")

    # 识别
    result = asr(random_audio_path)
    print("识别结果：", result)
    text = text_correction(result)
    print("纠错结果：", text)