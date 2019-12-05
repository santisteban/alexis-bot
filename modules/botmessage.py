import discord

from bot import Command, categories
from bot.utils import str_to_embed
from bot.regex import pat_channel, pat_snowflake


class BotSendMessage(Command):
    __version__ = '1.0.0'
    __author__ = 'makzk'

    def __init__(self, bot):
        super().__init__(bot)
        self.name = 'message'
        self.help = '$[botmsg-help]'
        self.format = '$[botmsg-format]'
        self.owner_only = True
        self.allow_pm = False
        self.category = categories.STAFF

    async def handle(self, cmd):
        if cmd.argc < 2 or not pat_channel.match(cmd.args[0]):
            await cmd.answer('$[format]: $[botmsg-format]')
            return

        chan = self.bot.get_channel(cmd.args[0][2:-1])
        if chan is None or chan.server.id != cmd.guild.id:
            await cmd.answer('$[botmsg-channel-not-found]')
            return

        try:
            text = ' '.join(cmd.args[1:])
            args = text.split('|')
            embed = None
            if len(args) > 2:
                embed = str_to_embed('|'.join(args[1:]))

            await self.bot.send_message(content=args[0], destination=chan, embed=embed)
        except discord.Forbidden:
            await cmd.answer('$[botmsg-error-perms]')


class BotEditMessage(Command):
    __version__ = '1.0.0'
    __author__ = 'makzk'

    def __init__(self, bot):
        super().__init__(bot)
        self.name = 'edit'
        self.help = '$[botmsg-edit-help]'
        self.owner_only = True
        self.allow_pm = False
        self.category = categories.STAFF

    async def handle(self, cmd):
        if cmd.argc < 3 or not pat_channel.match(cmd.args[0]) or not pat_snowflake.match(cmd.args[1]):
            await cmd.answer('$[format]: $[botmsg-format]')
            return

        chan = self.bot.get_channel(cmd.args[0][2:-1])
        if chan is None or chan.server.id != cmd.guild.id:
            await cmd.answer('$[botmsg-channel-not-found]')
            return

        msg = await self.bot.get_message(chan, cmd.args[1])
        if msg is None:
            await cmd.answer('$[botmsg-not-found]')
            return

        text = ' '.join(cmd.args[1:])
        args = text.split('|')
        embed = None
        if len(args) > 2:
            embed = str_to_embed('|'.join(args[1:]))

        await self.bot.edit_message(msg, args[0], embed=embed)
