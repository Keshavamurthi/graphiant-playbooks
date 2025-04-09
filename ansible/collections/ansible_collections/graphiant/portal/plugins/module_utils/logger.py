import logging

def setup_logger(logfile="logs/ansible.log", level=logging.INFO):
    logger = logging.getLogger("Graphiant_playbook")
    logger.setLevel(level)

    # Prevent duplicate handlers in Jupyter/IDE environments
    if not logger.handlers:
        # File handler
        fh = logging.FileHandler(logfile)
        fh.setLevel(level)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)  # Only errors to console
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        # Add handlers
        logger.addHandler(fh)
        logger.addHandler(ch)
    
    return logger