import random
from calib_core.logger import global_logger

class MockOcr:
    def __init__(self):
        pass

    def capture_frame(self):
        """模拟抓拍图像"""
        return {"frame_path":"mock/img001.png"}

    def recognize(self, true_val:float):
        """模拟OCR识别，加入小识别噪声"""
        noise = random.uniform(-0.025, 0.025)
        out_val = true_val*(1.0+noise)
        conf = random.uniform(0.88,0.985)
        return {
            "ocr_text":f"{out_val:.3f}",
            "value":round(out_val,3),
            "unit":"V/m",
            "ocr_confidence":round(conf,3)
        }

mock_ocr = MockOcr()