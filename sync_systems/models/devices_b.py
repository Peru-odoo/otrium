# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
import pandas as pd
import logging
from . import sftp_pandas
_logger = logging.getLogger(__name__)


def refactor_date_time(df_datatime):
    """ to convert decimal seconds to datetime format and remove timezone """

    if float(df_datatime[18:24]) > 60:
        converted_seconds = timedelta(seconds=float(df_datatime[18:24]))
        final_datetime = datetime.strptime(df_datatime[:17].lstrip(' '),"%Y-%m-%d %H:%M") + converted_seconds
        return final_datetime


class DevicesB(models.Model):
    _name = 'devices.b'
    _description = 'Devices'

    device_id = fields.Integer('Device ID')
    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    code = fields.Char(string='Code')
    expire_date = fields.Datetime(string='Expiry Date')
    state = fields.Selection([('enabled','Enabled'),('disabled','Disabled'),('deleted','Deleted')], string='State')

    _sql_constraints = [
                    ('field_unique',
                     'unique(code)',
                     'This Code Devices is already Available')
    ]

    @api.constrains('expire_date')
    def check_device_expiry_date(self):
        """ If expire date of device is in the past, the state should be taken as disabled """

        if self.expire_date < datetime.now():
            self.state = 'disabled'

    def get_devices_csv(self,data_location):

        devices_local_path = self.env['ir.config_parameter'].sudo().get_param('devices_local_path')
        devices_delimiter = self.env['ir.config_parameter'].sudo().get_param('devices_delimiter')
        hostname = self.env['ir.config_parameter'].sudo().get_param('sftp_hostname')
        sftp_username = self.env['ir.config_parameter'].sudo().get_param('sftp_username')
        sftp_password = self.env['ir.config_parameter'].sudo().get_param('sftp_password')
        devices_sftp_path = self.env['ir.config_parameter'].sudo().get_param('devices_sftp_path')
        devices_sftp_delimiter = self.env['ir.config_parameter'].sudo().get_param('devices_sftp_delimiter')

        if data_location == 'sftp':
            try:
                data_sftp = sftp_pandas.read_csv_sftp(hostname,sftp_username,sftp_password,devices_sftp_path,
                                                      header=None, error_bad_lines=False, delimiter=devices_sftp_delimiter)
                data = data_sftp
            except Exception as e:
                data = []
                _logger.error(e)
        elif data_location == 'local':
            try:
                data_local = pd.read_csv(devices_local_path,
                                   header=None, error_bad_lines=False, delimiter=devices_delimiter)
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
            if not self.env['devices.b'].search([('code', '=', data.iloc[i, 3])]):
                try:
                    self.create({'device_id': int(data.iloc[i, 0]),
                                 'name': data.iloc[i, 1],
                                 'description': data.iloc[i, 2],
                                 'code': data.iloc[i, 3],
                                 'expire_date': refactor_date_time(data.iloc[i, 4]),
                                 'state': str(data.iloc[i, 5].lstrip(' '))})
                    _logger.info("row %s %s device is Imported"%(i+1,data.iloc[i, 1]))
                except Exception as e:
                    _logger.error('in row %s ,%s'% (i+1, e))
            else:
                _logger.error("in row %s  Device Code %s is already exist"%(i+1,data.iloc[i, 3]))

