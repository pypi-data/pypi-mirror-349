import math
import numpy as np

from dataclasses import dataclass

@dataclass
class Position:
    x: float # m
    y: float # m
    z: float # m

@dataclass
class Orientation:
    roll: float # degrees
    pitch: float # degrees
    yaw: float # degrees

@dataclass
class LinearVelocity:
    u: float # m/s
    v: float # m/s
    w: float # m/s

@dataclass
class AngularVelocity:
    p: float # deg/s
    q: float # deg/s
    r: float # deg/s

@dataclass
class Velocity:
    u: float # m/s
    v: float # m/s
    w: float # m/s
    p: float # deg/s
    q: float # deg/s
    r: float # deg/s

@dataclass
class ForceCoefficients:
    x: Velocity
    y: Velocity
    z: Velocity
    k: Velocity
    m: Velocity
    n: Velocity

@dataclass
class State:
    position: Position
    orientation: Orientation
    linear_velocity: LinearVelocity
    angular_velocity: AngularVelocity
    voltage: float

@dataclass
class EnvironmentParams:
    gravity: float = 9.81 # m/s^2
    density: float = 1000 # kg/m^3

@dataclass
class PhysicalParams:
    mass: float # kg
    volume: float # m^3

    com: Position # Center of mass
    cob : Position # Center of buoyancy

    inertia: Position # Inertia tensor (Ixx, Iyy, Izz)
    projected_area: Position # Projected area in all 3 axes (m^2, m^2, m^2)

    drag: ForceCoefficients # Drag coefficients in all 6 degrees of freedom, subjected to const. velocities in each direction (36 values total)
    added_mass: ForceCoefficients # Added mass coefficients in all 6 degrees of freedom, subjected to const. acceleration in each direction (36 values total)

@dataclass
class ElectricalParams:
    voltage: float # V
    capacity: float # mAh

@dataclass
class ThrusterData:
    name: str
    pos: Position # Thruster position
    dir: Position # Thruster direction

@dataclass
class ThrusterParams:
    data: str
    list: list[ThrusterData]

@dataclass
class Params:
    name: str
    verbose: bool
    env: EnvironmentParams
    physical: PhysicalParams
    electrical: ElectricalParams
    thrusters: ThrusterParams

def body_to_world(state: np.ndarray) -> np.ndarray:
    """
        Convert body-fixed velocities to world frame.

        Input:
            state: State array containing orientation and body-fixed velocities.
        Output:
            world_velocities: World frame velocities.
    """
    # Unpack state
    roll, pitch, yaw = state[3], state[4], state[5]
    u, v, w = state[6], state[7], state[8]
    p, q, r = state[9], state[10], state[11]

    # Convert angles to radians
    roll, pitch, yaw = np.radians([roll, pitch, yaw])

    # Rotation matrix from body-fixed frame to world frame
    c_roll = math.cos(roll)
    c_pitch = math.cos(pitch)
    c_yaw = math.cos(yaw)
    s_roll = math.sin(roll)
    s_pitch = math.sin(pitch)
    s_yaw = math.sin(yaw)
    t_pitch = math.tan(pitch)
    r_trans = np.array([
        [c_yaw*c_pitch, -s_yaw*c_roll + c_yaw*s_pitch*s_roll, s_yaw*s_roll + c_yaw*s_pitch*c_roll],
        [s_yaw*c_pitch, c_yaw*c_roll + s_yaw*s_pitch*s_roll, -c_yaw*s_roll + s_yaw*s_pitch*c_roll],
        [-s_pitch, c_pitch*s_roll, c_pitch*c_roll]
    ])
    r_rot = np.array([
        [1, s_roll*t_pitch, c_roll*t_pitch],
        [0, c_roll, -s_roll],
        [0, s_roll/c_pitch, c_roll/c_pitch]
    ])

    return r_trans, r_rot

