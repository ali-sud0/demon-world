import random

def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

class Agent:
    def decide(self, view):
        print(view)
        hx, hy = view.hero

        moves = [
            (hx+1, hy), (hx-1, hy),
            (hx, hy+1), (hx, hy-1)
        ]

        moves = [
            m for m in moves
            if 0 <= m[0] < view.N and 0 <= m[1] < view.N and m not in view.walls
        ]

        if not moves:
            return view.hero 

        def toward(target):
            return min(moves, key=lambda m: manhattan(m, target))

        def away(target):
            return max(moves, key=lambda m: manhattan(m, target))

        if not view.has_sword:
            if view.hear_demon and view.demon:
                return away(view.demon)
            if view.sword:
                return toward(view.sword)
            return random.choice(moves)
        else:
            if view.demon:
                return toward(view.demon)
            elif view.hear_demon:
                return random.choice(moves)
            return random.choice(moves)