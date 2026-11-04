"""deglitch.py <frames-dir> [factor]: single frames where the pinned camera jumped (knockback between the pose and
the screenshot) are replaced by their predecessor. A frame counts as a jump when it differs from both neighbours much
more than the neighbours differ from each other."""
import sys, os, glob, shutil
from PIL import Image, ImageChops, ImageStat

d = sys.argv[1]
k = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
fs = sorted(glob.glob(os.path.join(d, 'f*.jpg')))
small = [Image.open(f).convert('L').resize((90, 160)) for f in fs]


def diff(a, b):
    return ImageStat.Stat(ImageChops.difference(a, b)).mean[0]


fixed = []
i = 1
while i < len(fs) - 1:
    done = False
    for L in (1, 2, 3, 4, 5, 6):
        if i + L >= len(fs):
            break
        a, c = small[i - 1], small[i + L]
        ac = diff(a, c)
        if ac < 2.5 and all(diff(a, small[j]) > 4.0 for j in range(i, i + L)):
            for j in range(i, i + L):
                shutil.copyfile(fs[i - 1], fs[j])
                small[j] = small[i - 1]
                fixed.append(j)
            i += L
            done = True
            break
    if not done:
        i += 1
print(d, 'replaced', len(fixed), fixed)
