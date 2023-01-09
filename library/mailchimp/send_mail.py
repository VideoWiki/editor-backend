import mandrill
from coutoEditor.global_variable import MANDRILL_API_KEY


def sendMail(template_name, to_email, name,subject, global_merge_vars):
    try:
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
        message = {
            'from_email': 'puneet@boarded.in',
            'from_name': 'VideoWiki',
            'global_merge_vars': global_merge_vars,
            # need reply mail
            'headers': {'Reply-To': 'support@videowiki.pt'},
            'merge': True,
            'merge_language': 'mailchimp',
            'subject': subject,
            'tags': ['password-resets'],
            'text': 'Example text content',
            'to': [{'email': to_email,
                    'name': name,
                    'type': 'to'}],
        }

        result = mandrill_client.messages.send_template(
            template_name=template_name, template_content=[], message=message, send_async=False, ip_pool='Main Pool')
        print(result)
        status = result[0]['status']
        return status

    except mandrill.Error as e:
        status = 'A mandrill error occurred:'
        print('A mandrill error occurred:')
        return status

def sendMess( to_email, name,subject, global_merge_vars, res_dict):
    try:
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
        message = {
            'from_email': 'puneet@boarded.in',
            'from_name': 'VideoWiki',
            'global_merge_vars': global_merge_vars,
            # need reply mail
            'headers': {'Reply-To': 'support@videowiki.pt'},
            'merge': True,
            'merge_language': 'mailchimp',
            'subject': subject,
            'tags': ['password-resets'],
            'text': 'Example text content',
            'to': [{'email': to_email,
                    'name': name,
                    'type': 'to'}],
        }
        result = mandrill_client.messages.send(message = message)
        print(result)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e.text))

def send_mail_hq(hq_mail_template, to_email, name ,subject, global_merge_vars):
    try:
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
        message = {
            'from_email': 'puneet@boarded.in',
            'from_name': 'VideoWiki',
            'global_merge_vars': global_merge_vars,
            # need reply mail
            'headers': {'Reply-To': 'support@videowiki.pt'},
            'merge': True,
            'merge_language': 'mailchimp',
            'subject': subject,
            'tags': ['password-resets'],
            'text': 'Example text content',
            'to': [{'email': to_email,
                    'name': name,
                    'type': 'to'}],
        }

        result = mandrill_client.messages.send_template(
            template_name=hq_mail_template, template_content=[], message=message, send_async=False, ip_pool='Main Pool')
        print(result)
        status = result[0]['status']
        return status

    except mandrill.Error as e:
        status = 'A mandrill error occurred!'
        print('A mandrill error occurred!')
        return status