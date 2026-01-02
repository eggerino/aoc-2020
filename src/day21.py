from collections import deque
from typing import Dict, List, Tuple, Set


type Dish = Tuple[List[str], List[str]]
type Dishes = List[Dish]
type UniqueIngredients = Set[str]
type AllergeneMap = Dict[str, UniqueIngredients]


def parse_dish(s: str):
    tokens = s.split("(contains ")
    ingredients = tokens[0].split()
    if len(tokens) == 1:
        return ingredients, []
    else:
        return ingredients, tokens[1].split(")")[0].split(", ")


def count_ingredients(dishes: Dishes):
    counter = {}
    for ingredients, _ in dishes:
        for ingredient in ingredients:
            counter[ingredient] = counter.get(ingredient, 0) + 1
    uniques = set(counter)
    return counter, uniques


def first_pass_allergene_map(dishes: Dishes, unique_ingredients: UniqueIngredients):
    map = {}
    for ingredients, allergenes in dishes:
        for allergene in allergenes:
            map[allergene] = map.get(
                allergene, unique_ingredients).intersection(ingredients)
    return map


def get_safe_ingredients(unique_ingredients: UniqueIngredients, allergene_map: AllergeneMap):
    safe = unique_ingredients
    for ingredients in allergene_map.values():
        safe = safe.difference(ingredients)
    return safe


def reduce_allergene_map(allergene_map: AllergeneMap):
    q = deque(allergene_map)
    while q:
        allergene = q.popleft()
        ingredients = allergene_map[allergene]
        if len(ingredients) == 1:
            ingredient = next(iter(ingredients))
            for other_allergene, other_ingredients in allergene_map.items():
                if other_allergene != allergene and ingredient in other_ingredients:
                    other_ingredients.remove(ingredient)
        else:
            q.append(allergene)


def produce_canonical_list(allergene_map: AllergeneMap):
    kvps = [(item[0], next(iter(item[1]))) for item in allergene_map.items()]
    kvps.sort(key=lambda x: x[0])
    return [kvp[1] for kvp in kvps]


dishes = list(map(parse_dish, open(0).read().splitlines()))
ingredients_counter, ingredients = count_ingredients(dishes)
allergene_map = first_pass_allergene_map(dishes, ingredients)
safe_ingredients = get_safe_ingredients(ingredients, allergene_map)
print("Part 1:", sum(ingredients_counter[s] for s in safe_ingredients))
reduce_allergene_map(allergene_map)
canonical_list = produce_canonical_list(allergene_map)
print("Part 2:", ",".join(canonical_list))
