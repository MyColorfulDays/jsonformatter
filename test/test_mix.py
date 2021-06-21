import logging

from jsonformatter import JsonFormatter

root = logging.getLogger()
root.setLevel(logging.INFO)

sh = logging.StreamHandler()
formatter = JsonFormatter(
    ensure_ascii=False,
    mix_extra=True,
    mix_extra_position='tail'  # optional: head, mix
)
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)
root.addHandler(sh)

root.info(
    'test mix extra in fmt',
    extra={
        'extra1': 'extra content 1',
        'extra2': 'extra content 2'
    })
root.info(
    'test mix extra in fmt',
    extra={
        'extra3': 'extra content 3',
        'extra4': 'extra content 4'
    })
