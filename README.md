# Auto Channel Copy Bot

A Telegram bot that automatically copies posts from source channels to multiple destination channels.

## Features
- Multiple source channels
- Multiple destination channels
- No sender tag
- Inline buttons remain unchanged
- Admin-controlled via bot commands
- Deployable on Render / VPS

## Commands (Admin Only)
/addsource -100xxxxxxxx  
/removesource -100xxxxxxxx  
/adddest -100xxxxxxxx  
/removedest -100xxxxxxxx  
/listsource  
/listdest  

## Setup (Render)
1. Create a Telegram bot and get BOT_TOKEN
2. Deploy this repo on Render
3. Set environment variables:
   - BOT_TOKEN
   - ADMIN_ID
4. Add bot as admin in source & destination channels
5. Start managing channels via commands
6. 
