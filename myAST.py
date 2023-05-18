class ASTNode:
    def __init__(self, type, value=None, source_pos=None, children=None):
        self.type = type
        self.value = value
        self.source_pos = source_pos
        self.children = children if children is not None else []

    def add_child(self, child):
        self.children.append(child)

    def set_value(self, value):
        self.value = value

    def set_source_pos(self, source_pos):
        self.source_pos = source_pos