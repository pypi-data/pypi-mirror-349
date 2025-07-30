import sys
import logging
from types import FrameType
from typing import Any, Dict, Optional
from datetime import datetime
import time

# ロガー設定 (フォーマッタなし、ハンドラは1つだけ)
logger = logging.getLogger('auto_logger')
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    logger.addHandler(handler)

# 各フレームの前回ローカル値を保持
_prev_locals: Dict[int, Dict[str, Any]] = {}


def banagher_links(frame: FrameType, event: str, arg: Optional[Any]) -> Any:
    ts = datetime.now().strftime('%H:%M:%S')
    fid = id(frame)

    if event == 'line':
        # 実行時
        logger.info(f"[{ts}]ユニコーーーーーーーーーーーーーーーーーーン！！！")
        time.sleep(0.05) 
        # 変数変更検出
        cur = frame.f_locals.copy()
        prev = _prev_locals.get(fid, {})
        for k, v in cur.items():
            if k not in prev or prev[k] != v:
                logger.info(f"[{ts}]うぉぉぉおおおおおおおおおおおおおおおお")
        _prev_locals[fid] = cur

    elif event == 'exception':
        # 例外発生時にファイル名と行番号を含めてログ
        exc_type, exc_value, exc_tb = arg
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
         logger.error(f"[{ts}] それでも！！")
        return banagher_links

    return banagher_links


def start():
    # 自動トレースを開始
    sys.settrace(banagher_links)