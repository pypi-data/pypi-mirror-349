import os
import sys
import re
import netrc
import logging
import requests
import json
import pprint
import traceback

logger = logging.getLogger(__name__)
logging.basicConfig(
		format="%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s",datefmt='%Y-%m-%d %H:%M:%S',
		handlers=[
			logging.StreamHandler(sys.stdout)
		],
		level=logging.INFO
	)


class NotFoundError(Exception):    
	def __init__(self, message):
		super().__init__(message)

class ArgumentNotFoundError(Exception):    
	def __init__(self, message):
		super().__init__(message)
	
class InternalServerError(Exception):    
	def __init__(self, message):
		super().__init__(message)

class PermissionDeniedError(Exception):    
	def __init__(self, message):
		super().__init__(message)
		
class DAHITI:
	
	api_url = "https://dahiti.dgfi.tum.de/api/v2/"
	
	def __init__(self, log_level=logging.INFO, debug=0):
		
		' set log level '
		logger.setLevel(log_level)
		
		if debug == 1:
			self.api_url = "https://dahiti.dgfi.tum.de:8002/api/v2/"
			logger.warning("Debug-API enabled ("+str(self.api_url)+")!")
			
		' read credential from ~/.netrc '		
		n = netrc.netrc()
		credentials = n.authenticators('dahiti.dgfi.tum.de')
		if credentials == None:
			logger.error('No credentials found in ~/.netrc')
			sys.exit(0)
		
		self.username = credentials[0]
		self.api_key = credentials[2]
		logger.info('Username: '+str(self.username))
		logger.info('API-Key: '+str(self.api_key))

		' authenicate user '		
		response = self.send_api_request(
			self.api_url+'auth/',
			{			
				'api_key' :  self.api_key
			}
		)
		if response.status_code == 200:
			logger.info('Authentication successful!')
		
	def send_api_request(self, url, args):
		
		response = requests.post(url, json=args)				
			
		if response.status_code == 400:	
			json_response = json.loads(response.text)			
			logger.error('400 - DAHITI-API url not found!')
			raise ArgumentNotFoundError(json_response['message'])
		elif response.status_code == 403:	
			json_response = json.loads(response.text)
			logger.error('403 - Permission denied!')
			raise PermissionDeniedError(json_response['message'])	
		elif response.status_code == 404:	
			json_response = json.loads(response.text)
			logger.error('404 - DAHITI target not found!')
			raise NotFoundError(json_response['message'])
		elif response.status_code == 500:
			json_response = json.loads(response.text)
			logger.error('500 - Internal Server Error')			
			raise InternalServerError(json_response['message'])	
					
		return response
	
	def get_quality_assessment(self, dahiti_id, dataset, software, parameters=None):
		
		logger.info('Get quality assessment of DAHITI target with id '+str(dahiti_id)+' ...')
		
		response = self.send_api_request(
			self.api_url+'get-quality-assessment/',
			{			
				'api_key' :  self.api_key,
				'dahiti_id' : dahiti_id,
				'dataset' : dataset,
				'software' : software,
				'parameters' : parameters
			}
		)
				
		return response
	
	def download_water_level(self, dahiti_id, software=None, path=None, parameters=None):
		
		logger.info('Download water levels DAHITI target with id '+str(dahiti_id)+' ...')
		
		response = self.send_api_request(
			self.api_url+'download-water-level/',
			{			
				'api_key' :  self.api_key,
				'dahiti_id' : dahiti_id,
				'format' : 'json',
				'software' : software,
				'parameters' : parameters,
			}
		)
		if type(response) == requests.models.Response:
			json_response = json.loads(response.text)						
			try:
				if path != None:
					logger.info('Writing data to '+path+' ...')
					if re.match('.*json',path) != None:
						with open(path, 'w') as f:
							json.dump(json_response, f)
					elif re.match('.*pkl',path) != None:
						file = open(path, 'wb')
						pickle.dump(json_response, file)
						file.close()				
					else:
						output = open(path,'w')
						for row in json_response['data']:							
							output.write(str(row['datetime'])+' '+str(row['wse'])+' '+str(row['wse_u']))
							if parameters != None and 'mission' in row:
								output.write(" "+str(row['mission']))
							if parameters != None and 'pass_nr' in row:
								output.write(" "+str(row['pass_nr']))
							if parameters != None and 'cycle' in row:
								output.write(" "+str(row['cycle']))
							if parameters != None and 'num_points' in row:
								output.write(" "+str(row['num_points']))
							output.write('\n')
						output.close()
				else:									
					return json_response
			except:
				traceback.print_exc()
				
		return response
	
	def download_surface_area(self, dahiti_id, software=None, path=None, parameters=None):
		
		logger.info('Download surface area DAHITI target with id '+str(dahiti_id)+' ...')
		
		response = self.send_api_request(
			self.api_url+'download-surface-area/',
			{			
				'api_key' :  self.api_key,
				'dahiti_id' : dahiti_id,
				'format' : 'json',
				'software' : software,
				'parameters' : parameters,
			}
		)
		if type(response) == requests.models.Response:
			json_response = json.loads(response.text)			
			pprint.pprint(json_response)
			try:
				if path != None:
					logger.info('Writing data to '+path+' ...')
					if re.match('.*json',path) != None:
						with open(path, 'w') as f:
							json.dump(json_response, f)
					elif re.match('.*pkl',path) != None:
						file = open(path, 'wb')
						pickle.dump(json_response, file)
						file.close()				
					else:
						output = open(path,'w')
						for row in json_response['data']:							
							output.write(str(row['datetime'])+' '+str(row['water_level'])+' '+str(row['error']))
							if parameters != None and 'mission' in row:
								output.write(" "+str(row['mission']))
							if parameters != None and 'pass_nr' in row:
								output.write(" "+str(row['pass_nr']))
							if parameters != None and 'cycle' in row:
								output.write(" "+str(row['cycle']))
							if parameters != None and 'num_points' in row:
								output.write(" "+str(row['num_points']))
							output.write('\n')
						output.close()
				else:
					return json_response
			except:
				traceback.print_exc()
				
		return response
	
	def download_water_occurrence_mask(self, dahiti_id, software=None, path=None):
		
		logger.info('Download water occurrence mask of DAHITI target with id '+str(dahiti_id)+' ...')
		
		response = self.send_api_request(
			self.api_url+'download-water-occurrence-mask/',
			{			
				'api_key' :  self.api_key,
				'dahiti_id' : dahiti_id,
				'software' : software
			}
		)
		if type(response) == requests.models.Response:
			#~ json_response = json.loads(response.text)			
			#~ pprint.pprint(response.text)
			logger.info('Writing data to '+path+' ...')
			print (type(response.text))
			print (response.text[0:200])
			output = open(path,'wb')
			output.write(response.text)
			output.close()
			"""
			try:
				if path != None:
					logger.info('Writing data to '+path+' ...')
					if re.match('.*json',path) != None:
						with open(path, 'w') as f:
							json.dump(json_response, f)
					elif re.match('.*pkl',path) != None:
						file = open(path, 'wb')
						pickle.dump(json_response, file)
						file.close()				
					else:
						output = open(path,'w')
						for row in json_response['data']:							
							output.write(str(row['datetime'])+' '+str(row['water_level'])+' '+str(row['error']))
							if parameters != None and 'mission' in row:
								output.write(" "+str(row['mission']))
							if parameters != None and 'pass_nr' in row:
								output.write(" "+str(row['pass_nr']))
							if parameters != None and 'cycle' in row:
								output.write(" "+str(row['cycle']))
							if parameters != None and 'num_points' in row:
								output.write(" "+str(row['num_points']))
							output.write('\n')
						output.close()
				else:
					return json_response
			except:
				traceback.print_exc()
			"""
		return response
		
	def download_water_surface_slope(self, dahiti_id, software=None, path=None, parameters=None):
		
		logger.info('Download water surface slope of DAHITI target with id '+str(dahiti_id)+' ...')
		
		response = self.send_api_request(
			self.api_url+'download-water-surface-slope/',
			{			
				'api_key' :  self.api_key,
				'dahiti_id' : dahiti_id,
				'format' : 'json',
				'software' : software,
				'parameters' : parameters,
			}
		)		
		if type(response) == requests.models.Response:
			json_response = json.loads(response.text)			
			try:
				if path != None:
					logger.info('Writing data to '+path+' ...')
					if re.match('.*json',path) != None:
						with open(path, 'w') as f:
							json.dump(json_response['data'], f)
					elif re.match('.*pkl',path) != None:
						file = open(path, 'wb')
						pickle.dump(json_response['data'], file)
						file.close()				
					else:
						output = open(path,'w')
						for row in json_response['data']:	
							print (row)
							output.write(str(row['datetime'])+' '+str(row['water_level'])+' '+str(row['error']))
							if parameters != None and 'mission' in row:
								output.write(" "+str(row['mission']))
							if parameters != None and 'pass_nr' in row:
								output.write(" "+str(row['pass_nr']))
							if parameters != None and 'cycle' in row:
								output.write(" "+str(row['cycle']))
							if parameters != None and 'num_points' in row:
								output.write(" "+str(row['num_points']))
							output.write('\n')
						output.close()
				else:
					return json_response['data']
			except:
				traceback.print_exc()
				
		return response
		
	def get_target_info(self, dahiti_id, software=None, path=None):
		
		logger.info('Get target info DAHITI target with id '+str(dahiti_id)+' ...')
		
		response = self.send_api_request(
			self.api_url+'get-target-info/',
			{			
				'api_key' :  self.api_key,
				'dahiti_id' : dahiti_id,
			}
		)
		
		if type(response) == requests.models.Response:
			json_response = json.loads(response.text)	
			return json_response['data']
			
		return response
	
	def list_targets(self,args):
		
		logger.info('List targets ...')
		
		args['api_key'] = self.api_key
		
		response = self.send_api_request(
			self.api_url+'list-targets/',
			args
		)	
				
		if type(response) == requests.models.Response:
			json_response = json.loads(response.text)
			logger.info(str(len(json_response['data']))+' target(s) found!')
			return json_response['data']
			
		return response
	
	def create_target(self, args):
		
		logger.info('Create new DAHITI target ...')
		
		args['api_key'] = self.api_key
		
		response = self.send_api_request(
			self.api_url+'create-target/',
			args
		)
		
		if type(response) == requests.models.Response:
			json_response = json.loads(response.text)
			return json_response['dahiti_id']
			
		return response
	
	def update_AOI_from_SWORD(self, dahiti_id, args):
		
		logger.info('Update AOI from SWORD ...')
		
		args['api_key'] = self.api_key
		args['dahiti_id'] = dahiti_id		
		
		response = self.send_api_request(
			self.api_url+'update-AOI-from-SWORD/',
			args
		)
		
		if type(response) == requests.models.Response:
			json_response = json.loads(response.text)
			return json_response['data']
			
		return response
	
	def update_AOI_from_JRC(self, dahiti_id, args):
		
		logger.info('Update AOI from JRC ...')
		
		args['api_key'] = self.api_key
		args['dahiti_id'] = dahiti_id		
		
		response = self.send_api_request(
			self.api_url+'update-AOI-from-JRC/',
			args
		)
		
		if type(response) == requests.models.Response:
			json_response = json.loads(response.text)
			return json_response['data']
			
		return response
		
	def is_location_in_AOI(self, args):
		
		logger.info('Is location in AOI ...')
		
		args['api_key'] = self.api_key
		
		response = self.send_api_request(
			self.api_url+'is-location-in-AOI/',
			args
		)
		
		if type(response) == requests.models.Response:
			json_response = json.loads(response.text)
			return json_response['data']
			
		return response
	
	def get_targets_in_AOI(self, args):
		
		logger.info('Get DAHITI targets in AOI ...')
		
		args['api_key'] = self.api_key
		
		response = self.send_api_request(
			self.api_url+'get-targets-in-AOI/',
			args
		)
		
		if type(response) == requests.models.Response:
			json_response = json.loads(response.text)
			return json_response['data']
			
		return response
	
	def update_PLD_information(self, dahiti_id):
		
		logger.info('Update PLD information ...')
		
		args = {}
		args['api_key'] = self.api_key
		args['dahiti_id'] = dahiti_id		
		
		response = self.send_api_request(
			self.api_url+'update-PLD-information/',
			args
		)
		
		if type(response) == requests.models.Response:
			json_response = json.loads(response.text)
			return json_response['data']
			
		return response
	
	def get_spreadsheet(self, args):
		
		logger.info('Get Spreadsheet ...')
		
		args['api_key'] = self.api_key
		
		response = self.send_api_request(
			self.api_url+'get-spreadsheet/',
			args
		)
		
		if type(response) == requests.models.Response:
			json_response = json.loads(response.text)
			return json_response['data']
			
		return response
	
	def get_country(self, tld):
		
		logger.info('Get Country ...')
		
		args = {}
		args['api_key'] = self.api_key
		args['tld'] = tld
		
		response = self.send_api_request(
			self.api_url+'get-country/',
			args
		)
		
		if type(response) == requests.models.Response:
			json_response = json.loads(response.text)
			return json_response['data']
			
		return response
		
	def get_targets_by_reach_id(self, reach_id):
		
		logger.info('Get DAHITI targets by reach_id `'+reach_id+'` ...')
		
		args = {}
		args['api_key'] = self.api_key
		args['reach_id'] = reach_id
		
		response = self.send_api_request(
			self.api_url+'get-targets-by-reach-id/',
			args
		)
		
		if type(response) == requests.models.Response:
			json_response = json.loads(response.text)
			return json_response['data']
			
		return response
		
