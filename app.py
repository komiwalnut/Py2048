"""Flask web app for Py2048 (Vercel entry: Flask instance named ``app``)."""

import os
from copy import deepcopy

from flask import Flask, jsonify, render_template, request, session

from game import add_new_tile, apply_move, has_valid_moves, new_game, slide_move_transitions

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-insecure-change-for-production")


def _get_board():
    b = session.get("board")
    if not b or len(b) != 4 or any(len(row) != 4 for row in b):
        return None
    return b


def _ensure_game():
    board = _get_board()
    if board is None:
        board = new_game()
        session["board"] = board
        session["over"] = False
        session["won"] = False
    return board


def _max_tile(board):
    return max(cell for row in board for cell in row)


@app.route("/")
def index():
    board = _ensure_game()
    max_tile = _max_tile(board)
    won = bool(session.get("won"))
    over = bool(session.get("over")) or (not has_valid_moves(board))
    return render_template(
        "index.html",
        board=board,
        max_tile=max_tile,
        game_over=over,
        won=won,
    )


@app.post("/api/move")
def api_move():
    payload = request.get_json(silent=True) or {}
    direction = str(payload.get("direction", "")).lower()
    if direction not in ("w", "a", "s", "d"):
        return jsonify(ok=False, error="invalid_direction"), 400

    board = deepcopy(_ensure_game())
    if session.get("over") or not has_valid_moves(board):
        session["over"] = True
        return jsonify(
            ok=True,
            changed=False,
            board=board,
            pre_spawn_board=None,
            spawn=None,
            moves=None,
            game_over=True,
            won=bool(session.get("won")),
            max_tile=_max_tile(board),
        )

    old = deepcopy(board)
    board, changed = apply_move(board, direction)
    pre_spawn = deepcopy(board) if changed else None
    spawn = None
    moves = None
    if changed:
        moves = slide_move_transitions(old, direction)
        spawn = add_new_tile(board)
        session["board"] = board
        if _max_tile(board) >= 2048:
            session["won"] = True
        if not has_valid_moves(board):
            session["over"] = True

    return jsonify(
        ok=True,
        changed=changed,
        board=board,
        pre_spawn_board=pre_spawn,
        spawn={"r": spawn[0], "c": spawn[1], "value": spawn[2]} if spawn else None,
        moves=moves,
        game_over=bool(session.get("over")) or (not has_valid_moves(board)),
        won=bool(session.get("won")),
        max_tile=_max_tile(board),
    )
