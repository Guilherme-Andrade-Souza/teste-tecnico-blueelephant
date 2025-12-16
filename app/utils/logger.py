import logging
import sys

def setup_logger(name: str):
    """Configura um logger padronizado para a aplicação."""
    logger = logging.getLogger(name)
    
    # Se o logger já tiver handlers, não adiciona de novo (evita logs duplicados)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Formato: [HORA] [NIVEL] [LOGGER]: MENSAGEM
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para o Console (Terminal)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        
        #Handler para Arquivo (salva em app.log)
        file_handler = logging.FileHandler("app.log", encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger