SCHEMA = {
    "Tcr": {
        "properties": {
            "id": str,
        },
        "relationships": {
            "Tra": {"HAS_TRA": {}},
            "Trb": {"HAS_TRB": {}},
            "Clone": {"ENCODES": {}},
            "Annotation": {"HAS_TCR": {}},
            "Species": {"PRODUCES": {}},
        },
    },
    "Tra": {
        "properties": {
            "id": str,
        },
        "relationships": {
            "VAlpha": {"HAS_V": {}},
            "JAlpha": {"HAS_J": {}},
            "Cdr3Alpha": {"HAS_CDR3": {}},
            "Tcr": {"HAS_TRA": {}},
        },
    },
    "VAlpha": {
        "properties": {
            "id": str,
        },
        "relationships": {
            "Tra": {"HAS_V": {}},
        },
    },
    "JAlpha": {
        "properties": {
            "id": str,
        },
        "relationships": {
            "Tra": {"HAS_J": {}},
        },
    },
    "Cdr3Alpha": {
        "properties": {
            "id": str,
        },
        "relationships": {
            "Tra": {"HAS_CDR3": {}},
        },
    },
    "Trb": {
        "properties": {
            "id": str,
        },
        "relationships": {
            "VBeta": {"HAS_V": {}},
            "JBeta": {"HAS_J": {}},
            "Cdr3Beta": {"HAS_CDR3": {}},
            "Tcr": {"HAS_TRB": {}},
        },
    },
    "VBeta": {
        "properties": {
            "id": str,
        },
        "relationships": {
            "Trb": {"HAS_V": {}},
        },
    },
    "JBeta": {
        "properties": {
            "id": str,
        },
        "relationships": {
            "Trb": {"HAS_J": {}},
        },
    },
    "Cdr3Beta": {
        "properties": {
            "id": str,
        },
        "relationships": {
            "Trb": {"HAS_CDR3": {}},
        },
    },
    "Clone": {
        "properties": {
            "id": str,
            "cdr3a_nt": str,
            "cdr3b_nt": str,
        },
        "relationships": {
            "Tcr": {"ENCODES": {}},
            "Repertoire": {
                "SAMPLED_FROM": {
                    "disease_state": str,
                    "timepoint": str,
                    "frequency": float,
                    "duplicate_count": int,
                }
            },
        },
    },
    "Repertoire": {
        "properties": {
            "id": str,
        },
        "relationships": {
            "Repertoire": {"IS_IN": {}},
            "Individual": {"IS_IN": {}},
            "Clone": {
                "SAMPLED_FROM": {
                    "disease_state": str,
                    "timepoint": str,
                    "frequency": float,
                    "duplicate_count": int,
                }
            },
            "Species": {"IS_OF_SPECIES": {}},
            "MhcB": {
                "EXPRESSES": {
                    "allele": str,
                }
            },
            "MhcA": {
                "EXPRESSES": {
                    "allele": str,
                }
            },
            "Study": {"IN_STUDY": {}},
        },
    },
    "Individual": {
        "properties": {
            "id": str,
        },
        "relationships": {
            "Repertoire": {"IS_IN": {}},
            "Clone": {
                "SAMPLED_FROM": {
                    "disease_state": str,
                    "timepoint": str,
                    "frequency": float,
                    "duplicate_count": int,
                }
            },
            "Species": {"IS_OF_SPECIES": {}},
            "MhcB": {
                "EXPRESSES": {
                    "allele": str,
                }
            },
            "MhcA": {
                "EXPRESSES": {
                    "allele": str,
                }
            },
            "Study": {"IN_STUDY": {}},
        },
    },
    "Study": {
        "properties": {
            "id": str,
        },
        "relationships": {
            "Repertoire": {"IN_STUDY": {}},
            "Individual": {"IN_STUDY": {}},
            "Database": {"IS_IN": {}},
            "Annotation": {
                "CLAIMS": {
                    "vdjdb_score": list[int],
                }
            },
        },
    },
    "Database": {
        "properties": {
            "id": str,
        },
        "relationships": {
            "Study": {"IS_IN": {}},
        },
    },
    "Annotation": {
        "properties": {
            "id": str,
        },
        "relationships": {
            "Tcr": {"HAS_TCR": {}},
            "Study": {
                "CLAIMS": {
                    "vdjdb_score": list[int],
                }
            },
            "PMhc": {"HAS_TARGET": {}},
        },
    },
    "PMhc": {
        "properties": {
            "id": str,
        },
        "relationships": {
            "Annotation": {"HAS_TARGET": {}},
            "Epitope": {"HAS_EPITOPE": {}},
            "Mhc": {"HAS_MHC": {}},
        },
    },
    "Mhc": {
        "properties": {
            "id": str,
            "class": int,
        },
        "relationships": {
            "PMhc": {"HAS_MHC": {}},
            "MhcA": {"HAS_MHCA": {}},
            "MhcB": {"HAS_MHCB": {}},
        },
    },
    "MhcA": {
        "properties": {
            "id": str,
        },
        "relationships": {
            "Mhc": {"HAS_MHCA": {}},
            "Repertoire": {"EXPRESSES": {}},
            "Individual": {"EXPRESSES": {}},
        },
    },
    "MhcB": {
        "properties": {
            "id": str,
        },
        "relationships": {
            "Mhc": {"HAS_MHCB": {}},
            "Repertoire": {"EXPRESSES": {}},
            "Individual": {"EXPRESSES": {}},
        },
    },
    "Epitope": {
        "properties": {
            "id": str,
        },
        "relationships": {
            "PMhc": {"HAS_EPITOPE": {}},
            "Species": {"PRODUCES": {"gene": str}},
        },
    },
    "Species": {
        "properties": {
            "id": str,
        },
        "relationships": {
            "Repertoire": {"IS_OF_SPECIES": {}},
            "Individual": {"IS_OF_SPECIES": {}},
            "Epitope": {"PRODUCES": {}},
            "Tcr": {"PRODUCES": {}},
        },
    },
}

from typing import TypeVar, List, Generic, Type

T = TypeVar("T")


class Relationships:
    def __setitem__(self, key, value: T):
        setattr(self, key, value)

    def __getitem__(self, key: str) -> T:
        return getattr(self, key)

    def __repr__(self) -> str:
        return str(list(self.__dict__.values()))


class Node:
    def __init__(self) -> None:
        self.rels: Relationships[Node] = Relationships()
        self.node_type = self.__class__.__name__


def class_factory(baseclass, name):
    class NewClass(baseclass):
        pass

    NewClass.__name__ = name
    NewClass.__qualname__ = name
    return NewClass


entry_points = [class_factory(Node, i)() for i in SCHEMA]


def find_by_classname(cls_list: List[T], name):
    for cls in cls_list:
        if cls.__class__.__name__ == name:
            return cls


for key, value in SCHEMA.items():
    curr_cls = find_by_classname(entry_points, key)
    if curr_cls is None:
        continue
    rels_to_add = value["relationships"]
    for rel in rels_to_add:
        rel_cls = find_by_classname(entry_points, rel)
        curr_cls.rels[rel] = rel_cls  # type: ignore
entry_points[
    0
].rels.Annotation.rels.PMhc.rels.Mhc.rels.MhcA.rels.Repertoire.rels.Clone.rels
