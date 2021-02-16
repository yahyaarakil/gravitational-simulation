class Entity:
    def __init__(self, comps = ()):
        self.comps = {}
        for comp in comps:
            self.add_comp(comp)

    def add_comp(self, comp):
        if comp.IDENTIFIER in self.comps:
            return
        for condition in comp.conditions:
            if not condition(self):
                return
        self.comps[comp.IDENTIFIER] = comp
        self.comps[comp.IDENTIFIER].init(self)