from tools.benchmark_shakespeare_crystallization import benchmark

def test_small_corpus_benchmark_preserves_frozen_closure():
    data = b"To be, or not to be.\n"
    r = benchmark(data, min_seconds=0.0)
    assert r["status"] == "0e"
    assert r["kernel_changed"] is False
    assert r["frozen_use_case_verified"] is True
    assert r["run"]["branch_bits"] == len(data) * 8
    assert r["run"]["crystallization_blocks_16"] == (len(data) * 8) // 16
    assert r["throughput"]["bytes_per_second"] > 0
    assert r["memory"]["python_peak_alloc_bytes"] >= 0
    assert r["closure"]["terminal"] == "0+0->oe"
    assert r["closure"]["seed"] == "+k.0.k- -> 0.0.0"
