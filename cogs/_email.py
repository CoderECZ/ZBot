import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class EmailSender:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def _read_html_file(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def send_email(self, to_email: str, html_file_path: str, subject: str = "CoderZ Legal Agreements", replacements=None, attachments=None):
        # Read the HTML content from the file
        html_content = self._read_html_file(html_file_path)

        # Replace placeholders in the HTML content
        if replacements:
            for placeholder, value in replacements.items():
                html_content = html_content.replace(placeholder, str(value))

        # Create the MIME object
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the HTML body
        msg.attach(MIMEText(html_content, 'html'))
        
        if attachments:
            for attachment_path in attachments:
                with open(attachment_path, 'rb') as file:
                    pdf_attachment = MIMEApplication(file.read(), _subtype="pdf")
                    pdf_attachment.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
                    msg.attach(pdf_attachment)

        # Connect to the SMTP server
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            # Login to the email account
            server.starttls()
            server.login(self.sender_email, self.sender_password)

            # Send the email
            server.sendmail(self.sender_email, to_email, msg.as_string())


    class SendEmail:
        def __init__(self, replacements, email_sender, to_email: str, clientName: str, productName: str, transactionID: str, html_file_path: str = "", subject: str = "CoderZ Legal Documentation", smtp_server: str = "", smtp_port: int = 587, sender_email: str = "", sender_password: str = ""):
            # Replace the placeholders with your SMTP server details and email credentials
            self.smtp_server = 'your_smtp_server.com'
            self.smtp_port = 587
            self.sender_email = 'your_email@example.com'
            # Store in config.json
            self.sender_password = 'your_email_password'

            # Create an instance of EmailSender
            email_sender = EmailSender(smtp_server, smtp_port, sender_email, sender_password)

            # Replace these values with the recipient's email, subject, HTML file path, and replacement values
            self.to_email = 'recipient@example.com'
            self.subject = 'CoderZ Legal Agreements'
            self.html_file_path = 'path/to/your/email_template.html'
            
            # Define replacement values (e.g., client name, product details)
            self.replacements = {
                '[Client Name]': clientName,
                '[Product Name]': productName,
                '[Transaction ID]': transactionID,
            }

            self.attachments = ['cogs/templates/documents/legal/TermsAndConditions.pdf', 'cogs/templates/documents/legal/PrivacyPolicy.pdf', 'cogs/templates/documents/legal/CustomerAgreement.pdf', 'cogs/templates/documents/legal/AcceptableUsagePolicy.pdf']
            
            # Send the email
            email_sender.send_email(to_email, subject, html_file_path, replacements)