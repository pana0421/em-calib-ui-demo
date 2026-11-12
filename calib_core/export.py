import csv
from typing import List
from calib_core.data_model import CalibPoint

def export_points_to_csv(filepath:str, point_list:List[CalibPoint]):
    headers = [
        "point_id","task_id","timestamp","step_name","status",
        "frequency_hz","source_amplitude","current_a","angle_deg","dwell_s","range_setting",
        "power_value","power_unit","voltage_value","reference_field","eut_field","eut_unit",
        "standard_field","calibration_factor","isotropy_value","u_c","U","coverage_factor",
        "ocr_text","ocr_confidence","frame_path","review_status","device_id","config_version"
    ]
    with open(filepath,"w",newline="",encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f,fieldnames=headers)
        writer.writeheader()
        for p in point_list:
            d = p.__dict__
            writer.writerow(d)
    return filepath