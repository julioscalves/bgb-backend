def assemble_message(key: str, message='', replace=False):
    messages = {
        'not_json': {
            'success': False,
            'message': 'Requisição inválida.'
        },
        'not_found': {
            'success': False,
            'message': 'Anúncio não encontrado.'
        },
        'not_200': {
            'success': False,
            'message': 'Erro HTTP status !OK.'
        },
        'banned': {
            'success':
            False,
            'message':
            'Este usuário foi banido do Bazar BGB e, por isso, não poderá enviar mensagens.'
        },
        'blocked': {
            'success': False,
            'message': 'Usuário impedido por tempo de envio.'
        },
        'invalid_command': {
            'success': False,
            'message': 'Comando inválido.'
        },
        'invalid_id': {
            'success': False,
            'message': 'ID inválido. Por favor, realize o login novamente.'
        },
        'invalid_username': {
            'success':
            False,
            'message':
            'Por favor, crie um nome de usuário junto ao Telegram antes de utilizar este site.'
        },
        'hash_failure': {
            'success':
            False,
            'message':
            'Falha na geração do token de autenticação. Por favor, faça o login novamente.'
        },
        'expired_token': {
            'success': False,
            'message': 'Token expirado. Por favor, faça o login novamente.'
        },
        'success': {
            'success': True,
            'message': ''
        },
    }

    response = {
        'success': messages[key]['success'],
        'message': message if replace else messages[key]['message'] + message,
    }

    return response
