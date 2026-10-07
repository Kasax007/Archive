import {Config} from '@remotion/cli/config';
// Chromium comes from the machine (no download): /opt/pw-browsers
Config.setBrowserExecutable('/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell');
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
Config.setCrf(21);
Config.setConcurrency(2);
Config.setPixelFormat('yuv420p');
