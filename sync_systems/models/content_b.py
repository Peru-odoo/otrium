# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import pandas as pd
import logging
from . import devices_b
from . import sftp_pandas

_logger = logging.getLogger(__name__)


class ContentB(models.Model):
    _name = 'content.b'
    _description = 'Content'

    content_id = fields.Char(string='Content Id')
    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    device_id = fields.Many2one('devices.b', string='Device', ondelete="restrict")
    expire_date = fields.Datetime(string='Expiry Date')
    state = fields.Selection([('enabled','Enabled'),('disabled','Disabled'),('deleted','Deleted')], string='State')

    @api.constrains('expire_date')
    def check_content_expiry_date(self):
        """ If expire date of Content is in the past, the state should be taken as disabled """

        if self.expire_date < datetime.now():
            self.state = 'disabled'

    def get_content_csv(self,data_location):
        content_local_path = self.env['ir.config_parameter'].sudo().get_param('content_local_path')
        content_delimiter = self.env['ir.config_parameter'].sudo().get_param('content_delimiter')
        hostname = self.env['ir.config_parameter'].sudo().get_param('sftp_hostname')
        sftp_username = self.env['ir.config_parameter'].sudo().get_param('sftp_username')
        sftp_password = self.env['ir.config_parameter'].sudo().get_param('sftp_password')
        content_sftp_path = self.env['ir.config_parameter'].sudo().get_param('content_sftp_path')
        content_sftp_delimiter = self.env['ir.config_parameter'].sudo().get_param('content_sftp_delimiter')

        if data_location == 'sftp':
            try:
                data_sftp = sftp_pandas.read_csv_sftp(hostname,sftp_username,sftp_password,content_sftp_path,
                                                      header=None, error_bad_lines=False, delimiter=content_sftp_delimiter)
                data = data_sftp
            except Exception as e:
                data = []
                _logger.error(e)
        elif data_location == 'local':
            try:
                data_local = pd.read_csv(content_local_path,
                                         header=None, error_bad_lines=False, delimiter=content_delimiter)
                """
                :param error_bad_lines: the offending lines to be skipped
                """
                data = data_local
            except Exception as e:
                data = []
                _logger.error(e)
        else:
            data = []

        for i in range(len(data)):
            """ Content Id is Unique """
            if not self.env['content.b'].search([('content_id', '=', data.iloc[i, 0])]):
                try:
                    self.create({'content_id': int(data.iloc[i, 0]),
                                 'name': data.iloc[i, 1],
                                 'description': data.iloc[i, 2],
                                 'device_id': self.env['devices.b'].search([('device_id','=',int(data.iloc[i, 3]))]).id,
                                 'expire_date': devices_b.refactor_date_time(data.iloc[i, 4]),
                                 'state': str(data.iloc[i, 5].lstrip(' '))})
                    _logger.info("row %s %s device is Imported" % (i + 1, data.iloc[i, 1]))
                except Exception as e:
                    _logger.error('in row %s ,%s' % (i + 1, e))
            else:
                _logger.error("in row %s  Content %s is already exist" % (i + 1, data.iloc[i, 0]))
