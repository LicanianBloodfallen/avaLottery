# Ava Lottery - Discord Raid Bot

## Features
- `/check [voice_channel]` - Record attendance from a voice channel.
- `/summary` - Show monthly summary of points and raid leader count.
- `/leaderboard` - Display current leaderboard.

## Setup

1. Copy `.env.example` to `.env` and fill in your credentials:
   ```env
   DISCORD_TOKEN=your_discord_token
   GOOGLE_SHEETS_CREDENTIALS=path/to/credentials.json
   SPREADSHEET_ID=your_spreadsheet_id
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create two sheets in your Google Sheets doc named `Obecności` and `Podsumowanie` with headers:
   - Obecności: `Data | Użytkownik | Raid Leader`
   - Podsumowanie: `Użytkownik | Punkty | Rajdy jako RL`

4. Run the bot:
   ```bash
   python bot.py
   ```
