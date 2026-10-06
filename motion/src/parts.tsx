import React from 'react';
import {AbsoluteFill, Easing, interpolate, random, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {FONT, PIXEL, YELLOW, GOLD, GREEN, INK, RED, FPS, outline, words, captions, norm} from './lib';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

/* ---------------------------------------------------------------- kinetic captions (word by word) */
type Chunk = {t0: number; t1: number; words: {w: string; hot: boolean; t0: number}[]};
const chunks: Chunk[] = (() => {
  let cur = 0;
  return captions.map((c) => {
    const n = c.text.split(/\s+/).length;
    const ws = words.slice(cur, cur + n).map((w) => ({w: w.w, hot: w.hot, t0: w.t0}));
    cur += n;
    return {t0: c.t0, t1: c.t1, words: ws};
  });
})();
export const chunkList = chunks;

export const KineticCaption: React.FC<{chunk: Chunk; size?: number; y?: number}> = ({chunk, size = 78, y = 1190}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const now = chunk.t0 + frame / fps;
  return (
    <div style={{position: 'absolute', left: 70, right: 70, top: y, display: 'flex', flexWrap: 'wrap', justifyContent: 'center',
      gap: `6px ${Math.round(size * 0.26)}px`, fontFamily: FONT, fontSize: size, lineHeight: 1.05, textAlign: 'center'}}>
      {chunk.words.map((w, i) => {
        const age = now - w.t0;
        const nextT = chunk.words[i + 1]?.t0 ?? chunk.t1;
        const active = age >= 0 && now < nextT;
        const s = spring({frame: Math.max(0, Math.round(age * fps)), fps, config: {damping: 11, stiffness: 220}, durationInFrames: 14});
        const scale = age < 0 ? 0.6 : interpolate(s, [0, 1], [0.6, 1]) * (active ? 1.1 : 1);
        return (
          <span key={i} style={{display: 'inline-block', opacity: age < -0.02 ? 0 : 1, transform: `scale(${scale}) translateY(${age < 0 ? 18 : 0}px)`,
            color: w.hot ? YELLOW : active ? '#fff' : '#f2f2f2', ...outline(size * 0.12)}}>{w.w}</span>
        );
      })}
    </div>
  );
};

/* ---------------------------------------------------------------- the hook: words slam in, big */
export const HookWords: React.FC<{from: number; to: number}> = ({from, to}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const now = from + frame / fps;
  const ws = words.filter((w) => w.t0 >= from - 0.01 && w.t0 < to);
  const fade = interpolate(frame, [(to - from) * fps - 8, (to - from) * fps], [1, 0], clamp);
  return (
    <div style={{position: 'absolute', left: 60, right: 60, top: 250, display: 'flex', flexWrap: 'wrap', justifyContent: 'center',
      gap: '4px 26px', fontFamily: FONT, fontSize: 118, lineHeight: 1.0, textAlign: 'center', opacity: fade}}>
      {ws.map((w, i) => {
        const age = now - w.t0;
        const s = spring({frame: Math.max(0, Math.round(age * fps)), fps, config: {damping: 9, stiffness: 260}, durationInFrames: 16});
        const rot = (i % 2 ? 1 : -1) * 2.5;
        const big = w.hot || /^(craziest|challenges)/i.test(w.w);
        return (
          <span key={i} style={{display: 'inline-block', opacity: age < -0.02 ? 0 : 1, color: big ? YELLOW : '#fff',
            transform: `rotate(${rot}deg) scale(${age < 0 ? 0.3 : interpolate(s, [0, 1], [2.2, 1])})`, ...outline(13)}}>{w.w.replace(/[.,]$/, '')}</span>
        );
      })}
    </div>
  );
};

/* ---------------------------------------------------------------- a stamp that slams on */
export const Stamp: React.FC<{text: string; color?: string; rot?: number; y?: number; size?: number; sub?: string}> = ({text, color = RED, rot = -4, y = 330, size = 104, sub}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 10, stiffness: 300}, durationInFrames: 14});
  const out = interpolate(frame, [durationInFrames - 6, durationInFrames], [1, 0], clamp);
  const sh = frame < 6 ? Math.sin(frame * 3) * (6 - frame) * 2 : 0;
  return (
    <div style={{position: 'absolute', left: 40, right: 40, top: y, textAlign: 'center', opacity: out,
      transform: `translateX(${sh}px) rotate(${rot}deg) scale(${interpolate(s, [0, 1], [2.4, 1])})`}}>
      <div style={{display: 'inline-block', padding: '10px 34px 6px', border: `10px solid ${color}`, borderRadius: 14, background: 'rgba(10,10,14,.72)',
        fontFamily: FONT, fontSize: size, color, lineHeight: 1.02, letterSpacing: 2, textShadow: '0 6px 0 rgba(0,0,0,.6)'}}>
        {text}
        {sub && <div style={{fontFamily: PIXEL, fontSize: 26, color: '#fff', letterSpacing: 1, marginTop: 8, paddingBottom: 6}}>{sub}</div>}
      </div>
    </div>
  );
};

