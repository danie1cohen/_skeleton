import smtplib
from email.utils import formatdate
from logging.handlers import SMTPHandler


class BufferingSMTPHandler(SMTPHandler):
    """
    A custom handler class that combines the functionality of SMTPHandler
    But without sending an email for every single log record
    """
    def __init__(self, mailhost, fromaddr, toaddrs, subject, capacity,
                 credentials=None, secure=None):
        """
        Initializes the handler and then adds a buffer as well
        """
        SMTPHandler.__init__(self, mailhost, fromaddr, toaddrs, subject,
                             credentials=None, secure=None)
        self.capacity = capacity
        self.buffer = []

    def shouldFlush(self, record):
        """
        If the buffer is bigger than the capacity, then yes, yes we should.
        """
        return (len(self.buffer) >= self.capacity)

    def emit(self, record):
        """
        Emits a record only to the buffer, and if necessary, calls flush()
        """
        self.buffer.append(record)
        if self.shouldFlush(record):
            self.flush()

    def flush(self):
        """
        Flushes everything out of the buffer. This is a list-handling version of
        SMTPHandler's emit
        """
        self.acquire()
        try:
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port, timeout=self._timeout)
            msg = '\r\n'.join([self.format(record) for record in self.buffer])
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                            self.fromaddr,
                            ",".join(self.toaddrs),
                            self.getSubject(record),
                            formatdate(), msg)
            if self.username:
                if self.secure is not None:
                    smtp.ehlo()
                    smtp.starttls(*self.secure)
                    smtp.ehlo()
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            for record in self.buffer:
                self.handleError(record)
        # would use finally here but it is too new for some systems
        self.buffer = []
        self.release()

    def close(self):
        """
        Close the handler.
        """
        self.flush()
        SMTPHandler.close(self)