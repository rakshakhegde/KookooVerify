# KookooVerify
Complete suite of API to verify and handle phone number verification

## Verify API
You use Verify API to confirm that a phone number is valid, reachable, and accessible by your user. Using a Verify Request you send
a PIN to a phone number. Your user enters this PIN into your App or Website, then you run a Verify Check to authenticate it.
Verifying phone numbers is a mission-critical process and is typically used for:
- SPAM Protection - prevent spammers from mass-creating messages.
- Hack protection - if you detect suspicious or significant activities, validate that the person using a phone number owns it. Reach Users - ensure you have the correct phone number to contact your user when you need to.

By default, the PIN is first sent in an SMS, if there is no reply Verify sends a Voice Call. The Verify API workflow To Verify that a phone number is valid, reachable, and accessible by your user you use the:
1. Verify Request: generate and send a PIN to your user. You use the request_id in theResponse for the Verify Check.
> https://hacks-rakheg.rhcloud.com/kookooverify?phone_no=xxxxxxxxxx&brand=MyApp
2. Verify Check: confirm that the PIN you received from your user matches the one sent by Nexmo after yourVerify Request.
> https://hacks-rakheg.rhcloud.com/kookooverify/check?request_id=xxxxxxxxxxxx&code=xxxx
3. Verify Search: lookup the status of one or more requests.
> https://hacks-rakheg.rhcloud.com/kookooverify/search?request_id=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
4. Verify Control: control the progress of your Verify Requests.
> https://hacks-rakheg.rhcloud.com/kookooverify/control?request_id=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&cmd=cancel
