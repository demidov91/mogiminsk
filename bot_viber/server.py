from messager.bot_server import BotServer


class ViberServer(BotServer):
    @classmethod
    def get_bot_context(cls, user):
        return user.viber_context

    @classmethod
    def set_bot_context(cls, user, full_context: dict):
        user.viber_context = full_context

    @classmethod
    async def get_remote_update(cls, request):
        pass
    @classmethod
    def get_or_create_user(cls, remote_update):
        pass

    @classmethod
    async def send_the_answer(cls, request, update, bot_messages):
        pass

    @classmethod
    def get_response(cls, update):
        pass