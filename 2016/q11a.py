import sys
from itertools import combinations

from prettytable import PrettyTable

table = PrettyTable()

import aiger

from aiger_sat import SolverWrapper

sys.setrecursionlimit(100000)


# TODO: check z3
solver = SolverWrapper()  # defaults to Glucose4

TIMESTEPS = 9  # find minimum satisfiable

# not solvable voor, t= 11, 33?

# example
# The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
# The second floor contains a hydrogen generator.
# The third floor contains a lithium generator.
# The fourth floor contains nothing relevant.

# echt
# The first floor contains a strontium generator, a strontium-compatible microchip, a plutonium generator, and a plutonium-compatible microchip.
# The second floor contains a thulium generator, a ruthenium generator, a ruthenium-compatible microchip, a curium generator, and a curium-compatible microchip.
# The third floor contains a thulium-compatible microchip.
# The fourth floor contains nothing relevant.

N_FLOORS = 4
# CHARACTERS = ['hm', 'lm', 'hg', 'lg'] # elevator not in characters
# INITIAL_FLOORS = [1, 1, 2, 3, 1] # last is elevator

CHARACTERS = ['sg', 'sm', 'pg', 'pm', 'tg', 'rg', 'rm', 'cg', 'cm', 'tm'] # elevator not in characters
INITIAL_FLOORS = [1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 1] # last is elevator

# create dummy variable (which will result to true) to start building clauses
DUMMY = aiger.atom('dummy')

# create variables for the problem: all characters + elevator at all timestamps on all floors
variables = {}
n_variables = 0

for character in CHARACTERS + ['elevator']:
    for t in range(TIMESTEPS + 1):  # 0 to TIMESTEPS (incl)
        for floor in range(1, N_FLOORS + 1):
            n_variables += 1
            variables[f"{character}_floor{floor}_time{t}"] = aiger.atom(f"{character}_floor{floor}_time{t}")

# initial positions
init = DUMMY
for i, character in enumerate(CHARACTERS + ['elevator']):
    for floor in range(1, N_FLOORS + 1):
        init &= variables[f"{character}_floor{floor}_time0"] if INITIAL_FLOORS[i] == floor else ~variables[f"{character}_floor{floor}_time0"]

# final positions
goal = DUMMY
for character in CHARACTERS + ['elevator']:
    for floor in range(1, N_FLOORS + 1):
        goal &= variables[f"{character}_floor{floor}_time{TIMESTEPS}"] if N_FLOORS == floor else ~variables[f"{character}_floor{floor}_time{TIMESTEPS}"]

    goal &= variables[f"{character}_floor{N_FLOORS}_time{TIMESTEPS}"]

expr = init & goal

# dangerous characters are dangerous for character, if not protected by other character
# DANGER = [(['hg'], 'lm', 'lg'), (['lg'], 'hm', 'hg')]

DANGER = [(['pg', 'tg', 'rg', 'cg'], 'sm', 'sg'), (['sg', 'tg', 'rg', 'cg'], 'pm', 'pg'), (['sg', 'pg', 'rg', 'cg'], 'tm', 'tg'), (['sg', 'pg', 'tg', 'cg'], 'rm', 'rg'), (['sg', 'pg', 'tg', 'rg'], 'cm', 'cg')]


# avoid dangerous combinations
for t in range(TIMESTEPS + 1):  # 0 to TIMESTEPS (incl)
    for floor in range(1, N_FLOORS + 1):
        for danger in DANGER:
            dangerous_characters, vulnerable_character, protecting_character = danger

            # start with a contradiction to create a false (needed to build the or by parts)
            dangerous_situation = DUMMY == ~DUMMY

            # there is at least one of the dangerous characters
            for dangerous_character in dangerous_characters:
                dangerous_situation |= variables[f"{dangerous_character}_floor{floor}_time{t}"]

            # and the vulnerable character is present
            dangerous_situation = variables[f"{vulnerable_character}_floor{floor}_time{t}"] & dangerous_situation

            # this implies the protector must be present
            protected = dangerous_situation.implies(variables[f"{protecting_character}_floor{floor}_time{t}"])

            expr = expr & protected