def world_to_body(state: np.ndarray) -> np.ndarray:
    """
        Returns rotation matrix to convert from world frame to body-fixed frame.

        Input:
            state: State array containing orientation and world frame velocities.
        Output:
            r_trans: Rotation matrix for translation.
            r_rot: Rotation matrix for rotation.
    """
    # Unpack state
    roll, pitch, yaw = state[3], state[4], state[5]
    u, v, w = state[6], state[7], state[8]
    p, q, r = state[9], state[10], state[11]

    # Convert angles to radians
    roll, pitch, yaw = np.radians([roll, pitch, yaw])

    # Rotation matrix from body-fixed frame to world frame
    c_roll = math.cos(roll)
    c_pitch = math.cos(pitch)
    c_yaw = math.cos(yaw)
    s_roll = math.sin(roll)
    s_pitch = math.sin(pitch)
    s_yaw = math.sin(yaw)
    t_pitch = math.tan(pitch)
    r_trans = np.array([
        [c_yaw*c_pitch, -s_yaw*c_roll + c_yaw*s_pitch*s_roll, s_yaw*s_roll + c_yaw*s_pitch*c_roll],
        [s_yaw*c_pitch, c_yaw*c_roll + s_yaw*s_pitch*s_roll, -c_yaw*s_roll + s_yaw*s_pitch*c_roll],
        [-s_pitch, c_pitch*s_roll, c_pitch*c_roll]
    ])
    r_rot = np.array([
        [1, s_roll*t_pitch, c_roll*t_pitch],
        [0, c_roll, -s_roll],
        [0, s_roll/c_pitch, c_roll/c_pitch]
    ])

    # Inverse rotation matrix from world frame to body-fixed frame
    inv_r_trans = np.linalg.inv(r_trans)
    inv_r_rot = np.linalg.inv(r_rot)

    return inv_r_trans, inv_r_rot

def fix_angular_circularity(state: np.ndarray) -> np.ndarray:
    """
        Ensure that the angular velocities are within the range of -180 to 180 degrees.

        Input:
            state: State array containing orientation and angular velocities.
        Output:
            state: Updated state with fixed angular velocities.
    """
    state[3] = (state[3] + 180) % 360 - 180
    state[4] = (state[4] + 180) % 360 - 180
    state[5] = (state[5] + 180) % 360 - 180
    return state

def state_object_to_array(state: State) -> np.ndarray:
    """
        Convert a State object to a numpy array.

        Input:
            state: State object containing position, orientation, linear velocity, angular velocity, and voltage.
        Output:
            state_array: Numpy array representation of the state.
    """
    return np.array([
        state.position.x, state.position.y, state.position.z,
        state.orientation.roll, state.orientation.pitch, state.orientation.yaw,
        state.linear_velocity.u, state.linear_velocity.v, state.linear_velocity.w,
        state.angular_velocity.p, state.angular_velocity.q, state.angular_velocity.r,
        state.voltage
    ])

def state_array_to_object(state_array: np.ndarray) -> State:
    """
        Convert a numpy array to a State object.

        Input:
            state_array: Numpy array representation of the state.
        Output:
            state: State object containing position, orientation, linear velocity, angular velocity, and voltage.
    """
    return State(
        position=Position(state_array[0], state_array[1], state_array[2]),
        orientation=Orientation(state_array[3], state_array[4], state_array[5]),
        linear_velocity=LinearVelocity(state_array[6], state_array[7], state_array[8]),
        angular_velocity=AngularVelocity(state_array[9], state_array[10], state_array[11]),
        voltage=state_array[12]
    )

def unpack_state_object(state: State) -> tuple:
    """
        Unpack a State object into its components.

        Input:
            state: State object containing position, orientation, linear velocity, angular velocity, and voltage.
        Output:
            x, y, z: Position coordinates.
            roll, pitch, yaw: Orientation angles.
            u, v, w: Linear velocities.
            p, q, r: Angular velocities.
    """
    return (
        state.position.x,
        state.position.y,
        state.position.z,
        state.orientation.roll,
        state.orientation.pitch,
        state.orientation.yaw,
        state.linear_velocity.u,
        state.linear_velocity.v,
        state.linear_velocity.w,
        state.angular_velocity.p,
        state.angular_velocity.q,
        state.angular_velocity.r,
        state.voltage
    )
