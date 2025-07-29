from loguru import logger 

def say_hello(name:str = None) -> str:
    text = "Hello Bro !" if not name else f"Hello {name}"
    logger.success(text)
    return text 