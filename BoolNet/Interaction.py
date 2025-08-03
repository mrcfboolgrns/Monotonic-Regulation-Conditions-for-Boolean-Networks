class Interaction: #define an interaction between to components
    def __init__(self, source, target, effect, optional=False): #define interaction (class)
        self.source = source
        self.target = target
        self.effect = effect
        self.optional = bool(optional)

    def print_inter(self):
        print(self.source, self.target, self.effect, self.optional)