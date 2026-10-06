"""challenges_v3: the voice-over drives the cut.  python challenges_v3.py [--plan]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v3lib
from cut import YELLOW, GOLD, RED, GREEN

H, C = 'chal/', 'casino/'
CARD = os.path.join(v3lib.SP, 'film/cards/end_challenges')
W_ = lambda g=0.4: (0, 'whoosh', None, g)
BEATS = [
    dict(at=None, hook='*VIRAL* CHALLENGES. IN MINECRAFT.', clips=[
        (H + 'size_matters', 0.3, 1.4, dict(zoom=(1.0, 1.06)), [(0, 'mc', 'mob/creeper/say1', 0.5)]),
        (H + 'chunk_blocks', 1.0, 1.4, dict(zoom=(1.0, 1.06)), []),
        (H + 'floor_lava', 0.8, 1.4, dict(zoom=(1.0, 1.06)), [(0, 'mc', 'fire/ignite', 0.5)]),
    ]),
    dict(at='In Red Light', clips=[
        (H + 'red_light', 1.8, 1.2, dict(zoom=(1.0, 1.07), focus=(0.5, 0.4)), [(0.0, 'mc', 'note/bell', 0.5)]),
        (H + 'red_light', 3.9, 1.2, dict(speed=1.2, zoom=(1.0, 1.07), focus=(0.5, 0.4)), []),
        (H + 'red_light', 5.0, 0.8, dict(zoom=(1.07, 1.1), focus=(0.5, 0.4), punch=True), [(0.2, 'mc', 'note/bass', 0.8)]),
        (H + 'red_light', 5.7, 1.6, dict(shake=0.4, flash=True), [(0.0, 'mc', 'damage/hit1', 0.8)]),
    ]),
    dict(at='Dice lets', clips=[
        (H + 'dice_throw', 0.3, 1.0, dict(zoom=(1.0, 1.06)), [(0.2, 'mc', 'random/bow', 0.4)]),
        (H + 'dice_throw', 1.6, 1.0, dict(zoom=(1.0, 1.06)), [(0.0, 'mc', 'random/pop', 0.5)]),
    ]),
    dict(at='Every chunk', clips=[
        (H + 'chunk_blocks', 2.2, 1.0, dict(zoom=(1.0, 1.07)), []),
        (H + 'chunk_blocks', 4.5, 1.0, dict(zoom=(1.0, 1.06)), []),
    ]),
    dict(at='the floor burns', clips=[
        (H + 'floor_lava', 1.4, 1.0, dict(zoom=(1.0, 1.07), focus=(0.5, 0.45)), [(0.6, 'mc', 'fire/ignite', 0.6)]),
        (H + 'floor_lava', 3.0, 1.0, dict(zoom=(1.0, 1.06), focus=(0.5, 0.45)), [(0.0, 'mc', 'damage/hit2', 0.5)]),
    ]),
    dict(at='and one zombie', clips=[
        (H + 'double_trouble', 0.9, 1.0, dict(zoom=(1.0, 1.06), focus=(0.45, 0.55)), [(0.0, 'mc', 'mob/zombie/say1', 0.6)]),
        (H + 'double_trouble', 1.7, 1.8, dict(zoom=(1.0, 1.12), focus=(0.5, 0.55), shake=0.35, flash=True, punch=True), [(0.0, 'impact', None, 0.6), (0.5, 'mc', 'mob/zombie/say2', 0.6)]),
    ]),
    dict(at="And here's the best", clips=[
        (H + 'force_item', 0.5, 1.0, dict(zoom=(1.0, 1.06), focus=(0.5, 0.45)), [(0.3, 'mc', 'random/orb', 0.5)]),
        (H + 'force_item', 1.8, 1.0, dict(zoom=(1.0, 1.05), focus=(0.5, 0.45)), []),
    ]),
    dict(at='or play against', clips=[
        (H + 'lockout_bob_run', 0.0, 1.2, dict(zoom=(1.0, 1.07)), []),
        (H + 'lockout_bob_run', 2.0, 1.0, dict(zoom=(1.0, 1.06)), []),
        (H + 'lockout_board', 0.5, 1.0, dict(zoom=(1.0, 1.06)), [(0, 'mc', 'random/click', 0.4)]),
    ]),
    dict(at='Stack challenges', clips=[
        ('ui/ui_select', 0.4, 1.4, dict(zoom=(1.7, 1.8), focus=(0.5, 0.35), ui=True), [(0.2, 'mc', 'random/click', 0.5)]),
        ('ui/ui_select', 1.6, 1.0, dict(zoom=(1.8, 1.7), focus=(0.5, 0.6), ui=True), [(0.2, 'mc', 'random/click', 0.5)]),
        ('ui/ui_journey', 0.2, 1.4, dict(zoom=(1.25, 1.32), focus=(0.55, 0.45), ui=True), [(0.0, 'mc', 'random/levelup', 0.4)]),
    ]),
    dict(at="It's called", cap_y=1400, clips=[
        (H + 'skyblock', 0.3, 1.0, dict(zoom=(1.0, 1.06)), []),
        (CARD, 0, 1.0, dict(zoom=(1.0, 1.04)), [(0, 'impact', None, 0.7)]),
    ]),
    dict(at='So which', cap_y=1400, clips=[
        (CARD, 0, 1.0, dict(zoom=(1.04, 1.07)), []),
    ]),
]
if __name__ == '__main__':
    v3lib.build('challenges_v3', BEATS, plan_only='--plan' in sys.argv)
