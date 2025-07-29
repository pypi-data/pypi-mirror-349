# playground_common_utils

Pythonで汎用的な**ファイル操作・ディレクトリ操作・ログ出力**を支援するライブラリです。

---

## 📦 主な機能

### 確認系
- `is_exist(path)` : パスの存在確認
- `is_file(path)` : ファイルか確認
- `is_dir(path)` : ディレクトリか確認

### 作成系
- `create_file(path)` : 空ファイル作成
- `create_dir(path)` : ディレクトリ作成

### 取得系
- `read_current_dir()` : カレントディレクトリ取得
- `read_file(path)` : ファイル内容取得
- `read_list_dir(path)` : ディレクトリ内一覧取得

### 更新系
- `overwrite_file(path, content)` : ファイルに上書き
- `append_file(path, content)` : ファイルに追記

### 削除系
- `delete_file(path)` : ファイル削除
- `delete_dir(path)` : ディレクトリ削除

### 操作系
- `copy_file(src_path, dst_path)` : ファイルコピー
- `move_file(src_path, dst_path)` : ファイル移動

---

## 🚀 インストール

インストールするには：

```bash
pip install playground-common-utils
```

## 🛠️ 使用例

``` python
ファイル作成・書き込み・削除
from playground_common_utils.files import *

# ファイル作成
create_file('sample.txt')

# ファイル上書き
overwrite_file('sample.txt', 'Hello World')

# ファイル削除
delete_file('sample.txt')
```

## ディレクトリ操作
``` python
from playground_common_utils.files import *

# ディレクトリ作成
create_dir('new_folder')

# ディレクトリ内一覧取得
items = read_list_dir('new_folder')

# ディレクトリ削除
delete_dir('new_folder')
```

## ⚙️ 対応バージョン

* Python 3.7以上

## 📄 ライセンス

MITライセンス

## 👤 作者情報

Author: Hiroki Umatani
Project URL: [Github](https://github.com/HirokiUmatani/playground_common_utils)

playground-common-utilsは、実業務に直結するファイル管理作業の効率化を目指して開発されました。
営業・開発・レポート作成などのプロジェクトを圧倒的スピードで推進するための基盤ライブラリです。