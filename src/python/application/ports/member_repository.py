from abc import ABC, abstractmethod

from domain.member import MemberId, Member


class MemberRepository(ABC):
    @abstractmethod
    def get(self, member_id: MemberId) -> Member:
        raise NotImplementedError

    @abstractmethod
    def save(self, member: Member) -> None:
        raise NotImplementedError
