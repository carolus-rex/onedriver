import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer

import os.path

from utils import *


redirect_uri = 'http://localhost:8080/'
api_base_url = 'https://api.onedrive.com/v1.0/'
scopes = ['wl.signin', 'wl.offline_access', 'onedrive.readwrite']


class RemoteFileNotFoundError(Exception):
	pass

class InvalidRemoteDirectoryError(Exception):
	pass

class MissingArgumentsError(Exception):
	pass


class OneDrive(object):
	USER_PATH = os.path.expanduser("~")
	CONFIG_FILE = USER_PATH + '/' + 'onedriver.config'
	SESSION_FILE = USER_PATH + '/' + 'onedriver.session'

	def __init__(self):
		print("STARTING CONNECTION")
		self.client_id = ''
		self.client_secret = ''

		self.client = self.mauthenticator()
		print("CONNECTION STARTED")

		self.working_dir_id = "root"
		self.working_dir_path = "/"

	def get_auth_data_from_prompt(self):
		client_id = input('client id: ')
		client_secret = input('client secret: ')

		with open(self.CONFIG_FILE, 'w') as file:
			file.write('\n'.join([client_id, client_secret]) + '\n')

	def get_local_auth_data(self):
		try:
			config_file = open(self.CONFIG_FILE)
		except FileNotFoundError:
			self.get_auth_data_from_prompt()

			config_file = open(self.CONFIG_FILE)

		config = config_file.readlines()

		self.client_id = config[0]
		self.client_secret = config[1]

	def authenticator(self):
		self.get_local_auth_data()

		client = onedrivesdk.get_default_client(client_id=self.client_id,
												scopes=scopes)

		auth_url = client.auth_provider.get_auth_url(redirect_uri)

		#this will block until we have the code
		code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)

		client.auth_provider.authenticate(code, redirect_uri, self.client_secret)

		return client

	def mauthenticator(self):
		self.get_local_auth_data()

		http_provider = onedrivesdk.HttpProvider()
		auth_provider = onedrivesdk.AuthProvider(
		    http_provider=http_provider,
		    client_id=self.client_id,
		    scopes=scopes)

		try:
			open(self.SESSION_FILE)
			session_exists = True
		except FileNotFoundError:
			session_exists = False

		if session_exists:
			auth_provider.load_session(path=self.SESSION_FILE)
			auth_provider.refresh_token()

			client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)
		else:
			client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)
			
			auth_url = client.auth_provider.get_auth_url(redirect_uri)
			# Ask for the code
			print('Paste this URL into your browser, approve the app\'s access.')
			print('Copy everything in the address bar after "code=", and paste it below.')
			print(auth_url)
			code = input('Paste code here: ')

			client.auth_provider.authenticate(code, redirect_uri, self.client_secret)
			client.auth_provider.save_session(path=self.SESSION_FILE)

		return client

	def bauthenticator(self):
		from onedrivesdk.helpers.resource_discovery import ResourceDiscoveryRequest

		discovery_uri = 'https://api.office.com/discovery/'
		auth_server_url='https://login.microsoftonline.com/common/oauth2/authorize'
		auth_token_url='https://login.microsoftonline.com/common/oauth2/token'

		http = onedrivesdk.HttpProvider()
		auth = onedrivesdk.AuthProvider(http,
		                                client_id,
		                                auth_server_url=auth_server_url,
		                                auth_token_url=auth_token_url)
		auth_url = auth.get_auth_url(redirect_uri)
		code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)
		auth.authenticate(code, redirect_uri, client_secret, resource=discovery_uri)
		# If you have access to more than one service, you'll need to decide
		# which ServiceInfo to use instead of just using the first one, as below.
		service_info = ResourceDiscoveryRequest().get_service_info(auth.access_token)[0]
		auth.redeem_refresh_token(service_info.service_resource_id)
		client = onedrivesdk.OneDriveClient(service_info.service_resource_id + '/_api/v2.0/', auth, http)

		return client

	def get_item(self, id):
		return self.client.item(drive="me", id=id).get()

	def get_folder_path(self, path):
		path_data = path.rsplit('/', 1)

		if len(path_data) == 1:
			return "", path_data[0]

		return path_data

	def get_item_parent_reference(self, id):
		return self.get_item(id).parent_reference.id

	def get_items(self, id):
		items = self.client.item(drive='me', id=id).children.get()
		return items

	def _find_item_id(self, path, id):
		searched_path = path.pop(0).strip()

		if searched_path == ".":
			found_id = self.working_dir_id
		elif searched_path == "..":
			found_id = self.get_item_parent_reference(self.working_dir_id)
		elif searched_path == "":
			found_id = id
		else:
			items = self.get_items(id)

			for item in items:
				if item.name == searched_path:
					break
			else:
				raise RemoteFileNotFoundError

			found_id = item.id

		if len(path) == 0:
			return found_id if found_id is not None else 'root'
		else:
			return self._find_item_id(path, found_id)

	def find_item_id(self, path):
		path = normpath(path)

		if path == '':
			return self.working_dir_id

		if path == '/':
			return 'root'

		if isinstance(path, str):
			parts = path.split('/')

		if isabs(path):
			id = "root"
			parts = parts[1:]
		else:
			id = self.working_dir_id

		return self._find_item_id(parts, id)

	def pwd(self):
		return self.working_dir_path

	def cd(self, path):
		if path != '':
			item = self.get_item(self.find_item_id(path))
			
			if item.folder is None:
				raise InvalidRemoteDirectoryError
			else:
				self.working_dir_id = item.id

				self.working_dir_path = self.abspath(path)

		return self.working_dir_path

	def abspath(self, path):
		return normpath(join(self.working_dir_path, path))

	def dir(self, path):
		return self.get_items(self.find_item_id(path))
		
	def mkdir(self, *paths):
		created_dirs = []
		for path in paths:
			path = normpath(path)
			base_path, folder_name = split(path)

			id = self.find_item_id(base_path)

			f = onedrivesdk.Folder()
			i = onedrivesdk.Item()

			i.name = folder_name
			i.folder = f

			dir = self.client.item(drive='me', id=id).children.add(i)

			created_dirs.append(dir)

		return created_dirs

	def delete(self, path):
		id = self.find_item_id(path)

		self.client.item(drive='me', id=id).delete()

	def upload(self, local_path, remote_path):
		path, file_name = os.path.split(local_path)

		remote_head_path, remote_filename = split(remote_path)

		file_name = (file_name if remote_filename == '' or remote_filename in ('.', '..') else remote_filename)
		
		id = self.find_item_id(remote_path if remote_filename in ('.', '..') else remote_head_path)

		self.client.item(drive='me', id=id).children[file_name].upload(local_path)

	def download(self, remote_path, local_path):
		remote_folder_path, remote_filename = split(remote_path)

		id = self.find_item_id(remote_path)

		local_path = os.path.abspath(local_path)

		local_folder_path, local_filename = os.path.split(local_path)

		self.client.item(drive='me', id=id).download(os.path.abspath(local_path) + (remote_filename if local_filename == '' else ''))
