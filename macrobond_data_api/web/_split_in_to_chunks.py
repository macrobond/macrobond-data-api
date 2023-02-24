from typing import Generator, Sequence, TypeVar


SplitInToChunksTypeVar = TypeVar("SplitInToChunksTypeVar")


def split_in_to_chunks(
    sequence: Sequence[SplitInToChunksTypeVar], chunk_size: int
) -> Generator[Sequence[SplitInToChunksTypeVar], None, None]:
    for i in range(0, len(sequence), chunk_size):
        yield sequence[i : i + chunk_size]
