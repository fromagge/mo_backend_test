
def str_to_bool(value: str | bool) -> bool:
	if type(value) == bool:
		return value

	if value.lower() == 'true':
		return True
	elif value.lower() == 'false':
		return False
	return False
