

mdp_q1 = {
    'S': [
        (0, 0),  # A
        (1, 0),  # B
        (2, 0),  # C
        (0, 1),  # D
        (1, 1),  # E
        (2, 1),  # F
        (5, 5),  # Terminal
    ],
    'A': [
        'NORTH',
        'EAST',
        'SOUTH',
        'WEST',
        'TERMINATE',
    ],
    'Sp': [
        lambda s: (s[0], s[1] - 1),
        lambda s: (s[0] + 1, s[1]),
        lambda s: (s[0], s[1] + 1),
        lambda s: (s[0] - 1, s[1]),
        lambda s: (5, 5) if s == (2, 1) else s
    ],
    'T': lambda s, a, sp: 1,
    'R': lambda s, a, sp: 1 if s == (2, 1) and a == 'TERMINATE' else 0,
    'gamma': 0.5,
}

mdp_q4 = {
    'S': [
        (0, 0),  # A
        (1, 0),  # B
        (0, 1),  # C
        (1, 1),  # D
        (2, 1),  # E
        (3, 1),  # F
        (5, 5),  # Terminal
    ],
    'A': [
        'NORTH',
        'EAST',
        'SOUTH',
        'WEST',
        'TERMINATE',
    ],
    'Sp': [
        lambda s: (s[0], s[1] - 1),
        lambda s: (s[0] + 1, s[1]),
        lambda s: (s[0], s[1] + 1),
        lambda s: (s[0] - 1, s[1]),
        lambda s: (5, 5) if s == (1, 0) else s
    ],
    'T': lambda s, a, sp: 1,
    'R': lambda s, a, sp: 1
    if s == (1, 0) and a == 'TERMINATE'
    else 5
    if sp == (1, 1) or sp == (3, 1)
    else -1,
    'gamma': 1,
}

mdp = {
    'S': [
        (0, 0),

        (0, 1),  # 1
        (1, 1),
        (2, 1),
        (4, 1),  # -1

        (3, 2),  # 1
        (5, 2),  # 4
        (6, 2),  # 1
        (7, 2),
        (8, 2)
    ],
    'A': [
        'NORTH',
        'EAST',
        'SOUTH',
        'WEST',
        'EXIT',
    ],
    'Sp': [
        lambda s: (s[0], s[1] - 1),
        lambda s: (s[0] + 1, s[1]),
        lambda s: (s[0], s[1] + 1),
        lambda s: (s[0] - 1, s[1]),
        lambda s: s
    ],
    'T': lambda s, a, sp: 1,
    'R': lambda s, a, sp: mdp_q5Rs[(s, a)] if (s, a) in mdp_q5Rs else 0,
    'gamma': 0.5,
}
mdp_q5Rs = {
    ((0, 1), 'EXIT'): 1,
    ((4, 1), 'EXIT'): -1,
    ((3, 2), 'EXIT'): 1,
    ((5, 2), 'EXIT'): 4,
    ((6, 2), 'EXIT'): 1,
}


def get_next_states(mdp, s):
    for idx, aFunc in enumerate(mdp['Sp']):
        sP = aFunc(s)
        if sP in mdp['S']:
            yield mdp['A'][idx], sP


def q_value(mdp, s, a, V):
    return a, sum(
        [
            mdp['T'](s, a, sp) * (
                mdp['R'](s, a, sp) + (mdp['gamma'] * V[sp][1])
            ) for _, sp in get_next_states(mdp, s)
        ]
    )


def value_iter(mdp, epsilon=5):
    k = 0
    V = {s: (None, 0) for s in mdp['S']}
    Vp = {s: (None, 0) for s in mdp['S']}
    delta = 0
    while delta <= epsilon*(1-mdp['gamma'])/mdp['gamma']:
        V = Vp.copy()
        delta = 0
        for s in mdp['S']:
            Vp[s] = max(
                (q_value(mdp, s, a, V) for a, _ in get_next_states(mdp, s)),
                key=lambda x: x[1]
            )
            if abs(Vp[s][1] - V[s][1]) > delta:
                delta = abs(Vp[s][1] - V[s][1])
        print(k, Vp)
        k += 1
    return V


if __name__ == '__main__':
    # print(list(get_next_states(mdp, (2, 1))))
    # print(q_value(mdp, (2, 1), 'TERMINATE', {
    #     s: 0 for s in mdp['S']
    # }))
    v = value_iter(mdp)
    print("")
    print(v)
