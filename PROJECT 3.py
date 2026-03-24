class Creature:
    def __init__(self, strength, defense):
        self.strength = strength
        self.defense = defense
        self.next = None

    def deep_copy(self):
        new_creature = Creature(self.strength, self.defense)
        if self.next:
            new_creature.next = self.next.deep_copy()
        return new_creature
class Commander:
    def __init__(self):
        self.hitPoints = 40
        self.firstCreature = None

    def _insert_sorted(self, creature):
        if not self.firstCreature:
            self.firstCreature = creature
            return

        prev = None
        curr = self.firstCreature

        while curr:
            if (creature.defense > curr.defense) or \
               (creature.defense == curr.defense and creature.strength > curr.strength):
                break
            prev = curr
            curr = curr.next

        if prev is None:
            creature.next = self.firstCreature
            self.firstCreature = creature
        else:
            creature.next = curr
            prev.next = creature

    def addCreature(self, creature):
        if creature is None:
            return

        copied_chain = creature.deep_copy()

        current = copied_chain
        while current:
            next_node = current.next
            current.next = None
            self._insert_sorted(current)
            current = next_node

    def _remove_first(self):
        if self.firstCreature:
            self.firstCreature = self.firstCreature.next

    def battle(self, other):
        while self.firstCreature and other.firstCreature:
            c1 = self.firstCreature
            c2 = other.firstCreature

            c1_dies = c2.strength >= c1.defense
            c2_dies = c1.strength >= c2.defense

            if not c1_dies and not c2_dies:
                return

            if c1_dies:
                self._remove_first()
            if c2_dies:
                other._remove_first()

        if self.firstCreature and not other.firstCreature:
            curr = self.firstCreature
            while curr:
                other.hitPoints -= curr.strength
                curr = curr.next

        elif other.firstCreature and not self.firstCreature:
            curr = other.firstCreature
            while curr:
                self.hitPoints -= curr.strength
                curr = curr.next

#EXAMPLE RUN:
c1 = Creature(10, 5)
c1.next = Creature(8, 6)

c2 = Creature(7, 5)

commander1 = Commander()
commander2 = Commander()

commander1.addCreature(c1)
commander2.addCreature(c2)

commander1.battle(commander2)

print(commander1.hitPoints, commander2.hitPoints)