import os
from bson import ObjectId
from common.auth import authenticated
from common.handlers import BaseHandler
from common.schema import CreateStoryRequest, UpdateStoryRequest
from common.speech import textToSpeech


class StoriesHandler(BaseHandler):
    @authenticated
    async def get(self):
        # TODO: Adding cursor based paging support
        stories = self.db.stories.find({'userID': self.current_user})
        stories = await stories.to_list(10)

        for story in stories:
            story['_id'] = str(story['_id'])
            story['userID'] = str(story['userID'])

        self.write({
            'stories': stories,
        })

        return

    @authenticated
    async def post(self):
        data = self.validate(CreateStoryRequest)
        story = await self.db.stories.insert_one({
            'prompt': data.prompt,
            'response': data.response,
            'userID': self.current_user,
        })
        story_id = str(story.inserted_id)

        self.set_status(201)
        self.write({
            '_id': story_id
        })

        return


class StoryHandler(BaseHandler):
    async def get(self, story_id: str):
        story_id = ObjectId(story_id)

        story = await self.db.stories.find_one({
            '_id': story_id,
            'userID': self.current_user,
        })
        story['_id'] = str(story['_id'])
        story['userID'] = str(story['userID'])

        self.write(story)

        return

    async def put(self, story_id):
        story_id = ObjectId(story_id)
        data = self.validate(UpdateStoryRequest)

        await self.db.stories.update_one(
            {
                '_id': story_id,
                'userID': self.current_user,
            },
            {
                '$set': {
                    'response': data.response,
                },
            }
        )

        self.write({
            '_id': str(story_id)
        })

        return


class ListenStoryHandler(BaseHandler):
    async def get(self, story_id: str):
        audio_path = f'data/stories_audio/{story_id}.mp3'

        story_id = ObjectId(story_id)

        if not os.path.exists(audio_path):
            story = await self.db.stories.find_one({
                '_id': story_id,
                'userID': self.current_user,
            })
            textToSpeech(
                story['response'],
                'data/reference_voice/example_voice.mp3',
                audio_path
            )

        self.set_header('Content-type', 'audio/mpeg')
        self.write(open(audio_path, 'rb').read())

        return
