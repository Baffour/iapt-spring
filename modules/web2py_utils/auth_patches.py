#
#  Copyright (C) 2009 Thadeus Burgess
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#

def set_controller(auth, controller='default', function='user'):
    auth.settings.controller = controller

    auth.settings.login_url = auth.url(function, args='login')
    auth.settings.logged_url = auth.url(function, args='profile')
    auth.settings.download_url = auth.url('download')
    auth.settings.login_next = auth.url('index')
    auth.settings.logout_next = auth.url('index')
    auth.settings.register_next = auth.url('index')
    auth.settings.verify_email_next = auth.url(function, args='login')
    auth.settings.profile_next = auth.url('index')
    auth.settings.retrieve_username_next = auth.url('index')
    auth.settings.retrieve_password_next = auth.url('index')
    auth.settings.request_reset_password_next = auth.url(function, args='login')
    auth.settings.reset_password_next = auth.url(function, args='login')
    auth.settings.change_password_next = auth.url('index')
    auth.settings.on_failed_authorization = auth.url(function, args='not_authorized')
