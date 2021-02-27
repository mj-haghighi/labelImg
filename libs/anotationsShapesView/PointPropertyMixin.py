import enum

class PointViewType(enum.Enum):
    P_SQUARE=1
    P_ROUND=2


class PointPropertyMixin:
    point_type = PointViewType.P_ROUND
    point_size = 8
    