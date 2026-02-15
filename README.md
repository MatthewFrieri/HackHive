# HackHive | Doug the Poker Bot

## Inspiration
Imagine how cool it would be to have your own personal dealer at your next home poker match... Lucky for you, you no longer need to imagine. We introduce Doug, your very own poker dealer and broadcaster. Doug's inspiration came from the problems we faced at our own home poker matches. Having a robotic dealer has the potential to drastically increase the speed of a game, no longer wait on a person to be constantly paying attention for when to deal cards. Additionally, as a spectator at a poker match, it is often boring to wait through a hand while wondering what everyone's cards are until the reveal. With Doug, spectators now become engaged and integrated into the game.

## What it does
Doug sits in the middle of your poker table, ready to deal cards when needed. It's constantly listening for players' betting actions (Check, Call, Raise, Fold) and following the game as it progresses. Our speech interpretation model filters out normal conversation from the table, while still accurately listening for these betting actions. Doug has a camera to view cards just before they are dealt, which allows us to stream a live preview of the game for spectators, showing everyone's cards along with their current odds of winning. And if this wasn't enough, we also compute several relevant statistics (win %, PFR, VPIP) on each player, for spectators to better understand their playing style.

## How we built it
Doug himself is mostly 3D printed. Some of the hardware we used included:
- ESP32 microcontroller to be the brains
- DC motor for card dispensing
- Servo motor for rotation
- Webcam to view cards before they are dealt
- Battery to keep Doug chugging
- And several smaller components like motor drivers, buck converters, and LEDs

Doug's vision is powered by a YOLO 26 nano model that we trained on data we collected ourselves.
Doug's speech recognition uses a speech to text model, which is then passed through an interpretation model to better understand what was spoken.
In terms of software, our stack consists of React for the frontend and flask for the backend.

## Challenges we ran into
Doug's vision was our main challenge. Initially he had pretty poor eyesight... We first tried using out of the box models to identify the rank and suit of a card, however this didn't work consitently enough for us due to the conditions the card was held in, along with the focal length of our webcam. We decided to address this by gathering ~650 images of the cards inside Doug's chamber and training our own YOLO model to be more consistent with our webcam conditions.

## Accomplishments that we're proud of
We were very pleased with the level of accuracy we were able to achieve with Doug's new vision. We were also proud of our speech interpretation pipeline, as it understands enough about the context of a conversation to filter our potential false positives. For example if someone said "Hey steve can you CHECK the time" this would not be interpretted as a check action.
