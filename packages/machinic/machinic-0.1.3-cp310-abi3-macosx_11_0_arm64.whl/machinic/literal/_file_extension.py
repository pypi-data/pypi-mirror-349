from typing import Literal


StandardFileExtension = Literal[
    "json",
    "jsonl",
    "jsonc",
    "yaml",
    "toml",
    "jpeg",
]

AlternativeFileExtension = Literal[
    "ndjson",
    "yml",
    "jpg",
]

FileExtension = StandardFileExtension | AlternativeFileExtension