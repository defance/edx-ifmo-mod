class CertSys(object):

    def __init__(self,
                 storage_prefix='/tmp',
                 url_prefix='/static/files/certificates',
                 secret='5Zp6KcWkYJhQ9nXzcAarXvgj',
                 strategy='ignore',
                 generate=False,
                 file_name='certificate.pdf'):
        self.storage_prefix = storage_prefix
        self.url_prefix = url_prefix
        self.secret = secret
        self.strategy = strategy
        self.need_generate = generate
        self.file_name = file_name