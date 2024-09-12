from nidavellir.clients.bifrost_proxy_redirects.cdc.cdc_proxy_manager import CDCProxyManager
from cdc_integration.account.users import Users
from config.environment import ENVIRONMENT
from discord.ext import commands

import discord
import random

random_color = discord.Color.from_rgb(
    random.randint(0, 255),
    random.randint(0, 255),
    random.randint(0, 255)
)
required_role_name = 'CDC ADMIN'


async def _create_person_embed(user_cdc_data: dict | None, ctx):
    if not user_cdc_data:
        embed = discord.Embed(
            title="Usuário não encontrado na CDC 😕",
            color=random_color
        )
        await ctx.send(embed=embed)
        return

    data = user_cdc_data['data'][0]

    embed = discord.Embed(
        title=f"🔍 Informações sobre: {data['name']}",
        description="Detalhes completos do usuário e suas informações bancárias.",
        color=random_color
    )

    embed.add_field(name="🆔 Código", value=data["code"], inline=False)
    embed.add_field(name="👤 Nome", value=data["name"], inline=False)
    embed.add_field(name="📊 Status", value=data["status_user"], inline=False)
    embed.add_field(name="📧 Email", value=data["email"], inline=False)
    embed.add_field(name="📞 Telefone", value=data["phone_number"], inline=False)

    if data["banking_data"]:
        banking_data = data["banking_data"][0]
        embed.add_field(name="🏦 Banco", value=f"{banking_data['bank']} (Código: {banking_data['code']})", inline=False)
        embed.add_field(name="🏢 Agência", value=banking_data["agency"], inline=True)
        embed.add_field(name="💳 Conta", value=f"{banking_data['account']} / {banking_data['digit']}", inline=True)

    embed.set_footer(text="📞 Para mais informações, consulte o suporte.", icon_url="https://i.imgur.com/PMzk8ST.png")

    await ctx.send(embed=embed)


class CdcPrd(commands.Cog):
    def __init__(self, bot, cdc_user: Users):
        self.bot = bot
        self.cdc_url = ENVIRONMENT.cateno_base_api_url
        self.cdc_user = cdc_user

    @commands.command()
    async def user(self, ctx, document):
        user = ctx.author
        if any(role.name == required_role_name for role in user.roles):
            try:
                user_info = self.cdc_user.get_user_by_document(document)
            except Exception as e:
                embed = discord.Embed(
                    title="Ocorreu algume erro!!",
                    color=random_color
                )

                embed.add_field(name="Erro: ", value=str(e), inline=False)
                await ctx.send(embed=embed)
                return

            await ctx.message.add_reaction("👍")

            await _create_person_embed(user_info, ctx)
        else:
            await ctx.send(f'Você não tem o cargo necessária para usar este comando.')




def setup(bot):
    return bot.add_cog(CdcPrd(bot, Users(proxy_manager=CDCProxyManager())))
