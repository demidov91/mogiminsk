pybabel extract . -o locale/_tmp_messages.po

msgmerge locale/ru/LC_MESSAGES/messages.po locale/_tmp_messages.po -o locale/ru/LC_MESSAGES/messages.po --lang=ru
msgmerge locale/be/LC_MESSAGES/messages.po locale/_tmp_messages.po -o locale/be/LC_MESSAGES/messages.po --lang=be

rm locale/_tmp_messages.po
