import json
import discord
from discord.ext import commands
import datetime
import time
from discord.ui import Button, View
import asyncio
from PIL import Image


class canvas(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Bot = bot
        tcanvas = json.load(open('canvas.json'))
        self.namesplacement = json.load(open("placenames.json"))
        self.activecanvas = [tuple(incoming) for incoming in tcanvas["colors"]]
        self.now = datetime.datetime.now()
        self.lastupdate = datetime.datetime.now()
        self.ALLCOLORS = {
            "Red": "ff0000",
            "Yellow":"ffff00",
            "Blue":"0000ff",
            "White":"ffffff",
            "Black": "000000",
            "Bright Green": "00ff00",
            "Purple": "ae00ff",
            "Cyan": "00ffee",
            "Orange": "ff8400",
            "Pink": "ff7ab8",
            "Gray": "ababab",
            "Bright Teal": "55f597",
            "Plum": "925b7a",
            "Dark Green": "268c3f"
        }
        self.cooldowns = {}

    @commands.slash_command(name="place", description="place your pixel in the canvas!")
    async def placepix(self, ctx: discord.context, colors: discord.Option(str, choices=["Red", "Yellow", "Blue", "White", "Black", "Dark Green", "Purple", "Cyan", "Orange", "Pink","Gray", "Bright Teal", "Plum", "Bright Green"], description="the available colors to pick"), width_axis: int, height_axis: int):
        # if (ctx.user.id == 240184919827939328):
            if (width_axis > 500 or width_axis < 1) or (height_axis > 500 or height_axis < 1):
                await ctx.respond("invalid placement! it must be in range of 1 - 500 for each axis")
            elif (not self.cooldown(ctx.author.id)):
                await ctx.respond(f"you're in cooldown, you can use <t:{self.cooldowns[ctx.author.id] + 20}:R>", delete_after=5)
            else:
                self.countuseCommand("place")
                width_axis -= 1
                height_axis -= 1
                if (width_axis > 489):
                    width_axis = 489
                if (height_axis > 491):
                    height_axis = 491
                
                vie = self.subview(outer=self, realcaller=ctx.author.id, x=height_axis, y=width_axis, color=colors, username=ctx.author.name, selcol=colors)
                emb = self.getsubareaembed(height_axis, width_axis, cursor=(height_axis*500 + width_axis + (2000 + 5)))
                emb.color = int(self.ALLCOLORS[colors], 16)
                emb.title = f"{ctx.author.name}'s panel\npixel placed by:\n{self.namesplacement[height_axis*500 + width_axis + (2000 + 5)]}"
                await ctx.respond(embed = emb, view = vie)

    @placepix.error
    async def buterr(self, ctx, err):
        print(err)
        await ctx.respond("there has been error in our code and it has been logged to the devs!")


    def actualplace(self, ctx, colors, cursor):
            if (colors == "Red"):
                self.activecanvas[cursor] = (255, 0, 0)
            elif (colors == "Yellow"):
                self.activecanvas[cursor] = (255, 255, 0)
            elif (colors == "Blue"):
                self.activecanvas[cursor] = (0, 0, 255)
            elif (colors == "White"):
                self.activecanvas[cursor] = (255, 255, 255)
            elif (colors == "Black"):
                self.activecanvas[cursor] = (0, 0, 0)
            elif (colors == "Bright Green"):
                self.activecanvas[cursor] = (0, 255, 0)
            elif (colors == "Purple"):
                self.activecanvas[cursor] = (174, 0, 255)
            elif (colors == "Cyan"):
                self.activecanvas[cursor] = (0, 255, 238)
            elif (colors == "Orange"):
                self.activecanvas[cursor] = (255, 132, 0)
            elif (colors == "Pink"):
                self.activecanvas[cursor] = (255, 122, 184)
            elif (colors == "Gray"):
                self.activecanvas[cursor] = (171, 171, 171)
            elif (colors == "Bright Teal"):
                self.activecanvas[cursor] = (85, 245, 151)
            elif (colors == "Plum"):
                self.activecanvas[cursor] = (146, 91, 122)
            elif (colors == "Dark Green"):
                self.activecanvas[cursor] = (38, 140, 63)

            img = Image.new(mode="RGB", size=(500, 500))
            img.putdata(self.activecanvas)
            img.save("C:/Users/faisa/Desktop/botMain/imagemix/canvas.png")
            self.namesplacement[cursor] = ctx.user.name
            self.countplacepix(commandname=ctx.user.name)
            fily = discord.File(filename="results.png",
                                fp="imagemix/canvas.png")
            emb = discord.Embed(title=f"{ctx.user.name}, you placed your pixel!",description=f"you can place pixel again in: <t:{self.cooldowns[ctx.user.id] + 20}:R>")
            emb.set_image(url="attachment://results.png")
            
            return [emb, fily]
    
    
    class subview(View):
        def __init__(self, outer, realcaller, x, y, color, username, selcol):
            self.username = username
            self.selcol = selcol
            self.borderupndown = 0
            self.borderleftnright = 0
            self.cursor = x*500 + y + (2000 + 5)
            self.outer = outer
            self.realcaller = realcaller
            self.x = x
            self.y = y
            self.color = color
            super().__init__()
            self.timeout
            self.b1 = Button(label=" ", emoji="⬅️")
            self.b2 = Button(label=" ", emoji="➡️")
            self.b3 = Button(label=" ", emoji="⬆️")
            self.b4 = Button(label=" ", emoji="⬇️")
            self.b5 = Button(label="Place!", style=discord.ButtonStyle.green)
            self.b6 = Button(label="cancel", style=discord.ButtonStyle.danger)
            self.b7 = Button(label="x3", emoji="⏫")
            self.b8 = Button(label="x3", emoji="⏬")
            self.b9 = Button(label="x3", emoji="➡️")
            self.b10 = Button(label="x3", emoji="⬅️")
            self.b7.callback = self.moveupthree
            self.b8.callback = self.movedownthree
            self.b9.callback = self.moverightthree
            self.b10.callback = self.moveleftthree
            self.b1.callback = self.moveleft
            self.b2.callback = self.moveright
            self.b3.callback = self.moveup
            self.b4.callback = self.movedown
            self.b5.callback = self.confirmation
            self.b6.callback = self.deleting
            self.add_item(self.b1)
            self.add_item(self.b3)
            self.add_item(self.b4)
            self.add_item(self.b2)
            self.add_item(self.b5)
            self.add_item(self.b10)
            self.add_item(self.b7)
            self.add_item(self.b8)
            self.add_item(self.b9)
            self.add_item(self.b6)
        async def deleting(self, ctx: discord.Interaction):
            if self.realcaller == ctx.user.id:
                await ctx.message.delete()

        async def on_timeout(self):
            try:
                await self.message.delete()
            except Exception as e:
                "just ignore"

        async def confirmation(self, ctx: discord.Interaction):
            if self.realcaller == ctx.user.id:
                chnl = self.outer.bot.get_channel(ctx.channel_id)
                self.outer.cooldowns[ctx.user.id] = int(time.time())
                if chnl == ctx.user.dm_channel:
                    user = await self.outer.bot.fetch_user(ctx.user.id)
                    emb = self.outer.actualplace(ctx, self.color, self.cursor)
                    if (self.outer.update()):
                        await user.send("canvas is updating, lag is expected for few seconds", delete_after=5)
                        self.outer.save()
                    self.remove_item(self.b1)
                    self.remove_item(self.b2)
                    self.remove_item(self.b3)
                    self.remove_item(self.b4)
                    self.remove_item(self.b5)
                    try:
                        await ctx.message.delete()
                    except Exception as e:
                        await ctx.message.edit(view = self)
                        self.b6.disabled = True
                        self.b5.disabled = True
                    await user.send(embed=emb[0], file=emb[1], delete_after=20)
                else:
                    emb = self.outer.actualplace(ctx, self.color, self.cursor)
                    if (self.outer.update()):
                        await chnl.send("canvas is updating, lag is expected for few seconds", delete_after=5)  
                        self.outer.save()
                    self.remove_item(self.b1)
                    self.remove_item(self.b2)
                    self.remove_item(self.b3)
                    self.remove_item(self.b4)
                    self.remove_item(self.b5)
                    try:
                        await ctx.message.delete()
                    except Exception as e:
                        self.b6.disabled = True
                        self.b5.disabled = True
                        await ctx.response.edit_message(view = self)
                        "just ignore"
                    await chnl.send(embed=emb[0], file=emb[1], delete_after=20)


        async def moveupthree(self, ctx: discord.Interaction):
            if self.realcaller == ctx.user.id:
                if (self.borderupndown < 2):
                    self.cursor -= 1500
                    self.borderupndown += 3
                emb = self.outer.getsubareaembed(self.x, self.y, self.cursor)
                emb.title = f"{self.username}'s panel\npixel placed by:\n{self.outer.namesplacement[self.cursor]}"
                emb.color = int(self.outer.ALLCOLORS[self.selcol], 16)
                await ctx.response.edit_message(embed = emb)
        
        async def movedownthree(self, ctx: discord.Interaction):
            if self.realcaller == ctx.user.id:
                if (self.borderupndown > -2):
                    self.cursor += 1500
                    self.borderupndown -= 3
                emb = self.outer.getsubareaembed(self.x, self.y, self.cursor)
                emb.title = f"{self.username}'s panel\npixel placed by:\n{self.outer.namesplacement[self.cursor]}"
                emb.color = int(self.outer.ALLCOLORS[self.selcol], 16)
                await ctx.response.edit_message(embed = emb)
        
        async def moverightthree(self, ctx: discord.Interaction):
            if self.realcaller == ctx.user.id:
                if (self.borderleftnright < 3):
                    self.cursor += 3
                    self.borderleftnright += 3
                emb = self.outer.getsubareaembed(self.x, self.y, self.cursor)
                emb.title = f"{self.username}'s panel\npixel placed by:\n{self.outer.namesplacement[self.cursor]}"
                emb.color = int(self.outer.ALLCOLORS[self.selcol], 16)
                await ctx.response.edit_message(embed = emb)
        
        async def moveleftthree(self, ctx: discord.Interaction):
            if self.realcaller == ctx.user.id:
                if (self.borderleftnright > -3):
                    self.cursor -= 3
                    self.borderleftnright -= 3
                emb = self.outer.getsubareaembed(self.x, self.y, self.cursor)
                emb.title = f"{self.username}'s panel\npixel placed by:\n{self.outer.namesplacement[self.cursor]}"
                emb.color = int(self.outer.ALLCOLORS[self.selcol], 16)
                await ctx.response.edit_message(embed = emb)
        
        async def moveup(self, ctx: discord.Interaction):
            if self.realcaller == ctx.user.id:
                if (self.borderupndown < 4):
                    self.cursor -= 500
                    self.borderupndown += 1
                emb = self.outer.getsubareaembed(self.x, self.y, self.cursor)
                emb.title = f"{self.username}'s panel\npixel placed by:\n{self.outer.namesplacement[self.cursor]}"
                emb.color = int(self.outer.ALLCOLORS[self.selcol], 16)
                await ctx.response.edit_message(embed = emb)

        async def moveright(self, ctx):
            if self.realcaller == ctx.user.id:
                if (self.borderleftnright < 5):
                    self.borderleftnright += 1
                    self.cursor += 1
                emb = self.outer.getsubareaembed(self.x, self.y, self.cursor)
                emb.title = f"{self.username}'s panel\npixel placed by:\n{self.outer.namesplacement[self.cursor]}"
                emb.color = int(self.outer.ALLCOLORS[self.selcol], 16)
                await ctx.response.edit_message(embed = emb)

        async def moveleft(self, ctx):
            if self.realcaller == ctx.user.id:
                if (self.borderleftnright > -5):
                    self.cursor -= 1
                    self.borderleftnright -=1
                emb = self.outer.getsubareaembed(self.x, self.y, self.cursor)
                emb.title = f"{self.username}'s panel\npixel placed by:\n{self.outer.namesplacement[self.cursor]}"
                emb.color = int(self.outer.ALLCOLORS[self.selcol], 16)
                await ctx.response.edit_message(embed = emb)

        async def movedown(self, ctx):
            if self.realcaller == ctx.user.id:
                if (self.borderupndown > -4):
                    self.cursor += 500
                    self.borderupndown -= 1
                emb = self.outer.getsubareaembed(self.x, self.y, self.cursor)
                emb.title = f"{self.username}'s panel\npixel placed by:\n{self.outer.namesplacement[self.cursor]}"
                emb.color = int(self.outer.ALLCOLORS[self.selcol], 16)
                await ctx.response.edit_message(embed = emb)
    
    class zoomview(View):
        def __init__(self, x, y, authorid, outer):
            self.outer = outer
            self.realcaller = authorid
            self.x = x
            self.y = y
            super().__init__()
            self.b1 = Button(label= "corner", emoji="↖️", row=0)
            self.b2 = Button(label= "5px", emoji="⬆️", row=0)
            self.b3 = Button(label= "corner", emoji="↗️", row=0)
         
            self.b4 = Button(label= "5px", emoji="⬅️", row=1)
            self.b5 = Button(label= "refresh", row=1)
            self.b6 = Button(label= "5px", emoji="➡️",row=1)
            self.b7 = Button(label= "corner", emoji="↙️",row=2)
            self.b8 = Button(label= "5px", emoji="⬇️",row=2)
            self.b9 = Button(label= "corner", emoji="↘️",row=2)
            self.b1.callback = self.cornertopleft
            self.b2.callback = self.moveup
            self.b3.callback = self.cornertopright
            self.b4.callback = self.moveleft
            self.b5.callback = self.refresh
            
            self.b6.callback = self.moveright
            self.b7.callback = self.cornerbottomleft
            self.b8.callback = self.movedown
            self.b9.callback = self.cornerbottomright      
            self.add_item(self.b1)
            self.add_item(self.b2)
            self.add_item(self.b3)
    
            self.add_item(self.b4)
            self.add_item(self.b5)
            self.add_item(self.b6)
            self.add_item(self.b7)
            self.add_item(self.b8)
            self.add_item(self.b9)
        
        async def closedele(self, ctx):
            if (ctx.user.id == self.realcaller):
                await ctx.message.delete()

        async def on_timeout(self):
            await self.message.delete()

        async def cornertopleft(self, ctx):
            if (ctx.user.id == self.realcaller):
                self.y = 0
                self.x = 0
                emb = self.outer.zoomedembed(self.x, self.y)
                emb.title = f"coordinates of center is:({self.x + 6} height, {self.y + 7} width)\nplaced by:\n{self.outer.namesplacement[self.x * 500 + self.y + 2000 + 5]}"
                await ctx.response.edit_message(embed = emb)

        
        async def cornertopright(self, ctx):
            if (ctx.user.id == self.realcaller):
                self.y = 489
                self.x = 0
                emb = self.outer.zoomedembed(self.x, self.y)
                emb.title = f"coordinates of center is:({self.x + 6} height, {self.y + 7} width)\nplaced by:\n{self.outer.namesplacement[self.x * 500 + self.y+ 2000 + 5]}"
                await ctx.response.edit_message(embed = emb)

        
        async def cornerbottomleft(self, ctx):
            if (ctx.user.id == self.realcaller):
                self.y = 0
                self.x = 491
                emb = self.outer.zoomedembed(self.x, self.y)
                emb.title = f"coordinates of center is:({self.x + 6} height, {self.y + 7} width)\nplaced by:\n{self.outer.namesplacement[self.x * 500 + self.y+ 2000 + 5]}"
                await ctx.response.edit_message(embed = emb)
        
        async def cornerbottomright(self, ctx):
            if (ctx.user.id == self.realcaller):
                self.y = 489
                self.x = 491
                emb = self.outer.zoomedembed(self.x, self.y)
                emb.title = f"coordinates of center is:({self.x + 6} height, {self.y + 7} width)\nplaced by:\n{self.outer.namesplacement[self.x * 500 + self.y+ 2000 + 5]}"
                await ctx.response.edit_message(embed = emb)
        
        async def moveleft(self, ctx):
            if (ctx.user.id == self.realcaller):
                if self.y >= 5:
                    self.y -= 5
                emb = self.outer.zoomedembed(self.x, self.y)
                emb.title = f"coordinates of center is:({self.x + 6} height, {self.y + 7} width)\nplaced by:\n{self.outer.namesplacement[self.x * 500 + self.y+ 2000 + 5]}"
                await ctx.response.edit_message(embed = emb)
        
        async def moveright(self, ctx):
            if (ctx.user.id == self.realcaller):
                if self.y <= 484:
                    self.y += 5
                emb = self.outer.zoomedembed(self.x, self.y)
                emb.title = f"coordinates of center is:({self.x + 6} height, {self.y + 7} width)\nplaced by:\n{self.outer.namesplacement[self.x * 500 + self.y+ 2000 + 5]}"
                await ctx.response.edit_message(embed = emb)
        
        async def moveup(self, ctx):
            if (ctx.user.id == self.realcaller):
                if self.x >= 5:
                    self.x -= 5
                emb = self.outer.zoomedembed(self.x, self.y)
                emb.title = f"coordinates of center is:({self.x + 6} height, {self.y + 7} width)\nplaced by:\n{self.outer.namesplacement[self.x * 500 + self.y+ 2000 + 5]}"
                await ctx.response.edit_message(embed = emb)

        async def movedown(self, ctx):
            if (ctx.user.id == self.realcaller):
                if self.x <= 486:
                    self.x += 5
                emb = self.outer.zoomedembed(self.x, self.y)
                emb.title = f"coordinates of center is:({self.x + 6} height, {self.y + 7} width)\nplaced by:\n{self.outer.namesplacement[self.x * 500 + self.y+ 2000 + 5]}"
                await ctx.response.edit_message(embed = emb)
        
        async def refresh(self, ctx):
            if (ctx.user.id == self.realcaller):
                emb = self.outer.zoomedembed(self.x, self.y)
                emb.title = f"coordinates of center is:({self.x + 6} height, {self.y + 7} width)\nplaced by:\n{self.outer.namesplacement[self.x * 500 + self.y+ 2000 + 5]}"
                await ctx.response.edit_message(embed = emb)

        


    @commands.slash_command(name="placezoom", description="zoom in specific area in emoji mode")
    async def zoomed(self,ctx: discord.context,  width_axis: int ,height_axis: int):
        if (width_axis > 500 or width_axis < 1 or height_axis > 500 or height_axis < 1):
            await ctx.respond("invalid placement! it must be in range of 1 - 500 for each axis")
        else:
            self.countuseCommand("placezoom")
            width_axis -= 1
            height_axis -= 1
            if (width_axis > 489):
                width_axis = 489
            if (height_axis > 491):
                height_axis = 491

            emb = self.zoomedembed(height_axis, width_axis)
            vie = self.zoomview(height_axis, width_axis, ctx.user.id, self)
            emb.title = f"coordinates center: ({height_axis + 6} height, {width_axis + 7} width)\nplaced by:\n{self.namesplacement[height_axis * 500 + width_axis+ 2000 + 5]}"
            await ctx.respond(embed = emb, view=vie)

    def zoomedembed(self, x, y):
        emb = discord.Embed()
        msg = ""
        for i in range(x, x + 9):
            for k in range(i*500 + y, i*500 + y + 11):
                if (self.activecanvas[k] == (255, 255, 255)):
                    msg += ":white_large_square:"
                elif (self.activecanvas[k] == (255, 0, 0)):
                    msg += ":red_square:"
                elif (self.activecanvas[k] == (255, 255, 0)):
                    msg += ":yellow_square:"
                elif (self.activecanvas[k] == (0, 0, 255)):
                    msg += "<:blue:1106905213299855390>"
                elif (self.activecanvas[k] == (0, 255, 238)):
                    msg += ":blue_square:"
                elif (self.activecanvas[k] == (0, 0, 0)):
                    msg += ":black_large_square:"
                elif (self.activecanvas[k] == (0, 255, 0)):
                    msg += ":green_square:"
                elif (self.activecanvas[k] == (255, 132, 0)):
                    msg += ":orange_square:"
                elif (self.activecanvas[k] == (255, 122, 184)):
                    msg += "<:pink:1106905625641885726>"
                elif (self.activecanvas[k] == (174, 0, 255)):
                    msg += ":purple_square:"
                elif (self.activecanvas[k] == (171, 171, 171)):
                    msg += "<:Gray:1106842084142501939>"
                elif (self.activecanvas[k] == (85, 245, 151)):
                    msg += "<:limegreen:1106882161618976859>"
                elif (self.activecanvas[k] == (146, 91, 122)):
                    msg += "<:plum:1106896046312931439>"
                elif (self.activecanvas[k] == (38, 140, 63)):
                    msg += "<:darkgreen:1106901501579903060>"
                
            msg +='\n'
        emb = discord.Embed(description=msg)
        return emb


    
        



    @commands.slash_command(name="placeleaderboard", description="shows the leaderboard in place")
    async def sortnsend(self, ctx):
        with open("placecount.json", 'r+') as file:
            fdata = json.load(file)

        sorted_names = sorted(fdata.items(),key=lambda x:x[1], reverse=True)
        lastindx = 10 if len(sorted_names) > 10 else len(sorted_names)
        emb = discord.Embed(title="Here is global leaderboard!", colour=int("78251d", 16))
        emb.set_footer(text=f"requested by: {ctx.user.name}", icon_url=ctx.user.avatar)
        msg = ""
        for arr in range(lastindx):
            msg += sorted_names[arr][0] + ": " + str(sorted_names[arr][1]) + " pixel placed"
            if arr == 0:
                msg += " :crown:"
            msg += '\n'
        emb.description = msg

        await ctx.respond(embed= emb)


    def getsubareaembed(self, x, y, cursor=0):
     
        msg =""
        for j in range(x, x + 9):
            for k in range((j*500) + y, (j*500) + y + 11):
                if ((k) == cursor):
                    msg += ":star:"
                elif (self.activecanvas[k] == (255, 255, 255)):
                    msg += ":white_large_square:"
                elif (self.activecanvas[k] == (255, 0, 0)):
                    msg += ":red_square:"
                elif (self.activecanvas[k] == (255, 255, 0)):
                    msg += ":yellow_square:"
                elif (self.activecanvas[k] == (0, 0, 255)):
                    msg += "<:blue:1106905213299855390>"
                elif (self.activecanvas[k] == (0, 255, 238)):
                    msg += ":blue_square:"
                elif (self.activecanvas[k] == (0, 0, 0)):
                    msg += ":black_large_square:"
                elif (self.activecanvas[k] == (0, 255, 0)):
                    msg += ":green_square:"
                elif (self.activecanvas[k] == (255, 132, 0)):
                    msg += ":orange_square:"
                elif (self.activecanvas[k] == (255, 122, 184)):
                    msg += "<:pink:1106905625641885726>"
                elif (self.activecanvas[k] == (174, 0, 255)):
                    msg += ":purple_square:"
                elif (self.activecanvas[k] == (171, 171, 171)):
                    msg += "<:Gray:1106842084142501939>"
                elif (self.activecanvas[k] == (85, 245, 151)):
                    msg += "<:limegreen:1106882161618976859>"
                elif (self.activecanvas[k] == (146, 91, 122)):
                    msg += "<:plum:1106896046312931439>"
                elif (self.activecanvas[k] == (38, 140, 63)):
                    msg += "<:darkgreen:1106901501579903060>"
            msg +='\n'
        emb = discord.Embed(description=msg)
        return emb
        


    def countplacepix(self, commandname, filename = "placecount.json"):
        new_data ={}
        with open(filename, 'r+') as file:
            fdata = json.load(file)
        
        if not (commandname in fdata):
            new_data[commandname] = 1
        else:    
            new_data[commandname] = 1 + int(fdata[commandname])

        for key, val in fdata.items():
            if key == commandname:
                continue
            else:
                new_data[key] = val

        with open(filename, "w") as file:
            json.dump(new_data, file, indent=4)


    def countuseCommand(self, commandname, filename = "counting.json"):
        new_data ={}
        with open(filename, 'r+') as file:
            fdata = json.load(file)
        
        if not (commandname in fdata):
            new_data[commandname] = 1
        else:    
            new_data[commandname] = 1 + int(fdata[commandname])

        for key, val in fdata.items():
            if key == commandname:
                continue
            else:
                new_data[key] = val

        with open(filename, "w") as file:
            json.dump(new_data, file, indent=4)

    def update(self):
        self.now = datetime.datetime.now()
        if (self.now - self.lastupdate > datetime.timedelta(minutes=5)):
            self.lastupdate = datetime.datetime.now()
            return True
        else:
            return False

    def save(self):

        print("canvas is being updated: ", datetime.datetime.now())
        t = [list(updated) for updated in self.activecanvas]
        new_data = {"colors": t}
        with open("canvas.json", "w") as file:
            json.dump(new_data, file, indent=4)
        
        with open("placenames.json", "w") as file:
            json.dump(self.namesplacement, file, indent=4)
        print("canvas has been updated")

    def cooldown(self, userid):
        if not (userid in self.cooldowns):
            self.cooldowns[userid] = 0
            return True
        if (int(time.time()) - self.cooldowns[userid] >= 20):
            self.cooldowns[userid] = 0
            return True
        return False
        


def setup(bot):
    bot.add_cog(canvas(bot))
