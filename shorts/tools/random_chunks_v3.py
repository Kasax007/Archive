"""random_chunks_v3: the voice-over drives the cut.  python random_chunks_v3.py [--plan]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v3lib
H = 'chal/'
CARD = os.path.join(v3lib.SP, 'film/cards/end_challenges')
G = lambda a=1.0, b=1.06, **k: dict(zoom=(a, b), **k)
BEATS = [
    dict(at=None, hook='EVERY CHUNK IS *ONE RANDOM BLOCK*', hook_y=360, clips=[
        (H + 'chunk_blocks', 1.2, 1.5, G(), [(0, 'mc', 'random/orb', 0.4)]),
        (H + 'chunk_walk', 0.2, 1.5, G(flash=True), []),
        (H + 'chunk_blocks', 4.0, 1.0, G(), []),
    ]),
    dict(at='Walk sixteen', clips=[
        (H + 'chunk_walk', 0.0, 1.3, G(speed=0.8), [(0, 'whoosh', None, 0.4)]),
        (H + 'chunk_walk', 1.2, 1.3, G(speed=0.8), [(0.8, 'mc', 'random/pop', 0.5)]),
    ]),
    dict(at='One chunk is gold', clips=[
        (H + 'chunk_walk', 0.0, 1.0, G(speed=0.35, focus=(0.5, 0.75)), [(0, 'casino', 'coins3', 0.5)]),
    ]),
    dict(at='the next is redstone', clips=[
        (H + 'chunk_walk', 0.42, 1.0, G(speed=0.5, focus=(0.5, 0.75)), [(0, 'mc', 'random/orb', 0.5)]),
    ]),
    dict(at='then diamond', clips=[
        (H + 'chunk_walk', 1.15, 1.0, G(speed=0.6, focus=(0.5, 0.75)), [(0, 'mc', 'random/levelup', 0.4)]),
    ]),
    dict(at='then emerald', clips=[
        (H + 'chunk_walk', 2.0, 1.0, G(speed=0.6, focus=(0.5, 0.75)), [(0, 'mc', 'random/orb', 0.6)]),
    ]),
    dict(at='And from above', clips=[
        (H + 'chunk_blocks', 1.8, 1.2, G(1.0, 1.07), [(0, 'whoosh', None, 0.4)]),
        (H + 'chunk_blocks', 3.0, 1.2, G(), []),
        (H + 'chunk_blocks', 5.0, 1.2, G(1.0, 1.1, punch=True), [(0.1, 'impact', None, 0.5)]),
    ]),
    dict(at='Every step', clips=[
        (H + 'chunk_walk', 2.8, 1.3, G(speed=0.8), [(0, 'mc', 'random/pop', 0.5)]),
        (H + 'chunk_blocks', 6.0, 1.3, G(), []),
    ]),
    dict(at="It's one of", clips=[
        ('ui/ui_select', 0.5, 1.2, dict(zoom=(1.7, 1.8), focus=(0.5, 0.35), ui=True), [(0.0, 'mc', 'random/click', 0.5)]),
        ('ui/ui_journey', 0.3, 1.2, dict(zoom=(1.25, 1.32), focus=(0.55, 0.45), ui=True), [(0.0, 'mc', 'random/levelup', 0.4)]),
    ]),
    dict(at='Would you survive', cap_y=1400, clips=[
        (CARD, 0, 1.0, dict(zoom=(1.0, 1.06)), [(0, 'impact', None, 0.7)]),
    ]),
]
if __name__ == '__main__':
    v3lib.build('random_chunks_v3', BEATS, plan_only='--plan' in sys.argv)
