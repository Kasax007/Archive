SP=/tmp/claude-0/-home-user-Kasax-Challenge-Craft/2061deb3-7247-5b5c-aa62-6c43681c8da7/scratchpad
cd $SP; . tts/bin/activate
export HF_HOME=$SP/hf SP
for i in 1 2 3 4 5 6 7 8; do
  nice -n 5 python /home/user/archive/shorts/tools/tts_v3.py "$@" 2>> vo3_err.log >> vo3_loop.log && break
done
echo LOOP_END >> vo3_loop.log
