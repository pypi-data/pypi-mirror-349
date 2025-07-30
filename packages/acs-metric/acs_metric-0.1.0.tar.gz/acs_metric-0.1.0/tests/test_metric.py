from acs import ACS

def test_basic_score():
    summary = (
        "The internet is used by people around the world. "
        "It is important for everyone. "
        "For example, it allows people to communicate globally."
    )
    acs = ACS()
    result = acs.score(summary)
    assert 0 <= result["ACS"] <= 1
    assert 0 <= result["PLA"] <= 1
    assert 0 <= result["SCM"] <= 1
    assert 0 <= result["CLE"] <= 1
    assert 0 <= result["ILA"] <= 1