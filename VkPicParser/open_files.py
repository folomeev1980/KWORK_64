import vk
token="09b3f2d8a8a8d91867641be4a56d4986716ddd587d86ddf7670291606f36e72093f7e1b0e5a6b9605a8fb"
owner_id=187613558
session = vk.AuthSession(access_token=token)
vk_api = vk.API(session)
# posts = vk_api.wall.get(owner_id=owner_id * (-1),
#                         count=1000, filter="postponed", v=5.101)


vk_api.wall.edit(post_id=1, message='hello world', v=5.103)