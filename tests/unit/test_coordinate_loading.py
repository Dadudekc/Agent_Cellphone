import importlib
import types
import sys
from unittest import mock


def test_coordinate_loading_and_format(monkeypatch):
    fake_move = mock.Mock()
    fake_pyautogui = types.SimpleNamespace(moveTo=fake_move, FAILSAFE=True)
    monkeypatch.setitem(sys.modules, 'pyautogui', fake_pyautogui)

    module = importlib.import_module('tests.manual_calibrated_coordinates')
    importlib.reload(module)

    tester = module.CoordinateTester()
    assert 'Agent-1' in tester.coords

    for agent, coords in tester.coords.items():
        for key in ('starter_location_box', 'input_box'):
            box = coords[key]
            assert isinstance(box['x'], int)
            assert isinstance(box['y'], int)

    result = tester.test_agent_coordinates('Agent-1')
    assert result['starter_location']['status'] == 'success'
    assert result['input_box']['status'] == 'success'

    starter = tester.coords['Agent-1']['starter_location_box']
    input_box = tester.coords['Agent-1']['input_box']
    assert fake_move.call_args_list == [
        mock.call(starter['x'], starter['y'], duration=0.5),
        mock.call(input_box['x'], input_box['y'], duration=0.5)
    ]
