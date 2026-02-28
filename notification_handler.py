import asyncio
from uuid import uuid4
from aioapns import APNs, NotificationRequest, PushType


async def run():
    apns_cert_client = APNs(
        client_cert='apple certificates//apns-pro-cert.pem',
        use_sandbox=False,
    )
    apns_key_client = APNs(
        key='apple certificates//apns-pro-key.pem',
        key_id='<KEY_ID>',
        team_id='<TEAM_ID>',
        topic='<APNS_TOPIC>',  # Bundle ID
        use_sandbox=False,
    )
    request = NotificationRequest(
        device_token='<DEVICE_TOKEN>',
        message = {
            "aps": {
                "alert": "Hello from APNs",
                "badge": "1",
            }
        },
        notification_id=str(uuid4()),  # optional
        time_to_live=3,                # optional
        push_type=PushType.ALERT,      # optional
    )
    await apns_cert_client.send_notification(request)
    await apns_key_client.send_notification(request)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())