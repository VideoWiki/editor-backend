from library.mailchimp.send_mail import send_mail_hq, sendMail

def concat_mail(email, url):
    name = email.split('@')[0]
    print(name)
    global_merge_vars = [
        {
            'name': 'NAME',
            'content': name,
        },
        {
            'name': 'url',
            'content': url,
        }

    ]
    hq_mail_template = "23: Tell the user that his high-quality video is r"
    subject = "your high-quality video is ready!"
    mail = send_mail_hq(hq_mail_template, email, name, subject, global_merge_vars)
    status = mail
    return status

def hd_video_start_mail(email):
    name = email.split('@')[0]
    global_merge_vars = [
        {
            'name': 'NAME',
            'content': name
        }

    ]
    split_chunks_template = "25-your-video-is-being-generated"
    subject = "your high-quality video is being processed"
    status_res = sendMail(split_chunks_template, email, name, subject, global_merge_vars)
    status = status_res
    return status
