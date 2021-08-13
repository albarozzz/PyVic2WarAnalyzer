class UnitList(list):
    """Represents a list of units in a :class:`Battle`
    """
    def __init__(self, *args):
        super().__init__()
        for arg in args:
            super().append(arg)

    def asdict(self):
        """Returns a dict with all soldiers in a battle and numbers of them.

        Returns
        -------
        :class:`dict`
        """
        _dict = {}
        for item in super().__iter__():
            _dict.update(item.asdict())
        return _dict


class Unit:
    """Represents a unit in a :class:`Battle`

    Attributes
    ----------
    soldier: :class:`str`
        Type of the unit.
    number: :class:`int`
        Number of soldiers in the unit.
    """
    def __init__(self, soldier: str = None, number: int = 0):
        self.soldier = soldier
        self.number = number

    def __bool__(self):
        if self.soldier and self.number:
            return True
        else:
            return False

    def __str__(self):
        return self.soldier

    def __int__(self):
        return self.number

    def __add__(self, other):
        if isinstance(other, Unit):
            return self.number + other.number
        else:
            return self.number + other

    def __radd__(self, other):
        if other == 0:
            return self.number
        else:
            self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, Unit):
            return self.number * other.number
        else:
            return self.number * other

    def __rmul__(self, other):
        self.__mul__(other)

    def asdict(self):
        """Returns a dict with the type of soldier and number of it.

        Returns
        -------
        :class:`dict`
        """
        return {self.soldier: self.number}

class Wargoal:
    """Represents a wargoal in a :class:`War`

    Attributes
    ----------
    state: :class:`int`
        A province id from 'take state' CB.
    casus_belli: :class:`str`
        The name of the casus belli.
    actor: :class:`str`
        The country which made this wargoal.
    country: :class:`str`
        The name of the country which the actor wants to liberate.
    receiver: :class:`str`
        The country which received this wargoal.
    date: :class:`str`
        Wargoal date.
    is_fulfilled: :class:`bool`
        May not be present, only if it's an active war.
    score: :class:`float`
        May not be present, only if it's an active war.
    change: :class:`float`
        May not be present, only if it's an active war.
    """

    aliases = {
        'casus': 'casus_belli',
        'casusbelli': 'casus_belli',
    }

    def __init__(self, state: int = None, casus_belli: str = None, actor: str = None,
                 receiver: str = None, date: str = None, is_fulfilled: bool = None,
                 score: float = None, change: float = None, country: str = None):

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

class OriginalWargoal(Wargoal):
    """Represents an original wargoal in a :class:`War`

    Attributes
    ----------
    state: :class:`int`
        A province id from 'take state' CB.
    casus_belli: :class:`str`
        The name of the casus belli.
    country: :class:`str`
        The name of the country which the actor wants to liberate.
    actor: :class:`str`
        The country which made this wargoal.
    receiver: :class:`str`
        The country which received this wargoal.
    """
    def __init__(self, state: int = None, casus_belli: str = None, actor: str = None, receiver: str = None, country: str = None):
        self.state = state
        self.casus_belli = casus_belli
        self.country = country
        self.actor = actor
        self.receiver = receiver
        super().__init__(state=self.state, casus_belli=self.casus_belli, actor=self.actor, receiver=self.receiver, country=self.country)

class War:
    """Represents a war between 2 nations or more

    Attributes
    ----------
    attackers: :class:`list`
        All attackers.
    defenders: :class:`list`
        All defenders.
    battles: List[:class:`Battle`]
        A list of all battles in that war.
    wargoals: List[:class:`Wargoal` or :class:`OriginalWargoal`]
        A list of wargoals.
    action: :class:`str`
    """
    def __init__(self, name: str = None,
                 action: str = None):
        self.name = name
        self.attackers = []
        self.defenders = []
        self.battles = []
        self.wargoals = []
        self.action = action

    @property
    def total_losses(self) -> int:
        """
        All losses from a :class:`War`
        """
        total = 0
        for a in self.battles:
            total += a.total_losses
        return total

    @property
    def total_army(self) -> int:
        """
        All forces from a :class:`War`
        """
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
    """Represents a battle in a :class:`War`

    Attributes
    ----------
    name: :class:`str`
        Indicates the battle name, aka the province name
    location: :class:`int`
        Indicates a province id
    result: :class:`bool`
        Indicates if the attacker won the battle or else
    defender: :class:`str`
    attacker: :class:`str`
    attackerLosses: :class:`int`
    defenderLosses: :class:`int`
    attackerLeader: :class:`str`
    defenderLeader: :class:`str`
    attackerArmy: List[:class:`Unit`]
    defenderArmy: List[:class:`Unit`]
    """
    def __init__(self, name: str = None, location: int = None, result: bool = None, defender: str = None,
                 attacker: str = None, attackerLosses: int = 0,
                 defenderLosses: int = 0, attackerLeader: str = None, defenderLeader: str = None):
        self.name = name
        self.location = location
        self.result = result
        self.defender = defender
        self.attacker = attacker
        self.attackerLosses = attackerLosses
        self.defenderLosses = defenderLosses
        self.attackerLeader = attackerLeader
        self.defenderLeader = defenderLeader
        self.attackerArmy = UnitList()
        self.defenderArmy = UnitList()

    @property
    def total_losses(self) -> int:
        """
        All losses from a :class:`Battle`
        """
        return self.defenderLosses + self.attackerLosses

    @property
    def total_army(self) -> int:
        """
        All forces from a :class:`Battle`
        """
        total = 0
        for a in self.attackerArmy:
            total += int(a)
        for b in self.defenderArmy:
            total += int(b)
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

