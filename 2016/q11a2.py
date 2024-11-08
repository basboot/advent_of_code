import heapq
from copy import copy
from functools import total_ordering
from itertools import combinations

from attr import dataclass

N_FLOORS = 4

# elements = list('hl')
# elements = list('sptrc')
elements = list('sptrced')

@total_ordering
@dataclass(eq=False)
class Building:
    elevator: int
    floors: list[list[set]]  # tuple of floors, with tuple with two sets microchips and generators

    def __copy__(self):
        new_floors = []
        for floor in self.floors:
            microchips, generators = floor
            new_floors.append([microchips.copy(), generators.copy()])
        return Building(self.elevator, new_floors)

    def create_hash(self):
        x = [(tuple([i] + sorted(list(microchips))), tuple([i] + sorted(list(generator)))) for
             i, (microchips, generator) in enumerate(self.floors)]
        x = tuple([self.elevator] + [item for sublist in x for item in sublist])
        return x

    def __hash__(self):
        return hash(self.create_hash())

    def __eq__(self, other):
        # Custom equality check that only considers the elevator
        return isinstance(other, Building) and self.create_hash() == other.create_hash()

    def __lt__(self, other):
        return self.elevator < other.elevator

    # def heuristic(self):
    #     h = 0
    #     for i in range(N_FLOORS):
    #         h += (len(self.floors[0]) + len(self.floors[1])) * (N_FLOORS - 1 - i)
    #     return h



# example
# The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
# The second floor contains a hydrogen generator.
# The third floor contains a lithium generator.
# The fourth floor contains nothing relevant.

# state = Building(0, [[{'h', 'l'}, set()], [set(), {'h'}], [set(), {'l'}], [set(), set()]])

# reals
# The first floor contains a strontium generator, a strontium-compatible microchip, a plutonium generator, and a plutonium-compatible microchip.
# The second floor contains a thulium generator, a ruthenium generator, a ruthenium-compatible microchip, a curium generator, and a curium-compatible microchip.
# The third floor contains a thulium-compatible microchip.
# The fourth floor contains nothing relevant.
# state = Building(0, [[{'s', 'p'}, {'s', 'p'}], [{'r', 'c'}, {'t', 'r', 'c'}], [{'t'}, set()], [set(), set()]])

# part 2
state = Building(0, [[{'s', 'p', 'e', 'd'}, {'s', 'p', 'e', 'd'}], [{'r', 'c'}, {'t', 'r', 'c'}], [{'t'}, set()], [set(), set()]])


def is_legal(b: Building) -> bool:
    for floor in b.floors:
        microchips, generators = floor
        if len(generators) == 0:
            continue # no generator, no worry
        for microchip in microchips:
            if microchip not in generators:
                return False # there is a generator and a microchip without its generator
    return True

def next_states(b: Building) -> list[Building]:
    result = []
    items = [(x, True) for x in b.floors[b.elevator][0]] + [(x, False) for x in b.floors[b.elevator][1]]
    options = list(combinations(items, 1)) + list(combinations(items, 2))

    for next_level in [-1, 1]:
        next_floor = b.elevator + next_level
        if next_floor < 0 or next_floor >= N_FLOORS:
            continue # floor does not exist
        # if floor is empty (and floors below), skip
        no_items = True
        for f in range(next_floor, -1, -1):
            if len(b.floors[f][0]) + len(b.floors[f][1]) > 0:
                no_items = False
                break
        if no_items:
            continue


        # now make all optional changes
        for option in options:
            # make copy
            nb = copy(b)
            nb.elevator = next_floor
            skip = False
            for item, is_microchip in option:
                if next_level == -1: # dont bring pairs back down
                    if item in b.floors[b.elevator][0] and item in b.floors[b.elevator][1]:
                        skip = True
                        break
                nb.floors[b.elevator][0 if is_microchip else 1].remove(item)
                nb.floors[nb.elevator][0 if is_microchip else 1].add(item)

            if not skip and is_legal(nb):
                result.append(nb)
    return result


explore = []
visited = set()
heapq.heappush(explore, (0, state))

max_depth = -1

while True and len(explore) > 0:
    cost, current_state = heapq.heappop(explore)
    # print(current_state)

    if cost > max_depth:
        print("Min steps: ", cost)
        max_depth = cost

    # check lose (no need to search further)
    if current_state.elevator == N_FLOORS - 1 and len(current_state.floors[N_FLOORS - 1][0]) == len(elements) and len(current_state.floors[N_FLOORS - 1][1]) == len(elements):
        print("FOUND", cost)
        print(current_state)
        exit()

    for next_state in next_states(current_state):
        if next_state in visited:
            continue
        visited.add(next_state)

        heapq.heappush(explore, (cost + 1, next_state))



