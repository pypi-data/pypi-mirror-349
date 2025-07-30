# fm_image_tagger

fm_image_taggerは、画像に対するキャプションやタグを管理するためのツールです。CLIを通じて、タグやキャプションの作成、編集、表示を行うことができます。

## 概要

- ディレクトリ内の画像に対して WD1.4 によるキャプションファイルを一括で作成します
- ローカルで動作している ollama と Vision LLM を利用したキャプションを作成できます
- 主に LoRA モデルを作成するときの学習データ作成時に使用します
- SmilingWolf 氏作成の wd-tagger のソースコードとモデルデータを使用しています
  - https://huggingface.co/spaces/SmilingWolf/wd-tagger/tree/main
  - これらモデルデータは初回起動時にダウンロードされます

### 注意事項

- WD1.4 tagger / wd-tagger では著名キャラクター名を表示する事ができますが、本ツールの目的には不必要なものなので削除しています

## インストール

以下の手順で fm_image_tagger をインストールしてください。

### pip を使用する場合

```bash
pip install fm_image_tagger
```

### uv を使用する場合(オススメ)

```bash
uv tool install fm_image_tagger
```

予め uv (astral-sh.uv) をインストールしておく必要があります。pip なり winget なりでインストールしておいてください。
python 仮想環境を作るので、python そのもののインストールが無くても uv だけで動くはずです。

### ソースコードからの起動

リポジトリをクローンした場合、インストール無しに uv を使って起動できます。

```bash
uv run fm_image_tagger <コマンド> [オプション]
```

## 使用方法

各種サブコマンドの使用で様々な操作を行うことができます。

- ディレクトリ下の全画像ファイルからタグファイルを作成 (LoRA作成用)
- ディレクトリ下の全画像ファイルに対し ollama の画像認識 LLM を使ったキャプションファイルを作成 (FLUX LoRA作成用)
- ディレクトリ下の全画像ファイルを連番にリネーム
- ディレクトリ下の全タグファイルからタグネームを集計して表示
- ディレクトリ下の全タグファイルに指定単語を追加、削除
- 指定した画像ファイル単体のタグやキャプションを表示

### ユースケース

#### SDXL LoRA 作成用にキャプションファイルを用意したい

1. 学習用画像を `./images` 内に用意
2. LoRA 用タグ作成を実行
`fm_image_tagger tagger ./Images`
3. 作成されたタグを確認
`fm_image_tagger total ./Images`
4. 生成されたタグのうち LoRA モデルに覚えさせたい特徴を表すタグを削除していく、キャラクター LoRA なら髪型や目の色などを徹底的に削除する、衣装は着せ替えしたい場合は残した方が良い
`fm_image_tagger remove blue_eyes ./Images`
5. 特徴ワードがなくなるまで 4. を繰り返す
6. モデルの特徴を集約させるトリガーワード(任意)を先頭に追加
`fm_image_tagger add -f my-original-lora-1 ./Images`


#### FLUX LoRA 作成用にキャプションファイルを用意したい

1. 学習用画像を `./images` 内に用意
2. LoRA 用キャプション作成を実行(`minicpm-v:latest` は任意の ollama model を指定する)
`fm_image_tagger caption minicpm-v:latest ./Images -l`
3. モデルの特徴を集約させるトリガーワード(任意)を先頭に追加
`fm_image_tagger add -f my-original-lora-1 ./Images`


### fm_image_tagger コマンドラインリファレンス

fm_image_taggerは、画像のタグ付け、キャプション生成、ファイル名変更などを行うためのツールです。`click`ライブラリを使用してコマンドラインインターフェースが構築されています。

#### 基本的な使い方:

`pip` もしくは `uv tool` でインストールしている場合、単体ツールとして起動できます。

```bash
fm_image_tagger <コマンド> [オプション]
```

インストールせずソースコードリポジトリから直接起動する場合は `uv run` を使います。

```bash
uv run fm_image_tagger <コマンド> [オプション]
```


#### コマンド一覧:

