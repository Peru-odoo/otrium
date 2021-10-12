
from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    devices_local_path = fields.Char('Local Path', config_parameter='sync_systems.devices_local_path')
    devices_delimiter = fields.Char('Delimiter', default=',',
                                    help='Default delimiter ","', config_parameter='sync_systems.devices_delimiter')

    content_local_path = fields.Char('Local Path', config_parameter='sync_systems.content_local_path')
    content_delimiter = fields.Char('Delimiter', default=',',
                            help='Default Delimiter ","', config_parameter='sync_systems.content_delimiter')

    sftp_hostname = fields.Char('Hostname', config_parameter='sync_systems.sftp_hostname')
    sftp_username = fields.Char('Username', config_parameter='sync_systems.sftp_username')
    sftp_password = fields.Char('Password', config_parameter='sync_systems.sftp_password')

    devices_sftp_path = fields.Char('sftp Path', config_parameter='sync_systems.devices_sftp_path')
    devices_sftp_delimiter = fields.Char('Delimiter', default=',',
                            help='Default delimiter ","', config_parameter='sync_systems.devices_sftp_delimiter')

    content_sftp_path = fields.Char('sftp Path', config_parameter='sync_systems.content_sftp_path')
    content_sftp_delimiter = fields.Char('Delimiter', default=',',
                            help='Default Delimiter ","', config_parameter='sync_systems.content_sftp_delimiter')
