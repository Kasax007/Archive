"""casino_v3: the voice-over drives the cut.  python casino_v3.py [--plan]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v3lib
C = 'casino/'
CARD = os.path.join(v3lib.SP, 'film/cards/end_challenges')
G = lambda a=1.0, b=1.06, **k: dict(zoom=(a, b), **k)
BEATS = [
    dict(at=None, hook='I BUILT A REAL *CASINO* IN MINECRAFT', clips=[
        (C + 'casino_slot_epic_show', 0.0, 1.5, dict(flash=True, zoom=(1.0, 1.08)), [(0, 'casino', 'win_epic', 0.8), (0.1, 'mc', 'fireworks/blast1', 0.4)]),
        (C + 'casino_plinko', 0.8, 1.0, G(focus=(0.5, 0.45)), [(0, 'casino', 'win_big', 0.5)]),
        (C + 'casino_slot_epic', 1.0, 1.0, G(focus=(0.5, 0.55)), [(0, 'casino', 'coins3', 0.6)]),
    ]),
    dict(at='Every item', clips=[
        (C + 'casino_counter', 0.3, 1.5, G(speed=1.3, focus=(0.4, 0.55)), [(0.1, 'casino', 'chip1', 0.6), (0.5, 'casino', 'chip2', 0.6)]),
        (C + 'casino_counter', 1.6, 1.0, G(speed=1.3, focus=(0.4, 0.55)), [(0.1, 'casino', 'chip3', 0.6)]),
    ]),
    dict(at='and the dealer', clips=[
        (C + 'casino_counter', 3.4, 1.2, G(focus=(0.5, 0.45)), [(0.0, 'mc', 'block/bell/bell_use01', 0.6), (0.2, 'casino', 'register', 0.7)]),
        (C + 'casino_counter', 4.2, 1.0, G(focus=(0.5, 0.45)), [(0.0, 'casino', 'coin_shower1', 0.6)]),
    ]),
    dict(at='But every ten', clips=[
        (C + 'casino_fee', 1.7, 1.3, dict(zoom=(1.25, 1.32), focus=(0.5, 0.12), ui=True), [(0.2, 'mc', 'block/bell/bell_use01', 0.5)]),
        (C + 'casino_fee', 3.4, 1.2, dict(zoom=(1.32, 1.28), focus=(0.5, 0.12), ui=True), [(0.1, 'casino', 'register', 0.8)]),
    ]),
    dict(at="and if you can't", clips=[
        (C + 'casino_bankrupt', 2.4, 1.5, dict(zoom=(1.25, 1.3), focus=(0.5, 0.12), ui=True, shake=0.3), [(0.2, 'casino', 'bankrupt', 0.9), (0.2, 'impact', None, 0.6)]),
        (C + 'casino_bankrupt', 3.5, 1.0, dict(zoom=(1.3, 1.25), focus=(0.5, 0.12), ui=True), []),
    ]),
    dict(at='So you can grind', clips=[
        (C + 'casino_square', 0.5, 1.2, G(speed=1.3), []),
        (C + 'casino_square', 2.0, 1.0, G(speed=1.3), []),
    ]),
    dict(at='Spin the slots', clips=[
        (C + 'casino_slot_freespins_intro', 1.4, 1.2, G(focus=(0.5, 0.45)), [(0.0, 'casino', 'free_spins', 0.8)]),
        (C + 'casino_slot_spins', 0.1, 1.0, G(focus=(0.5, 0.45)), [(0.0, 'casino', 'reel_spin', 0.5)]),
    ]),
    dict(at='drop the Plinko', clips=[
        (C + 'casino_plinko', 0.2, 1.0, G(focus=(0.5, 0.45)), []),
        (C + 'casino_plinko', 1.2, 1.0, G(focus=(0.5, 0.5)), [(0.2, 'casino', 'win_big', 0.8)]),
    ]),
    dict(at='and cash out', clips=[
        (C + 'casino_crash_launch', 0.5, 0.8, G(focus=(0.4, 0.4)), [(0.1, 'casino', 'rocket_launch', 0.8)]),
        (C + 'casino_crash_climb', 0.0, 1.0, G(speed=4.0, focus=(0.62, 0.42)), [(0.0, 'casino', 'rocket_flight', 0.6)]),
        (C + 'casino_crash_cashout', 0.4, 1.2, G(focus=(0.62, 0.45), flash=True), [(0.1, 'casino', 'cash_out', 0.9), (0.2, 'casino', 'coin_shower2', 0.7)]),
    ]),
    dict(at='And if you die', clips=[
        (C + 'casino_wave', 5.3, 1.0, G(shake=0.3), [(0.2, 'casino', 'house_sends', 0.8)]),
        (C + 'casino_blackjack', 0.0, 1.0, G(1.0, 1.05), [(0.0, 'mc', 'damage/hit1', 0.7)]),
    ]),
    dict(at='You play Blackjack', clips=[
        (C + 'casino_blackjack', 0.8, 1.5, G(speed=1.3, focus=(0.5, 0.42)), [(0.0, 'casino', 'card_slide1', 0.8), (0.4, 'casino', 'card_place1', 0.8)]),
        (C + 'casino_blackjack', 2.6, 1.2, G(focus=(0.5, 0.42)), [(0.3, 'casino', 'card_flip', 0.8)]),
    ]),
    dict(at="It's one of", clips=[
        ('ui/ui_select', 0.5, 1.3, dict(zoom=(1.7, 1.8), focus=(0.5, 0.35), ui=True), [(0.0, 'mc', 'random/click', 0.5)]),
        ('ui/ui_journey', 0.3, 1.3, dict(zoom=(1.25, 1.32), focus=(0.55, 0.45), ui=True), [(0.0, 'mc', 'random/levelup', 0.4)]),
    ]),
    dict(at='Would you gamble', end='WOULD YOU *GAMBLE*?', end_at=0.1, clips=[
        (CARD, 0, 1.0, dict(zoom=(1.0, 1.06)), [(0, 'impact', None, 0.7)]),
    ]),
]
if __name__ == '__main__':
    v3lib.build('casino_v3', BEATS, plan_only='--plan' in sys.argv)
