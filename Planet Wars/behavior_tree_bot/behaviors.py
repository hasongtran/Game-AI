import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(enemy_planets)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return

def spread_to_weakest_neutral_planet(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    neutral_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    neutral_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(neutral_planets)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return

def spread_to_closest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the closest neutral planet.
    closest_distance = 100000000
    closest_planet = None

    for planet in state.neutral_planets():
        temp = state.distance(strongest_planet.ID, planet.ID)

        if (temp < closest_distance):
            closest_planet = planet
            closest_distance = temp


    if not strongest_planet or not closest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the closest enemy planet.
        return issue_order(state, strongest_planet.ID, closest_planet.ID, strongest_planet.num_ships / 2)


def defend_weakest_owned_planet(state):
    my_planets = [planet for planet in state.my_planets()]
    if not my_planets:
        return False

    def strength(p):
        return p.num_ships \
               + sum(fleet.num_ships for fleet in state.my_fleets() if fleet.destination_planet == p.ID) \
               - sum(fleet.num_ships for fleet in state.enemy_fleets() if fleet.destination_planet == p.ID)

    avg = sum(strength(planet) for planet in my_planets) / len(my_planets)

    weak_planets = [planet for planet in my_planets if strength(planet) < avg]
    strong_planets = [planet for planet in my_planets if strength(planet) > avg]

    if (not weak_planets) or (not strong_planets):
        return False

    weak_planets = iter(sorted(weak_planets, key=strength))
    strong_planets = iter(sorted(strong_planets, key=strength, reverse=True))

    try:
        weak_planet = next(weak_planets)
        strong_planet = next(strong_planets)
        while True:
            need = int(avg - strength(weak_planet))
            have = int(strength(strong_planet) - avg)

            if have >= need > 0:
                return issue_order(state, strong_planet.ID, weak_planet.ID, need)
            elif have > 0:
                return issue_order(state, strong_planet.ID, weak_planet.ID, have)
            else:
                weak_planet = next(weak_planets)
                strong_planet = next(strong_planets)

    except StopIteration:
        return False
