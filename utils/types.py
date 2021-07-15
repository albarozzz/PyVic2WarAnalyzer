class War:
    def __init__(self, name=None, action=None):
        self.name = name
        self.attackers = []
        self.defenders = []
        self.battles = []
        self.wargoal = None
        self.action = action

    @property
    def total_losses(self):
        total = 0
        for a in self.battles:
            total += a.total_losses
        return total

    @property
    def total_army(self):
        total = 0
        for c in self.battles:
            total += c.total_army
        return total

    def __str__(self):
        return self.name

    def __add__(self, other):
        if isinstance(other, War):
            return self.total_losses + other.total_losses
        else:
            return self.total_losses + other

    def __radd__(self, other):
        if other == 0:
            return self.total_losses
        else:
            self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, War):
            return self.total_losses * other.total_losses
        else:
            return self.total_losses * other

    def __rmul__(self, other):
        self.__mul__(other)

    def __bool__(self):
        if self.name and self.attackers and self.defenders:
            return True
        else:
            return False


class Battle:
    def __init__(self, name=None, location=None, result=None, defender=None, attacker=None, attackerLosses=0,
                 defenderLosses=0, attackerLeader=None, defenderLeader=None):
        self.name = name
        self.location = location
        self.result = result
        self.defender = defender
        self.attacker = attacker
        self.attackerLosses = attackerLosses
        self.defenderLosses = defenderLosses
        self.attackerLeader = attackerLeader
        self.defenderLeader = defenderLeader
        self.attackerArmy = {}
        self.defenderArmy = {}

    @property
    def total_losses(self):
        return self.defenderLosses + self.attackerLosses

    @property
    def total_army(self):
        total = 0
        for a in self.attackerArmy.values():
            total += a
        for b in self.defenderArmy.values():
            total += b
        return total

    def __str__(self):
        return self.name

    def __add__(self, other):
        if isinstance(other, Battle):
            return self.total_losses + other.total_losses
        else:
            return self.total_losses + other

    def __radd__(self, other):
        if other == 0:
            return self.total_losses
        else:
            self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, Battle):
            return self.total_losses * other.total_losses
        else:
            return self.total_losses * other

    def __rmul__(self, other):
        self.__mul__(other)

    def __bool__(self):
        if self.name and self.defender and self.attacker:
            return True
        else:
            return False


class Wargoal:
    aliases = {
        'casus': 'casus_belli',
        'casusbelli': 'casus_belli',
    }
    def __init__(self, state=None, casus_belli=None, country=None, actor=None, receiver=None, date=None, is_fulfilled=None,
                 score=None, change=None):
        self.state = state
        self.casus_belli = casus_belli
        self.country = country
        self.actor = actor
        self.receiver = receiver
        self.date = date
        self.is_fulfilled = is_fulfilled
        self.score = score
        self.change = change

    def __setattr__(self, name, value):
        name = self.aliases.get(name, name)
        object.__setattr__(self, name, value)

    def __getattr__(self, name):
        if name == "aliases":
            raise AttributeError  # http://nedbatchelder.com/blog/201010/surprising_getattr_recursion.html
        name = self.aliases.get(name, name)
        return object.__getattribute__(self, name)

    def __bool__(self):
        if self.casus_belli and self.actor and self.receiver:
            return True
        else:
            return False

    def __str__(self):
        return self.casus_belli