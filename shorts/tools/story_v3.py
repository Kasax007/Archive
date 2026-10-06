"""story_v3 (Short 5): how Challenge Craft came to be.  python story_v3.py [--plan]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v3lib
H, C = 'chal/', 'casino/'
CARD = os.path.join(v3lib.SP, 'film/cards/end_challenges')
G = lambda a=1.0, b=1.06, **k: dict(zoom=(a, b), **k)
M = lambda shot, st: (H + shot, st, 1.0, G(1.0, 1.05), [(0, 'whoosh', None, 0.25)])
BEATS = [
    dict(at=None, hook='HOW A MOD MADE *VIRAL CHALLENGES* PLAYABLE', clips=[
        (H + 'size_matters', 0.3, 1.2, G(), []),
        (H + 'upside_down', 1.2, 1.2, G(), []),
        (H + 'double_trouble', 1.6, 1.2, G(), [(0, 'mc', 'mob/zombie/say1', 0.4)]),
    ]),
    dict(at='The floor is', clips=[(H + 'floor_lava', 0.8, 1.0, G(1.0, 1.07, focus=(0.5, 0.45)), [(0.2, 'mc', 'fire/ignite', 0.5)])]),
    dict(at='Every block drops', clips=[(H + 'upside_down', 1.0, 1.0, G(1.0, 1.07), [(0.3, 'mc', 'random/pop', 0.5)])]),
    dict(at='One heart', clips=[(H + 'red_light', 5.5, 1.0, G(1.0, 1.05, shake=0.3), [(0.2, 'mc', 'damage/hit1', 0.7)])]),
    dict(at='And every time', clips=[
        (H + 'chunk_blocks', 1.0, 1.3, G(), []),
        (H + 'skyblock', 0.3, 1.2, G(), []),
    ]),
    dict(at='So in April', clips=[
        (H + 'skyblock', 1.2, 1.2, G(), [(0, 'mc', 'random/levelup', 0.4)]),
        ('ui/ui_select', 0.4, 1.4, dict(zoom=(1.7, 1.8), focus=(0.5, 0.35), ui=True), [(0.2, 'mc', 'random/click', 0.5)]),
    ]),
    dict(at='Then came more', clips=[
        M('cushion', 1.0), M('chunk_blocks', 3.0), M('floor_lava', 2.0), M('size_matters', 1.3),
        M('dice_throw', 1.0), M('double_trouble', 1.7), M('red_light', 4.0), M('upside_down', 2.0),
    ]),
    dict(at='a level tree', clips=[
        ('ui/ui_journey', 0.2, 1.4, dict(zoom=(1.25, 1.32), focus=(0.55, 0.45), ui=True), [(0, 'mc', 'random/levelup', 0.5)]),
        ('ui/ui_journey', 1.8, 1.0, dict(zoom=(1.32, 1.25), focus=(0.55, 0.6), ui=True), []),
    ]),
    dict(at='until there were', clips=[
        ('ui/ui_select', 1.4, 1.0, dict(zoom=(1.8, 1.7), focus=(0.5, 0.6), ui=True), [(0.2, 'mc', 'random/click', 0.5)]),
        ('ui/ui_summary', 0.2, 1.0, dict(zoom=(1.5, 1.6), focus=(0.5, 0.55), ui=True), [(0.0, 'mc', 'random/orb', 0.5)]),
    ]),
    dict(at='Then I went', clips=[(C + 'casino_square', 0.8, 1.0, G(speed=1.3), [(0, 'impact', None, 0.5)])]),
    dict(at='A whole casino', clips=[
        (C + 'casino_slot_epic_show', 0.0, 1.2, G(1.0, 1.08, flash=True), [(0, 'casino', 'win_epic', 0.7)]),
        (C + 'casino_roulette_spin', 10.9, 1.0, G(), [(0.1, 'casino', 'roulette_drop', 0.6)]),
        (C + 'casino_blackjack', 8.9, 1.0, G(), [(0, 'mc', 'item/totem/use_totem', 0.5)]),
    ]),
    dict(at='And now', clips=[
        (H + 'lockout_bob_run', 0.0, 1.3, G(), []),
        (H + 'lockout_board', 0.5, 1.2, G(), [(0, 'mc', 'random/click', 0.4)]),
        (H + 'lockout_bob_run', 2.0, 1.0, G(), []),
    ]),
    dict(at="It's called", cap_y=1400, clips=[(CARD, 0, 1.0, dict(zoom=(1.0, 1.04)), [(0, 'impact', None, 0.7)])]),
    dict(at='and this is only', cap_y=1400, end='THIS IS ONLY THE *BEGINNING*', end_at=0.0, clips=[(CARD, 0, 1.0, dict(zoom=(1.04, 1.07)), [])]),
]
if __name__ == '__main__':
    v3lib.build('story_v3', BEATS, plan_only='--plan' in sys.argv)