/* ---------------------------------------------------------------- commit cards */
export type Commit = {date: string; msg: string; tag?: string};
export const CommitCard: React.FC<{c: Commit; slot: number; born: number}> = ({c, slot, born}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const age = frame - born;
  if (age < 0) return null;
  const s = spring({frame: age, fps, config: {damping: 14, stiffness: 160}});
  const sl = spring({frame: age, fps, config: {damping: 16, stiffness: 120}}); // slot moves down
  const x = interpolate(s, [0, 1], [1200, 0]);
  const fade = interpolate(slot, [0, 2.2, 3.2], [1, 0.75, 0], clamp);
  return (
    <div style={{position: 'absolute', left: 50, right: 50, top: (c.tag === "bob" ? 520 : c.tag === "first" ? 560 : 230) + slot * 150, opacity: fade, transform: `translateX(${x}px)`}}>
      <div style={{display: 'flex', background: 'rgba(14,17,26,.92)', borderRadius: 10, overflow: 'hidden', boxShadow: '0 10px 30px rgba(0,0,0,.5)', border: '2px solid #2b3144'}}>
        <div style={{width: 14, background: c.tag ? GOLD : GREEN}} />
        <div style={{padding: '16px 22px', flex: 1, minWidth: 0}}>
          <div style={{fontFamily: PIXEL, fontSize: 20, color: '#8fa0c8', marginBottom: 10}}>
            {'●'} COMMIT &nbsp;{c.date}
          </div>
          <div style={{fontFamily: PIXEL, fontSize: 25, color: '#fff', lineHeight: 1.35, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>{c.msg}</div>
        </div>
      </div>
    </div>
  );
};

/* ---------------------------------------------------------------- timeline strip */
const D0 = Date.UTC(2025, 3, 24), D1 = Date.UTC(2026, 9, 1);
const dx = (y: number, m: number, d: number) => (Date.UTC(y, m - 1, d) - D0) / (D1 - D0);
export const MILESTONES = [
  {p: dx(2025, 4, 24), label: 'FIRST COMMIT', sub: 'APR 2025'},
  {p: dx(2026, 3, 2), label: 'LEVEL SYSTEM', sub: 'MAR 2026'},
  {p: dx(2026, 5, 15), label: 'LOCKOUT BINGO', sub: 'MAY 2026'},
  {p: dx(2026, 7, 20), label: 'CHALLENGES 41-45', sub: 'JUL 2026'},
  {p: dx(2026, 9, 28), label: 'CHALLENGE 50', sub: 'SEP 2026'},
];
export const Timeline: React.FC<{y?: number}> = ({y = 1500}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const prog = interpolate(frame, [4, durationInFrames - 4], [0, 1], {...clamp, easing: Easing.inOut(Easing.quad)});
  const L = 100, R = 980, W = R - L;
  const appear = interpolate(frame, [0, 10], [0, 1], clamp);
  return (
    <div style={{position: 'absolute', left: 0, top: y, width: 1080, height: 260, opacity: appear}}>
      <div style={{position: 'absolute', left: L, top: 100, width: W, height: 10, background: '#333a4d', borderRadius: 5}} />
      <div style={{position: 'absolute', left: L, top: 100, width: W * prog, height: 10, background: GOLD, borderRadius: 5, boxShadow: `0 0 18px ${GOLD}`}} />
      <div style={{position: 'absolute', left: L + W * prog - 16, top: 89, width: 32, height: 32, background: '#fff', borderRadius: 16, border: `6px solid ${GOLD}`}} />
      {MILESTONES.map((m, i) => {
        const on = prog >= m.p - 0.002;
        const above = i % 2 === 0;
        const x = L + W * m.p;
        const born = interpolate(prog, [m.p - 0.002, m.p + 0.04], [0, 1], clamp);
        return (
          <div key={i} style={{position: 'absolute', left: x - 110, width: 220, top: above ? 4 : 128, textAlign: 'center', opacity: on ? 1 : 0.28,
            transform: `scale(${on ? 0.8 + 0.2 * born : 0.9})`}}>
            {above && <Label m={m} on={on} />}
            {!above && <Label m={m} on={on} />}
            <div style={{position: 'absolute', left: 95, top: above ? 62 : -22, width: 30, height: 30, borderRadius: 4, background: on ? GOLD : '#555d75', border: '4px solid #10131c', transform: 'rotate(45deg)'}} />
          </div>
        );
      })}
    </div>
  );
};
const Label: React.FC<{m: {label: string; sub: string}; on: boolean}> = ({m, on}) => (
  <div style={{display: 'inline-block', padding: '8px 10px', background: 'rgba(12,14,22,.85)', borderRadius: 8, border: `2px solid ${on ? GOLD : '#394058'}`}}>
    <div style={{fontFamily: PIXEL, fontSize: 15, color: '#fff', whiteSpace: 'nowrap'}}>{m.label}</div>
    <div style={{fontFamily: PIXEL, fontSize: 12, color: GOLD, marginTop: 6}}>{m.sub}</div>
  </div>
);

/* ---------------------------------------------------------------- XP bar and level */
export const XpBar: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames, fps} = useVideoConfig();
  const p = interpolate(frame, [6, durationInFrames - 6], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const lvl = Math.max(1, Math.round(p * 20));
  const pop = spring({frame, fps, config: {damping: 12, stiffness: 180}});
  return (
    <div style={{position: 'absolute', left: 60, right: 60, top: 270, transform: `scale(${interpolate(pop, [0, 1], [0.8, 1])})`, opacity: pop}}>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: 12}}>
        <div style={{fontFamily: PIXEL, fontSize: 24, color: '#fff', ...outline(0)}}>LIFETIME XP</div>
        <div style={{fontFamily: FONT, fontSize: 96, color: YELLOW, lineHeight: 0.9, ...outline(10)}}>LEVEL {lvl}</div>
      </div>
      <div style={{height: 54, background: '#1a1f2e', border: '6px solid #000', borderRadius: 10, overflow: 'hidden'}}>
        <div style={{width: `${p * 100}%`, height: '100%', background: `linear-gradient(90deg, ${GREEN}, #b8ff6a)`, boxShadow: `0 0 30px ${GREEN}`}} />
      </div>
      <div style={{fontFamily: PIXEL, fontSize: 18, color: '#c9d4f2', marginTop: 12, textAlign: 'right'}}>LEVEL 1 - 20 &nbsp;UNLOCKS CHALLENGES + PERKS</div>
    </div>
  );
};

