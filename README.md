# KookooVerify
The complete suite of API for all workflows of Phone Number Verification to prevent spamming and to ensure personal account uniqueness. Obviously this API is a demo and is still in Beta, hence make sure your phone number is *not* in DND and use the API only *between 9am-9pm*.

## Verify API
You use Verify API to confirm that a phone number is valid, reachable, and accessible by your user. Using a Verify Request you send
a PIN to a phone number. Your user enters this PIN into your App or Website, then you run a Verify Check to authenticate it.
Verifying phone numbers is a mission-critical process and is typically used for:
- SPAM Protection - prevent spammers from mass-creating messages.
- Hack protection - if you detect suspicious or significant activities, validate that the person using a phone number owns it.
- Reach Users - ensure you have the correct phone number to contact your user when you need to.

By default, the PIN is first sent in an SMS, if there is no reply Verify sends a Voice Call.

## Verify API workflow
To Verify that a phone number is valid, reachable, and accessible by your user you use the:

1. Verify Request: generate and send a PIN to your user. You use the request_id in theResponse for the Verify Check.
> https://hacks-rakheg.rhcloud.com/kookooverify?phone_no=xxxxxxxxxx&brand=MyApp

2. Verify Check: confirm that the PIN you received from your user matches the one sent by Nexmo after yourVerify Request.
> https://hacks-rakheg.rhcloud.com/kookooverify/check?request_id=xxxxxxxxxxxx&code=xxxx

3. Verify Search: lookup the status of one or more requests.
> https://hacks-rakheg.rhcloud.com/kookooverify/search?request_id=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

4. Verify Control: control the progress of your Verify Requests.
> https://hacks-rakheg.rhcloud.com/kookooverify/control?request_id=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&cmd=cancel

## Features
- Resending verification code to an ongoing verification i.e., Concurrent verifications are banned.
- Only 5 min window to verify code is allowed.
- Number of invalid tries are logged and only maximum of 3 tries are allowed to avoid hacks and brute force checks.
- API to query the status of an ongoing verification by using request_id in Search API
- API to cancel an ongoing verification using the Control API.
- 30 days validity allowed for a number to be marked as Verified which is queried using Search API.
- JavaScript SDK to easily integrate Verification API into Frontend Web Apps.

## How to run
- Fork this project and run command "python flaskapp.py" at the root directory of this project.
- The trigger times can be changed under ".openshift/cron" directory. The cron job python script running is cron_job.py under "hacks/kookooverify" directory. This cron job is used to find out the unverified numbers even after two mins of sending the verification code to them and send a Voice Call to them with the verification code as a confirmatory call.
