from enum import Enum

class GatewayMode(str, Enum):
    SIMULATION = "simulation"
    PRODUCTION = "production"

class RoutingStrategy(str, Enum):
    PRIORITY = "priority"
    ROUND_ROBIN = "round_robin"
    RANDOM = "random"
    WEIGHTED = "weighted"
