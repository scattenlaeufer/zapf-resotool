import configparser
import os
import unittest
import imaplib
import email
import time

import reso_mail

# load configuration data to access the test mailbox
config = configparser.ConfigParser()
config.read(os.path.join("tests/test_config.ini"))


class MailTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # create the mail data for all the test mails
        test_start_time = time.time()
        self.mail_dict = {}
        for i in range(1, 1 + int(config["Mail"]["n_test_mails"])):
            self.mail_dict["[{}] Test Mail {:04}".format(test_start_time, i)] = {
                # self.mail_dict["[blubb]"] = {
                "from": config["Mail"]["mail"],
                "to": config["Mail"]["mail"],
                "text": "Test text",
            }

        # connect to a given imap server
        self.mailbox = imaplib.IMAP4_SSL(host=config["Mail"]["server"])
        self.mailbox.login(
            user=config["Mail"]["username"], password=config["Mail"]["password"]
        )

    @classmethod
    def tearDownClass(self):
        # actually delete all mails marked for deletion
        self.mailbox.expunge()
        # close the connection to the mailbox
        self.mailbox.close()
        # logout from the imap server
        self.mailbox.logout()

    def test_mail_01_send(self):
        result_dict = {}
        for subject, mail_data in self.mail_dict.items():
            result = reso_mail.send_mail.delay(
                config["Mail"]["server"],
                config["Mail"]["smtp_port"],
                config["Mail"]["username"],
                config["Mail"]["password"],
                mail_data["from"],
                mail_data["to"],
                subject,
                mail_data["text"],
            )
            result_dict[subject] = result
        for subject, result in result_dict.items():
            with self.subTest(subject=subject):
                self.assertTrue(result.get(timeout=5))

    def test_mail_02_receive(self):
        # wait 5 seconds to give mails time to arrive
        time.sleep(10)
        # open the INBOX as the used mailbox
        self.mailbox.select(mailbox="INBOX", readonly=False)

        # create a list of all expected mails
        all_mails_list = list(self.mail_dict.keys())
        # get all mails from the mailbox
        response, data = self.mailbox.search(None, "ALL")
        print(data)
        print(self.mail_dict.keys())
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
            print(f"{subject} -> {subject in self.mail_dict.keys()}")
            if subject in self.mail_dict.keys():
                # remove the current mail from the list of expected mails
                all_mails_list.remove(subject)

                with self.subTest(subject=subject):
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
