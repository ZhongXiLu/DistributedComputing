
import schedule
import time
import requests

from util.send_request import *

# Services to be polled with their ping path
# IMPORTANT: assume user, authentication and notification service are ALWAYS up
SERVICES = [
    ("ad", "ads/ping"),
    ("anti-cyberbullying", "anti_cyberbullying/ping"),
    ("comment", "comments/ping"),
    ("follow", "follow/ping"),
    ("friend", "friend/ping"),
    ("like", "likes/ping"),
    ("message", "message/ping"),
    ("post", "posts/ping"),
    ("tag", "tags/ping")
]

# Keep dict of statuses of services
# => prevent sending the same notifications again every 30 seconds
# False = service down
service_status = {}


def send_notification_to_all(message):
    """Send notification to all users that a service is temporary down"""

    response_obj = send_request('get', 'users', 'users', timeout=3)
    all_users = [user['id'] for user in response_obj.json['data']['users']]

    send_request('post', 'notification', 'notifications', timeout=3,
                 json={'content': message,
                       'recipients': all_users}, auth=('2', 'admin'))


def poll_services():
    """Poll each service by pinging them"""

    for service, path in SERVICES:
        try:
            response_object = send_request('get', service, f'{path}', timeout=3)
            if response_object.json['status'] == "fail":
                if not service_status[service]:
                    service_status[service] = True  # status = down
                    send_notification_to_all(
                        f'{service} service is temporary down. Please wait while we\'ll try to fix this.')
            else:
                if service_status[service]:
                    service_status[service] = False     # status = up
                    send_notification_to_all(
                        f'{service} service is back up. Thank you for your patience.')
        except:
            if not service_status[service]:
                service_status[service] = True  # status = down
                send_notification_to_all(
                    f'{service} service is temporary down. Please wait while we\'ll try to fix this.')


def main():
    """
        Poll every service every 30 seconds
        IMPORTANT: assume user, authentication and notification service are ALWAYS up
    """

    for service, path in SERVICES:
        service_status[service] = False

    time.sleep(60)  # wait initial seconds
    schedule.every(10).seconds.do(poll_services)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
