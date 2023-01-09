from library.mailchimp.send_mail import sendMail

def clip_chunk_mail(email):
    name = email.split('@')[0]
    global_merge_vars = [
        {
            'name': 'NAME',
            'content': name
        }

    ]
    split_chunks_template = "26 your call recording is being processed"
    subject = "your call recording is being processed"
    status_res = sendMail(split_chunks_template, email, name, subject, global_merge_vars)
    status = status_res
    return status