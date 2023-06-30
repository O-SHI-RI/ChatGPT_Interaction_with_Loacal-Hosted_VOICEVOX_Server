# ChatGPT+ローカルVOICEVOXサーバを使ったずんだもん音声出力
VOICEVOX起動時に自動で立ち上がるサーバにAPIを使って何やらやってみたので、その時のコードです。

## 環境

- OS : Windows
- Python : Python 3.10.11(実行確認環境)
- VOICEVOX(インストール版)
https://voicevox.hiroshiba.jp/


## 実行

- VOICEVOXのアプリを起動(起動時にHTTPサーバも立ち上がる。APIを使う為起動は必須)
- ChatGPTのAPIキーはコードに埋め込むか環境変数で事前で設定。
- ./system_promptフォルダのテキストにChatGPTのシステムプロンプトを入力。

```
python chatgpt_zundamon_intaraction.py
```

- コマンド実行後に2画面が表示
- 上部ウィンドウにChatGPTに処理をさせたい文章を記述
- "ChatGPT実行"ボタンにより処理が走り出力を結果が下部ウィンドウに表示

![実行時イメージ](/img/img1.png)

- "ずんだもん"ボタンにより、出力された文字列をずんだもんが朗読。
- 出力結果は"output.wav"として実行ディレクトリに保存されています。

## 留意事項

- あくまで個人で作ったもので、Windows11の自前の環境でしか動作を確認していません。
- 「なぜVOICEVOX APIを使ったか？」の問については、「APIを使いたかったから」です。どう考えても、VOICEVOX Core(https://github.com/VOICEVOX/voicevox_core) をコンパイルしてそれを実行した方が軽いですし楽です。