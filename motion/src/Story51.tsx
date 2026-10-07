import React from 'react';
import {AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {Video} from '@remotion/media';
import {staticFile} from 'remotion';
import {at, fr, TOTAL_S, FPS, useFonts, GOLD, RED, YELLOW, GREEN} from './lib';
import {KineticCaption, chunkList, HookWords, Stamp, CommitCard, Commit, Timeline, XpBar, Counter, ChipRain, BobCard, Burst} from './parts';

export const STORY_FRAMES = Math.round(TOTAL_S * FPS);

const COMMITS: Commit[] = [
  {date: '2025-04-24', msg: 'Added Timer'},
  {date: '2025-04-30', msg: 'SkyBlock world generator'},
  {date: '2026-03-01', msg: 'Chunk made of random blocks added as challenge'},
  {date: '2026-03-04', msg: 'Added multiplayer server compatibility'},
  {date: '2026-05-15', msg: 'lockout bingo, no food'},
  {date: '2026-07-20', msg: 'added chal 41-45'},
];

/** a scene between two phrases of the voice-over */
const Scene: React.FC<{a: string | number; b: string | number; children: React.ReactNode}> = ({a, b, children}) => {
  const {fps} = useVideoConfig();
  const s0 = typeof a === 'number' ? a : at(a);
  const s1 = typeof b === 'number' ? b : at(b);
  return (
    <Sequence from={fr(s0)} durationInFrames={Math.max(1, fr(s1) - fr(s0))} premountFor={fps}>
      {children}
    </Sequence>
  );
};

const Cards: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const dt = durationInFrames / COMMITS.length;
  return (
    <>
      {COMMITS.map((c, i) => {
        const born = Math.round(i * dt);
        const newer = COMMITS.reduce((n, _, j) => n + (j > i && Math.round(j * dt) <= frame ? 1 : 0), 0);
        return <CommitCard key={i} c={c} slot={newer} born={born} />;
      })}
    </>
  );
};

const FirstCommit: React.FC = () => {
  const frame = useCurrentFrame();
  const s = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <>
      <Stamp text="24 APRIL 2025" color={GOLD} rot={-3} y={235} size={96} sub="THE FIRST COMMIT" />
      <div style={{opacity: s}}>
        <CommitCard c={{date: '2025-04-24', msg: 'Added challenges', tag: 'first'}} slot={0} born={14} />
      </div>
    </>
  );
};

export const Story51: React.FC<{captions: boolean}> = ({captions}) => {
  useFonts();
  const tHook = at('The floor is');
  const tStart = at('So in April');
  const tMore = at('Then came more');
  const tLevel = at('a level tree');
  const tFifty = at('until there were');
  const tHouse = at('A whole casino');
  const tBob = at('And now');
  const tCalled = at("It's called");
  const inHook = (c: {t0: number}) => c.t0 < tHook - 0.05;
  return (
    <AbsoluteFill style={{background: '#000'}}>
      {/* the cut of the film (V3 edit, with the voice-over and sound effects) */}
      <Video src={staticFile('base.mp4')} />
      {/* soft shading so the graphics read on every shot */}
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,.42) 0%, rgba(0,0,0,0) 30%, rgba(0,0,0,0) 62%, rgba(0,0,0,.35) 100%)'}} />

      <Scene a={0} b={tHook}><HookWords from={0} to={tHook} /></Scene>
      <Scene a="The floor is" b="Every block drops"><Stamp text="THE FLOOR IS LAVA" color={RED} /></Scene>
      <Scene a="Every block drops" b="One heart"><Stamp text="RANDOM DROPS" color={GOLD} rot={3} /></Scene>
      <Scene a="One heart" b="And every time"><Stamp text="ONE HEART" color={RED} sub="FOR THE WHOLE GAME" /></Scene>

      <Scene a={tStart} b={tMore}><FirstCommit /></Scene>
      <Scene a={tMore} b={tLevel}><Cards /></Scene>
      <Scene a={tLevel} b={tFifty}><XpBar /></Scene>
      <Scene a={tFifty} b={tHouse}><Counter /></Scene>
      <Scene a={tStart} b={tHouse}><Timeline /></Scene>

      <Scene a={tHouse} b={tBob}>
        <ChipRain />
        <Stamp text="THE HOUSE ALWAYS WINS" color={GOLD} rot={-3} y={300} size={92} sub="CHALLENGE 50 - THE CASINO" />
      </Scene>
      <Scene a={tBob} b={tCalled}>
        <BobCard />
        <div style={{opacity: 1}}><CommitCard c={{date: '2026-09-30', msg: 'Bot: plays Lockout Bingo', tag: 'bob'}} slot={0} born={20} /></div>
      </Scene>
      <Scene a={tCalled} b={TOTAL_S}><Burst /></Scene>

      {captions && chunkList.map((c, i) => (
        inHook(c) ? null : (
          <Sequence key={i} from={fr(c.t0)} durationInFrames={Math.max(2, fr(c.t1) - fr(c.t0))}>
            <KineticCaption chunk={c} y={c.t0 >= tCalled - 0.05 ? 1400 : 1190} />
          </Sequence>
        )
      ))}
    </AbsoluteFill>
  );
};
