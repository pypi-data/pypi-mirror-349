from smart_chunker_engine.window_segment import window_segment

def test_window_segment_basic():
    tokens = [str(i) for i in range(10)]
    windows = window_segment(tokens, window_size=4, step_size=3)
    assert windows == [(0, 4), (3, 7), (6, 10)]

def test_window_segment_exact_fit():
    tokens = [str(i) for i in range(6)]
    windows = window_segment(tokens, window_size=2, step_size=2)
    assert windows == [(0, 2), (2, 4), (4, 6)]

def test_window_segment_step_gt_window():
    tokens = [str(i) for i in range(7)]
    windows = window_segment(tokens, window_size=2, step_size=3)
    assert windows == [(0, 2), (3, 5), (6, 7)] 