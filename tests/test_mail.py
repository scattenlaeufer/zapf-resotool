import configparser
import os
import unittest
import imaplib
import email
import time


# load configuration data to access the test mailbox
config = configparser.ConfigParser()
config.read(os.path.join("test_config.ini"))


class MailTest(unittest.TestCase):
    def setUp(self):
        # connect to a given imap server
        self.mailbox = imaplib.IMAP4_SSL(host=config["Mail"]["server"])
        self.mailbox.login(
            user=config["Mail"]["username"], password=config["Mail"]["password"]
        )
        # open the INBOX as the used mailbox
        self.mailbox.select(mailbox="INBOX", readonly=False)

        # create the mail data for all the test mails
        test_start_time = time.time()
        self.mail_dict = {}
        for i in range(1, 1 + int(config["Mail"]["n_test_mails"])):
            self.mail_dict[f"[{test_start_time}] Test Mail {i:04}"] = {
                "from": config["Mail"]["mail"],
                "to": config["Mail"]["mail"],
                "text": "Test text",
            }

    def tearDown(self):
        # actually delete all mails marked for deletion
        self.mailbox.expunge()
        # close the connection to the mailbox
        self.mailbox.close()
        # logout from the imap server
        self.mailbox.logout()

    def test_mail_01_send(self):
        self.assertTrue(True)

    def test_mail_02_delivered(self):
        # create a list of all expected mails
        all_mails_list = list(self.mail_dict.keys())
        # get all mails from the mailbox
        response, data = self.mailbox.search(None, "ALL")
        # iterate over all mail data from the current mailbox
        for num in data[0].split():
            # convert binary data to a usable mail
            r, email_data = self.mailbox.fetch(num, "(RFC822)")
            email_string = email_data[0][1].decode("utf-8")
            email_message = email.message_from_string(email_string)
            # get subject from the current mail
            subject = str(
                email.header.make_header(
                    email.header.decode_header(email_message["Subject"])
                )
            )
            # check whether current mail is part of this test
            if subject in self.mail_dict.keys():
                # remove the current mail from the list of expected mails
                all_mails_list.remove(subject)

                # check for the correct sender
                email_from = str(
                    email.header.make_header(
                        email.header.decode_header(email_message["From"])
                    )
                )
                self.assertEqual(email_from, self.mail_dict[subject]["from"])

                # check for the correct recipient
                email_to = str(
                    email.header.make_header(
                        email.header.decode_header(email_message["To"])
                    )
                )
                self.assertEqual(email_to, self.mail_dict[subject]["to"])

                # mark the given mail for deletion
                self.mailbox.store(num, "+FLAGS", "\\Deleted")

        print(all_mails_list)
        self.assertEqual(0, len(all_mails_list))
