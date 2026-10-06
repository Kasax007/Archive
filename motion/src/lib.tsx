import React from 'react';
import {continueRender, delayRender, staticFile} from 'remotion';
import tl from './story_timeline.json';

export const FPS = 30;
export type Word = {w: string; hot: boolean; t0: number; t1: number};
export const words = tl.words as Word[];
export const captions = tl.captions as {t0: number; t1: number; text: string}[];
export const TOTAL_S = tl.total as number;
export const norm = (s: string) => s.toLowerCase().replace(/[^a-z0-9]/g, '');
export const fr = (s: number) => Math.round(s * FPS);

/** seconds at which a phrase of the voice-over starts (first word), searched in spoken order */
export const at = (phrase: string, from = 0): number => {
  const want = phrase.split(/\s+/).map(norm);
  const toks = words.map((w) => norm(w.w));
  for (let i = from; i <= toks.length - want.length; i++) {
    if (want.every((x, k) => toks[i + k] === x)) return words[i].t0;
  }
  throw new Error('phrase not found: ' + phrase);
};

export const YELLOW = '#ffe14d';
export const GOLD = '#ffc42e';
export const RED = '#ff4848';
export const GREEN = '#62eb68';
export const INK = '#10131c';

export const FONT = "'Luckiest', 'Luckiest Guy', Impact, sans-serif";
export const PIXEL = "'PressStart', 'Press Start 2P', monospace";

/** load the local fonts before a frame is rendered */
export const useFonts = () => {
  const [h] = React.useState(() => delayRender('fonts'));
  React.useEffect(() => {
    const f1 = new FontFace('Luckiest', `url(${staticFile('fonts/LuckiestGuy-Regular.ttf')})`);
    const f2 = new FontFace('PressStart', `url(${staticFile('fonts/PressStart2P-Regular.ttf')})`);
    Promise.all([f1.load(), f2.load()])
      .then((fs) => fs.forEach((f) => document.fonts.add(f)))
      .finally(() => continueRender(h));
  }, [h]);
};

export const outline = (px: number, color = '#000'): React.CSSProperties => ({
  WebkitTextStroke: `${px}px ${color}`,
  paintOrder: 'stroke fill',
  textShadow: '0 8px 18px rgba(0,0,0,.55)',
});
