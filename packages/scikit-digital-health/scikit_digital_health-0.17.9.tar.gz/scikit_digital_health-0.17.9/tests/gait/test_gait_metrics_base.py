import pytest
from numpy import array, allclose, arange, nan, isnan

from skdh.gait import gait_metrics


class EventEndpoint1Test(gait_metrics.GaitEventEndpoint):
    def __init__(self):
        super().__init__("test event ept 1", __name__, depends=None)

    def _predict(self, *args, **kwargs):
        print("inside event endpoint 1")


class EventEndpoint2Test(gait_metrics.GaitEventEndpoint):
    def __init__(self):
        super().__init__("test event ept 2", __name__, depends=[EventEndpoint1Test])

    def _predict(self, *args, **kwargs):
        print("inside event endpoint 2")


class BoutEndpoint1Test(gait_metrics.GaitBoutEndpoint):
    def __init__(self):
        super().__init__("test bout ept 1", __name__, depends=[EventEndpoint2Test])

    def _predict(self, *args, **kwargs):
        print("inside bout endpoint 1")


def test_depends(capsys):
    tbe1 = BoutEndpoint1Test()

    tbe1.predict(fs=50.0, leg_length=1.8, gait={}, gait_aux={})

    record = capsys.readouterr().out

    exp = "inside event endpoint 1\ninside event endpoint 2\ninside bout endpoint 1"
    assert exp in record


class TestBoutEndpoint:
    def test_already_run(self, capsys):
        tbe1 = BoutEndpoint1Test()
        tbe1.predict(fs=50.0, leg_length=1.8, gait={tbe1.k_: []}, gait_aux={})

        record = capsys.readouterr().out

        assert "inside bout endpoint 1" not in record


class TestEventEndpoint:
    def test_already_run(self, capsys):
        tee1 = EventEndpoint1Test()
        tee1.predict(fs=50.0, leg_length=1.8, gait={tee1.k_: []}, gait_aux={})

        record = capsys.readouterr().out

        assert "inside event endpoint 1" not in record

    def test__get_mask(self):
        gait = {
            "IC": array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100]),
            "Bout N": array([1, 1, 1, 2, 2, 2, 2, 2, 2, 2]),
            "forward cycles": array([2, 1, 0, 2, 2, 1, 0, 2, 1, 0]),
        }

        mask_1 = gait_metrics.GaitEventEndpoint._get_mask(gait, 1)
        mask_2 = gait_metrics.GaitEventEndpoint._get_mask(gait, 2)

        assert allclose(mask_1, [1, 1, 0, 1, 1, 1, 0, 1, 1, 0])
        assert allclose(mask_2, [1, 0, 0, 1, 1, 0, 0, 1, 0, 0])

        with pytest.raises(ValueError):
            gait_metrics.GaitEventEndpoint._get_mask(gait, 5)

    def test__predict_asymmetry(self):
        gait = {
            "IC": array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100]),
            "Bout N": array([1, 1, 1, 2, 2, 2, 2, 2, 2, 2]),
            "forward cycles": array([2, 1, 0, 2, 2, 1, 0, 2, 1, 0]),
            "test event ept 1": arange(1, 11),
        }

        tee1 = EventEndpoint1Test()
        tee1._predict_asymmetry(fs=50.0, leg_length=1.8, gait=gait, gait_aux={})

        res = gait["test event ept 1 asymmetry"]
        exp = array([1, 1, nan, 1, 1, 1, nan, 1, 1, nan], dtype="float")

        assert allclose(res, exp, equal_nan=True)

    def test__predict_init(self):
        gait = {
            "IC": array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100]),
            "Bout N": array([1, 1, 1, 2, 2, 2, 2, 2, 2, 2]),
            "forward cycles": array([2, 1, 0, 2, 2, 1, 0, 2, 1, 0]),
        }

        tee1 = EventEndpoint1Test()

        m, mo = tee1._predict_init(gait, init=True, offset=1)

        assert "test event ept 1" in gait
        assert gait["test event ept 1"].size == 10
        assert all(isnan(gait["test event ept 1"]))
