from functions import is_connected, log, check_relevant_roles, send_mail

# If connected to internet
if(is_connected()):
    try:
        log('Internet connection available')

        # Check for relevant roles
        relevant_roles = check_relevant_roles()

        # If relevant roles found
        if(relevant_roles):
            log(f'{len(relevant_roles)} relevant roles(s) found')

            # Send mail
            log('Sending mail...')
            send_mail(relevant_roles, 'success')

        # If no relevant roles found
        else:
            log('No relevant roles found')

    except Exception as e:
        log(f'Error: {str(e)}.')

        try:
            # Send error mail
            send_mail([], str(e))

        # If error mail cant be sent
        except Exception as e:
            log(f'Mail could not be sent. Error: {str(e)}.')

# If not connected to the internet
else:
    log('No internet connection')
