# setup_and_run_ribbon_sb_audio_fixed.py
import os
import subprocess
import sys
import requests
import json
import time
from datetime import datetime

def install_packages():
    """Install required Python packages"""
    print("📦 Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "seleniumbase", "requests"])

def verify_interview_page_loaded(sb):
    """Verify the interview page has loaded properly"""
    try:
        # Check for common interview page elements
        sb.assert_element('button', timeout=5)
        print("✅ Interview page loaded successfully")
        return True
    except:
        return False

def handle_cloudflare(sb):
    """Handle Cloudflare challenge if present"""
    try:
        # Check if we're on a Cloudflare challenge page
        if sb.is_element_visible('input[value*="Verify"]'):
            print("🔒 Cloudflare challenge detected, solving...")
            sb.uc_click('input[value*="Verify"]')
            time.sleep(2)
        elif "challenge" in sb.get_current_url().lower():
            print("🔒 Cloudflare captcha detected, attempting to solve...")
            sb.uc_gui_click_captcha()
            time.sleep(2)
    except:
        pass

def click_interview_button(sb):
    """Try multiple methods to click the interview start button"""
    clicked = False
    
    # Method 1: Direct click with class
    try:
        sb.click('button.css-ir55mp', timeout=10)
        clicked = True
        print("✅ Clicked button using class selector!")
    except:
        pass
    
    # Method 2: JavaScript click
    if not clicked:
        try:
            sb.execute_script("""
                const btn = document.querySelector('button.css-ir55mp');
                if (btn) { 
                    btn.click(); 
                    return true; 
                }
                return false;
            """)
            clicked = True
            print("✅ Clicked button using JavaScript!")
        except:
            pass
    
    # Method 3: Find button by partial class match
    if not clicked:
        try:
            buttons = sb.find_elements('button')
            for button in buttons:
                if 'css-ir55mp' in button.get_attribute('class'):
                    sb.execute_script("arguments[0].click();", button)
                    clicked = True
                    print("✅ Clicked button using element search!")
                    break
        except:
            pass
    
    return clicked

def setup_audio_permissions(sb):
    """Setup audio permissions and ensure microphone/speaker access"""
    print("🎤 Setting up audio permissions...")
    
    # Grant permissions using CDP
    try:
        sb.execute_cdp_cmd('Browser.grantPermissions', {
            'permissions': [
                'audioCapture',
                'videoCapture',
                'geolocation',
                'notifications'
            ],
            'origin': 'https://app.ribbon.ai'
        })
        print("✅ Browser permissions granted")
    except Exception as e:
        print(f"⚠️ Could not set CDP permissions: {e}")
    
    # Ensure audio context is allowed
    try:
        sb.execute_script("""
            // Create and resume audio context to ensure audio playback
            if (typeof AudioContext !== 'undefined') {
                window.audioContext = new AudioContext();
                window.audioContext.resume();
                console.log('Audio context created and resumed');
            }
        """)
        print("✅ Audio context enabled")
    except:
        pass

def create_interview_flow(api_key, base_url):
    """Create an interview flow"""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    interview_flow_data = {
        "org_name": "Automated Test Company",
        "title": "Customer Feedback Survey",
        "questions": [
            "What is your name and role?",
            "How would you rate your experience with our service?",
            "What features would you like to see improved?",
            "Would you recommend our service to others?"
        ],
        "voice_id": "11labs-Kate",
        "language": "en-US",
        "additional_info": "Please be friendly and professional. This is a test interview.",
        "interview_type": "general",
        "is_video_enabled": False,
        "is_phone_call_enabled": True,
        "is_doc_upload_enabled": False
    }
    
    response = requests.post(
        f"{base_url}/interview-flows",
        headers=headers,
        json=interview_flow_data
    )
    
    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to create interview flow: {response.text}")
    
    return response.json()['interview_flow_id']

def create_interview(api_key, base_url, interview_flow_id):
    """Create an interview instance"""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    interview_data = {
        "interview_flow_id": interview_flow_id,
        "interviewee_email_address": "test@example.com",
        "interviewee_first_name": "Test",
        "interviewee_last_name": "User"
    }
    
    response = requests.post(
        f"{base_url}/interviews",
        headers=headers,
        json=interview_data
    )
    
    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to create interview: {response.text}")
    
    return response.json()

def get_interview_data(api_key, base_url, interview_id):
    """Retrieve interview data"""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
    
    response = requests.get(
        f"{base_url}/interviews/{interview_id}",
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    return None

def main():
    """Main function using SeleniumBase with Cloudflare bypass and audio support"""
    install_packages()
    
    from seleniumbase import SB
    
    # Configuration
    API_KEY = "efbc484a-e854-4465-9426-b98e97bd35db"
    BASE_URL = "https://app.ribbon.ai/be-api/v1"
    
    print("\n🚀 Starting Ribbon AI Interview Automation with Audio Support\n")
    print("🎧 Make sure your headphones are connected!")
    print("🎤 Make sure your microphone is connected and working!")
    
    try:
        # Test API connection
        print("\n🔐 Testing API connection...")
        headers = {'Authorization': f'Bearer {API_KEY}'}
        test_resp = requests.get(f"{BASE_URL}/ping", headers=headers)
        if test_resp.status_code != 200:
            print(f"❌ API key invalid: {test_resp.status_code}")
            return
        print("✅ API key validated!")
        
        # Create interview flow
        print("\n📋 Creating interview flow...")
        interview_flow_id = create_interview_flow(API_KEY, BASE_URL)
        print(f"✅ Interview flow created: {interview_flow_id}")
        
        # Create interview
        print("\n🎤 Creating interview...")
        interview_result = create_interview(API_KEY, BASE_URL, interview_flow_id)
        interview_id = interview_result['interview_id']
        interview_link = interview_result['interview_link']
        print(f"✅ Interview created: {interview_id}")
        print(f"🔗 Link: {interview_link}")
        
        # Open browser and conduct interview
        print("\n🌐 Opening Chrome with audio support...")
        
        # Create SB instance with Chrome and audio permissions
        with SB(
            uc=True, 
            headless=False,  # Cannot be headless for audio
            chromium_arg=(
                "--use-fake-ui-for-media-stream,"  # Auto-accept media permissions
                "--auto-select-desktop-capture-source=Entire screen,"
                "--enable-usermedia-screen-capturing,"
                "--allow-running-insecure-content,"
                "--autoplay-policy=no-user-gesture-required,"  # Allow autoplay
                "--no-sandbox,"
                "--disable-setuid-sandbox,"
                "--disable-web-security,"
                "--disable-features=IsolateOrigins,site-per-process"
            ),
            firefox_pref={
                "profile.default_content_setting_values.media_stream_mic": 1,
                "profile.default_content_setting_values.media_stream_camera": 1,
                "profile.default_content_setting_values.notifications": 1,
                "profile.default_content_settings.popups": 0,
                "safebrowsing.enabled": True,
                # Audio settings
                "profile.default_content_setting_values.sound": 1,  # Enable sound
                "profile.content_settings.exceptions.sound.*,*.setting": 1,  # Allow all sites
            }
        ) as sb:
            # Navigate to interview with reconnect for Cloudflare
            print("📍 Navigating to interview page...")
            sb.uc_open_with_reconnect(interview_link, 3)
            
            # Handle Cloudflare if needed
            handle_cloudflare(sb)
            
            # Setup audio permissions after page load
            setup_audio_permissions(sb)
            
            # Verify page loaded
            if not verify_interview_page_loaded(sb):
                print("⚠️ Page may not have loaded correctly, attempting to continue...")
            
            # Wait a bit for full page load
            sb.sleep(3)
            
            # Additional audio setup after page is loaded
            try:
                sb.execute_script("""
                    // Ensure all audio elements are unmuted
                    document.querySelectorAll('audio').forEach(audio => {
                        audio.muted = false;
                        audio.volume = 1.0;
                        console.log('Audio element unmuted');
                    });
                    
                    // Ensure video elements with audio are unmuted
                    document.querySelectorAll('video').forEach(video => {
                        video.muted = false;
                        video.volume = 1.0;
                        console.log('Video element unmuted');
                    });
                    
                    // Log audio devices
                    navigator.mediaDevices.enumerateDevices()
                        .then(devices => {
                            const audioInputs = devices.filter(d => d.kind === 'audioinput');
                            const audioOutputs = devices.filter(d => d.kind === 'audiooutput');
                            console.log('Microphones found:', audioInputs.length);
                            console.log('Audio outputs found:', audioOutputs.length);
                        });
                """)
                print("✅ Audio elements configured")
            except:
                pass
            
            # Save initial screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            sb.save_screenshot(f"interview_page_{timestamp}.png")
            print("📸 Initial screenshot saved")
            
            # Try to click the interview start button
            print("\n🎯 Looking for interview start button...")
            
            if click_interview_button(sb):
                print("\n🎉 Interview started successfully!")
                print("🎧 Audio should be playing through your headphones")
                print("🎙️ Your microphone is active - speak clearly when prompted")
                print("💡 Make sure your system audio is not muted")
                
                # Monitor audio status
                try:
                    audio_status = sb.execute_script("""
                        const audioElements = document.querySelectorAll('audio');
                        const videoElements = document.querySelectorAll('video');
                        let activeAudio = 0;
                        audioElements.forEach(a => { if (!a.paused) activeAudio++; });
                        return {
                            audioCount: audioElements.length,
                            videoCount: videoElements.length,
                            activeAudio: activeAudio,
                            hasMediaStream: typeof navigator.mediaDevices !== 'undefined'
                        };
                    """)
                    print(f"\n📊 Media status: {audio_status}")
                except:
                    pass
                
                # Let the interview run
                print("\n⏳ Interview in progress...")
                print("🗣️ Listen for questions and respond naturally\n")
                
                # Extended runtime for real interview
                interview_duration = 90  # 90 seconds for a full interview
                for i in range(interview_duration):
                    print(f"   Running... {i+1}/{interview_duration} seconds", end='\r')
                    sb.sleep(1)
                    
                    # Check for any audio issues every 15 seconds
                    if i % 15 == 0 and i > 0:
                        try:
                            sb.execute_script("""
                                // Re-enable audio if needed
                                document.querySelectorAll('audio, video').forEach(elem => {
                                    if (elem.muted) {
                                        elem.muted = false;
                                        elem.volume = 1.0;
                                        console.log('Re-enabled muted element');
                                    }
                                });
                            """)
                        except:
                            pass
                
                print(f"\n✅ Interview session completed")
                
                # Save final screenshot
                sb.save_screenshot(f"interview_completed_{timestamp}.png")
                print("📸 Final screenshot saved")
            else:
                print("❌ Could not find/click the start button")
                
                # Debug information
                print("\n🔍 Debug: Searching for buttons...")
                buttons = sb.find_elements('button')
                print(f"Found {len(buttons)} buttons on page")
                
                for i, button in enumerate(buttons[:5]):
                    try:
                        btn_class = button.get_attribute('class')
                        btn_text = button.text.strip()
                        print(f"  Button {i+1}: class='{btn_class}', text='{btn_text}'")
                    except:
                        pass
                
                # Save debug screenshot
                sb.save_screenshot(f"debug_{timestamp}.png")
                print("📸 Debug screenshot saved")
        
        # Wait for processing
        print("\n⏳ Waiting for interview processing...")
        time.sleep(15)
        
        # Retrieve interview data
        print("\n📊 Retrieving interview data...")
        interview_data = get_interview_data(API_KEY, BASE_URL, interview_id)
        
        if interview_data:
            print("✅ Interview data retrieved!")
            
            # Save interview data
            output_file = f"interview_{interview_id}_{timestamp}.json"
            with open(output_file, 'w') as f:
                json.dump(interview_data, f, indent=2)
            print(f"💾 Interview data saved to: {output_file}")
            
            # Display key information
            print(f"\n📄 Interview Summary:")
            print(f"   Status: {interview_data.get('status', 'unknown')}")
            print(f"   Interview ID: {interview_id}")
            print(f"   Flow ID: {interview_flow_id}")
            
            if interview_data.get('transcript'):
                print(f"\n📝 Transcript preview:")
                print(f"   {interview_data['transcript'][:500]}...")
                
                # Save full transcript
                transcript_file = f"transcript_{interview_id}_{timestamp}.txt"
                with open(transcript_file, 'w', encoding='utf-8') as f:
                    f.write(interview_data['transcript'])
                print(f"📝 Full transcript saved to: {transcript_file}")
        else:
            print("❌ Could not retrieve interview data")
        
        # Get all recent interviews
        print("\n📋 Checking recent interviews...")
        headers = {'Authorization': f'Bearer {API_KEY}'}
        params = {"limit": 5, "offset": 0}
        
        resp = requests.get(f"{BASE_URL}/interviews", headers=headers, params=params)
        if resp.status_code == 200:
            interviews = resp.json().get('interviews', [])
            print(f"Found {len(interviews)} recent interview(s)")
            
            for interview in interviews:
                data = interview.get('interview_data', {})
                if data.get('interview_id') == interview_id:
                    print(f"✅ Our interview found with status: {data.get('status')}")
                    if data.get('transcript'):
                        print("✅ Transcript is available!")
                    break
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n✨ Automation complete!")
    print("📝 Check the JSON and TXT files for the full interview data and transcript")

if __name__ == "__main__":
    main()