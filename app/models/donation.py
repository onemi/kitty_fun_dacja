from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.abstract import Investment

REPR = (
    'Donation from user: {user}. '
    'Comment: {comment:.15}. {investment}'
)


class Donation(Investment):
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self) -> str:
        return REPR.format(
            user=self.user_id,
            comment=self.comment,
            investment=super().__repr__()
        )
