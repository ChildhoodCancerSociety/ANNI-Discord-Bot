#Local imports
import utils.helpers as helpers

#Discord imports
import discord
from discord.ext import commands

#Time imports
import datetime
from datetime import timezone


class time(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="link", description="save, remove, view links")
	async def link(self, ctx):
		stripped = ctx.message.content.replace("[","").replace("]","")
		tokens = stripped.split()
		data = str()

		#flag variables
		remove = bool(False)
		save = bool(False)
		all = bool(False)
		
		#set flag variables for save or remove
		if len(tokens) >= 2:
			if tokens[1] == "remove" or tokens[1] == "rm":
				remove = True
			if tokens[1] == "save" or tokens[1] == "make":
				save = True
			if tokens[1] == "all" or tokens[1] == "show" or tokens[1] == "list":
				all = True
		else:
			all = True


		#Logic for saving a link
		if save == True:
			if len(tokens) == 4:
				try:
					linkLog = helpers.loadCache("Links", "log.yaml")
				except:
					linkLog = dict()
				
				linkLog[tokens[2]] = tokens[3]
				try:
					helpers.saveCache("Links", "log.yaml", linkLog)
					data = "Done!"
					await ctx.send(data)
					return
				except:
					print("Error, Unable to save links [time::savelink]")
					data = "Sorry, I was not able to save this link."
					await ctx.send(data)
					return
			else:
				await ctx.send("I could not interpret your command. Use '!how' for help.\nCommand example: !savelink [name] [link]")
				return
			
		#Logic to show all links
		elif all == True:
			try:
				linkLog = helpers.loadCache("Links", "log.yaml")
				data = "**Links: **\n"
				for key in list(linkLog.keys()):
					data = data + "- " + key + " : " + linkLog[key] + "\n"

				data = data + "\n**Save new link:** !link save [name] [URL]\n"
				data = data + "**Remove saved link:** !link remove [name]\n"
				await ctx.send(data)
				return
			except Exception as e:
				print("Error, unable to load cache file [time::link]\n Exception: " + e)
				data = "Sorry, I was unable to retrieve the links."
				await ctx.send(data)
				return
			
		elif remove == True:
			if len(tokens) == 3:
				try:
					linkLog = helpers.loadCache("Links", "log.yaml")
				except Exception as e:
					print("Error: Unable to read links [time::link]\n Exception: " + e)
					await ctx.send("No need to delete. There are no links saved.")
					return

				if tokens[2] in list(linkLog.keys()):
					del linkLog[tokens[2]]
					try:
						helpers.saveCache("Links", "log.yaml", linkLog)
						data = str(tokens[2]) + " has been deleted."
						await ctx.send(data)
						return
					except Exception as e:
						print("Error, unable to save cache file [time::link]\n Exception: " + e)
						await ctx.send("I was unable to delete that link.")
						return
				else:
					data = "Sorry, I do not have a link associated with " + tokens[2]
					await ctx.send(data)
					return
			else:
				data = "Sorry, I was unable to interpret your command. Use the '!how' command for help."
				await ctx.send(data)
				return
		else:
			await ctx.send("It was not specified to save or remove this alias. Use the '!how' command for help.")
			return
	
	@commands.command(name="al", description="alias to alert command")
	async def al(self, ctx):
		await self.alert(ctx)
		
	@commands.command(name="alert", description="creates an alert")
	async def alert(self, ctx):
		syntaxError = bool(False)
		gotTime = bool() #flag used to denote the finding of a time value
		role = str("everyone")
		tokens = list() #command when separated by spaces
		data = str() #message that will be sent as response to command
		hour = int(0)
		minute = int(0)
		minOP = bool(False) #makes single value time minutes
		hourOP = bool(False) #makes single value time hours
		singleTimeValue = int() #stores time value if it is in the short format
		#alert messages
		meeting = bool(False) #sets message type to meeting (Default)
		delay = bool(True) #sets message type to delayed meeting
		linkLog = helpers.loadCache("Links", "log.yaml")
		link = str()
		gotLink = bool(False)
		
		
		stripped = ctx.message.content.replace("[","").replace("]","")
		tokens = stripped.split()
		#parse tokens, setting flags or values declared above
		if len(tokens) > 1:
			for idx, token in enumerate(tokens):
				for key in list(linkLog.keys()):
					if str(key).lower() == token:
						gotLink = True
						link = linkLog[key]
				if "min" in token.lower() or token.lower() == "m":
					minOP = True
						
				if "hour" in token.lower() or token.lower() == "h":
					hourOP = True
				
				if token.isdigit() == True and gotTime == False:
					singleTimeValue = int(token)
					gotTime = True
				
				if "meet" in token.lower() or "meeting" in token.lower():
					delay = False
					meeting = True
				
				if "$" in token:
					role = token.replace("$", "")
		else:
			data = "Sorry, I could not fullfill your command. Use the '!how' command for help."
			await ctx.send(data)
			return
		
		#Generate current time object
		now = datetime.datetime.now()
		
		if gotTime == True:
			if hourOP == True:
				hour = singleTimeValue
				future = now + datetime.timedelta(hours=hour)
			elif minOP == True:
				minute = singleTimeValue
				future = now + datetime.timedelta(minutes=minute)	
			else:
				data = "Sorry, I could not identify the time given.\nUse '!how' for help.\n"
				data = data + "Command example: !alert minute 5"
				await ctx.send(data)
				return
		
			#Generate discord timestamp useing new timedelta created above
			unix_timestamp = int(future.timestamp())
			discord_timestamp = f"<t:{unix_timestamp}:f>"
		
			#Construct data message for meeting mode
			#Meeting message is used in else clause because it is the default case
			if delay == True and meeting != True:
				data = data + "@" + role + " There has been a technical delay, our meeting will be starting at "
			else:
				data = data + "@" + role + " Meeting will be starting at "	
		
			#Add timestamp to data message
			data = data + discord_timestamp
		elif gotLink == True:
			data = data + f"@{role} Our meeting is starting! Join [here]({link})."
		else:
			await ctx.send("Sorry I was unable to interpret your command. Please use the '!how' command for help.")
			return

		#check for syntax errors before sending message
		if syntaxError == False:
			await ctx.send(data)
		elif syntaxError == True:
			await ctx.send("Improper syntax, command example: !alert min 5\nEnter !h for more help.")
		else:
			await ctx.send("I was unable to find a specified time or syntax is incorrect,\nCommand example: !alert min 5\nEnter '!how' for help.")


async def setup(bot):
	await bot.add_cog(time(bot))


