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
    await client.change_presence(status=discord.Status.online, activity= discord.Game('.info'))

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
    channel = client.get_channel(816364829362749456)
    role = discord.utils.get(member.guild.roles, id=config.AUTOROLE)
    await channel.send(f"Приветствуем {member.mention} в волшебной стране Чупленд!\n"
                       f"Назначаю тебя Чупакабриком, надеюсь тебе понравится у нас.")
    await member.add_roles(role)

@client.command(pass_context=True)
async def hello(ctx, member: discord.Member):
    await member.send(f'{member.name}, привет от {ctx.author.name}')

    
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
        '''
    with open('D:\\Programming\\Python\\chuplend bot2\\chuplvls.json', 'r') as f:
        users = json.load(f)

    async def update_data(users, user):
        if (user not in users) and (user != '798451540410105866'):
            users[user] = {}
            users[user]['xp'] = 0
            users[user]['lvl'] = 1

    async def add_xp(users, user, xp):
        users[user]['xp'] += xp

    async def add_lvl(users, user):
        exp = users[user]['xp']
        lvl = users[user]['lvl']
        if exp > lvl:
            users[user]['xp'] = 0
            users[user]['lvl'] += 1
            lvl = users[user]['lvl']
            await message.channel.send(f'Чупленд поздравляет {message.author.mention} с достижением нового {lvl} уровня! ☺')

    await update_data(users, str(message.author.id))
    await add_xp(users, str(message.author.id), 0.1)
    await add_lvl(users, str(message.author.id))
    with open('D:\\Programming\\Python\\chuplend bot2\\chuplvls.json', 'w') as f:
        json.dump(users, f)
   # for k in msg_list:
        #if k in black_list:
            #await message.delete()
      '''
    await client.process_commands(message)
'''
@client.command(pass_context=True)
async def lvl(ctx):
    with open('D:\\Programming\\Python\\chuplend bot2\\chuplvls.json', 'r') as f:
         users = json.load(f)
    await ctx.send(f"У {ctx.author.mention} {users[str(ctx.author.id)]['lvl']} уровень, {round(users[str(ctx.author.id)]['xp'], 1)} опыта")

@client.command(pass_context=True)
async def poem(ctx, *, response):
    await ctx.send('Какое стихотворение ты хочешь прочесть?\n'
                   '1 - стихотворение про Великого Огура\n'
                   '2 - стихотворение про Старого Мужлана')
    if response == 1:
        ctx.send('Огур, свет ты лучезарный\n' 
                            'Где гуляешь ты?\n'
                            'Какие перешел мосты?\n')

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

@client.command(pass_context=True)
async def info(ctx, member: discord.Member):
    emb = discord.Embed(title='Информация о пользователе', color=0xFF8000)
    emb.add_field(name='Никнейм:', value=member.display_name, inline=False)
    emb.add_field(name='Роль:', value=member.top_role, inline=False)
    emb.add_field(name="На сервере с:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M"), inline=False)
    # emb.add_field(name='ID:', value=member.id, inline=False)
    emb.add_field(name="Аккаунт был создан:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M"),
                  inline=False)
    emb.set_thumbnail(url=member.avatar_url)
    # emb.set_footer(text=f"Вызвано:{ctx.message.author}", icon_url=ctx.message.author.avatar_url)
    emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=emb)

client.run(config.token)
