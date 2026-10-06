import React from 'react';
import {Composition} from 'remotion';
import {Story51, STORY_FRAMES} from './Story51';

export const Root: React.FC = () => (
  <>
    {/* captions=true: kinetic word captions burnt in (_final); false: graphics only (_clean) */}
    <Composition id="Story51" component={Story51} durationInFrames={STORY_FRAMES} fps={30} width={1080} height={1920}
      defaultProps={{captions: true}} />
    <Composition id="Story51Clean" component={Story51} durationInFrames={STORY_FRAMES} fps={30} width={1080} height={1920}
      defaultProps={{captions: false}} />
  </>
);
