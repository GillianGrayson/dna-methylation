import GEOparse
import os


def get_gsm(gsm, path, is_remove=False):
    while True:
        try:
            gsm_data = GEOparse.get_GEO(geo=gsm, destdir=f'{path}', include_data=False, how="quick", silent=True)
            if is_remove:
                os.remove(f'{path}/{gsm}.txt')
        except ValueError:
            continue
        except IOError:
            continue
        except ConnectionError:
            continue
        break
    return gsm_data
