from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class tag_project(models.Model):

    _inherit = "project.project"

    project_url = fields.Char(string='Project URL Link')
    domain_name = fields.Char(string='Final Domain Name')
    host_name = fields.Char(string='Host Name')
    cpanel_user_sign_in = fields.Char(string='C Panel User Sign In')
    cpanel_pwd = fields.Char(string='C Panel Password')
    crm_email = fields.Char(string='CRM Email Address')
    mass_mail = fields.Char(string='Mass Mail Address')
    mass_mail_sender = fields.Char(string='Mass Mail Sender')
    google_folder_url = fields.Char(string='Google Folder URL')
