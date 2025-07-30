import numpy as np
import numpy.typing as npt
from typing import Union, List, Tuple, Annotated, Literal, TypeVar

np.float_ = np.float64  # for numpy 2 compatibility
intIterable = Union[List[int], Tuple[int], npt.NDArray[np.int_]]
floatIterable = Union[List[float], Tuple[float], npt.NDArray[np.float_]]
DType = TypeVar("DType", bound=np.generic)
Array3x3 = Annotated[npt.NDArray[DType], Literal[3, 3]]


def rotMat(axis: int, angle: float) -> npt.NDArray[np.float_]:
    r"""Returns the DCM :math:`{}^\mathcal{B}C^\mathcal{A}` for a rotation of the given
    angle about the specified axis of frame :math:`\mathcal{A}`

    Args:
        axis (int):
            Body axis to rotate about (1, 2, or 3 only)
        angle (float):
            Angle of rotation

    Returns:
        numpy.ndarray:
            3x3 rotation matrix

    """

    assert axis in [1, 2, 3], "Axis must be one of 1, 2, or 3, only."

    if axis == 1:
        out = np.array(
            (
                [1, 0, 0],
                [0, np.cos(angle), np.sin(angle)],
                [0, -np.sin(angle), np.cos(angle)],
            )
        )
    elif axis == 2:
        out = np.array(
            (
                [np.cos(angle), 0, -np.sin(angle)],
                [0, 1, 0],
                [np.sin(angle), 0, np.cos(angle)],
            )
        )
    elif axis == 3:
        out = np.array(
            (
                [np.cos(angle), np.sin(angle), 0],
                [-np.sin(angle), np.cos(angle), 0],
                [0, 0, 1],
            )
        )

    return out


def skew(v: npt.NDArray[np.float_]) -> npt.NDArray[np.float_]:
    """Given 3x1 vector v, return skew-symmetric matrix

    Args:
        v (iterable):
            Component representation of vector.  Must have 3 elements


    Returns:
        numpy.ndarray:
            3x3 skew-symmetric matrix

    """

    assert hasattr(v, "__iter__") and len(v) == 3, "v must be an iterable of length 3."

    if isinstance(v, np.ndarray):
        v = v.flatten()

    return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])


def colVec(n: npt.ArrayLike) -> npt.NDArray[np.float_]:
    """Turn any 3-element iterable into a 3x1 column vector

    Args:
        n (iterable):
            3 element iterable

    Returns:
        numpy.ndarray:
            3x1 component representation of the vector
    """

    assert np.size(n) == 3
    n = np.array(n, ndmin=2)
    if len(n) == 1:
        n = n.T

    return n


def calcDCM(n: floatIterable, th: float) -> npt.NDArray[np.float_]:
    r"""Rodrigues formula: Calculates the DCM :math:`{}^\mathcal{A}C^\mathcal{B}` for a
    rotation of the given angle about a given axis.  This is a generalization of
    :py:meth:`rotMat`.

    Args:
        n (iterable):
            3 element vector representing rotation axis
        th (float):
            Angle of rotation

    Returns:
        numpy.ndarray:
            3x3 rotation matrix

    .. note::
        ``n`` need not be normalized - it will automatically be transformed to a unit
        vector as part of the calculation.

    """

    n1 = vnorm(colVec(n))

    DCM: npt.NDArray[np.float_] = (
        np.eye(3) * np.cos(th) + (1 - np.cos(th)) * n1 * n1.T + skew(n1) * np.sin(th)
    )

    return DCM


def DCM2axang(DCM: npt.NDArray[np.float_]) -> Tuple[npt.NDArray[np.float_], float]:
    r"""Given a direction cosine matrix :math:`{}^\mathcal{B}C^\mathcal{A}` compute
    the axis and angle of the rotation.  Inverse of :py:meth:`calcDCM`.

    Args:
        DCM (numpy.ndarray):
            3x3 Direction cosine matrix transforming vector components from frame
            :math:`\mathcal{A}` to frame :math:`\mathcal{B}`.

    Returns:
        tuple:
            n (numpy.ndarray):
                3x1 matrix representation of the unit vector of the axis of rotation
            th (float):
                Expression for the angle of rotation. Will always be between 0 and pi

    """

    costh = (DCM.trace() - 1) / 2
    sinth = np.sqrt(1 - costh**2)
    tmp = np.array(
        [DCM[2, 1] - DCM[1, 2], DCM[0, 2] - DCM[2, 0], DCM[1, 0] - DCM[0, 1]]
    )
    n = tmp / 2 / sinth
    th = np.arccos(costh)

    return n, th


def vnorm(v: npt.NDArray[np.float_]) -> npt.NDArray[np.float_]:
    """Return components of unit vector of input vector

    Args:
        v (numpy.ndarray):
            Components of vector

    Returns:
        numpy.ndarray:
            Components of unit vector
    """

    return v / np.linalg.norm(v)


def calcang(x: npt.ArrayLike, y: npt.ArrayLike, z: npt.ArrayLike) -> float:
    """Compute the angle between vectors x and y when rotating counter-clockwise about
    vector z

    Args:
        x (iterable):
            3 components of x vector
        y (iterable):
            3 components of y vector
        z (iterable):
            3 components of z vector

    Returns:
        float:
            Angle in radians
    """

    x = vnorm(colVec(x))
    y = vnorm(colVec(y))
    z = vnorm(colVec(z))

    t1 = np.linalg.norm(np.matmul(skew(x), y)) * np.sign(
        np.linalg.det(np.hstack((x, y, z)))
    )
    t2 = np.matmul(x.T, y)[0][0]

    ang: float = np.arctan2(t1, t2)

    return ang


