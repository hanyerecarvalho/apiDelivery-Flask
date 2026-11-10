import os
import traceback
from datetime import datetime

class Logger:

    LOG_FILE = "api/system/log.log"

    @staticmethod
    def log_error(message: str):
        Logger._write_log("ERROR", message)

    @staticmethod
    def log(error: Exception):
        error_trace = ''.join(traceback.format_exception(type(error), error, error.__traceback__))

        Logger._write_log("ERROR", error_trace)


    @staticmethod
    def _write_log(log_type: str, message: str):
        directory_path = os.path.dirname(Logger.LOG_FILE)
        os.makedirs(directory_path, exist_ok=True)

        date_time = datetime.utcnow().isoformat()
        entry = f"[{date_time}] [{log_type}]\n{message}\n{'-'*80}\n"

        try:
            with open(Logger.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception as e:
            print("🔴 Falha ao gravar log:", e)