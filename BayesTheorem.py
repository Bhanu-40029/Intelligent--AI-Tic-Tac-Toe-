from flask import jsonify

# ---------------- WIN PATTERNS ---------------- #

win_patterns = [

    [0,1,2],
    [3,4,5],
    [6,7,8],

    [0,3,6],
    [1,4,7],
    [2,5,8],

    [0,4,8],
    [2,4,6]
]

# ---------------- CHECK WINNER ---------------- #

def check_winner(state):

    for pattern in win_patterns:

        a,b,c = pattern

        if state[a] != '' and state[a] == state[b] == state[c]:

            return state[a]

    return None


# ---------------- TERMINAL ---------------- #

def is_terminal(state):

    return check_winner(state) is not None or '' not in state


# ---------------- CURRENT PLAYER ---------------- #

def get_current_player(state):

    x_count = state.count('X')

    o_count = state.count('O')

    if x_count > o_count:

        return 'O'

    return 'X'


# ---------------- COUNT OUTCOMES ---------------- #

def count_outcomes(state):

    if is_terminal(state):

        winner = check_winner(state)

        if winner == 'O':

            return (1,0,0)

        elif winner == 'X':

            return (0,1,0)

        else:

            return (0,0,1)

    player = get_current_player(state)

    ai_wins = 0
    human_wins = 0
    draws = 0

    for i in range(9):

        if state[i] == '':

            new_state = state.copy()

            new_state[i] = player

            a,h,d = count_outcomes(new_state)

            ai_wins += a
            human_wins += h
            draws += d

    return (ai_wins,human_wins,draws)


# ---------------- BAYES THEOREM ---------------- #

def bayes_theorem(board):

    ai_wins, human_wins, draws = count_outcomes(board)

    total = ai_wins + human_wins + draws

    if total == 0:

        return {

            "prior": 0,
            "likelihood": 0,
            "evidence": 0,
            "posterior": 0
        }

    # PRIOR P(A)

    prior = ai_wins / total

    # EVIDENCE P(B)

    occupied_cells = 9 - board.count('')

    evidence = occupied_cells / 9

    if evidence == 0:

        evidence = 0.1

    # LIKELIHOOD P(B|A)

    likelihood = (occupied_cells + 1) / 10

    # BAYES

    posterior = (likelihood * prior) / evidence

    return {

        "prior": round(prior,4),

        "likelihood": round(likelihood,4),

        "evidence": round(evidence,4),

        "posterior": round(posterior,4),

        "posterior_percentage":
        round(posterior * 100,2),

        "ai_wins": ai_wins,

        "human_wins": human_wins,

        "draws": draws
    }