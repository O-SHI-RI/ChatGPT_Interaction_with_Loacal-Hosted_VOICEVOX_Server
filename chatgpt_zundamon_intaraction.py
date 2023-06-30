import tkinter as tk
import openai
import json
import os
import requests
import wave
import winsound

# OpenAI APIのAPIキーを設定(環境変数に設定済みの場合はコメントアウトのままでOK)
#openai.api_key = os.environ["自分のAPIキーを入力"]


#テキストからずんだもんの音声ファイルの出力と再生する関数
def Zundamon(text):
    url = 'http://localhost:50021/audio_query' #クエリー生成用APIのリクエスト先
    url2 = 'http://localhost:50021/synthesis' #音声ファイル作成APIのリクエスト先

    params1 = (
        ('text', text),
        ('speaker', 1), #音声データとしてずんだもんを指定
    )

    #VoiceVOX用のクエリを取得
    response_zundamon = requests.post(
        url,
        params=params1
    )

    print(response_zundamon)

    #音声の出力の為のヘッダの設定
    headers = {
        'accept': 'audio/wav',
        'Content-Type': 'application/json',
    }

    #音声の出力の為のパラメータの設定
    params2 = (
        ('speaker', 1), #ずんだもんの誰を使うか調整
        ('enable_interrogative_upspeak', 'true'), #疑問文の調子を調整
    )

    #初回のAPIリクエスト時に取得した返答から必要データを抽出
    data = response_zundamon.json()

    #音声ファイルの出力の為のリクエスト
    response_zundamon_wav = requests.post(
        url2,
        headers=headers,
        params=params2,
        data=json.dumps(data),
    )

    print(response_zundamon_wav)

    # 実行ディレクトリにoutput.wavというファイル名で音声ファイルを保存
    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(response_zundamon_wav.content)
    wf.close()

    # winsoundで音声ファイルを再生
    winsound.PlaySound("./output.wav", winsound.SND_FILENAME)

# ChatGPTのAPIを使って読み合わせの原稿を作成する関数
def chatgpt_process(text):

    system_prompt_dir = "./system_prompt"

    system_prompt_file = os.listdir(system_prompt_dir)[0]
    system_prompt_file_path = os.path.join(system_prompt_dir, system_prompt_file)

    # system_promptディレクトリにあるシステムを読み込み
    with open(system_prompt_file_path, 'r', encoding="utf-8") as file:
        system_prompt = file.read()

        # ファイル内の各プロンプトに対してGPT-3を実行します
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301", 
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": text
                },
            ],
            # ChatGPTからの返答の揺らぎを調整
            temperature=0.0,
        )
            
    return response.choices[0].message.content

# ChatGPT実行"ボタンをクリックした時の処理
def execute_chatgpt():
    # テキストボックスに入力されたテキストを取得
    text = input_text.get("1.0", tk.END)
    # Chatgptの実行
    result_chatgpt = chatgpt_process(text)
    # 前回の出力結果を下部ウィジェットから削除
    output_text.delete("1.0", tk.END)
    # 下部ウィジェットに出力
    output_text.insert(tk.END, result_chatgpt)
    

# "ずんだもん"ボタンクリック時の処理
def execute_playzundamon():
    # ChatGPTからの出力を改めて取得
    material_zundamon = output_text.get("1.0", tk.END)
    # ずんだもんへの音声出力と再生
    Zundamon(material_zundamon)

# Create the main window
window = tk.Tk()
window.title("ChatGPT-Zundamon")

# Create the input frame and its text widget
input_frame = tk.Frame(window, borderwidth=2, relief="groove")
input_frame.pack(side="top", fill="both", expand=True)
input_text = tk.Text(input_frame)
input_text.pack(fill="both", expand=True)

# Create a button that will call the execute function when clicked
#button1 = tk.Button(window, text="ChatGPT実行", command=execute_chatgpt)
button1 = tk.Button(window, text="ChatGPT実行", command=execute_chatgpt)
button1.pack()

# Create the output frame and its text widget
output_frame = tk.Frame(window, borderwidth=2, relief="groove")
output_frame.pack(side="top", fill="both", expand=True)
output_text = tk.Text(output_frame)
output_text.pack(fill="both", expand=True)

button2 = tk.Button(window, text="ずんだもん", command=execute_playzundamon)
button2.pack()

# Start the main loop
window.mainloop()
