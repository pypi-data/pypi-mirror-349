from functools import lru_cache
from typing import Annotated, Any, Type

from pydantic_core import core_schema
from pydantic_core.core_schema import GetCoreSchemaHandler
from rdkit import Chem
from rdkit.Chem import SanitizeFlags


@lru_cache(maxsize=4096)
def _validate_smiles(smiles: str) -> str:
    """
    A single cached function that parses → sanitizes → canonicalize(s?)
    """
    mol = Chem.MolFromSmiles(smiles, sanitize=False)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles!r}")
    try:
        Chem.SanitizeMol(mol, sanitizeOps=SanitizeFlags.SANITIZE_ALL)
    except Exception as e:
        raise ValueError(f"SMILES sanitization failed for {smiles!r}: {e}")
    return Chem.MolToSmiles(mol, canonical=True)


class SmilesValidator:
    """
    A Pydantic-compatible callable that validates SMILES strings using RDKit.

    Can be used in two ways:

      1) As a field alias:
         smiles: SmilesText

      2) Directly via Annotated:
         smiles: Annotated[str, SmilesValidator()]
    """

    def __call__(self, value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError(f"SMILES must be a string, got {type(value).__name__}")
        # delegate to our cached function
        return _validate_smiles(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[str], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        # tell Pydantic to use our __call__ for validation
        return core_schema.no_info_plain_validator_function(cls())


# One-liner alias so you can just write `SmilesText` in your Pydantic models
SmilesText = Annotated[str, SmilesValidator()]
