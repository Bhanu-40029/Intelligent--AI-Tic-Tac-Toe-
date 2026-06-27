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

# ---------------- CENTER OCCUPIED ---------------- #

def center_occupied(board):

    return board[4] == 'O'


# ---------------- TWO IN A ROW ---------------- #

def two_in_row(board):

    for pattern in win_patterns:

        values = [board[i] for i in pattern]

        if values.count('O') == 2 and values.count('') == 1:

            return True

    return False


# ---------------- WIN PROBABILITY ---------------- #

def win_probability(board):

    score = 0

    # CENTER BONUS

    if center_occupied(board):

        score += 30

    # TWO IN ROW BONUS

    if two_in_row(board):

        score += 50

    # CORNER BONUS

    corners = [0,2,6,8]

    occupied_corners = sum(

        1 for i in corners

        if board[i] == 'O'
    )

    score += occupied_corners * 5

    # LIMIT

    score = min(score,100)

    return score


# ---------------- BAYESIAN NETWORK ---------------- #

def bayesian_network(board):

    center = center_occupied(board)

    two_row = two_in_row(board)

    probability = win_probability(board)

    return {

        "center_occupied": center,

        "two_in_row": two_row,

        "ai_win_probability": probability,

        "network":

        "Center Occupied -> Two In A Row -> AI Win"
    }