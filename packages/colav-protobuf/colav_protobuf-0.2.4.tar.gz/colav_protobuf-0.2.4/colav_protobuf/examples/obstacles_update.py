from colav_protobuf import ObstaclesUpdate
import random
from typing import List
import numpy as np
from enum import Enum
from shapely.geometry import Polygon

mock_agent_x = 3_675_830.74
mock_agent_y = -272_412.13
mock_agent_z = 4_181_577.70


class DynamicObstacleTypeEnum(Enum):
    UNSPECIFIED = ObstaclesUpdate.DynamicObstacleType.DYNAMIC_UNSPECIFIED
    VESSEL = ObstaclesUpdate.DynamicObstacleType.VESSEL


class StaticObstacleTypeEnum(Enum):
    STATIC_UNSPECIFIED = ObstaclesUpdate.StaticObstacleType.STATIC_UNSPECIFIED
    BUOY = ObstaclesUpdate.StaticObstacleType.BUOY
    LAND_MASS = ObstaclesUpdate.StaticObstacleType.LAND_MASS


def _mock_dynamic_obstacles(
    agent_position: List[float],
    obstacles_update: ObstaclesUpdate,
    detection_range: float = 1000,
    num_dynamic_obstacles: int = 5,
) -> ObstaclesUpdate:
    """Mocks dynamic obstacles in the obstacle update"""
    obstacle_class = "DYNAMIC_OBSTACLE"

    # Ensure the list has enough elements before accessing indices
    for _ in range(num_dynamic_obstacles):
        obstacles_update.dynamic_obstacles.add()

    for x in range(num_dynamic_obstacles):
        obstacle_type = ObstaclesUpdate.DynamicObstacleType.VESSEL
        obstacles_update.dynamic_obstacles[x].tag = (
            f"{obstacle_class}_{obstacle_type}_{x}"
        )
        obstacles_update.dynamic_obstacles[x].type = obstacle_type

        p = _random_position(position=agent_position, range=detection_range)
        obstacles_update.dynamic_obstacles[x].state.pose.position.x = float(p[0])
        obstacles_update.dynamic_obstacles[x].state.pose.position.y = float(p[1])
        obstacles_update.dynamic_obstacles[x].state.pose.position.z = float(p[2])

        q = _random_quaternion()
        obstacles_update.dynamic_obstacles[x].state.pose.orientation.x = float(q[0])
        obstacles_update.dynamic_obstacles[x].state.pose.orientation.y = float(q[1])
        obstacles_update.dynamic_obstacles[x].state.pose.orientation.z = float(q[2])
        obstacles_update.dynamic_obstacles[x].state.pose.orientation.w = float(q[3])

        obstacles_update.dynamic_obstacles[x].state.velocity = random.uniform(2, 30)
        obstacles_update.dynamic_obstacles[x].state.yaw_rate = random.uniform(-2, 2)

        obstacles_update.dynamic_obstacles[x].geometry.safety_radius = float(
            random.uniform(1.2, 5)
        )
        obstacles_update.dynamic_obstacles[x].geometry.loa = float(5)
        obstacles_update.dynamic_obstacles[x].geometry.beam = float(2.5)

    return obstacles_update


def _mock_static_obstacles(
    agent_position: List[float],
    obstacles_update: ObstaclesUpdate,
    num_static_obstacles: int = 5,
    detection_range: float = 1000,
) -> ObstaclesUpdate:
    """mocks static obstacle sin teh obstacle update"""
    obstacle_class = "STATIC_OBSTACLE"
    for _ in range(num_static_obstacles):
        obstacles_update.static_obstacles.add()
    for x in range(0, num_static_obstacles):
        obstacle_type = ObstaclesUpdate.StaticObstacleType.BUOY
        obstacles_update.static_obstacles[x].tag = (
            f"{obstacle_class}_{obstacle_type}_{x}"
        )
        
        obstacles_update.static_obstacles[x].type = obstacle_type
        
        p = _random_position(position=agent_position, range=detection_range)
        obstacles_update.static_obstacles[x].pose.position.x = float(p[0])
        obstacles_update.static_obstacles[x].pose.position.x = float(p[1])
        obstacles_update.static_obstacles[x].pose.position.x = float(p[2])

        q = _random_quaternion()
        obstacles_update.static_obstacles[x].pose.orientation.x = float(q[0])
        obstacles_update.static_obstacles[x].pose.orientation.y = float(q[1])
        obstacles_update.static_obstacles[x].pose.orientation.z = float(q[2])
        obstacles_update.static_obstacles[x].pose.orientation.w = float(q[3])

        obstacles_update.static_obstacles[x].geometry.inflation_radius = float(
            random.uniform(1.2, 5)
        )

    return obstacles_update


def _random_polyshape(min_vertices: int = 3, max_vertices: int = 15):
    """Generate a random 2D polyshape with a random number of vertices."""
    # Random number of vertices between min and max
    num_vertices = random.randint(min_vertices, max_vertices)

    # Generate random points (x, y) within a given range
    points = []
    for _ in range(num_vertices):
        x = random.uniform(-100, 100)  # Adjust the range as needed
        y = random.uniform(-100, 100)
        points.append((x, y))

    # Create a polygon using Shapely to check validity
    polygon = Polygon(points)

    # Ensure the points form a valid, non-self-intersecting polygon
    if not polygon.is_valid or polygon.is_empty:
        return _random_polyshape(
            min_vertices, max_vertices
        )  # Recursively regenerate if invalid

    # Return the vertices as a list of points
    return np.array(polygon.exterior.xy).T


def _random_position(position: List[float], range: float) -> List[float]:
    """returns an obstacle random position based within the detection_range of a mock agent vessel"""
    try:
        return [
            float(random.uniform(position[0] - range, position[0] + range)),
            float(random.uniform(position[1] - range, position[1] + range)),
            float(random.uniform(position[2] - range, position[2] + range)),
        ]
    except Exception as e:
        raise e


def _random_quaternion():
    """Generate a random unit quaternion."""
    q = np.random.normal(0, 1, 4)  # Random values from normal distribution
    q /= np.linalg.norm(q)  # Normalize to make it a unit quaternion
    return q


obstacles_update = ObstaclesUpdate()
obstacles_update.mission_tag = "COLAV_MISSION_NORTH_BELFAST_TO_SOUTH_FRANCE"
obstacles_update.stamp.sec = int(101203120)
obstacles_update.stamp.nanosec = int(1001230124)

obstacles_update = _mock_dynamic_obstacles(
    agent_position=[mock_agent_x, mock_agent_y, mock_agent_z],
    obstacles_update=obstacles_update,
    num_dynamic_obstacles=int(random.uniform(int(1), int(5))),
)
obstacles_update = _mock_static_obstacles(
    agent_position=[mock_agent_x, mock_agent_y, mock_agent_z],
    obstacles_update=obstacles_update,
    num_static_obstacles=int(random.uniform(int(1), int(5))),
)
