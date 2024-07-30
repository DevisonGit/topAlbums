from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class Album:
    __tablename__ = 'albums'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    artist: Mapped[str]
    label: Mapped[str]
    year: Mapped[int]
    rating: Mapped[float] = mapped_column(nullable=True)
