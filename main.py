from interactions import Client, listen, slash_command, slash_option, OptionType, SlashContext, File
#print (interactions.__api_version__)
import os, asyncio
import requests, json
from io import BytesIO

bot = Client()
# Intents.MESSAGE_CONTENT = True
api_url = "https://cad.onshape.com/api/documents/58d051743d98a90f86e9e2ab"

api_url = "https://cad.onshape.com/api/documents/0eb28bc5213c7ee827495fda"

api_url = "https://cad.onshape.com/api/documents/"

search_by_name_url = "https://cad.onshape.com/api/v6/documents?q={keyword}&filter=9&owner=5d2a6dada58cf91515292c87&ownerType=1&sortColumn=createdAt&sortOrder=desc&offset=0&limit=10"

params = {}
api_keys = (os.environ['ONSHAPE_ACCESS_KEY'], os.environ['ONSHAPE_SECRET_KEY'])
headers = {
  'Accept': 'application/json;charset=UTF-8; qs=0.09',
  'Content-Type': 'application/json'
}


@listen()
async def on_startup():
  print("Bot is ready!")
  # response = requests.get(api_url,
  #                         params=params,
  #                         auth=api_keys,
  #                         headers=headers)
  # print(json.dumps(response.json()["thumbnail"]["sizes"], indent=4))
  # text = json.dumps(response.json()["name"], indent=4)
  # print(f"onshape response received: {text}")


@listen()
async def on_message_create(event):
  # This event is called when a message is sent in a channel the bot can see
  print(f"message received: {event.message.content}")


@slash_command(name="my_command", description="My first command :)")
async def my_command_function(ctx: SlashContext):

  await ctx.send("Hello World")

@slash_command(name="search_onshape", description="Search FTC Lib by keyword")
@slash_option(
  name="keyword",
  description="Keyword",
  required=True,
  opt_type=OptionType.STRING,
  # min_length=5,
  max_length=30)
async def searchOnshape(ctx: SlashContext, keyword: str):
  api_url = search_by_name_url.format(keyword=keyword)
  print("api_url: " + api_url)
  response = requests.get(api_url,
                          params=params,
                          auth=api_keys,
                          headers=headers)
  print(json.dumps(response.json(), indent=4))
  name = json.dumps(response.json()["items"][0]["name"], indent=4)
  description = json.dumps(response.json()["items"][0]["description"], indent=4)
  image_url = json.dumps(response.json()["items"][0]["thumbnail"]["sizes"][3]["href"],
                         indent=4)
  print("image url: " + image_url)
  img_data = requests.get(image_url.strip('"'), auth=api_keys).content
  img_bytes = BytesIO(img_data)  #.getvalue
  await ctx.send(description, file=File(img_bytes, 'cool_image.png'))
  
@slash_command(name="send_image", description="Post an image from url")
@slash_option(
  name="document_id",
  description="Document ID",
  required=True,
  opt_type=OptionType.STRING,
  # min_length=5,
  max_length=30)
async def sendImage(ctx: SlashContext, document_id: str):
  response = requests.get(api_url + document_id,
                          params=params,
                          auth=api_keys,
                          headers=headers)
  name = json.dumps(response.json()["name"], indent=4)
  image_url = json.dumps(response.json()["thumbnail"]["sizes"][3]["href"],
                         indent=4)
  print("image url: " + image_url)
  print(f"You input {document_id}")
  img_data = requests.get(image_url.strip('"'), auth=api_keys).content
  img_bytes = BytesIO(img_data)  #.getvalue

  # open("file_name.png", 'wb').write(img_data)
  await ctx.send(text=name, file=File(img_bytes, 'cool_image.png'))
  # await ctx.send(file="file_name.png")


@slash_command(name="my_long_command", description="My second command :)")
async def my_long_command_function(ctx: SlashContext):
  # need to defer it, otherwise, it fails
  await ctx.defer()

  # do stuff for a bit
  await asyncio.sleep(10)

  await ctx.send("Hello World")


bot.start(os.environ['DISCORD_BOT_SECRET'])
