from tools.alchemical_cipher import (
    CIPHER,
    YEARS_PER_RADIX_POSITION,
    project_all_radix,
    project_all_slots,
    project_radix,
    verify,
)


def test_cipher_literals_and_axes():
    assert CIPHER["1m"]["sex"] == "male"
    assert CIPHER["1m"]["axis"] == "y"
    assert CIPHER["1m"]["roles"] == ("base",)
    assert CIPHER["0f"]["sex"] == "female"
    assert CIPHER["0f"]["axis"] == "x"
    assert CIPHER["0f"]["roles"] == ("acid", "philosopher_stone")


def test_all_40_corpus_slots_receive_cipher():
    slots = project_all_slots()
    assert len(slots) == 40
    assert sum(s.sex == "male" for s in slots) == 20
    assert sum(s.sex == "female" for s in slots) == 20


def test_timing_is_exactly_nine_ten_year_radix_positions_per_life():
    assert YEARS_PER_RADIX_POSITION == 10
    ticks = project_all_radix()
    assert len(ticks) == 360
    for slot in range(40):
        chunk = ticks[slot * 9:(slot + 1) * 9]
        assert len(chunk) == 9
        assert all(t.end_year - t.start_year == 10 for t in chunk)


def test_slot_timing_closes_exactly_to_source_life_window():
    slots = project_all_slots()
    ticks = project_all_radix()
    for s in slots:
        chunk = ticks[s.slot * 9:(s.slot + 1) * 9]
        assert chunk[0].start_year == s.start_year
        assert chunk[-1].end_year == s.end_year


def test_radix_phases_run_full_alchemical_cycle():
    labels = [project_radix(i).phase_label for i in range(9)]
    assert labels == [
        "creation", "electrum", "matter", "tm8", "gas",
        "liquid", "solid", "plasma", "nature",
    ]


def test_kernel_is_untouched_use_case():
    assert verify()