/* ---------------------------------------------------------------- counter 0 -> 50, then version badges */
export const Counter: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const n = Math.round(interpolate(frame, [4, 4 + 1.1 * fps], [0, 50], {...clamp, easing: Easing.out(Easing.cubic)}));
  const hit = spring({frame: Math.max(0, frame - (4 + 1.1 * fps)), fps, config: {damping: 8, stiffness: 260}, durationInFrames: 18});
  const sc = frame > 4 + 1.1 * fps ? interpolate(hit, [0, 1], [1.25, 1]) : 1;
  const vers = ['1.21.5', '26.1.2', '26.2', '26.3'];
  return (
    <>
      <div style={{position: 'absolute', left: 0, right: 0, top: 215, textAlign: 'center', transform: `scale(${sc})`}}>
        <div style={{fontFamily: FONT, fontSize: 330, lineHeight: 0.95, color: n >= 50 ? YELLOW : '#fff', ...outline(18)}}>{n}</div>
        <div style={{fontFamily: FONT, fontSize: 92, color: '#fff', ...outline(10), marginTop: -6}}>CHALLENGES</div>
      </div>
      <div style={{position: 'absolute', left: 30, right: 30, top: 760, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 12}}>
        {vers.map((v, i) => {
          const b = 4 + 1.3 * fps + i * 7;
          const s = spring({frame: Math.max(0, frame - b), fps, config: {damping: 12, stiffness: 220}});
          return (
            <React.Fragment key={v}>
              {i > 0 && <span style={{fontFamily: PIXEL, fontSize: 24, color: GOLD, opacity: frame >= b ? 1 : 0}}>{'>'}</span>}
              <div style={{opacity: frame >= b ? 1 : 0, transform: `scale(${interpolate(s, [0, 1], [0.4, 1])})`, padding: '12px 14px', background: 'rgba(14,17,26,.92)',
                border: `3px solid ${i === 3 ? GOLD : '#3a4260'}`, borderRadius: 8, fontFamily: PIXEL, fontSize: 24, color: i === 3 ? GOLD : '#fff'}}>{v}</div>
            </React.Fragment>
          );
        })}
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 835, textAlign: 'center', fontFamily: PIXEL, fontSize: 17, color: '#c9d4f2',
        opacity: interpolate(frame, [4 + 1.3 * fps, 4 + 1.3 * fps + 10], [0, 1], clamp)}}>MINECRAFT VERSIONS SUPPORTED OVER TIME</div>
    </>
  );
};

