import discord
from discord import utils
from discord.ext import commands

import config

client = commands.Bot(command_prefix='.', intents=discord.Intents.all())

hello_list = ['hello bot', 'hi bot', 'привет, бот', 'ку, бот', 'хай, бот', 'чуп-чуп', 'чуп', 'привет, бот!',
                                                                                             'за чупленд!']
question_list = ['узнать информацию', 'команды', 'чуп?', 'помощь', 'что ты умеешь?', 'команды бота', 'команды сервера']
bye_list = ['пока', 'удачи!', 'чуп!', 'bye', 'goodbye', 'bb']
# black_list = ['пидр', 'нахуй', 'еблан', 'пидорас', 'заебал', 'даун', 'конч', 'хуй', 'пизда', 'блядина', 'ебало',
            #  'уёбище']


@client.event
async def on_ready():
    print('logged on!')


@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == config.POST_ID:
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.get(message.guild.members, id=payload.user_id)

        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=config.ROLES[emoji])

            if len([i for i in member.roles if i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER:
                await member.add_roles(role)
                print('[SUCCESS] User {0.display_name}  has been granted with role {1.name}'.format(member, role))
            else:
                await message.remove_reaction(payload.emoji, member)
                print('[ERROR] Too many roles for user {0.display_name}'.format(member))

        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))


@client.event
async def on_raw_reaction_remove(payload):
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    member = utils.get(message.guild.members, id=payload.user_id)

    try:
        emoji = str(payload.emoji)
        role = utils.get(message.guild.roles, id=config.ROLES[emoji])

        await member.remove_roles(role)
        print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))

    except KeyError as e:
        print('[ERROR] KeyError, no role found for ' + emoji)
    except Exception as e:
        print(repr(e))


@client.event
async def on_member_join(member):
    channel = client.get_channel(543857438345003040)
    role = discord.utils.get(member.guild.roles, id=config.AUTOROLE)
    await channel.send(f"Приветствуем {member.mention} в волшебной стране Чупленд!\n"
                       f"Назначаю тебя Чупакабриком, надеюсь тебе понравится у нас.")
    await member.add_roles(role)


@client.event
async def on_message(message):
    msg = message.content.lower()
    msg_list = set(msg.split())
    # print('Message from {0.author}: {0.content}'.format(message))
    if msg in hello_list:
        await message.channel.send('Приветствую, житель Чупленда!')
    if msg == 'найс найс найс':
        await message.channel.send('Ультра-мега-найс!')
    if msg in question_list:
        await message.channel.send('Чтобы узнать, что я умею, просто напиши команду .help')
    if msg in bye_list:
        await message.channel.send('Пока, удачи!')
   # for k in msg_list:
        #if k in black_list:
            #await message.delete()
    await client.process_commands(message)


@client.command(pass_context=True)
async def poem(ctx, *, response):
    await ctx.send('Какое стихотворение ты хочешь прочесть?\n'
                   '1 - стихотворение про Великого Огура\n'
                   '2 - стихотворение про Старого Мужлана')
    if response == 1:
        ctx.send('Огур, свет ты лучезарный\n' 
                            'Где гуляешь ты?\n'
                            'Какие перешел мосты?\n')
'''
мосты надежд, разлуки время
губят меня словно тысячелетнее бремя

Вернись Огур , вернись домой 
что тебя тревожит , сын мой? 
Может сила бога , наделяющая тебя 
только в чем проблема, не пойму я?

Огур пропал , на веки вечные
все жду и жду его старея 
но вскоре смерть моя придет
Умру я, не жалея

Огур , где ты ? 
спаси ты мою бездушную душонку
Забери с собой как время,воду,ветер твой

Огур, нет сил объяснять
насколько дорог мне.
ты мне дай понять , есть ли жизнь во мне?')
'''


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)


@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def ping(ctx):
    await ctx.send('pong')



client.run(config.token)
