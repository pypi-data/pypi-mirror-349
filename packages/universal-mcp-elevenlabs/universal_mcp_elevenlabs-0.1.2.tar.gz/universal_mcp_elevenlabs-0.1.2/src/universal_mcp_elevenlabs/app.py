from typing import Any
from universal_mcp.applications import APIApplication
from universal_mcp.integrations import Integration
# Add these imports at the top of your app.py
from loguru import logger
from universal_mcp.exceptions import NotAuthorizedError

class ElevenlabsApp(APIApplication):
    def __init__(self, integration: Integration = None, **kwargs) -> None:
        super().__init__(name='elevenlabs', integration=integration, **kwargs)
        self.base_url = "https://api.elevenlabs.io"

# This method should be added inside the ElevenlabsApp class in your app.py

    def _get_headers(self) -> dict[str, str]:
        """
        Overrides the base _get_headers to provide ElevenLabs-specific authentication.
        """
        if not self.integration:
            logger.warning(f"No integration configured for {self.name}. API calls will likely fail as API key cannot be retrieved.")
            # Returning empty headers will cause the API call to fail with 401, which is appropriate.
            return {}

        try:
            # self.integration is expected to be an ApiKeyIntegration instance.
            # ApiKeyIntegration.get_credentials() calls its 'api_key' property,
            # which retrieves the key from the store (e.g., EnvironmentStore via os.getenv)
            # or raises NotAuthorizedError if the key is missing from the store.
            credentials = self.integration.get_credentials()
        except NotAuthorizedError:
            # Log and re-raise. The actual HTTP request in the base class will then fail,
            # and the original HTTPError (e.g., 401) from ElevenLabs can be handled by the caller.
            logger.error(f"Authorization failed for {self.name}: API key not found or invalid. Ensure ELEVENLABS_API_KEY environment variable is set correctly.")
            raise
        except Exception as e:
            # Catch other potential errors from the integration's get_credentials()
            logger.error(f"Unexpected error fetching credentials for {self.name}: {e}")
            # Treat as an authorization failure for safety.
            raise NotAuthorizedError(f"Unexpected error during credential retrieval for {self.name}: {str(e)}") from e

        # ApiKeyIntegration.get_credentials() returns a dict like {'api_key': 'the_actual_key'}
        api_key_value = credentials.get("api_key")

        if not api_key_value:
            # This state should ideally be prevented by ApiKeyIntegration.api_key raising NotAuthorizedError.
            # However, as a defensive measure:
            logger.error(f"API key was not found in credentials for {self.name} after successful get_credentials call. This is unexpected.")
            raise NotAuthorizedError(f"API key for {self.name} is missing from successfully retrieved credentials. Check integration configuration.")

        logger.debug(f"Using 'xi-api-key' header for {self.name} authentication.")
        # ElevenLabs expects the API key in the 'xi-api-key' header.
        # 'Accept: application/json' is good practice for APIs that return JSON.
        return {
            "xi-api-key": api_key_value,
            "Accept": "application/json"
        }
        
    def get_generated_items(self, page_size=None, voice_id=None) -> dict[str, Any]:
        """
        Retrieves historical data based on specified parameters, including page size and voice ID, using the "GET" method at the "/v1/history" endpoint.

        Args:
            page_size (string): How many history items to return at maximum. Can not exceed 1000, defaults to 100. Example: '1'.
            voice_id (string): Voice ID to be filtered for, you can use GET to receive a list of voices and their IDs. Example: 'pMsXgVXv3BLzUgSXRplE'.

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            History, important
        """
        url = f"{self.base_url}/v1/history"
        query_params = {k: v for k, v in [('page_size', page_size), ('voice_id', voice_id)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_history_item_by_id(self, history_item_id) -> dict[str, Any]:
        """
        Retrieves a specific history item by its identifier using the API defined at "/v1/history/{history_item_id}" with the GET method.

        Args:
            history_item_id (string): history_item_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            History
        """
        if history_item_id is None:
            raise ValueError("Missing required parameter 'history_item_id'")
        url = f"{self.base_url}/v1/history/{history_item_id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_history_item(self, history_item_id) -> dict[str, Any]:
        """
        Deletes a specific history item identified by its ID using the DELETE method.

        Args:
            history_item_id (string): history_item_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            History
        """
        if history_item_id is None:
            raise ValueError("Missing required parameter 'history_item_id'")
        url = f"{self.base_url}/v1/history/{history_item_id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_audio_from_history_item(self, history_item_id) -> Any:
        """
        Retrieves audio data for a specific history item identified by `{history_item_id}` using the `GET` method at the `/v1/history/{history_item_id}/audio` endpoint.

        Args:
            history_item_id (string): history_item_id

        Returns:
            Any: Success

        Tags:
            History
        """
        if history_item_id is None:
            raise ValueError("Missing required parameter 'history_item_id'")
        url = f"{self.base_url}/v1/history/{history_item_id}/audio"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def download_history_items(self, history_item_ids=None) -> Any:
        """
        Initiates a historical data download process and returns a success status upon completion.

        Args:
            history_item_ids (array): history_item_ids
                Example:
                ```json
                {
                  "history_item_ids": [
                    "history_item_ids",
                    "history_item_ids"
                  ]
                }
                ```

        Returns:
            Any: Success / Success

        Tags:
            History
        """
        request_body = {
            'history_item_ids': history_item_ids,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/history/download"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_sample(self, voice_id, sample_id) -> dict[str, Any]:
        """
        Deletes a specific voice sample identified by the `sample_id` from a voice with the given `voice_id` using the DELETE method.

        Args:
            voice_id (string): voice_id
            sample_id (string): sample_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Samples
        """
        if voice_id is None:
            raise ValueError("Missing required parameter 'voice_id'")
        if sample_id is None:
            raise ValueError("Missing required parameter 'sample_id'")
        url = f"{self.base_url}/v1/voices/{voice_id}/samples/{sample_id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_audio_from_sample(self, voice_id, sample_id) -> Any:
        """
        Retrieves the audio file for a specific sample associated with a given voice using the specified voice_id and sample_id.

        Args:
            voice_id (string): voice_id
            sample_id (string): sample_id

        Returns:
            Any: Success

        Tags:
            Samples
        """
        if voice_id is None:
            raise ValueError("Missing required parameter 'voice_id'")
        if sample_id is None:
            raise ValueError("Missing required parameter 'sample_id'")
        url = f"{self.base_url}/v1/voices/{voice_id}/samples/{sample_id}/audio"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def convert(self, voice_id, optimize_streaming_latency=None, output_format=None, text=None, voice_settings=None) -> Any:
        """
        Converts text into speech using a specified voice, allowing for optimization of streaming latency and selection of output format.

        Args:
            voice_id (string): voice_id
            optimize_streaming_latency (string): You can turn on latency optimizations at some cost of quality. The best possible final latency varies by model. Example: '0'.
            output_format (string): The output format of the generated audio. Example: 'mp3_22050_32'.
            text (string): text Example: "It sure does, Jackie… My mama always said: “In Carolina, the air's so thick you can wear it!”".
            voice_settings (object): voice_settings
                Example:
                ```json
                {
                  "text": "It sure does, Jackie\u2026 My mama always said: \u201cIn Carolina, the air's so thick you can wear it!\u201d",
                  "voice_settings": {
                    "similarity_boost": 0.75,
                    "stability": 0.5,
                    "style": 0
                  }
                }
                ```

        Returns:
            Any: Success

        Tags:
            Text To Speech
        """
        if voice_id is None:
            raise ValueError("Missing required parameter 'voice_id'")
        request_body = {
            'text': text,
            'voice_settings': voice_settings,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/text-to-speech/{voice_id}"
        query_params = {k: v for k, v in [('optimize_streaming_latency', optimize_streaming_latency), ('output_format', output_format)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def text_to_speech_with_timestamps(self, voice_id, text=None) -> dict[str, Any]:
        """
        Generates speech from text with precise character or word-level timing information using the specified voice, supporting audio-text synchronization through timestamps.

        Args:
            voice_id (string): voice_id
            text (string): text
                Example:
                ```json
                {
                  "text": "text"
                }
                ```

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Text To Speech
        """
        if voice_id is None:
            raise ValueError("Missing required parameter 'voice_id'")
        request_body = {
            'text': text,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/text-to-speech/{voice_id}/with-timestamps"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def convert_as_stream(self, voice_id, optimize_streaming_latency=None, output_format=None, text=None, voice_settings=None) -> Any:
        """
        Converts text to speech stream using the specified voice ID with configurable latency and output format.

        Args:
            voice_id (string): voice_id
            optimize_streaming_latency (string): You can turn on latency optimizations at some cost of quality. The best possible final latency varies by model. Example: '0'.
            output_format (string): The output format of the generated audio. Example: 'mp3_22050_32'.
            text (string): text Example: "It sure does, Jackie… My mama always said: “In Carolina, the air's so thick you can wear it!”".
            voice_settings (object): voice_settings
                Example:
                ```json
                {
                  "text": "It sure does, Jackie\u2026 My mama always said: \u201cIn Carolina, the air's so thick you can wear it!\u201d",
                  "voice_settings": {
                    "similarity_boost": 0.3,
                    "stability": 0.1,
                    "style": 0.2
                  }
                }
                ```

        Returns:
            Any: Success

        Tags:
            Text To Speech
        """
        if voice_id is None:
            raise ValueError("Missing required parameter 'voice_id'")
        request_body = {
            'text': text,
            'voice_settings': voice_settings,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/text-to-speech/{voice_id}/stream"
        query_params = {k: v for k, v in [('optimize_streaming_latency', optimize_streaming_latency), ('output_format', output_format)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def text_to_speech_streaming_with_timestamps(self, voice_id, text=None) -> Any:
        """
        Converts text to speech using the specified voice ID, streaming the audio output with timestamps.

        Args:
            voice_id (string): voice_id
            text (string): text
                Example:
                ```json
                {
                  "text": "text"
                }
                ```

        Returns:
            Any: Success / Success

        Tags:
            Text To Speech
        """
        if voice_id is None:
            raise ValueError("Missing required parameter 'voice_id'")
        request_body = {
            'text': text,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/text-to-speech/{voice_id}/stream/with-timestamps"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def voice_generation_parameters(self) -> dict[str, Any]:
        """
        Retrieves the parameters required for generating voice using the specified API endpoint.

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Voice Generation
        """
        url = f"{self.base_url}/v1/voice-generation/generate-voice/parameters"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def generate_arandom_voice(self, accent=None, accent_strength=None, age=None, gender=None, text=None) -> Any:
        """
        Generates an audio file by converting text into speech using a specified voice, allowing for customizable voice selection and text input.

        Args:
            accent (string): accent Example: 'american'.
            accent_strength (number): accent_strength Example: '2'.
            age (string): age Example: 'middle_aged'.
            gender (string): gender Example: 'female'.
            text (string): text
                Example:
                ```json
                {
                  "accent": "american",
                  "accent_strength": 2,
                  "age": "middle_aged",
                  "gender": "female",
                  "text": "It sure does, Jackie\u2026 My mama always said: \u201cIn Carolina, the air's so thick you can wear it!\u201d"
                }
                ```

        Returns:
            Any: Success

        Tags:
            Voice Generation
        """
        request_body = {
            'accent': accent,
            'accent_strength': accent_strength,
            'age': age,
            'gender': gender,
            'text': text,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/voice-generation/generate-voice"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_apreviously_generated_voice(self, generated_voice_id=None, voice_description=None, voice_name=None) -> dict[str, Any]:
        """
        Generates a custom voice using the provided parameters via the "/v1/voice-generation/create-voice" endpoint by sending a POST request, allowing users to create unique voice models.

        Args:
            generated_voice_id (string): generated_voice_id Example: 'generated_voice_id'.
            voice_description (string): voice_description Example: 'voice_description'.
            voice_name (string): voice_name
                Example:
                ```json
                {
                  "generated_voice_id": "generated_voice_id",
                  "voice_description": "voice_description",
                  "voice_name": "voice_name"
                }
                ```

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Voice Generation
        """
        request_body = {
            'generated_voice_id': generated_voice_id,
            'voice_description': voice_description,
            'voice_name': voice_name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/voice-generation/create-voice"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def generate_avoice_preview_from_description(self, text=None, voice_description=None) -> dict[str, Any]:
        """
        Generates a voice preview from a given text prompt using the ElevenLabs API.

        Args:
            text (string): text Example: 'text'.
            voice_description (string): voice_description
                Example:
                ```json
                {
                  "text": "text",
                  "voice_description": "voice_description"
                }
                ```

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Text To Voice
        """
        request_body = {
            'text': text,
            'voice_description': voice_description,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/text-to-voice/create-previews"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_anew_voice_from_voice_preview(self, generated_voice_id=None, voice_description=None, voice_name=None) -> dict[str, Any]:
        """
        Creates a new voice entry in the voice library using a generated preview ID and returns voice details.

        Args:
            generated_voice_id (string): generated_voice_id Example: 'generated_voice_id'.
            voice_description (string): voice_description Example: 'voice_description'.
            voice_name (string): voice_name
                Example:
                ```json
                {
                  "generated_voice_id": "generated_voice_id",
                  "voice_description": "voice_description",
                  "voice_name": "voice_name"
                }
                ```

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Text To Voice
        """
        request_body = {
            'generated_voice_id': generated_voice_id,
            'voice_description': voice_description,
            'voice_name': voice_name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/text-to-voice/create-voice-from-preview"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_user_subscription_info(self) -> dict[str, Any]:
        """
        Retrieves the user's subscription details from the API.

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            User
        """
        url = f"{self.base_url}/v1/user/subscription"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_user_info(self) -> dict[str, Any]:
        """
        Retrieves user information from the API.

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            User, important
        """
        url = f"{self.base_url}/v1/user"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_voices(self) -> dict[str, Any]:
        """
        Retrieves a list of voices using the "GET" method at the "/v1/voices" API endpoint.

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            voices, important
        """
        url = f"{self.base_url}/v1/voices"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_default_voice_settings(self) -> dict[str, Any]:
        """
        Retrieves the default voice settings using the "GET" method at the "/v1/voices/settings/default" endpoint.

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            voices
        """
        url = f"{self.base_url}/v1/voices/settings/default"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_voice_settings(self, voice_id) -> dict[str, Any]:
        """
        Retrieves voice settings for a specific voice identified by `{voice_id}` using the "GET" method, returning the current configuration for that voice.

        Args:
            voice_id (string): voice_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            voices
        """
        if voice_id is None:
            raise ValueError("Missing required parameter 'voice_id'")
        url = f"{self.base_url}/v1/voices/{voice_id}/settings"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_voice(self, voice_id) -> dict[str, Any]:
        """
        Retrieves the details of a specific voice by its ID using the "GET" method at the "/v1/voices/{voice_id}" endpoint.

        Args:
            voice_id (string): voice_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            voices
        """
        if voice_id is None:
            raise ValueError("Missing required parameter 'voice_id'")
        url = f"{self.base_url}/v1/voices/{voice_id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_voice(self, voice_id) -> dict[str, Any]:
        """
        Deletes a voice with the specified ID using the DELETE method at the "/v1/voices/{voice_id}" endpoint.

        Args:
            voice_id (string): voice_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            voices
        """
        if voice_id is None:
            raise ValueError("Missing required parameter 'voice_id'")
        url = f"{self.base_url}/v1/voices/{voice_id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_voice(self, name=None) -> dict[str, Any]:
        """
        Adds a new voice entry to the voices collection using the provided data.

        Args:
            name (string): name
                Example:
                ```json
                {
                  "name": "Alex"
                }
                ```

        Returns:
            dict[str, Any]: Success

        Tags:
            voices
        """
        request_body = {
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/voices/add"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def edit_voice(self, voice_id, name=None) -> dict[str, Any]:
        """
        Updates the specified voice by ID using a POST request and returns a success status upon completion.

        Args:
            voice_id (string): voice_id
            name (string): name
                Example:
                ```json
                {
                  "name": "George"
                }
                ```

        Returns:
            dict[str, Any]: Success

        Tags:
            voices
        """
        if voice_id is None:
            raise ValueError("Missing required parameter 'voice_id'")
        request_body = {
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/voices/{voice_id}/edit"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_sharing_voice(self, public_user_id, voice_id, new_name=None) -> dict[str, Any]:
        """
        Adds a voice associated with a public user ID and voice ID using the specified API endpoint.

        Args:
            public_user_id (string): public_user_id
            voice_id (string): voice_id
            new_name (string): new_name
                Example:
                ```json
                {
                  "new_name": "new_name"
                }
                ```

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            voices
        """
        if public_user_id is None:
            raise ValueError("Missing required parameter 'public_user_id'")
        if voice_id is None:
            raise ValueError("Missing required parameter 'voice_id'")
        request_body = {
            'new_name': new_name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/voices/add/{public_user_id}/{voice_id}"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_shared_voices(self, page_size=None, gender=None, language=None) -> dict[str, Any]:
        """
        Retrieves a list of shared voices filtered by parameters like gender and language, with pagination support via page_size.

        Args:
            page_size (string): How many shared voices to return at maximum. Can not exceed 100, defaults to 30. Example: '1'.
            gender (string): gender used for filtering Example: 'female'.
            language (string): language used for filtering Example: 'en'.

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            voices
        """
        url = f"{self.base_url}/v1/shared-voices"
        query_params = {k: v for k, v in [('page_size', page_size), ('gender', gender), ('language', language)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_aprofile_page(self, handle) -> dict[str, Any]:
        """
        Retrieves a unified customer profile by handle and returns the associated attributes, identifiers, and traits.

        Args:
            handle (string): handle

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            voices
        """
        if handle is None:
            raise ValueError("Missing required parameter 'handle'")
        url = f"{self.base_url}/profile/{handle}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_projects(self) -> dict[str, Any]:
        """
        Retrieves a list of projects using the API defined at the "/v1/projects" endpoint via the GET method.

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Projects
        """
        url = f"{self.base_url}/v1/projects"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_project(self, default_model_id=None, default_paragraph_voice_id=None, default_title_voice_id=None, name=None) -> dict[str, Any]:
        """
        Creates a new project and returns a status message.

        Args:
            default_model_id (string): default_model_id Example: 'default_model_id'.
            default_paragraph_voice_id (string): default_paragraph_voice_id Example: 'default_paragraph_voice_id'.
            default_title_voice_id (string): default_title_voice_id Example: 'default_title_voice_id'.
            name (string): name
                Example:
                ```json
                {
                  "default_model_id": "default_model_id",
                  "default_paragraph_voice_id": "default_paragraph_voice_id",
                  "default_title_voice_id": "default_title_voice_id",
                  "name": "name"
                }
                ```

        Returns:
            dict[str, Any]: Success

        Tags:
            Projects
        """
        request_body = {
            'default_model_id': default_model_id,
            'default_paragraph_voice_id': default_paragraph_voice_id,
            'default_title_voice_id': default_title_voice_id,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/projects/add"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_by_id(self, project_id) -> dict[str, Any]:
        """
        Retrieves information for a specific project identified by `{project_id}` using the API endpoint at "/v1/projects/{project_id}" via the GET method.

        Args:
            project_id (string): project_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Projects
        """
        if project_id is None:
            raise ValueError("Missing required parameter 'project_id'")
        url = f"{self.base_url}/v1/projects/{project_id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def edit_basic_project_info(self, project_id, default_paragraph_voice_id=None, default_title_voice_id=None, name=None) -> dict[str, Any]:
        """
        Creates a new project resource by sending data to the specified project identifier using the POST method at the "/v1/projects/{project_id}" endpoint.

        Args:
            project_id (string): project_id
            default_paragraph_voice_id (string): default_paragraph_voice_id Example: 'default_paragraph_voice_id'.
            default_title_voice_id (string): default_title_voice_id Example: 'default_title_voice_id'.
            name (string): name
                Example:
                ```json
                {
                  "default_paragraph_voice_id": "default_paragraph_voice_id",
                  "default_title_voice_id": "default_title_voice_id",
                  "name": "name"
                }
                ```

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Projects
        """
        if project_id is None:
            raise ValueError("Missing required parameter 'project_id'")
        request_body = {
            'default_paragraph_voice_id': default_paragraph_voice_id,
            'default_title_voice_id': default_title_voice_id,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/projects/{project_id}"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_project(self, project_id) -> dict[str, Any]:
        """
        Deletes the specified project and returns a success status upon completion.

        Args:
            project_id (string): project_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Projects
        """
        if project_id is None:
            raise ValueError("Missing required parameter 'project_id'")
        url = f"{self.base_url}/v1/projects/{project_id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def convert_project(self, project_id) -> dict[str, Any]:
        """
        Converts a specified project identified by project_id and returns the conversion result.

        Args:
            project_id (string): project_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Projects
        """
        if project_id is None:
            raise ValueError("Missing required parameter 'project_id'")
        url = f"{self.base_url}/v1/projects/{project_id}/convert"
        query_params = {}
        response = self._post(url, data={}, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_snapshots(self, project_id) -> dict[str, Any]:
        """
        Retrieves a list of snapshots associated with a specified project.

        Args:
            project_id (string): project_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Projects
        """
        if project_id is None:
            raise ValueError("Missing required parameter 'project_id'")
        url = f"{self.base_url}/v1/projects/{project_id}/snapshots"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def streams_archive_with_project_audio(self, project_id, project_snapshot_id) -> Any:
        """
        Archives a project snapshot using the specified project ID and snapshot ID and returns a success status.

        Args:
            project_id (string): project_id
            project_snapshot_id (string): project_snapshot_id

        Returns:
            Any: Success / Success

        Tags:
            Projects
        """
        if project_id is None:
            raise ValueError("Missing required parameter 'project_id'")
        if project_snapshot_id is None:
            raise ValueError("Missing required parameter 'project_snapshot_id'")
        url = f"{self.base_url}/v1/projects/{project_id}/snapshots/{project_snapshot_id}/archive"
        query_params = {}
        response = self._post(url, data={}, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_chapter_to_aproject(self, project_id, name=None) -> dict[str, Any]:
        """
        Adds a new chapter to a specified project using the provided project identifier and returns a success status upon completion.

        Args:
            project_id (string): project_id
            name (string): name
                Example:
                ```json
                {
                  "name": "name"
                }
                ```

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Projects
        """
        if project_id is None:
            raise ValueError("Missing required parameter 'project_id'")
        request_body = {
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/projects/{project_id}/chapters/add"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_pronunciation_dictionaries(self, project_id, pronunciation_dictionary_locators=None) -> dict[str, Any]:
        """
        Updates pronunciation dictionaries for a specified project using the POST method, returning a successful status message upon completion.

        Args:
            project_id (string): project_id
            pronunciation_dictionary_locators (array): pronunciation_dictionary_locators
                Example:
                ```json
                {
                  "pronunciation_dictionary_locators": [
                    {
                      "pronunciation_dictionary_id": "pronunciation_dictionary_id",
                      "version_id": "version_id"
                    },
                    {
                      "pronunciation_dictionary_id": "pronunciation_dictionary_id",
                      "version_id": "version_id"
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Projects
        """
        if project_id is None:
            raise ValueError("Missing required parameter 'project_id'")
        request_body = {
            'pronunciation_dictionary_locators': pronunciation_dictionary_locators,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/projects/{project_id}/update-pronunciation-dictionaries"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_chapters(self, project_id) -> dict[str, Any]:
        """
        Retrieves a chapter for a specified project by ID using the GET method.

        Args:
            project_id (string): project_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Chapters
        """
        if project_id is None:
            raise ValueError("Missing required parameter 'project_id'")
        url = f"{self.base_url}/v1/projects/{project_id}/chapters"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_chapter_by_id(self, project_id, chapter_id) -> dict[str, Any]:
        """
        Retrieves a specific chapter within a project identified by project_id and chapter_id.

        Args:
            project_id (string): project_id
            chapter_id (string): chapter_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Chapters
        """
        if project_id is None:
            raise ValueError("Missing required parameter 'project_id'")
        if chapter_id is None:
            raise ValueError("Missing required parameter 'chapter_id'")
        url = f"{self.base_url}/v1/projects/{project_id}/chapters/{chapter_id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_chapter(self, project_id, chapter_id) -> dict[str, Any]:
        """
        Deletes a specific chapter within a project using the "DELETE" method.

        Args:
            project_id (string): project_id
            chapter_id (string): chapter_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Chapters
        """
        if project_id is None:
            raise ValueError("Missing required parameter 'project_id'")
        if chapter_id is None:
            raise ValueError("Missing required parameter 'chapter_id'")
        url = f"{self.base_url}/v1/projects/{project_id}/chapters/{chapter_id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def convert_chapter(self, project_id, chapter_id) -> dict[str, Any]:
        """
        Converts a chapter in a project using the POST method and returns a response upon successful conversion.

        Args:
            project_id (string): project_id
            chapter_id (string): chapter_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Chapters
        """
        if project_id is None:
            raise ValueError("Missing required parameter 'project_id'")
        if chapter_id is None:
            raise ValueError("Missing required parameter 'chapter_id'")
        url = f"{self.base_url}/v1/projects/{project_id}/chapters/{chapter_id}/convert"
        query_params = {}
        response = self._post(url, data={}, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_chapter_snapshots(self, project_id, chapter_id) -> dict[str, Any]:
        """
        Retrieves a snapshot for a specific chapter within a project using the provided project and chapter IDs.

        Args:
            project_id (string): project_id
            chapter_id (string): chapter_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Chapters
        """
        if project_id is None:
            raise ValueError("Missing required parameter 'project_id'")
        if chapter_id is None:
            raise ValueError("Missing required parameter 'chapter_id'")
        url = f"{self.base_url}/v1/projects/{project_id}/chapters/{chapter_id}/snapshots"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def dub_avideo_or_an_audio_file(self, target_lang=None) -> dict[str, Any]:
        """
        Initiates a dubbing process and returns a status message using the API defined at the "/v1/dubbing" endpoint via the POST method.

        Args:
            target_lang (string): target_lang
                Example:
                ```json
                {
                  "target_lang": "target_lang"
                }
                ```

        Returns:
            dict[str, Any]: Success

        Tags:
            Dubbing
        """
        request_body = {
            'target_lang': target_lang,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/dubbing"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_dubbing_project_metadata(self, dubbing_id) -> dict[str, Any]:
        """
        Retrieves the details of a specific dubbing job using the provided dubbing ID.

        Args:
            dubbing_id (string): dubbing_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Dubbing
        """
        if dubbing_id is None:
            raise ValueError("Missing required parameter 'dubbing_id'")
        url = f"{self.base_url}/v1/dubbing/{dubbing_id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_dubbing_project(self, dubbing_id) -> dict[str, Any]:
        """
        Deletes a dubbing project with the specified ID and returns a success status upon completion.

        Args:
            dubbing_id (string): dubbing_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Dubbing
        """
        if dubbing_id is None:
            raise ValueError("Missing required parameter 'dubbing_id'")
        url = f"{self.base_url}/v1/dubbing/{dubbing_id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_transcript_for_dub(self, dubbing_id, language_code) -> dict[str, Any]:
        """
        Retrieves the transcript for a specific dubbing task in the requested language using the "GET" method.

        Args:
            dubbing_id (string): dubbing_id
            language_code (string): language_code

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Dubbing
        """
        if dubbing_id is None:
            raise ValueError("Missing required parameter 'dubbing_id'")
        if language_code is None:
            raise ValueError("Missing required parameter 'language_code'")
        url = f"{self.base_url}/v1/dubbing/{dubbing_id}/transcript/{language_code}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_models(self) -> list[Any]:
        """
        Retrieves a list of models using the GET method at the "/v1/models" endpoint.

        Returns:
            list[Any]: Success / Success

        Tags:
            Models
        """
        url = f"{self.base_url}/v1/models"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def creates_audionative_enabled_project(self, name=None) -> dict[str, Any]:
        """
        Processes audio data using the audio-native API and returns a response.

        Args:
            name (string): name
                Example:
                ```json
                {
                  "name": "name"
                }
                ```

        Returns:
            dict[str, Any]: Success

        Tags:
            Audio Native
        """
        request_body = {
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/audio-native"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_characters_usage_metrics(self, start_unix=None, end_unix=None) -> dict[str, Any]:
        """
        Retrieves character statistics within a specified time frame using the start and end Unix timestamps provided in the query parameters.

        Args:
            start_unix (string): UTC Unix timestamp for the start of the usage window, in milliseconds. To include the first day of the window, the timestamp should be at 00:00:00 of that day. Example: '1'.
            end_unix (string): UTC Unix timestamp for the end of the usage window, in milliseconds. To include the last day of the window, the timestamp should be at 23:59:59 of that day. Example: '1'.

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Usage
        """
        url = f"{self.base_url}/v1/usage/character-stats"
        query_params = {k: v for k, v in [('start_unix', start_unix), ('end_unix', end_unix)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_apronunciation_dictionary(self, name=None) -> dict[str, Any]:
        """
        Creates a pronunciation dictionary from a lexicon file and returns its ID and metadata.

        Args:
            name (string): name
                Example:
                ```json
                {
                  "name": "name"
                }
                ```

        Returns:
            dict[str, Any]: Success

        Tags:
            Pronunciation Dictionary
        """
        request_body = {
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/pronunciation-dictionaries/add-from-file"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_rules_to_the_pronunciation_dictionary(self, pronunciation_dictionary_id, rules=None) -> dict[str, Any]:
        """
        Adds pronunciation rules to a specific pronunciation dictionary identified by its ID using the POST method.

        Args:
            pronunciation_dictionary_id (string): pronunciation_dictionary_id
            rules (array): rules
                Example:
                ```json
                {
                  "rules": [
                    {
                      "alias": "alias",
                      "string_to_replace": "string_to_replace",
                      "type": "alias"
                    },
                    {
                      "alias": "alias",
                      "string_to_replace": "string_to_replace",
                      "type": "alias"
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Pronunciation Dictionary
        """
        if pronunciation_dictionary_id is None:
            raise ValueError("Missing required parameter 'pronunciation_dictionary_id'")
        request_body = {
            'rules': rules,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/pronunciation-dictionaries/{pronunciation_dictionary_id}/add-rules"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_rules_from_the_pronunciation_dictionary(self, pronunciation_dictionary_id, rule_strings=None) -> dict[str, Any]:
        """
        Removes specified pronunciation rules from a pronunciation dictionary using a POST request.

        Args:
            pronunciation_dictionary_id (string): pronunciation_dictionary_id
            rule_strings (array): rule_strings
                Example:
                ```json
                {
                  "rule_strings": [
                    "rule_strings",
                    "rule_strings"
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Pronunciation Dictionary
        """
        if pronunciation_dictionary_id is None:
            raise ValueError("Missing required parameter 'pronunciation_dictionary_id'")
        request_body = {
            'rule_strings': rule_strings,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/pronunciation-dictionaries/{pronunciation_dictionary_id}/remove-rules"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_pls_file_with_apronunciation_dictionary_version_rules(self, dictionary_id, version_id) -> Any:
        """
        Retrieves and downloads a specific version of a pronunciation dictionary file using its dictionary ID and version ID.

        Args:
            dictionary_id (string): dictionary_id
            version_id (string): version_id

        Returns:
            Any: Success

        Tags:
            Pronunciation Dictionary
        """
        if dictionary_id is None:
            raise ValueError("Missing required parameter 'dictionary_id'")
        if version_id is None:
            raise ValueError("Missing required parameter 'version_id'")
        url = f"{self.base_url}/v1/pronunciation-dictionaries/{dictionary_id}/{version_id}/download"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_metadata_for_apronunciation_dictionary(self, pronunciation_dictionary_id) -> dict[str, Any]:
        """
        Retrieves a specific pronunciation dictionary by its ID using the "GET" method from the "/v1/pronunciation-dictionaries/{pronunciation_dictionary_id}" endpoint.

        Args:
            pronunciation_dictionary_id (string): pronunciation_dictionary_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Pronunciation Dictionary
        """
        if pronunciation_dictionary_id is None:
            raise ValueError("Missing required parameter 'pronunciation_dictionary_id'")
        url = f"{self.base_url}/v1/pronunciation-dictionaries/{pronunciation_dictionary_id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_pronunciation_dictionaries(self, page_size=None) -> dict[str, Any]:
        """
        Retrieves a list of pronunciation dictionaries using the GET method at the "/v1/pronunciation-dictionaries" endpoint, allowing users to specify the number of items per page via the "page_size" query parameter.

        Args:
            page_size (string): How many pronunciation dictionaries to return at maximum. Can not exceed 100, defaults to 30. Example: '1'.

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Pronunciation Dictionary
        """
        url = f"{self.base_url}/v1/pronunciation-dictionaries"
        query_params = {k: v for k, v in [('page_size', page_size)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def invite_user(self, email=None) -> dict[str, Any]:
        """
        Invites a user to join a workspace by sending an invitation, allowing them to access the specified workspace upon acceptance.

        Args:
            email (string): email
                Example:
                ```json
                {
                  "email": "email"
                }
                ```

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Workspace
        """
        request_body = {
            'email': email,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/workspace/invites/add"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_existing_invitation(self, email=None) -> dict[str, Any]:
        """
        Deletes a workspace invite and returns a success response upon completion.

        Args:
            email (string): email
                Example:
                ```json
                {
                  "email": "email"
                }
                ```

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Workspace
        """
        request_body = {
            'email': email,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/workspace/invites"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_member(self, email=None) -> dict[str, Any]:
        """
        Adds members to a workspace and returns the updated member list upon success.

        Args:
            email (string): email
                Example:
                ```json
                {
                  "email": "email"
                }
                ```

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Workspace
        """
        request_body = {
            'email': email,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/workspace/members"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_signed_url(self, agent_id=None) -> dict[str, Any]:
        """
        Generates a signed URL for initiating a conversation with a specific conversational AI agent, identified by the provided `agent_id`, using the ElevenLabs API.

        Args:
            agent_id (string): The id of the agent you're taking the action on. Example: '21m00Tcm4TlvDq8ikWAM'.

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Conversational Ai
        """
        url = f"{self.base_url}/v1/convai/conversation/get_signed_url"
        query_params = {k: v for k, v in [('agent_id', agent_id)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_agent(self, conversation_config=None) -> dict[str, Any]:
        """
        Creates a conversational AI agent with specified configuration settings and returns the agent details.

        Args:
            conversation_config (object): conversation_config
                Example:
                ```json
                {
                  "conversation_config": {}
                }
                ```

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Conversational Ai
        """
        request_body = {
            'conversation_config': conversation_config,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/convai/agents/create"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_agent(self, agent_id) -> dict[str, Any]:
        """
        Retrieves information about a specific conversational AI agent by its unique identifier using the GET method at the "/v1/convai/agents/{agent_id}" API endpoint.

        Args:
            agent_id (string): agent_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Conversational Ai
        """
        if agent_id is None:
            raise ValueError("Missing required parameter 'agent_id'")
        url = f"{self.base_url}/v1/convai/agents/{agent_id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_agent(self, agent_id) -> dict[str, Any]:
        """
        Deletes a specified Conversational AI agent using the DELETE method.

        Args:
            agent_id (string): agent_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Conversational Ai
        """
        if agent_id is None:
            raise ValueError("Missing required parameter 'agent_id'")
        url = f"{self.base_url}/v1/convai/agents/{agent_id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_agent_widget_config(self, agent_id) -> dict[str, Any]:
        """
        Retrieves and configures the Convai widget for the specified agent, but the provided details do not specify the exact functionality of this specific endpoint, suggesting it may relate to integrating or customizing Convai's character interaction capabilities.

        Args:
            agent_id (string): agent_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Conversational Ai
        """
        if agent_id is None:
            raise ValueError("Missing required parameter 'agent_id'")
        url = f"{self.base_url}/v1/convai/agents/{agent_id}/widget"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_shareable_agent_link(self, agent_id) -> dict[str, Any]:
        """
        Retrieves and establishes a link for a Convai agent using the specified agent ID, facilitating integration or connectivity operations.

        Args:
            agent_id (string): agent_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Conversational Ai
        """
        if agent_id is None:
            raise ValueError("Missing required parameter 'agent_id'")
        url = f"{self.base_url}/v1/convai/agents/{agent_id}/link"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()



    def get_documentation_from_agent_sknowledge_base(self, agent_id, documentation_id) -> dict[str, Any]:
        """
        Retrieves specific documentation for a knowledge base associated with an agent in Convai.

        Args:
            agent_id (string): agent_id
            documentation_id (string): documentation_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Conversational Ai
        """
        if agent_id is None:
            raise ValueError("Missing required parameter 'agent_id'")
        if documentation_id is None:
            raise ValueError("Missing required parameter 'documentation_id'")
        url = f"{self.base_url}/v1/convai/agents/{agent_id}/knowledge-base/{documentation_id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_asecret_to_the_agent_which_can_be_referenced_in_tool_calls(self, agent_id, name=None, secret_value=None) -> dict[str, Any]:
        """
        Adds a secret to a specified conversational AI agent through the API and returns a status confirmation.

        Args:
            agent_id (string): agent_id
            name (string): name Example: 'name'.
            secret_value (string): secret_value
                Example:
                ```json
                {
                  "name": "name",
                  "secret_value": "secret_value"
                }
                ```

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Conversational Ai
        """
        if agent_id is None:
            raise ValueError("Missing required parameter 'agent_id'")
        request_body = {
            'name': name,
            'secret_value': secret_value,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1/convai/agents/{agent_id}/add-secret"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_agents_page(self) -> dict[str, Any]:
        """
        Retrieves a list of conversational AI agents available in the Convai system.

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Conversational Ai
        """
        url = f"{self.base_url}/v1/convai/agents"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_conversations(self, agent_id=None) -> dict[str, Any]:
        """
        Retrieves conversation history for a specified agent ID.

        Args:
            agent_id (string): The id of the agent you're taking the action on. Example: '21m00Tcm4TlvDq8ikWAM'.

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Conversational Ai
        """
        url = f"{self.base_url}/v1/convai/conversations"
        query_params = {k: v for k, v in [('agent_id', agent_id)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_conversation_details(self, conversation_id) -> dict[str, Any]:
        """
        Retrieves and formats the details of a specific conversation based on the provided conversation ID.

        Args:
            conversation_id (string): conversation_id

        Returns:
            dict[str, Any]: Success / Success

        Tags:
            Conversational Ai
        """
        if conversation_id is None:
            raise ValueError("Missing required parameter 'conversation_id'")
        url = f"{self.base_url}/v1/convai/conversations/{conversation_id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_conversation_audio(self, conversation_id) -> Any:
        """
        Retrieves the audio from a specific conversation using the ElevenLabs Conversational AI API.

        Args:
            conversation_id (string): conversation_id

        Returns:
            Any: Success / Success

        Tags:
            Conversational Ai
        """
        if conversation_id is None:
            raise ValueError("Missing required parameter 'conversation_id'")
        url = f"{self.base_url}/v1/convai/conversations/{conversation_id}/audio"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_tools(self):
        return [
            self.get_generated_items,
            self.get_history_item_by_id,
            self.delete_history_item,
            self.get_audio_from_history_item,
            self.download_history_items,
            self.delete_sample,
            self.get_audio_from_sample,
            self.convert,
            self.text_to_speech_with_timestamps,
            self.convert_as_stream,
            self.text_to_speech_streaming_with_timestamps,
            self.voice_generation_parameters,
            self.generate_arandom_voice,
            self.create_apreviously_generated_voice,
            self.generate_avoice_preview_from_description,
            self.create_anew_voice_from_voice_preview,
            self.get_user_subscription_info,
            self.get_user_info,
            self.get_voices,
            self.get_default_voice_settings,
            self.get_voice_settings,
            self.get_voice,
            self.delete_voice,
            self.add_voice,
            self.edit_voice,
            self.add_sharing_voice,
            self.get_shared_voices,
            self.get_aprofile_page,
            self.get_projects,
            self.add_project,
            self.get_project_by_id,
            self.edit_basic_project_info,
            self.delete_project,
            self.convert_project,
            self.get_project_snapshots,
            self.streams_archive_with_project_audio,
            self.add_chapter_to_aproject,
            self.update_pronunciation_dictionaries,
            self.get_chapters,
            self.get_chapter_by_id,
            self.delete_chapter,
            self.convert_chapter,
            self.get_chapter_snapshots,
            self.dub_avideo_or_an_audio_file,
            self.get_dubbing_project_metadata,
            self.delete_dubbing_project,
            self.get_transcript_for_dub,
            self.get_models,
            self.creates_audionative_enabled_project,
            self.get_characters_usage_metrics,
            self.add_apronunciation_dictionary,
            self.add_rules_to_the_pronunciation_dictionary,
            self.remove_rules_from_the_pronunciation_dictionary,
            self.get_pls_file_with_apronunciation_dictionary_version_rules,
            self.get_metadata_for_apronunciation_dictionary,
            self.get_pronunciation_dictionaries,
            self.invite_user,
            self.delete_existing_invitation,
            self.update_member,
            self.get_signed_url,
            self.create_agent,
            self.get_agent,
            self.delete_agent,
            self.get_agent_widget_config,
            self.get_shareable_agent_link,
            self.get_documentation_from_agent_sknowledge_base,
            self.add_asecret_to_the_agent_which_can_be_referenced_in_tool_calls,
            self.get_agents_page,
            self.get_conversations,
            self.get_conversation_details,
            self.get_conversation_audio
        ]
