"""This module defines the Detector elements."""

from typing import Any, Optional

from torch import Tensor
from torch.nn.functional import linear

from ..fields import Field
from ..type_defs import Scalar, Vector2
from ..utils import validate_tensor_ndim
from .elements import Element


class Detector(Element):
    r"""
    Detector element.

    Computes the power measured by the detector for each grid cell using the following equation:

    .. math::
        P_{i,j} = I_{i,j} \cdot \Delta A_{\text{cell}}

    where:
        - :math:`P_{i,j}` is the power measured in the grid cell at position :math:`(i, j)`,
        - :math:`I_{i,j}` is the intensity at position :math:`(i, j)`, and
        - :math:`\Delta A_{\text{cell}}` is the area of a single grid cell.

    Args:
        shape (Vector2): Number of grid points along the planar dimensions.
        z (Scalar): Position along the z-axis. Default: `0`.
        spacing (Optional[Vector2]): Distance between grid points along planar dimensions. Default: if
            `None`, uses a global default (see :meth:`torchoptics.set_default_spacing()`).
        offset (Optional[Vector2]): Center coordinates of the plane. Default: `(0, 0)`.
    """

    def forward(self, field: Field) -> Tensor:
        """
        Calculates the power per cell area.

        Args:
            field (Field): The input field.

        Returns:
            Tensor: The power per cell area.
        """
        self.validate_field(field)
        return field.intensity() * self.cell_area()


class LinearDetector(Element):
    r"""
    Linear detector element, conceptually similar to :class:`torch.nn.Linear`.

    Applies a spatially varying weight to the field intensity and integrates over the plane,
    producing a weighted sum for each output channel.

    The total weighted power measured by the detector is computed as:

    .. math::
        P_c = \sum_{i, j} w_{c, i, j} \cdot I_{i, j} \cdot \Delta A_{\text{cell}}

    where:
        - :math:`P_c` is the total weighted power measured by the detector for channel :math:`c`,
        - :math:`w_{c, i, j}` is the weight matrix for channel :math:`c`,
        - :math:`I_{i, j}` is the intensity at position :math:`(i, j)`, and
        - :math:`\Delta A_{\text{cell}}` is the area of a single grid cell.

    .. note::
        This equation in its integral form is expressed as:

        .. math::
            P_c = \int \int w_c(x, y) \cdot I(x, y) \, dx \, dy

    Args:
        weight (Tensor): Weight matrix of shape (C, H, W).
        z (Scalar): Position along the z-axis. Default: `0`.
        spacing (Optional[Vector2]): Distance between grid points along planar dimensions. Default: if
            `None`, uses a global default (see :meth:`torchoptics.set_default_spacing()`).
        offset (Optional[Vector2]): Center coordinates of the plane. Default: `(0, 0)`.
    """

    weight: Tensor

    def __init__(
        self,
        weight: Tensor,
        z: Scalar = 0,
        spacing: Optional[Vector2] = None,
        offset: Optional[Vector2] = None,
    ) -> None:
        validate_tensor_ndim(weight, "weight", 3)
        super().__init__(weight.shape[1:], z, spacing, offset)
        self.register_optics_property("weight", weight)

    def forward(self, field: Field) -> Tensor:
        """
        Calculates the weighted power.

        Args:
            field (Field): The input field.

        Returns:
            Tensor: The weighted power.
        """
        self.validate_field(field)
        intensity_flat, weight_flat = field.intensity().flatten(-2), self.weight.flatten(-2)
        return linear(intensity_flat, weight_flat) * self.cell_area()

    def visualize(self, *index: int, **kwargs) -> Any:
        """
        Visualizes the detector output or the weight matrix.

        Args:
            *index (int): The index of the channel to visualize.
            sum_weight (bool): Whether to plot the sum of the weight matrix. Default: `False`.
            **kwargs: Additional keyword arguments for visualization.
        """
        kwargs.update({"symbol": r"$\mathcal{W}_{" + str(index[-1]) + r"}$"})
        return self._visualize(self.weight, index, **kwargs)