# define transitions
for t in range(1, TIMESTEPS + 1):  # 1 to TIMESTEPS (incl)

    # elevator can only be on one floor, and must be on one floor
    one_elevator = DUMMY == ~DUMMY
    for floor in range(1, N_FLOORS + 1):
        one_floor = DUMMY
        for to_other_floor in range(1, N_FLOORS + 1):
            one_floor &= variables[f"elevator_floor{to_other_floor}_time{t}"] if floor == to_other_floor else ~variables[f"elevator_floor{to_other_floor}_time{t}"]


        one_elevator |= one_floor

    # elevator must be one floor higher or lower than at t - 1
    elevator_moves = DUMMY
    for floor in range(1, N_FLOORS + 1):
        # elevator always moves, so it cannot be at the same floor the next timestep
        # we have checked there is only one elevator, so here we only need to check up and down
        to_other_floor = (variables[f"elevator_floor{floor}_time{t - 1}"]).implies(
        (variables[f"elevator_floor{floor + 1}_time{t}"] if floor < N_FLOORS else (DUMMY == ~DUMMY)) |  # one higher
        (variables[f"elevator_floor{floor - 1}_time{t}"] if floor > 1 else (DUMMY == ~DUMMY)) # one lower
        )

        elevator_moves &= to_other_floor # all implications must be true (only relevant for the one with the elevator)

    # all objects must exist exactly once
    all_characters_exist = DUMMY # everything must exists
    max_one_character_exists = DUMMY # nothing exists more than once
    for character in CHARACTERS:
        this_character_exists = DUMMY == ~DUMMY
        this_character_exists_once = DUMMY == ~DUMMY
        for floor in range(1, N_FLOORS + 1):
            this_character_exists |= variables[f"{character}_floor{floor}_time{t}"]
            this_character_exists_on_this_floor_only = variables[f"{character}_floor{floor}_time{t}"]
            for other_floor in range(1, N_FLOORS + 1):
                if floor == other_floor:
                    continue
                this_character_exists_on_this_floor_only &= ~variables[f"{character}_floor{other_floor}_time{t}"]
            this_character_exists_once |= this_character_exists_on_this_floor_only

        max_one_character_exists &= this_character_exists_once
        all_characters_exist &= this_character_exists

    # if a charcter moves, it must be with the elevator
    # and all other characters must remain in place => TODO: verkeerd gelezen, er mogen 2 dingen mee in de lift
    for character in CHARACTERS:


        for floor in range(1, N_FLOORS + 1):
            has_moved_here = variables[f"{character}_floor{floor}_time{t}"] & ~variables[f"{character}_floor{floor}_time{t - 1}"]
            with_elevator = DUMMY

            # print(f"IF {character}_floor{floor}_time{t} & ~{character}_floor{floor}_time{t - 1}:")
            for other_floor in range(1, N_FLOORS + 1):
                with_elevator &= variables[f"{character}_floor{other_floor}_time{t}"] == variables[f"elevator_floor{other_floor}_time{t}"]
                with_elevator &= variables[f"{character}_floor{other_floor}_time{t - 1}"] == variables[f"elevator_floor{other_floor}_time{t - 1}"]

            expr &= (has_moved_here.implies(with_elevator))

    # array with clauses where the floor does not change for each character
    no_move_for_characters = []
    for character in CHARACTERS:
        no_move_for_character = DUMMY
        for floor in range(1, N_FLOORS + 1):
            no_move_for_character &= variables[f"{character}_floor{floor}_time{t}"] == variables[f"{character}_floor{floor}_time{t - 1}"]

        no_move_for_characters.append(no_move_for_character)

    # max 2 characters can move => n - 2 characters do not move
    max_two_moving = DUMMY == ~DUMMY
    for not_moving_characters in combinations(no_move_for_characters, len(no_move_for_characters) - 2):
        not_moving_characters_clause = DUMMY
        for not_moving_character in not_moving_characters:
            not_moving_characters_clause &= not_moving_character
        max_two_moving |= not_moving_characters_clause

    # min 1 chacter must mice => not no one moves
    no_one_moves = DUMMY
    for not_moving_character in no_move_for_characters:
        no_one_moves &= not_moving_character


    # combine all constraints for this timestep, and add them to the problem
    expr = expr & one_elevator & elevator_moves & all_characters_exist & max_one_character_exists & max_two_moving & ~no_one_moves

solver.add_expr(expr)


satifiable = solver.is_sat()

if satifiable:
    print("Possible")

    model = solver.get_model()
    print("Model", model)

    table = PrettyTable()

    table.field_names = ["time"] + [f"Floor {x}" for x in range(1, N_FLOORS + 1)]

    for t in range(TIMESTEPS + 1):
        object_locations_t = [f"t = {t}"]
        for floor in range(1, N_FLOORS + 1):
            object_locations_t_floor = ""
            for character in CHARACTERS:
                if f"{character}_floor{floor}_time{t}" not in model:
                    print (f"{character}_floor{floor}_time{t} undefined")
                if f"{character}_floor{floor}_time{t}" in model and model[f"{character}_floor{floor}_time{t}"]:
                    object_locations_t_floor += f"{character} "
            if model[f"elevator_floor{floor}_time{t}"]:
                object_locations_t_floor = f"*{object_locations_t_floor}"
            object_locations_t.append(object_locations_t_floor)
        table.add_row(object_locations_t)

    print(table)


else:
    print("Not possible")
