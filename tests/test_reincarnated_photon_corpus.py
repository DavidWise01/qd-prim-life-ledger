from tools.reincarnated_photon_corpus import (
    LIFE_YEARS,
    LIVES,
    LIVES_PER_RING,
    PHOTON_YEARS,
    RINGS,
    RING_YEARS,
    SOURCE_SLOTS,
    TOROID_LIVES,
    TOROID_YEARS,
    life_at,
    photon_corpus,
)


def test_photon_is_eighty_lives_of_ninety_years():
    assert LIVES == 80
    assert LIFE_YEARS == 90
    assert PHOTON_YEARS == 7200


def test_twenty_rings_take_four_lives_each():
    assert RINGS == 20
    assert LIVES_PER_RING == 4
    assert RING_YEARS == 360
    assert 20 * 360 == 7200


def test_dual_toroid_is_forty_lives_per_side():
    assert SOURCE_SLOTS == TOROID_LIVES == 40
    assert TOROID_YEARS == 3600
    assert life_at(0).toroid == "-d"
    assert life_at(39).toroid == "-d"
    assert life_at(40).toroid == "+d"
    assert life_at(79).toroid == "+d"


def test_second_pass_reuses_source_without_inventing_identity():
    a = life_at(7)
    b = life_at(47)
    assert a.source_slot == b.source_slot == 7
    assert a.incarnation == 0
    assert b.incarnation == 1
    assert a.mnemonic_name == b.mnemonic_name


def test_ring_quarters_are_four_by_ninety():
    corpus = photon_corpus()
    for ring in range(RINGS):
        chunk = corpus[ring * 4:(ring + 1) * 4]
        assert [x.ring_quarter for x in chunk] == [0, 1, 2, 3]
        assert sum(x.life_years for x in chunk) == 360
