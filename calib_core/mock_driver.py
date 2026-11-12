import random
from calib_core.logger import global_logger

class MockSigGen:
    """模拟信号源"""
    def __init__(self):
        self.connected = False
        self.freq = 0.0
        self.amp = 0.0
        self.output_enable = False

    def connect(self):
        self.connected = True
        global_logger.info("MockSigGen","模拟信号源已连接")
        return True

    def close(self):
        self.output_enable = False
        self.connected = False

    def set_frequency(self, hz:float):
        if not self.connected: raise Exception("设备未连接")
        self.freq = hz

    def set_amplitude(self, amp:float):
        if not self.connected: raise Exception("设备未连接")
        self.amp = amp

    def output_on(self): self.output_enable=True
    def output_off(self): self.output_enable=False

    def read_sim_value(self)->float:
        """模拟输出读数，带噪声"""
        noise = random.uniform(-0.04,0.04)
        return self.amp*(1.0+noise)


class MockPowerMeter:
    """模拟功率计"""
    def __init__(self):
        self.connected=False

    def connect(self):
        self.connected=True
        global_logger.info("MockPowerMeter","模拟功率计已连接")
        return True

    def close(self): self.connected=False
    def set_range(self, rng:str): pass
    def read(self, base_amp:float)->float:
        noise = random.uniform(-0.03,0.03)
        return base_amp*(1+noise)


class MockRotStage:
    """模拟旋转台"""
    def __init__(self):
        self.connected=False
        self.angle=0.0

    def connect(self):
        self.connected=True
        global_logger.info("MockRotStage","模拟旋转台已连接")
        return True

    def close(self): self.connected=False
    def move_to(self, deg:float):
        self.angle=deg

class MockDMM:
    """模拟数字电压表"""
    def __init__(self):
        self.connected=False
    def connect(self):
        self.connected=True
        global_logger.info("MockDMM","模拟数字电压表已连接")
        return True
    def close(self): self.connected=False
    def set_ac_mode(self): pass
    def read_voltage(self, base:float):
        noise = random.uniform(-0.025,0.025)
        return base*(1+noise)


#全局模拟设备实例
mock_siggen = MockSigGen()
mock_powermeter = MockPowerMeter()
mock_rot = MockRotStage()
mock_dmm = MockDMM()

def mock_device_all_connect():
    mock_siggen.connect()
    mock_powermeter.connect()
    mock_rot.connect()
    mock_dmm.connect()

def mock_device_all_disconnect():
    mock_siggen.close()
    mock_powermeter.close()
    mock_rot.close()
    mock_dmm.close()