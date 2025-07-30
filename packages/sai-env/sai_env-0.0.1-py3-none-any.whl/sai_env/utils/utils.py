from token import OP
from typing import Union
from pydantic import BaseModel, RootModel
from typing import List, Optional, Dict
import yaml

class CameraSpawn(BaseModel):
    focal_length: float
    focus_distance: float
    horizontal_aperture: float
    clipping_range: List[float]

class CameraOffset(BaseModel):
    pos: List[float]
    rot: List[float]
    convention: str

class IMUOffset(BaseModel):
    pos: List[float]
    rot: List[float]

class IsaacCamera(BaseModel):
    prim_path: str
    update_period: float
    height: int
    width: int
    data_types: List[str]
    spawn: CameraSpawn
    offset: CameraOffset

class IMU(BaseModel):
    prim_path: str
    update_period: int
    history_length: int
    debug_vis: bool
    offset: IMUOffset

class IsaacLabProps(BaseModel):
    camera: Dict[str, IsaacCamera]
    imu: Dict[str, IMU]

class MujocoProps(BaseModel):
    accelerometer: Optional[List[str]] = None
    velocimeter: Optional[List[str]] = None
    gyro: Optional[List[str]] = None
    force: Optional[List[str]] = None
    torque: Optional[List[str]] = None
    magnetometer: Optional[List[str]] = None
    framezaxis: Optional[List[str]] = None
    framexaxis: Optional[List[str]] = None
    framelinvel: Optional[List[str]] = None
    frameangvel: Optional[List[str]] = None
    framepos: Optional[List[str]] = None
    framequat: Optional[List[str]] = None
    camera: Optional[Dict[str, str]] = None

class SensorProperties(BaseModel):
    mujoco: Optional[MujocoProps] = None
    isaac_lab: Optional[IsaacLabProps] = None

class SensorConfig(BaseModel):
    name: str
    include_state: bool
    properties: SensorProperties

class GripperCommand(RootModel[Dict[str, float]]):
    pass

class GripperFingers(BaseModel):
    left: str
    right: str

class GripperConfig(BaseModel):
    fingers: Optional[GripperFingers] = None
    open_command: Optional[GripperCommand] = None
    close_command: Optional[GripperCommand] = None

class RobotConfig(BaseModel):
    name: str
    type: str
    robot_class: Optional[str] = None
    position: List[float]
    orientation: List[float]
    control_type: str  # Could be validated with literal type: Literal["joint_space", "task_space"]
    gripper: bool
    include_state: bool
    default_pose: List[float]
    init_ctr: List[float]
    properties: List[str]

    sim_dt: float

    hand_link: str
    target_name: Optional[str] = None
    base_link: str
    gripper_link: Optional[Union[str, List[str]]] = None
    left_finger: Optional[Union[str, List[str]]] = None
    right_finger: Optional[Union[str, List[str]]] = None
    arm_joints: Optional[List[str]] = None
    gripper_joints: Optional[List[str]] = None

    gripper: Optional[GripperConfig] = None

def load_yaml(yaml_file_path: str) -> dict:

    try:
        with open(yaml_file_path) as stream:
            return yaml.safe_load(stream)
    except Exception as e:
        raise FileNotFoundError(f"Environment configuration file not found at {yaml_file_path}")

def validate_sensor_config(config):
    """
    Checks if the configuration files are correct
    """

    try:
        validated_config = SensorConfig(**config).dict()
        return validated_config
    except Exception as e:
        raise e
    
def validate_robot_config(config):
    """
    Checks if the configuration files are correct
    """

    try:
        validated_config = RobotConfig(**config).dict()
        return validated_config
    except Exception as e:
        raise e
