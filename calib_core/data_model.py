from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CalibTask:
    """校准任务总记录"""
    task_id: str
    system_type: str  # TEM / GTEM / ANECHOIC / MAG_AC
    run_id: str
    create_time: str

@dataclass
class CalibPoint:
    """单条测量点，文档统一字段"""
    point_id: str
    task_id: str
    timestamp: str
    step_name: str
    status: str # pending / ok / abort / error

    # 设定量
    frequency_hz: Optional[float] = None
    source_amplitude: Optional[float] = None
    current_a: Optional[float] = None
    angle_deg: Optional[float] = None
    dwell_s: Optional[float] = None
    range_setting: Optional[str] = None

    # 仪器读数
    power_value: Optional[float] = None
    power_unit: Optional[str] = None
    voltage_value: Optional[float] = None
    reference_field: Optional[float] = None
    eut_field: Optional[float] = None
    eut_unit: Optional[str] = None

    # 计算结果
    standard_field: Optional[float] = None
    calibration_factor: Optional[float] = None
    isotropy_value: Optional[float] = None
    u_c: Optional[float] = None
    U: Optional[float] = None
    coverage_factor: float = 2.0

    # OCR质量
    ocr_text: Optional[str] = None
    ocr_confidence: Optional[float] = None
    frame_path: Optional[str] = None
    review_status: str = "auto"

    #溯源
    device_id: Optional[str] = None
    config_version: Optional[str] = None

def gen_task_id()->str:
    return f"TASK_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def gen_point_id()->str:
    return f"PT_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]}"