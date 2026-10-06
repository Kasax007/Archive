"""blackjack_life_v3: the voice-over drives the cut.  python blackjack_life_v3.py [--plan]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v3lib
C = 'casino/'
CARD = os.path.join(v3lib.SP, 'film/cards/end_casino')
G = lambda a=1.0, b=1.06, **k: dict(zoom=(a, b), **k)
BEATS = [
    dict(at=None, hook='MINECRAFT, BUT *DYING* IS A CARD GAME', hook_y=360, clips=[
        (C + 'casino_wave', 6.0, 1.0, G(shake=0.3), [(0, 'mc', 'mob/ravager/roar1', 0.6)]),
        (C + 'casino_blackjack', 0.0, 1.0, G(1.0, 1.05, flash=True), [(0, 'mc', 'damage/hit1', 0.7)]),
        (C + 'casino_blackjack', 0.9, 1.2, G(focus=(0.5, 0.42)), [(0, 'casino', 'card_slide1', 0.7)]),
    ]),
    dict(at='In my casino', clips=[
        (C + 'casino_square', 0.5, 1.0, G(speed=1.3), []),
        (C + 'casino_fee', 1.7, 1.3, dict(zoom=(1.25, 1.32), focus=(0.5, 0.12), ui=True), [(0.2, 'mc', 'block/bell/bell_use01', 0.5)]),
        (C + 'casino_fee', 3.4, 1.1, dict(zoom=(1.32, 1.28), focus=(0.5, 0.12), ui=True), [(0.1, 'casino', 'register', 0.8)]),
    ]),
    dict(at="and if you can't", clips=[
        (C + 'casino_bankrupt', 2.4, 1.5, dict(zoom=(1.25, 1.3), focus=(0.5, 0.12), ui=True, shake=0.3), [(0.2, 'casino', 'bankrupt', 0.9), (0.2, 'impact', None, 0.6)]),
        (C + 'casino_bankrupt', 3.5, 1.0, dict(zoom=(1.3, 1.25), focus=(0.5, 0.12), ui=True), []),
    ]),
    dict(at='But when you die', clips=[
        (C + 'casino_wave', 6.6, 1.2, G(shake=0.3), [(0.1, 'casino', 'house_sends', 0.8)]),
        (C + 'casino_blackjack', 0.0, 0.8, G(1.0, 1.05, shake=0.3), [(0.0, 'mc', 'damage/hit1', 0.7)]),
        (C + 'casino_blackjack', 0.3, 1.2, G(focus=(0.4, 0.4)), [(0.2, 'casino', 'lever', 0.5)]),
    ]),
    dict(at='Beat the dealer', clips=[
        (C + 'casino_blackjack', 0.8, 1.2, G(speed=1.3, focus=(0.5, 0.42)), [(0.0, 'casino', 'card_slide1', 0.8), (0.4, 'casino', 'card_place1', 0.8)]),
        (C + 'casino_blackjack', 2.0, 1.2, G(focus=(0.5, 0.42)), [(0.3, 'casino', 'card_flip', 0.8)]),
    ]),
    dict(at='Hit, stand', clips=[
        (C + 'casino_blackjack', 1.6, 1.0, dict(zoom=(1.4, 1.5), focus=(0.15, 0.55), ui=True), [(0.0, 'casino', 'card_place2', 0.8)]),
        (C + 'casino_blackjack', 2.0, 1.0, dict(zoom=(1.4, 1.5), focus=(0.4, 0.55), ui=True), [(0.0, 'casino', 'card_place3', 0.8)]),
        (C + 'casino_blackjack', 2.4, 1.0, dict(zoom=(1.4, 1.5), focus=(0.65, 0.55), ui=True), [(0.0, 'casino', 'card_slide2', 0.8)]),
    ]),
    dict(at='and pray', clips=[
        (C + 'casino_blackjack', 3.0, 1.5, G(focus=(0.5, 0.42)), [(0.0, 'casino', 'card_flip', 0.8)]),
    ]),
    dict(at='And when he does', clips=[
        (C + 'casino_blackjack', 3.9, 1.0, G(focus=(0.5, 0.42), flash=True), [(0.0, 'casino', 'win_small', 0.8)]),
        (C + 'casino_blackjack', 8.55, 1.8, dict(zoom=(1.0, 1.12), punch=True), [(0.5, 'mc', 'item/totem/use_totem', 0.9), (0.5, 'casino', 'revive', 0.7)]),
    ]),
    dict(at="It's one of", clips=[
        ('ui/ui_select', 0.5, 1.2, dict(zoom=(1.7, 1.8), focus=(0.5, 0.35), ui=True), [(0.0, 'mc', 'random/click', 0.5)]),
        ('ui/ui_journey', 0.3, 1.2, dict(zoom=(1.25, 1.32), focus=(0.55, 0.45), ui=True), [(0.0, 'mc', 'random/levelup', 0.4)]),
    ]),
    dict(at='Would you gamble', cap_y=1400, clips=[
        (CARD, 0, 1.0, dict(zoom=(1.0, 1.06)), [(0, 'impact', None, 0.7)]),
    ]),
]
if __name__ == '__main__':
    v3lib.build('blackjack_life_v3', BEATS, plan_only='--plan' in sys.argv)
