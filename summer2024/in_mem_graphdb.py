SCHEMA = {
    "Tcr": {},
    "Tra": {},
    "VAlpha": {},
    "JAlpha": {},
    "Cdr3Alpha": {},
    "Trb": {},
    "VBeta": {},
    "JBeta": {},
    "Cdr3Beta": {},
    "Clone": {},
    "Repertoire": {},
    "Individual": {},
    "Study": {},
    "Database": {},
    "Annotation": {},
    "PMhc": {},
    "Mhc": {},
    "MhcA": {},
    "MhcB": {},
    "Epitope": {},
    "Species": {},
}

fake = [
    {"node_label": "VAlpha", "id": 3},
    {"node_label": "JAlpha", "id": 4},
    {"node_label": "Cdr3Alpha", "id": 5},
    {"node_label": "Trb", "id": 6},
    {"node_label": "VBeta", "id": 7},
    {"node_label": "JBeta", "id": 8},
    {"node_label": "Cdr3Beta", "id": 9},
    {"node_label": "Clone", "id": 10},
    {"node_label": "Repertoire", "id": 11},
    {"node_label": "Individual", "id": 12},
    {"node_label": "Study", "id": 13},
    {"node_label": "Database", "id": 14},
    {"node_label": "Annotation", "id": 15},
    {"node_label": "PMhc", "id": 16},
    {"node_label": "Mhc", "id": 17},
    {"node_label": "MhcA", "id": 18},
    {"node_label": "MhcB", "id": 19},
    {"node_label": "Epitope", "id": 20},
    {"node_label": "Species", "id": 21},
]
fake_data = [
    {"node_label": "Tcr", "id": 1},
    {"node_label": "Tcr", "id": 0},
    {"node_label": "Tra", "id": 2},
    {"node_label": "Tra", "id": 3},
    {"node_label": "JAlpha", "id": 4},
    {"node_label": "Cdr3Alpha", "id": 5},
]


class Relationships:
    def __setitem__(self, key, value: T):
        setattr(self, key, value)

    def __getitem__(self, key: str) -> T:
        return getattr(self, key)

    def __repr__(self) -> str:
        return str(list(self.__dict__.values()))


class Node:
    def __init__(self, **kwargs) -> None:
        self.rels: Relationships[Node] = Relationships()
        self.node_type = self.__class__.__name__
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self) -> str:
        props = {
            k: v for k, v in self.__dict__.items() if k not in ["node_type", "rels"]
        }
        prop_str = " ".join([f"{k}='{v}'" for k, v in props.items()])

        return f"<{self.node_type} {prop_str}>"


def class_factory(baseclass, name):
    class NewClass(baseclass):
        pass

    NewClass.__name__ = name
    NewClass.__qualname__ = name
    return NewClass


def find_class_by_classname(cls_list: List[T], name):
    for cls in cls_list:
        if cls.__name__ == name:
            return cls


available_classes = [class_factory(Node, i) for i in SCHEMA]


class QuerySet:
    def __init__(self, queryset) -> None:
        self.query_set = queryset

    def to(self, __name: str):
        nodes = [getattr(node.rels, __name, None) for node in self.query_set]
        nodes_cleaned = [node for node in nodes if node]
        self.query_set = nodes_cleaned
        return self

    def __repr__(self) -> str:
        return str(self.query_set)


class GraphDB:
    def __init__(self, cls_list) -> None:
        self.nodes = []
        self.cls_list = cls_list

    def update_index(self):
        self.index = {}

        for node in self.nodes:
            self.index[node.id] = node

    def create(self, classname: str, prop: dict):
        cls = find_class_by_classname(self.cls_list, classname)
        obj = cls(**prop)
        self.nodes.append(obj)

        self.update_index()
        return obj

    def create_rel(self, id1, id2):
        node1 = self.index[id1]
        node2 = self.index[id2]

        node1.rels[node2.__class__.__name__] = node2
        node2.rels[node1.__class__.__name__] = (
            node1  # to do: need to use array for rels if not cannot handle more than 1 rels for 1 dtype
        )

    def query(self, node_label):
        res = [node for node in self.nodes if node.node_label == node_label]
        return QuerySet(res)


db = GraphDB(available_classes)

for node in fake_data:
    db.create(node['node_label'], node)

db.create_rel(1, 2)
db.create_rel(0,3)
db.nodes[0].rels.Tra.rels.Tcr
db.query('Tcr').to('Tra').to('Tcr')
