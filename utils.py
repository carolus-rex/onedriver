import posixpath

from time import strftime


def isabs(path):
	return path.startswith('/')


def split(path):
	if '/' not in path:
		return '', path

	path_data = path.rsplit('/', 1)

	if isabs(path) and len(path_data[0]) == 0:
		return '/' , path_data[1]
 
	return path_data


def normpath(path):
	return posixpath.normpath(path)


def join(a, *p):
	"""Join two or more pathname components, inserting '/' as needed.
   	If any component is an absolute path, all previous path components
   	will be discarded.  An empty last part will result in a path that
   	ends with a separator."""
	sep = '/'
	path = a
	try:
		for b in p:
			if b.startswith(sep):
   	    	    		path = b
			elif not path or path.endswith(sep):
   	    	    		path += b
			else:
   	    	    		path += sep + b
	except TypeError:
   	    valid_types = all(isinstance(s, (str, bytes, bytearray))
   	                      for s in (a, ) + p)
   	    if valid_types:
   	        # Must have a mixture of text and binary data
   	        raise TypeError("Can't mix strings and bytes in path "
   	                        "components.") from None
   	    raise
	return path

def date_to_meridian(datestring):
	if '.' in datestring:
		timestamp = time.mktime(datetime.datetime.strptime(datestring, "%Y-%m-%d %H:%M:%S.%f").timetuple())
	else:
		timestamp = time.mktime(datetime.datetime.strptime(datestring, "%Y-%m-%d %H:%M:%S").timetuple())

	return strftime('%d/%m/Y  %I:%M %p', timestamp)

#print(os.path.normpath('/daily_metal'))