/* ---------------------------------------------------------------- casino chip rain */
export const ChipRain: React.FC<{n?: number}> = ({n = 46}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  return (
    <AbsoluteFill style={{pointerEvents: 'none', overflow: 'hidden'}}>
      {Array.from({length: n}).map((_, i) => {
        const x = random('cx' + i) * 1000 + 20;
        const start = random('cs' + i) * durationInFrames * 0.5;
        const speed = 22 + random('cv' + i) * 18;
        const size = 62 + random('cz' + i) * 40;
        const t = frame - start;
        if (t < 0) return null;
        const y = -120 + t * speed * 0.9 + 0.5 * 0.9 * t * t * 0.5;
        const spin = (random('cr' + i) * 2 - 1) * 14;
        const squash = Math.abs(Math.cos((t * spin) / 30));
        const col = ['#e03c3c', '#2f7de0', '#2fbf5a', '#111', GOLD][i % 5];
        return (
          <div key={i} style={{position: 'absolute', left: x, top: y, width: size, height: size, borderRadius: '50%', background: col,
            border: '5px dashed #fff', boxShadow: '0 6px 14px rgba(0,0,0,.5), inset 0 0 0 6px rgba(0,0,0,.25)',
            transform: `scaleX(${0.25 + 0.75 * squash}) rotate(${t * 3}deg)`}} />
        );
      })}
    </AbsoluteFill>
  );
};

/* ---------------------------------------------------------------- Bob */
export const BobCard: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 13, stiffness: 170}});
  const lines = ['LOCKOUT BINGO', 'AI OPPONENT', 'STILL LEARNING'];
  const blink = Math.floor(frame / 8) % 2 === 0;
  return (
    <div style={{position: 'absolute', left: 60, right: 60, top: 250, transform: `translateY(${interpolate(s, [0, 1], [-260, 0])}px)`}}>
      <div style={{display: 'flex', gap: 26, alignItems: 'center', background: 'rgba(14,17,26,.92)', border: '3px solid #3a4260', borderRadius: 14, padding: 24}}>
        <div style={{width: 150, height: 150, background: '#7d8aa8', borderRadius: 14, position: 'relative', border: '6px solid #10131c', flex: 'none'}}>
          <div style={{position: 'absolute', left: 28, top: 44, width: 28, height: blink ? 28 : 8, background: '#7dffb0', borderRadius: 4, boxShadow: '0 0 14px #7dffb0'}} />
          <div style={{position: 'absolute', right: 28, top: 44, width: 28, height: blink ? 28 : 8, background: '#7dffb0', borderRadius: 4, boxShadow: '0 0 14px #7dffb0'}} />
          <div style={{position: 'absolute', left: 40, right: 40, bottom: 28, height: 12, background: '#10131c', borderRadius: 3}} />
          <div style={{position: 'absolute', left: 70, top: -26, width: 10, height: 22, background: '#10131c'}} />
          <div style={{position: 'absolute', left: 60, top: -40, width: 30, height: 18, background: RED, borderRadius: 9}} />
        </div>
        <div style={{flex: 1}}>
          <div style={{fontFamily: FONT, fontSize: 96, color: YELLOW, lineHeight: 1, ...outline(8)}}>BOB</div>
          {lines.map((l, i) => {
            const st = 8 + i * 9;
            const n = Math.max(0, Math.min(l.length, Math.floor((frame - st) * 1.6)));
            return <div key={i} style={{fontFamily: PIXEL, fontSize: 20, color: i === 2 ? GOLD : '#c9d4f2', marginTop: 12, height: 26}}>{l.slice(0, n)}</div>;
          })}
        </div>
      </div>
    </div>
  );
};

export const Burst: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {Array.from({length: 34}).map((_, i) => {
        const a = random('a' + i) * Math.PI * 2;
        const v = 8 + random('v' + i) * 22;
        const t = frame;
        const x = 540 + Math.cos(a) * v * t * 1.4;
        const y = 640 + Math.sin(a) * v * t * 1.4 + 0.6 * t * t;
        const col = ['#6cc4ff', '#b48cff', '#7dff9a', '#ffe14d', '#ff7aa8'][i % 5];
        return <div key={i} style={{position: 'absolute', left: x, top: y, width: 18, height: 18, background: col, opacity: interpolate(t, [0, 40], [1, 0], clamp)}} />;
      })}
    </AbsoluteFill>
  );
};
