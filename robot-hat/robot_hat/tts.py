from .basic import _Basic_class
from .utils import is_installed, run_command
from .music import Music
from distutils.spawn import find_executable

class TTS(_Basic_class):
    """Text to speech class"""
    _class_name = 'TTS'
    SUPPORTED_LANGUAGES = [
        'en-US',
        'en-GB',
        'de-DE',
        'es-ES',
        'fr-FR',
        'it-IT',
        'vi-VN'  # Added support for Vietnamese
    ]

    ESPEAK = 'espeak'
    """espeak TTS engine"""

    def __init__(self, engine=ESPEAK, lang='en-US', *args, **kwargs):
        """
        Initialize TTS class.

        :param engine: TTS engine (default is espeak)
        :type engine: str
        :param lang: Language for TTS
        :type lang: str
        """
        super().__init__()
        self.engine = engine
        self._lang = lang if lang in self.SUPPORTED_LANGUAGES else 'en-US'

        if not is_installed(self.ESPEAK):
            raise Exception(f"TTS engine: {self.ESPEAK} is not installed.")

        self._amp = 100
        self._speed = 175
        self._gap = 5
        self._pitch = 50

    def _check_executable(self, executable):
        executable_path = find_executable(executable)
        return executable_path is not None

    def say(self, words):
        """
        Say words.

        :param words: Words to say.
        :type words: str
        """
        self.espeak(words)

    def espeak(self, words):
        """
        Say words with espeak.

        :param words: Words to say.
        :type words: str
        """
        self._debug(f'espeak: [{words}]')
        if not self._check_executable(self.ESPEAK):
            raise Exception(f"{self.ESPEAK} is not available on the system.")

        cmd = (
            f'{self.ESPEAK} -a{self._amp} -s{self._speed} -g{self._gap} -p{self._pitch} '
            f'-v {self._lang} "{words}" --stdout | aplay 2>/dev/null &'
        )
        status, result = run_command(cmd)
        if len(result) != 0:
            raise Exception(f'TTS-espeak:
\t{result}')
        self._debug(f'command: {cmd}')

    def lang(self, *value):
        """
        Set/get language. Leave empty to get the current language.

        :param value: Language.
        :type value: str
        """
        if len(value) == 0:
            return self._lang
        elif len(value) == 1:
            v = value[0]
            if v in self.SUPPORTED_LANGUAGES:
                self._lang = v
                return self._lang
        raise ValueError(
            f'Argument "{value}" is not supported. Run tts.supported_lang to get supported language types.'
        )

    def supported_lang(self):
        """
        Get supported languages.

        :return: Supported languages.
        :rtype: list
        """
        return self.SUPPORTED_LANGUAGES

    def espeak_params(self, amp=None, speed=None, gap=None, pitch=None):
        """
        Set espeak parameters.

        :param amp: Amplitude.
        :type amp: int
        :param speed: Speed.
        :type speed: int
        :param gap: Gap.
        :type gap: int
        :param pitch: Pitch.
        :type pitch: int
        """
        self._amp = amp if amp is not None else self._amp
        self._speed = speed if speed is not None else self._speed
        self._gap = gap if gap is not None else self._gap
        self._pitch = pitch if pitch is not None else self._pitch

        if not (0 <= self._amp <= 200):
            raise ValueError(f'Amp should be in 0 to 200, not "{self._amp}"')
        if not (80 <= self._speed <= 260):
            raise ValueError(f'Speed should be in 80 to 260, not "{self._speed}"')
        if not (0 <= self._pitch <= 99):
            raise ValueError(f'Pitch should be in 0 to 99, not "{self._pitch}"')
