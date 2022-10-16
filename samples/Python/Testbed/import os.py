from operator import add
import os
import logging
import functools

def make_log():
    if not os.path.exists('/logging_3'):
        print('exist')
        os.makedirs('/logging_3')
    else:
        pass

logging.basicConfig(filename = 'logging_3/loggernew3', filemode = 'w', level = logging.DEBUG)

logger = logging.getLogger()
""" 
def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.exception(f'Exception raised in {func.__name__}. exception: ')
            #raise e
    return wrapper
def write_log():
    logging.error('logging created')
@log
def add_number():
    x = 2 *3 
    if x ==6:
        raise Exception('it worked')
    #logging.warning(x) """

def log(func):
        @functools.wraps(func)
        def wrappper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                logger.Exception(f'{func.__name__} had a problem')
                raise e
        return wrapper

def make_num(num):
    print('first level')
    def sq_num(num):
        print('second level')
        print (num**2)
    sq_num(num)

def outer():
    def inner():
        print('innner')
        def even_inner():
            print('even_inner')
        even_inner()
    return inner

x = outer()
    #return outer 

if __name__ == '__main__':
    x()

