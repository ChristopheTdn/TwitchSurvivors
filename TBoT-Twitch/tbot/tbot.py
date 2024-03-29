"""
▄▄▄▄▄▄▄▌ ▐ ▄▌▪  ▄▄▄▄▄ ▄▄·  ▄ .▄
•██  ██· █▌▐███ •██  ▐█ ▌▪██▪▐█
 ▐█.▪██▪▐█▐▐▌▐█· ▐█.▪██ ▄▄██▀▐█
 ▐█▌·▐█▌██▐█▌▐█▌ ▐█▌·▐███▌██▌▐▀
 ▀▀▀  ▀▀▀▀ ▀▪▀▀▀ ▀▀▀ ·▀▀▀ ▀▀▀ ·
    .▄▄ · ▄• ▄▌▄▄▄   ▌ ▐·▪   ▌ ▐·      ▄▄▄  .▄▄ ·
    ▐█ ▀. █▪██▌▀▄ █·▪█·█▌██ ▪█·█▌▪     ▀▄ █·▐█ ▀.
    ▄▀▀▀█▄█▌▐█▌▐▀▀▄ ▐█▐█•▐█·▐█▐█• ▄█▀▄ ▐▀▀▄ ▄▀▀▀█▄
     █▄▪▐█▐█▄█▌▐█•█▌ ███ ▐█▌ ███ ▐█▌.▐▌▐█•█▌▐█▄▪▐█
     ▀▀▀▀  ▀▀▀ .▀  ▀. ▀  ▀▀▀. ▀   ▀█▄▀▪.▀  ▀ ▀▀▀▀
----------------------------------------------------------------
Game integration in twitch and project zomboid

Idea : Thibaud "TancredTerror"
code : Christophe 'GToF_' Tdn
Overlay : Thomas 'Masoht_'
Github : https://github.com/ChristopheTdn/TwitchSurvivors

"""
import json
import twitchio
import asyncio
from twitchio.ext import commands
import os
from tbot.tbot_bdd import TBOT_BDD
from . import tbot_com

with open("./Configuration/config.json", "r", encoding="utf-8") as fichier:
    CONFIG = json.load(fichier)

with open(
    "./Configuration/Secret/config_Token_Client.json", "r", encoding="utf-8"
) as fichier:
    CLIENT = json.load(fichier)

TBOTPATH, filename = os.path.split(__file__)
TBOTBDD = TBOT_BDD(TBOTPATH)


