#!/usr/bin/env python3
#-*-coding:utf8-*-
import sys
import inspect
import logging
import logging.handlers

_single_logger = logging.getLogger('easylog')
_level_enable_list = [False,False,False,False,False]  # DEBUG, INFO, WARNING, ERROR, CRITICAL
_cur_special_flag = None

def setup(log_name="nohup_0.out", level='debug', log_file_enable=False ,file_size_mb=4, file_count=2):
	format = '[PID:%(process)d %(asctime)s-%(levelname)s %(message)s'
	ipa_format = logging.Formatter(format)
	if level == 'debug':
		enable_index = 0
		_single_logger.setLevel(logging.DEBUG)
	elif level == 'info':
		enable_index = 1
		_single_logger.setLevel(logging.INFO)
	elif level == 'warning':
		enable_index = 2
		_single_logger.setLevel(logging.WARNING)
	elif level == 'error':
		enable_index = 3
		_single_logger.setLevel(logging.ERROR)
	elif level == 'critical':
		enable_index = 4
		_single_logger.setLevel(logging.CRITICAL)
	else:
		_single_logger.error('Unknown level:%s WARNING will be used')
		enable_index = 2
		_single_logger.setLevel(logging.WARNING)
		
	for i in range(enable_index, 5):
		_level_enable_list[i] = True
	
	if log_file_enable:
		handler = logging.handlers.RotatingFileHandler(log_name, maxBytes=1024*1024*file_size_mb, backupCount=file_count)
		handler.setFormatter(ipa_format)
		_single_logger.addHandler(handler)
	else:
		# writes to stderr
		handler = logging.StreamHandler(stream=sys.stdout) 
		handler.setFormatter(ipa_format)
		_single_logger.addHandler(handler)


def set_special_flag(special_flag):
	global _cur_special_flag
	_cur_special_flag = special_flag

def debug(format, *argv):
	if _level_enable_list[0]:
		caller_info = inspect.stack()[1]	
		_single_logger.debug("{%s} %s():%d]: " + format, _cur_special_flag, caller_info[3], caller_info[2], *argv)

def info(format, *argv):
	if _level_enable_list[1]:
		caller_info = inspect.stack()[1]	
		_single_logger.info("{%s} %s():%d]: " + format, _cur_special_flag, caller_info[3], caller_info[2], *argv)

def warning(format, *argv):
	if _level_enable_list[2]:
		caller_info = inspect.stack()[1]	
		_single_logger.warning("{%s} %s():%d]: " + format, _cur_special_flag, caller_info[3], caller_info[2], *argv)

def error(format, *argv):
	if _level_enable_list[3]:
		caller_info = inspect.stack()[1]	
		_single_logger.error("{%s} %s():%d]: " + format, _cur_special_flag, caller_info[3], caller_info[2], *argv)

def tornado_security_log(request_obj, format, *argv):
	if _level_enable_list[3] and hasattr(request_obj, "request"):
		caller_info = inspect.stack()[1]
		_single_logger.error("{%s} %s():%d][HEADERS:%s]:\n" + format, 
			_cur_special_flag, caller_info[3], caller_info[2], 
			request_obj.request.headers,
			*argv)
		
def exception(format, *argv):
	if _level_enable_list[3]:
		_single_logger.exception("{%s}]: " + format, _cur_special_flag, *argv)
	
def critical(format, *argv):
	if _level_enable_list[4]:
		caller_info = inspect.stack()[1]	
		_single_logger.critical("{%s} %s():%d]: " + format, _cur_special_flag, caller_info[3], caller_info[2], *argv)
	
