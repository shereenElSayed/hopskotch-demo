#!/usr/bin/env python

import smtplib
import argparse
import json
from hop import stream
from hop.models import GCNCircular
from hop import cli
from hop import subscribe
import sys


def _add_parser_args(parser):
    
    """Parse arguments for broker, configurations and options
    """
    #All args from the subscriber
    subscribe._add_parser_args(parser)

    #Emails
    parser.add_argument(
        "-E",
        "--email",
        action="append",
        help="Emails of the receivers",
        required=True,
    )

def prepare_gcn(gcn_dict, json_dump=False):
    """Parse a gcn dictionary and print to stdout.
    Args:
      gcn_dict:  the dictionary object containing a GCN-formatted message
    Returns:
      None
    """
    if json_dump:
        return (json.dumps(gcn_dict))
    else:
        gcn = GCNCircular(**gcn_dict)
        message = ""
        for line in str(gcn).splitlines():
            message += line + "\n"
        return message

def send_email(message, receivers):
    """Send an email for each receiver with the message
    Args:
      message: the gcn message
      receivers: a list of email addresses to receive the message
    Returns:
      None
    """
    gmail_user = 'hopskotch.demo@gmail.com'
    gmail_password = 'bntcfycgqgzgzysk'

    sent_from = gmail_user
    to = receivers
    subject = 'Message from Hopskotch'

    email_text = 'Subject: {}\n\n{}'.format(subject, message)
    try:
    
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print ('Email sent! :)')
    except:
        print ("Email could not be sent :(", sys.exc_info()[0])
        raise

# ------------------------------------------------
# -- main

def _main(args=None):

    if not args:
        parser = argparse.ArgumentParser()
        _add_parser_args(parser)
        args = parser.parse_args()

    # load config if specified
    config = cli.load_config(args)

    # load consumer options
    start_offset = "earliest" if args.earliest else "latest"

    gcn_format = "json"
    receivers =  [email for email in args.email]

    with stream.open(args.url, "r", format=gcn_format, config=config, start_at=start_offset) as s:
        for gcn_dict in s(timeout=args.timeout):
            send_email(prepare_gcn(gcn_dict, args.json), receivers)
