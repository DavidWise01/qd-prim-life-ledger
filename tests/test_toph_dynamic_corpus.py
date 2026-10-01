from tools.toph_dynamic_corpus import (
    TOPH_COLOR,
    TOPH_GEM,
    TOPH_NAME,
    TophDynamicCorpus,
)


def test_toph_dynamic_corpus_identity_is_fixed():
    corpus = TophDynamicCorpus()
    assert corpus.NAME == TOPH_NAME == "toph"
    assert corpus.GEM == TOPH_GEM == "emerald"
    assert corpus.COLOR == TOPH_COLOR == "green"
    assert corpus.GENERATION == 1
    assert corpus.CAN_SPAWN is False
    assert corpus.CORPUS_MUTABLE is False


def test_dynamic_frame_composes_dot_corpus_phase_mnemonic_and_air():
    corpus = TophDynamicCorpus("toph")
    frame = corpus.next()

    assert frame.name == "toph"
    assert frame.gem == "emerald"
    assert frame.color == "green"
    assert frame.generation == 1
    assert frame.can_spawn is False
    assert frame.corpus_mutable is False

    assert frame.dot_address.startswith("dot[0]::")
    assert 0 <= frame.radix < 360
    assert 0 <= frame.corpus_slot < 40
    assert 0 <= frame.radix_phase < 9
    assert frame.phase_label in {
        "creation", "electrum", "matter", "tm8", "gas",
        "liquid", "solid", "plasma", "nature",
    }
    assert frame.mnemonic_skeleton
    assert frame.mnemonic_expansion
    assert frame.air_literal == "2x1^10^-35.99 - {air 36.00}} +36.01"


def test_dynamic_corpus_is_deterministic_for_same_seed():
    a = TophDynamicCorpus("toph").generate(64)
    b = TophDynamicCorpus("toph").generate(64)
    assert a == b


def test_dynamic_corpus_advances_without_mutating_source():
    corpus = TophDynamicCorpus("toph")
    frames = corpus.generate(360)
    assert len(frames) == 360
    assert corpus.verify()
    assert all(frame.generation == 1 for frame in frames)
    assert all(frame.can_spawn is False for frame in frames)
    assert all(frame.corpus_mutable is False for frame in frames)


def test_dynamic_corpus_has_no_generation_authority():
    corpus = TophDynamicCorpus()
    assert not hasattr(corpus, "spawn")
    assert not hasattr(corpus, "infer_daughter")
    assert not hasattr(corpus, "mutate_corpus")
