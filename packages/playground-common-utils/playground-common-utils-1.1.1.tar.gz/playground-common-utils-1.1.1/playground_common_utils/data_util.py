from Utilities.logger import *

from datetime import datetime

# --- データ構造変換 ---

def convert_tuple_to_dict(row, columns):
    """
    タプルとカラムリストから辞書に変換する
    引数:
        row: tupleデータ
        columns: カラムリスト
    戻り値:
        dictionayデータ
    """
    return dict(zip(columns, row))


def convert_object_to_dict(obj, attrs):
    """
    オブジェクトの属性から辞書に変換する
    """
    return {attr: getattr(obj, attr, None) for attr in attrs}


# --- データ型変換 ---

def convert_str_to_date(date_str, fmt="%Y-%m-%d"):
    """
    文字列から日付(datetime.date)に変換する
    """
    return datetime.strptime(date_str, fmt).date()


def convert_date_to_str(date_obj, fmt="%Y-%m-%d"):
    """
    日付(datetime.date)を文字列に変換する
    """
    return date_obj.strftime(fmt)

def expand_list_in_nested_dict(data, key_path):
    """
    ネストされた辞書の中からリストを取り出す

    引数:
        data -- 辞書データ<dict>
        key_path -- キーのリスト（例: ["company", "employees"]）
    戻り値:
        要素ごとのリスト<list>
    """
    current = data
    for key in key_path:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            log(ICON["WARN"], f"無効なキー: {key}")
            return []

    if isinstance(current, list):
        return current
    else:
        log(ICON["WARN"], "最終的な値がリストではありません")
        return []

def expand_dict_in_nested_dict(data, key_path):
    """
    ネストされた辞書の中からさらに辞書を取り出す

    引数:
        data -- 辞書データ<dict>
        key_path -- キーのリスト（例: ["company", "info"]）
    戻り値:
        辞書データ<dict>
    """
    current = data
    for key in key_path:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            log(ICON["WARN"], f"無効なキー: {key}")
            return {}

    if isinstance(current, dict):
        return current
    else:
        log(ICON["WARN"], "最終的な値が辞書ではありません")
        return {}