class TBoT(commands.Bot):
    """Bot Twitch basé sur le package TWITCH IO"""

    def __init__(self):
        # Initialise our Bot with our access token,
        # prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns
        # a list of strings or a string...
        # initial_channels can also be a callable
        # which returns a list of strings...
        super().__init__(
            token=CLIENT["TOKEN"],
            prefix=CLIENT["PREFIX"],
            initial_channels=[CLIENT["CHANNEL"]],
        )
        TBOTBDD.initTableSql()
        with open("./Data/raid.json", "r", encoding="utf-8") as fichier:
            self.config_raid_json = json.load(fichier)
        self.BASE_READY = bool(CONFIG["BASE_READY"])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...

        print("▄▄▄▄▄▄▄▌ ▐ ▄▌▪  ▄▄▄▄▄ ▄▄·  ▄ .▄")
        print("•██  ██· █▌▐███ •██  ▐█ ▌▪██▪▐█")
        print(" ▐█.▪██▪▐█▐▐▌▐█· ▐█.▪██ ▄▄██▀▐█")
        print(" ▐█▌·▐█▌██▐█▌▐█▌ ▐█▌·▐███▌██▌▐▀")
        print(" ▀▀▀  ▀▀▀▀ ▀▪▀▀▀ ▀▀▀ ·▀▀▀ ▀▀▀ ·")
        print("    .▄▄ · ▄• ▄▌▄▄▄   ▌ ▐·▪   ▌ ▐·      ▄▄▄  .▄▄ ·")
        print("    ▐█ ▀. █▪██▌▀▄ █·▪█·█▌██ ▪█·█▌▪     ▀▄ █·▐█ ▀.")
        print("    ▄▀▀▀█▄█▌▐█▌▐▀▀▄ ▐█▐█•▐█·▐█▐█• ▄█▀▄ ▐▀▀▄ ▄▀▀▀█▄")
        print("     █▄▪▐█▐█▄█▌▐█•█▌ ███ ▐█▌ ███ ▐█▌.▐▌▐█•█▌▐█▄▪▐█")
        print("     ▀▀▀▀  ▀▀▀ .▀  ▀. ▀  ▀▀▀. ▀   ▀█▄▀▪.▀  ▀ ▀▀▀▀")
        print("")
        print(f"Logged in as : {self.nick}")
        print(f"User id is : {self.user_id}")
        await tbot_com.msg_init_TboT()
        if not self.BASE_READY:
            await tbot_com.message(
                key="error_no_base",
                channel=self.get_channel(CLIENT["NICK"]),
                name=CLIENT["NICK"],
            )
        else:
            await tbot_com.message(
                key="base_in_place",
                channel=self.get_channel(CLIENT["NICK"]),
                name=CLIENT["NICK"],
            )

        await self.timer_Raid()

    async def timer_Raid(self):
        channel = self.get_channel(CLIENT["CHANNEL"])
        while True:
            await TBOTBDD.actualise_statRaid(channel)
            await asyncio.sleep(
                CONFIG["TIMING"]
            )  # defini le cycle en seconde de progression et MaJ des raids.

    async def event_message(self, message: twitchio.Message):
        if message.echo:
            return

        # channel = self.get_channel("GToF_")
        # channel = message.channel#
        # await channel.send('coucou') #envois directement
        # un message dans le channel a l origine du message
        # Print the contents of our message to console...
        print(message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    async def creation_survivant(self, ctx: commands.Context):
        """active le flag ALIVE du survivant apès avoir testé son existence
           et si les credits sont suffisants

        Args:
            ctx: commands.Context twitchIo
        """
        survivant = await TBOTBDD.get_stats_survivant(ctx.author.id)
        if (
            survivant is not None and survivant["alive"] == 1
        ):  # le pseudo existe deja dans la base de donnée
            await tbot_com.message(
                "survivant_exist", channel=ctx.channel, name=survivant["name"]
            )
        elif (
            # le survivant doit etre ressucité
            survivant is not None and survivant["alive"] == 0
        ):
            # pas assez de credit
            if survivant["credit"] < CONFIG["COUT_REVIVE"]:
                await tbot_com.message(
                    "survivant_credit_insuffisant",
                    channel=ctx.channel,
                    name=survivant["name"],
                    credit=str(CONFIG["COUT_REVIVE"]),
                )
            # mort en raid
            elif survivant["inraid"] == 1:
                await tbot_com.message(
                    "survivant_revive_impossible_en_raid",
                    channel=ctx.channel,
                    name=survivant["name"],
                )
            else:
                # on peut faire revivre le survivant
                await TBOTBDD.revive_survivant(ctx.author.id)
                await tbot_com.message(
                    "revive_survivant",
                    channel=ctx.channel,
                    name=survivant["name"],
                    credit=str(CONFIG["COUT_REVIVE"]),
                )
        else:
            await tbot_com.message(
                "survivant_no_exist",
                channel=ctx.channel,
                name=ctx.author.display_name
            )

    async def ajout_credit(
        self, id_twitch, name, channel, credit: int = CONFIG["AJOUT_CREDIT"]
    ):
        """ajoute des credits au survivant

        Args:
            name (str): nom du survivant
            channel (_type_): channel twitch id
            CREDIT (_type_, optional): nombre de crédits.
                                       Default à CONFIG["AJOUT_CREDIT"].
        """

        survivant = await TBOTBDD.get_stats_survivant(id_twitch)
        if survivant is None:
            await TBOTBDD.create_survivant(id_twitch, name)

        await TBOTBDD.add_credit(id_twitch, credit=credit)
        await tbot_com.message(
            "survivant_ajout_credit",
            credit=str(credit),
            channel=channel,
            name=name
        )

        survivant = await TBOTBDD.get_stats_survivant(id_twitch)

        if (
            survivant["alive"] is False
            and survivant["inraid"] is False
            and survivant["credit"] >= CONFIG["COUT_REVIVE"]
        ):
            await TBOTBDD.revive_survivant(id_twitch)
            await tbot_com.message(
                "revive_survivant",
                channel=channel,
                name=name,
                credit=str(CONFIG["COUT_REVIVE"]),
            )

    async def creer_raid(self, ctx: commands.Context, type_raid: str):
        """Test la validité de la demande pour creer un raid
        Args:
            ctx (commands.Context): environnement twitchIO
                                    pour récupérer les informations
            type_raid (str): nom du raid
        """

        survivor = await TBOTBDD.get_stats_survivant(ctx.author.id)
        gain_prestige = self.config_raid_json[
            "raid_" + type_raid
            ][
            "gain_prestige"]

        if survivor is None or survivor["alive"] is False:
            await tbot_com.message(
                "survivant_no_exist",
                channel=ctx.channel,
                name=ctx.author.display_name
            )

        elif survivor["inraid"]:
            await tbot_com.message(
                "raid_deja_en_cours",
                channel=ctx.channel,
                name=ctx.author.display_name
            )

        elif survivor["credit"] < gain_prestige:
            await tbot_com.message(
                "raid_credit_insuffisant",
                channel=ctx.channel,
                name=ctx.author.display_name,
                gain_prestige=str(gain_prestige),
            )

        else:
            """Création du Raid"""
            # recupere le level du joueur en fonction du type de raid

            await TBOTBDD.raid_initialise(survivor, type_raid, gain_prestige)
            await tbot_com.message(
                f"raid_{type_raid}",
                channel=ctx.channel,
                name=ctx.author.display_name,
                credit=str(gain_prestige),
            )

    async def create_support(
        self,
        ctx: commands.Context,
        raider_name: str,
        channel: str,
        support: str,
    ):
        """Test les conditions et realise un suppport specifique
           d'un survivant en raid par un autres survivant.

        Args:
            helper (str): le survivant a l'initiative de la commande
            raider (str): le survivant beneficiaire de la commande

            channel (str): le channel pour envoyer les messages
            support (str): le type de support
        """
        helper = await TBOTBDD.get_stats_survivant(ctx.author.id)
        raider_name = raider_name.lower().replace("@", "").strip()
        raider_id = await TBOTBDD.get_id_survivant(raider_name.lower())

        while "tant_que_no_error":
            if helper is None or helper["alive"] is False:
                await tbot_com.message(
                    key="survivant_no_exist",
                    channel=channel,
                    name=helper["name"]
                )
                break

            if helper["inraid"] is True:
                await tbot_com.message(
                    key="survivant_no_support_when_raid",
                    channel=channel,
                    name=helper["name"]
                )
                break

            if raider_id == "":
                await tbot_com.message(
                    key="error_noName", channel=channel, name=helper["name"]
                )
                break

            raider = await TBOTBDD.stat_raid(raider_id)

            if raider is None:
                await tbot_com.message(
                    key="error_noRaid", channel=channel, name=helper["name"]
                )
                break

            if raider["time_renfort"] >= CONFIG["MAX_TIME_RENFORT"]:
                await tbot_com.message(
                    key="error_raid_timeOut",
                    channel=channel,
                    name=helper["name"],
                    name2=raider["name"],
                )
                break
            type_raid = "raid_"+raider["type"]
            cout_support = (
                self.config_raid_json[type_raid]["gain_prestige"]//4
            )

            if helper["credit"] < cout_support:
                await tbot_com.message(
                    key="survivant_credit_insuffisant_support",
                    channel=channel,
                    name=helper["name"],
                    name2=raider["name"],
                    credit=str(cout_support),
                )
                break
            equipe = raider["renfort"]
            liste = equipe.split(",")
            if len(liste) >= 3:
                await tbot_com.message(
                    key="error_raid_MaxSurvivor",
                    channel=channel,
                    name=helper["name"],
                    name2=raider["name"],
                )
                break

            listefinale = []
            for joueur in liste:
                if joueur != "":
                    listefinale.append(joueur)
            listefinale.append(helper["name"])
            await tbot_com.message(
                key="survivant_join_raid",
                channel=channel,
                name=helper["name"],
                name2=raider["name"],
                credit=str(cout_support),
            )

            await TBOTBDD.join_raid(raider, helper, listefinale, cout_support)
            # Gestion influence d un support specifique
            if support == "transport":
                await TBOTBDD.support_revision("transport", raider, helper)
            if support == "weapon":
                await TBOTBDD.support_revision("weapon", raider, helper)
            if support == "armor":
                await TBOTBDD.support_revision("armor", raider, helper)
            if support == "gear":
                await TBOTBDD.support_revision("gear", raider, helper)
            break

    async def upgrade_aptitude(self, ctx: commands.Context, aptitude: str):
        survivant = await TBOTBDD.get_stats_survivant(ctx.author.id)
        level = survivant[f"level_{aptitude}"]
        if level >= 5:
            await tbot_com.message(
                key="survivant_max_aptitude",
                channel=ctx.channel,
                name=ctx.author.display_name,
                aptitude=aptitude,
            )
            return

        if survivant is None or survivant["alive"] is False:
            await tbot_com.message(
                "survivant_no_exist",
                channel=ctx.channel,
                name=ctx.author.display_name
            )
        elif survivant["inraid"] is True:
            await tbot_com.message(
                "raid_deja_en_cours",
                channel=ctx.channel,
                name=ctx.author.display_name
            )
        else:
            prestige = survivant["prestige"]
            tarif = CONFIG["TARIF_UPGRADE"]

            if tarif[level] <= prestige:
                await TBOTBDD.upgrade_aptitude(
                    ctx.author.id,
                    aptitude,
                    tarif[level]
                    )

                await tbot_com.message(
                    key="survivant_upgrade_aptitude",
                    channel=ctx.channel,
                    name=ctx.author.display_name,
                    aptitude=aptitude,
                    tarif_level=str(tarif[level]),
                )
            else:
                await tbot_com.message(
                    key="survivant_prestige_insuffisant",
                    channel=ctx.channel,
                    name=ctx.author.display_name,
                    aptitude=aptitude,
                    tarif_level=str(tarif[level]),
                )

    async def armaggedon_time(self, ctx: commands.Context):
        await tbot_com.message(key="armaggedon", channel=ctx.channel)
        await TBOTBDD.kill_them_all(ctx.channel)

    async def message_radio(self, ctx: commands.Context):
        message = ctx.message.content
        message = message.replace("!radio", "")

        survivor = await TBOTBDD.get_stats_survivant(ctx.author.id)

        while "tant_que_no_error":
            if survivor is None or survivor["alive"] is False:
                await tbot_com.message(
                    key="survivant_no_exist",
                    channel=ctx.channel,
                    name=ctx.author.display_name,
                )
                break

            if survivor["credit"] < CONFIG["COUT_MSG_RADIO"]:
                await tbot_com.message(
                    key="survivant_credit_insuffisant_radio",
                    channel=ctx.channel,
                    name=ctx.author.display_name,
                    credit=str(CONFIG["COUT_MSG_RADIO"]),
                )
                break
            await TBOTBDD.withdraw_credit(ctx.author.id,
                                          CONFIG["COUT_MSG_RADIO"])
            await tbot_com.message(
                channel=ctx.channel,
                mod=f"<radio {ctx.author.display_name}> : {message}",
                ovl=f"⚡&ltradio <span class='pseudo'>{ctx.author.display_name}\
                    </span> > : {message} (- {CONFIG['COUT_MSG_RADIO']} \
                    crédits)",
                sound="",
            )

            break

    @commands.command()
    async def create_survivor(self, ctx: commands.Context):
        """
        Commande !create_survivor
        -----------
        Traite la commande twitch !create_survivor.
        """
        await self.creation_survivant(ctx)

    @commands.command()
    async def radio(self, ctx: commands.Context):
        """
        Commande !radio <message>
        -----------
        Traite la commande twitch !radio. Envois in game le message passé
        en parametre avec un son radio
        """

        if self.BASE_READY:
            await self.message_radio(ctx)

    @commands.command()
    async def my_survivor(self, ctx: commands.Context):
        """
        Commande !my_survivor
        -----------
        Traite la commande twitch !my_survivor. retourne les stats
        du joueurs dans le chat Twitch
        """
        name = ctx.author.display_name
        channel = ctx.channel
        test_survivant_exist = await TBOTBDD.get_stats_survivant(ctx.author.id)
        if test_survivant_exist is not None:
            dictStat, score = await TBOTBDD.Get_CurScore(ctx.author.id)
            if score is None:
                score = 0
            dead = ""
            if not dictStat["alive"]:
                dead = "(☠️)"
            message = (f"{dead} " + "{name}" +
                       f" {dead}" +
                       "> 💰:{credit}   🌿{name2} ")
            message += f"<p>🪓: {dictStat['level_weapon']} | \
                🛡️: {dictStat['level_armor']} | \
                🚙 : {dictStat['level_transport']} | \
                🛠️ : {dictStat['level_gear']}</p>"
            message += f"<p>score : <span style='color:rgb(230, 138, 0);'>\
                {str(score)} pts.</span></p>"
            stat_Raid = await TBOTBDD.stat_raid(ctx.author.id)
            if stat_Raid is not None:
                message += f"<p>statut Raid : \
                    <span style='color:rgb(230, 138, 0);'>\
                    {stat_Raid['type']}</span></p>"
                equipe = stat_Raid["renfort"]
                if equipe != "":
                    message += f'<p>support : \
                        <span style="color:rgb(230, 138, 0);">\
                        {equipe}</span></p>'
                else:
                    message += '<p>support : \
                        <span style="color:rgb(230, 138, 0);">\
                        none</span></p>'
            if dictStat["support_raid"] != "":
                message += f"<p>support RAID : \
                    <span style='color:rgb(230, 138, 0);'>\
                    {dictStat['support_raid']}</span></p>"
            await tbot_com.message(
                channel=channel,
                ovl=message,
                name=name,
                name2=str(test_survivant_exist["prestige"]),
                credit=str(test_survivant_exist["credit"]),
            )
        else:
            await tbot_com.message(key="survivant_no_exist",
                                   channel=channel,
                                   name=name)

    @commands.command()
    async def raid_weapon(self, ctx: commands.Context):
        """
        Commande !raid_weapon
        -----------
        Traite la commande twitch !raid_weapons
        """
        if self.BASE_READY:
            await self.creer_raid(ctx, "weapon")
        else:
            await tbot_com.message(
                key="error_no_base", channel=ctx.channel, name=CLIENT["NICK"]
            )

    @commands.command()
    async def raid_tool(self, ctx: commands.Context):
        """
        Commande !raid_tool
        -----------
        Traite la commande twitch !raid_outil.
        """
        if self.BASE_READY:
            await self.creer_raid(ctx, "tool")
        else:
            await tbot_com.message(
                key="error_no_base", channel=ctx.channel, name=CLIENT["NICK"]
            )

    @commands.command()
    async def raid_medic(self, ctx: commands.Context):
        """
        Commande !raid_medic
        -----------
        Traite la commande twitch !raid_medic.
        """
        if self.BASE_READY:
            await self.creer_raid(ctx, "medic")
        else:
            await tbot_com.message(
                key="error_no_base", channel=ctx.channel, name=CLIENT["NICK"]
            )

    @commands.command()
    async def raid_food(self, ctx: commands.Context):
        """
        Commande !raid_nourriture
        -----------
        Traite la commande twitch !raid_food.
        """
        if self.BASE_READY:
            await self.creer_raid(ctx, "food")
        else:
            await tbot_com.message(
                key="error_no_base", channel=ctx.channel, name=CLIENT["NICK"]
            )

    @commands.command()
    async def raid_car(self, ctx: commands.Context):
        """
        Commande !raid_car
        -----------
        Traite la commande twitch !raid_car.
        """
        if self.BASE_READY:
            await self.creer_raid(ctx, "car")
        else:
            await tbot_com.message(
                key="error_no_base", channel=ctx.channel, name=CLIENT["NICK"]
            )

    @commands.command()
    async def raid_alcohol(self, ctx: commands.Context):
        """
        Commande !raid_alcohol
        -----------
        Traite la commande twitch !raid_alcohol.
        """
        if self.BASE_READY:
            await self.creer_raid(ctx, "alcohol")
        else:
            await tbot_com.message(
                key="error_no_base", channel=ctx.channel, name=CLIENT["NICK"]
            )

    @commands.command()
    async def raid_agriculture(self, ctx: commands.Context):
        """
        Commande !raid_agriculture
        -----------
        Traite la commande twitch !raid_agriculture.
        """
        if self.BASE_READY:
            await self.creer_raid(ctx, "agriculture")
        else:
            await tbot_com.message(
                key="error_no_base", channel=ctx.channel, name=CLIENT["NICK"]
            )

    @commands.command()
    async def upgrade_weapon(self, ctx: commands.Context):
        """
        Commande !upgrade_weapon
        -----------
        Traite la commande twitch !upgrade_weapon.
        """
        if self.BASE_READY:
            await self.upgrade_aptitude(ctx, "weapon")
        else:
            await tbot_com.message(
                key="error_no_base", channel=ctx.channel, name=CLIENT["NICK"]
            )

    @commands.command()
    async def upgrade_armor(self, ctx: commands.Context):
        """
        Commande !upgrade_armor
        -----------
        Traite la commande twitch !upgrade_armor.
        """
        if self.BASE_READY:
            await self.upgrade_aptitude(ctx, "armor")
        else:
            await tbot_com.message(
                key="error_no_base", channel=ctx.channel, name=CLIENT["NICK"]
            )

    @commands.command()
    async def upgrade_transport(self, ctx: commands.Context):
        """
        Commande !upgrade_transport
        -----------
        Traite la commande twitch !upgrade_transport.
        """
        if self.BASE_READY:
            await self.upgrade_aptitude(ctx, "transport")
        else:
            await tbot_com.message(
                key="error_no_base", channel=ctx.channel, name=CLIENT["NICK"]
            )

    @commands.command()
    async def upgrade_gear(self, ctx: commands.Context):
        """
        Commande !upgrade_gear
        -----------
        Traite la commande twitch !upgrade_gear.
        """
        if self.BASE_READY:
            await self.upgrade_aptitude(ctx, "gear")
        else:
            await tbot_com.message(
                key="error_no_base", channel=ctx.channel, name=CLIENT["NICK"]
            )

    @commands.command()
    async def add_credits(self, ctx: commands.Context):
        """
        Commande !ajout_credits
        -----------
        Traite la commande twitch !ajout_credit.
        """
        if CONFIG["DEBUG"]:
            await self.ajout_credit(
                ctx.author.id,
                ctx.author.display_name,
                ctx.channel,
                credit=CONFIG["AJOUT_CREDIT"],
            )

    @commands.command()
    async def visi_on(self, ctx: commands.Context):
        """
        Commande !visi_on
        -----------
        Traite la commande twitch !visi_on.
        """

        survivant_stats = await TBOTBDD.get_stats_survivant(ctx.author.id)
        if survivant_stats is None:
            await tbot_com.message(
                key="survivant_no_exist",
                channel=ctx.channel,
                name=ctx.author.display_name,
            )
        else:
            if survivant_stats["support_raid"] != "":
                await TBOTBDD.add_visi(
                    await TBOTBDD.get_id_survivant(
                        survivant_stats["support_raid"])
                )
            else:
                await TBOTBDD.add_visi(ctx.author.id)

    @commands.command()
    async def help_transport(self, ctx: commands.Context):
        """
        Commande !help_transport
        -----------
        Traite la commande twitch !help_transport.
        """
        channel = ctx.channel
        raider = ctx.message.content.replace("!help_transport", "").strip()
        if self.BASE_READY:
            await self.create_support(ctx, raider, channel, "transport")
        else:
            await tbot_com.message(
                key="error_no_base", channel=ctx.channel, name=CLIENT["NICK"]
            )

    @commands.command()
    async def help_weapon(self, ctx: commands.Context):
        """
        Commande !help_weapon
        -----------
        Traite la commande twitch !help_weapon.
        """
        channel = ctx.channel
        raider = ctx.message.content.replace("!help_weapon", "").strip()
        if self.BASE_READY:
            await self.create_support(ctx, raider, channel, "weapon")
        else:
            await tbot_com.message(
                key="error_no_base", channel=ctx.channel, name=CLIENT["NICK"]
            )

    @commands.command()
    async def help_gear(self, ctx: commands.Context):
        """
        Commande !help_gear
        -----------
        Traite la commande twitch !help_gear.
        """
        channel = ctx.channel
        raider = ctx.message.content.replace("!help_gear", "").strip()
        if self.BASE_READY:
            await self.create_support(ctx, raider, channel, "gear")
        else:
            await tbot_com.message(
                key="error_no_base", channel=ctx.channel, name=CLIENT["NICK"]
            )

    @commands.command()
    async def help_armor(self, ctx: commands.Context):
        """
        Commande !help_armor
        -----------
        Traite la commande twitch !help_armor.
        """
        channel = ctx.channel
        raider = ctx.message.content.replace("!help_armor", "").strip()
        if self.BASE_READY:
            await self.create_support(ctx, raider, channel, "armor")

    @commands.command()
    async def armageddon(self, ctx: commands.Context):
        """
        Commande !help_armageddon
        -----------
        Traite la commande twitch !help_armageddon.
        """
        name = ctx.author.display_name
        if name.lower() == CLIENT["USERNAME"].lower():
            await self.armaggedon_time(ctx)

    @commands.command()
    async def top_score(self, ctx: commands.Context):
        """
        Commande !top_score
        -----------
        Traite la commande twitch !top_score.
        """
        test_survivant_exist = await TBOTBDD.get_stats_survivant(ctx.author.id)
        if test_survivant_exist is not None:
            TopScore = await TBOTBDD.Get_TopScore()
            message = "<p>   🏆 HALL OF FAMES 🏆  </p>"
            if TopScore is not None:
                for i in range(len(TopScore)):
                    classement = str(i + 1)
                    if i + 1 == 1:
                        classement = "🥇"
                    if i + 1 == 2:
                        classement = "🥈"
                    if i + 1 == 3:
                        classement = "🥉"
                    message += f'<p>{classement} : \
                        <span style="color:rgb(230, 138, 0);">\
                        {TopScore[i][2]}</span> - <span style="color:rgb(230,\
                        138, 0);">{TopScore[i][3]}</span> Pts</p>'

            else:
                message += "<p>none</p>"
            await tbot_com.message(channel=ctx.channel, ovl=message)

    @commands.command()
    async def init_score(self, ctx: commands.Context):
        """
        Commande !init_score
        -----------
        Traite la commande twitch !init_score.
        """
        name = ctx.author.display_name
        if name.lower() == CLIENT["USERNAME"].lower():
            await TBOTBDD.init_score()

    @commands.command()
    async def base_on(self, ctx: commands.Context):
        """
        Commande !base_on
        -----------
        Traite la commande twitch !base_on.
        """
        name = ctx.author.display_name

        if name.lower() == CLIENT["USERNAME"].lower():
            self.BASE_READY = True
            await tbot_com.message(
                key="base_in_place", channel=ctx.channel, name=CLIENT["NICK"]
            )

    @commands.command()
    async def base_off(self, ctx: commands.Context):
        """
        Commande !base_off
        -----------
        Traite la commande twitch !base_off.
        """
        name = ctx.author.display_name

        if name.lower() == CLIENT["USERNAME"].lower():
            self.BASE_READY = False
            await tbot_com.message(
                key="error_no_base", channel=ctx.channel, name=CLIENT["NICK"]
            )

    @commands.command()
    async def my_raid(self, ctx: commands.Context):
        """
        Commande !my_raid
        -----------
        Traite la commande twitch !my_raid
        """
        survivant_stats = await TBOTBDD.get_stats_survivant(ctx.author.id)
        if survivant_stats is None:
            await tbot_com.message(
                key="survivant_no_exist",
                channel=ctx.channel,
                name=ctx.author.display_name,
            )
        elif survivant_stats["inraid"] is False:
            await tbot_com.message(
                key="error_raid_NoExist",
                channel=ctx.channel,
                name=ctx.author.display_name,
            )
        raid_stats = await TBOTBDD.stat_raid(ctx.author.id)
        #todo: Finir de gerer la commande !my_raid
        if raid_stats is None:
            print("pas de raid a ton nom")


if __name__ == "__main__":
    print("Ne peut etre lancé directement")
