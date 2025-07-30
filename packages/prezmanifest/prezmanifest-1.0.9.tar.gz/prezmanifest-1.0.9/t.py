from prezmanifest import validate
from pathlib import Path

v = validate(Path("tests/validator/manifest-syntax-error.ttl"))