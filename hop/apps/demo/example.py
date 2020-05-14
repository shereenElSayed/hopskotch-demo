#!/usr/bin/env python

import smtplib
import argparse
import json
from hop import stream


def _add_parser_args(parser):
    """Parse arguments for broker, configurations and options
    """

    parser.add_argument(
        "-b",
        "--broker-url",
        required=True,
        help="Sets the broker URL (kafka://host[:port]/topic) to publish GCNs to.",
    )

    # Configuration options
    config = parser.add_mutually_exclusive_group()
    config.add_argument(
        "-F", "--config-file", help="Set client configuration from file.",
    )

    # Subscription option
    parser.add_argument(
        "-e",
        "--earliest",
        help="Request to stream from the earliest available Kafka offset",
        action="store_true",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        help="Specifies the time (in seconds) to wait for new messages.",
    )

def send_email(message):
    gmail_user = 'hopskotch.demo@gmail.com'
    gmail_password = 'uksesoslhiskqihz'

    sent_from = gmail_user
    to = ['shereenhussein92@gmail.com']
    subject = 'OMG Super Important Message'
    body = message

    email_text = """\
    From: %s
    To: %s
    Subject: %s
    
    %s
    """ % (sent_from, ", ".join(to), subject, body)
    try:
    
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print ('Email sent! :)')
    except:
        print ('Email could not be sent :(')

def _main(args=None):
    """Send messages to your email
    """
    if not args:
        parser = argparse.ArgumentParser()
        _add_parser_args(parser)
        args = parser.parse_args()

    # load config if specified
    config = args.config_file if args.config_file else config=None

    # load consumer options
    start_offset = "earliest" if args.earliest else "latest"
    timeout = 20  if args.timeout else int(args.timeout)


    with stream.open(
        args.broker_url, "r", format=gcn_format, config=config, start_at=start_offset
    ) as s:
        for _, gcn_dict in s(timeout=timeout):
            send_email(json.dumps(gcn_dict))
            # post_message_to_slack(slack_config_dict, gcn_dict, json_dump)