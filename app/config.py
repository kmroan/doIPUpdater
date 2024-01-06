import logging,sys
handler = logging.StreamHandler(stream=sys.stdout)
logging.basicConfig(level=logging.INFO,handlers = handler,
                    format='[%(asctime)s] %(name)s %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %Z',force=True
)

logger = logging.getLogger("doIPUpdate")