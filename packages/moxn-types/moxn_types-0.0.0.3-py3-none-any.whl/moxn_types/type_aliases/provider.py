from typing import Sequence

from moxn_types.type_aliases.anthropic import AnthropicContentBlock
from moxn_types.type_aliases.google import GoogleContentBlock
from moxn_types.type_aliases.openai_chat import OpenAIChatContentBlock

ProviderContentBlock = (
    AnthropicContentBlock | OpenAIChatContentBlock | GoogleContentBlock
)


ProviderContentBlockSequence = (
    Sequence[Sequence[AnthropicContentBlock]]
    | Sequence[Sequence[OpenAIChatContentBlock]]
    | Sequence[Sequence[GoogleContentBlock]]
)
