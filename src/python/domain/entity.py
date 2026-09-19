from value_object import ISBN, BookTitle, BookCopyId, LendingStatus, MemberId, MemberName

## Entities

class Book:
    """
    Book / 蔵書
    ISBTと署名で識別される書誌情報 
    """
    def __init__(self, isbn: ISBN, title: BookTitle):
        self.isbn = isbn
        self.title = title
