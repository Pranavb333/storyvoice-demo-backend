Feature Improvements

- Text to Speech
  If this became an actual feature, I don't think we should allow users to generate an audiobook until the stories are finalized. Generating voice from text is time-consuimg and resource intense, so it does not make sense to keep doing it again and again while the stories are still being edited.

  The ideal flow would look something like this -> user creates final book preview -> checks create audiobook option if he wants it -> uploads a voice sample -> hears a quick sample of generated audio -> if he is happy, an audio book is crated for all stories, else upload a better voice sample and try again or cancel if he does not think the generated audio is good enough

- Speech to Text
  I digged down into your old FAQs and ProductHunt history and found that you guys did offer speech to text transcription before (not sure if it is still offered) using actual humans for transcription. I think the ML models have gotten good enough now to do this on their own. In the demo I used whisper's tiny variant because I did not have enough RAM and it did pretty good even if it had some tiny errors. However I tried the base and small models too and they were nearly perfect.

  I think the current flow is good becuase it works like this -> user uploads audio -> user gets text -> he checks the preview and makes edits for any mistakes (this is really important) that the model made -> saves the edited version

  The only problem with the current flow would be with audio files that are 10 mins+. The speech to text model will take at least a few mintues to generate the text and the UX needs to be better than just showing a loading button for 3 mins.

  This would work pretty well for email based flows -> user replied with audio files attachment to the story prompt email -> acknowledgement email that the audio is being transcribed and will be available soon -> email the transcribed text -> user clicks on edit link to go into the in-app editor or copy pastes the text, makes changes and replies again to the email.

  Another related feature is to implement live transcription (whisper does not directly support live stream, but there are some hacks to use it to get a near-real time experience or just use an external model like AssemblyAI) where the users speaks from his microphone and see the text directly transcribed in real-time.

Technical Improvements

- Volumes
  If I had more time and more importantly right servers, I would do a more better arrangement for storing audio files of stories and the reference voices used to generate them. I would use a S3 Bucket or volumes of some kind to ensure that my audio files persist.

- Job Queues and Workers
  Job queues and workers are the perfect tool for things like running AI models. I would move the transcription and voice cloing models into workers and use a job queue to process them. I would make changes on the forntend to support this flow too.

- Clean up of frontend components
  I would create reusable components like Buttons that I can re-use in multiple places instead of building the same thing from scartch with the same styles all the time. There are also some more refactors that I could do to the tailwind styles and the components in it to make it more clear, clean and concise.
