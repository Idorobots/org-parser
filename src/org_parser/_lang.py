"""Internal: tree-sitter Language and Parser singletons for Org Mode."""

from tree_sitter import Language, Parser
import tree_sitter_org

__all__ = ["ORG_LANGUAGE", "PARSER"]

#: The Org Mode :class:`~tree_sitter.Language` instance (module-level singleton).
ORG_LANGUAGE: Language = Language(tree_sitter_org.language())

#: A :class:`~tree_sitter.Parser` pre-configured with :data:`ORG_LANGUAGE`.
PARSER: Parser = Parser(ORG_LANGUAGE)