*   **`tagger`**: 画像ファイルにタグファイルを生成します。

    *   使い方:

        ```bash
        fm_image_tagger tagger <パス> [オプション]
        ```

    *   引数:

        *   `<パス>`: 画像ファイルを含むディレクトリのパス。

    *   オプション:

        *   `-t`, `--threshold`: スコアの閾値 (デフォルト: 0.35)。例: `-t 0.5`

*   **`caption`**: Ollama vision-modelを使用してキャプションファイルを生成します。

    *   使い方:

        ```bash
        fm_image_tagger caption <ollama-vision-model> <パス> [オプション]
        ```

    *   引数:

        *   `<ollama-vision-model>`: 使用するOllama visionモデルの名前。
        *   `<パス>`: 画像ファイルを含むディレクトリのパス。

    *   オプション:

        *   `-l`, `--for-lora`: LoRAキャプションモードを有効にします。

*   **`rename`**: ファイルに連番でリネームします。

    *   使い方:

        ```bash
        fm_image_tagger rename <サフィックス> <パス>
        ```

    *   引数:

        *   `<サフィックス>`: ファイル名に付加するサフィックス。
        *   `<パス>`: ファイルを含むディレクトリのパス。

*   **`add`**: ディレクトリ内全てのタグファイルにキーワードを追加します。

    *   使い方:

        ```bash
        fm_image_tagger add <キーワード> <パス> [オプション]
        ```

    *   引数:

        *   `<キーワード>`: 追加するキーワード。
        *   `<パス>`: タグファイルを含むディレクトリのパス。

    *   オプション:

        *   `-f`, `--first`: タグの先頭にキーワードを追加します。

*   **`remove`**: ディレクトリ内全てのタグファイルからキーワードを削除します。

    *   使い方:

        ```bash
        fm_image_tagger remove <キーワード1> [<キーワード2> ...] <パス>
        ```

    *   引数:

        *   `<キーワード1> [<キーワード2> ...]`: 削除する1つ以上のキーワード。スペースで区切って複数指定できます。
        *   `<パス>`: タグファイルを含むディレクトリのパス。

*   **`total`**: ディレクトリ内全てのタグファイルを集計して全タグと使用数を集計します。

    *   使い方:

        ```bash
        fm_image_tagger total <パス>
        ```

    *   引数:

        *   `<パス>`: タグファイルを含むディレクトリのパス。

*   **`display`**: 画像情報を表示します。

    *   使い方:

        ```bash
        fm_image_tagger display <パス> [オプション]
        ```

    *   引数:

        *   `<パス>`: 画像ファイルのパス。

    *   オプション:

        *   `-m`, `--meta`: メタ情報（プロンプトなど）を表示します。
        *   `-t`, `--threshold`: スコアの閾値 (デフォルト: 0.35)。
        *   `-c`, `--caption-model`: Ollamaモデルを指定した場合、キャプションを表示します。
        *   `-l`, `--for-lora`: LoRA向けのキャプション出力を有効にします。(キャプション表示時 `-c` との併用時のみ有効)

**例:**

- `fm_image_tagger tagger images/`: `images/`ディレクトリ内の画像にタグファイルを生成します。
- `fm_image_tagger caption llama2-vision images/`: `images/`ディレクトリ内の画像にllama2-visionモデルを使用してキャプションファイルを生成します。
- `fm_image_tagger rename photo images/`: `images/`ディレクトリ内のファイル名を`photo_0001.jpg`のようにリネームします。
- `fm_image_tagger add beautiful images/`: `images/`ディレクトリ内のタグファイルに`beautiful`というキーワードを追加します。
- `fm_image_tagger display image.png -m`: `image.png` のメタ情報に含まれている A1111 形式のプロンプト情報を表示します。
- `fm_image_tagger display image.png -c minicpm-v:latest`: `image.jpg`のキャプションを minicpm-v モデルで生成し表示します。


## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 更新履歴

- Jan.05.2025 - v0.4.0
  - ファーストリリース

## 作者

rerofumi
