"""Test Romeo y Julieta by Shakespeare.
"""


def test_romeo(character):
    assert character["name"] == "Romeo"
    assert "Julieta" in character["mindmap"]


def test_julieta(character):
    assert character["name"] == "Julieta"
    assert "Romeo" in character["mindmap"]


def test_play(play):
    assert play["location"] == "Verona"


def test_author(author):
    assert author["name"] == "William"
