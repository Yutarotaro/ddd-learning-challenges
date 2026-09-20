from domain.member import MemberName

import pytest


def test_01_member_name_cannot_be_empty():
    empty_name = ""

    with pytest.raises(ValueError) as e:
        new_name = MemberName(empty_name)

    assert str(e.value) == "Member name cannot be empty"
