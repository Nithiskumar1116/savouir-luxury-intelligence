import requests
import json

# YOUR CONFIGURATION - REPLACE THESE!
BOT_TOKEN = "8593148481:AAEaz5UBehgaJFjNV1wFEskQJ-o242Xe85c"  # Your token
CHAT_ID = "5138828109"  # Your chat ID

def verify_setup():
    print("🔍 Verifying Telegram Setup...\n")
    
    # Step 1: Check bot token
    print("Step 1: Checking bot token...")
    response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getMe")
    
    if response.status_code == 200:
        bot_info = response.json()
        print(f"✅ Token valid! Bot name: @{bot_info['result']['username']}")
    else:
        print(f"❌ Invalid token: {response.text}")
        return
    
    # Step 2: Check for recent messages
    print("\nStep 2: Checking for recent messages...")
    response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates")
    
    if response.status_code == 200:
        updates = response.json()
        if updates['result']:
            print("✅ Found recent messages!")
            latest = updates['result'][-1]
            chat_id = latest['message']['chat']['id']
            print(f"📱 Your Chat ID: {chat_id}")
            
            if str(chat_id) == CHAT_ID:
                print("✅ Chat ID matches your configuration!")
            else:
                print(f"⚠️ Your configured Chat ID ({CHAT_ID}) doesn't match the one from Telegram ({chat_id})")
                print(f"Update your code to use: {chat_id}")
        else:
            print("❌ No messages found!")
            print("Send a message to your bot first, then run this script again")
            return
    
    # Step 3: Send test message
    print("\nStep 3: Sending test message...")
    test_message = "✅ Verification successful! Your Telegram is ready for Savouir alerts."
    
    payload = {
        'chat_id': CHAT_ID,
        'text': test_message,
        'parse_mode': 'HTML'
    }
    
    response = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json=payload)
    
    if response.status_code == 200:
        print("✅ Test message sent! Check your Telegram.")
    else:
        print(f"❌ Failed to send: {response.text}")

if __name__ == "__main__":
    verify_setup()