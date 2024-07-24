# RepeaterAnnouncements
 
Overview:
Add a repeater announcement engine if your controller does not have one. This script runs on a linux computer (Le Potato/Rasberry Pi) and we use it with a seperate radio $20 low power Boefeng using VOX, but cen be wired in to the repeater with some extra configuration. 

Example Schedule via Cron:
```
#Welcome - between 6am and 8pm every two hours
0 6-20/2 * * * /root/Announcements.py /root/WelcomeMessage.wav 30 0

#Net Invite - every day 3:15pm
15 15 * * * /root/Announcements.py /root/Net\ Invite.wav 30 0

#Net Tonight - Wednesday at 3pm
0 15 * * 3 /root/Announcements.py /root/NetTonight.wav 20 0
```

Use any of the AI text to speach to create a realistic voice for your message. 

The script has a threshold value you can set for receive busy this is used to reset the counter. When executed it will count to the specified seconds to wait/listen. If the receive threshold is met then it will reset the timer. When the timer hits the wait time the message will play. If the repeater is busy for the max_wait default to 300 seconds or 5 min then this run will terminate.  

Setup:
Install requirements (below) and depending on audio files ffmpeg
```
pip3 install -r requirements.txt
```
```
brew install ffmpeg
```

Usage: 
Announcements.py <sound_file> <seconds> <device_index>

Example useage and log output:
```
./Announcements.py Testing\ AD5QA.m4a 10 0
2024-07-24 11:58:43 Announcements.py Testing AD5QA.m4a 10 0 threshold=50
        -> [003s / 003s] - Avg RMS: [002/50] BELOW
        -> [004s / 004s] - Avg RMS: [003/50] BELOW
        -> [005s / 005s] - Avg RMS: [017/50] BELOW
        -> [006s / 006s] - Avg RMS: [049/50] BELOW
        -> [007s / 007s] - Avg RMS: [030/50] BELOW
        -> [008s / 008s] - Avg RMS: [076/50] ABOVE, resetting timer
        -> [001s / 009s] - Avg RMS: [002/50] BELOW
        -> [002s / 010s] - Avg RMS: [004/50] BELOW
        -> [003s / 011s] - Avg RMS: [003/50] BELOW
        -> [004s / 012s] - Avg RMS: [003/50] BELOW
        -> [005s / 013s] - Avg RMS: [008/50] BELOW
        -> [006s / 014s] - Avg RMS: [003/50] BELOW
        -> [007s / 015s] - Avg RMS: [006/50] BELOW
        -> [008s / 016s] - Avg RMS: [003/50] BELOW
        -> [009s / 017s] - Avg RMS: [003/50] BELOW
        -> [010s / 018s] - Avg RMS: [003/50] BELOW
        -> [011s / 019s] - Avg RMS: [003/50] BELOW
Elapsed Time: 11.1s | Total Time: 19.9s - Condition met. Playing sound...
```