def projplane(
    v: npt.NDArray[np.float_], nv: npt.NDArray[np.float_]
) -> npt.NDArray[np.float_]:
    """Project vectors v onto a plane normal to nv

    Args:
        v (numpy.ndarray):
            3xn vectors to be projected
        nv (numpy.ndarray):
            3x1 or 1x3 components of vector orthogonal to plane of projection

    Returns:
        numpy.ndarray:
            Output has equivalent size to v and contains the projected vectors

    """
    nv = vnorm(nv.flatten())

    projv: npt.NDArray[np.float_] = (
        v - np.vstack([np.dot(x, nv.flatten()) * nv for x in v.T]).T
    )

    return projv


def validateEulerAngSet(rotSet: intIterable) -> int:
    """Ensure that a rotation set is valid and return the number of unique elements

    Args:
        rotSet (iterable):
            3-element iterable defining order of rotations of a body Euler angle set.
            Indexing is 1-based, so valid rotation sets may only contains 1, 2, or 3.
            A valid rotation set contains exactly 3 elements, at least 2 of which are
            distinct, and with no rotations about the same axis repeated in a row.
            [1, 2, 3] and [1, 3, 1] are valid, but [1, 1, 2] is not.

    Returns:
        int:
            Number of unique axes used in rotation (2 or 3).

    """
    # ensure rotation set if valid
    assert (
        hasattr(rotSet, "__iter__") and len(rotSet) == 3
    ), "rotSet must be an iterable of length 3."
    assert (
        len(set(rotSet) - set([1, 2, 3])) == 0
    ), "Rotation set must contain only values 1, 2, 3."
    assert np.all(
        np.diff([1, 2, 1]) != 0
    ), "Rotation set cannot contain two rotations about the same axis in a row."

    # figure out whether this is a 2- or 3- rotation set
    n = len(np.unique(rotSet))
    assert n in [2, 3], "Rotation set must contain either 2 or 3 distinct elements."

    return n


def EulerAng2DCM(
    rotSet: intIterable,
    angs: floatIterable,
    body: bool = True,
) -> npt.NDArray[np.float_]:
    r"""Calculate the equivalent direction cosine matrix for an Euler Angle set


    Args:
        rotSet (iterable):
            3-element iterable defining order of rotations of a body Euler angle set.
            See :py:meth:`validateEulerAngSet`.
        angs (iterable):
            3-element iterable of symbols or expressions defining the angle of each
            rotation.
        body (bool):
            True for body rotations, False for space rotations. Defaults to True.

    Returns:
        numpy.ndarray:
            3x3 equivalent direction cosine matrix :math:`{}^\mathcal{B}C^\mathcal{A}`

    """
    _ = validateEulerAngSet(rotSet)

    assert (
        hasattr(angs, "__iter__") and len(angs) == 3
    ), "v must be an iterable of length 3."

    DCM = np.eye(3)
    for rot, ang in zip(rotSet, angs):
        if body:
            DCM = np.matmul(rotMat(rot, ang), DCM)
        else:
            DCM = np.matmul(DCM, rotMat(rot, ang))

    return DCM


def DCM2EulerAng(
    DCM: npt.NDArray[np.float_], rotSet: intIterable, body: bool = True
) -> List[float]:
    """

    Args:
        DCM (numpy.ndarray):
            Direction Cosine Matrix
        rotSet (iterable):
            3-element iterable defining order of rotations of a body Euler angle set.
            See :py:meth:`validateEulerAngSet`.
        body (bool):
            True for body rotations, False for space rotations. Defaults to True.

    Returns:
        list:
            List of the three computed angles

    """
    # ensure rotation set if valid
    n = validateEulerAngSet(rotSet)

    # extract elements of the Euler angle set for easier use in indexing
    i, j, k = np.asarray(rotSet) - 1

    if n == 3:
        # 3-axis rotation
        # first apply the negatives
        A = np.array([[1, 1, -1], [-1, 1, 1], [1, -1, 1]]) * DCM

        # if this is a space rotation, transpose the matrix
        if not body:
            A = A.T

        # extract the angles
        sinth2 = A[k, i]  # sin(\theta_2)
        costh2 = np.sqrt(A[i, i] ** 2 + A[j, i] ** 2)  # cos(\theta_2)
        th2 = np.arctan2(sinth2, costh2)
        th1 = np.arctan2(A[k, j] / costh2, A[k, k] / costh2)
        th3 = np.arctan2(A[j, i] / costh2, A[i, i] / costh2)
    else:
        # 2-axis rotation
        # first take care of the negative
        A = DCM.copy()
        negval = {1: (2, 1), 2: (0, 2), 3: (1, 0)}
        A[negval[rotSet[1]]] *= -1  # type: ignore

        # if this is a space rotation, transpose the matrix
        if not body:
            A = A.T

        # compute element missing from rotation set
        p = 5 - (rotSet[0] + rotSet[1])  # type: ignore

        costh2 = A[i, i]  # cos(\theta_2)
        sinth2 = np.sqrt(A[p, i] ** 2 + A[j, i] ** 2)  # sin(\theta_2)
        th2 = np.arctan2(sinth2, costh2)
        th1 = np.arctan2(A[i, j] / sinth2, A[i, p] / sinth2)
        th3 = np.arctan2(A[j, i] / sinth2, A[p, i] / sinth2)

    return [th1, th2, th3]
