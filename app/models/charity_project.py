from sqlalchemy import Column, String, Text

from app.models.abstract import Investment

REPR = 'Project name: {name:.15}. {investment}'


class CharityProject(Investment):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return REPR.format(
            name=self.name,
            investment=super().__repr__()
        )
