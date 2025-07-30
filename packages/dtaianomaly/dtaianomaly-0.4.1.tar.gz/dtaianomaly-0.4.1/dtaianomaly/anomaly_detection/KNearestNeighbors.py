from pyod.models.knn import KNN

from dtaianomaly.anomaly_detection.BaseDetector import Supervision
from dtaianomaly.anomaly_detection.PyODAnomalyDetector import PyODAnomalyDetector


class KNearestNeighbors(PyODAnomalyDetector):
    """
    Anomaly detector based on K-nearest neighbors :cite:`ramaswamy2000efficient`.

    Given some distance metric :math:`dist`, the :math:`K`-nearest neighbor of an
    instance :math:`x` is the sample :math:`y` such that there exist exactly :math:`K-1`
    other samples :math:`z` with :math:`dist(x, z) < dist(x, y)`. The :math:`K`-nearest neighbor
    distance of :math:`x` equals the distance to this :math:`K`the nearest neighbor.
    The larger this :math:`K`-nearest neighbor distance of a sample is, the further
    away it is from the other instances. :math:`K`-nearest neighbor uses this distance
    as an anomaly score, and thus detects distance-based anomalies.

    Parameters
    ----------
    window_size: int or str
        The window size to use for extracting sliding windows from the time series. This
        value will be passed to :py:meth:`~dtaianomaly.anomaly_detection.compute_window_size`.
    stride: int, default=1
        The stride, i.e., the step size for extracting sliding windows from the time series.
    **kwargs
        Arguments to be passed to the PyOD isolation forest.

    Attributes
    ----------
    window_size_: int
        The effectively used window size for this anomaly detector
    pyod_detector_ : KNN
        A K-nearest neighbors detector of PyOD

    Examples
    --------
    >>> from dtaianomaly.anomaly_detection import KNearestNeighbors
    >>> from dtaianomaly.data import demonstration_time_series
    >>> x, y = demonstration_time_series()
    >>> knn = KNearestNeighbors(10).fit(x)
    >>> knn.decision_function(x)  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    array([0.2527578 , 0.26430228, 0.2728953 , ..., 0.26269151, 0.26798469, 0.26139759]...)

    Notes
    -----
    The K-nearest neighbors inherets from :py:class:`~dtaianomaly.anomaly_detection.PyodAnomalyDetector`.
    """

    def _initialize_detector(self, **kwargs) -> KNN:
        return KNN(**kwargs)

    def _supervision(self):
        return Supervision.UNSUPERVISED
