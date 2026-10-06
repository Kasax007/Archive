# deliver.sh NAME  (e.g. challenges_v3): copy the finished files to shorts/v3 and the send folder
SP=/tmp/claude-0/-home-user-Kasax-Challenge-Craft/2061deb3-7247-5b5c-aa62-6c43681c8da7/scratchpad
N=$1; D=/home/user/archive/shorts/v3; S=$SP/out3; X=$SP/out/send-v3
mkdir -p $X
for k in final clean; do cp $S/${N}_$k.mp4 $D/; cp $S/${N}_$k.mp4 $X/; done
cp $S/$N.srt $D/; cp $S/$N.srt $X/
cp $S/${N}_voice.m4a $D/; cp $S/${N}_voice.m4a $X/
cp $S/${N}_sheet.png $X/
ls -la $D | grep $N
