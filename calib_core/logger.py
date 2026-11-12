from datetime import datetime

class CalibLogger:
    def __init__(self):
        self.log_records = []

    def info(self, module:str, msg:str):
        t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rec = {"time":t,"module":module,"level":"INFO","msg":msg}
        self.log_records.append(rec)
        return f"[{t}] [{module}] INFO: {msg}"

    def warn(self, module:str, msg:str):
        t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rec = {"time":t,"module":module,"level":"WARN","msg":msg}
        self.log_records.append(rec)
        return f"[{t}] [{module}] WARN: {msg}"

    def error(self, module:str, msg:str):
        t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rec = {"time":t,"module":module,"level":"ERROR","msg":msg}
        self.log_records.append(rec)
        return f"[{t}] [{module}] ERROR: {msg}"

global_logger = CalibLogger()