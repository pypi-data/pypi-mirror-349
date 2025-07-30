import sys
import logging
from types import FrameType
from typing import Any, Dict, Optional

# logger 設定
logger = logging.getLogger('auto_logger')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%H:%M:%S')
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)

# 各フレームの前回ローカル値を保持
_prev_locals: Dict[int, Dict[str, Any]] = {}


def banagher_links(frame: FrameType, event: str, arg: Optional[Any]) -> Any:
    code = frame.f_code
    fid = id(frame)
    if event == 'line':
        # 実行時ログ
        logger.info(f"Executing {code.co_filename}:{frame.f_lineno}")
        # 編集(変数変更)検出
        cur_locals = frame.f_locals.copy()
        prev = _prev_locals.get(fid, {})
        for name, value in cur_locals.items():
            if name not in prev or prev[name] != value:
                logger.info(f"Variable changed: {name} = {value!r}")
        _prev_locals[fid] = cur_locals
    elif event == 'exception':
        exc_type, exc_value, exc_tb = arg
        logger.error(f"Exception at {code.co_filename}:{frame.f_lineno} - {exc_value}")
    return banagher_links


def start():
    """トレースを開始して自動ログを有効化"""
    sys.settrace(banagher_links)