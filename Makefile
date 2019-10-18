# ? use filename + "_" + command
# * example: $ prepare_dev

include makes/cmd.mk
# [clean]

include makes/prepare.mk
# [dev, prod]

include makes/django.mk
# [runserver, startapp app=name]

include makes/git.mk
# [push]
