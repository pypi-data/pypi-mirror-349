import sys
import logging
from types import FrameType
from typing import Any, Dict, Optional
from datetime import datetime

logger = logging.getLogger('auto_logger')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%H:%M:%S')
handler.setFormatter(formatter)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(handler)

_prev_locals: Dict[int, Dict[str, Any]] = {}


def banagher_links(frame: FrameType, event: str, arg: Optional[Any]) -> Any:
    code = frame.f_code
    fid = id(frame)
    ts = datetime.now().strftime('%H:%M:%S')
    if event == 'line':
        # 実行時ログ
        logger.info(f"[{ts}]ユニコーーーーーーーーーーーーーーーーーーン！！！")
        # 編集(変数変更)変数変更検出
        cur_locals = frame.f_locals.copy()
        prev = _prev_locals.get(fid, {})
        for name, value in cur_locals.items():
            if name not in prev or prev[name] != value:
                logger.info(f"[{ts}]うぉぉぉおおおおおおおおおおおおおおおお")
        _prev_locals[fid] = cur_locals

    elif event == 'exception':
        exc_type, exc_value, exc_tb = arg
        logger.error(f"[{ts}] それでも！！")
    return _trace


def start():
    """トレースを開始して自動ログを有効化"""
    sys.settrace(_trace)